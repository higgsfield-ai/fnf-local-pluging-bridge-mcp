import { createHash } from "node:crypto";
import { lstatSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";

if (process.argv.slice(2).some((argument) => argument !== "--check"))
  throw new Error("Usage: node scripts/generate-skills-manifest.mjs [--check]");

const root = resolve(import.meta.dirname, "../skills");
const manifestPath = join(root, "manifest.json");
const manifest = {
  schemaVersion: 2,
  sourceRepository: "higgsfield-ai/fnf-local-pluging-bridge-mcp",
  sourcePath: "skills",
  skills: [],
};

for (const name of readdirSync(root).toSorted()) {
  if (name === "manifest.json") continue;
  const base = join(root, name);
  const skillStat = lstatSync(base);
  if (skillStat.isSymbolicLink()) throw new Error(`Symlink forbidden: ${base}`);
  if (!skillStat.isDirectory()) throw new Error(`Unexpected skill file: ${base}`);
  if (!/^[a-z0-9-]+$/.test(name)) throw new Error(`Invalid skill name: ${name}`);
  const documents = {};
  const walk = (directory, prefix = "") => {
    for (const item of readdirSync(directory).toSorted()) {
      const file = join(directory, item);
      const relative = prefix + item;
      const stat = lstatSync(file);
      if (stat.isSymbolicLink()) throw new Error(`Symlink forbidden: ${file}`);
      if (stat.isDirectory()) walk(file, relative + "/");
      else if (item.endsWith(".md")) {
        if (!/^(SKILL\.md|references\/[a-zA-Z0-9/_-]+\.md)$/.test(relative))
          throw new Error(`Invalid document: ${relative}`);
        documents[relative] = createHash("sha256").update(readFileSync(file)).digest("hex");
      }
    }
  };
  walk(base);
  const entry = readFileSync(join(base, "SKILL.md"), "utf8");
  const description = entry.match(/^description: (.+)$/m)?.[1];
  if (!description || !entry.startsWith(`---\nname: ${name}\n`))
    throw new Error(`Invalid metadata: ${name}`);
  manifest.skills.push({ name, description, documents });
}

if (!manifest.skills.length) throw new Error("No skills found");
const content = JSON.stringify(manifest, null, 2) + "\n";
if (process.argv.includes("--check")) {
  if (readFileSync(manifestPath, "utf8") !== content)
    throw new Error("Skill manifest is stale. Run npm run skills:manifest and commit the result.");
  console.log(`Verified manifest for ${manifest.skills.length} skills.`);
} else {
  writeFileSync(manifestPath, content);
  console.log(`Generated manifest for ${manifest.skills.length} skills.`);
}
