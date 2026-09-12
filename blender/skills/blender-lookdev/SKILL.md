---
name: blender-lookdev
description: Materials, UVs, texture scale and procedural wear serving the passport's roles; normalizes generated imports and proves the look under an active-camera render.
---

# Look development

Lookdev starts only after the blockout passes the camera-read gate, and it
serves the Scene Passport's material roles and visual hierarchy — not swatch
preferences.

## Material strategy

- `bl_set_material` covers plain Principled work: base color, metallic,
  roughness.
- `bl_execute` covers the rest: node graphs, image textures, UV work,
  bump/normal, transmission, emission, displacement, shared material
  libraries.
- One named material per role, reused across repeats — accidental
  `Material.001` variants are a defect.
- Keep shader controls exposed. Procedural masks and reusable node groups
  beat baked one-off textures where practical.
- Color, roughness, normal, and displacement are different data; each image
  texture gets the color space its data requires.
- Node trap: Map Range with `To Min > To Max` and clamp on collapses to zero
  (it clamps to an inverted interval) — invert with a `SUBTRACT` node
  instead. And a Mix node in RGBA mode carries several sockets named
  "Factor"; setting one by name can hit an unused socket and silently drop a
  branch.

## Lookdev order

1. Neutral world, broad light: validate base color and roughness first.
2. Assign roles: hero, secondary, support, ground, accent.
3. Match real-world texture scale in metres.
4. Normal/bump and edge treatment only where they change the camera read.
5. Restore the intended lighting and tune the material's response under it.

## Procedural wear

Two cheap node setups do most of the work of making a manufactured surface
look used (Cycles for Pointiness):

- **Per-part tonal variation** — Voronoi on object coordinates at low scale →
  RGB to BW → remap to roughly 0.9–1.1 → multiply into base color. Real
  material is assembled from batches that never quite match, and that
  mismatch is most of the read.
- **Edge wear** — Geometry → Pointiness remapped over a narrow band, mixed
  toward bare material and driving roughness/metallic. Free on every convex
  corner, exactly where wear happens in life.
- Weathering follows exposure: fade on surfaces facing the dominant light
  (`dot(Normal, light_dir)`), grime/deposits accumulating along one
  object-space axis. Directional wear turns a colored solid into a used
  object.

## Generated imports

An imported generated model is normalized, not trusted:

- walk every material slot and texture link;
- find missing images and unsupported node setups;
- check alpha mode, normals, roughness/metallic interpretation, UV scale;
- merge duplicate materials only when their rendered roles truly coincide;
- never silently swap a textured generated asset for a flat material.

## Render consistency

- Confirm the render engine before leaning on engine-specific nodes or
  features.
- **EEVEE renders a bare Glass BSDF as a white fill when ray tracing is
  off.** Either enable `use_raytracing` or substitute Principled with base
  0.020, roughness 0.07, transmission 0.34, `blend_method='BLEND'`, and
  backface culling.
- A surface that does not respond to any lighting change is a material
  defect, not a lighting one. Insensitivity to light is the diagnosis, and it
  is faster than eliminating light sources one by one.
- Keep color management explicit; solid shading is not a look judgment.
- Iterate in material preview; prove with `bl_render` from the active camera.
- Check highlights at the intended exposure; dark materials must keep
  readable form.
- A light emissive part on a light body has no read. Contrast comes from dark
  glass and a dark rim with emission held around 2-3; higher values blow the
  shape to flat white.
- Avoid detail frequencies that shimmer or vanish at delivery resolution.

## Gate

Lookdev is done when material roles are coherent, texture scale is
believable, generated and local assets live in one visual world, and a camera
render shows no missing textures, accidental pink surfaces, broken alpha, or
unreadable value merges.
