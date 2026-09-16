# Face construction

## Eyes and brows

Read this reference when building or repairing a face. Preserve the reference's default expression and proportions. Separate white aperture, whole pupil, eyelid fill, visible eyelid contour and brow so movement has a clear owner. Use smooth cubic curves for rounded eyes; sparse polygon sampling can produce a diamond despite valid geometry. Under a pose blend or projection, transform both tangent handles consistently with their vertices.

Bound gaze and clip the entire pupil by the current eye aperture. White, clipping matte and visible opening must calculate exactly the same local boundary through gaze, independent eyelids and blink. Do not rely on a skin-colored cover to hide a pupil escaping its eye. At full closure use one lid line, and hide the white; avoid overlapping upper and lower outlines. A partially closed eye may narrow naturally without introducing corners into its fully open shape.

Check upper-lid volume and crease against the brow in neutral and expressive poses. Scale their separation to the artwork rather than copying a previous character's pixel values. Where a forward nose hides an eye or crease, supply an opaque skin nose volume beneath its shading and contour. Shorten occluded crease paths with rounded endpoints before the holdout when clipping would leave a pointed fragment.

## Mouth and jaw

Remove the original mouth from the head base. Use a single current aperture and lip contour, driven by opening, expression and any required mouth poses. Interpolate compatible geometry or select a complete pose cleanly; avoid crossfading two visible mouths. Closing must restore one line without a leftover lip shape.

When internal anatomy is requested, separate the throat cavity, palate, uvula, tongue and optional teeth, all clipped to the same live mouth opening. Keep the palate above and tongue below, with the uvula attached to the palate. Animate details within that structure rather than floating them independently across the lips. Derive jaw extension and mouth placement together so large openings remain below the nose and inside the moving face. Inspect small openings as well as fully open poses.

## Local evaluation and expression

Keep face controls local to the rig instance and forward them across precomposition boundaries. The visible lip and clipping aperture must agree in the final nested render, not just the source composition. If a cross-layer path read ignores Essential Property overrides, calculate both boundaries from the same local controls instead of relying on a source-comp lookup.

For requested line boil, use restrained, adjustable contour variation with coherent sampling across fill and matte boundaries. Begin geometric QA with boil and motion blur disabled, then inspect the final effect. Keep motion, hair response and facial acting intentional; unrelated perpetual random movement does not add volume.
