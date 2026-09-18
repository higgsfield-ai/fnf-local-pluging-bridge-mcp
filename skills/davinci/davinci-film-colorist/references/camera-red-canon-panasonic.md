# RED, Canon, and Panasonic Sources

## RED

Separate RAW development, grading, and output rendering in IPP2. REDWideGamutRGB and Log3G10 are appropriate only when they describe the actual decoded signal before the selected transform. R3D and IPP2 alone do not establish that stage. Do not silently replace legacy processing, Log3G12, or another confirmed decode.

Distinguish an RMD file's presence, its loading, the effective overrides, and writing changes to the sidecar. Metadata curves or version controls do not prove all four. For processed ProRes, distinguish a log profile from Image/LUT recording; white balance and ISO can already be baked. Model-specific recording behavior must not be generalized across the family.

## Canon

Cinema RAW Light does not imply already decoded Canon Log 2. Inspect effective Color Space, Gamma, Decode Using, and earlier processing. A camera's display or playback settings can differ from the RAW recording's development contract.

Canon Log 3 can be paired with more than one gamut, depending on the model and recording settings. A preset number does not identify the same profile on different cameras. A camera without a particular recorded Log choice can still produce that gamma after suitable RAW development or transcoding; establish the actual path.

A Custom Picture file in metadata, a look affecting recorded video, and a RAW image are different cases. Confirm the exact model, firmware, recording mode, and origin of a proxy or transcode before assigning a profile.

## Panasonic

Use V-Gamut and V-Log only for a confirmed signal with that pair. A published middle-gray code describes that encoding under stated conditions, not a diagnostic signature of an arbitrary pixel or post-output waveform. V-Log L's curve does not establish identical captured dynamic range across cameras.

Separate Monitor or HDMI LUT View Assist from recorded Log and from RAW output. A V-Log preview of outgoing RAW does not establish the decoder's output gamma. For Panasonic-origin BRAW or another RAW recording, identify the actual decoder and its effective output.

Do not move a RAWGamut conversion LUT documented for a particular recorder and development application into another pipeline solely because the source camera matches. A LUT's availability does not prove codec support or the needed conversion in Resolve.

## Verification boundary

Use current model and decoder documentation for uncertain choices. Keep format-specific metadata and inheritance differences visible. Reset restores defaults and Revert has its own reference state; neither automatically restores the task baseline. A clip version does not capture every project setting or sidecar. The supplied source research is not a new live validation of these camera branches.
