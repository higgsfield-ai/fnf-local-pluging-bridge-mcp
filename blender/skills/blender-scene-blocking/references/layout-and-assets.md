# Layout and Assets

## Rooms and openings

Use Rectangle or L-shaped room controls for simple plans and Draw Room for a custom closed outline without self-intersections. Set dimensions and wall thickness before decorating. Floor Plan and Overview help establish circulation and camera access. For adjacent rooms, avoid duplicate shared walls and align their actual passage openings.

Disable a wall through its checkbox in Walls & Corners. Deleting its generated mesh is temporary because rebuilding restores it. Use Edit Outline, Split Wall, and Remove Corner to change the plan. Resolve affected openings before changing the number of walls; wall numbers follow the ordered outline rather than screen direction.

Door, Window, and Passage generate real openings. Position their centers with From Wall Start on the correct Wall Number, then set their dimensions and sill where applicable. Use Reposition on Wall instead of moving generated opening geometry independently. Door Open Angle can be animated. Windows provide open frames without a glass shader.

Cutaway, Complete, and Open Top affect rendering as well as the viewport. Choose the mode intentionally for the camera; ceiling fixtures can remain visible in cutaway mode. Use Ceiling and Trim controls for structural changes. Room dimensions are layout controls, not a substitute for animated geometry.

## Furniture and lighting

Choose native furniture from the thumbnail library. Place supports click placement and rotation; Object Properties provides Add at the 3D Cursor. Use Select Root and the asset's Dimensions to transform a complete piece. Moving an arbitrary child mesh breaks the intended assembly. Room resizing preserves furniture positions, so adjust their arrangement when the plan changes.

Room furniture presets require a rectangular room at least 4.8 by 4.8 meters. They add independent assets and do not replace existing furniture. Prefer individual placement when matching a reference. Thumbnails show the default assets, not a live depiction of customized geometry.

Mount ceiling fixtures through native room controls and adjust Ceiling Drop and Light Power. Keep lighting readable for the requested shot. Furniture Color affects an entire asset; separately rooted child assets remain independent. Walls Color covers the wall assembly, including its trim and opening parts. Floor and ceiling colors are separate. Use these controls for simple color blocking; create additional shaders only when requested.
