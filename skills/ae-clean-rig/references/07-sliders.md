# Gallery, Coverflow and complex 3D sliders



## Select the correct construction

Measure the reference's card count, front-card size, overlap, side angles, depth, rounding, stage bounds and camera perspective. A curved gallery, a Coverflow stack and a loop with straight stretches and tight bends are different rigs. Do not turn a complex loop into a generic circular carousel because both contain cards. For a still reference, match the neutral layout first, then make the simplest smooth movement consistent with that layout and the user's controls.

Use a distinct precomposition for each independently replaceable card. Each card's CONTENT holds its media; captions are native text and graphic treatments remain native AE layers or effects. Add a clearly named REPLACE MEDIA source. Automatic Cover/Fit must account for the source and comp pixel aspect ratios, while retaining a way to adjust framing. Do not combine all cards into an atlas or crop them out of the screenshot.

## One Slide control

Place the main Slide slider on a named null. A useful index convention is 1 = first card, 2 = second, with fractional values giving intermediate positions; keep the convention consistent across all expressions and the guide. For an N-card cyclic rig, normalize indices with positive modulo, conceptually `((x % N) + N) % N`, because a plain remainder can fail for negative input. A full-loop percentage convention such as 0–100 is also valid when clearly labeled. Never mix conventions invisibly.

Derive card position, orientation, depth, emphasis and related shading from the same Slide value. Maintain continuity through wraparound and front-card handoff. Resolve depth/sorting changes where cards actually exchange order, without a visible teleport, opacity pop or extra sway. Put timing on Slide with sparse editable curves. Keep optional demo keys separate, with manual control effective by default when that is the task.

Expose only useful layout controls: spacing, side angle, depth, gap, bend radius or overall tilt as appropriate. Add per-card offsets/width only when needed. Essential Properties may expose Slide to a parent composition, but nested media sources still need deliberate uniqueness.

## Curved gallery

Keep the center card readable while side cards follow the measured fan/perspective arrangement. Rounded corners should belong to the card construction, so swapping a photograph cannot destroy them. Retain live surrounding headings and labels. Test the largest visible card and the smallest side card with the actual content: a good source image can still crop badly in perspective.

## Coverflow

Use real 3D card planes when the user needs camera animation. Preserve the front-facing central card and the reference's side spacing, rotation and overlap. Use native editable bottom shading and captions above the image, with a restrained side-dimming control. For a rounded black stage on a larger background, place the 3D scene inside a stage precomp and apply the stage boundary at the parent level; avoid flattening the cards themselves.

Keep a separately animatable camera inside the relevant stage. Name its location in the guide. Do not lock its Position/Orientation behind expressions that prevent the user's planned camera move. A camera orbit null may provide an additional clean control.

## A loop with straight segments and bends

Build the actual path topology: straight runs, transitions and bends in their observed proportions. Parameterize travel along distance when needed to maintain consistent spacing and apparent speed; an arbitrary curve parameter need not correspond to uniform distance. Derive continuous orientation from the path/tangent, verify AE's rotation convention, and inspect the joins between straight and curved portions.

Each card must remain its own object and its own content comp. If cards visibly bend, a native renderer/deformation that preserves the reference may be appropriate; use built-in Cinema 4D curvature only when available and verified for that construction. A rigid-card loop needs rigid cards. Never substitute an image atlas moving over stationary surfaces for individually moving cards.

Keep real geometry clipped to the intended visible card. Check back faces, occlusion and surfaces hidden around bends in the native renderer: zero opacity may not remove their depth/occlusion contribution. In the tested rig, zero scale disabled a hidden surface; revalidate this behavior for the renderer in use rather than assuming it universally.

Separate camera control from path/Slide control. Test the rig from a modest alternate camera angle; a setup that only survives its original view does not meet a request for an animatable camera.

## Verify the control, not only the demonstration

Test integer, fractional and negative Slide values, the loop seam, a full cycle, forward and reverse movement, and a manual keyframe sequence. Check interpolation between cards and repeated cycles. If there is a camera, test a camera move. Replace one card with a different aspect-ratio image, use a longer caption where applicable, and verify that unrelated cards retain their own content. Restore intended originals after the test. Explain any genuinely fixed layout limitations.
