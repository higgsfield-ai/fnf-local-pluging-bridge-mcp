import { afterEach, describe, expect, it } from "vitest";
import {
  cpSync,
  mkdtempSync,
  readFileSync,
  rmSync,
  symlinkSync,
  unlinkSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { SkillStore } from "../src/skills.js";
import { getSkillTool } from "../src/tools/get-skill.js";
import { nullTransport } from "./helpers/null-transport.js";
import { ALL_TOOLS } from "../src/tools/index.js";
import { McpTestClient } from "./harness.js";

const temporary: string[] = [];
afterEach(() => {
  for (const dir of temporary.splice(0)) rmSync(dir, { recursive: true, force: true });
});
function copyCorpus() {
  const root = mkdtempSync(join(tmpdir(), "fnf-skills-test-"));
  temporary.push(root);
  cpSync(resolve("skills"), root, { recursive: true });
  return root;
}

describe("pinned AE skills", () => {
  it("loads every pinned entry/reference and validates documented tool names", () => {
    const store = new SkillStore();
    const tools = new Set(ALL_TOOLS.map((tool) => tool.name));
    expect(store.index().skills).toHaveLength(10);
    for (const skill of store.manifest.skills) {
      for (const document of Object.keys(skill.documents)) {
        const result = store.read(skill.name, document);
        expect(result.content.length).toBeGreaterThan(100);
        for (const match of result.content.matchAll(/\bae_[a-z_]+\b/g))
          expect(tools.has(match[0]), match[0]).toBe(true);
      }
    }
  });

  it("returns only the selected entry or reference", () => {
    const store = new SkillStore();
    const entry = store.read("ae-clean-rig");
    expect(entry.references).toHaveLength(10);
    expect(entry.content).not.toContain("# Practical editability and exposed controls");
    expect(store.read("ae-clean-rig", "references/06-editable-rigs.md").content).toContain(
      "# Practical editability and exposed controls",
    );
  });

  it.each([
    "../../package.json",
    "/etc/passwd",
    "__proto__",
    "references/../../../package.json",
    "references%2F07-sliders.md",
  ])("rejects unlisted references: %s", (reference) => {
    expect(() => new SkillStore().read("ae-clean-rig", reference)).toThrow("Unknown reference");
  });

  it("rejects unknown skills, including prototype property names", () => {
    for (const name of ["missing", "__proto__", "../../etc"])
      expect(() => new SkillStore().read(name)).toThrow("Unknown skill");
  });

  it("detects edited bundle documents", () => {
    const root = copyCorpus();
    writeFileSync(join(root, "ae-clean-rig/SKILL.md"), "tampered");
    expect(() => new SkillStore(root).read("ae-clean-rig")).toThrow("integrity mismatch");
  });

  it.skipIf(process.platform === "win32")(
    "rejects a listed document symlink outside the corpus",
    () => {
      const root = copyCorpus();
      const file = join(root, "ae-clean-rig/SKILL.md");
      unlinkSync(file);
      symlinkSync(resolve("package.json"), file);
      expect(() => new SkillStore(root).read("ae-clean-rig")).toThrow("escapes");
    },
  );

  it("rejects duplicate manifest names", () => {
    const root = copyCorpus();
    const path = join(root, "manifest.json");
    const data = JSON.parse(readFileSync(path, "utf8"));
    data.skills.push(data.skills[0]);
    writeFileSync(path, JSON.stringify(data));
    expect(() => new SkillStore(root)).toThrow("Duplicate");
  });

  it("does not dispatch AE for index, documents or invalid arguments", async () => {
    const transport = nullTransport();
    expect((await getSkillTool.handler({}, transport)).isError).toBe(false);
    expect((await getSkillTool.handler({ name: "ae-clean-rig" }, transport)).isError).toBe(false);
    expect((await getSkillTool.handler({ reference: "SKILL.md" }, transport)).isError).toBe(true);
    expect((await getSkillTool.handler({ name: "missing" }, transport)).isError).toBe(true);
    expect(transport.calls).toHaveLength(0);
  });

  it("serves skills through real stdio in read-only mode without AE", async () => {
    const client = new McpTestClient();
    await client.connect({ AE_MCP_READONLY: "1" });
    try {
      const index = await client.call<{ skills: unknown[] }>("ae_get_skill");
      expect(index.skills).toHaveLength(10);
      const entry = await client.call<{ content: string; references: string[] }>("ae_get_skill", {
        name: "ae-clean-rig",
      });
      expect(entry.content).toContain("Clean native AE rigs");
      expect(entry.references).toContain("references/07-sliders.md");
      expect(await client.callExpectError("ae_get_skill", { name: "missing" })).toContain(
        "INVALID_ARGS",
      );
    } finally {
      await client.close();
    }
  });
});
