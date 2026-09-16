# Blackmagic RAW and Processed Recording

Treat camera model, source codec, recording settings, effective decode, and node input as separate evidence. Blackmagic RAW can originate from supported external cameras and recorders; its filename does not identify a universal camera profile.

Read Color Science Version, gamut, gamma, LUT source, and whether the LUT is applied. These are separate settings. Metadata, project inheritance, clip overrides, and an external sidecar can affect the effective result. A sidecar can override embedded values without changing the original BRAW; losing it during a copy can change the interpreted image. An embedded LUT is not necessarily active.

Obtain available decoding choices from the actual SDK or interface rather than extrapolating from a camera name. A generation of color science does not require every output to use its Film gamma. Custom gamma, contrast, rolloff, or an active LUT adds processing that a base-profile label alone does not describe. Do not change Decode Using merely to inspect an otherwise readable inherited state.

Ordinary ProRes and ProRes RAW are different cases. For developed ProRes or another transcode, establish Film, Extended Video, or Video recording and any baked LUT. Those pixels cannot be redeveloped as BRAW by changing Color Science. Film is a log mode; Extended Video includes a display-oriented rendering, and Video's primaries alone do not establish every output gamma or highlight behavior.

Distinguish BRAW Apply LUT in File from a processed recording that bakes a LUT into the image. A LUT used for monitoring is another case. Check the exact model and recording route before drawing a conclusion. Apply the user's confirmed pair only after establishing its relationship to effective decode and earlier transforms.

The official Blackmagic RAW SDK exposes a broader contract than some Resolve scripting interfaces. Do not claim getters or decode controls are available in Resolve merely because they exist in that SDK. Runtime support and color fidelity remain host-specific checks.
