---
name: ae-ui-mastery
description: Create coherent editable interface layouts in After Effects using typography, spacing, component anatomy, contrast and reusable design tokens.
---

# UI composition

Use the local `fnf-after-effects` MCP tools. Read `ae_catalog` for exact operation arguments before calling `ae_do`; availability depends on server policy and the installed AE version. Load `ae-clean-rig` as the shared construction and delivery standard. User instructions and existing project constraints take precedence over recipe defaults.

Extract the reference or brand system first. For new work, choose one coherent visual direction and define spacing, type, palette, radii, strokes and elevation before creating layers. Use the same tokens across sibling components. Defaults are adaptable, not a requirement to impose a particular brand.

A useful starting spacing scale is 4, 8, 12, 16, 24, 32, 48, 64, 96. A type scale might use 12/14/16/20/24/32/40/48/64; choose actual sizes for the output resolution and expected viewing size. Align optically where strict grid arithmetic looks wrong. Preserve reference dimensions rather than rounding them indiscriminately.

Compose readable hierarchy: one dominant message, a supporting level and restrained metadata. Use contrast, whitespace and alignment before adding glow or decorative gradients. Dark tech, editorial monochrome, warm consumer and premium finance are possible directions; do not mix their type and surface conventions without intent.

Define component anatomy: card background, heading, body, media, action and optional badge. Build text as native text, surfaces as simple shapes and icons from clean paths or authentic assets. Keep text padding and container fitting tied to source bounds without animated layout jitter. Test a longer label and an alternate image in a duplicate.

Expose a small semantic token/control set for repeated colors, corner radii and spacing. Keep source defaults distinct from instance overrides. Nest component internals while leaving useful content and controls discoverable. Review at final frame size; do not judge legibility only at a zoomed-in editor scale.
