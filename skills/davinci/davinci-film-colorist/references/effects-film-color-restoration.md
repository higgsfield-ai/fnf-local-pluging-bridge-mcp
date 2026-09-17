# Film, Color, and Restoration Effects

## Film processing

Separate Film Look Creator's color settings, internal input and output handling, and spatial or temporal texture. Richness and subtractive saturation have different effects on already saturated colors. Exposure and white-balance controls inside a creative effect are not new RAW development and do not supersede the native technical corrections required by the entrypoint.

When exporting a LUT-compatible color chain, establish the complete chain included in the export. The LUT replaces that exported processing, which may include technical transforms; substituting it only for one creative node can duplicate them. A 3D LUT does not preserve grain, halation, vignette, or motion. Restore spatial processing separately when appropriate.

For Halation, distinguish source isolation, glow color, spread, and final composition. Film Saturation Level affects the transition of source color toward white, while the reflected-layer saturation controls the halo. Relative Spread can affect channels differently. Basic Grain belongs to that halation layer. Global Aspect Ratio changes the effect's shape, not the source pixel aspect.

For Film Grain, establish size before balancing its contrast and overall contribution. Strength controls grain-layer contrast; Opacity controls application strength. Offset and Symmetry alter the relationship of light and dark grains rather than merely resizing them. Inspect Grain Only and then the composition. Shadow, Midtone, and Highlight Gain alter the contribution in their respective ranges.

Grain depends on project resolution and viewing scale. Freeze and Animate on Every Refresh affect static comparisons but do not prove identical pattern generation. Reevaluate motion after a still comparison and restore the intended settings. Plan separate Halation and Film Grain nodes unless the actual host verifies a different supported arrangement.

## Color correction effects

Color Compressor independently brings hue, saturation, and luminance toward a target. Fully compressing hue does not equalize brightness; compressing every component can erase form. Establish its actual domain instead of inventing a camera-log or display-input guarantee.

Color Stabilizer needs a suitable reference and analyzed region. A selected analysis area is not necessarily a local correction mask. Track that analysis region when appropriate, choose only the affected brightness, balance, or channel components, and distinguish Levels and Contrast, Offset, and Gain behavior. Captured Analysis Values are not tracking controls. Inspect the entire interval for errors caused by moving objects or intentional lighting changes.

White-point adaptation is part of a defined transform, not a substitute for arbitrary creative balance. Gamut Limiter is a clipping operation whose effective position depends on the remaining chain. For OCIO, preserve the exact config, context variables, search paths, referenced LUTs, direction, and selected color spaces or Display and View. A color-space conversion can involve a view transform; its name does not guarantee simple recoding. A collection's selected correction and reload state require explicit verification.

## Restoration and detail

For replacement or concealment tools, establish the source frame or clean plate before increasing strength. A filled defect is not necessarily preserved texture. Inspect reconstructed detail, occlusions, repeating patterns, and temporal consistency.

Detail Recovery requires two real RGB inputs. The normal first input receives detail and the second supplies it, subject to Transfer Direction. Verify the actual node and ports. Preview Detail and the frequency and edge controls establish what is being extracted. Detail Mix zero is not whole-node bypass; inspect its actual replacement behavior. Ensure that recovered texture does not reintroduce the original dust, flicker, or noise.

Photochemical negative, print, silver retention, grain statistics, and digital approximations describe different stages and quantities. A density curve, grain metric, or process name does not determine a complete digital recipe. Preserve these distinctions when interpreting a requested film character.
