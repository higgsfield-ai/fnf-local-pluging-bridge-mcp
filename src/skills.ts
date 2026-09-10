import { createHash } from "node:crypto";
import { readFileSync, realpathSync } from "node:fs";
import { isAbsolute, relative, resolve } from "node:path";
import { z } from "zod";
import { PACKAGE_ROOT } from "./config.js";

const documentName = /^(SKILL\.md|references\/[a-zA-Z0-9/_-]+\.md)$/;
const manifestSchema = z.object({
  schemaVersion: z.literal(1),
  sourceRepository: z.string(),
  sourceCommit: z.string().regex(/^[a-f0-9]{40}$/),
  skills: z
    .array(
      z.object({
        name: z.string().regex(/^[a-z0-9-]+$/),
        description: z.string().min(1),
        documents: z.record(z.string().regex(documentName), z.string().regex(/^[a-f0-9]{64}$/)),
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
      sourceCommit: this.manifest.sourceCommit,
      skills: this.manifest.skills.map(({ name, description, documents }) => ({
        name,
        description,
        references: Object.keys(documents).filter((p) => p !== "SKILL.md"),
      })),
    };
  }

  read(name: string, document = "SKILL.md") {
    const skill = this.manifest.skills.find((s) => s.name === name);
    if (!skill)
      throw new RangeError(
        `Unknown skill '${name}'. Call ae_get_skill with no arguments for the index.`,
      );
    if (!Object.hasOwn(skill.documents, document))
      throw new RangeError(
        `Unknown reference '${document}' for '${name}'. Load the entry to list references.`,
      );
    const file = realpathSync(resolve(this.root, name, document));
    const local = relative(this.root, file);
    if (local === ".." || local.startsWith("../") || local.startsWith("..\\") || isAbsolute(local))
      throw new Error("Skill path escapes the bundled corpus");
    const bytes = readFileSync(file);
    const sha256 = createHash("sha256").update(bytes).digest("hex");
    if (sha256 !== skill.documents[document])
      throw new Error(
        `Skill integrity mismatch: ${name}/${document}. Restore or resync the pinned bundle.`,
      );
    return {
      name,
      document,
      content: bytes.toString("utf8"),
      sha256,
      sourceCommit: this.manifest.sourceCommit,
      references: Object.keys(skill.documents).filter((p) => p !== "SKILL.md"),
    };
  }
}
