# Source Identification

Match the exact clip, timecode, original file, and selected stream. Establish whether the visible media is original, proxy, or a transcode. Read available Info and source properties without leaving the Color workflow. Preserve the original field names, values, and provenance; a missing value remains unknown. Do not invent fields that the interface did not expose.

Separate sensor RAW from already formed RGB or YCbCr video. Container, codec profile, bit depth, and a flat appearance do not specify camera gamut and gamma. Inspect the exact camera model, recording mode, camera or recorder documentation, and relevant sidecar or production metadata. Present a candidate profile for the confirmation required by the entrypoint.

For RAW, read effective Camera Raw decoding and its inheritance. Project inheritance requires the relevant project Camera Raw settings; a disabled clip control does not show the effective result. Trace earlier LUTs, managed input, and Group or Clip transforms before assigning a node's input. A later output transform does not retroactively change the earlier node's signal.

Distinguish primaries, transfer function, matrix coefficients, and range. The ffprobe color_space field identifies matrix coefficients, while a YUV ColorSpace field does not determine the camera gamut. A reported original value or a container default is not proof of capture encoding. Resolve conflicts through the actual format and decoder rather than a universal priority between container and bitstream.

Record whether a LUT is for monitoring, embedded metadata, baked recording, or an external recorder. Absence of an external LUT or sidecar does not prove absence of earlier processing. A trimmed or transcoded file can carry formerly external settings internally. A clip version does not restore an independently modified sidecar.

For unreadable media, distinguish container recognition, decoding, playback performance, and correct color. Check the exact codec profile, depth, chroma, resolution, rate, and host against the relevant official support matrix. Do not require transcoding solely because of an extension or a historical unsupported-codec report.

Record the source type, effective decode, pre-node transforms, confirmed input, working and output domains, and remaining uncertainty. A pleasant image or plausible waveform is not proof that the selected profile is correct.
