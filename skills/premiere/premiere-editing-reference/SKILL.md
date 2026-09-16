---
name: premiere-editing-reference
description: Choose Premiere pr_* tools and recipes for framing, B-roll, music, captions, effects, transitions, multicam and export. Use alongside premiere-assembly when an edit needs specialized operations or recovery from a tool failure. Catalog availability does not imply runtime verification.
---

# Premiere tool reference and recipes

Read `premiere-assembly` for addressing, units, assembly, verification and tested compatibility limits. Read only the recipes relevant to the task. The current live schema governs arguments; some operations below were not exercised in the 2026-09-16 test.

## Tool map

| Job | Tools |
|---|---|
| Project / sequence inspection | `pr_get_project_info`, `pr_list_project_items`, `pr_list_sequences`, `pr_get_active_sequence`, `pr_list_sequence_tracks`, `pr_get_sequence_settings` |
| Clip inspection / selection | `pr_get_clip_properties`, `pr_get_selected_clips`, `pr_select_clips_by_name`, `pr_deselect_all_clips` |
| Sequence lifecycle | `pr_create_sequence`, `pr_create_sequence_from_clips`, `pr_set_active_sequence`, `pr_set_sequence_format`, `pr_ensure_tracks`, `pr_clear_sequence`, `pr_save_project` |
| Import / bins | `pr_import_media`, `pr_create_bin`, `pr_import_mogrt` |
| Assembly | `pr_assemble_edit` (new sequence), `pr_apply_cut_plan` (active sequence), `pr_fit_all_video` (broad framing reset) |
| Placement / editing | `pr_add_to_timeline`, `pr_overwrite_to_timeline`, `pr_remove_from_timeline`, `pr_move_clip`, `pr_trim_clip`, `pr_split_clip`, `pr_replace_clip`, `pr_copy_clip_transform`, `pr_close_gaps` |
| Transform / speed | `pr_set_clip_transform`, `pr_set_clip_speed` |
| Tracks | `pr_add_track`, `pr_delete_track`, `pr_set_track_lock`, `pr_set_track_visibility`, `pr_set_track_mute` |
| Audio | `pr_set_audio_level`, `pr_reset_audio_level`, `pr_add_audio_fade`, `pr_duck_music`, `pr_add_music_bed`, `pr_recompact_audio`, `pr_audit_audio_gaps` |
| Analysis / source views | `pr_upload_media`, `pr_probe_media`, `pr_detect_silence`, `pr_detect_beats`, `pr_sync_media`, `pr_render_audio_edl`, `pr_extract_audio`, `pr_extract_frames`, `pr_compare_angles` |
| Multicam | `pr_build_multicam_video` |
| Effects / transitions | `pr_apply_effect`, `pr_list_available_effects`, `pr_remove_effect`, `pr_color_correct`, `pr_add_transition`, `pr_list_available_transitions` |
| Properties / animation | `pr_get_effect_properties`, `pr_set_effect_property`, `pr_add_keyframe`, `pr_set_keyframe_interpolation` |
| Markers / playhead | `pr_add_marker`, `pr_list_markers`, `pr_delete_marker`, `pr_set_playhead_position` |
| Text / captions | `pr_set_mogrt_text`, `pr_create_caption_track` |
| Timeline still / export | `pr_export_sequence_frame`, `pr_export_frame`, `pr_export_sequence`, `pr_add_to_render_queue` |
| Skill lookup on an older build | `pr_get_skill` (its enum may still carry the pre-revision skill names) |

### Shared operation rules

- Fresh read after structural changes; use current IDs and actual frame-quantized ends.
- When layering into an occupied range, use a suitable free higher track. Overwrite/delete only when the requested edit calls for replacing content.
- `pr_close_gaps` changes the timeline arrangement; dependents on other tracks may retain old times. Inspect linked audio and all affected tracks. It is not an automatic finishing pass.
- Avoid `pr_recompact_audio` on linked AV in the tested build: it left stray video fragments. Audio-only compaction needs a disposable representative test first. Explicitly pass the speech track and pause bounds, then inspect all tracks, not just the audio audit.
- `pr_split_clip` may leave the linked counterpart unsplit. Check both sides before retiming or making J/L cuts.
- `pr_color_correct` can partially mutate multiple Lumetri sections and still error. `pr_set_effect_property` is also name-based: use it only if the desired property is unambiguous. For repeated names that cannot be addressed precisely, use UI control or leave the grade unchanged and report the limitation.

## Media analysis and local fallback

`pr_upload_media` returns a key for server probe/silence/beats/sync. Check current upload limits before sending a large file. A timeout occurred even for a small file in the test; reduce size only when size is actually the issue, not as an identical timeout retry.

