---
name: ae-clean-rig
description: Creates, edits, reconstructs from a reference, animates, simplifies and renders compositions in a live After Effects session through the connector's ae_* tools, preserving reference appearance and motion with clean editable rigs instead of dense traced shapes. This is the ENTRY skill and router for all After Effects work: it carries the start-of-task checks, the construction and motion-fidelity doctrine, its own ten reference modules, and the table naming any further module a request reaches. Fires whenever the user asks to create, change, animate, rebuild, fix or render anything in After Effects (AE, Adobe After Effects), or names any ae_* tool. Load this one skill and let its tables route the rest; nothing else is loaded ahead of it. Does not apply to video editing outside AE.
---

# After Effects: clean construction, faithful motion

Treat the reference's appearance and motion as the target, and editable semantic construction as the method. Reducing complexity must not turn a distinctive reference into a generic approximation. Apply these decisions to text, objects, interfaces, backgrounds, and effects throughout the composition.

This skill preserves the practices learned from the user's AE iterations: the Duolingo chest, native UI and products, typography and gradients, Higgsfield media, controlled galleries and 3D loops, Coverflow, and editable agent characters. Read the relevant detailed module below when that kind of work is involved; do not load every module for a small correction. Current explicit user instructions override saved defaults.

## Essential workflow

0. Read everything the request touches from the two tables below — the reference modules of this skill, and the companion skills — before the first mutating `ae_*` call. This file is deliberately incomplete: the construction rules, motion evidence tests, rig conventions and delivery gates live in the modules, and work produced without the matching module is invalid even when the calls succeed.
1. Inspect the current AE project through the available bridge/API. Discover current capabilities; do not assume yesterday's port, project ID or app version. Save a separate backup before structural changes and work in a named iteration. Keep unrelated compositions intact.
2. Establish the baseline: inspect the supplied reference at actual timestamps, or use the approved existing comp for an edit. Record both moving and stationary elements, cuts, holds, direction changes and important poses. Build a compact map of semantic components and motion. Do not infer missing motion from what an object usually does.
3. Choose the simplest representation that preserves the design: native text for editable wording, a few meaningful primitives/clean paths for graphics, native controls/effects for UI, and actual depth for products when visible. Do not build surfaces from dense traced fragments, crop reference screenshots into finished objects, or generate UI as a bitmap.
4. Put each independently useful object in a named precomp and give ordinary edits a clear source. A separate media placeholder must really have independent content. Expose useful controls on a null and, where appropriate, Essential Properties. Preserve existing user keys and overrides when correcting appearance.
5. Use sparse intentional native keys and curves, shared motion controls and the right built-in effects. Preserve reference-supported bounce, overlap and settling; add no arbitrary motion. Do not hide dense animation behind an expression or precomp and call it simple. Keep actual custom deformation distinct from transforms and font changes.
6. Validate the native result: compare intermediate motion as well as key poses, resolve expression errors, inspect the nested render, and test one real content/control edit. Save a working AEP with required media and a completed usable preview. Report material differences honestly and retain a return path to the previous version.

## Read the module that changes the current decision

| When the task involves | Read |
| --- | --- |
| Simplifying an object, choosing shapes versus text/media, building UI, logos or 3D products | [01 · Construction](references/01-construction.md) |
| Reconstructing a reference, fixing extra motion, preserving timing, sparse keys and curves | [02 · Reference and motion](references/02-reference-motion.md) |
| Fonts, kinetic type, tracking, glyph deformation, diagrams and typographic construction | [03 · Typography](references/03-typography.md) |
| Gradients, colour flow, travelling light, glow, native ribbons and surface warps | [04 · Gradients and effects](references/04-gradients-effects.md) |
| New photographic stills or footage, generation settings and source packaging | [05 · Higgsfield media](references/05-higgsfield-media.md) |
| Precomps, replaceable elements, null controls, Essential Properties and shared sources | [06 · Editable rigs](references/06-editable-rigs.md) |
| A gallery, Coverflow, cyclic slider, curved 3D loop or user-animatable camera | [07 · Controlled sliders](references/07-sliders.md) |
| Mascot/agent silhouettes, blink, gaze, smooth head turns and subtle parallax | [08 · Characters](references/08-characters.md) |
| Final checks, 2K upgrades, render defects or delivery/packaging | [09 · Validation and delivery](references/09-validation-delivery.md) |
| Scripting/expressions, bridge timeouts, property references or renderer inconsistencies | [10 · AE scripting](references/10-ae-scripting.md) |

