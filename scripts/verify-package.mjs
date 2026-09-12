import { execFileSync } from "node:child_process";
import { mkdtempSync, mkdirSync, symlinkSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import assert from "node:assert/strict";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
const root = resolve(import.meta.dirname, "..");
const temp = mkdtempSync(join(tmpdir(), "fnf-ae-package-"));
const client = new Client({ name: "fnf-package-verification", version: "1.0.0" });
try {
  const packed = JSON.parse(
    execFileSync("npm", ["pack", "--json", "--pack-destination", temp], {
      cwd: root,
      encoding: "utf8",
    }),
  )[0];
  assert(packed.files.some((x) => x.path === "skills/manifest.json"));
  assert(
    !packed.files.some(
      (x) =>
        x.path.startsWith("blender/") ||
        x.path.startsWith("archive/") ||
        x.path.startsWith("runtime/") ||
        x.path.startsWith("creative-skills/"),
    ),
  );
  mkdirSync(join(temp, "extracted"));
  execFileSync("tar", ["-xzf", join(temp, packed.filename), "-C", join(temp, "extracted")]);
  const pkg = join(temp, "extracted/package");
  symlinkSync(join(root, "node_modules"), join(pkg, "node_modules"), "junction");
  await client.connect(
    new StdioClientTransport({
      command: process.execPath,
      args: [join(pkg, "dist/index.js")],
      cwd: tmpdir(),
      stderr: "pipe",
    }),
  );
  assert.equal(client.getServerVersion().name, "higgsfield-use-after-effects");
  assert.equal(client.getServerVersion().title, "Higgsfield use After Effects");
  const tools = await client.listTools();
  assert.equal(tools.tools.length, 12);
  const skill = await client.callTool({
    name: "ae_get_skill",
    arguments: { name: "ae-clean-rig", reference: "references/07-sliders.md" },
  });
  assert(!skill.isError);
  assert(skill.structuredContent.content.includes("Slide"));
  const catalog = await client.callTool({ name: "ae_catalog", arguments: {} });
  assert(!catalog.isError);
  console.log(
    JSON.stringify(
      {
        ok: true,
        packedFiles: packed.files.length,
        tools: tools.tools.length,
        sha256: skill.structuredContent.sha256,
        dependencies:
          "Shared installed dependencies; package content extracted independently, cwd outside checkout.",
      },
      null,
      2,
    ),
  );
} finally {
  await client.close();
  rmSync(temp, { recursive: true, force: true });
}
