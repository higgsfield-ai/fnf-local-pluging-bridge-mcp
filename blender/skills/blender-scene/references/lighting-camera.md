# Lighting and camera

Inspect the active camera, focal length and framing before changes. Use `bl_add_camera` and `bl_set_active_camera`; angles are radians. For a look-at orientation, derive rotation from target minus camera location with `to_track_quat('-Z', 'Y')`.

Choose a key, fill and separation only where they improve the requested image. Light size controls softness; exposure and material roughness also affect highlight appearance. Test at low resolution and sample count with `bl_render`, view the image, then raise quality. A viewport capture is not evidence of the final camera render.
