# HF-Astra-Looks

## Dependency contract

Use the bundled HF-Astra-Looks DCTL and all five external LUTs. Keep their names, relative directory structure, settings and the manifest-verified bytes unchanged. The complete parameter identifiers, defaults, and ranges belong to the supplied parameter data. Read those data when configuring the effect rather than reconstructing identifiers from historical screenshots or numeric OFX indices.

The DCTL declares its five LUT dependencies even when only an analytical palette is used. Inspect the real installation and compilation on the current host. A supplier report from another operating system or GPU does not establish compatibility here. Preserve the current recipe before switching files, and read controls back after loading.

## Processing domain

The original input and output are DaVinci Wide Gamut / DaVinci Intermediate. Internal processing and mixing use linear DWG before returning to Intermediate encoding. Camera log, display-referred Rec.709, and unencoded linear RGB are not interchangeable inputs.

The film LUTs contain tone as well as color and specify an RCM SDR display rendering context. An arbitrary Gamma 2.4 CST or HDR output is not automatically equivalent. When activating a film LUT branch, compare the full effect with direct use of the corresponding cube under the same agreed output rendering. An external tonal curve plus the LUT's baked tone is an additional creative choice.

## Controls and starting state

The original provides 49 controls spanning mixing, analytical palettes, film LUT weights, common color, a common curve, Tetra, and ramp diagnostics. Preserve all of them. A starting recipe neutralizes selected processing without removing the ability to use it later.

After an accepted separate tonal foundation, start in Normal mixing with Master Strength and Original at unity, Additive Experimental off, and film and analytical palette weights at zero for the baseline comparison. Keep the internal curve at identity, Tetra Strength and Chroma Density Stops at zero, Saturation at unity, and Hue, Split, and Warm Hue Protection at zero. Keep unused coordinates and supporting curve controls at their documented defaults. Disable View Ramp. Read back the full state, verify bypass, then choose palette, hue, saturation, and split according to the image.

Normal mixing normalizes branch weights. Relative weights determine the branch mixture; their absolute magnitude is not an independent overall-strength control. Original is the internal base after applicable curve and Tetra processing, not a bypass of the entire node. Zero palette weights do not disable active common controls.

Master Strength mixes with the node input in linear DWG. Host Key Output Gain mixes in the node's host processing domain, ordinarily encoded Intermediate in the established pipeline. They are not interchangeable strength controls. Start both at unity, choose the intended attenuation method, preserve both values, and reevaluate the domain if Node Gamma changes.

## Creative use and failure limits

Establish the character of individual hues before solving an unwanted hue by global desaturation. Compare a more expressive candidate and its attenuated result against skin, material differences, depth, and artifacts. A restrained image can remain colorful. Preserve an accepted technical base when only the creative character needs revision.

Tetra changes the input to the look branches; a vertex coordinate is not the final output color of every matching pixel. A neutral diagonal does not establish gamut safety: permitted coordinates can collapse color or produce negative luminance. Warm Hue Protection is based on warm hue and chroma, not semantic skin recognition, and does not protect against the LUT, curve, or Tetra.

The analytical hue, saturation, and split processing can preserve computed linear luminance under the documented neutral-curve conditions without preserving perceived contrast, RGB ratios, or gamut containment. Split intentionally tints neutrals. Density changes the exposure of colored regions and must be evaluated separately from a retained tonal foundation.

Keep Additive Experimental off by default. The supplied source audit identifies highlight inversion and negative channel values for some multi-LUT additive combinations. A deliberate experiment requires gray and colored highlight tests, not only a midtone frame. Film lookup clamps its input coordinates to the LUT domain; full LUT weighting can lose negative or extended-highlight distinctions. The supplied cubes do not implement grain, halation, bloom, or temporal effects.

## Acceptance

Verify the selected DCTL, all dependencies, complete control state, neutral baseline, Master bypass, one analytical palette, and the intended Normal mixture. Inspect skin, clothing, shadows, saturated highlights, and available motion through the agreed output. Disable ramp diagnostics before delivering frames. A correct label, parameter readback, or historical successful load is not evidence of the current rendered look.
