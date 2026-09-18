---
name: ae-liquid-glass
description: Companion module of ae-clean-rig, loaded on demand through ae_get_skill. Not an entry point: do not select it directly and do not use it to start After Effects work — ae-clean-rig decides when this module is needed. Covers editable glass surfaces with refraction, edge light, restrained tint, shadows and verified alpha/matte behavior.
---

# Liquid glass

Use the local `higgsfield-use-after-effects` MCP tools. Read `ae_catalog` for exact operation arguments before calling `ae_do`; availability depends on server policy and the installed AE version. Load `ae-clean-rig` as the shared construction and delivery standard. User instructions and existing project constraints take precedence over recipe defaults.

Treat glass as a coordinated response to the background: slight distortion, edge light, transmission, a restrained tint and a contact shadow. A white translucent rectangle alone does not communicate refraction. Inspect installed native effects and their parameter names before constructing the stack; the recipe is not proof of availability or a validated preset for this AE installation.

Suggested component layers, top to bottom: hidden refraction-map hole; hidden refraction map; edge highlights; edge-darkness mask helper; edge darkness; color tint; main outline/matte guide; adjustment/effects surface; shadow; controller; background source. Some helpers are non-rendering. Keep independent visual roles selectable and name them by function.

Possible native building blocks include CC Glass, CC Lens, displacement, transform, blur and two light sweeps. Use only catalog-discovered effects and properties. Build one effect at a time and compare renders. Gray ramp/ring maps can guide refraction; pin the ramp to meaningful component bounds. Pair opposing light directions instead of adding an even white wash. A second sweep offset around 118 degrees is a recipe example, not a universal requirement.

Light gray edge darkness in Multiply can shade an edge without turning it into a heavy border. Keep color tint restrained. Blur and slight image expansion may prevent empty samples at displaced edges; tune to actual comp resolution and background detail. Do not blindly reuse pixel values such as blur 40 or scale 110 at every size.

Matte relationships and alpha must survive layer reorder and precomposition. Verify that an inverted hole cuts the intended region, helper layers do not leak into output, and adjustment layers affect only the intended surface. Convert centers to the needed comp/layer coordinates after parenting. Reconnect and inspect mattes after structural changes.

Expose useful controls for radius, tint, refraction, highlight and shadow. Test over bright, dark and detailed backgrounds, in motion, and at small sizes. Render edge crops and full composition; report missing effects or unsupported behavior rather than substituting an unrelated look silently.
