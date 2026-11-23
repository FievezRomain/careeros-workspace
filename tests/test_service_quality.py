import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parents[1]))
from scripts.check_service_quality import check_service


PYPROJECT = """
[project]
name = "example-service"
version = "0.1.0"
requires-python = ">=3.14,<3.15"
dependencies = ["pydantic>=2,<3", "pydantic-settings>=2,<3"]

[tool.mypy]
strict = true

[tool.careeros.quality]
package = "src/example"
persistence = true
domain = "src/example/domain"
application = "src/example/application"
ports = "src/example/ports"
adapters = "src/example/adapters"
composition_root = "src/example/bootstrap.py"
migrations = "src/example/adapters/migrations"
migration_runner = "src/example/adapters/migrations/runner.py"

[tool.careeros.quality.commands]
format = "ruff format --check ."
lint = "ruff check ."
type = "mypy src tests"
test = "pytest"
security = "pip-audit && bandit -r src"
secret = "gitleaks detect --redact --no-banner"
migrate_up = "alembic upgrade head"
migrate_down = "alembic downgrade -1"

[tool.careeros.quality.logging]
structured = true
correlation = true
redaction = true

[tool.careeros.quality.evidence]
unit = "tests/unit"
integration = "tests/integration"
contract = "tests/contract"
health = "tests/integration/test_health.py"
logging = "tests/unit/test_logging.py"
security = "tests/integration/test_authorization.py"
migrations = "tests/integration/test_migrations.py"
startup_migrations = "tests/integration/test_startup_migrations.py"
"""


class ServiceQualityTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "pyproject.toml").write_text(PYPROJECT, encoding="utf-8")
        (self.root / "uv.lock").touch()
        (self.root / ".python-version").write_text("3.14\n", encoding="utf-8")
        for directory in (
            "src/example/domain", "src/example/application", "src/example/ports",
            "src/example/adapters/migrations", "tests/unit", "tests/integration", "tests/contract",
        ):
            (self.root / directory).mkdir(parents=True)
        files = {
            "src/example/bootstrap.py": "from pydantic_settings import BaseSettings\n",
            "src/example/domain/model.py": "class Profile: pass\n",
            "src/example/application/use_case.py": "from example.domain import model\n",
            "src/example/ports/commands.py": "from pydantic import BaseModel\nclass Command(BaseModel): pass\n",
            "src/example/adapters/api.py": "from pydantic import BaseModel\nclass Input(BaseModel): pass\n",
            "src/example/adapters/migrations/runner.py": "class MigrationRunner: pass\n",
            "tests/integration/test_health.py": "# readiness test\n",
            "tests/unit/test_logging.py": "# redaction and correlation test\n",
            "tests/integration/test_authorization.py": "# authorization test\n",
            "tests/integration/test_migrations.py": "# apply and rollback test\n",
            "tests/integration/test_startup_migrations.py": "# startup enforcement test\n",
        }
        for name, content in files.items():
            (self.root / name).write_text(content, encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_accepts_complete_python_service(self) -> None:
        self.assertEqual([], check_service(self.root))

    def test_reports_missing_runtime_dependency_and_lockfile(self) -> None:
        pyproject = (self.root / "pyproject.toml").read_text(encoding="utf-8")
        pyproject = pyproject.replace(">=3.14,<3.15", ">=3.13").replace(
            '"pydantic-settings>=2,<3"', '"httpx"'
        )
        (self.root / "pyproject.toml").write_text(pyproject, encoding="utf-8")
        (self.root / "uv.lock").unlink()
        (self.root / ".python-version").unlink()
        errors = check_service(self.root)
        self.assertTrue(any("Python 3.14" in error for error in errors))
        self.assertTrue(any("pydantic-settings" in error for error in errors))
        self.assertTrue(any("lockfile" in error for error in errors))
        self.assertTrue(any(".python-version" in error for error in errors))

    def test_rejects_outward_import_from_inward_layer(self) -> None:
        path = self.root / "src/example/domain/model.py"
        path.write_text("from example.adapters import api\n", encoding="utf-8")
        self.assertTrue(any("forbidden dependency" in error for error in check_service(self.root)))

    def test_requires_pydantic_boundaries_and_settings(self) -> None:
        (self.root / "src/example/adapters/api.py").write_text("class Input: pass\n", encoding="utf-8")
        (self.root / "src/example/bootstrap.py").write_text("# composition root\n", encoding="utf-8")
        errors = check_service(self.root)
        self.assertTrue(any("Pydantic v2" in error for error in errors))
        self.assertTrue(any("pydantic-settings" in error for error in errors))

    def test_requires_declared_operational_evidence(self) -> None:
        (self.root / "tests/contract").rmdir()
        (self.root / "tests/integration/test_health.py").unlink()
        (self.root / "tests/unit/test_logging.py").unlink()
        errors = check_service(self.root)
        self.assertTrue(any("evidence.health" in error for error in errors))
        self.assertTrue(any("evidence.logging" in error for error in errors))
        self.assertTrue(any("evidence.contract" in error for error in errors))

    def test_requires_adapter_owned_migrations_and_startup_runner_evidence(self) -> None:
        pyproject = (self.root / "pyproject.toml").read_text(encoding="utf-8")
        pyproject = pyproject.replace(
            'migrations = "src/example/adapters/migrations"', 'migrations = "migrations"'
        ).replace(
            'migration_runner = "src/example/adapters/migrations/runner.py"',
            'migration_runner = "migrations/runner.py"',
        )
        (self.root / "pyproject.toml").write_text(pyproject, encoding="utf-8")
        (self.root / "migrations").mkdir()
        (self.root / "migrations/runner.py").touch()
        (self.root / "tests/integration/test_startup_migrations.py").unlink()

        errors = check_service(self.root)

        self.assertTrue(any("inside the adapters" in error for error in errors))
        self.assertTrue(any("not repository-root" in error for error in errors))
        self.assertTrue(any("startup_migrations" in error for error in errors))

    def test_rejects_unsafe_logging_and_security_configuration(self) -> None:
        pyproject = (self.root / "pyproject.toml").read_text(encoding="utf-8")
        pyproject = pyproject.replace("correlation = true", "correlation = false")
        pyproject = pyproject.replace("pip-audit && bandit -r src", "echo skipped")
        (self.root / "pyproject.toml").write_text(pyproject, encoding="utf-8")
        errors = check_service(self.root)
        self.assertTrue(any("logging.correlation" in error for error in errors))
        self.assertTrue(any("bandit and pip-audit" in error for error in errors))

    def test_cli_returns_non_zero_with_actionable_output(self) -> None:
        (self.root / "uv.lock").unlink()
        result = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).parents[1] / "scripts/check_service_quality.py"),
                str(self.root),
            ],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(1, result.returncode)
        self.assertIn("ERROR: a deterministic lockfile is required", result.stderr)


if __name__ == "__main__":
    unittest.main()
