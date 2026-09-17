# Read-Only Context Inspection

## Restore and locate the helper

Python helpers and JSON data are plain files under scripts/ and assets/ in this skill directory. The context helper is scripts/inspect_resolve.py; it uses official scripting getters and emits film-colorist-readonly-snapshot-2. It does not launch Resolve, switch pages or projects, select a grade, or modify processing. GetMediaPoolItem is used only to read source properties.

Use the helper's CLI with a compatible 64-bit Python interpreter and an available official scripting session. Its documented minimum is Python 3.6; the bundled helpers are tested with Python 3.9 or later. Native library compatibility remains a separate requirement. The helper reads RESOLVE_SCRIPT_API as the official Developer/Scripting directory; RESOLVE_SCRIPT_LIB identifies the native library through the official wrapper. Discovery of SDK files, successful import, and a connected application are distinct outcomes. A found but unimportable wrapper is not silently replaced.

The helper first requires GetCurrentPage to return color. Otherwise it reports not_color_page or page_unavailable without reading project context. Prepare the required page through the designated operator; the helper does not open it.

## Execution and output

The CLI supervises one child with a default sixty-second budget. The --timeout argument changes that budget; cleanup may add four seconds. Direct imported main and snapshot calls are not bounded in the same way. Filesystem operations and process creation are not hard-deadline guarantees. On timeout, do not treat the missing snapshot as an empty project. If cleanup_completed is false, do not start a replacement client while the earlier operation remains unresolved.

Use stdout or provide --output with a new JSON filename in an existing task directory. Output validation happens before vendor import. The helper does not create the parent directory or overwrite an existing report. Exclusive creation prevents a concurrent existing-file overwrite, but a later write failure can leave an incomplete new file. Choose a new path after a failure; do not assume that file existence proves complete output.

Exit zero means a JSON report was formed, not that its contents are complete. Read the top-level status and each nested status. An absent current project, timeline, or video item is reported only when the corresponding getter succeeds and returns no object. Missing or failing getters and unexpected types remain unknown with a reason. A confirmed graph with zero nodes is different from an unreadable graph. A no-group result is not_applicable only after a successful GetColorGroup call returns no group.

## Coverage and limitations

The snapshot includes available project, timeline, clip, version, timecode, limited color settings and media properties, accessible Clip node-stack layers, Timeline graph, and Group pre-clip and post-clip graphs. If the layer count is unknown, only the documented first layer is read and that limitation is retained.

Graph labels, counts, LUT names, and tool names do not establish RGB connections, enabled state, arbitrary OFX parameters, Shared-node identity, or the complete display path. The helper does not report unique object IDs. GetCurrentVersion provides a name and local or remote type, not an independent version ID. It leaves raw_decode_output unknown and cannot infer effective decoding from camera notes. No LUT in the Clip graph does not rule out managed, Group, Timeline, or monitoring transforms.

Diagnostic failures use exit two with a stage and reason, distinguishing runtime, wrapper discovery or import, session connection, snapshot reading, serialization, output validation, and writing. Argument-parser errors have their own format. A session connection returning no application does not distinguish all causes of unavailable access.

The supplied tests exercise fake SDK objects, errors, timeout ownership, and temporary-process cleanup. Historical live reports apply only to their recorded host and helper version. The current package does not certify another operating system, native ABI, every getter, or grading quality. Keep the helper read-only; separately authorized mutations require their own address, scope, recovery, and image verification.
