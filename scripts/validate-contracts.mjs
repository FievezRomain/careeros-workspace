import { execFileSync, spawnSync } from "node:child_process";
import { existsSync, readFileSync, readdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { DiagnosticSeverity, Parser } from "@asyncapi/parser";
import Ajv2020 from "ajv/dist/2020.js";
import YAML from "yaml";

const WORKSPACE = path.resolve(fileURLToPath(new URL("..", import.meta.url)));
const REDOCLY = path.join(WORKSPACE, "node_modules", "@redocly", "cli", "bin", "cli.js");
const FORMATS = {
  openapi: new Set([".json", ".yaml", ".yml"]),
  asyncapi: new Set([".json", ".yaml", ".yml"]),
  "json-schema": new Set([".json"]),
};
const STRUCTURAL_MAPS = new Set([
  "channels", "content", "messages", "operations", "paths", "properties",
  "responses", "schemas", "securitySchemes",
]);
const HTTP_METHODS = new Set(["delete", "get", "head", "options", "patch", "post", "put", "trace"]);
const STABLE_VALUES = new Set(["$ref", "action", "address", "const", "format", "type"]);

function filesUnder(directory, extensions) {
  if (!existsSync(directory)) return [];
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const target = path.join(directory, entry.name);
    if (entry.isDirectory()) return filesUnder(target, extensions);
    return extensions.has(path.extname(entry.name)) ? [target] : [];
  });
}

function parse(text, filename) {
  try {
    return YAML.parse(text);
  } catch (error) {
    throw new Error(`${filename}: ${error.message}`);
  }
}

function assertLocalRefs(value, filename, contractRoot, seen = new WeakSet()) {
  if (!value || typeof value !== "object") return;
  if (seen.has(value)) return;
  seen.add(value);
  for (const [key, child] of Object.entries(value)) {
    if (key === "$ref" && typeof child === "string") {
      const reference = child.split("#", 1)[0];
      const target = path.resolve(path.dirname(filename), reference);
      const root = path.resolve(contractRoot);
      const outsideRoot = reference && target !== root && !target.startsWith(`${root}${path.sep}`);
      if (/^[a-z][a-z\d+.-]*:/i.test(reference) || reference.startsWith("//") || outsideRoot) {
        throw new Error(`${filename}: $ref must resolve inside the contracts directory`);
      }
    }
    assertLocalRefs(child, filename, contractRoot, seen);
  }
}

async function validateFile(family, filename, contractRoot) {
  const document = parse(readFileSync(filename, "utf8"), filename);
  assertLocalRefs(document, filename, contractRoot);
  if (family === "openapi") {
    if (document?.openapi !== "3.1.2") throw new Error(`${filename}: openapi must be 3.1.2`);
    const result = spawnSync(process.execPath, [REDOCLY, "lint", filename], { encoding: "utf8" });
    if (result.status !== 0) throw new Error(`${filename}: ${result.stdout}${result.stderr}`);
  } else if (family === "asyncapi") {
    if (document?.asyncapi !== "3.1.0") throw new Error(`${filename}: asyncapi must be 3.1.0`);
    const result = await new Parser().parse(document);
    const errors = result.diagnostics.filter((item) => item.severity === DiagnosticSeverity.Error);
    if (!result.document || errors.length) {
      throw new Error(`${filename}: ${errors.map((item) => item.message).join("; ")}`);
    }
  } else {
    if (document?.$schema !== "https://json-schema.org/draft/2020-12/schema") {
      throw new Error(`${filename}: $schema must select JSON Schema 2020-12`);
    }
    if (!document.$id || !/v\d+/i.test(path.basename(filename)) || !/v\d+/i.test(document.$id)) {
      throw new Error(`${filename}: filename and $id must contain the major version`);
    }
    new Ajv2020({ allErrors: true, strict: true }).compile(document);
  }
}

export function breakingChanges(before, after, location = "$") {
  const findings = [];
  if (Array.isArray(before) && Array.isArray(after)) {
    if (location.endsWith(".required")) {
      for (const value of after) if (!before.includes(value)) findings.push(`${location}: required ${value} added`);
    }
    if (location.endsWith(".enum")) {
      for (const value of before) if (!after.includes(value)) findings.push(`${location}: enum value ${value} removed`);
    }
    return findings;
  }
  if (!before || !after || typeof before !== "object" || typeof after !== "object") {
    const key = location.split(".").at(-1);
    if (STABLE_VALUES.has(key) && before !== after) findings.push(`${location}: changed from ${before} to ${after}`);
    return findings;
  }

  const key = location.split(".").at(-1);
  if (STRUCTURAL_MAPS.has(key)) {
    for (const name of Object.keys(before)) {
      if (!(name in after)) findings.push(`${location}.${name}: removed`);
    }
  }
  if (location.startsWith("$.paths.") && location.split(".").length === 3) {
    for (const method of HTTP_METHODS) {
      if (method in before && !(method in after)) findings.push(`${location}.${method}: operation removed`);
    }
  }
  for (const name of Object.keys(before)) {
    if (name in after) findings.push(...breakingChanges(before[name], after[name], `${location}.${name}`));
  }
  return findings;
}

function compatibilityFailures(base, contractRoot) {
  if (!base || /^0+$/.test(base)) return [];
  const relativeRoot = path.relative(WORKSPACE, contractRoot).replaceAll("\\", "/");
  const output = execFileSync(
    "git", ["diff", "--name-status", "--no-renames", "--diff-filter=MD", `${base}...HEAD`, "--", relativeRoot],
    { cwd: WORKSPACE, encoding: "utf8" },
  );
  const changes = output.trim().split(/\r?\n/).filter(Boolean).map((line) => line.split("\t"));
  return changes.filter(([, filename]) => Object.entries(FORMATS).some(([family, extensions]) => (
    filename.startsWith(`${relativeRoot}/${family}/`) && extensions.has(path.extname(filename))
  ))).flatMap(([status, filename]) => {
    if (status === "D") return [`${filename}: contract removed; publish a new major version instead`];
    const before = parse(execFileSync("git", ["show", `${base}:${filename}`], { cwd: WORKSPACE, encoding: "utf8" }), filename);
    const after = parse(readFileSync(path.join(WORKSPACE, filename), "utf8"), filename);
    return breakingChanges(before, after).map((finding) => `${filename}: ${finding}`);
  });
}

export async function validateContracts(contractRoot, base) {
  const failures = [];
  for (const [family, extensions] of Object.entries(FORMATS)) {
    const files = filesUnder(path.join(contractRoot, family), extensions);
    for (const filename of files) {
      try { await validateFile(family, filename, contractRoot); } catch (error) { failures.push(error.message); }
    }
    console.log(`${family}: ${files.length} contract(s) validated`);
  }
  failures.push(...compatibilityFailures(base, contractRoot));
  if (failures.length) throw new Error(failures.join("\n"));
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const root = path.resolve(process.argv[2] ?? "contracts");
  const baseIndex = process.argv.indexOf("--base");
  const base = baseIndex >= 0 ? process.argv[baseIndex + 1] : undefined;
  if (baseIndex >= 0 && !base) throw new Error("--base requires a git revision");
  await validateContracts(root, base);
}
