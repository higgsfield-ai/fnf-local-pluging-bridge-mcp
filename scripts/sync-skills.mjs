import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import {
  mkdirSync,
  readFileSync,
  readdirSync,
  lstatSync,
  writeFileSync,
  existsSync,
  rmSync,
  renameSync,
} from "node:fs";
import { resolve, join } from "node:path";
const source = process.argv[2];
if (!source)
  throw new Error("Usage: node scripts/sync-skills.mjs /path/to/fnf-creative-apps-skills");
const root = resolve(source);
if (execFileSync("git", ["-C", root, "status", "--porcelain"], { encoding: "utf8" }).trim())
  throw new Error("Commit source changes before pinning skills.");
const sourceCommit = execFileSync("git", ["-C", root, "rev-parse", "HEAD"], {
  encoding: "utf8",
}).trim();
const destination = resolve(import.meta.dirname, "../skills");
const staged = destination + ".staging";
if (existsSync(staged))
  throw new Error("Remove stale skills.staging after reviewing its contents.");
const manifest = {
  schemaVersion: 1,
  sourceRepository: "fnf-creative-apps-skills",
  sourceCommit,
  skills: [],
};
const docs = [];
for (const name of readdirSync(join(root, "skills")).toSorted()) {
  if (!/^[a-z0-9-]+$/.test(name)) throw new Error(`Invalid skill name: ${name}`);
  const base = join(root, "skills", name);
  const entry = readFileSync(join(base, "SKILL.md"), "utf8");
  const description = entry.match(/^description: (.+)$/m)?.[1];
  if (!description || !entry.startsWith(`---\nname: ${name}\n`))
    throw new Error(`Invalid metadata: ${name}`);
  const documents = {};
  const walk = (dir, prefix = "") => {
    for (const item of readdirSync(dir).toSorted()) {
      const file = join(dir, item),
        relative = prefix + item,
        stat = lstatSync(file);
      if (stat.isSymbolicLink()) throw new Error(`Symlink forbidden: ${file}`);
      if (stat.isDirectory()) walk(file, relative + "/");
      else if (item.endsWith(".md")) {
        if (!/^(SKILL\.md|references\/[a-zA-Z0-9/_-]+\.md)$/.test(relative))
          throw new Error(`Invalid document: ${relative}`);
        const data = readFileSync(file);
        documents[relative] = createHash("sha256").update(data).digest("hex");
        docs.push({ path: name + "/" + relative, data });
      }
    }
  };
  walk(base);
  manifest.skills.push({ name, description, documents });
}
mkdirSync(staged);
try {
  for (const doc of docs) {
    const file = join(staged, doc.path);
    mkdirSync(resolve(file, ".."), { recursive: true });
    writeFileSync(file, doc.data);
  }
  writeFileSync(join(staged, "manifest.json"), JSON.stringify(manifest, null, 2) + "\n");
  if (existsSync(destination)) rmSync(destination, { recursive: true });
  renameSync(staged, destination);
} finally {
  if (existsSync(staged)) rmSync(staged, { recursive: true });
}
console.log(
  `Pinned ${manifest.skills.length} skills (${docs.length} documents) from ${sourceCommit}`,
);
