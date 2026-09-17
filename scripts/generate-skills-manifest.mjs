import { createHash } from "node:crypto";
import { lstatSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";

if (process.argv.slice(2).some((argument) => argument !== "--check"))
  throw new Error("Usage: node scripts/generate-skills-manifest.mjs [--check]");

const root = resolve(import.meta.dirname, "../skills");
// A SKILL.md is loaded whole into the model's context; keep it readable.
const MAX_DOCUMENT_BYTES = 64 * 1024;
// Total assets/ + scripts/ per skill; the package ships them to every install.
const MAX_SKILL_FILE_BYTES = 96 * 1024 * 1024;

function fileSha256(file) {
  return createHash("sha256").update(readFileSync(file)).digest("hex");
}
const manifestPath = join(root, "manifest.json");
const manifest = {
  schemaVersion: 4,
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
  // Non-Markdown files a skill ships for local use: LUTs, DCTLs, JSON data and
  // Python helpers. Served by path (never by content) through ae_get_skill_asset.
  const files = {};
  let bytes = 0;
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
        if (stat.size > MAX_DOCUMENT_BYTES)
          throw new Error(`Document exceeds ${MAX_DOCUMENT_BYTES} bytes: ${relative}`);
        documents[relative] = createHash("sha256").update(readFileSync(file)).digest("hex");
      } else if (/^(assets|scripts)\//.test(relative)) {
        if (
          !/^(assets|scripts)\/[a-zA-Z0-9][a-zA-Z0-9/._-]*$/.test(relative) ||
          relative.includes("/.")
        )
          throw new Error(`Invalid skill file: ${relative}`);
        bytes += stat.size;
        files[relative] = { sha256: fileSha256(file), bytes: stat.size };
      } else if (!/^agents\/[a-z0-9-]+\.ya?ml$/.test(relative)) {
        throw new Error(`Unexpected skill file: ${relative}`);
      }
    }
  };
  walk(base);
  if (bytes > MAX_SKILL_FILE_BYTES)
    throw new Error(`Skill files exceed ${MAX_SKILL_FILE_BYTES} bytes: ${name} (${bytes})`);
  const entry = readFileSync(join(base, "SKILL.md"), "utf8");
  const description = entry.match(/^description: (.+)$/m)?.[1];
  if (!description || !entry.startsWith(`---\nname: ${name}\n`))
    throw new Error(`Invalid metadata: ${name}`);
  const entry_ = { name, path: `${group}/${name}`, description, documents };
  if (Object.keys(files).length) entry_.files = files;
  manifest.skills.push(entry_);
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
