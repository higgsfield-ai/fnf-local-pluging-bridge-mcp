# Materials

Inspect existing material slots and shared datablocks before changing them. `bl_set_material` creates a new Principled material and replaces the first slot; use `bl_execute` when editing an existing shader graph or preserving several slots. Blender colors may use linear scene values; do not treat screenshot RGB values as automatically equivalent.

Keep texture color spaces appropriate: color textures normally sRGB, roughness/metallic/normal/displacement Non-Color. Verify UV coverage and texture scale. Judge materials using the final render engine and lighting, including both highlight and shadow response.
