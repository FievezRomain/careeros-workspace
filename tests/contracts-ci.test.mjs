import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";

import { breakingChanges } from "../scripts/validate-contracts.mjs";

const SCRIPT = path.resolve("scripts/validate-contracts.mjs");

function fixture(documents) {
  const root = mkdtempSync(path.join(tmpdir(), "careeros-contracts-"));
  for (const [filename, document] of Object.entries(documents)) {
    const target = path.join(root, filename);
    mkdirSync(path.dirname(target), { recursive: true });
    writeFileSync(target, JSON.stringify(document, null, 2));
  }
  return root;
}

const valid = {
  "openapi/example/v1/openapi.json": {
    openapi: "3.1.2",
    info: {
      title: "Synthetic API",
      version: "1.0.0",
      license: { name: "Apache-2.0", identifier: "Apache-2.0" },
    },
    servers: [{ url: "https://api.example.invalid" }],
    paths: {},
  },
  "asyncapi/example/v1/asyncapi.json": {
    asyncapi: "3.1.0",
    info: { title: "Synthetic events", version: "1.0.0" },
    channels: {},
    operations: {},
  },
  "json-schema/example/profile.v1.schema.json": {
    $schema: "https://json-schema.org/draft/2020-12/schema",
    $id: "https://careeros.example/schemas/example/profile.v1.schema.json",
    type: "object",
    properties: { id: { type: "string" } },
    required: ["id"],
    additionalProperties: false,
  },
};

test("accepts conforming OpenAPI, AsyncAPI and JSON Schema contracts", (context) => {
  const root = fixture(valid);
  context.after(() => rmSync(root, { recursive: true, force: true }));
  const result = spawnSync(process.execPath, [SCRIPT, root], { encoding: "utf8" });
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /openapi: 1 contract/);
  assert.match(result.stdout, /asyncapi: 1 contract/);
  assert.match(result.stdout, /json-schema: 1 contract/);
});

test("rejects invalid versions and schemas with actionable output", (context) => {
  const documents = structuredClone(valid);
  documents["openapi/example/v1/openapi.json"].openapi = "3.0.3";
  documents["openapi/example/v1/remote.json"] = structuredClone(valid["openapi/example/v1/openapi.json"]);
  documents["openapi/example/v1/remote.json"].components = {
    schemas: { External: { $ref: "https://untrusted.example/schema.json" } },
  };
  documents["asyncapi/example/v1/asyncapi.json"].asyncapi = "2.6.0";
  documents["json-schema/example/profile.v1.schema.json"].$schema = "http://json-schema.org/draft-07/schema#";
  const root = fixture(documents);
  context.after(() => rmSync(root, { recursive: true, force: true }));
  const result = spawnSync(process.execPath, [SCRIPT, root], { encoding: "utf8" });
  assert.equal(result.status, 1);
  assert.match(result.stderr, /openapi must be 3\.1\.2/);
  assert.match(result.stderr, /\$ref must resolve inside the contracts directory/);
  assert.match(result.stderr, /asyncapi must be 3\.1\.0/);
  assert.match(result.stderr, /JSON Schema 2020-12/);
});

test("detects removals, new required fields and narrowed enums", () => {
  const before = {
    paths: { "/profiles": { get: { responses: { 200: {} } } } },
    properties: { status: { type: "string", enum: ["draft", "ready"] } },
    required: ["status"],
  };
  const after = {
    paths: { "/profiles": {} },
    properties: { status: { type: "string", enum: ["ready"] }, owner: { type: "string" } },
    required: ["status", "owner"],
  };
  const findings = breakingChanges(before, after);
  assert(findings.some((value) => value.includes("operation removed")));
  assert(findings.some((value) => value.includes("required owner added")));
  assert(findings.some((value) => value.includes("enum value draft removed")));
});

test("allows additive optional fields", () => {
  const before = { properties: { id: { type: "string" } }, required: ["id"] };
  const after = { properties: { id: { type: "string" }, label: { type: "string" } }, required: ["id"] };
  assert.deepEqual(breakingChanges(before, after), []);
});
