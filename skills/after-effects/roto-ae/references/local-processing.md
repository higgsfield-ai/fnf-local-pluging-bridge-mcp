# Local Processing and Portability

## Discover the available implementation

Locate the user's current checkout and working interpreter rather than reusing an absolute path from another Mac. A transferred workspace may contain RotoTransfer/toolkit/runtime, its engine directory, and a local virtual environment. Confirm these files actually exist. Moving a skill does not move footage, checkpoints, Python environments, compiled libraries, AE projects, or licenses. Rebuild an unavailable runtime from its recorded dependencies instead of assuming a copied virtual environment is portable.

Use the selected implementation's argument definitions, schemas, and result records to establish supported geometry, timing, guide format, precision, and side effects. Existing pinned environments may require isolated Python execution and disabled bytecode writes; preserve those verified invocation conditions. Inspect unfamiliar, modified, or consequential helpers before using them. Reuse previously verified unchanged helpers without repeatedly reading their complete dependency trees.

## Choose a compatible processing route

The observed short-pilot implementation uses SAM 2.1 and ViTMatte through auto_roto.py. Preparation can decode footage and create a job; it is not a read-only preview. Segmentation capture resolution and matting resolution are separate. A low-resolution initial mask can lose a narrow lace or aperture that larger matting settings cannot reconstruct reliably.

The observed recurrent route uses decode_roto_sequence, stream_roto_sequence_chunked with MatAnyone2, and package_roto_sequence. Inspect current supported frame rates, duration guards, rotation handling, and seed requirements. A maximum-frame guard should reject an unsupported source rather than silently truncate the requested range. A fixed crop needs motion-containment evidence across that range, especially where the source clips the subject at image borders.

For an established native tiled ViTMatte route, retain original decoded RGB, source-derived trimaps, native tile coordinates, overlap weights, and timing. Preserve the selected implementation's distinction between raw predictions and trimap-clamped output. Changing tile support, preprocessing, or clamping changes the experiment even when the checkpoint is unchanged. Record the actual mode rather than inferring it from inherited metadata.

A source-confirmed fully absent frame can bypass inference and remain exactly transparent. Tracking failure, weak foreground confidence, or a nearly hidden subject is not evidence of complete absence. Check emergence and disappearance against the original frames.

## Memory and speed

Measure a representative difficult interval before estimating throughput. Separate generation waits, decoding, model loading, inference, encoding, AE transfer, and human-like review time. A compute benchmark is not a guaranteed end-to-end delivery time.

Recurrent query chunking can reduce affinity-matrix memory while retaining the complete memory bank and recurrent state. Restarting temporal memory, reducing stored frames, resizing RGB, or cropping the scene is a different algorithmic change. Validate an optimized path against a bounded known result before extending it. Clearing an allocator cache cannot release tensors that remain live.

Reuse identical decoded inputs, verified completed frames, and unchanged output files when their contracts permit it. Do not repeat a full shot to test a small local hypothesis. If a runtime or producer fails, preserve its partial evidence and diagnose the failure before restarting.

## Interchange contract

Keep source timestamps and time bases separate from AE's observed composition clock. Preserve frame count, ordering, geometry, channels, and alpha interpretation. A sixteen-bit container holding expanded eight-bit RGB does not recover discarded source precision. The generic source-color packager does not estimate uncontaminated foreground color. HDR, OCIO, variable frame rate, and estimated-foreground inputs require an implementation that explicitly supports their contract.
