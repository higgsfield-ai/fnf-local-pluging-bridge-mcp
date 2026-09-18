---
name: ae-depth-space
description: Companion module of ae-clean-rig, loaded on demand through ae_get_skill. Not an entry point: do not select it directly and do not use it to start After Effects work — ae-clean-rig decides when this module is needed. Covers depth and parallax with native 3D or layered 2D, perspective, shadows, atmospheric cues and restrained motion.
---

# Depth and space

Use the local `higgsfield-use-after-effects` MCP tools. Read `ae_catalog` for exact operation arguments before calling `ae_do`; availability depends on server policy and the installed AE version. Load `ae-clean-rig` as the shared construction and delivery standard. User instructions and existing project constraints take precedence over recipe defaults.

Choose depth representation from the task. Native 3D layers and cameras are available when the catalog and installed renderer support the needed operation; do not inherit the old bridge's blanket ban on cameras. Layered 2D is sufficient for many UI and illustration scenes. Do not introduce a camera merely to move flat text.

Assign coherent depth planes. Farther planes usually move less under parallax and may lose contrast, saturation and detail; keep these cues consistent. Example saturation reductions of 0/15/30/50 percent and haze increments around 15 percent are starting points, not physically universal values. Match the reference and avoid washing out readable text.

Use small contact shadows to anchor touching surfaces and broader restrained shadows for separation. Keep one light direction and check shadows after parenting or precomposition. Anchor rigid objects before rotations; inspect actual perspective rather than compensating with arbitrary skew.

Expose a depth/parallax strength control whose zero returns exactly to the baseline layout. Test foreground and background extremes for uncovered edges, excessive scale and clipping. Add camera drift or idle wiggle only when requested. Enable motion blur when motion benefits from it, then render at actual settings and check thin UI strokes and text.
