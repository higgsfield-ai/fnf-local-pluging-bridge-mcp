import { z } from "zod";
import { errorResult } from "../errors.js";
import { SkillStore } from "../skills.js";
import { defineTool, jsonResult } from "./define-tool.js";

export const getSkillAssetTool = defineTool({
  name: "ae_get_skill_asset",
  title: "Skill asset path",
  description:
    "Locate a file bundled with a skill (LUT, DCTL, JSON data or Python helper) and return its absolute on-disk path after verifying its hash. Returns the path only, never the content; pass it to the host application, a shell or Python. Files are listed by ae_get_skill.",
  group: "inspect",
  blockedInReadOnly: false,
  effect: "read",
  inputShape: {
    name: z
      .string()
      .min(1)
      .describe("Exact skill name from the index, such as davinci-film-colorist."),
    path: z
      .string()
      .min(1)
      .describe("Exact file path listed by the skill, such as assets/tonality/portra.cube."),
  },
  handler: async (args, _transport) => {
    try {
      return jsonResult(new SkillStore().resolveFile(args.name, args.path));
    } catch (error) {
      return errorResult(
        error instanceof RangeError ? "INVALID_ARGS" : "IO",
        error instanceof Error ? error.message : String(error),
      );
    }
  },
});
