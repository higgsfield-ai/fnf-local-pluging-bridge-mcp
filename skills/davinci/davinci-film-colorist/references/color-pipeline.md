# Color Pipeline

## Establish the signal

Distinguish sensor RAW, capture metadata, and the RGB image produced by decoding. A container or codec does not specify the image's gamut and transfer function. Read effective Camera Raw settings and their inheritance. A disabled control does not establish the inherited value. A CST transforms decoded color; it does not debayer RAW.

Trace source decoding, input LUTs and assignments, Clip and Group processing, Timeline processing, project color management, output transforms, and monitoring. Record each unknown rather than treating an empty field as Rec.709. A confirmed source profile applies at the source; a later node may already receive a working-space or display-referred signal.

For mixed sources, classify the actual original, proxy, or transcode separately. In a managed RAW workflow, ordinary clip input assignment may not override the decoder's colorimetry. In a managed non-RAW workflow, inspect manual input assignment and the project's fallback. Available ACES choices inside a CST do not by themselves establish a complete ACES workflow.

## Build the established manual pipeline

Follow the graph order and personal constraints in the entrypoint. In the input CST, use the confirmed source gamut and gamma and convert to DaVinci Wide Gamut / DaVinci Intermediate. Evaluate tone mapping, gamut mapping, and OOTF independently of those four space and gamma fields. Do not copy display-mapping settings into the input stage without a reason.

The two secondary groups are sequential groups, each with genuinely independent branches receiving a common input and converging through a Parallel Mixer. A single shared parallel branch is not equivalent. Inspect connections and mask interactions rather than inferring topology from node numbers or screen positions.

For native linear white balance, use the intended working gamut and Node Gamma Linear on the technical node before adjusting RGB Gain. This changes that node's processing domain, not the project gamma. Preserve gamut and Node Gamma when reading or transferring gain values. Native linear Master Gain can place exposure independently of the tonal curve; derive its multiplier from the intended stop change and verify both the local gamma and the image. Do not combine exposure placement with curve-strength changes and attribute the result to one operation.

## Output and migration

Set the output transform for the agreed viewing target. A gamut and gamma label does not fully specify a display rendering transform. Read tone mapping, gamut compression, and OOTF settings and inspect highlight and saturated-color behavior. Project Output Color Space, the last CST's output gamma, monitoring, and file metadata are distinct parts of the pipeline.

An effect requiring another domain needs a verified conversion into and out of that domain or a compatible alternative. Avoid a second display transform. Creative LUTs may include tone as well as color. Matching input and output labels does not prove that a manufacturer LUT and a CST render identically.

For a specifically requested manual display-referred look, establish its output primaries and gamma before placing it after the main output conversion. Reevaluate controls and keys in that domain. Moving nodes or copying the same numerical settings across a transform does not preserve the image.

During an authorized migration, retain a usable prior version and identify project, timeline, group, shared-node, and RAW state that a clip version cannot restore. Remove duplicate transforms by tracing their real scope. Do not reset an accepted managed project merely to match the preferred new-project template.

## Diagnose clipping and metadata

Locate the first stage that loses distinctions in highlights or saturated colors. Input clipping, tone mapping, LUT domain limits, gamut compression, and output range errors require different remedies. Expanding a working gamut cannot recreate lost source detail. Do not claim recovery merely because an output patch becomes darker.

Check image levels against the agreed output, not a universal SDR or HDR threshold. Primaries, transfer function, matrix coefficients, and range have separate meanings. Resolve container, bitstream, sidecar, and decoder conflicts according to the actual format and effective interpretation; no universal priority rule applies.

Verify serialized settings by fresh parameter readback and native images, particularly boolean mapping controls. Test the same timecode and display conditions, inspect adjacent shots, and check available motion. Do not attribute a visual change to the working space when balance, look, and mapping also changed.
