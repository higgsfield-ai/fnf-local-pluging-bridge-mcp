# Light and Color Foundations

Separate the scene, capture, processing, and display. Scene illumination, recorded sensor exposure, encoded RGB, coded luma, displayed luminance, and perceived brightness are related but different quantities. A scope reading does not directly measure the set's light or a physical monitor's output.

A stop is a ratio of exposure in a suitable linear representation, not a fixed increment of camera-log code, a generic Offset number, or a fixed waveform distance. A request for a stop change requires the actual processing domain and an appropriate native operation. Historical gray-chart responses do not establish portable exposure units for every control.

Gamut defines color coordinates and primaries; gamma or a transfer function defines encoding. A container's color matrix and signal range are additional conditions. A log image can store a broad scene range while using values that do not resemble final display brightness. Changing a tag is not the same as converting pixels.

White balance responds to an image's light and material relationships. Similar nominal color temperatures do not ensure identical spectral rendering. Kelvin, tint, an application wheel, and RAW decoding are not interchangeable controls. A neutral result in one region can damage another under mixed light.

Read lighting from highlight shape, shadow direction and softness, reflections, falloff, and relative subject and background levels. Distinguish diffuse material color from specular reflection. Apparent color or texture changes can come from lighting rather than a defect in the grade. Do not infer a specific physical source or camera solely from a finished frame.

Photographic negative density, a positive print, scanned RGB, and display rendering involve different transformations. A digitized density curve or a process name does not provide a complete digital color model. Grain metrics describe some statistical behavior without determining a unique particle size, distribution, or temporal appearance.

When interpreting historical response maps, preserve the exact input chart, domain, control, output, quantization, and tested range. Equality after integer export does not prove equality in floating point. A nondetected small change may reflect quantization or another limitation and does not prove that the control is universally inactive. Stochastic grain needs distributional and temporal assessment rather than one output code per input.

Signed CDL, Offset, Slope, and Power must be identified by the actual requested and applied parameters. A helper's field name is not evidence that the SDK accepted the intended operation. Compare real readback and the native image. Do not transfer measured pixel-drag distances, code maps, or legacy recipe values as current presets.