| Need | Local route, if tools are available | Connector route |
|---|---|---|
| Source duration, streams, dimensions | ffprobe | `pr_probe_media` after upload |
| Speech transcription | Installed ASR, with its supported audio format | Discover an actual ASR tool; editing tools do not supply one |
| Silence / loudness | ffmpeg analysis on the relevant audio track | `pr_detect_silence` / `pr_probe_media(loudness:true)` |
| Source moments | Local stills/contact sheet | `pr_extract_frames` / `pr_compare_angles` |
| Timeline proof | `pr_export_frame` to disk, then view the returned file | `pr_export_sequence_frame`, then view the image |
| Large source requiring remote analysis | Compact audio or time-preserving proxy | `pr_extract_audio` can export a sequence mix, then upload |

Example source-audio extraction:

```sh
ffmpeg -i "INPUT.mp4" -vn -ac 1 -b:a 64k "speech.mp3"
```

Select the intended stream explicitly if the source contains several. Keep the extraction's source offset. A sequence mix uses timeline time and may contain music; it is not interchangeable with original-source timecodes. `pr_render_audio_edl` is an audio preview/extraction route, not a Premiere timeline mutation. Its `gap_after` field does not belong in a cut plan.

Source stills help select footage; they cannot prove that a timeline effect or crop applied. For local frame export, inspect the returned path: the tested tool sometimes appended `.png` to an already suffixed path. Do not assume a requested filename exists.

Keep remote DSP concurrency modest and reduce it after timeouts. No analysis upload is necessary for a local job that can already be checked locally.

## A. New rough cut or selected speech reel

1. Import local `file_paths` or authorized media `urls`; inspect source content and metadata.
2. Build the new sequence with `pr_assemble_edit` and explicit tracks, or use `pr_apply_cut_plan` in the intended active sequence.
3. Inspect all tracks, source ranges and seams; fit/reframe only where needed, then save.

Example argument for contiguous AV selections on V1:

```json
{"plan":[{"item":"<project-item-nodeId>","in":2.0,"out":5.4,"track":"V","idx":0,"at":0,"butt":true},{"item":"<project-item-nodeId>","in":9.1,"out":12.0,"track":"V","idx":0,"butt":true}]}
```

Use `premiere-radio-edit` for choosing speech ranges. Retain intended breaths in source handles. Do not automatically compact linked audio afterwards. Before layering, audit the explicit speech track with the intended maximum pause, and examine picture continuity separately.

## B. Vertical reframe with protected content

1. Read source and sequence dimensions, pixel aspect, existing transforms and representative frames.
2. Set the intended sequence format, for example `{"width":1080,"height":1920}`. This tool sets dimensions, not frame rate.
3. Choose contain or cover per clip. Frame-size fit is not a guarantee of fill; the tested global fit left black fields in a vertical frame. Read the resulting scale and inspect actual output.
4. Adjust scale/position manually where required, checking face, product, text and logos throughout movement. Existing burned-in text cannot be reflowed like editable captions.
5. If cover destroys content, keep a sharp contained foreground over a suitable background. A blurred duplicate is one option: place both on free higher tracks and inspect the layout. Blur/effect availability needs verification.
6. Do not apply global fit after per-clip crops, split screens or PiP. Export with an appropriate/verified Match Source preset and check dimensions.

For 1080×1920, top 10–12%, bottom 18–25% and right 8–12% margins can be conservative starting guides. Platform UI and placement vary; inspect the intended presentation. No `pr_set_safe_zone` tool is exposed: use deliberate positioning.

## C. B-roll over speech

Ensure free tracks, then place B-roll on a higher V track with `drop:true` to remove its linked audio:

```json
{"plan":[{"item":"<broll-project-item>","track":"V","idx":1,"at":3.0,"in":0,"out":2.0,"drop":true}]}
```

Inspect the audio bed after placement; linked-track behavior must be verified. A cutaway should explain the current point or cover a speech join. Return to the speaker for emotional lines; use longer coverage over a cluster of joins when clearer. Choose full screen, split or PiP by readability. Avoid a global fit pass once the layout is authored.

## D. Music and ducking

Lock the content end and inspect free audio tracks. A typical one-call bed uses explicit indices:

```json
{"item_id":"<audio-only-project-item>","music_track_index":1,"speech_track_index":0,"duck":true,"duck_db":-18,"ramp_sec":0.3,"fade_in_sec":0.5,"fade_out_sec":2,"overlap_sec":1.5}
```

`pr_add_music_bed` tiles on the chosen track and its neighbor, so reserve both (A2/A3 here). Verify tile starts/ends, crossfades, ducking keys and final content end. Use audio-only items for manual audio placement.

`pr_duck_music` uses speech clip spans, not signal-driven voice detection. Long clips with internal pauses can stay ducked; pauses between speech clips can return toward unity, which may be too loud. Check both speech and pauses. `duck_db` and `pr_set_audio_level` are absolute gain values, not relative offsets or measured mix loudness.

