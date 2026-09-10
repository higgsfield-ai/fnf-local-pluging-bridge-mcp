import { z } from "zod";
import { errorResult } from "../errors.js";
import { SkillStore } from "../skills.js";
import { defineTool, jsonResult } from "./define-tool.js";

export const getSkillTool = defineTool({
  name: "ae_get_skill",
  title: "After Effects skills",
  description:
    "Read bundled local AE workflows without opening After Effects or using the network. Omit name for the index; supply name for an entry, and reference for one listed module. Start with ae-clean-rig before building or editing projects.",
  group: "inspect",
  blockedInReadOnly: false,
  effect: "read",
  inputShape: {
    name: z
      .string()
      .min(1)
      .optional()
      .describe("Exact skill name from the index, such as ae-clean-rig."),
    reference: z
      .string()
      .min(1)
      .optional()
      .describe(
        "Exact reference path listed by the skill, such as references/01-construction.md. Requires name.",
      ),
  },
  handler: async (args, _transport) => {
    if (args.reference && !args.name)
      return errorResult("INVALID_ARGS", "reference requires a skill name");
    try {
      const store = new SkillStore();
      return jsonResult(args.name ? store.read(args.name, args.reference) : store.index());
    } catch (error) {
      return errorResult(
        error instanceof RangeError ? "INVALID_ARGS" : "IO",
        error instanceof Error ? error.message : String(error),
      );
    }
  },
});
