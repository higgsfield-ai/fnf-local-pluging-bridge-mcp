# AE Visual Matcher

**Dissect a reference image** and rebuild its visual properties inside After Effects using built-in effects only (no 3rd-party plugins required). It complements `ae-build-orchestration (module: scene-director)` (composition direction) and `ae-mcp-realities (module: mcp-reference)` (low-level tool/property paths).

> **Defer:** this skill produces a Visual Passport to FEED a build; when the user wants the whole frame reconstructed (not just its style matched), pass the passport to **ae-design-first** to author + build the frame as HTML.

> **Prerequisite:** load `ae-mcp-realities` first — colors are `{r,g,b}` 0-1 (not hex), position is the layer CENTER, and effect keys / property names are case-sensitive. This skill records colors as hex in the passport for human readability, but **every hex must be converted to `{r,g,b}` 0-1 before any tool call** (see "Hard rule" step 5 below).

## Hard rule

Before any `ae_*` call, you MUST:

1. **Read each image reference** using the Read tool (the image path is in the user prompt under "IMAGE REFERENCES").
2. **SAMPLE colors and gradients — don't name them by eye.** Use the `ae_measure_reference` tool so every color in the passport is a real pixel value, not a guess. Address the reference by `url` (any reachable image — a generated/Higgsfield asset, a web image, or an R2 presigned URL) or `key` (R2), and pass a batch of `ops`:
   ```
   ae_measure_reference(url|key, ops:[
     {op:"size"},                              # FIRST — learn the ref pixel space
     {op:"swatch", x,y,w,h},                   # median fill of a region (BG, panel) -> palette anchor
     {op:"pixel", x,y},                        # exact accent / text / dot color
     {op:"gradient", x1,y1,x2,y2, n:5},        # real stops + direction of any gradient
     {op:"crop", x,y,w,h, zoom:6}              # returns a URL — view it to judge texture/glow/type
   ])
   ```
   Each result carries BOTH `hex` and `rgb:{r,g,b}` 0-1 (the ae-mcp format) — keep the `rgb` for tool calls. A `crop` result returns a `url` to view the zoomed region.

   > **Reachability + fallback.** `ae_measure_reference` runs server-side, so the reference must be reachable as a URL (a generated/Higgsfield asset URL, a web URL, or an R2 key). If you only have a LOCAL file path: get it to a URL first (e.g. via the Higgsfield connector's media upload) — then measure. **If you cannot make it reachable:** fall back to viewing the image with the **Read** tool and sampling colors by eye — note the hex per passport field and say so explicitly (by-eye is less accurate, but still beats naming colors from a generic library). Either path lands you on a color per field; step 6 converts hex if needed.
3. **Write a Visual Passport** (below) — the palette/gradient fields filled from sampled values, plus type/lighting/texture readings. Passport fields are recorded as `#hex` for human readability.
4. Map every observed element to an AE effect from the **Effect Atlas** (below).
5. **Convert every hex → `{r,g,b}` 0-1 before any tool call.** Hex strings silently fail per `ae-mcp-realities` §1 — a passport hex must never flow straight into a tool call. For each color you're about to pass, explicitly compute and write out the conversion (e.g. "Hex `#2dff8a` → `{r:0.176, g:1, b:0.541}`") using the §1 formula `r=parseInt("RR",16)/255`, `g=parseInt("GG",16)/255`, `b=parseInt("BB",16)/255`. If you used `ae_measure_reference`, each result already carries the `rgb:{r,g,b}` 0-1 form — use that and skip the manual math.
6. ONLY THEN start building with `ae_create_composition` etc. — every tool is called via `custom_mcp(action="call", server="adobe_creativeapps", tool="ae_<name>", args={…})` (shorthand `ae_<name>({…})`; no `mcp__adobeae__` form — see ae-mcp-realities) and takes `compositionName` as its first param.

Skipping the passport = building blind = mismatched output. Naming colors/gradients by eye instead of sampling = washed-out, wrong-hue output. Passing raw hex into a tool call = silent wrong color. Do not skip any step.

---

## Visual Passport — fill these fields before building

```
PALETTE:
  - dark anchor:     #______  (the darkest non-black, used for BG)
  - dark mid:        #______  (secondary BG / shadow)
  - light mid:       #______  (mid-tone, often the primary subject color)
  - light highlight: #______  (highlights, glow color)
  - accent (if any): #______  (saturated pop color — neon, brand, alert)

GRADIENT:
  - type:       [none | linear | radial | conic | 4-corner | noise-driven]
  - direction:  [top→bottom | left→right | NW→SE | center-out | ...]
  - stops:      [color1 → color2 (→ color3)]   ← from `gradient` sampling, with the axis coords you used

LIGHTING:
  - key direction:   [top | top-left | left | bottom-up | front | back-rim]
  - hardness:        [hard | soft | mixed]
  - color temp:      [cool ~6500K | neutral ~5500K | warm ~3200K]
  - intensity:       [low | mid | high blow-out]
  - secondary fill:  [none | low ambient | rim from opposite side]

TYPE (if visible):
  - face:        [sans-serif geometric | sans-serif humanist | serif | mono | display | hand]
  - weight:      [thin | regular | medium | bold | black]
  - case:        [UPPER | lower | Title | Mixed]
  - tracking:    [tight -50 | normal 0 | loose +50 | wide +200]
  - color:       #______
  - treatment:   [plain | stroke | glow | drop-shadow | emboss | gradient-fill | knockout]

DEPTH / SHADOW:
  - drop shadows:    [none | soft contact | hard offset | long directional]
  - inner glow/shadow: [yes/no, color, intensity]
  - bevel/emboss:    [none | subtle | pronounced | glassy]

TEXTURE:
  - grain:           [none | light | medium | heavy]
  - noise:           [none | digital | film | analog (hue noise)]
  - artifacts:       [clean | compression banding | scanlines | chromatic aberration | dust]

ATMOSPHERE:
  - vignette:        [none | subtle | strong corner darkening]
  - haze/bloom:      [none | mild bloom on highlights | atmospheric haze]
  - light leaks:     [none | corner warm leak | streak]

GRADE:
  - black point:     [lifted | normal | crushed]
  - white point:     [normal | rolled-off]
  - saturation:      [desaturated | normal | punchy]
  - color cast:      [neutral | teal-shadows orange-highlights | unified blue | unified amber | mono]

MOTION IMPLIED (if you have to guess animation from a still):
  - direction:    [static | slow push | pull | orbit | parallax slide]
  - rhythm:       [continuous loop | one-shot reveal | rhythmic pulses]
```

After filling, write 3 lines:
- **Hero element** — what the eye lands on first.
- **Negative space** — how much of the frame is empty / dark.
- **Style label** — pick one: `cinematic | brutalist | minimal | Y2K | holographic | grunge | corporate | editorial | maximalist | glass | neon`.

---

## Effect Atlas — Visual → AE built-in effect → exact parameters

All effects below are stock After Effects. No 3rd-party. Use `ae_apply_effect { compositionName, layerName, effect, properties? }` — the `effect` string is either one of the 24 registered friendly keys OR a raw AE match name (see note below); tune parameters via `ae_modify_effect_properties { compositionName, layerName, effectName, properties }`.

> **Effect key rule.** Only these 24 friendly keys are registered: `gaussianBlur, directionalBlur, radialBlur, sharpen, brightnessContrast, curves, hueSaturation, levels, colorBalance, vibrance, exposure, tint, tritone, fill, gradient, stroke, noise, fractalNoise, addGrain, glow, dropShadow, mosaic, posterize, linearWipe, radialWipe, numberEffect`. Anything NOT in that list must be passed as its **raw AE match name** as the `effect` string (an unknown friendly key passes through unchanged and fails). Notable raw names used below: `"CC Light Burst"`, `"CC Light Sweep"`, `"CC Light Rays"`, `"CC Vignette"`, `"ADBE 4ColorGradient"` (4-Color Gradient), `"ADBE Bevel Alpha"` (Bevel Alpha), `"ADBE Turbulent Displace"` (Turbulent Displace), `"ADBE Photo Filter"` (Photo Filter), `"CC Composite"`. A gradient ramp uses the friendly key `gradient` (NOT `gradientRamp`).
> **Effect property names are NOT MCP-introspectable.** Names like `"Glow Threshold"`, `"Shadow Color"`, `"Start of Ramp"`, `"Center"` are real AE strings passed through `properties` untouched (no validation). Verify the exact spelling on a live comp in AE. `ae_list_effects` only returns `{index, name, matchName}` of effects already applied.

> **Coordinates assume a 1920×1080 comp.** Every `[960, 540]` (center), `[960, 0]` / `[960, 1080]` (top/bottom-center), and corner point in the tables below is a 2-number `[x, y]` tuple hard-coded for HD landscape. For any other comp size, **recompute** them: center = `[width/2, height/2]`, and scale edge/corner positions to the actual `width`/`height`. Per `ae-mcp-realities` §8, square (1080×1080) center = `[540, 540]` and portrait (1080×1920) center = `[540, 960]`. Origin is top-left, X grows right, Y grows down (realities §2). Effect-property coordinate values (e.g. `"Center"`, `"Start of Ramp"`) are passed as `[x, y]` arrays inside `ae_apply_effect`'s `properties` object.
> **Colors below are written as `#hex` for readability — convert each to a `{r,g,b}` 0-1 OBJECT (each channel 0-1) before the tool call** (Hard rule step 5; realities §1).

### A. Background fills & gradients

| Observed | AE effect (key) | Layer | Key parameters |
|---|---|---|---|
| Solid dark BG | `ae_add_solid_layer` with color from PALETTE.dark anchor | bottom | Color = `{r,g,b}` 0-1 from `#______` |
| Linear gradient top→bottom | `gradient` (friendly key → `ADBE Ramp`) on a solid | over BG | `Start of Ramp` = `[960, 0]`, `End of Ramp` = `[960, 1080]`, `Start Color` / `End Color` from palette (`{r,g,b}` 0-1), `Ramp Shape` = `1` (INTEGER — 1=Linear, 2=Radial; NOT a string, realities §5) |
| Radial gradient (centerlight) | `gradient` (friendly key → `ADBE Ramp`) on a solid | over BG | `Start of Ramp` = `[960, 540]`, `End of Ramp` = `[960, 1080]`, `Ramp Shape` = `2` (INTEGER — 2=Radial) |
| 4-corner gradient | `"ADBE 4ColorGradient"` (raw match name) on full-comp solid | over BG | `Point 1-4` at 4 corners (each `[x, y]`), colors from palette (`{r,g,b}` 0-1), `Blend` = `1.0`, `Jitter` = `0.05` |
| Subtle wash over BG | `tint` (friendly key) on adjustment layer | top | `Map Black To` = darkColor, `Map White To` = lightColor (both `{r,g,b}` 0-1), `Amount to Tint` = `30-60` |
| Tritone color separation | `tritone` (friendly key) | top adj | `Highlights` = light, `Midtones` = mid, `Shadows` = dark (all `{r,g,b}` 0-1) |
| Multi-stop color grade map | `"CC Toner"` (raw match name — not a registered key) | top adj | 5 stops as `{r,g,b}` 0-1 colors |
| Animated organic gradient | `fractalNoise` (friendly key) + blending mode Overlay | over BG | `Contrast` = `100`, `Brightness` = `0`, `Scale` = `300`, `Evolution` keyframed |

### B. Glows / luminescence / neon

| Observed | AE effect (key) | Layer | Key parameters |
|---|---|---|---|
| Soft text/shape glow | `glow` (friendly key) | on the layer | `Glow Threshold` = `60`, `Glow Radius` = `30`, `Glow Intensity` = `1.5`, `Glow Colors` = `1` (NUMBER toggle: `0` = Original Colors, `1` = A & B Colors — per realities §5; it does NOT take a color), `Color A` = light, `Color B` = accent (both `{r,g,b}` 0-1) |
| Hard punchy neon | `glow` (friendly key) × 2 instances | on the layer | First: `Threshold 70, Radius 8, Intensity 2.0`. Second: `Threshold 50, Radius 60, Intensity 0.8` |
| Big atmospheric bloom | `glow` (friendly key) on adjustment layer | top | `Glow Threshold` = `40`, `Glow Radius` = `120`, `Glow Intensity` = `0.5` |
| Light sweep across element | `"CC Light Sweep"` (raw match name) | on layer | `Center` = `[960, 540]`, `Direction` = `45°`, `Shape` = `0` (INTEGER — 0=Linear, 1=Smooth, 2=Sharp), `Width` = `25`, `Sweep Intensity` = `35`, `Edge Intensity` = `1.5` — keyframe `Center` for the sweep motion |
| God-rays from point | `"CC Light Rays"` (raw match name) | on light source layer | `Intensity` = `100`, `Center` = `[x, y]`, `Radius` = `50`, `Warp Softness` = `50`, `Color From` = `0` (INTEGER — 0=Light, 1=Solid) |
| Lens flare burst | `"CC Light Burst"` (raw match name) | on layer | `Center` = `[x, y]`, `Intensity` = `50` (effect property names are not MCP-introspectable — verify the exact prop name in AE before relying on it; e.g. drive ray spread through `Intensity`) |
| Volumetric light beam | `"ADBE Beam"` (raw match name — not a registered key) | shape layer | `Starting Point` = `[x, y]`, `Ending Point` = `[x, y]`, `Length` = `100`, `Starting Thickness` = `4`, `Ending Thickness` = `30`, `Inside Color`, `Outside Color` (`{r,g,b}` 0-1), `Softness` = `60` |

### C. Shadows

> **Drop Shadow `Opacity` is on the 0-255 scale, NOT 0-100** (realities §5). The `Opacity` numbers in this table read as percentages for intuition — multiply by 2.55 before the tool call (e.g. `50` → pass `~128`, `30` → `~76`, `100` → `255`). And `Shadow Color` is a `{r,g,b}` 0-1 object, not the hex shown.

| Observed | AE effect (key) | Layer | Key parameters |
|---|---|---|---|
| Standard drop shadow | `dropShadow` (friendly key) | on layer | `Shadow Color` = `{r:0,g:0,b:0}` (from #000000), `Opacity` = `50` (→ pass `~128` on 0-255 scale), `Direction` = `135°`, `Distance` = `10`, `Softness` = `15` |
| Long offset shadow | `dropShadow` (friendly key) | on layer | `Direction` = `135°`, `Distance` = `40`, `Softness` = `0`, `Opacity` = `100` (→ pass `255` on 0-255 scale) |
| Soft floor contact | `dropShadow` (friendly key) | on layer | `Distance` = `3`, `Softness` = `40`, `Opacity` = `30` (→ pass `~76` on 0-255 scale) |
| Multiple stacked shadows for depth | `dropShadow` (friendly key) × 2-3 | on layer | Stack with varying Distance / Softness / Opacity |
| Colored shadow (neon glow downward) | `dropShadow` (friendly key) | on layer | `Shadow Color` = accent `{r,g,b}` 0-1, `Softness` = `50` |
| Inner shadow effect | `"CC Composite"` (raw match name) trick OR `"ADBE Bevel Alpha"` (raw match name) with negative light | on layer | `Light Angle` = inverted, `Edge Thickness` = small |

### D. Bevel / emboss / 3D-look

| Observed | AE effect (key) | Layer | Key parameters |
|---|---|---|---|
| Subtle text emboss | `"ADBE Bevel Alpha"` (raw match name) | on text layer | `Edge Thickness` = `2`, `Light Angle` = `-60°`, `Light Color` = `{r:1,g:1,b:1}` (from #ffffff), `Light Intensity` = `0.6` |
| Pronounced beveled edges | `"ADBE Bevel Alpha"` (raw match name) | on layer | `Edge Thickness` = `4-6`, `Light Intensity` = `0.8` |
| Glossy plastic | `"CC Plastic"` (raw match name — not a registered key) | on layer | `Surface Bump From` = `Same Layer`, `Light Direction`, `Specular Highlight` = `100` |
| Glass / refraction | `"CC Glass"` (raw match name — not a registered key) | on layer | `Bump Map` = same layer, `Property` = `Lightness`, `Softness` = `7`, `Height` = `50`, `Refraction` = `1.5` |
| Metallic chrome | `"CC Glass"` (raw) + `tritone` (friendly key) + `glow` (friendly key) | on layer | Chain effects |

### E. Texture / grain / noise

| Observed | AE effect (key) | Layer | Key parameters |
|---|---|---|---|
| Film grain | `addGrain` (friendly key) | top adj | `Viewing Mode` = `1` (INTEGER — 1=Final Output), `Intensity` = `0.6`, `Size` = `1.0`, `Saturation` = `0.5`, `Monochromatic` toggle |
| Digital noise | `noise` (friendly key) | top adj | `Amount of Noise` = `10%`, `Noise Type` = `Use Color Noise` off for mono, `Clipping` on |
| Organic animated texture | `fractalNoise` (friendly key) + Overlay mode | new solid | `Contrast` = `120`, `Brightness` = `0`, `Scale` = `200`, `Complexity` = `3`, `Evolution` keyframed 0→360 over duration |
| Cracked / liquid distortion | `"ADBE Turbulent Displace"` (raw match name) | on layer | `Amount` = `15`, `Size` = `50`, `Complexity` = `3`, `Evolution` keyframed |
| Wave displacement | `"ADBE WarpWave"` (raw match name — not a registered key) | on layer | `Wave Type` = `Sine`, `Wave Height` = `5`, `Wave Width` = `40` |
| Stipple / dot halftone | `mosaic` (friendly key) + `levels` (friendly key) | on layer | `Horizontal Blocks` = `120`, `Vertical Blocks` = `68`, then `levels` to crush mids (curve points aren't MCP-settable) |
| Hexagonal tiling | `"CC HexTile"` (raw match name — not a registered key) | on layer | `Center` = `[x, y]`, `Radius` = `30` |
| Scanlines | shape layer with rect repeater + low opacity OR `"CC Slant"` (raw match name) animated | over content | |
| VHS chromatic shift | duplicate layer × 3, each with `tint` (friendly key) to R/G/B + position offset | content stack | |

### F. Blur / depth of field / atmosphere

| Observed | AE effect (key) | Layer | Key parameters |
|---|---|---|---|
| Soft background blur | `gaussianBlur` (friendly key) | on BG layer | `Blurriness` = `15-30`, `Blur Dimensions` = `Horizontal and Vertical` |
| Heavy bokeh / cinema DOF | `"ADBE Camera Lens Blur"` (raw match name — not a registered key) | on layer | `Blur Radius` = `20`, `Iris Shape` = `Hexagonal`, `Highlight Gain` = `2` |
| Motion blur trails | `"CC Force Motion Blur"` (raw match name) | top adj | `Motion Blur Samples` = `16`, `Shutter Angle` = `360` |
| Radial blur from center | `"CC Radial Fast Blur"` (raw match name) | on layer | `Center` = `[x, y]`, `Amount` = `50`, `Zoom` = `Smooth Zoom` |
| Directional speed blur | `directionalBlur` (friendly key) | on layer | `Direction` = motion angle, `Blur Length` = `40` |
| Atmospheric haze layer | duplicate of content + `gaussianBlur` (friendly key, Blurriness 30) + Opacity `30%` + Screen blend | above content | |

### G. Color grade / cinematic look

| Observed | AE effect (key) | Layer | Key parameters |
|---|---|---|---|
| Crush blacks | `levels` (friendly key) | top adj | `Input Black` = `30` — curve POINTS aren't MCP-settable (realities §5); use levels Input Black to crush |
| Lift whites (matte film) | `levels` (friendly key) | top adj | `Output Black` = `15` — curve points aren't MCP-settable; use levels Output Black to lift |
| Punch contrast | `levels` (friendly key) | top adj | `Input Black` = `15`, `Input White` = `240`, `Gamma` = `1.05` |
| Teal-orange cinematic | `colorBalance` (friendly key) | top adj | `Shadow Cyan-Red` = `-25`, `Shadow Yellow-Blue` = `+25`, `Highlight Cyan-Red` = `+20`, `Highlight Yellow-Blue` = `-20` |
| Cool blue unified | `"ADBE Photo Filter"` (raw match name) | top adj | `Filter` = `2` (INTEGER preset — 2=Cooling Filter 80), `Density` = `40` |
| Warm amber unified | `"ADBE Photo Filter"` (raw match name) | top adj | `Filter` = `0` (INTEGER preset — 0=Warming Filter 85), `Density` = `40` |
| Desaturated film | `hueSaturation` (friendly key) | top adj | `Master Saturation` = `-40` |
| Punchy modern | `hueSaturation` (friendly key) | top adj | `Master Saturation` = `+15`, `Master Lightness` = `0` |
| Vignette | `"CC Vignette"` (raw match name) | top adj | `Amount` = `-40`, `Angle of View` = `60`, `Pin Highlights` = `0` |
| Monochrome | `hueSaturation` (friendly key) + `tint` (friendly key) | top adj | Sat -100, then Tint to brand color |

### H. Distortion / stylize / glitch

| Observed | AE effect (key) | Layer | Key parameters |
|---|---|---|---|
| Glitch slice | `"CC Slant"` (raw match name) keyframed | on content | `Slant` = `0→15→-10→0` over 4 frames at glitch moment |
| Pixel sort / mosaic | `mosaic` (friendly key) | on layer | `Horizontal Blocks` = `80`, `Vertical Blocks` = `45`, `Sharp Colors` ON |
| Liquid melt | `"ADBE Turbulent Displace"` (raw match name) keyframed | on layer | `Amount` = `0→50` over 1s |
| Cartoon outlines | `"ADBE Cartoonify"` (raw match name — not a registered key) | on layer | `Rendering` = `Fill & Edges`, `Detail Threshold` = `1.5`, `Detail Radius` = `1` |
| Stained glass cells | `mosaic` (friendly key) + low blocks count + `curves` (friendly key) | on layer | `Blocks` = `40×22` |
| Find edges | `"ADBE Find Edges"` (raw match name — not a registered key) | on layer | `Invert` ON, `Blend with Original` = `0` |
| Posterize / flat color | `posterize` (friendly key) | on layer | `Level` = `5` |
| Roughen edges (organic) | `"ADBE Roughen Edges"` (raw match name — not a registered key) | on layer | `Edge Type` = `Roughen`, `Edge Color`, `Border` = `30`, `Edge Sharpness` = `0.5` |

### I. Light leaks / atmosphere

| Observed | AE effect (key) | Layer | Key parameters |
|---|---|---|---|
| Corner light leak | new solid (warm color) + `gaussianBlur` (friendly key, Blurriness 80) + Screen blend + corner position | new layer | Opacity `40%` |
| Volumetric beam | `"ADBE Beam"` (raw match name) + `glow` (friendly key) + Add blend | shape layer | (see B for Beam params) |
| Dust motes | shape layer (small ellipses) + `wiggle()` on Position | shape layer | |
| Smoke / fog | `fractalNoise` (friendly key, low contrast, gray) + Overlay blend + Opacity `40%` | new solid | `Scale` = `400`, `Evolution` keyframed |
| Film burn | `"CC Burn Film"` (raw match name — not a registered key) | on layer | `Burn` = `0.5`, `Center` = `[x, y]`, `Random Seed` = `1` |

### J. Type treatments (text-specific)

| Observed | AE effect (key) | Layer | Key parameters |
|---|---|---|---|
| Stroke / outline | `stroke` (friendly key, effect) | on text | `Color` (`{r,g,b}` 0-1), `Brush Size` = `2-4`, `Paint Style` = `On Original Image`. (Note: `ae_add_text_layer` has NO stroke param — apply the `stroke` effect instead.) |
| Knockout / hollow | text + `"ADBE Set Matte3"` (raw match name) against background OR fill alpha = 0 with stroke | | |
| Gradient fill text | text + `"ADBE 4ColorGradient"` (raw match name) on a precomp containing only the text + `"ADBE Set Matte3"` (raw) | precomp | |
| Glowing edge text | text + `stroke` (friendly key, white) + `glow` (friendly key, accent) | on text | |
| Typewriter reveal | `ae_create_text_animator { compositionName, layerName, animatorType: "typewriter", duration }` | on text | reveals chars over `duration` (built-in opacity-range animator) |
| Wiggle / unstable text | `ae_create_text_animator { compositionName, layerName, animatorType: "randomize", duration }` (closest built-in to a per-char wiggle; there is no "wiggle" animatorType — enum is typewriter\|fadeInChars\|scaleInChars\|slideInChars\|randomize\|wave). For a Position wiggle on the whole layer, use `ae_apply_expression_template { ..., propertyName: "Position", template: "wiggle" }` instead. | on text | `duration` = ~1.5 |

---

## Build sequence (after passport is written)

For each scene, follow this order — it produces clean, layered, regradeable comps. Wherever a step passes a `PALETTE.*` color into a tool, convert that hex to `{r,g,b}` 0-1 first (Hard rule step 5):

1. `ae_list_compositions {}` (verify AE connection / see what comps exist — there is no `get_project_info` tool)
2. `ae_create_composition { name, width, height, frameRate, duration, backgroundColor? }` (use width/height/frameRate/duration matched to ref aspect ratio; default `1920×1080 30fps 5–8s` loop). Returns the comp `name` — pass it as `compositionName` to every later call (there is no comp id).
3. **BG group**:
   - `ae_add_solid_layer { compositionName, name, color }` color = `PALETTE.dark anchor` (`{r,g,b}` 0-1)
   - if gradient detected: `ae_add_solid_layer` (full comp) + `ae_apply_effect { compositionName, layerName, effect }` with `effect: "gradient"` (friendly key → `ADBE Ramp`) or `effect: "ADBE 4ColorGradient"` (raw), passing stops from passport via `properties`
4. **ENV group** (atmosphere): grid lines, scanlines, fractal noise overlay if detected
5. **CONTENT group**: text layers (`ae_add_text_layer`), shape layers (`ae_add_shape_layer`) for hero element. Use exact `{r,g,b}` 0-1 from `PALETTE.light mid` / `accent`
6. **EFFECTS group**: per-layer effects from atlas via `ae_apply_effect` — `glow` for luminescence, `dropShadow` for depth, `"ADBE Bevel Alpha"` (raw) if embossed
7. **LIGHT adjustment**: top adjustment layer (`ae_add_adjustment_layer { compositionName, name? }`) with `glow` (bloom) + optional `"CC Light Sweep"` (raw)
8. **GRADE adjustment**: top-most adjustment layer with `curves` + `colorBalance` (or `"ADBE Photo Filter"` raw) + `addGrain` + `"CC Vignette"` (raw) — chain in this order
9. **Loop**: on any continuous property (Evolution, Position, Rotation) add a cycle loop via `ae_set_expression { compositionName, layerName, propertyName, expression: 'loopOut("cycle")' }`, or use `ae_apply_expression_template { ..., template: "loopCycle" }`
10. (There is no `save_project` tool — AE has no save/project-info MCP tool. Saving is done manually in AE; optionally `ae_export_frame { compositionName, time?, filename? }` to preview a frame.)

---

## Light in the passport has no light layer

Light *layers* are NOT supported (there is no `add_light_layer`; realities §11). Route every
lighting note from the passport through the **LIGHT adjustment layer** (build sequence step 7):
`"CC Light Burst"` (raw) centred on the hero for a directional key burst, or `"CC Light Rays"`
(raw) for god-ray streaks, plus `glow` for the bloom.

---

## Don'ts

- Don't apply effects you can't justify from the passport. Effect bloat = render slowdown for no visual gain.
- Don't use `dropShadow` when a `"CC Composite"` (raw match name) inner-shadow trick is appropriate — read the ref direction.
- Don't apply `glow` to every layer. Use it where there's actual luminescence, then optionally one atmospheric bloom on adjustment.
- Don't pick colors from generic libraries, and don't name them by eye. Always `swatch`/`pixel`/`gradient` the actual reference and paste the sampled hex/{r,g,b}.
- Don't skip `tint` / `colorBalance` when the ref has a unified cast — that's how cinematic looks happen.
