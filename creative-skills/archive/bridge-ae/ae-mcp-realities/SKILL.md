---
name: ae-mcp-realities
description: The parameter contract the ae_* tool surface actually enforces — colours as {r,g,b} 0-1 objects (not hex, not 0-255), position/size/scale as [x,y] tuples, position as the layer CENTER, case-sensitive effect keys and property names, easing influence and spatial arity, the registered effect roster plus raw AE match names, silent-failure modes, and the full ae_* tool catalog with its enums and worked call sequences.
---

# AE-MCP Realities

The other AE skills describe an idealized world. This skill documents the **actual API surface** of the connector (the `mcp-creativeapps` worker, exposed to the supercomputer as server **`adobe_creativeapps`**).

**Every tool is invoked through the `custom_mcp` wrapper:**
```
custom_mcp(action="call", server="adobe_creativeapps", tool="ae_<name>", args={ /* the tool's parameters */ })
```
- `tool` carries the `ae_` prefix (`ae_create_composition`, `ae_set_keyframe`, …); Premiere uses `pr_`; `get_host_status` has NO prefix.
- **There is NO `mcp__adobeae__` / `mcp__ae-mcp__` form** — it does not exist in the registry; calling it = "tool not found".
- The argument object's field is **`args`** (NOT `arguments`, NOT `input`).
- **Shorthand:** everywhere in these skills, `ae_<name>({ … })` is shorthand for the full `custom_mcp(action="call", server="adobe_creativeapps", tool="ae_<name>", args={ … })` call — the `{ … }` is the `args`.
- Inside **`ae_batch`** ONLY, each op names the tool WITHOUT the prefix (`"add_shape_layer"`) and puts its parameters under **`input`** (that is `ae_batch`'s internal shape — distinct from the outer `args`).

Every value range, color format, effect key, and property name below matches that server's schemas.

If you're about to call any `ae_*` tool — re-read the relevant section here first.

**Two universal corrections** that older skills get wrong everywhere:
1. **Invocation.** Call every tool via `custom_mcp(action="call", server="adobe_creativeapps", tool="ae_<name>", args={…})` (see the header). There is **no** `mcp__adobeae__` / `mcp__ae-mcp__` form — those do not exist. Older skills that write `mcp__…__ae_<x>` are wrong; use the `custom_mcp` wrapper.
2. **compositionName is required.** Almost every tool's FIRST parameter is `compositionName` (the exact comp-name string). Older skills omit it — always add it. There is no `compId`/comp-ID; comps are referenced by name.

> **Companion skill — full tool catalog.** This file covers the *gotcha-prone* contracts (colors, coordinates, effect keys, property names) and the call sequence. For the complete roster of tools and their roles — `ae_add_solid_layer`, `ae_modify_effect_properties`, `ae_get_layer_info`, `ae_list_layers`, `ae_precompose_layers`, `ae_import_image`, `ae_create_text_animator`, and the prebuilt templates (`ae_create_lower_third`, `ae_create_title_card`, `ae_create_transition`, `ae_create_logo_reveal`) — see the **`ae-mcp-realities (module: mcp-reference)`** skill. Tools used in the examples below but not defined here (e.g. `ae_add_solid_layer` in §9) are documented there.

---

## §1. Colors — the #1 source of silent failures

**ALL color parameters take an object `{r, g, b}` with each channel in 0-1 range.** NOT hex strings. NOT 0-255 integers. If you pass `"#ff5f57"` or `{r:255,g:95,b:87}`, the call either errors or sets a wrong color silently.

**Conversion formula** for any hex `#RRGGBB`:
```
r = parseInt("RR", 16) / 255
g = parseInt("GG", 16) / 255
b = parseInt("BB", 16) / 255
```

**Common UI colors pre-converted** (use these directly):
```
#000000  → {r:0,     g:0,     b:0}
#ffffff  → {r:1,     g:1,     b:1}
#1e1e1e  → {r:0.118, g:0.118, b:0.118}   (VSCode dark BG)
#252526  → {r:0.145, g:0.145, b:0.149}   (panel bg)
#3c3c3c  → {r:0.235, g:0.235, b:0.235}   (border)
#0078d4  → {r:0,     g:0.471, b:0.831}   (microsoft blue)
#1db954  → {r:0.114, g:0.725, b:0.329}   (spotify green)
#5865f2  → {r:0.345, g:0.396, b:0.949}   (discord blurple)
#ff5f57  → {r:1,     g:0.373, b:0.341}   (macos close)
#febc2e  → {r:0.996, g:0.737, b:0.180}   (macos min)
#28c840  → {r:0.157, g:0.784, b:0.251}   (macos max)
#4ec9b0  → {r:0.306, g:0.788, b:0.690}   (success cyan)
#cccccc  → {r:0.8,   g:0.8,   b:0.8}     (light text)
#888888  → {r:0.533, g:0.533, b:0.533}   (muted text)
```

Before any tool call that needs a color, **explicitly compute and write out** the conversion: "Hex #1db954 → {r:0.114, g:0.725, b:0.329}".

---

## §2. Coordinate system

- **Origin** is comp top-left: `[0, 0]`.
- **X grows right**, **Y grows down** (screen-space, not math-space).
- **Comp center** for a 1920×1080 comp is `[960, 540]`.
- **`position` / `size` / `scale` / `anchorPoint` are 2-number TUPLES `[x, y]`, NOT objects.** `size = [width, height]`. `scale = [xPercent, yPercent]` (e.g. `[130, 130]` for 130%). Never pass `{x,y}` or `{width,height}`.
- **Position parameter** in `ae_add_shape_layer`, `ae_add_text_layer`, etc. = CENTER of the layer's bounding box, not top-left of the layer. To place a 300×100 card whose top-left should be at [40, 80]: position = `[40 + 150, 80 + 50]` = `[190, 130]`.
- **Text layers** position = anchor point of the text (default = baseline of first char). Justification affects which edge.

---

## §3. ae_add_shape_layer — the UI workhorse

**Supported parameters (per schema):**
- `compositionName`: exact comp-name string (REQUIRED — first param)
- `name`: layer name
- `shapeType`: `"rectangle"` | `"ellipse"` (default `"rectangle"`)
- `size`: `[width, height]` (tuple, px)
- `position`: `[x, y]` (tuple, center of shape)
- `fillColor`: `{r, g, b}` in 0-1
- `roundness`: number (px) — **rectangle corner radius**. 0=sharp. Typical UI: 4/8/12/16/24. For a pill, set to `height/2`.

**NOT supported (don't try — these params do not exist):**
- ~~`shapeType: "polygon"` / `"star"`~~ — only rectangle/ellipse exist
- ~~`strokeColor` / `strokeWidth`~~ — shapes have no stroke param; for an outline, layer a slightly larger filled shape behind it, OR apply the `stroke` effect (`ADBE Stroke`) afterward
- ~~`points` / `innerRadius` / `outerRadius`~~ — no polygon/star, so these don't exist
- ~~individual corner radii~~ (top-left ≠ top-right) — use precomp+mask if needed
- ~~gradient fill on shape~~ — apply the `gradient` effect after, OR put shape in precomp + `ADBE 4ColorGradient`
- ~~drop shadow as shape style~~ — apply the `dropShadow` effect

**Naming convention:** always pass `name` with semantic value: `"card-revenue-bg"`, `"cta-button"`, `"sidebar-divider"`. Never let it default to "Shape Layer 1". You reference the layer in every later call (`ae_set_keyframe`, `ae_apply_effect`, `ae_apply_easy_ease`, …) by this exact `name` via the `layerName` parameter — so keep it unique.

**Real call example** — a rounded green CTA button (size 200×48, at top-left [880, 516]):
```
ae_add_shape_layer({
  compositionName: "MainComp",
  name: "cta-play-button",
  shapeType: "rectangle",
  size: [200, 48],
  position: [980, 540],                   // center = top-left + half size
  fillColor: {r: 0.114, g: 0.725, b: 0.329},  // #1db954
  roundness: 24                           // height/2 = pill
})
```

---

## §4. ae_add_text_layer

There is **no** `add_text_layer_advanced` tool — `ae_add_text_layer` is the only text-layer tool.

**Supported parameters (per schema):**
- `compositionName`: exact comp-name string (REQUIRED — first param)
- `name`: layer name
- `text`: string content
- `position`: `[x, y]` (tuple, anchor point)
- `fontSize`: number (pt, default 72)
- `fontFamily`: string (default `"Helvetica"`) — must match exactly an installed AE-recognized font (`"SF Pro Display"`, `"SF Pro Text"`, `"Helvetica Neue"`, `"Inter"`, `"Roboto"`, `"Segoe UI"`, `"Menlo"`, `"SF Mono"`, `"JetBrains Mono"`). To get a specific weight, include it in the family name: `"SF Pro Display Bold"`, `"Inter Medium"`, `"Helvetica Neue Black"`. **There is no separate `fontWeight` parameter.**
  **Field-tested:** if the call fails with **"Unable to set font"**, the display name with spaces didn't resolve on that system — retry with the **PostScript name** (no spaces, hyphenated weight): `HelveticaNeue`, `ArialMT`, `SFProDisplay-Bold`, `Inter-Medium`. Don't burn turns re-trying the same spaced name; one retry per fallback name down the chain, then ship with the working font. (There is no font-probe tool on this server — the AE 24+ `app.fonts` probe is a host-side API; a server-side pre-check inside ae_add_text_layer/ae_style_text is backlog.)
- `fillColor`: `{r, g, b}` in 0-1
- `justification`: `"left"` | `"center"` | `"right"` (LOWERCASE — uppercase variants and full-justify do NOT exist)

**NOT supported as `ae_add_text_layer` params — but most have a dedicated tool now:**
- `tracking` / `leading` / text stroke → **`ae_style_text({ layerName, compositionName?, fillColor?, fontSize?, font?, tracking?, leading?, strokeColor?, strokeWidth? })`** — restyles an EXISTING text layer via its text document (real text stroke incl. stroke-over-fill; colours `{r,g,b}` 0-1). Create the layer first, then style.
- text-on-path (circular seals, arcs) → **`ae_add_text_on_path`** — native editable text on a bezier path (precompose option, spinSeconds for rotating seals). Don't bake curved text into an image.
- ~~italic toggle~~ — include `"Italic"` in fontFamily
- ~~underline~~ — add a separate thin shape layer below
- ~~per-character formatting~~ — use multiple text layers, or animate with `ae_create_text_animator`

**Emoji & missing glyphs (field-tested — they fail SILENTLY):**
- **Emoji do NOT render in AE text layers** (colour-emoji fonts aren't rasterized) — the layer exists
  but paints **no ink**. Never put emoji in text (incl. HTML text for `ae_build_scene_from_html`).
  For avatars/memoji use PNG images instead: `ae_import_image` with a URL — e.g. DiceBear
  `https://api.dicebear.com/9.x/big-smile/png?seed=<name>&size=256`, then scale ~18–30%.
- **Special glyphs (→ ↑ ↓ …) can be missing** from the chosen font's fallback and also paint no ink —
  set them in `ArialMT` (has full arrows) as a separate small text layer, or draw a shape.
- Because both failures are silent, **verify ink after render**: `ae_export_frame` → pixel-probe the
  glyph zones via `ae_measure_reference` on the render URL — "no ink where a face/arrow should be"
  means the glyph didn't render.

---

## §5. ae_apply_effect — the effects API

**Signature:**
```
ae_apply_effect({
  compositionName: "MainComp",   // REQUIRED — first param
  layerName: "text-layer-1",
  effect: "<key | raw match name>",   // see below
  properties: { "<AE-prop-name>": value, ... }   // optional
})
```

The `effect` field accepts either:
- One of the **24 registered friendly keys** below (resolved to its AE match name), OR
- A **raw AE match name** like `"CC Vignette"` or `"ADBE 4ColorGradient"` for anything not in those 24.

**Critical:** the server's `resolveMatchName` passes unknown keys through **unchanged**. So an invented camelCase key (e.g. `"ccLightBurst"`, `"gradientRamp"`) becomes an *invalid* match name and the call fails. If an effect is not one of the 24 keys, you MUST pass its exact raw AE match name string instead.

### The 24 registered friendly keys (the ONLY ones) → match name

```
gaussianBlur        → ADBE Gaussian Blur 2
directionalBlur     → ADBE Motion Blur
radialBlur          → ADBE Radial Blur
sharpen             → ADBE Sharpen
brightnessContrast  → ADBE Brightness & Contrast 2
curves              → ADBE CurvesCustom
hueSaturation       → ADBE HUE SATURATION
levels              → ADBE Levels2
colorBalance        → ADBE Color Balance 2
vibrance            → ADBE Vibrance
exposure            → ADBE Exposure2
tint                → ADBE Tint
tritone             → ADBE Tritone
fill                → ADBE Fill
gradient            → ADBE Ramp        ← key is "gradient", NOT "gradientRamp"
stroke              → ADBE Stroke
noise               → ADBE Noise
fractalNoise        → ADBE Fractal Noise
addGrain            → ADBE Add Grain
glow                → ADBE Glo2
dropShadow          → ADBE Drop Shadow
mosaic              → ADBE Mosaic
posterize           → ADBE Posterize
linearWipe          → ADBE Linear Wipe
radialWipe          → ADBE Radial Wipe
numberEffect        → ADBE Numbers2
```

### Common effects NOT in the 24 → pass these RAW match name strings

```
CC Light Burst      → "CC Light Burst"
CC Vignette         → "CC Vignette"
CC Light Sweep      → "CC Light Sweep"
CC Light Rays       → "CC Light Rays"
4-Color Gradient    → "ADBE 4ColorGradient"
Bevel Alpha         → "ADBE Bevel Alpha"
Turbulent Displace  → "ADBE Turbulent Displace"
Photo Filter        → "ADBE Photo Filter"
CC Composite        → "CC Composite"
Venetian Blinds     → "ADBE Venetian Blinds"
```

For any other effect, supply its real AE match name as the `effect` string.

### ae_apply_effect_template — preset effect stacks

`ae_apply_effect_template({ compositionName, layerName, template })` applies a curated stack. `template` enum is ONLY these 5: `cinematicLook` | `glow` | `filmGrain` | `neonGlow` | `vibrance`.

### Property names per effect (most common)

These are EXACT case-sensitive AE property strings, used as keys in `properties`. **They are NOT MCP-introspectable**: the server does not validate property names (a wrong name is silently ignored — its internal try/catch eats the error), and `ae_list_effects` returns only `{index, name, matchName}` of *applied* effects, never their property schemas. Verify on a live comp if a value must be exact.

### Effect-parameter value RANGES — NOT all 0-1 (these bite)
A real failure: the model set 4-Color Gradient `Blend = 0.7` thinking 0-1; AE's range is **5–10000** (percent), and the wrong value **aborted the whole script**. Known ranges:
- **4-Color Gradient** · `Blend`: 5–10000 (default ~100; use 50–200, never 0.x — or just skip it) · `Jitter`: 0–1000 · `Opacity`: 0–100
- **Glow** · `Glow Intensity`: 0–10 (default 1) · `Glow Threshold`: 0–100 · `Glow Radius`: 0–3500
- **Drop Shadow** · `Opacity`: 0–100 · `Distance`: 0–10000 · `Softness`: 0–500
- **CC Light Sweep** · `Sweep Intensity`: 0–100 · `Width`: 1–500 · `Edge Intensity`: 0–100 · `Direction`: 0–360
- **Linear Wipe** · `Transition Completion`: 0–100 · `Wipe Angle`: 0–360 · `Feather`: 0–500
- **Fast/Box Blur** · `Blur Radius`: 0–500
- **Colours** via `setValue([r,g,b])` ARE 0–1 floats — the ONE place 0–1 is right. Everything else is whatever AE's UI shows.
- **Safety:** when unsure of a range, wrap the set so one bad value doesn't abort the script: `try { fx.property("Blend").setValue(100); } catch(e){}`. (Transform Position/Opacity/Scale have well-known ranges — this is for *effect* props.)

### Effect MATCH NAMES (canonical strings; wrong name = silent fail) — for raw JSX / `effect` arg
`ADBE Box Blur2` · `ADBE Gaussian Blur 2` · `ADBE Camera Lens Blur` · `CC Radial Fast Blur` · `ADBE Glo2` (Glow) · `ADBE Drop Shadow` · `ADBE Noise2` · `ADBE Ramp` · `ADBE 4ColorGradient` · `ADBE Fill` · `ADBE Tint` · `ADBE HUE SATURATION` · `ADBE CurvesCustom` · `ADBE Brightness & Contrast 2` · `ADBE Invert` · `ADBE Grid` · `ADBE Fractal Noise` · `ADBE Optics Compensation` · `CC Vignette` · `CC Light Sweep` · `ADBE Linear Wipe` · `ADBE Slider Control` · `ADBE Color Control` · `ADBE Point Control`

### Blur effects — MANDATORY `Repeat Edge Pixels = 0`
Default is TRUE = hard clamp at layer bounds (blur stops dead at the edge). Always: `try { blur.property("Repeat Edge Pixels").setValue(0); } catch(e){}` — for `ADBE Box Blur2`, `ADBE Gaussian Blur 2`, `ADBE Fast Blur`.

**glow (`ADBE Glo2`):**
- `"Glow Threshold"` (number, 0-100, default 60)
- `"Glow Radius"` (number, default 30)
- `"Glow Intensity"` (number, default 1)
- `"Composite Original"` (number — 0/1/2)
- `"Glow Operation"` (number)
- `"Glow Colors"` (number — 0 = Original Colors, 1 = A & B Colors)
- `"Color A"` (color object)
- `"Color B"` (color object)
- `"Color Looping"` (number)

**dropShadow (`ADBE Drop Shadow`):**
- `"Shadow Color"` (color)
- `"Opacity"` (the server passes this value straight through; AE's classic Drop Shadow Opacity is on the **0-255** scale, NOT 0-100, where 255 = fully opaque — e.g. pass 192 for ~75%, 80 for ~31%. Verify on a live comp.)
- `"Direction"` (number, degrees)
- `"Distance"` (number, px)
- `"Softness"` (number, px)
- `"Shadow Only"` (number, 0/1)

**curves (`ADBE CurvesCustom`):**
- ~~direct curve points are hard via MCP~~ — use levels or colorBalance instead

**levels (`ADBE Levels2`):**
- `"Channel"` (number — 0=RGB, 1=R, 2=G, 3=B, 4=Alpha)
- `"Input Black"` (number, 0-255)
- `"Input White"` (number, 0-255)
- `"Gamma"` (number, default 1)
- `"Output Black"`, `"Output White"`

**hueSaturation (`ADBE HUE SATURATION`):**
- `"Channel Control"` (number — 0=Master)
- `"Master Hue"` (number, -180 to 180)
- `"Master Saturation"` (number, -100 to 100)
- `"Master Lightness"` (number, -100 to 100)
- `"Colorize"` (number, 0/1)

**colorBalance (`ADBE Color Balance 2`):**
- `"Shadow Red Balance"` (-100 to 100)
- `"Shadow Green Balance"`
- `"Shadow Blue Balance"`
- `"Midtone Red Balance"`, `"Midtone Green Balance"`, `"Midtone Blue Balance"`
- `"Highlight Red Balance"`, `"Highlight Green Balance"`, `"Highlight Blue Balance"`
- `"Preserve Luminosity"` (0/1)

**tint (`ADBE Tint`):**
- `"Map Black To"` (color)
- `"Map White To"` (color)
- `"Amount to Tint"` (number, 0-100)

**CC Vignette (effect string `"CC Vignette"`):**
- `"Amount"` (number, -100 to 100; negative = darker corners)
- `"Angle of View"` (number)
- `"Center"` (position)
- `"Pin Highlights"` (number)

**CC Light Sweep (effect string `"CC Light Sweep"`):**
- `"Center"` (position)
- `"Direction"` (number, 0-360)
- `"Shape"` (number — 0=Linear, 1=Smooth, 2=Sharp)
- `"Width"` (number)
- `"Sweep Intensity"` (number)
- `"Edge Intensity"` (number)
- `"Edge Thickness"` (number)
- `"Light Color"` (color)
- `"Light Reception"` (number — 0=Add, 1=Composite, 2=Cutout)

**CC Light Rays (effect string `"CC Light Rays"`):**
- `"Intensity"` (number, 0-200)
- `"Center"` (position)
- `"Radius"` (number)
- `"Warp Softness"` (number)
- `"Shape"` (number — 0=Round, 1=Square)
- `"Direction"` (number)
- `"Color From"` (number — 0=Light, 1=Solid)
- `"Transfer Mode"` (number)

**addGrain (`ADBE Add Grain`):**
- `"Viewing Mode"` (number — 0=Preview, 1=Final Output, 2=Blending Tweaks, 3=Tweaking, 4=Final Output Mask, 5=Sample)
- `"Preset"` (number)
- `"Intensity"` (number, 0-5)
- `"Size"` (number)
- `"Softness"` (number)
- `"Saturation"` (number)

**Bevel Alpha (effect string `"ADBE Bevel Alpha"`):**
- `"Edge Thickness"` (number)
- `"Light Angle"` (number, degrees)
- `"Light Color"` (color)
- `"Light Intensity"` (number, 0-1)

**gradient (`ADBE Ramp`):**
- `"Start of Ramp"` (position)
- `"Start Color"` (color)
- `"End of Ramp"` (position)
- `"End Color"` (color)
- `"Ramp Shape"` (number — 1=Linear, 2=Radial)
- `"Ramp Scatter"` (number)
- `"Blend With Original"` (number, 0-100)
- Gradient Ramp is **2 stops** (start+end); 4-Color does 3–4. **Apply gradients with `ae_apply_gradient`** (`{compositionName, layerName, stops:[{r,g,b,pos?}], type:"linear"|"radial", angleDeg?}`) — it runs native ExtendScript that sets the Ramp/4-Color colours **reliably and READS THEM BACK to confirm** (`StartColor=[...]` in the result), **bypassing the bridge bug** where setting Ramp `Start Color`/`End Color` through raw `ae_apply_effect`+`ae_modify_effect_properties`/`ae_set_shape_fill` is **silently swallowed** (leaving the default black→white ramp, a grey/colourless plate). **Do NOT set gradient colours via the raw atomic tools — use `ae_apply_gradient`.** Use **measured** stops (`ae_measure_reference {op:"gradient"}`). **Only** genuinely painterly artwork (mesh, conic, photographic/illustrative texture — NOT a 2–4-colour card/plate ramp) is generated-and-cut as a raster (`ae_import_image`). A normal card/plate gradient is a native `ae_apply_gradient` layer — **never** a baked PNG and **never** a flat solid-fill "workaround" (that workaround existed only because the raw colour-set was broken; `ae_apply_gradient` fixes it).

**4-Color Gradient (effect string `"ADBE 4ColorGradient"`):**
- `"Point 1"` (position), `"Color 1"` (color)
- `"Point 2"` (position), `"Color 2"` (color)
- `"Point 3"`, `"Color 3"`, `"Point 4"`, `"Color 4"`
- `"Blend"` (number, 0-100)
- `"Jitter"` (number, 0-100)
- `"Opacity"` (number, 0-100)

**fractalNoise (`ADBE Fractal Noise`):**
- `"Fractal Type"` (number)
- `"Noise Type"` (number)
- `"Invert"` (number, 0/1)
- `"Contrast"` (number)
- `"Brightness"` (number)
- `"Overflow"` (number)
- `"Rotation"` (number)
- `"Uniform Scaling"` (number, 0/1)
- `"Scale"` (number)
- `"Scale Width"`, `"Scale Height"`
- `"Offset Turbulence"` (position)
- `"Complexity"` (number)
- `"Sub Settings"` ...
- `"Evolution"` (number, degrees — keyframe this for animation)
- `"Opacity"` (number, 0-100)

**mosaic (`ADBE Mosaic`):**
- `"Horizontal Blocks"` (number)
- `"Vertical Blocks"` (number)
- `"Sharp Colors"` (number, 0/1)

**Turbulent Displace (effect string `"ADBE Turbulent Displace"`):**
- `"Displacement"` (number — type)
- `"Amount"` (number)
- `"Size"` (number)
- `"Offset (Turbulence)"` (position)
- `"Complexity"` (number)
- `"Evolution"` (number)
- `"Pinning"` (number)

**Photo Filter (effect string `"ADBE Photo Filter"`):**
- `"Filter"` (number — preset, 0=Warming Filter (85), 1=Warming Filter (LBA), 2=Cooling Filter (80) ...)
- `"Color"` (color — when Filter=Custom)
- `"Density"` (number, 0-100)
- `"Preserve Luminosity"` (number)

**Pattern**: when unsure of a property name, use `ae_modify_effect_properties({ compositionName, layerName, effectName, properties })` carefully. Wrong names silently fail (the server's try/catch eats the error). There is no property-introspection tool — `ae_list_effects` only returns `{index, name, matchName}` of applied effects — so verify the visual result on a live comp if the effect must be correct.

### Animating / expressing EFFECT properties — ae_set_effect_keyframe / ae_set_effect_expression
`ae_set_keyframe`/`ae_set_expression` are **transform-only** (Position/Scale/…). For EFFECT
properties (Glow Intensity pulse, animated Blurriness, colour-shift ramps) use the dedicated pair:
- `ae_set_effect_keyframe({ compositionName, layerName, effectName, propertyName, time, value, influence? })` —
  `effectName` matches by display name OR matchName; `propertyName` is the effect's property display
  name from the §5 tables (same case-sensitivity rules); `value` is a number or array (color = the
  usual `{r,g,b}` 0-1 object is NOT accepted here — pass the array form `[r,g,b,a?]` 0-1). Optional
  `influence` (0-100) applies a BEZIER ease on that key. The call reads back `valueAtTime` — check it.
- `ae_set_effect_expression({ compositionName, layerName, effectName, propertyName, expression })` —
  sets an expression on an effect property; the result reports `expressionError` if AE rejected it —
  treat a non-empty `expressionError` as a FAILURE, don't assume it took.
- Recipe (glow pulse): apply `glow`, then `ae_set_effect_expression` on `"Glow Intensity"` with
  `Math.sin(time*4)*0.5+1.0` — or two `ae_set_effect_keyframe` calls + `influence: 75` for a settle.

---

## §6. ae_set_keyframe / ae_apply_easy_ease / ae_set_temporal_ease / ae_set_keyframe_advanced

**`propertyName` uses the CAPITALIZED enum** (NOT lowercase, and the param is `propertyName`, NOT `property`):
`"Position"` | `"Scale"` | `"Rotation"` | `"Opacity"` | `"Anchor Point"`.

**Signature:**
```
ae_set_keyframe({
  compositionName: "MainComp",   // REQUIRED — first param
  layerName: "text-layer",
  propertyName: "Position",      // Capitalized enum
  time: 0.0,                     // seconds
  value: <see below>
})
```

**Bulk keys = `ae_set_keyframes` (the COST lever for motion — use it, not per-key calls):**
```
ae_set_keyframes({ compositionName, keys: [
  { layerName: "main-card", propertyName: "Position", time: 0,   value: [540, 690] },
  { layerName: "main-card", propertyName: "Position", time: 0.9, value: [540, 648], influence: 75 },
  ...100+ keys in ONE call is fine
]})
```
- Per-key field is **`layerName`** (NOT `layer`) — a wrong field name fails per-key with "layer not found: undefined".
- Ease per key = **`influence` (0-100) + optional `speed`** — there is NO `ease:"easyEase"` keyword;
  a key without `influence` lands LINEAR (finalize will rescue easing later, but set it here when you
  know the value). Batch a whole build's motion into 2–4 calls.

**Value types per property:**
- `Position`: `[x, y]` (2D) or `[x, y, z]` (3D layer)  — **CHEAP** (transform, GPU-friendly)
- `Scale`: `[percentX, percentY]` (e.g. `[100, 100]` = 100%)  — **CHEAP** (transform, GPU-friendly)
- `Opacity`: number (0-100)  — **CHEAP** (transform, GPU-friendly)
- `Rotation`: number (degrees) OR `[x, y, z]` for 3D  — **CHEAP** (transform, GPU-friendly)
- `Anchor Point`: `[x, y]`  — **CHEAP** (transform; static-set it before animating, don't keyframe it as the motion)

> **Cheap vs heavy to animate.** The 5 transform props above (Position / Scale / Rotation / Opacity) are the **cheapest, GPU-accelerated path** — favor them for all motion. **HEAVY** (avoid keyframing where a transform substitute exists): `Source Text` (each keyframe forces a full text re-layout — and it's not MCP-reachable anyway, see §7); many simultaneous **effect params** (`ae_set_keyframes` on `"Glow Threshold"`, `"Evolution"`, gradient points, etc. each re-render the effect per frame); and **live shape-path** reveals. For a reveal, prefer a **track-matte or precompose** (§11) over animating a shape path. See §12.

**Set a uniform ease via `ae_apply_easy_ease`** (after the keys exist):
```
ae_apply_easy_ease({
  compositionName: "MainComp",
  layerName: "text-layer",
  propertyName: "Opacity",   // a SCALAR prop. Do NOT pass 2D "Position" here — see the gotcha below.
  influence: 33              // 0-100, default 33 — that's the ONLY knob
})
```
There is **no** `easeType` parameter, and no `"easeOut"`/`"easeIn"`/`"easeInOut"`/`"IN"`/`"OUT"`/`"BOTH"` values — `ae_apply_easy_ease` applies a single uniform bezier ease (controlled only by `influence`) to **all** keyframes of that property. **The keyframes must already exist** — set them with `ae_set_keyframe` first; this tool only re-interpolates existing keys, it never creates them.

> **Gotcha — `ae_apply_easy_ease` ERRORS on 2D `Position`.** It only re-interpolates scalar props that already have keys; for positional ease use `ae_set_keyframe_advanced` (key + bezier in one call) instead.

**Directional / asymmetric ease → `ae_set_temporal_ease`:**
```
ae_set_temporal_ease({
  compositionName: "MainComp",
  layerName: "text-layer",
  propertyName: "Position",
  time: 1.0,            // or keyIndex
  speedIn: 0,    influenceIn: 33,
  speedOut: 0,   influenceOut: 33
})
```
Direction is expressed through the in/out influence split: an **ease-OUT** is high `influenceOut` + low `influenceIn`; an **ease-IN** is the reverse. (See ae-animation-principles for curve values.) Use `ae_apply_easy_ease` for a quick uniform ease across all keys; `ae_set_temporal_ease` when you need a different influence/speed on one keyframe or an asymmetric in/out.

**Set a key + its bezier ease in one call → `ae_set_keyframe_advanced`:**
```
ae_set_keyframe_advanced({
  compositionName: "MainComp",
  layerName: "text-layer",
  propertyName: "Opacity",
  time: 0.0,
  value: 0,
  influence: 50
})
```

Read existing keys with `ae_get_keyframes({ compositionName, layerName, propertyName })`.

---

## §7. ae_set_expression / ae_apply_expression_template

**Signature:**
```
ae_set_expression({
  compositionName: "MainComp",   // REQUIRED — first param
  layerName: "text-layer",
  propertyName: "Opacity",       // Capitalized enum (Position/Scale/Rotation/Opacity/Anchor Point)
  expression: "wiggle(2, 8)"
})
```

The expression string is AE expression syntax. Property must already exist on the layer.

> **Only the 5 transform properties accept an expression** — `propertyName` here is the SAME Capitalized enum as keyframes (`Position` / `Scale` / `Rotation` / `Opacity` / `Anchor Point`). **`ae_set_expression` CANNOT target `"Source Text"`** (the schema rejects it, and the tool is literally "set an expression on a transform property"). There is **no** MCP tool that sets a text layer's content or a Source-Text expression. So a live numeric **counter**, a **typewriter that rewrites the string**, or expression-driven **ASCII / data text** cannot be applied through the MCP. Use instead: (a) static content via `ae_add_text_layer`; (b) per-character motion via `ae_create_text_animator` (`typewriter`/`fadeInChars`/`scaleInChars`/`slideInChars`/`randomize`/`wave` — it animates the existing characters, it does NOT change the string); (c) for anything that must REWRITE the text (counters, ticking data), author that Source-Text expression directly in the After Effects UI — it is out of MCP reach.

**Preset expressions → `ae_apply_expression_template`:**
```
ae_apply_expression_template({
  compositionName: "MainComp",
  layerName: "text-layer",
  propertyName: "Position",
  template: "wiggle",            // see enum below
  params: { /* template-specific */ }
})
```
`template` enum: `wiggle` | `wiggleSmooth` | `wiggleFadeIn` | `loopCycle` | `loopPingpong` | `loopOffset` | `loopContinue` | `time` | `bounce` | `inertia` | `overshoot`.

To wire up expression controls (sliders, etc.) use `ae_add_expression_control({ compositionName, layerName, controlType: "slider"|"angle"|"checkbox"|"color"|"point", name? })`, and link properties with `ae_link_properties({ compositionName, sourceLayerName, sourcePropertyName, targetLayerName, targetPropertyName })`.

> **Cost note.** A plain keyframed bezier ease is cheap; heavy expressions re-evaluate every property every frame. `wiggle()`, the `sampleImage`/sampler functions, and layer-space sampling (`toComp`/`fromComp`, `valueAtTime` on another layer) are the expensive ones — when several layers run them at once, **precompose** the expression-driven layers so AE caches the result rather than recomputing live. See §12.

**Common expression patterns (copy-paste-ready):**

```javascript
// loop a keyframed property forever
loopOut("cycle")
loopOut("pingpong")
loopOut("offset")

// wiggle a property
wiggle(2, 8)         // 2Hz frequency, 8 unit amplitude

// link to another layer's property
thisComp.layer("Null 1").transform.position

// time-based animation
[value[0] + Math.sin(time * Math.PI * 2 * 0.5) * 10, value[1]]

// counter text — returns a STRING, so it can only live on Source Text, which
// ae_set_expression cannot target (see the caveat above). Author this one in the
// AE UI directly — it is NOT applicable via MCP.
Math.round(time * 100).toString()

// flicker — apply to Opacity (a valid transform property), NOT to Source Text
(time * 4) % 1 < 0.1 ? 0 : 100

// stepped time
posterizeTime(12);
wiggle(8, 30)
```

---

## §8. Composition setup

```
ae_create_composition({
  name: "MainComp",
  width: 1920,            // px
  height: 1080,           // px
  frameRate: 30,          // default 30
  duration: 8,            // seconds, default 5
  backgroundColor: {r: 0, g: 0, b: 0}   // 0-1 range, optional
})
```

Returns `{name, width, height}` — there is **no** comp ID / `compId`. Every later call references the comp by its name via the `compositionName` parameter. Keep comp names unique to avoid ambiguity. Related comp tools: `ae_modify_composition`, `ae_duplicate_composition`, `ae_get_composition_info({ compositionName })`, `ae_list_compositions({})`.

**Common comp dimensions:**
- HD landscape: 1920×1080
- 4K: 3840×2160
- Square (social): 1080×1080
- Vertical (TikTok/Stories): 1080×1920
- Cinema 2.39:1: 2048×858

---

## §9. Workflow for a complex scene — the actual call sequence

For a UI reference matching a dashboard screenshot (every call carries `compositionName`; positions/sizes are tuples):

```
1.  ae_create_composition({name:"MainComp", width:1920, height:1080, frameRate:30, duration:8})   → returns {name,...}; reference by compositionName from here on
2.  ae_add_solid_layer({compositionName:"MainComp", name:"BG", color:{r:0.07,g:0.07,b:0.07}})
3.  ae_add_shape_layer({compositionName:"MainComp", name:"sidebar-bg", shapeType:"rectangle", size:[240,1080], position:[120,540], fillColor:{r:0,g:0,b:0}})
4.  ae_add_shape_layer({compositionName:"MainComp", name:"sidebar-divider", shapeType:"rectangle", size:[1,1080], position:[240,540], fillColor:{r:0.235,g:0.235,b:0.235}})
5.  ae_add_text_layer({compositionName:"MainComp", name:"logo", text:"Brand", fontFamily:"SF Pro Display Bold", fontSize:22, position:[30,50], fillColor:{r:1,g:1,b:1}, justification:"left"})
6.  ... repeat for every measured element from ae-build-orchestration (module: ui-rebuilder) Measurement section ...
7.  ae_add_shape_layer({compositionName:"MainComp", name:"cta-button", shapeType:"rectangle", size:[160,44], position:[1700,60], fillColor:{r:0,g:0.471,b:0.831}, roundness:8})
8.  ae_add_text_layer({compositionName:"MainComp", name:"cta-text", text:"Get Started", fontFamily:"Inter Medium", fontSize:14, position:[1700,67], fillColor:{r:1,g:1,b:1}, justification:"center"})
9.  ae_apply_effect({compositionName:"MainComp", layerName:"cta-button", effect:"dropShadow", properties:{"Shadow Color":{r:0,g:0.471,b:0.831},"Opacity":80,"Direction":135,"Distance":0,"Softness":24}})   // "Opacity" is 0-255 → 80 ≈ 31% (subtle)
10. ... animations: ae_set_keyframe + ae_apply_easy_ease (influence) per element ...
11. ae_add_adjustment_layer({compositionName:"MainComp", name:"GRADE"})
12. ae_apply_effect({compositionName:"MainComp", layerName:"GRADE", effect:"CC Vignette", properties:{"Amount":-25}})   // raw match name — ccVignette is NOT a registered key
13. ae_apply_effect({compositionName:"MainComp", layerName:"GRADE", effect:"addGrain", properties:{"Intensity":0.3,"Viewing Mode":1}})
```

**There is no project-info step and no save step** — the server exposes neither `get_project_info` nor `save_project` (see §11). Begin straight at `ae_create_composition`; preview/export single frames with `ae_export_frame` if needed.

---

## §10. Common silent-failure modes

1. **Wrong invocation** → tool not found. FIX: go through `custom_mcp(action="call", server="adobe_creativeapps", tool="ae_<name>", args={…})`. There is no `mcp__adobeae__` / `mcp__ae-mcp__` tool.
2. **Missing `compositionName`** → call errors or targets the wrong/active comp. FIX: pass `compositionName` (exact comp name) as the first param on every tool.
3. **Color as hex** → tool fails silently, layer has wrong color (default black or last default). FIX: always pass `{r,g,b}` 0-1.
4. **position/size/scale as an object `{x,y}` / `{width,height}`** → wrong placement or rejected. FIX: pass a `[x, y]` tuple; `size=[w,h]`, `scale=[xPct,yPct]`.
5. **Lowercase `property` / wrong propertyName** → key not set. FIX: param is `propertyName` and uses the Capitalized enum `"Position"`/`"Scale"`/`"Rotation"`/`"Opacity"`/`"Anchor Point"`.
6. **`easeType` on apply_easy_ease** → no such param; value ignored. FIX: `ae_apply_easy_ease` takes only `influence` (uniform); for directional ease use `ae_set_temporal_ease` with `influenceIn`/`influenceOut`.
7. **Effect property name wrong case** → property not set, no error (try/catch eats it; not introspectable). FIX: use exact strings from §5, verify on a live comp.
8. **Invented effect key** (e.g. `gradientRamp`, `ccLightBurst`) → passed through as an invalid match name, call fails. FIX: use one of the 24 keys (`gradient`, not `gradientRamp`) OR the raw AE match name (`"CC Light Burst"`).
9. **Position is anchor not top-left** → layers placed wrong relative to measurement. FIX: position = top-left + half-size.
10. **roundness on non-rectangle shape** → ignored. FIX: only use roundness with `shapeType: "rectangle"`.
11. **fontFamily without weight suffix** → defaults to Regular. FIX: include weight in name: `"SF Pro Display Bold"`.
12. **set_keyframe before layer exists** → tool throws. FIX: ensure the `ae_add_*_layer` call succeeded first, use that exact layer name.
13. **Multiple comps named same** → ambiguous. FIX: keep comp names unique (there is no `compId`; comps are referenced only by name).

---

## §11. What's NOT possible (don't promise the user)

**No such tools (do NOT call or imply they exist):**
- **No camera-layer creation** — there is no `ae_add_camera_layer`. For a push-in / parallax, add an `ae_add_null_layer`, parent layers to it (`parentLayerName`), and animate the Null's `Scale`/`Position`.
- **No light-layer creation** — there is no `add_light_layer`. Fake lighting with an `ae_add_adjustment_layer` + the `glow` effect or raw `"CC Light Rays"` / `"CC Light Burst"`.
- **No `get_project_info` and no `save_project`** — there is no project-info or save/render tool at all. The MCP mutates the open project live; there is nothing to save or render from here. For final output use AE's own UI / `aerender` CLI externally; single-frame previews via `ae_export_frame`.

**Possible but worth noting — track mattes ARE supported:** use `ae_set_track_matte({ compositionName, layerName, matteLayerName, type: "alpha"|"alphaInverted"|"luma"|"lumaInverted" })`. Blending modes via `ae_set_blending_mode`, masks via `ae_add_mask`, motion blur via `ae_set_motion_blur`, precompose via `ae_precompose_layers`. **To clip an image/video into a shape** (circular avatar, rounded thumbnail): place the media layer ABOVE the shape layer, then `ae_set_track_matte({ compositionName, layerName: <media>, matteLayerName: <shape>, type: "alpha" })` — the shape becomes the mask (a rectangle's `roundness` sets the corner radius).

**Genuinely not available:**
- Per-corner radii (only uniform roundness)
- Polygon / star shapes and shape strokes (see §3). (TEXT strokes ARE possible now — `ae_style_text`, §4.)
  **The field-standard workaround for outlines/frames = DOUBLE PLATE:** outer shape in the
  frame colour + inner shape in the bg colour, inset by the border width (r_inner = r_outer −
  border). Works for outline pills/CTAs, badges (e.g. an "AD" frame), 3px photo-card frames —
  verified across real builds. **Hollow display text** (outline-only headline): `ae_style_text`
  with `fillColor` = the BACKGROUND hex + `strokeColor` = accent, `strokeWidth` 2–3.
- Mocha tracking, Roto Brush, Content-Aware Fill
- 3rd party plugins (Trapcode, Element 3D, Saber, Plexus)
- Direct image-to-mask conversion
- Custom Bezier shape paths beyond rectangle/ellipse primitives
- Audio mixing / sub-tracks
- Render queue control (render externally with `aerender`)

If the user asks for any of the genuinely-unavailable items, propose a workaround using the built-in tools above.

---

## §12. GPU-friendly animation — cheap motion that actually previews fast

AE's render path is fastest when motion lives on the **transform** properties; everything else makes the layer re-render per frame. Default to the cheap path; reach for the heavy one only when the look genuinely demands it.

**The cheap path (use this by default):**
- **Animate only Position / Scale / Rotation / Opacity** (the transform props from §6). These ride AE's GPU-accelerated transform pipeline — they don't force the layer's pixels to re-render, just re-transform. Anchor Point counts too, but set it once before animating, don't keyframe it as the motion.
- **Cubic-bezier easing is free.** A keyframed ease (`ae_apply_easy_ease` / `ae_set_temporal_ease` / `ae_set_keyframe_advanced`, house settle-weight ≈ in22/out75) costs essentially nothing per frame — it's just curve evaluation. Prefer it over expression-driven motion wherever a static keyframe pair would do.

**The heavy path (precompose / substitute):**
- **Source Text re-layout.** Keyframing or expression-driving the text string re-lays-out the whole layer each frame (and isn't MCP-reachable — §7). For "appearing text", animate the text layer's **Opacity/Position** or use `ae_create_text_animator` (per-character transform), never the string.
- **Many simultaneous effect params.** Each keyframed effect property (`"Glow Threshold"`/`"Glow Radius"` via `ae_set_keyframes`, `"Evolution"` on fractal/turbulent noise, gradient `"Start of Ramp"`, etc.) re-renders that effect every frame. Keyframe **one** signature effect param, not five at once; bake the rest static.
- **Live shape-path reveals.** Animating a mask/shape path for a wipe is costly. Prefer a **track-matte reveal** (a moving solid/shape as the matte) or **precompose** the artwork and animate the precomp's Position/Scale behind a static matte (§11) — the reveal then runs on the cheap transform path.
- **Heavy expressions.** `wiggle()`, `sampleImage`/samplers, and layer-space sampling (`toComp`/`fromComp`, cross-layer `valueAtTime`) recompute every frame. **Precompose** the layers carrying them so AE caches the rendered result.

**Rule of thumb — the profiler pass:** once a comp has **> 10 layers animating simultaneously**, do a profiler/precompose pass before adding more. Group finished, independently-animating clusters into precomps (`ae_precompose_layers`) so each renders + caches as a single layer, and collapse any heavy-expression or effect-keyframed layers into precomps. This keeps the live transform count low and RAM-preview responsive.

**Quick triage when a build previews slowly:**
1. Count simultaneously-animated layers — over ~10, precompose finished clusters.
2. Move any motion off Source Text / shape paths onto transform + Opacity (or a track-matte reveal).
3. Reduce to one keyframed param per effect; bake the rest.
4. Precompose every `wiggle`/sampler/cross-layer-expression layer.
