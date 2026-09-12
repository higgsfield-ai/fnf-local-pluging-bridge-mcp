---
name: blender-generation
description: The shared credit workflow for [GEN] assets — live bl_list_models schema as source of truth, non-spending estimate then immediate submit, poll/import/normalize, and the selection report.
---

# Generation — the shared credit workflow

Generation spends the signed-in user's credits. This module is the
common contour for everything marked `[GEN]` in the Scene Passport;
`blender-hdri` and `blender-pbr` add media-specific rules on top
of it, never instead of it, and `blender-greybox` owns the scene the
generated assets land in. Whether an asset
is `[BLOCK]` or `[GEN]` was already decided by the construction routing and
spend policy in `blender-scene` — this module starts after that decision.

## Source of truth

The live catalog decides everything. Before every estimate or submission:

1. `bl_list_models({type:"image"|"3d"|"video", include_schema:true})`;
2. locate the exact `job_type`;
3. build parameters from that returned JSON Schema and nothing else.

The routing hints in `blender-volatile` are intent-to-model guidance
only. A model missing from them is not thereby invalid, and a field they
mention is not thereby current.

## Estimate, then submit immediately

1. Pick the job type from the live schema; validate complete parameters,
   with placeholder UUIDs standing in for media at estimate time.
2. `bl_estimate_generation({job_type, params})` — non-spending.
3. Record and report asset, model, parameters, estimated credits.
4. Submit at once. The user's Generated/Hybrid request was the
   authorization; asking again is a policy violation, not politeness.

`bl_generate_3d`, `bl_image_to_3d`, `bl_generate_image`, and
`bl_generate_video` are submissions, not probes — their `credits` value
arrives after spend has started. If `bl_estimate_generation` is missing or
failing, stop and report that the cost cannot be established; submitting to
discover the price is forbidden.

## Blender-first model defaults

- Unclear image-model choice → `image_auto`.
- Detailed generated material, texture source, environment map, or
  composition-preserving restyle → `gpt_image_2`.
- Text-to-3D → pick among the live text-to-3D models by requested
  topology/PBR support.
- One image to 3D → a live single-image model whose required field is
  `image_references`.
- Multiple ordered views → a multiview-to-3D model, preserving
  front/back/left/right order.
- Unclear video-model choice → ask about
  quality, speed, audio, and reference needs; silently picking the most
  expensive studio chain is not a default.
- A normal Blender texture/environment request never routes through a
  marketing, identity, or preset app chain just because the catalog lists
  one.

## Prompt and proxy

- A measured proxy stays in place before generation.
- One asset per prompt: identity, proportions, material intent, topology/use
  intent, explicit exclusions.
- For image-to-3D, a clean source in the intended view without irrelevant
  background.
- Texture/PBR/quality options only when the passport needs them — higher
  settings can change cost.

## 3D intake rules

- Multiple images: same object, clean background, consistent scale and
  lighting, useful angle coverage, deterministic order.
- The Blender proxy survives until the generated asset passes scale,
  silhouette, material, and camera-read audits.
- Rigging/remesh job types may require public model URLs; a private media id
  is not a URL and pretending otherwise fails.
- If the job's media shape cannot be expressed by the available typed
  submission tool, report the connector capability gap — do not stuff paths
  into arbitrary `params`.

## Submit, poll, import

1. Submit with the matching tool immediately after the estimate, with a
   stable `idempotency_key`; reuse the key after an uncertain timeout.
2. Record job id, estimate, parameters.
3. Poll `bl_generation_status(job_id)` at reasonable intervals. Minutes-long
   generation is not a reason to submit a duplicate.
4. On completion, import by job id with `bl_import_generation`;
   `bl_import_model` is only for an external URL/path no generation job owns.
   Persist video results with `bl_download_generation`.
5. The proxy stays until the replacement passes audit.

A completed image's `result_url` goes to the typed consumer for its declared
purpose: environments through `blender-hdri` and `bl_apply_hdri` (a raw
16:9 image slapped onto the World is not a finished HDRI), materials through
`blender-pbr` and `bl_apply_pbr_maps`.

This path goes only through the connector's `bl_*` generation tools — never
an external provider, client library, or generation script. The backend has
no job-cancel method; do not advertise cancellation.

## Normalize the imported asset

Inspect with `bl_get_scene_summary` and `bl_get_object`, then:

- group and rename imports semantically;
- correct scale in metres, orientation, location, origin;
- parent into the intended collection/rig;
- inspect mesh density, normals, materials, texture links, bounding box;
- fit the approved proxy footprint without distorting critical proportions;
- keep provenance for the final report.

Structural and camera-view checks come before deleting or hiding the proxy.
A completed job is not an approved scene asset until it passes them.

## Selection report

Before the immediate submission, record:

- user intent and the Blender consumer;
- chosen `job_type` and why it beats the nearest alternative;
- exact live-schema parameters and reference count/type;
- expected output and follow-up tool;
- estimated credits.

After completion, keep job id, model id, parameters, result path/URL, and
which Blender object/material/World/shot consumed it.
