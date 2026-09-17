# Primaries, Log, HDR, and Curves

## Tonal control selection

Lift, Gamma, and Gain have broad overlapping influence. Log Shadows, Midtones, and Highlights are more localized in signal value, but cannot isolate a subject that shares those values with its surroundings. Lowering Low Range narrows Shadows and broadens Midtones; raising it does the reverse. Lowering High Range broadens Highlights and narrows Midtones; raising it does the reverse. Log does not provide a separate overlap amount and does not normalize camera log automatically.

Inspect the actual signal domain and the project's legacy Log-range setting. Do not toggle that setting merely to reproduce a lesson. Strong corrections in normalized signals can disrupt tonal smoothness or order. LGG and Log adjustments remain active when switching palettes. Their internal processing order differs from palette navigation. Offset is shared between the two modes and is not an independent Y-only exposure control.

## HDR zones

HDR Color Space and Gamma must describe the signal at the node. An additional Node HDR Mode is not a prerequisite for the HDR palette. Contrast's saturation preservation is perceptual, not a promise of an unchanged vectorscope.

Use the node-input histogram and range preview to establish which values a zone covers before increasing its Exposure. Max Range bounds a zone that extends toward shadows; Min Range bounds one extending toward highlights. Zones overlap, and the displayed stops are relative to photographic middle gray. Some historical manual passages interchange the labels, so verify the actual preview direction. A zone beyond all input data can accept a value without producing an image change.

Falloff sets transition softness near the boundary. Inspect visible contours and unwanted additional coverage. Black Offset affects the darkest values and the Exposure reference with a transition; it is not a global shift or limiter. Negative results remain possible and may be clipped by later processing. Hiding a zone does not disable it. Reset Color Adjustments and Reset Zone Definitions restore different state; use the saved version when a complete return is required.

## Curves

Distinguish selected channel, linked editing, selection input, output adjustment, curve shape, and strength. Gang links editing; selecting a channel does not guarantee that other output channels remain unchanged because Lum Mix can compensate for luminance. At its documented zero setting, that compensation and Y-only contrast behavior differ from the normal setting. Verify the actual state rather than relying on a channel label.

Curve Intensity or Mix attenuates that curve, not the whole node. Inversion controls are not attenuation. For HSL work, hold Input constant when the same selected range must be tested and change the intended Output. Neighboring anchors constrain the adjusted range. The output histogram describes the result without changing the curve's selection principle.

Hue is cyclic. Abrupt changes, especially luminance changes selected by hue on compressed material, can create boundaries, noise, or banding. High Soft begins compression before the High cutoff; lowering the cutoff can permanently remove distinctions for downstream nodes. A later gain reduction does not restore them. Compare tonal order, neutral regions, saturated gradients, and available motion through the unchanged output.
