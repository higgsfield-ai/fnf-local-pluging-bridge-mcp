---
name: blender-scene
description: Create, inspect, edit and render native scenes through the local Higgsfield use Blender MCP.
---

# Local Blender workflow

Call `bl_health` and `bl_get_scene_summary` before editing. Inspect important objects with `bl_get_object`. If several instances are open, select the intended PID in the server environment before mutation.

Prefer the typed tools listed by this server. Use `bl_execute` for other bpy operations; assign a JSON-compatible value to `result`. Returned stdout/stderr are capped at 64 KiB each. Do not start threads that touch bpy. Use data APIs where possible; operators depend on mode, selection and UI context.

Distances are in scene units (normally metres); Z is up and Euler angles are radians. Check the scene's unit settings when scale matters. Names identify objects exactly; inspect suffixes rather than assuming them.

Read topic guidance through `bl_get_skill`: `modeling`, `materials`, `lighting-camera`, or `animation`, as needed.

Preserve unrelated objects. Save `.blend` deliverables requested by the user with `bl_save_project`; existing files need `overwrite=true`. Before replacing the active project, save needed changes. `bl_open_project` refuses unsaved changes unless explicitly discarded.

A script may partially mutate before failing. Inspect current state before retrying. A timed-out command may still be running; use its `job_id` with `bl_job_status` on the same Blender PID. Commands are not automatically retried or rolled back. Job history is in-memory and bounded; restarting Blender loses it.

Verify structure with fresh reads and appearance by viewing `bl_screenshot` or `bl_render`. Screenshots require a VIEW_3D area; headless renders need a scene camera. Rendering can block Blender while it runs. Set the MCP client's tool timeout above 300 seconds for long renders.

This package has no cloud generation tools or bundled bpy API/manual search. Use a separately connected Higgsfield service for generated assets; download results then call `bl_import_model` with an absolute local path. Read official version-matched Blender docs for unfamiliar APIs.
