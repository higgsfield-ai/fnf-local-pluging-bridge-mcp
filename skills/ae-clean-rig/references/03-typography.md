# Typography, layout and construction diagrams

## Resolve identity before fitting motion

When a distinctive typeface is material to a reference match, check the source project’s credits or design case study before settling on a substitute. If the original is unavailable, compare a few full words and diagnostic glyphs (counters, terminals, M/N construction, numerals) in the actual AE render. Pixel overlap is supporting evidence, not a substitute for visual review; whole-word alignment and compression can mis-rank weights. Verify that AE resolves the intended installed font in every visible instance.

For tracking and translation animation, keep glyph proportions stable. Independently keying a fitted width, fitted height and tracking — while Scale divides by the changing sourceRectAtTime bounds — makes the text breathe or squash. Use fixed font metrics, native tracking and shared phase controls where the motion is shared. Let content edits reflow naturally or offer an explicit size/fit control; do not silently turn letter spacing changes into changing glyph width. Preserve an actual reference scale cut or deformation when it is visible.

For kinetic typography, distinguish a rotated glyph, a font-weight transition, a bespoke contour deformation, and a change of text before choosing the rig. Compare ordinary and extreme poses: easing the wrong representation cannot recover the reference. Use the native font for ordinary states and a few consistent-topology contour poses only for the actual custom deformation. Keep construction overlays separate from the editable wording and disclose if those overlays are specific to a logo or glyph.

For reveals, cuts, and montage cards, record the first visible frame and final hold explicitly. AE extrapolates the first key backward: a delayed type-on needs an initial zero value or a matching layer in-point. Validate the first frame before each reveal, the last frame before each cut, and the first frame after it. Do not infer global camera motion from a growing collage; measure persistent landmarks. For tracked particles, sample stable interior colours separately from geometry so black-to-colour transitions do not corrupt particle identity.

For construction diagrams, bind anchors, tangents, dimensions, and labels to the geometry they describe. Keep independent rules as separate paths; joining two vertical rules with one polyline introduces an unintended diagonal. Match circle proportions and shared angular phase before adding motion. A graph that grows along a curve must use a progressive path and related values, not a rotating pointer. Verify the actual font weight against the reference contour before compensating with scale or strokes. For typographic echoes, measure each copy’s offset, scale, first outline, first fill, and disappearance; a uniform offset stack can produce the wrong silhouette even with the correct text.

When showing typographic construction, use the meaningful curve extrema and corner anchors visible in the reference. A font may contain intermediate quadratic points that should not all become visible diagram controls. Preserve optical stroke and node sizes after fitting or scaling text: a correct pre-scale stroke width can become nearly invisible on a small glyph. Validate the final nested render at its intended viewing scale.

## Spatial typography and motion with a destination

Keep phrases together with a clear reading order and a readable hold. Use negative space and a deliberate contrast between supporting text and selected keywords. Take the type treatment from the chosen visual direction and any applicable reference; do not require one font pair across unrelated pieces.

When it serves the scene, attach text to a page, wall, card or object and match that surface's perspective, movement and occlusion. Keep phrases complete and do not cover meaningful faces or evidence. Solve legibility through placement, scale, timing and timed changes of text contrast before reaching for heavy decorative treatments.

Give continuous motion a destination that reveals or connects information. Inspect easing, stops, inertia and motion blur. Balance energetic passages with time to read and understand, and do not apply the same word bounce or camera pulse to every moment unless the requested treatment calls for it.
