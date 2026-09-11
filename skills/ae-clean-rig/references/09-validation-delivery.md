# Native validation, resolution and delivery

## Verify and deliver an iteration

- Compare new renders against the reference at identical timestamps: initial pose, movement extrema, transitions, final pose, and frames around fast events. Inspect at full output resolution as well as playback speed. Compare the whole frame and component crops; a few attractive stills do not establish animation fidelity.
- Check for seams, color banding, shimmering, disconnected parts, font substitutions, clipped effects, missing media, blank frames, wrong duration, and audio drift. For overlapping surfaces, extend the hidden part behind the foreground edge; independently fitted touching boundaries can leave animated antialiasing gaps. Preserve the visible edge instead of blurring the seam. Confirm a render file exists and is complete; a queued job or successful script return is not a finished render.
- Audit real complexity recursively: compositions, layers, shape paths, shape keys, numeric animation keys, text layers, and dependencies. Inspect the actual interpolation types and density of the resulting keys, not just the count of shape paths. Do not hide complexity behind precomps or report only the top-level layer count.
- Keep the output resolution and frame rate the user requested. When upscaling an existing comp, inspect nested comps and footage sampling; changing only the main comp dimensions is insufficient. Recheck masks, effects, stroke widths, anchors, and positions.
- Deliver a saved AE iteration plus a usable preview or comparison, and describe material remaining differences honestly. Do not claim “1:1” unless the evidence supports it. Retain a reliable return path to the earlier version.
- Incorporate the user's visual corrections into the same example. If the user explicitly reserves acceptance or says to stay on one example until approval, do not declare it approved or move to a harder example on their behalf. Routine authorized edits do not require a new permission checkpoint.

## Quality and portability

Treat 2K as a requested output tier that still needs concrete dimensions and aspect ratio. Preserve the established dimensions unless the task changes them; do not force every 2K task into a square or the same long-edge convention. Distinguish a Half/Quarter preview from a Full final render. Check nested sampling, image dimensions, effect bounds, antialiasing and suitable project bit depth when diagnosing rough edges or gradient bands. Fix the local source of a defect before applying any blanket blur or upscaling.

Before expensive rendering, inspect expression errors and missing dependencies in the render hierarchy and render a representative frame. Then inspect a completed native motion preview covering the changed behavior and relevant transitions. A successful bridge return or external illustration is not proof of an AE render.

Deliver the saved AEP with relative packaged media dependencies and a usable preview. Retain any required editable 3D sources. List needed fonts and plugin/renderer dependencies; include font files only when redistribution is permitted and their terms are included. State material substitutions and remaining match differences without describing an unverified result as exact. Explain how to replace content and which control to animate.

## Check both resemblance and regressions

Keep two comparisons distinct: current AE versus the original tests fidelity; current AE versus the saved previous render finds unintended changes. A shared character can be correct in its import scene but broken much later. After changing a shared source, review its other consumers even if their scene layers were untouched.

Use a sparse full-timeline comparison to locate differences, then inspect original-resolution consecutive frames at each suspicious event. A sampled pixel-difference threshold is a triage tool, not proof of motion quality or pixel identity. Record the sampling rate, expected change ranges, exceptions reviewed and actual checks performed; do not widen an exclusion range merely to make a scan pass. Sampled checks cannot certify every intervening frame.

For the changed behavior, include entrance, full pose, pose changes, contact/extrema, exit and both sides of cuts. Inspect complete-frame layout and character/detail crops together. Verify advertised manual pose/build/phase controls, normal transforms and a real text or content edit; restore intended values even if a check fails. Keep visual acceptance separate from the absence of expression errors.

Validate delivered media metadata: concrete dimensions, frame rate, frame count/duration and audio alignment. A corrupt or unfinished movie can exist on disk. Confirm exported stills exist and decode too. If assembling a review from separately rendered native segments, preserve exact frame ranges, colour interpretation, audio continuity and provenance; this must not introduce an external-only fix absent from the saved AEP. Package current previews clearly, keeping superseded comparisons out of the primary review set.

## Learn from feedback without overstating the result

Carry the user's confirmed corrections into future work: simpler semantic geometry, editable source text/media, reference-supported motion, deliberate gradients, controller-driven rigs and real rendered checks. An accepted iteration does not establish that every creative style has been mastered. The open-ended Apple-style text exercise and the ALL IN font substitution case received weaker feedback; use their concrete failure lessons, not a promise that a similar effect stack will produce an approved result.

For an open-ended brief, establish a coherent visual direction, type system and motion logic before adding effects. Keep the user's request moving; do not introduce a mandatory approval stop for routine reversible work. If the user has supplied a reference, its actual design and timing take priority over a generic style recipe.
