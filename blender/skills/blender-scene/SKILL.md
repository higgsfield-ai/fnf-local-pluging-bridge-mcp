---
name: blender-scene
description: Create, inspect, edit and render native scenes through the local Higgsfield use Blender MCP.
---

# Local Blender workflow

Call `bl_health` and `bl_get_scene_summary` before editing. Inspect important objects with `bl_get_object`. This is a dedicated background session, not an open desktop window. Load saved input files with bl_open_project; save outputs before reconnecting.

Prefer the typed tools listed by this server. Use `bl_execute` for other bpy operations; assign a JSON-compatible value to `result`. Returned stdout/stderr are capped at 64 Ki characters each. Do not start threads that touch bpy. Use data APIs where possible; operators depend on mode, selection and UI context.

Distances are in scene units (normally metres); Z is up and Euler angles are radians. Check the scene's unit settings when scale matters. Names identify objects exactly; inspect suffixes rather than assuming them.

## Topic modules

Keep this entry as the runtime contract for the local background session. Read only
modules relevant to the current task through the host's installed plugin skills,
using the relative files below. This entry routes the task; the model reads the
selected guidance and performs the relevant checks and tool calls.

`bl_get_skill` remains an optional route to this entry and the original short
references (`modeling`, `materials`, `lighting-camera`, `animation`). It does not
serve the new `blender-*` modules: read their installed skill files instead. An
MCP-only connection does not expose those files to the host; if the skill bundle is
missing, report the unavailable module instead of calling an unsupported name or
pretending that a link loaded its contents.

| Task | Module |
|---|---|
| Whole-scene specification, scale, hierarchy and acceptance criteria | [blender-scene-spec](../blender-scene-spec/SKILL.md) |
| Blockout, geometry, topology and editable construction | [blender-modeling](../blender-modeling/SKILL.md) |
| Materials, UVs, texture scale and appearance | [blender-lookdev](../blender-lookdev/SKILL.md) |
| Lighting, camera composition and render setup | [blender-lighting-camera](../blender-lighting-camera/SKILL.md) |
| Motion, rigs, keyframes and loops | [blender-animation](../blender-animation/SKILL.md) |
| Generated assets through a separately connected provider | [blender-generation](../blender-generation/SKILL.md) |
| Generated environment maps | [blender-hdri](../blender-hdri/SKILL.md), with blender-generation |
| Generated tileable materials | [blender-pbr](../blender-pbr/SKILL.md), with blender-generation |
| Greybox scene and motion-reference rendering | [blender-greybox](../blender-greybox/SKILL.md) |
| Structural, motion and visual checks, then delivery | [blender-audit-finalize](../blender-audit-finalize/SKILL.md) |
| Model catalog and Blender API/version differences | [blender-volatile](../blender-volatile/SKILL.md) |

These modules are preserved from the cloud connector export. Its `get_host_status`,
panel/host `blr`, viewport, cloud generation and extended typed-tool instructions do
not establish those capabilities in this local package. Inspect the actual exposed
tools; retain this entry's background-session, save and job-recovery contract. Use
available typed tools or `bl_execute` for supported local bpy work. A separate
provider is required for generation; name a missing capability or external reference
before dependent work instead of inventing a tool, connection or successful check.

## Local execution and delivery

Preserve unrelated objects. Save `.blend` deliverables requested by the user with `bl_save_project`; existing files need `overwrite=true`. Before replacing the active project, save needed changes. `bl_open_project` refuses unsaved changes unless explicitly discarded.

A script may partially mutate before failing. Inspect current state before retrying. A timed-out command may still be running; use its `job_id` with `bl_job_status` on the same MCP session. Commands are not automatically retried or rolled back. Job history is in-memory and bounded; reconnecting loses it and any unsaved scene changes.

Verify structure with fresh reads and appearance by viewing `bl_render` output. Set a scene camera first; no viewport exists in this session. Rendering occupies the session until it completes. Set the MCP client's tool timeout above 300 seconds for long renders.

This package has no cloud generation tools or bundled bpy API/manual search. Use a separately connected Higgsfield service for generated assets; download results then call `bl_import_model` with an absolute local path. Read official version-matched Blender docs for unfamiliar APIs.
