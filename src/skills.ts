import { createHash } from "node:crypto";
import { readFileSync, realpathSync } from "node:fs";
import { isAbsolute, relative, resolve } from "node:path";
import { z } from "zod";
import { PACKAGE_ROOT } from "./config.js";

const documentName = /^(SKILL\.md|references\/[a-zA-Z0-9/_-]+\.md)$/;
const fileName = /^(assets|scripts)\/[a-zA-Z0-9][a-zA-Z0-9/._-]*$/;
const manifestSchema = z.object({
  schemaVersion: z.literal(4),
  sourceRepository: z.string(),
  sourcePath: z.literal("skills"),
  skills: z
    .array(
      z.object({
        name: z.string().regex(/^[a-z0-9-]+$/),
        path: z.string().regex(/^[a-z0-9-]+\/[a-z0-9-]+$/),
        description: z.string().min(1),
        documents: z.record(z.string().regex(documentName), z.string().regex(/^[a-f0-9]{64}$/)),
        // Binary or data files (LUTs, DCTLs, JSON, Python) served by path, never by content.
        files: z
          .record(
            z.string().regex(fileName),
            z.object({
              sha256: z.string().regex(/^[a-f0-9]{64}$/),
              bytes: z.number().int().min(0),
            }),
          )
          .optional(),
      }),
    )
    .min(1),
});

export class SkillStore {
  readonly manifest: z.infer<typeof manifestSchema>;
  private readonly root: string;

  constructor(root = resolve(PACKAGE_ROOT, "skills")) {
    this.root = realpathSync(root);
    this.manifest = manifestSchema.parse(
      JSON.parse(readFileSync(resolve(this.root, "manifest.json"), "utf8")),
    );
    const names = this.manifest.skills.map((s) => s.name);
    if (new Set(names).size !== names.length) throw new Error("Duplicate skill names in manifest");
    for (const skill of this.manifest.skills) {
      if (!Object.hasOwn(skill.documents, "SKILL.md"))
        throw new Error(`Missing entry for ${skill.name}`);
    }
  }

  index() {
    return {
      skills: this.manifest.skills.map(({ name, description, documents, files }) => ({
        name,
        description,
        references: Object.keys(documents).filter((p) => p !== "SKILL.md"),
        ...(files ? { files: Object.keys(files) } : {}),
      })),
    };
  }

  private skill(name: string) {
    const skill = this.manifest.skills.find((s) => s.name === name);
    if (!skill)
      throw new RangeError(
        `Unknown skill '${name}'. Call ae_get_skill with no arguments for the index.`,
      );
    return skill;
  }

  /** Absolute path of a bundled file, checked against the corpus root and its recorded hash. */
  private locate(skill: { path: string }, entry: string, expected: string) {
    const file = realpathSync(resolve(this.root, skill.path, entry));
    const local = relative(this.root, file);
    if (local === ".." || local.startsWith("../") || local.startsWith("..\\") || isAbsolute(local))
      throw new Error("Skill path escapes the bundled corpus");
    const bytes = readFileSync(file);
    const sha256 = createHash("sha256").update(bytes).digest("hex");
    if (sha256 !== expected)
      throw new Error(
        `Skill integrity mismatch: ${skill.path}/${entry}. Restore the bundled files or run npm run skills:manifest after editing skills.`,
      );
    return { file, bytes, sha256 };
  }

  /**
   * Resolve one asset or script to its on-disk path so a local tool (Resolve,
   * Python, a shell) can open it. The content is hashed but never returned.
   */
  resolveFile(name: string, path: string) {
    const skill = this.skill(name);
    if (!skill.files || !Object.hasOwn(skill.files, path))
      throw new RangeError(`Unknown file '${path}' for '${name}'. Load the entry to list files.`);
    const { file, sha256 } = this.locate(skill, path, skill.files[path].sha256);
    return {
      name,
      path,
      absolute_path: file,
      sha256,
      bytes: skill.files[path].bytes,
      files: Object.keys(skill.files),
    };
  }

  read(name: string, document = "SKILL.md") {
    const skill = this.skill(name);
    if (!Object.hasOwn(skill.documents, document))
      throw new RangeError(
        `Unknown reference '${document}' for '${name}'. Load the entry to list references.`,
      );
    const { bytes, sha256 } = this.locate(skill, document, skill.documents[document]);
    return {
      name,
      document,
      content: bytes.toString("utf8"),
      sha256,
      references: Object.keys(skill.documents).filter((p) => p !== "SKILL.md"),
      ...(skill.files ? { files: Object.keys(skill.files) } : {}),
    };
  }
}
