# AE UI Rebuilder

This skill reconstructs UI screenshots inside After Effects. The output is **not a screenshot pasted as a footage** — it's a fully editable layer stack where each UI element is its own shape/text layer with proper hierarchy, animatable independently.

> **Prerequisite:** load `ae-mcp-realities` first — colors are `{r,g,b}` 0-1 OBJECTS (not hex), position/size/scale are 2-number `[x,y]` TUPLES (size = `[width,height]`), position is the layer CENTER (top-left + half size), `propertyName` uses the Capitalized enum, effect keys / property names are case-sensitive. This skill issues `ae_*` calls via the `custom_mcp` wrapper (`custom_mcp(action="call", server="adobe_creativeapps", tool="ae_<name>", args={…})`; shorthand `ae_<name>({…})`; no `mcp__adobeae__` form — see ae-mcp-realities), and every tool's first param is `compositionName`, so those contracts apply to every layer you build here.

> **Defer:** if the screen can be faithfully mocked in HTML/CSS, build it with **ae-design-first** (`ae_build_scene_from_html`, one call) instead. Use this skill only when the screenshot is opaque and needs a measured, pixel-exact rebuild.

This complements `ae-build-orchestration (module: visual-matcher)` (which extracts palette and style). Use both when a UI screenshot is the reference. Animation recipe codes used below (R1 Fade-Up, R3 Slide-In, R4 Typewriter/caret, R13 Counter — and any other `R#`) are defined in **`ae-animation-principles`**: that skill's Recipe Library is where the recipe library lives, so look the code up there before keyframing. For the full tool roster and import behavior, see **`ae-mcp-realities (module: mcp-reference)`**.

---

## Measurement procedure — fill BEFORE construction

> **MEASURE, don't eyeball.** Vision is unreliable for exact pixels — coords, corner radii, gradient stops, tiny icons, font size. You have a measurement toolkit; USE IT instead of guessing. A "looks about 8px" radius or a hand-picked hex is the #1 cause of references coming out wrong.

### 0. Reference-measurement tool (call it, paste the numbers)

