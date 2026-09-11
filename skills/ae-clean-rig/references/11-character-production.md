# Articulated characters: artwork → rig → poses → composite

Use this module for illustrated characters with independently moving limbs, a face, clothing or held props. A simple two-eye mascot normally needs module 08 instead. Follow the current task's application constraints; in this user's AE-only studies, construct the artwork inside AE rather than introducing an Illustrator dependency.

## Establish the actual motion before designing the rig

Inspect clean and occluded reference frames. Separate whole-scene motion, character/vehicle movement, limb gestures, changing face shapes, fluid/ribbon deformation and foreground occlusion. Different elements may have different periods. In the flying-bottle study, image measurements revealed a one-second bottle translation cycle; the overall reference/gesture/atmosphere was treated over two seconds. A visual contact sheet alone initially suggested the wrong period.

Use measurements to identify extrema and fit a sparse trajectory. Sampling every source frame for analysis or QA is allowed; that is not a reason to put an animation key on every frame. Preserve real contact points and phase relationships. Clouds that hide a hand are not evidence that the hand disappears or changes shape.

## Artwork before rigging

Make a usable neutral pose first. Separate head/hair/face, torso, upper and lower limb pieces, palms/fingers, shoes, clothing and held props according to their actual motion and overlap. The design can use a few custom Bézier silhouettes when ellipses and rounded rectangles cannot preserve the reference. A semantic contour is different from a traced patch of colour.

Give a garment its own designed contour; a constant-width bone capsule is often a poor trouser or sleeve. When independent rigid segments distort the intended silhouette, a compact rest contour with two-bone skinning can preserve the garment. Keep vertex topology stable, expose the rest contour, and bind its vertices/tangents deliberately to the bones; moving a target should deform the same authored contour rather than swap frame drawings. Adding vertices also requires reviewing the skin weights. Overlap the upper/lower artwork under the intended joint edge so bending does not expose seams. Put a shoulder's skin below the sleeve and the forearm/palm on the correct side of the torso. Verify the painted rest pose with effects and foreground occluders disabled before tuning motion.

Keep illustration details editable: label marks as a few open paths, facial features as separate groups, and words as native text. If converting deliberately authored path data into AE, preserve separate subpaths as separate groups; joining multiple move commands into a single contour can connect eyes, finger lines or shirt folds accidentally.

## Controller and coordinate design

A practical hierarchy is:

- a character root for shared transforms;
- hips, torso and head controls, with pivots at the meaningful joint;
- hand/foot IK target nulls with ordinary editable Position;
- elbow/knee pole controls that determine bend direction;
- hidden joint/solver helpers and visible named artwork;
- a separate pose-source layer for measured automatic offsets.

Use two-bone IK where end contacts matter; use FK or a small, consistent-topology deformation where it fits the reference better. Do not introduce a puppet mesh merely because the object is a character. A head turn that reveals new surfaces needs additional designed poses, not an unlimited scale/skew approximation.

For analytic IK, convert the start, target and pole into one declared coordinate space before solving. In a root-local solution, use root.fromComp(control.toComp(anchorPoint)), rather than subtracting unconverted parented Position values. Derive joint location with the law of cosines, choose the bend side using the pole, and handle coincident/unreachable targets explicitly. A bounded stretch/reach option should have clear units. The rendered hand/foot must use the solver's reachable endpoint too; otherwise the limb can stop short of a freely moving palm or shoe.

Drive both segment artwork transforms from the same solved joints. Reposition the complete wrist/ankle assembly, including palm, fingers, cuff, shoe and prop, from the endpoint. Keep twist/foot rotation independently editable. Test a moved parent and a moved endpoint together; testing only neutral root transforms will miss coordinate-space errors. After reparenting, explicitly set the intended local anchor, position, scale and rotation for each attached detail. AE can retain transform compensation; a small prop foot or cuff can detach even when the main hand is correct.

## Manual posing and reference playback

Put automatic offsets on a parent/helper, leaving the advertised hand/foot Position controls free for user keys. Preserve a clear way to disable automatic motion. A useful arrangement has a reference-loop checkbox, a phase control, motion amount controls and a sparse source-pose library. A manual template can be a real independent copy of the character rig with automatic motion disabled.

Document ownership: a manual target may add an offset to an automatic pose; a source or instance override may replace another value. Do not expose a slider that has no visual connection. Exercise face controls as well as limb controls. Blink should contract each eye around its own local centre, rather than moving the whole eye layer toward the head's origin.

Fit independent curves for the observed gesture and shared motion; keep holds where the reference holds. Snap intended pose events to source frame times. Use temporal/spatial curves suited to the trajectory and compare between poses. Do not add idle breathing, head bob, extra foot swings or arbitrary noise to make the rig appear sophisticated.

## Compositing as editable passes

After the rig works, add lighting, contact shadows, material variation and texture as distinct, named passes. Put the rider, vehicle and the attached part of a fluid trail under the same flight transform. Keep distant and near atmosphere separate so the foreground can cross the subject without becoming part of its artwork.

Clip contact shadow to the receiving surface. A duplicated character alpha with native Drop Shadow can serve as the shadow source, but share the same pose and timing; do not maintain a second independent shadow animation. Verify that assigning a layer as a track matte did not switch off the receiver/artwork's visible rendering.

Use native gradients and soft light for material illumination. Keep printed colour regions distinct from moving illumination. Expose the useful light/material parameters and check that changing them affects the intended pass.

Choose texture coordinates intentionally: object-attached surface grain and a screen/film overlay are different looks. For static paper grain, a native noise precomp sampled at a fixed time avoids frame-to-frame boiling; clip/blend it with the intended object. A global blur does not fix a rough silhouette or a broken joint.

Inspect blur bounds and Repeat Edge Pixels explicitly. In this study a blur's edge repetition produced rectangular colour-field edges; setting it appropriately restored the soft field. Verify rendered alpha/edges instead of blindly enabling that option on every blur.

## Validate the rig, then record the lesson

Render a clean neutral pose, maximum reference bend/gesture and at least one manual pose with automatic motion off. Move a hand, a foot and the hips/torso, edit a material colour and a facial control, and verify connections, overlap, contact and clipping. Check the advertised reach limit as well as comfortable poses. Save the intended settings after the test.

Review a native motion render at normal playback speed and at matching reference timestamps, including intervals partly hidden by foreground effects. Check that the loop boundary, parent motion and independently phased gesture remain coherent. Count meaningful artwork, helpers and source keys honestly; a three-layer main comp can still hide a broken or dense construction.

Deliver the animated scene, editable rig/manual entry point, required dependencies and a usable preview. A reference layer may be an explicitly labelled guide or audio-only source, never the hidden rendered character. Distinguish a measured structural reconstruction from unproven pixel-exact fidelity. Keep aesthetic acceptance separate from technical rig validation, and refine this workflow using the user's actual corrections.
