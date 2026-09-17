---
name: davinci-film-colorist
description: Grade film and video in DaVinci Resolve Studio, analyze frames and visual references, configure color pipelines, match shots, and verify the result. Use for requested Color-page work or practical training in Color tools and built-in effects. Excludes editing, compositing, audio work, and final video delivery.
---

# Film Colorist

Turn an observed image problem or creative intention into a justified correction and verify its effect on the frame and scene. Preserve an accepted image when a change does not serve the brief. Respond in the user's language and read control names and values from the actual interface.

## Scope and requirements

Work on the Color page, including Nodes, Scopes, Gallery, masks, tracking, built-in effects, Camera Raw, and necessary project color settings. Deliver a verified Color grade and available control frames. Editing, compositing, audio, and final video delivery require a separate workflow. Do not replace source faces, objects, geometry, or motion through generative redrawing. Identify a separately requested mockup as an illustration.

Use the project, material, range, and display target established by the current request. Preserve sources, editing, accepted normalization, and a usable return state. A historical project, path, camera, coordinate, or measured setting is evidence of that session only. The supplied skill does not itself establish application access, a license, a complete API, or a currently verified technique.

Before processing material, obtain the user's Input Color Space and Input Gamma for the specific file or explicitly covered group. Reuse an existing confirmation for that material. Metadata supports a proposed pair but does not replace confirmation. Reconfirm affected material after a profile, effective RAW decode, or transcode change, or when the actual signal conflicts with the recorded input. While waiting, continue independent preparation or confirmed clips only if shared processing cannot affect the unconfirmed material. The confirmed source pair does not describe the signal after an earlier transform.

The personal workflow uses native Resolve tools for technical white balance and exposure. Do not generate or apply exposure or white-balance LUTs or DCTLs. Keep those corrections in separate technical nodes and verify their working gamut and Node Gamma. Treat Linear RGB Gain as a preferred white-balance method to consider, not an automatic replacement for suitable RAW controls or every other native method. Saturation is a separate decision. Replace a historical exposure DCTL only in a recoverable new grade version and verify the result.

For a new grade, the established pipeline is unmanaged DaVinci YRGB with a DaVinci Wide Gamut / DaVinci Intermediate timeline. Place input conversion first, then any needed denoising, white balance, primary exposure, secondary exposure, secondary color balance, an accepted tonal foundation when needed, the global HF-Astra-Looks, and the final output conversion. Each secondary group uses independent branches joined by its own Parallel Mixer. Preserve an accepted existing RCM or ACES project unless a migration is requested. Do not add a second display transform.

HF-Astra-Looks is the principal creative look dependency. It operates in DWG/Intermediate before the output transform. Keep the LOOK global: subject masks, windows, qualifiers, luma keys, and external matte or key inputs belong in secondary correction before it. Preserve an accepted separate tonal foundation. A manually built display-referred look after output requires an explicit current request and a verified domain; do not move the original HF DCTL there. Choose the actual output from the confirmed display target. Rec.709 / Gamma 2.4 applies to the agreed SDR workflow, not every delivery.

## Start and select references

For an application task, read [access and recovery](references/autonomous-workflow.md) to establish the current Color page, project, timeline, clip, grade version, and available tools. If an official scripting session is available, read [context inspection](references/resolve-scripting.md). Otherwise use an available permitted GUI route. Report the specific access limitation while continuing independent analysis.

When source identity or decoding needs investigation, read [camera identification](references/camera-identification.md). Select the matching camera reference only when that source family is established: [ARRI](references/camera-arri.md), [Sony](references/camera-sony.md), [Blackmagic RAW](references/camera-blackmagic.md), or [RED, Canon, and Panasonic](references/camera-red-canon-panasonic.md). Before constructing, migrating, or diagnosing a signal chain, read the relevant section of [color pipeline](references/color-pipeline.md). Before changing connections or grade scope, read [nodes and keys](references/nodes-key-practice.md).

Before the first correction, consult the relevant diagnostic section of [correction principles](references/color-correction-handbook.md). For palette relationships, read [color relationships](references/color-relationships.md). For final brightness, highlight placement, or local light relationships, read [exposure decisions](references/exposure-decisions.md). Read [light and color](references/light-and-color-basics.md) when a signal or perception distinction remains unclear. Do not load the full library or reread an unchanged reference before every node.

For a full grade or matching assignment, read [scene production](references/scene-production-workflow.md). For visual intention and attention, read [taste and evaluation](references/taste-workflow.md). When choosing the strength of contrast, saturation, denoising, split tone, or a film look, read the relevant section of [perceptual decisions](references/perceptual-decisions.md). When the user supplies creative references, use [reference comparison](references/reference-look-cases.md) to identify transferable relationships. Treat project-specific titles and creators as inputs, not preset identities.

