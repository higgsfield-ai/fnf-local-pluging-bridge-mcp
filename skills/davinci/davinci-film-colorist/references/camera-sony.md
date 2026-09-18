# Sony Source Profiles

XAVC, a camera name, and a container do not identify the color profile. Establish recording mode, gamma, gamut, original or proxy status, and any recorder or transcode processing. Preserve metadata provenance; an application's assigned source color space may be an override rather than capture evidence.

S-Gamut with S-Log2, S-Gamut3 with S-Log3, and S-Gamut3.Cine with S-Log3 are different input pairs. S-Log3 alone leaves the gamut unresolved. Do not substitute the Cine gamut because its name resembles another profile, or extend one model's picture-profile choices to every camera.

For cameras with dedicated Log shooting modes, read the selected gamut in that mode. Flexible ISO and Cine EI do not themselves select between the two S-Log3 gamuts. For a camera or recorder capable of applying LUTs to recording, inspect the original recording route separately from viewfinder, proxy, streaming, and external video outputs.

X-OCN requires effective RAW-decoder inspection. A common decoded S-Log3 output does not prove the current decoder's gamma or gamut. The recording's scene-linear description is not necessarily the RGB signal entering the node. For already encoded video, investigate the saved pixels and any baked transformation.

Separate a monitoring LUT, an embedded LUT reference, and a LUT applied to recorded pixels. A display LUT's gamma and primaries do not fully specify its creative rendering. Establish the exact file and documented input and output before treating a manufacturer LUT and a CST as equivalent.

Use the exact camera and recording-mode documentation for uncertain fields. Historical clip tests do not prove other cameras, modes, effective RAW decoding, or a complete master. Validate the current source, transform, and displayed image independently.
