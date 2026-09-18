# Masks, Tracking, and Relight

## Windows and tracking repair

Choose a window that supports plausible light and stable selection rather than tracing every object edge. Check the actual matte and the ordinary image through the correction. Track from a clear reference frame using relevant motion components, and inspect the whole affected interval instead of treating a completed progress bar as successful tracking.

Clip-mode window adjustments affect the track broadly, while Frame-mode adjustments create local interpolation. Place an unchanged key at the last good frame before a repair when earlier motion must remain fixed. Shape changes during a turn may need separate correction. For an occlusion, repair or remove only the bad track interval and inspect interpolation; a motion path alone does not hide the correction behind a foreground object.

Use a subtractive selection or deliberately animated correction strength where the target is occluded or exits. Verify the transitions in playback and frame inspection. Restore the intended tracking mode and diagnostic views afterward.

## Qualifier and matte refinement

Qualifier selection depends on node input. A preceding grade can change the selected range. HSL, RGB, and LUM select signal properties, not semantic objects; a 3D qualifier selects a color volume, not scene depth. Disable an unstable selection component only after checking object and background separation.

Pre-Filter acts before sampling. Matte Denoise cleans the extracted key rather than denoising the RGB image. Clean Black removes background flecks and can contract partly transparent edges. Clean White fills holes and can expand edges. Neither restores lost detail. Blur Radius softens the edge but can create a halo. In/Out Ratio controls where that refinement extends and can also affect small defects when the blur radius is zero.

Inspect hair, transparency, motion blur, edge softness, and background leakage before seeking a uniformly white matte. Isolate the effect of one refinement at a time and test changing light and movement. A visually tidy matte alone does not prove a useful RGB correction.

## AI selection and depth

Read the active Magic Mask interface before choosing its procedure. Click List and legacy Stroke List have different selection workflows; do not infer the active model from a menu option or an isolated control name. In the click workflow, positive and negative clicks select and exclude. Smart Refine, Consistency, and Paint have distinct purposes: Paint is a frame correction rather than a tracked repair, and temporal smoothing can lag movement.

The documented click-based analysis can be independent of upstream grades and color management. Do not transfer HSL input-selection behavior to that model or promise that an upstream contrast node improves analysis. RAW, geometry, cache, and legacy-model changes require their own verified invalidation rules.

Depth Map estimates relative depth in alpha, not physical distance or surface normals. Read Target Depth, Tolerance, Softness, polarity, and blanking behavior. If a narrow isolated region pulses, compare the unisolated map before changing the selection. Spatial blur or node caching does not establish temporal repair. Adjust Map Levels constrains the map rather than calibrating distance.

## Relight and alpha

Relight uses image RGB and can use a separate Surface Map through its second input. Alpha limits the correction. With preview off, an image adjustment such as Gain uses the light map; Brightness is not independently a complete image-lighting operation. Surface normals and depth maps are not interchangeable, and synthetic inter-object shadows are not guaranteed.

Inspect the actual OFX alpha and key connections. In legacy alpha controls, disabling Enable and disabling Use For Mixing have different effects; the latter can remove the node's alpha restriction while retaining alpha output. Do not disable mixing merely to expose a connector.

Verify a neutral baseline before a relighting correction, then separate map defects from subject-matte defects. Inspect edges, motion, and occlusion. A rendered traveling matte or cached result requires checking its files, timing, and correspondence after subsequent source or mask changes; portability and automatic refresh are not assumed.
