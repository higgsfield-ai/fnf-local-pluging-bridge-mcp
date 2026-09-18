# Tonal Shaping Assets

## Purpose and file selection

The supplied GreenShape assets are experimental positive tonal interpretations of published sensitometric curves. They are not complete film, scanner, print, skin-color, grain, or halation models. Their technical filenames identify the supplied assets and remain unchanged. Use them as optional tonal tools, not automatic creative presets.

GreenShape_250D_DWG_DI_static.dctl and GreenShape_500T_DWG_DI_static.dctl use the respective measured-curve interpretations. GreenShape_DWG_DI_UI.dctl exposes curve choice, PrintContrast, and Strength. FilmInspired_v1_soft_static.dctl, FilmInspired_v1_dense_static.dctl, and FilmInspired_v1_bold_static.dctl are separate creative shapes rather than fits to the measured CSV. All are in assets/tonality and expect encoded DaVinci Wide Gamut / DaVinci Intermediate at both input and output.

## Model limitations

The model uses the green density curve from each source graph and applies the resulting nonlinear function separately to every RGB channel. It does not process only green, preserve luminance alone, or reproduce three measured spectral density curves. The per-channel function preserves a neutral diagonal but can alter hue and saturation elsewhere.

The positive interpretation uses an engineering anchor of log exposure minus 1.5 at scene-linear 0.18 and normalizes by the local density derivative. The static PrintContrast is 1.15. This is a chosen positive tonal model, not a measured print-stock gamma or exposure-speed calibration. The deep-shadow continuation and upper tangent are modeled extensions beyond the sampled curve. They do not establish measured minimum density, maximum density, or latitude.

Graph digitization and axis interpretation introduce uncertainty. The supplied historical analysis identified an ambiguous horizontal scale for one source graph. Do not turn a digitized curve, local derivative, or numerical fit into a stronger claim of physical film fidelity. Original source notes and measurements remain available as provenance.

## Application

Establish the actual signal before the tonal node. Its internal decoding and encoding do not replace the output display transform. Preserve an accepted tonal foundation rather than applying an additional curve merely because one is bundled. Native contrast and curves remain valid alternatives when the task does not require the prototype.

Separate curve strength from exposure placement and saturation. If a chosen curve obscures an important object, compare weakening that curve with a small native exposure adjustment upstream. Evaluate skin, saturated materials, colored highlights, noise in opened shadows, and the final output. Do not apply an automatic saturation compensation to every frame.

The retained ExposurePlus DCTL files are historical resources only. Their presence in the package does not supersede the entrypoint's requirement for native technical exposure and white balance.

## Verification

Check identity or bypass, a neutral ramp, middle gray, monotonic progression, and relevant highlight values through the intended output. Compilation errors, inverted tonal order, unexplained neutral color, or unexpected clipping prevent acceptance. Quantized exported equality does not prove floating-point parity or preserved negative and extended-range values.

Historical native static-chart tests covered particular files, export quantization, and one host. They did not certify all UI combinations, operating systems, GPUs, negative values, or temporal behavior. Reestablish the current frame, version, selected asset, and export path before comparing a new result.
