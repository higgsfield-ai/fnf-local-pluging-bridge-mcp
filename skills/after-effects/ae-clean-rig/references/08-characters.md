# Character families, blink, gaze and parallax

For a character with articulated arms/legs, clothing, props and compositing passes, also read [11 · Character production](11-character-production.md). This module covers the simpler avatar/face rig.

## Character families and silhouette quality

For a named avatar or mascot system, inspect the actual product's base-shape set and primary design examples before inventing variants. Prefer clean source vector geometry when available. A set of twenty characters does not necessarily need twenty unrelated silhouette categories: use controlled proportion, orientation, colour and eye variations within the observed family unless the user explicitly needs distinct base geometries. When the user flags repeated silhouettes, recolouring, stretching or rotating the same base shape does not resolve that feedback. Develop visibly different silhouettes with consistent curve quality, and compare their outlines before animating.

Inspect each silhouette without eyes, at its final display size and enlarged. Look for unintended cusps, flat spots, pinched valleys, asymmetric corner transitions and self-intersections. Arbitrary radial points or automatic spline handles can make a mathematically valid path look broken. Preserve intentional asymmetry and meaningful lobes, with deliberate tangent continuity. If a source SVG is densely sampled, reconstruct or fit its static outline into a few meaningful Bézier arcs and verify the contour error visually; do not carry hundreds of sample vertices into an otherwise simple editable body.

When correcting a character's silhouette, preserve approved gaze, blink timing, control overrides and precomp identity. Reposition the face optically only where the replacement's centre or available interior changes, then check open eyes, a closed blink and extreme gaze positions inside the new body. Geometry containment is a technical check, not evidence that a silhouette looks good.

When the user requests subtle head parallax for a flat mascot, derive the added depth cues from the existing look direction: small relative face/body translation, restrained foreshortening and a short adjustable follow delay can preserve the graphic style. Expose an amount control whose zero value restores the prior motion. Check both the automatic cycle and the full advertised manual look range; narrow or rotated silhouettes may need smaller face travel. Do not add an independent idle oscillation to simulate this effect.

## Compact editable agent rig

Use one transparent precomp per agent. A practical structure is a controller null, one continuous BODY silhouette, two separate capsule-eye shape layers, a FACE helper and a shared-motion dependency if needed. Use only the meaningful vertices needed for that silhouette. Build the family cleanly before animating it; recoloring the same cloud is not a new silhouette when the user asks for distinct forms.

For a twenty-agent set, compare silhouettes together at the final grid size and in monochrome. Keep visual mass, margin and face placement coherent across the grid without forcing every body into identical geometry. The successful family used circle, squircle, diamond, wedge, oval, cloud, rounded triangle, drop, egg, hexagon, four-lobe, bean, pill, pentagon, heart, six-lobe, dome, leaf, fan and soft-cross silhouettes. These are examples of controlled variety, not a mandatory catalog or a claim that every shape is an official Grok asset.

## Blink and gaze

Expose Look X / Look Y, Blink, Tilt, body/eye colours, body proportions and eye size/spacing. Use a shared set of intentional gaze/blink curves with per-agent phase offsets for automatic motion. Allow manual animation; clearly define whether manual gaze offsets add to or replace automatic gaze, and clamp the final supported range. Keep a speed and motion amount control if useful.

Blink by reducing native capsule-eye height around its center with a short intentional close/open curve. Keep a small closed-eye height and recompute roundness from the current width and height so the eyes remain capsules through the blink. Do not let fixed corner radius or a failed expression turn the eyes into squares. Inspect the actual closed frame and intermediate frames.

A small shared motion library is easier to edit than independent dense key sets on every eye. Use different phases to avoid synchronized staring or blinking unless the reference calls for it. Preserve accepted gaze and blink timing while replacing body geometry. Keep optional breathing at zero unless requested or supported by the visual target.

## Subtle head-turn parallax

Derive face and body motion from the same Look signal. Let the eyes travel slightly farther than the body and let the body follow by a short adjustable delay. Add very mild foreshortening to body width and eye-pair spacing; avoid animated silhouette morphs for a simple head-turn illusion. This is a restrained 2D depth cue, not a volumetric 3D head.

Expose Parallax amount with 0 restoring the prior non-parallax motion, and Turn lag in frames or seconds with an explicit unit. In the accepted 30 fps example, a lag of 2.4 frames (about 0.08 s) and an amount of 70/100 were useful starting points, not universal presets. Scale travel to the character's dimensions and available face interior.

Test automatic poses and full advertised manual Look X/Y extremes, including diagonals, combined Tilt and maximum supported parallax. Narrow eggs and rotated diamonds may need smaller gaze travel than circles. Test open eyes and blinks at these extremes; clipping checks alone do not establish pleasant eye placement. Recheck neutral framing and prove that amount 0 retains the approved baseline.

## Carry-over evidence

When improving only silhouettes or parallax, compare source colours, comp identity, user overrides and existing motion keys before/after. Preserve the numbering and editable controls unless changing them is needed. Test a real manual edit through Essential Properties in the parent comp and directly through the source controller, explaining override precedence.
