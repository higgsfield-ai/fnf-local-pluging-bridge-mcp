# Recut from a video reference

Use this branch when rendered language versions must match a supplied short edit in separate compositions. Preserve the selected After Effects workflow and do not begin a new text localization unless requested.

## Establish the reference and frame map

Inspect actual media type, duration, frame rate, resolution, and content even if the user calls a video an image or banner. A supplied reference layer can define the requested editing, camera, and composition even when disabled in the final composition. Equal source durations do not prove that language versions are synchronized. Preserve the project state with imported sources before building compositions.

Review the reference and locate its scenes. Match reference frames to the longer source using visual features or reduced images, reducing the influence of translated text regions. Use contact sheets for navigation, not proof of an exact cut.

Infer continuous segments, cuts, speed changes, repeated sections, and freezes from the sequence of matches. Unstable nearest-frame matches in static scenes do not alone establish variable speed. Refine cut boundaries and offsets at larger image sizes and validate every language version independently. Use rational frame-rate and speed relationships. If reliable correspondence is unavailable, identify the missing source or unresolved method instead of claiming frame accuracy.

Record the plan in integer frames with inclusive output starts, exclusive output ends, source starts, playback rates, and frame-selection methods. Derive all values from the current sources rather than reusing an earlier edit's scene count, duration, or speed.

## Composition and audio assembly

Create a composition for each requested version and a separate reference composition for comparison. Match the user's language and source naming conventions, retain sources, organize the new compositions in a clear folder, and mark cuts.

Use trimmed, unstretched layers for normal-speed sections. For changed speeds, reproduce the observed frame-selection method with linear remapping or stretch, or with discrete HOLD keys when the reference demonstrably skips frames without blending. Do not add frame blending or optical interpolation automatically. Follow the Time Remap handling in [10 · AE scripting](10-ae-scripting.md).

Choose audio deliberately: arbitrary cuts through the long source's music may disrupt accents. For a matched banner without speech requiring replacement, retain the continuous reference audio and disclose that choice. Resolve audio source selection when speech languages or tracks differ. Do not silently replace the spoken language. With one master audio track, mute other video-layer audio to avoid a doubled mix. Check audio enablement and active time independently from video visibility, then listen to the result during available preview and authorized export verification.

## Branch acceptance

Verify the source frame selected at every output frame and check the start, end, and both sides of every cut. For hard cuts, confirm exactly one active video layer and no gaps or accidental overlaps. For intentional transitions, validate their actual overlap structure. Check output dimensions, frame rate, duration, and playback speed.

Apply the save, reopen, visual verification, export approval and delivery requirements in [13 · Localization](13-localization.md). Record whether complete playback with sound was performed. Structural checks alone do not establish visual accuracy. Show the language compositions in the Project panel or their tabs when the user wants to inspect them; do not create duplicate files or export video merely to demonstrate where compositions are stored.
