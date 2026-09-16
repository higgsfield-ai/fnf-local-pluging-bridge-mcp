import { createHash } from "node:crypto";
import { lstatSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";

if (process.argv.slice(2).some((argument) => argument !== "--check"))
  throw new Error("Usage: node scripts/generate-skills-manifest.mjs [--check]");

const root = resolve(import.meta.dirname, "../skills");
const manifestPath = join(root, "manifest.json");
const manifest = {
  schemaVersion: 3,
  sourceRepository: "higgsfield-ai/fnf-local-pluging-bridge-mcp",
  sourcePath: "skills",
  skills: [],
};

// Skills are grouped one level deep by host application: skills/<group>/<name>.
// The group is a filing decision only; the skill's identity stays its leaf name,
// so ae_get_skill(name) and every stored reference keep working across a regroup.
const groups = [];
for (const group of readdirSync(root).toSorted()) {
  if (group === "manifest.json") continue;
  const groupBase = join(root, group);
  const groupStat = lstatSync(groupBase);
  if (groupStat.isSymbolicLink()) throw new Error(`Symlink forbidden: ${groupBase}`);
  if (!groupStat.isDirectory())
    throw new Error(`Unexpected file beside skill groups: ${groupBase}`);
  if (!/^[a-z0-9-]+$/.test(group)) throw new Error(`Invalid skill group: ${group}`);
  for (const name of readdirSync(groupBase).toSorted()) groups.push([group, name]);
}

const seen = new Set();
for (const [group, name] of groups) {
  const base = join(root, group, name);
  const skillStat = lstatSync(base);
  if (skillStat.isSymbolicLink()) throw new Error(`Symlink forbidden: ${base}`);
  if (!skillStat.isDirectory()) throw new Error(`Unexpected skill file: ${base}`);
  if (!/^[a-z0-9-]+$/.test(name)) throw new Error(`Invalid skill name: ${name}`);
  if (seen.has(name)) throw new Error(`Duplicate skill name across groups: ${name}`);
  seen.add(name);
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
  manifest.skills.push({ name, path: `${group}/${name}`, description, documents });
}

manifest.skills.sort((a, b) => (a.name < b.name ? -1 : a.name > b.name ? 1 : 0));

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
