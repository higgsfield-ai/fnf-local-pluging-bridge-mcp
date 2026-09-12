---
name: blender-audit-finalize
description: Structural + motion + visual audit against the passport, measuring a complaint, specialist audit hand-offs, the repair loop, and non-destructive bl_finalize_build (save only on explicit request).
---

# Audit and finalize

The audit compares the scene to the Scene Passport — not to memory, and not to
the arguments of the calls that built it. A build passes only when structural,
motion, and visual evidence all agree.

## Structural audit

Run `bl_validate_scene`, diff against the pre-build snapshot with
`bl_scene_diff`, and inspect the important objects with `bl_get_object`
(`bl_execute` only for facts the typed reads do not expose). Confirm:

- every expected object exists exactly once, under its semantic name;
- dimensions, transforms, origins, parents, collections, visibility match;
- active camera, frame range, fps, render engine, resolution match, and
  `frame_end` reaches the last marker and the last key;
- material slots and texture links resolve;
- generated replacements sit inside their proxy footprints;
- no stray defaults, `.001` duplicates, orphan stand-ins, or hidden failures;
- related objects found under every prefix they use — one prefix search is
  not a sweep;
- hero/export meshes have sane normals, manifold state, and density.

## Motion audit

Mandatory for dynamic-default scenes; skipped only on an explicit static
request.

- Run `bl_audit_motion`; when diagnosing a failure, enumerate animated
  objects/properties, key times, and interpolation.
- Sample first/rest, departure, peak, settle, and final/loop frames.
- Check collisions, clipping, constraint jumps, rotation flips, camera
  framing, visibility, loop continuity.
- The promised motion must be perceptible and purposeful.

A still image cannot pass this audit.

## Visual audit

1. Viewport screenshot for composition and editability.
2. `bl_audit_render` for active-camera material, light, shadow, transparency,
   and engine-specific proof.
3. `bl_render_contact_sheet` for dynamic scenes.
4. View the returned evidence — success JSON says nothing about appearance.
   And view it at scale: image previews downsample, so few-pixel features
   average away to nothing. Crop 1:1 and count bright pixels numerically
   before concluding something did not render.
5. **Unreachable evidence fallback** — when the render/screenshot URL cannot
   be opened from the agent's environment (network policy, expired link), say
   so explicitly, hand the URL and on-disk render paths to the user, and mark
   the visual audit `blocked` — never `passed`. Also write renders to disk
   via `scene.render.filepath` + `bpy.ops.render.render(write_still=True)` so
   the user has local files. Numeric proxies cover structure and motion only.
   One useful framing proxy:
   `bpy_extras.object_utils.world_to_camera_view(scene, cam, world_co)`
   returns NDC — x/y in `[0,1]` **with z > 0** means in-frame (z ≤ 0 is
   behind the camera) — but NDC cannot tell a cylinder from a cactus.

Check silhouette hierarchy, scale cues, contact, depth separation, texture
scale, highlight/shadow detail, generated/local style coherence, and delivery
framing. One extra rule: **no asset may read as an unresolved primitive from
the active camera** unless its passport fidelity is `blockout`. A bare
cylinder standing in for a cactus, or a uniform sphere for a rock, fails this
check even when every structural metric passes.

## Specialist audits

Owned by their modules, executed here at finalize time when the Scene
Passport declares the matching work:

- **Cinematic lighting** (cinematic, commercial, product, night, atmosphere,
  reference-matched): the full "Lighting audit" in
  `blender-lighting-camera`. If isolated or grayscale evidence cannot
  be produced, the lighting audit is `blocked`, not `passed`.
- **Generated environment**: the "Audit gate" in `blender-hdri`. Record
  the SDR limitation; a GPT Image PNG is never reported as true HDR/EXR.
- **Generated PBR material**: the "Audit gate" in `blender-pbr`.
  Luminance-derived maps are inferred, not measured.

## Measuring a complaint

- Measure the quantity that was complained about, in world space over time —
  never the nearest available proxy. A perfect reading on the wrong quantity
  closes the wrong case, and the complaint returns.
- A clean zero can be the failure. A component that never varies proves rigid
  parenting as readily as correctness; pick the reference frame the physical
  claim is about — for a wheel that is the ground, not the body.
- A hidden object returns a stale matrix. Measure on a frame where it is
  visible.
- `scene.ray_cast` follows viewport visibility, not render visibility. When
  the ray and the render disagree, the render is the evidence.

## Repair loop

Fix the largest concrete failure first, then rerun the affected audit. No
polishing of secondary detail while scale, framing, contact, or motion is
wrong. A blocked check is reported as blocked — never dressed up as a pass.

## Finalize

- Modifiers, rigs, materials, and generated assets stay editable unless the
  deliverable explicitly demands destructive application.
- Proxies are removed only after their replacements pass; otherwise they are
  parked predictably and reported.
- Restore a useful frame and the intended active camera.
- Record generated job ids, models, estimates, imported object names.
- Report created/modified/deleted objects with the audit evidence.

Run `bl_finalize_build` once, after repairs. Completion requires
`valid=true`; anything else means fixing the reported structural/motion
failures and rerunning.

## Save policy

No save, save-as, overwrite, resource packing, or filepath change without an
explicit user request. When saving is requested: confirm the target
path/overwrite intent if ambiguous, save after all audits pass, and report
the actual saved path.
