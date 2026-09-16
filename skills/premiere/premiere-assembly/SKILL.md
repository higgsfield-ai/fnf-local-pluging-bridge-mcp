---
name: premiere-assembly
description: Assemble and revise editable Adobe Premiere Pro timelines with the connected pr_* tools, from importing footage and placing selected source ranges to checking tracks, framing, audio and exports. Use for Premiere montage and timeline edits; pair with premiere-radio-edit for speech selection and premiere-editing-reference for specialized operations.
---

# Premiere assembly

Turn selected footage into an editable Premiere sequence and verify the result. When the user requests a finished video file, delivery includes a Premiere export, not just a plan or saved project.

This replaces the earlier `premiere-api-realities` skill. A build that still exposes only `pr_get_skill(name:"premiere-api-realities")` is on the older lookup enum; do not send `premiere-assembly` to an enum that does not accept it. Read this module through the skill lookup the installed server actually accepts, and use its contract either way.

## Connect and identify

- Discover the registered tools first. If no `pr_*` tool is present, the Premiere tool family is not registered in this build; report that plainly and stop at analysis rather than describing an edit as executable. Distinguish file analysis from tests actually performed in Premiere.
- Read the active sequence and project items. Prefer timeline clip `nodeId`, project item `nodeId`, and sequence `sequenceID` over potentially duplicated names.
- Refresh `pr_get_active_sequence` after a user turn and structural changes. Use the IDs and timings from that read for the next mutation.
- Build a new sequence for a new edit; use the existing sequence when revising it. Clearing a sequence is a deliberate destructive operation, not a setup requirement.

## Value contract

- API times are seconds; boundaries are quantized to sequence frames. Read actual ends before computing subsequent placements. `in` / `out` are source times; `at` is timeline time.
- Indexes are zero-based: V1/A1 = `0`, V2/A2 = `1`. Pass them explicitly for assembly, audio audit, compaction and ducking; tool defaults differ.
- Audio gain is in dB: `0` is unity, not measured voice loudness. Fade keyframe times are clip-relative; do not add the source in-point yourself.
- Position is normalized: `position_x:0.5, position_y:0.5` = center. `scale` is percent (`100` = original); cut-plan `punch` is a multiplier (`1.15` = 15% above its base scale).
- Read live schemas for supported fields. A successful response does not override observed behavior.

## Assemble

For a new video edit prefer `pr_assemble_edit`; for placements into the active sequence use `pr_apply_cut_plan`. Plan item example:

```json
{"item":"<project-item-nodeId>","in":2.0,"out":5.4,"track":"V","idx":0,"at":0,"butt":true}
```

`butt:true` places subsequent items at the previous item's actual end; their `at` is ignored. Use it for contiguous cuts on one track, with separate passes for layers. Use `butt:false` and explicit `at` for intentional spacing. `gap_after` is not a Premiere cut-plan field. Preserve natural pauses inside source ranges where possible so they do not create picture gaps.

1. Import source media and select content-based ranges. For speech use `premiere-radio-edit`.
2. Execute the plan, then read all V/A tracks. Confirm ranges, count, order, timing and linked audio.
3. Lock main timing before B-roll, graphics, music and captions. Reposition dependents after later recuts.
4. Adjust framing per clip, verify and save.

For audio-only assembly from AV footage, use an extracted audio-only project item. In the tested build, `track:"A"` with an AV item also placed video. Verify a representative placement before expanding. Do not blindly remove unexpected video that may overlap user content.

## Compatibility limits observed in Premiere 26.5.0.99 (2026-09-16)

These observations are version-specific. Re-test affected operations on a disposable sequence before relying on a different build.

| Operation | Observed behavior and route |
|---|---|
| `pr_recompact_audio` on linked AV | Moved audio, changed V1 and left extra video fragments. Avoid automatic compaction on linked AV. Assemble AV ranges together with intended pauses; test audio-only sources separately and inspect every track. |
| `pr_color_correct` | Returned `Invalid parameter` after changing repeated parameter names in multiple Lumetri sections. Inspect properties after errors. Name-based setters are suitable only for unambiguous properties; otherwise use available UI or preserve the grade and report the limitation. Verify the affected section and frame. |
| Transition / clip speed | Cross Dissolve application failed; speed change failed to locate a clip after split. Keep a suitable hard cut or original speed unless a verified alternative is needed. |
| `pr_create_caption_track` | Reported `created:true, verified:false, captionTracks:0`, yet a caption appeared in the exported frame. Inspect a cue before retrying to avoid duplicates. |
| Cloud frame export / upload | `PLUGIN_TIMEOUT` occurred even for a small upload. Use local `pr_export_frame` for timeline stills and local source analysis when available. |

Errors can follow partial edits; successes can omit requested behavior. Re-read affected tracks/properties and inspect the result before recovery. After a mutation timeout, redo only confirmed missing work. Do not repeat an identical failing call without new evidence.

## Framing

`pr_fit_all_video` resets framing broadly; it is not final polish after manual crops or PiP. Run it only when every affected clip should be reset, then inspect frames. Neither `fit:true` nor a success count proves full canvas coverage.

Decide per clip whether to contain the full picture or crop to cover. For unscaled square-pixel footage, initial estimates are `100 × min(targetW/sourceW, targetH/sourceH)` for contain and `100 × max(...)` for cover. Existing frame-size scaling, pixel aspect and transforms can change the effective base; verify first. Check subjects and existing captions/logos at edges. Use a contained layout with a background when cropping would lose protected content. See `premiere-editing-reference`.

## Audio and analysis

Correct fade arguments:

```json
{"node_id":"<audio-clip-nodeId>","keyframes":[{"time_seconds":0,"level_db":-60},{"time_seconds":0.012,"level_db":-2}]}
```

For a full clip preserve intended gain with another key near its end before fading out. Keep keys within actual duration. Roughly 5–15 ms micro-fades can reduce clicks; they cannot restore clipped words. Resetting level clears automation, so use it deliberately.

`pr_audit_audio_gaps({track_index:0,max_pause_sec:1.0})` checks gaps between A1 clips. Match the threshold to allowed pauses. It cannot detect internal silence, lost words, clicks, loudness or video fragments.

Server probe/silence/beats/sync requires a successful upload and its key. Respect the current size cap. With local tools available, analyze locally or extract compact audio. A source extraction from zero preserves source time; an edited sequence export uses sequence time. Keep the mapping before transferring cut points.

Do not assume Higgsfield speech-to-text exists. Discover available ASR or use a local engine; the tested fallback was whisper.cpp on CPU. Local ffmpeg can prepare audio, proxies and stills. A requested Premiere edit remains an editable sequence with its Premiere export.

## Verify and deliver

- Structural: fresh sequence read including all affected V/A tracks, ranges, intended gaps, end time and dependents.
- Visual: export and view actual timeline frames, through `pr_export_sequence_frame` or local `pr_export_frame`. Inspect seams, protected text, representative crops and settled animation.
- Audio: combine timing/transcript checks with listening where available. Do not call a gap audit proof of clean sound or measured loudness.
- Export: save, render through Premiere/AME when requested, then check actual duration, dimensions, streams and representative frames. Vertical output needs an appropriate or verified Match Source preset.
- Report actual project/output paths and unverified features. A plan or passed schema check is not a finished edit.

Generation is separate from montage. Use available authorized services, preserve visual style and honor spending limits. Existing footage can complete an edit without generated inserts.
