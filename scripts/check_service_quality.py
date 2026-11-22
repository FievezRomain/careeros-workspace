"""Validate the deterministic CareerOS Python service baseline."""

from __future__ import annotations

import argparse
import ast
import re
import sys
import tomllib
from pathlib import Path

LOCKFILES = ("uv.lock", "poetry.lock", "pdm.lock")
LAYOUT_KEYS = ("domain", "application", "ports", "adapters", "composition_root")
TEST_KEYS = ("unit", "integration", "contract", "health", "logging", "security")
COMMAND_KEYS = ("format", "lint", "type", "test", "secret", "security")
FRAMEWORK_PARTS = {
    "aio_pika", "alembic", "boto3", "fastapi", "keycloak", "pika",
    "sqlalchemy", "starlette",
}


def _dependency_names(values: list[str]) -> set[str]:
    return {re.split(r"[<>=!~\s\[]", value, 1)[0].lower() for value in values}


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def check_service(root: Path) -> list[str]:
    errors: list[str] = []
    pyproject = root / "pyproject.toml"
    if not pyproject.is_file():
        return ["pyproject.toml is required"]
    try:
        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        return [f"pyproject.toml cannot be read: {exc}"]

    project = data.get("project", {})
    requires_python = project.get("requires-python", "")
    if not re.search(r"(?:>=|~=|==)\s*3\.14", requires_python):
        errors.append("project.requires-python must pin Python 3.14")
    dependency_values = project.get("dependencies", [])
    dependencies = _dependency_names(dependency_values)
    for dependency in ("pydantic", "pydantic-settings"):
        if dependency not in dependencies:
            errors.append(f"project.dependencies must include {dependency}")
    pydantic_spec = next(
        (value for value in dependency_values if _dependency_names([value]) == {"pydantic"}), ""
    )
    if not re.search(r"(?:(?:==|~=)\s*2|>=\s*2.*<\s*3)", pydantic_spec):
        errors.append("Pydantic must be constrained to v2")
    runtime = root / ".python-version"
    if not runtime.is_file() or not runtime.read_text(encoding="utf-8").strip().startswith("3.14"):
        errors.append(".python-version must pin Python 3.14")
    if not any((root / name).is_file() for name in LOCKFILES):
        errors.append("a deterministic lockfile is required (uv.lock, poetry.lock or pdm.lock)")

    quality = data.get("tool", {}).get("careeros", {}).get("quality", {})
    package_value = quality.get("package")
    package = root / package_value if isinstance(package_value, str) else None
    if package is None or not package.is_dir():
        errors.append("tool.careeros.quality.package must name an existing package directory")

    paths: dict[str, Path] = {}
    for key in LAYOUT_KEYS:
        value = quality.get(key)
        path = root / value if isinstance(value, str) else None
        if path is None or not path.exists():
            errors.append(f"tool.careeros.quality.{key} must name an existing path")
        else:
            paths[key] = path

    commands = quality.get("commands", {})
    required_commands = list(COMMAND_KEYS)
    persistence = quality.get("persistence")
    if not isinstance(persistence, bool):
        errors.append("tool.careeros.quality.persistence must be true or false")
    elif persistence:
        required_commands.extend(("migrate_up", "migrate_down"))
    for key in required_commands:
        if not isinstance(commands.get(key), str) or not commands[key].strip():
            errors.append(f"tool.careeros.quality.commands.{key} is required")
    if "bandit" not in commands.get("security", "") or "pip-audit" not in commands.get("security", ""):
        errors.append("security command must run both bandit and pip-audit")
    if "gitleaks" not in commands.get("secret", ""):
        errors.append("secret command must run gitleaks")
    if not data.get("tool", {}).get("mypy", {}).get("strict", False):
        errors.append("tool.mypy.strict must be true")

    logging = quality.get("logging", {})
    for key in ("structured", "correlation", "redaction"):
        if logging.get(key) is not True:
            errors.append(f"tool.careeros.quality.logging.{key} must be true")

    evidence = quality.get("evidence", {})
    for key in TEST_KEYS:
        value = evidence.get(key)
        path = root / value if isinstance(value, str) else None
        if path is None or not path.exists():
            errors.append(f"tool.careeros.quality.evidence.{key} must name existing test evidence")
    if persistence:
        migration_evidence = evidence.get("migrations")
        path = root / migration_evidence if isinstance(migration_evidence, str) else None
        if path is None or not path.exists():
            errors.append("tool.careeros.quality.evidence.migrations must prove apply and rollback")

    if package and package.is_dir():
        python_files = list(package.rglob("*.py"))
        adapter_files = list(paths.get("adapters", package / "__missing__").rglob("*.py"))
        port_files = list(paths.get("ports", package / "__missing__").rglob("*.py"))
        if not any("pydantic" in _imports(path) for path in adapter_files):
            errors.append("adapter boundaries must contain Pydantic v2 models")
        if not any("pydantic" in _imports(path) for path in port_files):
            errors.append("application ports must contain Pydantic v2 models")
        if not any("pydantic_settings" in _imports(path) for path in python_files):
            errors.append("service configuration must use pydantic-settings")
        for path in adapter_files:
            source = path.read_text(encoding="utf-8")
            if re.search(r"(?:@dataclass|from\s+dataclasses\s+import)", source):
                errors.append(f"{path.relative_to(root)}: boundary data must use Pydantic, not dataclasses")

        layers = (("domain", {"application", "adapters"}), ("application", {"adapters"}))
        for layer, forbidden_layers in layers:
            layer_path = paths.get(layer)
            if not layer_path:
                continue
            for path in layer_path.rglob("*.py"):
                try:
                    imports = _imports(path)
                except SyntaxError as exc:
                    errors.append(f"{path.relative_to(root)}: invalid Python: {exc.msg}")
                    continue
                for imported in imports:
                    parts = set(imported.split("."))
                    forbidden = (parts & FRAMEWORK_PARTS) | (parts & forbidden_layers)
                    if forbidden:
                        errors.append(
                            f"{path.relative_to(root)}: inward layer imports forbidden dependency "
                            f"{imported}"
                        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("service", type=Path)
    args = parser.parse_args()
    errors = check_service(args.service.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("CareerOS service quality baseline: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
