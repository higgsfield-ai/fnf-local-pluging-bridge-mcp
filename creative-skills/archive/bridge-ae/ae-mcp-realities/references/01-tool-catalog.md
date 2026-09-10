# AE MCP — tool roster

**Prerequisite: load `ae-mcp-realities` first.** It owns the value contracts (colour `{r,g,b}` 0-1, position = layer CENTRE, effect keys, easing). This file is the tool ROSTER and its enums; it does not restate those contracts.

**Invocation:** every tool goes through `custom_mcp(action="call", server="adobe_creativeapps", tool="ae_<name>", args={…})`. Below, `ae_<name>({…})` is shorthand for that call. There is no `mcp__adobeae__` form. Almost every tool takes `compositionName` (exact comp-name string) first. There is no `compId`.

## Property paths

- **Transform `propertyName` enum — exactly these 5 Capitalized strings:** `"Position"`, `"Scale"`, `"Rotation"`, `"Opacity"`, `"Anchor Point"`. Nothing else is accepted.
- **`"Source Text"` is NOT in the enum.** `ae_set_expression` and `ae_set_keyframe` reject it and no MCP tool sets text content. Set the string at creation with `ae_add_text_layer`; for character motion use `ae_create_text_animator`; for a counter use the `numberEffect` (ADBE Numbers2) or author the Source-Text expression in the AE UI.
- **Shape group:** `"Contents.Shape 1.Transform.Position"` / `".Scale"`.
- **Effect parameter:** `"Effects.Gaussian Blur.Blurriness"`.
- **Text animator:** relative paths inside animator context, e.g. `"Opacity"`.

## Tool enums (the roster's real content — these are closed sets)

| Tool | Enum param | Allowed values |
|---|---|---|
| `ae_create_text_animator` | `animatorType` | `typewriter` · `fadeInChars` · `scaleInChars` · `slideInChars` · `randomize` · `wave` (+ `duration`, default 1.5) |
| `ae_apply_effect_template` | `template` | `cinematicLook` · `glow` · `filmGrain` · `neonGlow` · `vibrance` |
| `ae_apply_expression_template` | `template` | `wiggle` · `wiggleSmooth` · `wiggleFadeIn` · `loopCycle` · `loopPingpong` · `loopOffset` · `loopContinue` · `time` · `bounce` · `inertia` · `overshoot` (+ `params?`) |
| `ae_create_transition` | `type` | `dissolve` · `wipe_left` · `wipe_right` · `zoom` |
| `ae_create_logo_reveal` | `style` | `scale` · `fade` · `slide` · `spin` (no `glitch`, no `particle`; needs a logo imported first) |
| `ae_add_shape_layer` / `ae_add_mask` | `shapeType` | `rectangle` · `ellipse` only — there is NO polygon or star |
| `ae_set_blending_mode` | `mode` | `normal` · `multiply` · `screen` · `overlay` · `add` · `lighten` · `darken` · `difference` · `softLight` · `hardLight` · `color` · `luminosity` |

An invented value outside these sets fails. For effects, the 24 registered friendly keys and the raw-match-name fallback live in ae-mcp-realities §5 — anything not in the 24 must be passed as its RAW AE match name.

## Keyframe / easing signatures

| Tool | Signature | Use |
|---|---|---|
| `ae_set_keyframe` | `{compositionName, layerName, propertyName, time, value}` | plain key, no easing; time in SECONDS |
| `ae_set_keyframe_advanced` | `{…, time, value, influence}` | key + bezier in one call; `influence` 0-100. No inType/outType/inEase/outEase params exist |
| `ae_apply_easy_ease` | `{…, propertyName, influence}` | ONE uniform ease across ALL keys of the property. No direction param. ERRORS on 2D `Position` |
| `ae_set_temporal_ease` | `{…, time? \| keyIndex?, speedIn=0, influenceIn=33, speedOut=0, influenceOut=33}` | directional / per-key. ease-OUT = high `influenceOut`; ease-IN = the reverse |

Easing values and motion timing are owned by `ae-animation-principles` — do not pick numbers here.

## Rules the tool surface enforces

- **No project lifecycle tools.** There is no `ae_create_project` and no `ae_save_project`. Start at `ae_create_composition`; refer to it by `compositionName` in every later call.
- **`ae_import_image` is the single import tool** — image OR video, `{url? | path?, compositionName?, name?, position?, scaleToFit?}` — and it also adds the layer to the comp. There is no `ae_import_footage`, no `ae_add_av_layer`, no batch import, no replace-footage, no find-missing-footage, no collect-files. One call per file. Inspect with `ae_list_project_items`; there is no folder-organize tool.
- **No camera-layer tool.** Use `ae_add_null_layer` as the camera controller and drive layers from it.
- **`ae_link_properties`** `{compositionName, sourceLayerName, sourcePropertyName, targetLayerName, targetPropertyName}` has NO `offset` param. Per-layer multipliers (parallax) require an expression on each target that scales the source value.
- **`ae_set_motion_blur`**: omit `layerName` to toggle the comp-level switch.
- **`properties` on `ae_apply_effect` / `ae_modify_effect_properties` is free-form** `{"<AE Property Name>": number | [x,y]}` and is NOT validated — no introspection. Use the exact case-sensitive strings from ae-mcp-realities §5 and verify on a live comp.
- Layers resolve by `layerName` (preferred) or 1-based `layerIndex` (1 = top). Verify existence with `ae_list_layers` / `ae_get_layer_info` before modifying.
- Absolute paths only for local files: `/Users/name/file.png`, `C:/Users/name/file.png`.

## Error → cause

| Error | Cause |
|---|---|
| Property not found | Not one of the 5 Capitalized transform props, or the path is missing its parent group |
| Value is not an array | Position/Scale/Size/Anchor Point need a TUPLE `[x,y]`, not an object `{x,y}` |
| Property is hidden | Shape-layer property not exposed until the layer exists; navigate via `Contents.…` |

## Roster

**Create:** `ae_create_composition` · `ae_add_text_layer` · `ae_add_shape_layer` · `ae_add_solid_layer` · `ae_add_null_layer` · `ae_import_image`
**Modify:** `ae_modify_layer` (incl. `newName`) · `ae_modify_effect_properties` · `ae_set_blending_mode` · `ae_set_track_matte` · `ae_add_mask` · `ae_set_motion_blur`
**Animate:** `ae_set_keyframe` · `ae_set_keyframe_advanced` · `ae_apply_easy_ease` · `ae_set_temporal_ease` · `ae_set_expression` · `ae_apply_expression_template` · `ae_link_properties` · `ae_create_text_animator`
**Effects:** `ae_apply_effect` · `ae_apply_effect_template` · `ae_set_effect_keyframe` · `ae_set_effect_expression`
**Prebuilt:** `ae_create_lower_third` · `ae_create_title_card` · `ae_create_transition` · `ae_create_logo_reveal`
**Structure:** `ae_precompose_layers` `{compositionName, layerNames, name?, moveAttributes?}` · `ae_add_marker` · `ae_set_work_area`
**Read:** `ae_list_compositions` · `ae_list_layers` · `ae_get_composition_info` · `ae_get_layer_info` · `ae_list_project_items` · `ae_export_frame` `{filename?}`
