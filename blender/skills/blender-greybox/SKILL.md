---
name: blender-greybox
description: Build, animate, and render a greybox scene — static stills and 2-30s motion-reference video via bl_render / bl_render_motion_reference, with shot planning and verification.
---

# Greybox

Requires: `blender-lighting-camera` for framing; `blender-animation`
when the scene is animated.

Scope: creating a greybox/blockout scene and rendering its artifact —
role-coloured semantic proxies, deterministic camera and object animation,
then a static still from the active camera, a motion video of that animation,
or both. The caller states which artifact the task needs; this module owns how
the scene is built, animated, and rendered.

## Static still

1. Frame from the active camera; check composition with `bl_screenshot`
   before spending a render.
2. `bl_render` with an explicit output path (e.g. `/tmp/<name>.png`) — the
   default temp directory is hard for the user to find (see
   `blender-volatile`).
3. View the result. A written file is not a verified render.

## Motion video — shot planning

One motion clip is **2–30 seconds**. Longer sequences split into separate
shots: a two-minute four-camera
sequence is four shot blocks, one clip per camera. One primary camera move per
clip — never hide several unrelated camera cuts inside one clip.

Each shot records:

- duration/fps and active camera;
- hero, support, background, and occluder roles;
- subject start/end transforms and key beats;
- one primary camera move, at most one subtle secondary;
- continuity anchors to adjacent shots;
- acceptance criteria: composition, path, timing, silhouette.

## Build and motion gate

1. Inspect the live scene and reuse clear existing assets before creating
   proxies. Never factory-reset a live user scene.
2. Checkpoint, then build/update role-coloured semantic proxies idempotently.
3. Animate deterministic key poses and camera motion, with readable holds and
   no random per-object movement.
4. Run `bl_validate_scene`, `bl_audit_motion`, `bl_render_contact_sheet`, and
   fix the scene until spatial and timing checks pass.
5. Call `bl_render_motion_reference` for the shot: native H.264 MP4 plus its
   exact first-frame PNG, default `1280x720`, 2–30 s, prior render settings
   restored.

An MP4 existing is not a pass. View start/middle/end and verify camera axis,
collisions, ground contact, screen direction, beat timing, and subject scale.

## Deliverable

Stills: the verified PNG. Motion: the verified MP4 plus its exact first-frame
PNG, per shot. Report local file paths, per-shot beats, and any continuity
risk between adjacent shots.
