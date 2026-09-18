# Review and AE Delivery

## Visual coverage

Inspect original source, parent and candidate alpha, and final composites on light and dark backgrounds. Combine native optical detail with wider material context. Review every changed frame and both interval joins, then the requested shot duration and silhouette. Cover moving features spatially as well as temporally; a crop can contain all frame numbers while clipping the feature.

Observe normal and slow playback when the available interface supports actual observation. With still-image tools, inspect ordered consecutive frames and source-registered diagnostics, and state the limitation. A player reaching its end does not establish observed continuous playback. Generated review boards are not actual inspection, and reviewer acceptance is not user approval.

Scale sixteen-bit alpha explicitly for display. A viewer can make valid soft alpha look binary through incorrect display conversion. Check panel dimensions and display scaling before claiming native pixel inspection. Reuse prior visual evidence when source, region, renderer, and displayed pixels are identical; identify that as carried evidence rather than another viewing pass.

Practical acceptance need not establish physical ground truth, but it cannot ignore a demonstrated lost feature or retained background. Preserve uncertain interpretations separately from confirmed defects. A newly reported jitter issue can reopen an older accepted delivery.

## Media integrity and color

Verify frame endpoints, ordering, completeness, dimensions, rate, duration, channels, precision, and alpha interpretation. Preserve original source timing and project color settings. Native PNG or RGBA sequences are the deliverable; reduced review movies are viewing aids. File hashes establish identity, not quality.

Check alpha, opaque RGB, and associated foreground contribution using the actual decoder and renderer conventions. AE's decoded source RGB may differ from a separate CPU decoder. A source-only AE control at matching timing can distinguish decoder differences from matte transfer errors. Do not compare associated RGB directly with straight RGB or reinterpret transparent RGB as visible color.

Calibrate tolerances on the actual producer and host in explicit numerical units. Historical sixteen-bit transfer measurements cannot be interpreted as eight-bit codes or reused as universal acceptance thresholds. Investigate mismatches rather than widening limits to obtain a pass. A sampled transfer test does not verify every untested frame or matte quality.

## AE construction

Inspect the current project and preserve its existing items and relevant state. Use original source footage and the selected new matte when building a new result. Duplicating an old reference composition can retain hidden dependencies on its old alpha or Refine Soft Matte effects. For a color-only wrapper, trace every layer and Set Matte dependency to the intended new result.

Match each matte effect's channel choice to its input. A grayscale sequence may carry an opaque alpha channel; selecting that alpha cannot extract the grayscale matte. A Set Matte operation sourcing an already composited RGBA layer has a different contract. Verify the final graph rather than assuming an effect name establishes correct wiring.

Check actual transform readback. After Effects can return three-component position, anchor, and scale arrays for a two-dimensional layer. Validate the observed two-dimensional flag and numerical values instead of treating array length alone as a transform failure. Preserve original placement, pixel aspect, and source-to-composition timing.

Use the observed AE clock when sampling held frames and keep original rational timestamps separately. Some nominal fractional frame rates use slightly different host clocks. Floating-point serialization error, host-clock agreement, and cadence integrity are different checks; none permits dropped or duplicated frames.

## Completion and recovery

AE can acknowledge saveFrameToPng before its file is complete. Wait within a bounded timeout for stable bytes and complete PNG structure before decoding. A completed-file mismatch still fails; a write race does not require new matting inference. An AppleScript process returning success does not prove that the AE operation succeeded; verify the receipt and actual application state. Node syntax validation also cannot establish ExtendScript compatibility. Capture actual AE evaluation errors, including legacy reserved-word failures, before assuming a submitted script ran.

After partial import, inspect the created items and preserve the original state record. Resume only matching owned work, or undo the specific failed operation when safe. Blind reimport can duplicate compositions and invalidate bindings. Remove only owned temporary verification items after checking their dependencies.

Save a separate versioned AEP with accessible sequences. Verify the saved file and visibly open the relevant result when UI tools are available. Record source and parent identities, processing version, actual review scope, open defects, transfer evidence, and saved paths in the project. Keep generation records immutable and add later decisions separately. Technical transfer, editorial quality, and model generalization remain distinct conclusions.
