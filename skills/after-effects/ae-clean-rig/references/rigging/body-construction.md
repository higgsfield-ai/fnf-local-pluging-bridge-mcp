# Body construction

## Hierarchy and sockets

Read this reference for torso or limb work. Define whether side labels mean anatomical left/right or screen left/right in neutral, and apply that convention consistently. Build rest landmarks from the actual reference. Head, neck, torso, hair and clothing remain independently editable wherever their movement requires separation; parenting does not require merging their artwork.

Place pivots at the intended joints and preserve the neutral appearance when assigning parents. Parenting may compensate transforms, so do not then treat local values as unchanged world coordinates. Use one solver space for roots and targets. If body volume changes, project sockets and limb geometry consistently using the volume reference; do not turn only the costume artwork.

Conceal complete shoulder roots beneath the actual foreground costume or body surface, with filled geometry behind them. Do not raise an entire arm above the costume merely to reveal its hand. Check foreground and background sleeve exits in both turn directions. Where a gesture crosses the torso, design the required forearm/hand occlusion explicitly while retaining hidden roots.

## Limb mechanics

Use bounded two-bone IK, FK or a suitable bendable shape according to the requested motion. Keep joint radii and overlapping fills compatible; internal stroked end caps should not form visible rings. Clamp reach between the difference and sum of the segment lengths with a small nonzero margin, and constrain inverse-cosine input to its valid interval. Handle unreachable targets deliberately without numerical explosions or silently stretching the limbs.

Choose bend direction from the character's anatomy and camera view, then verify the signed hip-knee-ankle relationship and the silhouette. Do not apply a frontal character's left/right signs universally. Test planted feet, each lifted foot, a crouch and the opposite planted leg. Foot targets intended to stay on the ground must not inherit body turns. Report target error against reachable targets or the deliberately clamped endpoint, as appropriate.

When only body yaw changes and hand offsets remain neutral, preserve the projected rest-arm pose. Projected endpoint positions with unchanged planar bone lengths can create an unintended elbow bend. Use consistently projected rest lengths or another coherent spatial solver.

## Hands and secondary parts

Identify whether the reference shows a palm, back of hand or side before authoring wrist motion. Use a wrist frame and a recognizable thumb with correct handedness. A flat rotation of a dorsal hand does not create a palm-facing gesture. If a palm/back turn is needed, author compatible views and a rounded side thickness, preserve finger length and suppress a collapsed primary outline near the edge-on position.

Extend the hand beneath its cuff. Inspect the connection with a flat cuff or an appropriate artwork-specific opening rather than covering the palm with a rounded sleeve cap. Test both hands in rest, raised and intermediate turn poses. Use delayed keys for secondary rigid parts; load the Puppet reference only when a flexible part needs actual mesh deformation.
