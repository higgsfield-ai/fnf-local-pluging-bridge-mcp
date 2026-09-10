---
name: ae-transition-kit
description: Build reusable editable After Effects transitions with independent placeholders, continuous boundary frames and resolution-aware controls.
---

# Reusable transitions

Use the local `fnf-after-effects` MCP tools. Read `ae_catalog` for exact operation arguments before calling `ae_do`; availability depends on server policy and the installed AE version. Load `ae-clean-rig` as the shared construction and delivery standard. User instructions and existing project constraints take precedence over recipe defaults.

Use two independently replaceable content sources, A and B, inside a clear transition comp. Define duration and the invariant at each boundary: before the transition only A is visible; after it only B is visible. At a reused seam, placement, opacity and motion should agree with the adjacent scene.

Expose progress, direction, edge softness and the few style-specific controls the user needs. Express distances relative to frame width/height where useful. Separate manual progress from optional automatic playback. Verify negative or out-of-range inputs are clamped or intentionally wrapped.

Door, card and peel transitions can use native 3D where supported or simple 2D mattes for a flat look. Discover operations before choosing a construction. Keep the content rig independent from decorative shading; do not bake the footage into a single flattened clip when editability is requested.

Test 0%, midpoint and 100%, plus the frames immediately before and after each seam. Replace A and B with different aspect ratios and longer content. Verify crop, alpha, overlap and motion blur at actual output settings. Export a motion-graphics template only if an available catalog operation supports the desired result and the user requests it; this runtime does not imply a Premiere connection.
