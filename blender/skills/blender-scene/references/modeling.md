# Modeling

Inspect object types, dimensions, transforms and parent relationships before editing. Keep meaningful object names and editable modifiers. Work in object mode for object-level operators; restore selection when it matters. Apply scale only when a downstream operation needs it. Duplicate or save a recovery copy before broad destructive changes within the user's scope.

Use `bl_add_primitive`, `bl_set_transform`, and `bl_get_object` for focused edits. For topology operations use `bl_execute` with explicit context and validate mesh counts, bounds, normals and silhouette afterward. Never clear the default scene as an incidental setup step in an existing project.
