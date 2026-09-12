---
name: blender-hdri
description: Generated pseudo-HDRI / environment maps — the SDR limitation, 2:1 center-crop + seam repair via bl_apply_hdri, completing directional light, and the environment audit gate.
---

# Generated environment maps (pseudo-HDRI)

Requires: `blender-generation` (credit workflow),
`blender-lighting-camera` (lighting integration), and
`skill_view("image-generation", "references/hdri-panorama.md")` (prompt
contract, model, generation parameters).

Scope: a generated HDRI, sky, panorama, or custom environment applied to the
live Blender World.

## What this output is — and is not

The generated map is an SDR PNG/JPEG, not floating-point radiance
`.hdr`/`.exr`. Name it honestly: an **AI environment map** or **pseudo-HDRI**.
It carries background, reflections, ambient color, and low-frequency fill; it
does not carry trustworthy high-dynamic-range sun values.

The image arrives at `16:9` (no native `2:1`); `bl_apply_hdri` center-crops
to `2:1` and repairs the horizontal seam. An equirectangular map wraps
horizontally only — zenith and nadir are poles, so never promise vertical
tiling.

If the deliverable explicitly requires a true HDR/EXR light probe, this
workflow does not satisfy it. Say so, and use a real bracketed/CG HDRI or an
approved radiance-reconstruction pipeline.

## Inspect before generation

1. Read `bl_scene_snapshot`, the active camera, World nodes, exposure/view
   transform, existing lights, reflective hero materials, and the motion
   range.
2. An existing suitable environment map gets reused automatically; with
   several candidates, ask which one.
3. The Scene Passport records:
   - environment description, biome/interior, time, weather, horizon height;
   - intended key/sun direction relative to the active camera;
   - what the map must supply: background only, reflections, ambient light,
     or all three;
   - dynamic camera range and seam-sensitive reflective objects;
   - the existing World/map kept for rollback.

## Prompt, model, and parameters

The prompt contract, model choice, and generation parameters live in
`skill_view("image-generation", "references/hdri-panorama.md")` — compose the
scene-specific prompt there. Then run the estimate-and-submit gate from
`blender-generation` with that job type and those params through the
connector's `bl_generate_image` — never through the image-generation skill's
own tools. State the SDR limitation alongside the estimate.

## Apply

When status is `completed`, call `bl_apply_hdri`:

```json
{
  "image_url": "<result_url>",
  "source_job_id": "<job_id>",
  "crop_to_2_1": true,
  "make_seamless": true,
  "seam_fraction": 0.05,
  "strength": 0.35,
  "rotation": 0
}
```

It downloads the result, center-crops to 2:1, blends the left/right edge
bands, writes a local PNG under `~/.higgsfield/generations/environments/`,
optionally packs it, applies it to the World, and records job provenance.
Keep the returned path and `seam_error_before/after`.

Choose the World rotation by looking at shadows, reflections, and the visible
horizon — not by picking an angle. Keep strength restrained: an SDR sky at
full strength flattens the authored lighting.

## Complete the lighting

- The AI map covers background, reflections, ambient color, broad fill.
- When the scene needs directional high-dynamic-range light, add a separate
  Sun/Area/Spot key aligned with the visible or implied sun, moon, window, or
  brightest sky region.
- Key and environment must agree in direction and hue. A painted sun pointing
  one way while cast shadows point another is an automatic failure.
- For product shots, audit reflected seam bands and panorama landmarks across
  the whole turntable; add controlled white/black cards as needed.
- The previous World stays in a disabled alternative or checkpoint until the
  new environment passes.

## Audit gate

Accepted only when viewed evidence confirms:

1. dimensions exactly `2:1`, `seam_error_after` zero or negligible;
2. no brightness/color band at the wrapped left/right seam;
3. horizon, zenith, and nadir free of obvious stretching, duplicated
   structures, text, borders, or split panels;
4. visible sun/window direction agrees with the separate key and cast shadows;
5. glossy objects expose no seam repair, duplicated landmarks, or broken
   highlight motion;
6. World strength does not flatten silhouette, contact, or focal hierarchy;
7. opening, midpoint, and final/rest frames stay coherent for animated
   cameras or turntables.

Evidence is real `bl_render_preview` / `bl_render_contact_sheet` output.
Numeric seam checks prove edge equality, not panorama quality. If renders
cannot be viewed, the environment audit is `blocked`, never `passed`.