## What the user asked for decides which skill to load

Check this table on EVERY request, including a follow-up to work already done. Having read this router is not the same as having read the module a new ask needs. Load through `ae_get_skill`; these are modules of this procedure, not alternatives to it, so where one contradicts the doctrine above, the doctrine wins. Load only the rows the request hits.

| The user wants | Load |
|---|---|
| a frame, screen, card or scene rebuilt to match a reference image or screenshot | no companion skill — work it from the reference modules above, starting with 02 |
| a whole layout described in words, with no reference to match | `ae-ui-mastery` for the design values |
| a new screen, section or component invented from scratch — spacing, type sizes, colour roles, component specs | `ae-ui-mastery` |
| something to move, or to move differently — timing, speed, easing, stagger, an entrance, a loop, an expression-driven motion | `ae-animation-principles` |
| a glass, frosted, glassmorphic or refractive panel, pill, button or bar over a background | `ae-liquid-glass` |
| more depth or space — parallax, atmosphere, a push-in, defocus, a floor, or a fix for "it looks flat" | `ae-depth-space` |
| a transition between shots, a seam effect, or a `.mogrt` for the Premiere transition library | `ae-transition-kit` |
| a frame that is genuinely faster to write once as one HTML mock or one Lottie JSON than to place natively | `ae-design-first` — optional; the native build needs neither |
| a font, gradient, travelling light, slider, character rig, generated still or footage, or a delivery check | no companion skill — these are the reference modules above |

## Adding to a composition that already exists

An addition or a correction is not a new build, and the work already accepted is a constraint on it.

- Load the module for what is being added, apply it to that element, and leave the rest of the composition alone.
- Do not restart the reference-match pipeline from measurement when nothing new is being matched.
- Do not re-run whole-composition finalize or audit passes for a local change.
- Do not apply a default entrance to elements that already animate.
- Preserve existing keys and fitted curves, exposed controls and their values, layer and comp names, precomp identity, and approved media. A module loaded for the addition does not authorize normalizing any of them.
- Where the new instruction genuinely conflicts with earlier work, say so and change only what the instruction requires.
- Validate the change and whatever depends on it, not the whole composition again.

## Saved preferences that affect tool choice

- Create required photographic footage through Higgsfield with **Seedance 2.5 at 1080p** and still images with **Nano Banana Pro at 2K**, unless the current task specifies otherwise. An explicit **Soul 2.0 at 2K** request takes precedence. Verify current model availability and actual returned media dimensions; do not silently replace the model or moving footage with a still. Preserve already approved media during unrelated fixes.
- Keep text, buttons, prompt windows, construction diagrams, captions and simple graphics native and editable. Keep clean authentic standalone logos when available. Use generated imagery for appropriate image/footage content, not as a way to flatten an editable interface.
- Preserve requested resolution, aspect ratio and frame rate across the hierarchy. Native vectors are not inherently the cause of rough rendering: diagnose fragmented geometry, sampling, effects and colour depth before choosing a local fix.
- When the user asks for a controllable rig, manual control must work directly. Keep optional demo timing separate and document units/ranges. Do not require the user to repair hidden duplicate layers for routine changes.
- If the user reserves acceptance or says to stay on one case, continue that case until they accept it. Routine authorized reversible work does not require an extra approval gate. If the user moves on, do not keep polishing the old case without reason.
