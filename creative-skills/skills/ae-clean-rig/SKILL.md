---
name: ae-clean-rig
description: Build and edit clean native After Effects projects, preserve reference appearance and motion, expose useful controls, and verify rendered results through the local MCP.
---

# Clean native AE rigs

Start with the user's requested change and inspect the current project using `ae_project_info`, `ae_comp_info` and `ae_layer_info` as appropriate. Use `ae_catalog` to discover exact local operation schemas, then `ae_do` to execute them. Do not invent bridge tool names. User constraints override examples and defaults in these skills.

Preserve appearance, timing and approved content. Build meaningful native text, paths, controls and semantic precomps. Use media for actual footage and imagery, not screenshot fragments that pretend to be editable components. Shared motion belongs on the component's parent rig; unrelated editable content needs independent sources.

Before a broad structural edit, use a separate project copy or a suitable backup within the authorized workflow. Do not save over a source, close an unsaved project, or reset the project merely to simplify implementation. Routine reversible edits do not need repeated confirmation.

## Read relevant references

Use `ae_get_skill({name: "ae-clean-rig", reference: "references/01-construction.md"})` to load one module, or follow the relative link when reading from disk.

- [Construction](references/01-construction.md): native layers, paths, source media.
- [Reference motion](references/02-reference-motion.md): observation, timing and curves.
- [Typography](references/03-typography.md): stable layout, readable native text.
- [Gradients and effects](references/04-gradients-effects.md): alpha, coordinate spaces and effect order.
- [Media](references/05-higgsfield-media.md): optional generation and portable local assets.
- [Editable rigs](references/06-editable-rigs.md): controllers and independent sources.
- [Sliders](references/07-sliders.md): wraparound, fitting and manual controls.
- [Characters](references/08-characters.md): silhouettes, gaze and expression controls.
- [Validation](references/09-validation-delivery.md): rendered proof and delivery.
- [Scripting](references/10-ae-scripting.md): native AE API pitfalls.

## Companion routing

Load only what the task needs through `ae_get_skill`: `ae-mcp-realities` for transport/capability limits; `ae-build-orchestration` for larger builds; `ae-animation-principles` for motion; `ae-ui-mastery` for interface composition; `ae-design-first` for planning a layout; `ae-depth-space` for depth; `ae-liquid-glass` for glass; `ae-transition-kit` for reusable transitions.

## Finish

Inspect returned results and expression errors, render representative frames with `ae_render_frame`, and review the images. Include start, peak motion, settled state and seams when relevant. Check editability with a representative content change in a temporary duplicate. Save the intended deliverable only to its authorized destination and report the actual file, verified behavior and remaining limitations. A completed tool call or queued render alone is not visual proof.