> **Use the `ae_measure_reference` tool** — it measures the reference server-side (Pillow). Address the reference by `url` (any reachable image — a generated/Higgsfield asset, a web image, or an R2 presigned URL) or `key` (R2). **Reachability + fallback:** if you only have a LOCAL file path, get it to a URL first (e.g. via the Higgsfield connector's media upload) then measure. **If you cannot make it reachable:** `Read` the screenshot (and `crop`-zoom close reads via any tool that can) and eyeball coords/colors/radii — but say so explicitly, because eyeballed numbers are the #1 cause of references coming out wrong (see the MEASURE box above). Prefer measuring over guessing.

```
ae_measure_reference(url|key, ops:[
  {op:"size"},                          # FIRST — get ref pixel space
  {op:"crop", x,y,w,h, zoom:6},          # zoom a region; the result returns a URL — view it to SEE detail
  {op:"swatch", x,y,w,h},                # median fill color of a panel/card interior
  {op:"pixel", x,y},                     # exact color of one point (stroke, text, dot)
  {op:"gradient", x1,y1,x2,y2, n:5},     # real gradient stops + direction along an axis
  {op:"radius", x,y,w,h, corner:"tl"},   # measured corner radius in px (NOT a guess)
  {op:"fontsize", x,y,w,h}               # cap-height -> font-size estimate
])
```

Each result carries BOTH `hex` and `rgb:{r,g,b}` 0-1 (the ae-mcp format) — **pass the `rgb` form to ae-mcp; the hex will silently fail (ae-mcp-realities §1).** Every coordinate, width, height, stroke width, AND corner radius the tool reports is in **REF pixel space** (the screenshot's own resolution). **Multiply each of these by SCALE before building** — including `roundness` / corner radii (a 12px radius at SCALE 1.5 becomes 18px). Colors are NOT scaled.

Mandatory minimum before construction (batch them in one `ae_measure_reference` call where you can):
1. `size` once.
2. `crop` (zoom) every small element (icons, badges, dense text, corners) and view the returned URL — never measure a <40px element from the full image.
3. `radius` for every rounded surface (don't default it) — then multiply the measured radius by SCALE for the `roundness` parameter.
4. `swatch`/`pixel` for every fill/stroke/text color (don't name colors by eye).
5. `gradient` for every gradient (don't guess direction or stops).
6. `fontsize` for at least the title, body, and caption tiers.

### 0b. Live bounds rig (`sourceRectAtTime`) — size to content, don't hardcode

A built text/shape layer reports its OWN rendered bounds via `sourceRectAtTime(t, includeExtents=true)` → `{left, top, width, height}` in the layer's space. Use this to make containers RESPONSIVE to their content instead of pasting a measured `[w,h]` that breaks the moment the copy or font changes:

- **Background sized to text.** Drive a behind-rect's **Scale** (a transform prop — legal for `ae_set_expression`, ae-mcp-realities §5) off the text's measured extent: `ae_set_expression { compositionName, layerName:"card-bg", propertyName:"Scale", expression:"t=thisComp.layer('card-title').sourceRectAtTime(); pad=24; [ (t.width+2*pad)/100*100, (t.height+2*pad)/100*100 ]" }` (build the base rect at 100×100 so the ratio reads cleanly, or compute against your real base size). Padding lives in the expression, not in a frozen width.
- **Pin to the moving edge.** A divider/underline that must hug a label: read `sourceRectAtTime().width` of the label and drive the divider's **Position** X (transform prop — legal). Re-flows automatically when text length changes.
- **Contract guard:** `ae_set_expression` is TRANSFORM-ONLY — read `sourceRectAtTime` of any layer, but only ever ASSIGN it to `Position` / `Scale` / `Rotation` / `Opacity` / `Anchor Point`. Never onto Source Text or an effect prop. The right pattern is "text layer's bounds drive the SHAPE layer's transform," not the text's own text.
- **Two ported container helpers (run via `execute_script` — they touch shape Rect props / Source Text, which `ae_set_expression` can't reach):**
  - **`autoFitPill`** — a rounded-rect that **adapts to its text** (lower-third, name tag, chip, button, tooltip, badge). Writes expressions on the rect's Size + Position; the live-refit trick is reading the text layer's `.text.sourceText` INSIDE the expression so AE re-evaluates on every edit, plus `sourceRectAtTime(time,false).width`. Default pins the LEFT edge (grows right); `center=true` grows symmetrically. **Opposite of fitText** (box adapts to text, not text to box).
    ```jsx
    function autoFitPill(rectPath, textLayerName, padW, pillH, center){ padW=(padW==null?80:padW); pillH=(pillH==null?0:pillH); var base='var n=thisComp.layer("'+textLayerName+'");var st=n.text.sourceText;var r=n.sourceRectAtTime(time,false);var w=(r&&r.width>0)?r.width:0;'; var h=(pillH>0)?String(pillH):'((r?r.height:0)+50)'; rectPath.property("ADBE Vector Rect Size").expression=base+'[w+'+padW+','+h+'];'; rectPath.property("ADBE Vector Rect Position").expression=center?'[0,0];':(base+'[(w+'+padW+')/2,0];'); }
    ```
  - **`fitText`** — iteratively **shrinks fontSize** until the text fits a FIXED container (no overflow/clip). Re-reads the TextDocument after each `setValue` (it's a snapshot — refetch each iteration).
    ```jsx
    function fitText(L, maxW, maxH, minSize){ minSize=minSize||10; var src=L.property("Source Text"), td=src.value; for(var i=0;i<18;i++){ var r=L.sourceRectAtTime(0,false); var overW=r.width>maxW; var overH=maxH?(r.height>maxH):false; if((!overW&&!overH)||td.fontSize<=minSize) break; td.fontSize=Math.max(minSize,td.fontSize-2); src.setValue(td); td=src.value; } }
    ```
  - Use `autoFitPill` when the box should adapt (the plate-too-small / clipped-label bug); `fitText` when the box is fixed and text must shrink in.

### 0c. Anchor-point snapping (so transforms pivot where you measured)

Off-center anchors are the #1 cause of a "scaled" element drifting. Set the anchor deliberately:

- **Pan-Behind (Y) tool + Shift** — drag to reposition the anchor while Shift LOCKS it to the X or Y axis (no diagonal slip).
- **Ctrl+drag** the anchor — snaps it to comp guides / layer edges.
- **Cmd+Opt+Home** (mac) / **Ctrl+Alt+Home** (win) — resets the anchor to the layer's CENTER in one shot; do this before any Scale-from-center entrance.
- Anchor lives in layer space; after moving it, re-confirm `position` (still the CENTER convention, §2) hasn't shifted the layer on screen.

### 1. Canvas
```
REF DIMENSIONS:   _____ x _____ px        (actual pixel size of the screenshot)
TARGET COMP:      1920 x 1080 30fps  OR matched ref aspect ratio  OR 1080 x 1920 for mobile UI
SCALE FACTOR:     target_width / ref_width = _____    (multiply all measured coords, sizes, stroke widths, font sizes AND corner radii by this — colors are not scaled)
```

### 2. Grid & rhythm
```
COLUMNS:          [4 | 6 | 8 | 12 | none-bespoke]
GUTTER:           _____ px      (space between columns)
MARGIN (outer):   _____ px      (canvas → first content)
BASE UNIT:        [4 | 8 | 12 | 16] px   (smallest consistent spacing — usually 8 for web, 4 for dense UI)
```

### 3. Anatomy — list every distinct UI element
For each element measure: bounding box `[x, y, w, h]`, content, style. Number them top-to-bottom, left-to-right. **`x, y` here are the TOP-LEFT corner of the measured bbox** (toolkit convention) — NOT a position you can pass to ae-mcp as-is (see the conversion rule below). Whenever you express a measured bbox/size/position as a tool argument, write it as a `[x,y]` / `[w,h]` TUPLE (never an object `{x,y}`/`{width,height}`):

> Hex codes in the E# rows below (and in the worked-example Passport/build sections) are **measured-input notation** — what the toolkit prints / what you read off the screen. They are NOT the literal value you pass to ae-mcp. Convert each to `{r,g,b}` 0-1 (ae-mcp-realities §1 formula; the toolkit prints the `{r,g,b}` form for you) before any tool call, and multiply the bounding-box numbers by SCALE.

> **Convert measured bbox → `position` (ae-mcp-realities §2) — MANDATORY before every layer call.** The Anatomy `[x, y, w, h]` gives the bbox **top-left** `[x, y]`. ae-mcp's `position` is NOT the top-left — never pass `[x, y]` raw. `position` is always a 2-number `[x,y]` TUPLE (never `{x,y}`). Convert per element type:
> - **SHAPE** (panel, card, divider, button rect, icon box): `position = [x + w/2, y + h/2]` — the bbox **center**. Then multiply by SCALE: `position = [(x + w/2) × SCALE, (y + h/2) × SCALE]`. (Size `[w, h]` is also × SCALE, and is passed as the tuple `size: [w, h]`.)
> - **TEXT** (`ae_add_text_layer`): `position` is the text's **anchor / baseline point** (default = baseline of the first character, per §2), NOT the bbox top-left. With `justification: "left"` (LOWERCASE — the only accepted form) the anchor sits at the left edge of the text on its baseline, so `position ≈ [x × SCALE, (y + capHeight) × SCALE]` (baseline ≈ a cap-height below the bbox top). With `"center"` use `x + w/2`. Do not pass the bbox top-left `[x, y]` as the text position.
>
> SCALE applies to the converted coordinates and to `[w, h]`; colors are never scaled.

```
E1  Top bar               [0, 0, 1920, 64]      bg #1e1e1e, border-bottom #3c3c3c 1px
E2    Window controls     [20, 20, 60, 14]      3 circles ø12, gap 6, colors #ff5f57 #febc2e #28c840
E3    Tab "AE-MCP"        [200, 40, 120, 28]    text 12pt SF Pro Medium #ccc, underline accent #0078d4 2px
E4    Tab "pinterest"     [340, 40, 100, 28]    text 12pt #888 (inactive)
...
```

Be granular — even a 1px border is its own layer.

### 4. Component types observed
Mark each E# with its archetype from the Anatomy Table below. This drives construction.

---

## UI Anatomy Table — component → AE construction

For each component, the row tells you (a) which `ae_*` tool, (b) the parameter pattern, (c) common effects to apply.

> **Effect names in the tables below are the friendly prose labels. Pass the `effect` key** as one of the 24 registered friendly keys OR, for anything not registered, the **raw AE match name string** (an invented camelCase key fails — `resolveMatchName` passes unknown keys through unchanged): "Drop Shadow" → `dropShadow`, "Gaussian Blur" → `gaussianBlur`, "Gradient Ramp" → `gradient` (the registered key is `gradient`, NOT `gradientRamp`), "Glow" → `glow`, "Add Grain" → `addGrain`, "Tint" → `tint`, "Curves" → `curves`, "Levels" → `levels`, "Drop Shadow" → `dropShadow`. NOT registered → pass the raw match name: "CC Vignette" → `"CC Vignette"`, "CC Composite" → `"CC Composite"`, "Bevel Alpha" → `"ADBE Bevel Alpha"`, "Turbulent Displace" → `"ADBE Turbulent Displace"`. Effect **property** strings (e.g. `"Glow Threshold"`, `"Shadow Color"`, `"Distance"`) are real AE strings passed in the free-form `properties` object; the MCP does not validate them, so verify on a live comp. Drop Shadow's `"Opacity"` is on the **0-255** scale, not 0-100 — pass ~40 for ~15%, ~64 for ~25% (user-confirmed; verify on a live comp). Every layer you create is referenced in later `ae_apply_effect` / `ae_set_keyframe` / `ae_apply_easy_ease` calls by the exact `name` you pass it via the `layerName` parameter (ae-mcp-realities §3), and every such call also takes `compositionName` — so name each layer uniquely as the build sequence below instructs.

### Containers / surfaces

| Component | Tool | Pattern |
|---|---|---|
| Solid panel / card / sheet | `ae_add_shape_layer` | shapeType=`rectangle`, size=`[w,h]`, position=center `[x,y]`, fillColor=bg-color `{r,g,b}`, roundness=**measured** `radius` (run the toolkit per surface; the 8/12/16/24/4/0 scale is only a sanity check, NOT a value to plug in blind) |
| Stroked card (1-2px border) | `ae_add_shape_layer` + a second thin rect | `ae_add_shape_layer` has **no stroke parameter** (only shapeType/size/fillColor/roundness/position). Fake a border with a slightly larger filled rect of the border color placed behind, or a same-size precomp with a stroke effect. **Do NOT pass `stroke`/`strokeWidth` — they don't exist.** |
| Floating card with shadow | `ae_add_shape_layer` + `ae_apply_effect` Drop Shadow (`dropShadow`) | Shadow Color `{r:0,g:0,b:0}` (#000), Distance 8, Softness 24 — modern shadow. **`"Opacity"` is 0-255, so 15-25% = pass ~40-64, NOT 15-25 (user-confirmed; verify live).** |
| Glassmorphic | `ae_add_shape_layer` + `ae_apply_effect` Gaussian Blur (`gaussianBlur`) on a duplicated BG | Card opacity 60-80%, white fake-border via a behind rect (`{r:1,g:1,b:1}` — no stroke param), blur of underlying BG |
| Gradient header | `ae_add_shape_layer` rect + `ae_apply_effect` `gradient` | `"Ramp Shape": 1` (linear), top→bottom (`"Start of Ramp"` / `"End of Ramp"`), 2 stops from palette (`"Start Color"` / `"End Color"`) |
| Inset / sunken field | `ae_add_shape_layer` + `dropShadow` with the negative-distance trick (or raw `"CC Composite"`, or an inverted raw `"ADBE Bevel Alpha"`) | |
| Divider / 1px line | `ae_add_shape_layer` shapeType=`rectangle` size=`[w,1]` | Or `ae_add_solid_layer` 1px tall |

### Text elements

> **Tool note:** there is **no `add_text_layer_advanced`** — use `ae_add_text_layer` (params: `compositionName, name, text, fontFamily, fontSize, fillColor`(`{r,g,b}`)`, position`(`[x,y]`)`, justification`(LOWERCASE `"left"|"center"|"right"`)). It has **no tracking, no leading, and no stroke** params — express those design intents in your measurement notes, but do NOT pass them as arguments. For an underline/stroke look, add a separate thin rect or a `stroke` effect on a precomp.

| Component | Tool | Pattern |
|---|---|---|
| Body text | `ae_add_text_layer` | fontFamily: SF Pro / Inter / Roboto / Segoe UI / Helvetica Neue (pick by OS look). fontSize: 12-14pt body, 16-20pt headers, 24-48pt display, 64-120pt hero. (Tracking -10 to -25 for display / 0 to +25 for caps is a design note only — no tracking param exists.) |
| Label / caption | `ae_add_text_layer` | 10-11pt, color #888-#aaa, often UPPERCASE (uppercase the `text` string yourself; +50 tracking is a note only — no param) |
| Hyperlink | `ae_add_text_layer` | Color = accent (e.g. #0078d4), optional underline via a separate thin rect (no Stroke param on text) |
| Heading hierarchy | `ae_add_text_layer` × N | H1 32-48pt bold, H2 24-32pt semibold, H3 18-20pt medium, body 14pt regular |
| Code / mono | `ae_add_text_layer` | fontFamily: SF Mono / JetBrains Mono / Fira Code / Menlo. Color: syntax-highlighted (#ce9178 strings, #569cd6 keywords, #6a9955 comments — VSCode dark) |
| Numeric ticker | `ae_add_text_layer` + expression | Mono font + counter expression (see ae-animation-principles R13) |

### Buttons

| Component | Tool | Pattern |
|---|---|---|
| Primary CTA | `ae_add_shape_layer` rect + `ae_add_text_layer` on top | Rect: roundness 6-8 (× SCALE), fillColor accent color, no stroke. Text: white, 14pt medium, `justification:"center"`. Optional `dropShadow` Shadow Color = accent, `"Opacity"` ~77 (= ~30% on the 0-255 scale) for "elevated" feel |
| Secondary outlined | shape + text | Transparent fill rect with a slightly larger behind-rect in the border color to fake the 1px outline (no stroke param), text in that border color |
| Ghost / minimal | text-only | Just text + hover state (which you simulate via alternate frame if animating) |
| Icon button | shape ellipse/rect + icon shape | Icon = shape layers (`ae_add_shape_layer` shapeType=`rectangle`/`ellipse` only — there is no path shapeType; compose icons from rects/ellipses, see Icons section) |
| Toggle / switch | shape pill (rounded rect) + shape ellipse thumb | Pill width 2.5×height via roundness=height/2, height 16-20px, ellipse ø=height-4, position animatable |

### Lists & data

| Component | Tool | Pattern |
|---|---|---|
| List row | `ae_add_shape_layer` rect (full width, ~48-56px tall) + child elements | Repeat with Y offset = row height + gap |
| Avatar | `ae_add_shape_layer` shapeType=`ellipse` | Ellipse fill (solid color) OR, for a real photo: `ae_import_image` the image (the image/video import tool — there is no `import_footage`/`add_av_layer`), place it above an ellipse shape layer, and `ae_set_track_matte { compositionName, layerName, matteLayerName, type:"alpha" }` so it reads as a circular crop. |
| Progress bar | 2× `ae_add_shape_layer` rects | BG: full width pill, color #2a2a2a. FG: same shape, Scale X animated [0 → target] (or width), color accent |
| Tag / chip | shape rect + text | roundness=height/2 (pill), padding 8-12px L/R, height 24-28 |
| Tab bar | shape rect + text × N | Active tab underline = thin rect under text, color accent |

### Charts / data viz

> **Tool note:** `ae_add_shape_layer` only does `rectangle` / `ellipse` (no path, no repeater, no stroke param). For arbitrary path-based charts (line/area), build the line in a precomp via a shape layer whose path you set in AE directly, or approximate with thin rotated rects; the MCP can't author bezier vertices. Use bars (rects) wherever you can.

| Component | Tool | Pattern |
|---|---|---|
| Line chart | precomp / manual path (MCP can't author path vertices) | Approximate with thin rotated `rectangle` segments [[x1,y1]→[x2,y2]] in accent, width=2-3. Optional: animate Trim Paths End 0%→100% by hand in AE over 1-2s |
| Bar chart | `ae_add_shape_layer` rect × N | Stagger animate Scale Y `[0,0]`→`[100,100]`-style (Scale tuple) with 4-frame offset per bar |
| Area chart | shape rect/precomp with fill + `gradient` effect | Same as line + fill with linear `gradient` (top accent → bottom transparent) |
| Pie / donut | `ae_add_shape_layer` shapeType=`ellipse` | No stroke param — build the ring as two stacked ellipses (outer accent, inner bg) or as a precomp with a `stroke` effect; "fill" arc segments by hand in AE |
| Pixel grid / heatmap | `ae_add_shape_layer` rect × N | No repeater tool — duplicate a rect `[w,h]` in a Rows × Columns grid (each its own layer or a duplicated precomp), per-cell color via fillColor |

### Icons — RECOGNIZE, never trace from the raster

**Do NOT try to trace icon vertices off a small bitmap — that always produces garbage.** Vision can't read a 16–24px glyph's exact path, but it CAN name what the icon *is*. So the rule is:

1. `crop --zoom 8` the icon region and Read it — identify it semantically ("magnifier / search", "hamburger", "heart", "chevron-right", "gear", "play", "bell", "user", "plus").
2. Note its bounding box (px), stroke vs filled, stroke width (measure on the zoomed crop), and color (`pixel`/`swatch`).
3. Reconstruct from the canonical recipe below — a clean primitive composition, NOT a hand-traced path. A crisp recognizable icon beats a "pixel-accurate" blob every time.

> **Primitive note:** `ae_add_shape_layer` exposes only `rectangle` and `ellipse` (no polystar/polygon/star, no path, no stroke param). The "strokes / paths / polystar / triangle" recipes below describe the *target shape*; build each from thin rotated `rectangle`s (for line strokes), `ellipse`s, and rounded rects, or author a precomp path by hand in AE. Match measured line width with the rect's short side and set color via fillColor.

| Icon | Canonical AE construction (centered [0,0], 24×24 box, scale to measured size) |
|---|---|
| close | Two thin rects (rotated ±45°) [-8,-8]→[8,8] and [-8,8]→[8,-8], rounded ends |
| check | Two thin rects forming [-8,0]→[-3,5]→[8,-6], rounded ends |
| play | Filled triangle [-6,-8],[-6,8],[8,0] (rotated rect/precomp — no triangle primitive) |
| pause | Two rounded rects [3,16] at x=−5 and x=+5 |
| + plus / add | Two thin rects [0,-9]→[0,9] and [-9,0]→[9,0] |
| hamburger | 3 thin rects [-9,-6]→[9,-6], [-9,0]→[9,0], [-9,6]→[9,6] |
| gear/settings | No polystar — approximate with a ring of small rects around a central ellipse + ellipse hole ø7 (or import a gear glyph) |
| home | Rect [0,2,16,12] + roof triangle [-10,0],[0,-9],[10,0] (rotated rects/precomp) |
| search | Ellipse ø11 (ring: two stacked ellipses) at [-2,-2] + thin rect [4,4]→[9,9] |
| heart | Two ellipses ø11 at [-5,-3] & [5,-3] + triangle to [0,10] (rotated rects/precomp) |
| bell | Rounded-top rect/arc body + small ellipse clapper below |
| user | Ellipse head ø9 at [0,-5] + arc/half-ellipse shoulders below |
| › chevron | Two thin rects [-3,-6]→[4,0]→[-3,6], rounded ends (rotate for ‹ ∧ ∨) |
| ↗ arrow | Thin-rect shaft + 2 short head rects; rotate to direction |
| ⊕ / brand logo | If it's a real brand/product logo, do NOT redraw — `crop` it to a file, then bring that crop in with `ae_import_image { compositionName, path/url }` (the image/video import tool — there is no `import_footage`) and place the resulting layer; or substitute the closest text glyph. Position the imported layer by its CENTER like any other layer (ae-mcp-realities §2). |

For anything not in this table: compose from the available primitives (ellipse / rect / rounded rect) that read as the recognized icon. Match measured line width and color. Multiple primitives across stacked shape layers (or one precomp) is fine.

### Effects per archetype

| UI archetype | Mandatory effects on top adj |
|---|---|
| **macOS app window** | Drop Shadow (`dropShadow`, large/soft): Color `{r:0,g:0,b:0}` (#000), Distance 0, Softness 60, `"Opacity"` ~77 (= ~30% on the 0-255 scale; user-confirmed, verify live). Title bar gradient ramp (`gradient`) top→bottom dark. |
| **Modern web app** | No vignette. Subtle Drop Shadow on cards. Clean type. |
| **Dashboard / SaaS** | Optional `curves` slight blacks-lift (direct curve points are awkward via MCP — prefer `levels` `"Output Black"` for a blacks-lift). Slight `addGrain` (`"Intensity": 0.2`) for premium feel. |
| **Sci-fi / HUD** | `glow` on all text and lines (`"Glow Threshold": 70`, `"Glow Radius": 15`, `"Glow Intensity": 1.2`). Scanlines via duplicated thin rects (no repeater tool). raw `"CC Vignette"` `"Amount": -20`. Color cast via `tint` (`"Map Black To"` / `"Map White To"`) to a single hue. |
| **Terminal / code editor** | Mono font. Syntax color text layers. Subtle `glow` on text. Optional CRT effect via raw `"ADBE Turbulent Displace"` (very low `"Amount": 2`). |
| **Mobile app screen** | Status bar (time/battery/wifi) at top 44px on iOS, 24px on Android. Round-corner mask if showing whole phone (corner radius 50-60). |
| **Game UI** | `glow` heavy. `dropShadow` heavy. raw `"ADBE Bevel Alpha"` on buttons. |

---

## Build sequence for a UI ref

After passport (visual-matcher) + measurement (this skill) are written:

1. `ae_list_compositions` (or `ae_get_composition_info { compositionName }`) to orient — there is **no** `get_project_info` tool.
2. `ae_create_composition { name, width, height, frameRate, duration }` with width/height/aspect matching the UI (mobile = 1080x1920 portrait, web = 1920x1080, app = 1440x900 etc.). All later calls reference it by `compositionName` (the name you pass here — there is no compId).
3. **Build bottom-up by Z-order**, not in arbitrary order (every call below takes `compositionName`):
   - BG color solid (`ae_add_solid_layer`) — the canvas/background of the UI
   - Surfaces (panels, sidebars, headers) — each its own `ae_add_shape_layer`, NAMED clearly: `header-bar`, `sidebar`, `main-card-1`
   - Strokes / dividers (1px lines) as thin rects
   - Content text layers (`ae_add_text_layer`) — match font, size, weight, color exactly
   - Buttons (rect + text pair, group into a precomp via `ae_precompose_layers` if reused)
   - Icons (shape layers composed from rects/ellipses)
   - Effects per archetype (`ae_apply_effect`, see table)
4. **Use precomps for repeating components** (`ae_precompose_layers { compositionName, layerNames }`): a list row → make 1 row as a precomp, then `ae_duplicate_composition` / duplicate-and-shift Y for the rest. Faster + editable.
5. **Name layers semantically**: never leave default names like "Shape Layer 1". Rename via `ae_modify_layer { ..., newName }` to `card-revenue-bg`, `card-revenue-title`, `card-revenue-value`.
6. **Final touch**: top adjustment layer (`ae_add_adjustment_layer`) with `ae_apply_effect` per archetype (see table above).
7. There is **no `save_project` tool** — do NOT call one. Saving is done by the user in the AE UI; preview a frame if needed with `ae_export_frame { compositionName }`.

---

## Animation patterns specific to UI

When the user wants the UI to feel "alive":

> **Easing note:** "easeOut" / "easeInOut" below describe the *feel*. There is **no `easeType`** param. Apply a uniform ease to all keys of a property with `ae_apply_easy_ease { compositionName, layerName, propertyName, influence }` (0-100) — **but `ae_apply_easy_ease` ERRORS on 2D `Position` (ae-mcp-realities §6), so use it only on scalar `Opacity`/`Rotation`.** For `Position`/`Scale`, or for a directional ease (ease-OUT = high `influenceOut`, low `influenceIn`), use `ae_set_temporal_ease { compositionName, layerName, propertyName, speedIn, influenceIn, speedOut, influenceOut }` or `ae_set_keyframe_advanced` (key + bezier in one call). `propertyName` is the Capitalized enum (`Position`/`Scale`/`Rotation`/`Opacity`/`Anchor Point`).

| Element | Animation (use ae-animation-principles recipes) |
|---|---|
| Card entrance | R1 Fade-Up (Opacity 0→100 + Y +30→0 over 12f, easeOut) — stagger 4f per card |
| Counter / stat | R13 Counter — a "Source Text" counter is author-in-AE, NOT MCP-settable. MCP-compatible options: the effect-based `numberEffect` (ADBE Numbers2, with its own value/keyframe setup), or `ae_create_text_animator` for a per-character reveal. See ae-animation-principles R13 |
| Progress bar | Scale X from 0 to target over 24f, easeOut |
| Line chart draw | Trim Paths End [0→100%] over 30-45f, easeInOut |
| Bar chart bars | Stagger Scale Y from 0→1, 4f offset per bar |
| Cursor blink | Opacity expression `(time * 2) % 1 < 0.5 ? 100 : 0` (see R4) |
| Click feedback | On a button: Scale [100→95→100] over 6f with hard cut + flash white solid |
| Modal entrance | Backdrop Opacity 0→60 over 8f + modal Scale 92→100% + Opacity 0→100 over 12f, easeOut |
| Toast / notification | Slide-In R3 from top, hold 90f, slide-out R3 reversed |
| Tab switch | Underline shape Position X animated to new tab center over 12f, easeInOut. Crossfade tab contents over 8f. |

---

## Close the loop — measure → build → AUDIT → fix (don't ship on vibes)

A rebuild is "done" only when it MEASURES close to the reference, not when it looks close. After the build, run the deterministic gate and iterate:

1. **Measure → Build.** Construct from measured values (§0) — never eyeballed.
2. **Audit.** `ae_audit_frame(compositionName, reference_url|reference_key)` renders the comp's frame and compares it to the reference cell-by-cell in CIE-Lab. It returns `ok` (the gate: `flaggedPct ≤ 5%` AND `meanDE ≤ 8`), `worstCells` (the worst-mismatching regions, located in RENDER pixels, ref vs render colour), and `scanlines` / `stripeCountMismatch` (exact stripe positions/widths when the reference has repeating geometry — rings, bars, grids).
3. **Bounds check (`sourceRectAtTime`).** Don't trust the `[w,h]` you typed — read what each built layer ACTUALLY renders: `sourceRectAtTime(t, includeExtents=true)` → `{left, top, width, height}`. Compare that measured `width`/`height` against the reference bbox (× SCALE) for every panel, card, and text block. A title whose `sourceRectAtTime().width` overruns its card means the font/size/copy is wrong, not the card. Fix the source measurement, not the container. This catches sizing drift that `ae_audit_frame`'s colour gate can miss when the fill is correct but the geometry isn't.
4. **Vision pass (the half the audit can't see).** Also VIEW the returned `renderUrl` yourself: the audit scores colour/region drift but is blind to layout sense, copy, alignment, and spacing rhythm. Catch those by eye.
5. **Fix the specifics, not everything.** For each `worstCell`, the colour pair tells you what's off (wrong fill, missing element, mis-placed layer) and the box tells you WHERE — go fix that layer (re-`swatch`/`radius`/`fontsize` the reference region if you mis-measured). For a `stripeCountMismatch`, copy the reference stripe centres/widths/COUNT numerically — don't re-eyeball spacing.
6. **Re-audit.** Repeat until `ok` is true AND the vision pass is clean. If `meanDE` stops dropping across two passes, you're fighting the wrong thing — re-measure the region instead of nudging.


---

## Don'ts

- Don't paste a screenshot as footage and call it done — the user wants it rebuilt, not imported.
- Don't generate a label/badge/chip/stat-pill/plate as one image — even small ones with a gradient or glow. Build the surface as a shape (+ Gradient Ramp/shadow) and put its text in a SEPARATE editable text layer; a generated plate bakes its label into the picture (the "labelled plate came back flat" bug).
- Don't use Generic "Arial" font — match the OS/brand: SF Pro (macOS/iOS), Roboto (Android), Inter (modern web), Segoe UI (Windows). Identify the family by letterforms on a zoomed `crop`, and set the kegl from `fontsize`, not by eye.
- Don't trace icons off the bitmap — `crop --zoom`, recognize the icon, rebuild from the canonical recipe.
- Don't eyeball colors or radii — `swatch`/`pixel`/`radius`/`gradient` give real values; paste them.
- Don't skip the 1px borders and dividers — they're 80% of what makes UI feel real.
- Don't use perfectly clean rectangles for "premium" UI — add Drop Shadow (subtle: 0/8/24, ~15-25% → pass `"Opacity"` ~40-64 on the 0-255 scale, NOT 15-25).
- Don't forget rounded corners — modern UI is rarely 0-radius. Measure each with `radius`; only fall back to 8px web / 12-16px mobile if a corner genuinely can't be measured.
- Don't apply Glow to a "clean SaaS" UI — Glow belongs on HUD/gaming/sci-fi only.
- Don't animate every UI element on entrance — pick 2-3 hero animations max, rest just appear.
- Don't forget to name layers semantically.
