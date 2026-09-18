# Geometry and Cropping

## Coordinates and hierarchy

Use local frame dimensions rather than rotated document bounds. Express a node in the retained parent's coordinates by composing its absolute transform with the inverse parent absolute transform. Do not assume a captured relative transform already targets the retained parent. Both applications use rightward horizontal and downward vertical coordinates.

Apply parent relationships before assigning local transforms. Account for native center anchors versus source origins exactly once. Transform vertices with the complete affine matrix and tangent offsets with its linear part only. Preserve shear through supported native transforms or transformed geometry; do not discard it during rotation and scale decomposition.

Flatten deeper organizational containers into the nearest retained parent while preserving editable children and identities. Auto Layout does not require an additional wrapper. Report a scope that cannot fit the shared hierarchy limit without a material tradeoff.

## Cropping newly constructed precompositions

Crop deepest first while preserving main-composition dimensions. Derive conservative visible bounds from effect-aware source bounds or verified native render bounds in the retained composition's coordinates. Include overflow, strokes and masks. Round outward and validate supported composition dimensions. Missing trustworthy bounds must not cause destructive clipping.

Inspect existing animation, expressions, three-dimensional layers and masks before choosing a crop operation. Automatic static compensation applies only to newly constructed static two-dimensional content. Cached and existing animated compositions follow the reuse reference instead.

Use a supported crop operation with known coordinate behavior. If the connection exposes only an application command, discover that command in the actual version. A temporary bounds layer may define the crop region when the command requires a selection; remove it after cropping and restore unrelated selection. Do not hardcode numeric menu identifiers.

Preserve every parent instance's placement. For a crop implementation that leaves parent transforms untouched, add the crop origin and new composition center, subtract the old anchor, transform that displacement through the instance's scale and rotation, and add it to the old position; set the anchor to the new center. This compensation is in the instance's parent space. Inspect the crop operation's actual changes before applying compensation so it is not performed twice.

Shift content coordinates and layer-space mask vertices by the crop offset only where the native operation has not already done so. Tangent offsets do not change under translation. Reconcile effects using normalized or composition-space coordinates with the new dimensions. Verify parent appearance, unchanged root dimensions, no clipping, no leftover helpers and a composition graph without cycles or import-owned orphans.
