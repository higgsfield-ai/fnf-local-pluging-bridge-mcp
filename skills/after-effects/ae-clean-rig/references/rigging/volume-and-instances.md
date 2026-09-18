# Volume and instance ownership

## Dimensional movement

Read this reference when the user requests depth, head turns or dimensional body motion. Define the supported range from the available design and reconstructed surfaces. Frontal and three-quarter motion can be a limited 2.5D rig; do not promise a rear view or full rotation without the needed artwork.

Provide separate horizontal and vertical turn controls for the face and, when requested, the body. Use a coherent projected surface or a compatible pose bank. Silhouette, cheek exposure, feature depth, near/far widths, shading and occlusion must respond differently. Moving every feature by the same offset, applying only in-plane rotation, or rotating an intact flat image does not produce the requested form change.

A pose bank must retain matching topology and blend vertices plus both tangent handles with identical weights. A projection must apply one sign convention, pivot and coordinate system to artwork, attachment landmarks, shading and limb frames. Avoid projecting twice through an additional equivalent turning parent. Preserve rounded body thickness through its visible contour while front details move over the surface; reveal reconstructed side geometry as needed.

Keep nose, eyes, mouth, cheeks and face rim at meaningful relative depths. Compress the far side without negative scales or feature collapse. Keep a face opening attached to its costume while its internal form turns. Body-only turns, face-only turns and counter-turns should remain independently recognizable.

## Instance ownership

Use local controls and forward Essential Properties at every nested precomposition boundary. Shared immutable pose data is acceptable; a control expression reading a named global rest composition makes independent characters share a pose and is not acceptable. Keep the rest rig manual and unkeyed, with animation in a separate performance composition.

When repairing an existing project, locate dependent source and demonstration compositions plus user-authored instances before changing control routing. Preserve names and keyframes that already work. Update the intended shared sources or all relevant copies explicitly; do not leave an obsolete manual rig while fixing only the demonstration. Verify two nested instances with opposite body/face turns and different mouth or hand states, and confirm the source defaults remain unchanged.
