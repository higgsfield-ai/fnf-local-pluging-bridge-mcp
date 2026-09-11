import { readFile } from "node:fs/promises";

export const SKILL_NAMES = ["blender-scene", "modeling", "materials", "lighting-camera", "animation"] as const;
export async function getSkill(name: typeof SKILL_NAMES[number]): Promise<string> {
  const relative = name === "blender-scene" ? "SKILL.md" : `references/${name}.md`;
  return readFile(new URL(`../skills/blender-scene/${relative}`, import.meta.url), "utf8");
}
