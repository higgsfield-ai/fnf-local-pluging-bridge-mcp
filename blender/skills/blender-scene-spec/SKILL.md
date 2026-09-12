---
name: blender-scene-spec
description: Scene Passport and Scene Manifest templates — the contract for scale, hierarchy, asset routing (EXISTING/BLOCK/GEN), lighting/motion intent, and acceptance criteria that every later phase measures against. Write it before any whole-scene build.
---

# Scene Passport and Scene Manifest

The Scene Passport is written before any whole-scene build and becomes the
contract everything else answers to — modeling, generation, lighting,
animation, and the final audit all measure against it.

## Passport template

```text
SCENE
- intent:
- deliverable:
- units: metres; axes: right-handed Z-up
- render: engine, resolution, fps, frame range
- dynamic: yes by default; explicit static request:

HIERARCHY
- collection/object naming:
- parent/child relationships:
- protected existing objects:

ASSETS
- A01 name | route [EXISTING|BLOCK|GEN] | fidelity [blockout|stylized|detailed]
  | dimensions [x,y,z] m | location [x,y,z] | orientation [x,y,z] rad
  | origin/anchor | parent | role
- generation estimate/submission state for each [GEN]:
- fidelity defaults: hero=detailed, midground prop=stylized,
  background=blockout; commercial/ad/deliverable intent raises every
  camera-visible tier by one. Fidelity is decided HERE, at passport time,
  not rediscovered during refinement.

SHOT
- active camera:
- framing/lens/target:
- foreground, subject, background depth:

LOOK
- material roles and palette:
- material route [EXISTING|GENERATE|NONE] / target object:
- texture scale in metres / UV or Generated coordinates:
- relief polarity / bump-only or true displacement:
- dielectric/metallic / roughness/specular intent:
- world/background:

LIGHTING
- focal subject / secondary focal point / intended darkest region:
- reference mood and time of day:
- environment route [EXISTING|GENERATE|NONE] / true HDR-EXR required:
- world-only and zero-world baseline:
- key direction / camera relation / softness:
- fill target and intended contrast:
- practical or implied source motivation:
- reflection strategy for glossy/product assets:
- gobos / flags / negative fill / atmosphere:
- color management and locked exposure:

MOTION
- fps/frame range:
- object/camera/light beats:
- rest poses and loops:

ACCEPTANCE
- structural:
- motion:
- visual: silhouette, value hierarchy, material/reflection read:
- lighting: key-only, grayscale, clipping, spill, motivation, atmosphere A/B:
```

Names are semantic and unique — `ENV_floor`, `PRP_table`, `HERO_robot`,
`CAM_main`, `LGT_key`, `RIG_turntable` — describing role, never creation
order.

## Route markers

Routes are decided by the construction routing in `blender-scene`; the passport
records the decision per asset:

- a clear existing subject → `[EXISTING]`;
- an explicit blocking request → every asset `[BLOCK]`;
- an explicit generated-3D request → only the named assets `[GEN]`; mixed
  scenes route asset by asset;
- every `[GEN]` asset keeps a proxy footprint, so generation cannot derail
  the layout.

## Dynamic default

Without an explicit static/still-only request, the passport sets
`dynamic: yes` with at least one purposeful beat. When the brief is
essentially a still, the motion stays subtle — camera drift, turntable, light
sweep, environmental movement, or an action with a stable final rest.

## Cinematic lighting intent

For cinematic, commercial, product, night, or reference-matched work, read
`blender-lighting-camera` and fill the LIGHTING section before any
secondary light exists. Every planned light carries purpose, motivation,
target, camera relation, and expected effect. Record relationships and audit
goals, never copied power presets — scene scale, source type/size/distance,
exposure, and materials make raw energy values non-portable.

An existing intentional camera, view transform, exposure, World, or rig is
preserved and recorded unless the brief demands the change. And because
lighting is camera-relative, any camera motion must state how key direction,
blockers, gobos, and reflections stay coherent across it.

## Scene Manifest

`bl_build_scene` and `bl_build_blockout` accept one JSON object:

```json
{
  "name": "Studio",
  "construction_mode": "blockout",
  "motion_mode": "auto",
  "frame_start": 1,
  "frame_end": 120,
  "collections": [{"id": "main", "name": "HF_Studio"}],
  "materials": [
    {"id": "hero-blue", "color": [0.1, 0.35, 0.8, 1], "roughness": 0.55}
  ],
  "objects": [
    {
      "id": "hero",
      "name": "HeroProxy",
      "kind": "cube",
      "role": "hero",
      "collection": "main",
      "dimensions": [2, 1, 1],
      "location": [0, 0, 0.5],
      "material": "hero-blue"
    }
  ],
  "camera": {"id": "camera", "name": "HF_Camera", "frame_objects": true},
  "lights": [
    {"id": "key", "name": "HF_Key", "type": "AREA", "location": [4, -4, 6]}
  ],
  "render": {"engine": "BLENDER_EEVEE", "resolution": [1280, 720], "fps": 24}
}
```

Manifest ids persist as custom properties, so re-running the same manifest
updates the managed datablocks instead of duplicating them. Broad builds get
a `dry_run: true` first, and complex calls get their exact field set from
`bl_describe_tool`, not from memory.

## Checkpoint manifest

Immediately before mutation, capture:

- fresh `bl_health` and `bl_scene_snapshot`;
- `bl_get_object` for protected or edited objects;
- active camera, frame range, render engine, current frame;
- `bl_screenshot` in solid or material shading;
- the planned created/modified/deleted names.

Before destructive or broad edits, also `bl_checkpoint` with a meaningful
label — a timestamped recovery copy that leaves the active filepath alone.
For risky edits, prefer new collections/datablocks and keep the replaced
originals until the audit passes.

Checkpoint after every step that lands, not only before broad ones — a live
file can lose objects between calls with no undo behind it. The label states
the state reached; copies named only by time carry no recovery information.

## Gate

Detail work starts only when every visible asset has dimensions, a route, an
origin/parent plan, and an audit criterion. Artistic details may stay open;
unknown scale, cost route, or mutation scope may not.
