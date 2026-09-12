---
name: blender-pbr
description: Generated tileable PBR — one seamless albedo tile with every map derived in Blender via bl_apply_pbr_maps, material-specific decisions, and the PBR audit gate.
---

# Generated tileable PBR materials

Requires: `blender-generation` (credit workflow),
`blender-lookdev` (material integration),
`blender-audit-finalize` (PBR audit), and
`skill_view("image-generation", "references/pbr-albedo.md")` (prompt
contract, model, generation parameters).

Scope: a generated material, seamless texture, or PBR map set.

## Core method

Generate **one** seamless flat albedo swatch, then derive every
geometry/shading map from that same tile in Blender via `bl_apply_pbr_maps`.
Never generate Base Color, Normal, Displacement, AO, and Specular as separate
image jobs — independent generations do not align at the pixel level and
cannot form a coherent set.

The derived maps are coherent but **inferred**, not scan data:

- **Base Color** — the generated tile, treated as sRGB.
- **Displacement/Height** — normalized luminance; bright means high unless
  `invert_height:true`.
- **Normal** — tile-aware central gradients of that height map.
- **Ambient Occlusion** — tile-aware local cavity estimate from height.
- **Specular** — a constant dielectric level by default, because albedo does
  not reliably encode IOR/specular response; optional luminance/height
  modulation is an artistic mode, not a measurement.

When pigment and physical relief are unrelated, or the deliverable demands
scan-grade maps, do not pretend luminance-derived height is accurate — use
authored or scanned height/specular data instead.

## Inspect and specify

1. Inspect the live object: material slots, UV maps, dimensions, render
   engine, subdivision, displacement support, intended camera scale.
2. One clear suitable existing texture set gets reused automatically; ask
   only when several candidates are plausible.
3. The Scene Passport records:
   - object and semantic material role;
   - real-world tile width/height in metres;
   - surface description, age, wear, grain/fiber direction, palette;
   - relief polarity — whether bright or dark features are raised;
   - dielectric/metallic behavior, roughness, specular intent;
   - UV or Generated coordinate route;
   - bump-only versus true Cycles displacement.

## Prompt, model, and parameters

The prompt contract, model choice, and generation parameters live in
`skill_view("image-generation", "references/pbr-albedo.md")` — compose the
material-specific prompt there. Then run the estimate-and-submit gate from
`blender-generation` with that job type and those params through the
connector's `bl_generate_image` — never through the image-generation skill's
own tools. State the inferred-map limitation alongside the estimate.

## Derive and apply

After completion, call `bl_apply_pbr_maps`:

```json
{
  "object": "<exact mesh object>",
  "image_url": "<result_url>",
  "source_job_id": "<job_id>",
  "map_resolution": 2048,
  "seam_fraction": 0.05,
  "tile_scale": 1,
  "coordinate_mode": "auto",
  "height_contrast": 1,
  "invert_height": false,
  "normal_strength": 2,
  "ao_radius": 8,
  "ao_strength": 2,
  "specular_level": 0.5,
  "specular_mode": "constant",
  "displacement_scale": 0.05,
  "bump_strength": 0.35,
  "metallic": 0,
  "roughness": 0.5
}
```

It center-crops square, repairs all four tile edges, writes Base
Color/Normal/Displacement/AO/Specular PNGs under
`~/.higgsfield/generations/pbr/<job-id>/`, optionally packs them, builds one
repeatable Mapping-driven material (AO multiplied into Base Color, Specular
wired to Principled, Normal combined with a Displacement-derived bump), and
connects true displacement for Cycles where supported.

No automatic destructive subdivision. True displacement needs Cycles plus
sufficient non-destructive subdivision; EEVEE and unsubdivided meshes get the
bump/normal result. Use UV coordinates whenever a valid UV map exists —
Generated coordinates are a fallback, not a substitute for deliberate UVs on
hero assets.

## Material-specific decisions

- **Stone, plaster, bark, concrete:** luminance-derived relief is a workable
  start; verify polarity and lower displacement before ever raising it.
- **Wood:** align grain with UV orientation; a unique knot must not expose the
  repeat at hero scale.
- **Fabric:** small displacement, stronger micro-normal; large
  luminance-derived height reads inflated.
- **Painted/printed surfaces:** pigment is not height. Low height contrast,
  constant dielectric specular.
- **Metal:** `metallic:1` — a grayscale Specular map is not a metallic
  workflow. Base Color then represents conductor reflectance.
- **Wet/varnished:** brightness does not imply coating; tune
  roughness/coating explicitly in lookdev.

## Audit gate

Approved only when viewed evidence confirms:

1. `seam_error_after.horizontal` and `.vertical` zero or negligible;
2. a plane with at least 3x3 repetitions shows no cross-shaped seams,
   mirrored edge bands, brightness drift, or an obvious repeated landmark;
3. Base Color carries no baked directional shadows, highlights, AO, text,
   border, or perspective;
4. Normal direction is correct under a grazing moving light, with no
   inverted-green-channel look;
5. displacement polarity is right, the silhouette stays plausible, and scale
   is measured against the object's metre dimensions;
6. AO darkens cavities without dirtying all color or double-shadowing;
7. Specular matches the dielectric/metal intent instead of merely copying
   albedo brightness;
8. UV/Generated coordinates and `tile_scale` match the declared real-world
   texel scale;
9. opening, midpoint, and final turntable frames expose no seams or texture
   swimming.

Use `bl_render_preview`, plus `bl_render_contact_sheet` for dynamic scenes.
Numeric seam equality does not prove the tile looks natural. If the rendered
material cannot be viewed, the PBR audit is `blocked`, never `passed`.
