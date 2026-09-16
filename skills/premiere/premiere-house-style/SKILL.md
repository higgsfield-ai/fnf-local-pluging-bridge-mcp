---
name: premiere-house-style
description: Apply the Higgsfield Reels house style to short-form vertical Premiere edits: hook, visual cadence, restrained punch-ins, product B-roll, designed captions, sound and color. Use when that style is requested or appropriate to the brief; adapt targets to speech clarity, source framing and available tools.
---

# House style — Higgsfield Reels

Creative defaults for energetic 9:16 edits, not platform requirements or proven retention guarantees. The user's brief, readable content and intact speech take precedence. Use `premiere-assembly` for tool contracts and verification, `premiere-radio-edit` for speech.

## Hook and cadence

- Make the opening stake clear in the first few seconds. Choose a claim, curiosity gap, visual interruption or proof-first opening that the footage supports.
- Aim for an early visual change around 2 s when it helps the hook. A graphic or B-roll change can supply energy without cutting spoken words.
- Use cadence as a wave: establish → demonstrate quickly → slow for explanation → build energy → let the close land.

| Phase | Starting shot-length target |
|---|---|
| Open | about 1.5 s |
| Demo | about 1.1 s |
| Explanation | about 2.5 s or longer for clarity |
| Action | about 0.8–1.2 s |
| Close | enough time to understand the final action |

These visual targets do not require a speech cut every 1–2 s. Retention and view effects require actual audience analytics; do not promise numerical improvements from an editing device.

## Framing and movement

- Light punch-in: about 1.15–1.25 times the established base framing. Cut-plan `punch` is a multiplier; transform `scale` is an absolute percentage. If the base scale is 177.8, a 15% push is about 204.5, not 115. Read the actual base and verify protected content.
- Rotate useful visual changes: framing, text, B-roll, sound accent or angle. Do not add effects merely to hit a timer.
- A 60/40 split can pair action with interface proof when both remain readable. Show input before result where the brief is a product demonstration.
- Continuous time-remapping is not exposed by these tools. Constant-speed segments are only an approximation, and `pr_set_clip_speed` failed in the tested build after a split. Do not promise a ramp until representative retiming works and AV sync/duration are verified. Original speed is the default fallback.
- Vertical conversion requires per-clip inspection. Global fit does not guarantee cover and may undo manual crops/PiP. Preserve faces, product details and burned-in captions; use contain plus background when cropping loses them.

## B-roll

Use B-roll to prove or clarify the spoken point. For a product reel prefer actual output or usage to generic illustration. Short 0.8–1.5 s inserts and visual changes every few seconds can work, but a longer cutaway may better cover several speech joins. Return to the speaker for emotional/key lines.

Land changes on musical accents when compatible with meaning. If a beat and a phrase boundary conflict, preserve the phrase; change the visual independently or choose another beat. Do not alter speech merely to satisfy both grids.

## Text and captions

- Large bold sans-serif, white with sufficient contrast; highlight key words in yellow or a consistent accent.
- At 1080×1920, 48–60 pt is a starting size, not a guarantee across fonts/templates. Check the rendered frame at viewing size.
- Use short readable groups, often 3–7 words and under roughly 30 characters per line; adjust to language, delivery and space. Avoid flashing long text too briefly.
- Captions are the house default for spoken reels, unless the user requests otherwise. Reuse suitable existing burned-in captions instead of duplicating them.
- Word highlighting needs word timing and a template/graphics path that supports it. SRT plus `pr_create_caption_track` provides timed captions; it does not by itself guarantee karaoke animation or house styling.
- The tested caption tool returned `verified:false` despite visible captions. Inspect an active cue and an out-of-cue frame before retrying. Check the final export for caption inclusion.
- Keep palette/type/motion consistent while adapting layouts to their editorial purpose. Use cards when a bounded reading surface helps, not on every insert.
- Use conservative margins as a starting point (top about 10–12%, bottom 18–25%, right 8–12%); inspect against the intended platform placement rather than claiming those are universal safe zones.

## Sound

- Choose music that supports the voice and mood; instrumental hip-hop/electro suits the energetic variant. Existing footage may already contain music: inspect first.
- Clip levels are gain values, not guaranteed mix balance. Music at −15 to −20 dB under speech and up to −6 dB in a voice-free insert are starting points only. Measure/listen and adjust for source loudness.
- Keep voice clear and intelligible. Unity gain is not a loudness target; compression and EQ depend on the source and available verified controls.
- Use whooshes/clicks at motivated accents, avoiding constant effects that compete with speech.
- For music generation, specify mood, energy, editorial role and instrumental/no-vocal requirements where needed. Honor the user's spending limits. Detect the real beat grid after import; prompt text does not establish exact beat timing.
- `pr_add_music_bed` can trim/tile/fade/duck. Pass `music_track_index` and `speech_track_index` explicitly; tiling uses the neighboring audio track too, so inspect its contents first. Verify all tiles and the content end.
- Ducking sets absolute gain under detected speech clip spans; it is not a measured sidechain compressor and can miss silence inside a clip. Ramps around 200–500 ms are a starting point. Inspect keys and listen to representative speech/pauses.

## Loudness and color

Choose and state a delivery loudness target. A practical house starting target is −14 LUFS with true peak below −1 dBTP; these are house choices, not claims of mandatory platform normalization. Measure the actual mix/export, apply supported gain/limiting if needed, and remeasure. Gain alone is not two-pass loudness normalization and may breach the peak limit. Do not report normalized audio merely because clip gain was set.

Creative color options: warm face/cool background for a studio, controlled contrast/saturation outdoors, or a deliberately cold archive treatment when appropriate. Preserve skin tone, readable UI and continuity.

`pr_color_correct` partially mutated multiple Lumetri sections and errored in the test. Avoid it as an unchecked batch grade. Inspect/target exact properties or use available UI and verify the affected sections and rendered frame. LUT application needs its own verification.

## Close and delivery

For a product reel, end with one clear action and enough reading time, often about 2 s. Do not invent a sales CTA for noncommercial material. Save the editable sequence and export when requested. Verify framing, text, intact speech, duration, dimensions and measured audio; separate achieved styling from features that remain unverified.
