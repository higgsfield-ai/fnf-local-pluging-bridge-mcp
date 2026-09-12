# Verify the local connection

Use this conversation's tools from **higgsfield-use-blender**:

1. `bl_health` must return the actual Blender version, PID, active file and scene.
2. `bl_get_scene_summary` must return current scene contents.
3. Before edits, load `bl_get_skill` with `name: "blender-scene"` and inspect relevant objects. View a screenshot or render when visual evidence is needed; a mutation is not necessary for a connectivity check.

Successful `doctor` output proves a local shell-to-Blender round trip. It does not prove that this conversation has discovered the MCP tools. If tools are absent, inspect the intended client's server configuration, paths, startup error and tool restrictions, then refresh its connection. Do not claim conversation control until its local MCP call succeeds.

No bridge: verify the add-on is enabled in the intended Blender instance, both processes run as the same user and their runtime directories match. Multiple bridges: select the intended `BLENDER_MCP_PID`; never silently pick the first. Health works but commands wait: Blender's main thread may be busy or blocked by a modal operation. Wait/check job status before retrying mutations.

A timeout or execution error can leave partial changes. Use the returned `job_id` with `bl_job_status` on the original process. History is bounded and disappears when Blender exits; inspect scene state if the result is unavailable. No automatic retries or rollbacks occur.

Screenshots require a VIEW_3D area. Use a camera render in a headless session. macOS/Windows/Linux support is intended, but report only platforms and Blender versions actually verified; never treat Python unit tests as live Blender validation.
