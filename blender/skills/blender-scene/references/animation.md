# Animation

Establish duration, frame rate, start/end state and intended motion before adding keys. Inspect existing animation to preserve curves outside the requested range. `bl_set_frame`, `bl_set_transform`, and `bl_insert_keyframe` cover basic object motion; use bpy for constraints, rigs, custom properties or interpolation.

Check start, middle and end frames plus extrema. Verify contact, camera framing, loop seams and unwanted Euler flips. Blender animation API details vary by version; inspect live version and API before addressing actions, slots or channel bags. Save the native .blend when requested and render actual frames before claiming visual completion.
