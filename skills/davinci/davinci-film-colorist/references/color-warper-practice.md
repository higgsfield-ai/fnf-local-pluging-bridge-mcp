# Color Warper and ColorSlice

## ColorSlice qualification

Use Highlight to inspect the selected sector before correcting it. Center changes qualification within that sector. Hue changes the selected color while preserving that selection; hold Center fixed when comparing corrections of the same range.

Density changes luminance preferentially in more saturated colors. Saturation uses subtractive behavior, so inspect brightness as well as chroma. The global controls affect the whole image. Den.Depth and Sat.Depth alter the corresponding adjustment's influence in bright regions. Sat.Balance adjusts the luminance relationship of moderately saturated colors during saturation changes. Compare these controls separately from a shared baseline and recheck other sectors, because their consequences overlap. Sector reset and full ColorSlice reset have different scope.

## Grid qualification and adjustment

The Viewer crosshair identifies a color and the nearest grid point, not an exact object mask. Preview affected pixels and pin colors that should remain stable. Confirm the pin state in the actual interface. Moving a point can pin it automatically; preserve the neutral center when neutrality matters.

Hue–Saturation grid movement around the center changes hue and radial movement changes saturation. Chroma–Luma uses the selected grid and axis angle to represent color ranges, with vertical movement affecting luminance. Establish resolution, color space, grid, axis, pins, and selection before editing. Changing grid resolution after a correction interpolates it and can alter the result.

Range and drawn selection affect groups of points. Falloff changes the selected neighborhood, while Auto Lock and border settings protect surrounding points. Pull and Push alter differences among neighboring colors. Component smoothing progressively returns selected chroma, saturation, or luminance toward its original state; Reset is a different operation.

## Stroke-based Chroma Warp

For Chroma Warp, distinguish moving a color range in Normal from targeting a particular color in Point to Point. Chroma Range changes the neighboring coverage; pin points protect colors. Exposure adjusts target brightness. Tonal Range Low, High, and Pivot limit tonal influence across strokes, not only the latest selection. Treat this as an alternative working mode rather than assuming grid controls apply unchanged.

## Acceptance

Check target material in shadows and highlights, adjacent hues, skin, and neutral objects. Inspect smooth gradients, noise, patchiness, and temporal flicker. If a correction cannot reliably separate important materials, revise its scope or strength instead of increasing it until damage becomes visible. Restore selection, pins, processing state, and baseline image when concluding a control experiment.
