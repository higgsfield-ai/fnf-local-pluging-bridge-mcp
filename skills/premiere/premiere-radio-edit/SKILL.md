---
name: premiere-radio-edit
description: Select and join recorded speech in Premiere for interview, talking-head, podcast and vlog edits. Use for cleanup, highlights, retakes or a target script, preserving meaning, breath, natural pauses and AV sync. Includes transcription fallbacks and speech-seam checks.
---

# Radio edit craft

Use `premiere-assembly` for execution and tool limitations. Source delivery and the requested tone take precedence over fixed craft timings.

## Editorial mode

Infer the mode from the request; clarify only if ambiguity changes what survives.

| Mode | Keep / remove |
|---|---|
| Cleanup | Preserve the argument; remove unwanted fillers, false starts, retakes and dead air. |
| Highlight | Select complete thoughts for the requested length, preserving qualifications that affect meaning. |
| Reorder | Move whole blocks and inspect every new join. |
| Target script | Match takes to the script; flag missing lines instead of constructing speech the person never said. |

## Transcribe and map time

1. Identify the speech source/track. Use available ASR or local transcription; do not assume the connector exposes speech-to-text. TTS is not ASR.
2. Extract audio if needed, following the engine's format/size requirements. Local Whisper can use 16 kHz mono WAV; an upload service may prefer MP3. A source extraction from zero retains source time. An edited sequence mix does not: preserve its mapping and avoid added music in ASR input.
3. Local fallback verified in the test: whisper.cpp with an installed model. If GPU allocation fails, use CPU mode (`-ng` in the tested CLI). Discover executable/model paths and check help; do not assume paths from the test machine exist elsewhere.
4. Inspect transcript and approximate timecodes. Preserve offsets when chunking; overlap chunks to avoid losing a boundary sentence. Silence level or ASR confidence alone does not prove a clean cut.
5. Build a phrase bank: thought, source ranges, take alternatives and missing context. Similar beginnings do not prove duplicate meaning.

If ASR is unavailable, direct listening or a supplied timed transcript can support selection. With neither, keep continuous takes and disclose the limitation instead of inventing phrase boundaries.

## Select complete speech

- Prefer one complete take per thought. Compare clarity, energy and context rather than automatically keeping the latest.
- Remove false starts as units. Join takes only at real phrase boundaries with meaning intact.
- Check repeated seam words ("…and so / and so…") and unique setup omitted by a retake.
- Remove unwanted hesitation noises where a clean seam is possible. Judge "so", "well", "like" and "but" by their role; a blacklist can strip meaning and natural rhythm.
- Preserve laughter/emotion with enough lead-in and release.

## Seams and breath

Cut in quiet intervals between phrases, not through consonants or sustained words. Keep inhales whole; they belong to the next phrase. Do not remove every breath to meet cadence.

Use server `pr_detect_silence` after a successful upload, or local analysis:

```sh
ffmpeg -hide_banner -i "INPUT.mp4" -vn -af "silencedetect=noise=-35dB:d=0.4" -f null -
```

Read `silence_start` / `silence_end` from stderr. Start near −35 dB / 0.4 s; raise toward −30/−25 dB if few pauses appear, lower the threshold if soft tails are classified as silence. These are starting points, not speech boundaries. Music/noise can mask pauses. Without a reliable interval, preserve a wider phrase boundary and inspect/listen rather than trimming harder.

For tight social edits, about 0.15 s before the first word and 0.2 s after the last can be starting targets; preserve more when breath/delivery needs it. Choose the quiet point nearest the intact phrase.

## Assemble picture and speech together

For talking-head footage, assemble AV ranges on explicit V1 (`track:"V",idx:0`), then inspect linked audio. Butt-join with desired breathing room included in source handles.

Do not use `pr_recompact_audio` as routine polish on linked AV: the tested build left extra video fragments. Do not assume `track:"A"` suppresses an AV item's picture. For audio-first work use an audio-only item, verify representative placement and set timing before picture.

For intentional gaps use explicit `at` with `butt:false`. `gap_after` belongs to audio EDL preview, not the Premiere cut plan. Audio gaps are silence, not room tone; picture gaps are black without coverage. Use source handles or a verified room-tone/coverage arrangement when continuity needs it.

After structural edits, inspect all affected V/A tracks and refresh IDs. `pr_split_clip` may split only the targeted video while audio remains continuous. J/L cuts require deliberate independent AV boundaries and a sync check.

## Rhythm and levels

Useful pause ranges: 0.1–0.3 s within a sentence, 0.3–0.5 s between sentences, 0.6–1.0 s between meaning blocks. Preserve deliberate longer pauses where appropriate. Count quiet source handles as well as inter-clip gaps.

Pass the actual speech track and allowed maximum to `pr_audit_audio_gaps`, for example:

```json
{"track_index":0,"max_pause_sec":1.0}
```

Do not demand a clean default 0.4 s audit while allowing 1.0 s pauses. Consider frame rounding near thresholds. Inspect findings; do not loop compaction until empty. Gap audit cannot evaluate internal silence, speech integrity or video artifacts.

Short fades can reduce clicks, not restore syllables. Correct clip-relative fade example for a 4.3 s clip at −2 dB:

```json
{"node_id":"<audio-clip-nodeId>","keyframes":[{"time_seconds":0,"level_db":-60},{"time_seconds":0.012,"level_db":-2},{"time_seconds":4.288,"level_db":-2},{"time_seconds":4.3,"level_db":-60}]}
```

Substitute actual duration/gain and inspect existing automation. Roughly 5–15 ms ramps are a starting point. `pr_reset_audio_level` clears keys; use it deliberately.

Measure comparable speech windows locally or with `pr_probe_media(...,loudness:true)`. Derive gain from level differences, account for existing gain/automation and check peaks. `pr_set_audio_level` takes absolute clip gain, not a relative correction. LUFS does not replace listening for timbre and room tone.

## Lock and verify

Lock speech before B-roll, titles, music and captions; re-map them after recuts. Do not globally fit video after manual crops/PiP.

At important seams check intact words/breath, meaning, repetition/omission, pause, level/energy and picture coverage. Read actual assembled order against the script. Transcribing the export is an additional content check, not proof of clean sound. Describe audio that could not be heard honestly. Report suspect seams with a short quote and timeline timecode.

## Voiceover to picture

For requested narration derive visual beat windows from footage, write lines that fit, use available authorized TTS, measure output duration and place audio-only items at those beats. Tighten an oversized script instead of speeding speech. Recheck after picture retiming. If generation is unavailable or spending declined, preserve existing audio and identify remaining narration work.
