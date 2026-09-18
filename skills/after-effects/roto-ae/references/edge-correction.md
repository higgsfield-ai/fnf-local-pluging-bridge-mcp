# Matte and Color Correction

## Determine material before changing opacity

Use original source context and neighboring frames to distinguish subject material, reflections, exposed background, cast shadows, and adjacent objects. Brightness, connected-component size, template correlation, or reliable optical flow alone cannot establish identity. A small detached component can be real skin behind an occluder; a well-tracked shape can be stationary background.

Separate confirmed opaque interiors from uncertain optical boundaries. Recover dense cloth, skin, laces, and metal without forcing hair or motion blur to opacity. Preserve true holes, temporary contact apertures, source clipping, and requested accessories. Internal hair-to-clothing contact is not automatically exposed background.

## Locate the cause

Inspect source RGB, the original segmentation or trimap, raw alpha, any output clamp, application weights, and final composite separately. A foreground label over unwanted sock material can retain it despite further model training. A correct trimap does not guarantee that a network will recover a tiny reappearing shoe. A color fringe can remain after alpha is correct.

Correct displaced geometry before tuning softness. Inspect the complete source contour, solver context, uncertain band, correction support, and review window as different regions. An outward-safe polygon can still under-cover the unwanted feature. Place the transition where parent and candidate agree, with enough support to remove or restore the complete defect.

For a source-guide change, create a separate candidate input. Preserve unrelated trimap pixels and use definite foreground or background only where source evidence supports it. Keep ambiguous lining, shadow, crossing strands, and mixed edges uncertain. Inspect the resulting output beyond the changed guide because a neural model's receptive field can alter distant pixels.

## Compare and compose corrections

Compare alpha candidates using identical foreground RGB. Compare color candidates using identical alpha. Judge changes on light and dark backgrounds, including weak premultiplied contributions. Preserve genuine colored illumination and reflective highlights; a pale edge is not automatically contamination.

Recompute replacement trials from a fixed parent instead of repeatedly applying removal or restoration to their own output. Integrate actual changed pixels rather than whole overlapping crop rectangles. Resolve intersections explicitly and retain unaffected values, including hidden RGB when required by the producer.

For additive coverage, use the actual quantized delivered alpha increment to add foreground contribution to existing premultiplied RGB. Apply the correction weight once. No added coverage should produce no additive color change. A signed replacement or joint temporal alpha-and-color operation has a different contract; do not copy an additive-only gate into it.

Keep color finishing localized to source-supported contamination. AE Remove Color Matting and Spill Suppressor can change real skin or fabric color, including opaque pixels. Reusing an accepted hair treatment on a new matte still requires review; applying its sampled background color to a different body region is a separate hypothesis. Preserve the intended alpha after color processing using a compatible new alpha source.

## Temporal coherence

Follow each feature through its actual entrance, movement, occlusion, and exit, including both joins of a local edit. A correct curve name does not preserve material correspondence if point roles or widths change between frames. Independently moving components may need separate correspondence.

A moving application boundary or noisy confidence field can introduce flicker even when the solver output is coherent. Inspect source-registered alpha, support, and confidence changes before altering the model. Temporal smoothing can spread a persistent omission into neighboring frames or stabilize false background. Correct source scope and morphology first; apply a selected temporal correction to a coherent fixed input rather than averaging successive outputs. Avoid end-to-start coupling unless the footage is genuinely a loop.
