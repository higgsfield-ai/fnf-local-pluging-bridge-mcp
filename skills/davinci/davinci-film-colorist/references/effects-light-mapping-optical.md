# Light, Mapping, and Optical Effects

## Source and composition

For Glow, Light Rays, and Aperture Diffraction, distinguish alpha that limits source regions from alpha that limits the completed effect or supplies its source. A source mask can allow a halo to spread beyond a lamp, whereas a compositing mask can cut that spread off. Do not assume the same alpha semantics for every effect or connect clip Alpha Output without a relevant need.

Glow's Screen and Add modes produce different intensity behavior. Framing controls can strengthen or suppress the effect near frame edges; a secondary glow can color the outer halo. A colored halo does not demonstrate simulated illumination of surrounding surfaces.

For Light Rays, inspect source selection, threshold, length, dropoff, composition, and any animation separately. Edge-based sources can produce unwanted rays from nonemissive objects. Some CCD Bloom modes couple length to source intensity, so a brighter source is not necessarily a threshold error.

Aperture Diffraction behaves differently for small and broad sources. Inspect source size and isolation before increasing the effect. Normalize Brightness can rescale the result per frame; evaluate its response when bright sources appear or disappear. It is not scene-exposure recovery.

## Mapping controls

Tone mapping and gamut mapping solve different limitations. Clip discards out-of-range values; a simple tone mapping curve can still lose extreme highlights. Swapping transform direction does not restore discarded data. Compare tone methods with gamut mapping fixed, then compare gamut treatment with the selected tone method fixed.

Saturation-preserving mapping and subsequent highlight saturation rolloff have separate roles. The rolloff thresholds use their documented luminance units; gamut Saturation Knee and Max use different units relative to the selected output space. Changing output requires reevaluating saturated sources. A separate gamut mapper can duplicate compression already enabled in the CST.

Custom maximum luminance and adaptation settings relate the chosen input and output interpretation and rendering. They do not measure physical camera brightness or replace exposure placement. Evaluate the relevant bright texture, hue, and channel behavior through the actual agreed transform.

## Optical effects

For Dehaze, inspect its estimated depth and Haze Color before raising Strength. Its depth controls do not simply select ordinary RGB tonal ranges. Increased strength can change shadow contrast, color balance, and saturation together; it cannot fix an incorrect depth or haze-color estimate by force.

For Lens Reflections, source-region Brightness is a selection threshold and Global Brightness controls the reflection. Inspect source isolation, individual reflections, and final result separately. Presets populate elements without solving source selection. Optical-path position is not ordinary subject tracking.

For Lens Distortion, inspect linked or independent channels, adjustment range, center, and edge behavior. Reflection, wrapping, or replication can repeat details at borders. Use the actual Color Node Sizing controls only when the task permits the resulting crop. Straight lines, edges, and motion verify the geometry; scopes do not establish calibrated lens correction.