When using HF-Astra-Looks, read [its dependency and parameter contract](references/hf-astra-looks.md). When a tonal prototype is requested or useful, read [tonal shaping](references/tonal-shaping.md); it is optional and does not establish a measured film profile. For a requested native alternative, select a relevant section of [native look techniques](references/native-look-recipes.md). Do not add paid third-party dependencies as mandatory requirements.

For interface navigation or selecting a control, read [Color fundamentals](references/resolve-fundamentals.md) or [control selection](references/color-tools-atlas.md). Load [Primaries, Log, HDR, and Curves](references/primaries-log-hdr-curves.md), [Warper and ColorSlice](references/color-warper-practice.md), [masks and tracking](references/masks-tracking-relight.md), or [noise and texture](references/noise-texture-practice.md) only for the relevant operation. For effects, select [effect selection](references/effects-tool-atlas.md), [effect contracts](references/resolve-effects.md), [film and restoration](references/effects-film-color-restoration.md), or [light and optical effects](references/effects-light-mapping-optical.md) according to the decision.

For measurement, read [scope diagnostics](references/scopes-and-diagnostics.md) or [scopes during grading](references/scopes-in-grading.md). For faces and continuity, read [skin and matching](references/shot-matching-and-skin.md). For stills, DRX, or grade transfer, read [Gallery and comparison](references/gallery-matching-perception.md). When the task needs provenance or the exact tested scope, read [evidence access](references/evidence-access.md); historical material does not replace current verification.

## Decisions and completion

Establish the brief, inspect the frame and available scene, identify the main subject and distracting regions, and preserve the baseline. Prepare and balance the source, prototype on representative available material, refine attention and matching, then assess texture and motion. For one clip, scale the process to available moments. Create several distinct variants when exploration is requested; an explicit look does not require three alternatives.

Before a meaningful change, state the observed problem, desired relationship, and stopping criterion. Use one purposeful task per node with a verified label. After the change, reassess the whole image and accept, weaken, or undo it. Preserve motivated lighting, material differences, and intentional scene changes. Neither slider values, scope traces, genre names, nor increased overall brightness determine artistic success.

Make local exposure work unobtrusive. Evaluate the actual intersection of windows and qualifiers, matte edges, ordinary image, node bypass, and available motion. Correct halos, unstable keys, visible boundaries, and an artificially isolated subject before acceptance. Reduce noise reduction or sharpening when it damages useful texture; do not wait for the user to identify lost detail. An unavailable control limits execution, not the diagnosis of an image need.

One operator owns the shared Resolve session, including reads that seek or change selection. Any authorized independent helpers work from supplied artifacts and follow the user's applicable model requirements. Preserve operation ownership through pending calls, then recheck context before subsequent actions.

For interface training, verify control location, purpose, actual response, and restoration. Artistic improvement is a separate criterion. For a completed grade, verify the active version, signal chain, native frames, relevant cuts, available motion, and saved result. Reopen exported stills or grades when claiming successful export or transfer. A still does not validate tracking, temporal processing, or a finished video master.

Report what changed, what was observed, and material limitations. Distinguish verified in the application, partially verified, studied from a source, unverified, and blocked by access. Store task records beside the current task. Update persistent skill knowledge only when skill development is requested. Use current official documentation for uncertain control behavior and distinguish text, sampled frames, audio, and continuous-video access when recording source coverage.

## Scripts and data

Python helpers live in `scripts/` and JSON data beside the LUT and DCTL files in `assets/`, as plain files. Run them from this skill directory; no restoration step exists. The `.cube` and `.dctl` files are large and must not be read into the reasoning context; address them by path.

For read-only context, use `scripts/inspect_resolve.py` according to the context-inspection reference. For HF installation, `scripts/install_hf_astra.py` requires an explicit `--lut-dir`, verifies `assets/HF-Astra-Looks/manifest.json` and the bundled DCTL hash, and defaults to dry-run. Only `--apply` writes verified missing files. It refuses different existing files and does not operate Resolve. After an authorized installation, refresh the actual LUT list in Resolve and verify compilation and native output separately. The tonality DCTL and `.cube` files in `assets/tonality/` are installed the same way, by copying into the Resolve LUT directory.

The historical measurement dumps formerly embedded here (`references/practice-evidence`, `references/video-evidence`) are archival and are not distributed with this skill. When a reference cites them, report the missing provenance rather than inventing results.
