---
name: blender-volatile
description: Volatile knowledge — live model-catalog routing hints, connector build variance with fallback tools, and Blender 5.x API traps. Verify against the live environment before relying on it.
---

# Volatile knowledge

Everything in this file is tied to the live model catalog, a connector build,
or a Blender version. Verify against the live environment before relying on
it, and refresh this file when entries stop matching reality. 

## Model catalog context

Routing hints only. The live
`bl_list_models({type, include_schema:true})` schema is always authoritative
(see `blender-generation`). Entries irrelevant to Blender work
(marketing chains, social-clip, dubbing, lipsync, stylist/skin apps) are
omitted deliberately; do not route Blender requests through them. `llm_text`
is listed under the live video catalog, but job submission has previously
been refused as unavailable in alpha v2 — do not route Blender viewport
analysis through it until a real estimate and non-spending test prove the
backend accepts it.

### Image — the routes this skill consumes

| job_type | Routing knowledge |
|---|---|
| `image_auto` | Auto-selects an image model; safest ambiguous default. Prompt + optional references. |
| `gpt_image_2` | High-detail 1K/2K/4K generation/editing; the HDRI/PBR source and composition-preserving restyle route. |

The rest of the live image catalog is not routing knowledge for Blender work —
pick from `bl_list_models` output when these two do not fit.

### 3D

| job_type | Input and best use |
|---|---|
| `tripo_3d` | Text prompt → GLB. Supports face limit, geometry/texture quality, PBR, and auto size. |
| `meshy_v6_text_to_3d` | Text → GLB with topology, target polycount, remesh, PBR, optional rigging/animation. |
| `hunyuan3d_v3_1_text_to_3d` | Text → GLB with face count, mode, type, and PBR controls. |
| `sam_3_3d` | One image → textured object GLB; optional detection threshold/prompt/seed. |
| `sam_3_3d_body` | One human image → body shape/pose GLB and optional keypoints/parameters. |
| `tripo_h3_1_image_to_3d` | One image → Tripo H3.1 GLB with orientation, quad, face limit, textures, PBR. |
| `tripo_h3_1_multiview_to_3d` | Two to four ordered views → Tripo H3.1 GLB. |
| `hunyuan3d_v3_image_to_3d` | One or several views → Hunyuan GLB with face/polygon type and PBR. |
| `image_to_3d` | One image → GLB with optional texture, remesh, rigging, animation, topology, polycount. |
| `multi_image_to_3d` | One to four ordered images of the same subject → GLB; supports texture/rig/animation. |
| `3d_rigging` | Public `model_url` → rigged GLB, optionally with a predefined animation. |
| `meshy_v5_remesh` | Public `model_url` → remeshed GLB with topology/polycount/origin/height controls. |

## Connector build variance

- The typed tool set varies by connector build: production builds have lacked
  `bl_health`, `bl_scene_snapshot`, `bl_build_blockout`, `bl_checkpoint`,
  `bl_finalize_build`, `bl_set_frame`, `bl_set_transform`. Use the fallback
  table in `blender-scene` — do not skip the gates.
- `bl_screenshot` returns an r2.dev URL with roughly one-day expiry, and
  sandbox egress policies often block it. Per `blender-audit-finalize`,
  mark the visual audit `blocked`, hand the URL to the user, and also write
  renders to disk.
- `bl_render` writes to the Blender machine's temp dir (e.g. macOS
  `/var/folders/...`). Prefer explicit `/tmp/<name>.png` paths so the user can
  find them.

## Blender 5.x traps

Observed on Blender 5.x; recheck on other versions.

- **Slotted actions (5.1+):** `action.fcurves` is GONE. Access via
  `action.layers[].strips[].channelbags[].fcurves`:

  ```python
  def fcurves_of(ob):
      act = ob.animation_data.action
      slot = ob.animation_data.action_slot.handle
      return [fc for layer in act.layers
                 for strip in layer.strips
                 for cb in strip.channelbags
                 if cb.slot_handle == slot
                 for fc in cb.fcurves]
  ```

  The `slot_handle` filter is not optional: an unfiltered walk also returns
  the object-data curves and edits them by accident.

  `ob.keyframe_insert(...)` still works unchanged — only reading/editing
  curves (interpolation, easing, handles) needs the new path.
- **bmesh op naming:** it is `bmesh.ops.create_uvsphere` (one word), alongside
  `create_icosphere`, `create_grid`, `create_cone`. Snippets writing
  `create_uv_sphere` raise `AttributeError` — a common hallucinated spelling,
  not an old API.
- **EEVEE engine enum:** legacy scenes may report `BLENDER_EEVEE` while the
  render tool enum expects `BLENDER_EEVEE_NEXT`. Read the scene's current
  engine before passing one explicitly.
- **Background movie output:** Blender 5.1 background sessions can omit
  `FFMPEG` from `ImageFormatSettings.file_format` even when GUI sessions
  expose it. Use `bl_render_motion_reference`; it selects native H.264 in GUI
  and a vendored PyAV fallback in background automation.
- **Compositor:** `Scene.node_tree` is gone → `Scene.compositing_node_group`,
  and `CompositorNodeComposite` no longer exists; the group's output is the
  result. The compositing group must contain a `CompositorNodeRLayers` — feed
  it from a Group Input and nothing depends on the render, so Blender skips
  rendering entirely and writes a transparent black frame in 0.1 s. A
  suspiciously fast render is this bug.
- **Glare/Lensdist settings** moved from properties onto sockets, and the
  enums take display names: `"Fog Glow"`, `"Streaks"`, `"High"` — not
  `FOG_GLOW`.
