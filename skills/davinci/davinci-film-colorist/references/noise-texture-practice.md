# Noise and Texture Decisions

## Identify the defect

Separate recorded noise, compression artifacts, lighting or surface variation, added grain, and texture enhancement. A colored patch on skin is not automatically noise. Inspect the source and individual grade stages before increasing smoothing. A processed RGB image may have different channel relationships from its original RAW; appearance alone does not identify a noise model.

## Temporal and spatial controls

With motion estimation enabled, reducing Motion Threshold excludes more moving regions from Temporal NR; increasing it allows more pixels to be processed. Motion Estimation None removes that protection. Evaluate frame count and the actual motion-estimation mode separately. Compare moving edges and stationary regions rather than judging temporal processing from only one of them.

When Temporal NR damages moving edges before sufficiently cleaning them, compare Spatial NR for the remaining problem. Spatial processing avoids temporal averaging but can remove fine texture. Read the actual mode before assuming independent Luma and Chroma thresholds: their availability differs between Better, Enhanced, and other modes. For UltraNR, inspect the analysis region and its specific controls.

Blend direction and scale depend on the tool. In Motion Effects NR, increasing Blend moves toward the unprocessed image; the documented scale runs from zero to one hundred. Noise Reduction FX Global Blend uses zero to one for the corresponding endpoints. These are tool contracts, not recommended strengths or a rule for all OFX.

## Acceptance and sharpening

Compare the same frame and scale in a smooth noisy region and in useful hair, skin, or fabric detail. Inspect near one-to-one pixel scale and ordinary viewing size. Select the least processing that reduces distracting noise while preserving important texture. Residual noise is preferable to a damaged surface. Added sharpening or grain does not restore detail removed by smoothing.

Evaluate a short moving segment for trails, flicker, occlusions, and edge behavior under comparable playback conditions. A non-real-time comparison can conceal or distort temporal perception; record that limit. Isolate added grain and downstream texture enhancement when diagnosing where noise becomes conspicuous.

In the Sharpen palette, Level can exclude weak-detail regions and Coring Softness can soften that selection's transition. This limits sharpening rather than adding noise reduction. Texture Pop Differences and Difference Magnitude are diagnostic views of affected detail; return to Final Result after inspection. If sharpening reveals the defect, reassess that operation before increasing NR.