For manual fades use `{"time_seconds":0,"level_db":-60}`-style keys, with clip-relative times and explicit plateau keys. Preserve existing automation when appropriate. Trim a long track; tile a short one with supported overlaps. Do not retime music just to fit duration. Measure the exported mix and listen where available; structure alone does not establish audio quality.

## E. Titles and captions

Inspect an actual target-time frame before choosing placement. Existing captions may already be burned in.

- **MOGRT available:** import its absolute path, inspect returned text fields and use `pr_set_mogrt_text`. Adjust duration according to the template's supported controls; do not trim through an entrance/outro without checking it.
- **Static graphic without MOGRT:** a locally rendered transparent PNG can provide exact text, but its text is rasterized and not editable in Premiere. Choose this when it fits the requested deliverable; use an editable template/UI route when editable typography is required.
- **After Effects:** use only if available and appropriate to the requested workflow. It is not required to complete a Premiere cut.
- **Captions:** import SRT as a project item, then call `pr_create_caption_track` with its `item_id` and intended offset. SRT does not guarantee house styling or karaoke.

Caption creation returned `created:true` with a failed verification/count in the test, while the rendered caption was visible. Check an active cue in a timeline frame before retrying; also inspect an out-of-cue frame and the final export. Do not duplicate a caption track based only on `verified:false`.

## F. Effects, animation and transitions

Inspect available effect/property names and units before writing values. Scale keyframes and Bezier interpolation worked in the test; that does not verify every effect or interpolation. Supported interpolation enum values are `linear`, `hold`, `bezier`, not custom handle curves.

Choose a seam for an editorial reason: hard cut on action, hold for readable text, match/carry for continuity, or an occlusion/change for a scene reset. Avoid decorative transitions by default.

When a native transition is needed, an exact-name call can resolve even if enumeration is empty. If it resolves but application errors, read state and stop repeating it. Cross Dissolve did fail this way in the tested build.

Alternative paths, subject to a representative check:

- A suitable existing MOGRT, with its actual timing and transparency verified.
- Crossfade: overlap incoming video on a higher free track and ramp only its opacity from transparent to opaque. Ensure source handles, correct property units and sufficient outgoing coverage. Avoid also crossfading dialogue unless intended.
- Dip through black: outgoing fade, cut, incoming fade when that pause suits the story.
- A scale/blur transition using available inspected properties, if the added motion serves the edit.
- A hard cut when appropriate; unavailable effects are not a reason to generate an insert.

Inspect outgoing/incoming boundary frames and the midpoint; sample animated titles after they settle and near their exit. A single still does not establish smooth motion. Continuous time-remapping is not exposed; after any constant-speed attempt, verify changed duration/source timing and AV sync. The tested post-split speed call failed, so do not treat segmented ramps as a guaranteed workaround.

Generated seam bridges require a separately authorized generation task/budget and supported start/end-frame input. Honor declined spending; keep an existing-footage solution when generation is not authorized.

## G. Beat montage

Detect actual music beats locally or through `pr_detect_beats` after upload, then place markers and use selected strong beats for visual changes. Verify representative detected beats against audio where possible. Preserve speech/meaning if it conflicts with the grid. Beat detection does not certify the whole edit's pacing.

## H. Multicam from recorder and cameras

This route was not runtime-tested in the audit. Establish sync on a small representative section before building a full edit.

1. Use an audio-only recorder item for the speech master. Identify the actual scratch/reference and external audio roles.
2. `pr_sync_media` takes `ref_key` and `ext_key`; inspect its result and verify offset sign with a clap/visible event. Treat confidence as a diagnostic, not sufficient proof.
3. Select speech ranges and intended pauses before camera construction. Avoid unverified compaction of linked AV.
4. `pr_build_multicam_video` takes explicit audio/video track indexes and per-recorder `takes`. Each camera entry uses `item` and `offset` (not `offset_sec`); the schema defines camera source time as recorder time minus that offset. Translate/verify sync results accordingly.
5. The builder replaces the target video arrangement; use a dedicated sequence/track whose contents may be replaced. Inspect sync at the beginning and end of long takes, then check actual camera source ranges against the edited recorder ranges.
6. Save after verification; do not run a final gap-closing pass that invalidates the established timing and dependents.

## I. Export and delivery

Save the editable project. Export directly through `pr_export_sequence`, or queue with `pr_add_to_render_queue` when AME is available. An accepted queue request is not a completed file.

For a vertical sequence do not rely on an unspecified default preset. Pass an appropriate `.epr` or verified Match Source preset; a Match Source export produced 1080×1920 in the test. Check actual dimensions and duration regardless of preset name or warning. Preset locations vary; find an installed file rather than inventing a path.

Wait for completion, confirm the output exists and decodes, and check streams, duration, dimensions, seams, captions and audio. Compare the real final sequence/export with the intended edit. Deliver the actual file and editable project when requested; note missing media or unverified features without claiming full certification of this catalog.
