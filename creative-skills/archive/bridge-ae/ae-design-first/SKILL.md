---
name: ae-design-first
description: Optional one-call authoring routes that replace a native build for a single frame — a whole layout written as one HTML document and built through ae_build_scene_from_html, and a whole animated vector scene written as one Lottie JSON and built through ae_build_scene_from_lottie. Both land as editable AE layers. Neither is required: the native atomic build produces the same layers with no authoring detour.
---

# AE Design-First (HTML -> scene)

Build an entire frame in **one call** from an HTML mock, instead of placing
layers one at a time. **This pipeline is optional.** The native atomic `ae_*`
build is the default path and produces the same editable layers without HTML;
choose this one only when a single HTML doc is genuinely the faster way to
reach that frame. Put everything
expressible into the HTML (layout, plates, gradients, and the REAL text — it
lands as editable AE text layers); keep atomic calls for the surgical pass
after: text restyle (`ae_style_text`), imported/generated imagery, elements
HTML can't express (e.g. text-on-path), and motion.
You author a self-contained HTML page sized to the comp;
the Higgsfield panel renders it in a hidden Chromium iframe, walks the DOM into
a layer spec, applies animation from your free-text intent, and builds a NEW
composition of **editable AE layers** (rects -> shape layers with rounded
corners, text -> text layers, svg `<path>` -> shape layers) plus keyframes and
a BG solid.

> **Prerequisite:** this pipeline is its own path — it does NOT use the atomic
> `ae_*` tools to build. But if you afterwards do surgical edits
> on the built comp, hold the value contract: colors `{r,g,b}` 0-1,
> `[x,y]` tuples, position = layer CENTER, case-sensitive effect keys.
>
> **Companion skill:** `ae-clean-rig` carries the construction, editability and
> motion-fidelity rules for the native build, which owns the default path.

---

## The two tools

**`ae_html_to_spec(html, compW=1920, compH=1080, usePrecomps?=true)` — INSPECT ONLY.**
Renders the HTML and returns `spec.json` **without touching the project** (Phase
2 only, non-destructive):
```
{ comp: { width, height, bg: {r,g,b}  // 0-1 },
  layers: [ rect | text | svgPath | group ] }   // colors {r,g,b,a} 0-1; positions comp-space top-left px
```
Use it to debug what the DOM walk extracted — confirm the layer count and
positions — before you commit a build.

**`ae_build_scene_from_html(html, compW=1920, compH=1080, userText?, duration?, usePrecomps?=true)` — FULL pipeline.**
Render -> walk to spec -> apply animation (intent parsed from `userText`) ->
generate self-contained ExtendScript -> run it -> build a new comp
(`Vibecode_<ts>`; finalize it with `ae_finalize_build` to rename `hf_<ts>`). `duration`
is in **seconds** (default 8) and auto-extends to fit the animation.

### Precompose semantic groups (`usePrecomps`) — ON by default

**`usePrecomps` now defaults to TRUE in the connector**, so the DOM walk groups each
semantic container (a card + its children) into its **own precomp** automatically —
you do NOT need to pass it. Why it matters: a precomp is editable and animatable as ONE
unit — fade/scale/move/restyle the whole card by touching the precomp, apply one
grade/effect to a group, and duplicate a card by duplicating its precomp. A flat stack
would force you to nudge every child layer by hand. If a build comes back as a flat
stack, you're on an old deploy or someone passed `usePrecomps:false` — re-check.

- **HOUSE RULE — any 2+ layer unit MUST end up precomposed** (bg + text = already a unit).
  The only things left flat are genuinely standalone single layers (a lone background,
  a lone heading). Auto or manual — but it must happen.
- **Drive the auto-grouping from your HTML class names.** The walker only groups
  containers whose class/id contains one of these hints — so NAME your containers with
  them and the 2+ rule enforces itself with zero extra calls:
  `terminal, code-window, code-editor, code-block, code-card, editor, card, panel,
  surface, tile, feature-card, pricing-card, stat-card, header, top-bar, topbar, nav,
  navbar, sidebar, footer, hero, section, banner, callout, modal, dropdown, menu, popup,
  tooltip, list-item, row, item, window, pane, frame, browser, cta, announce, notice,
  alert, widget, module, block`.
  A `<div class="price-cta">` groups; a `<div class="wrapper">` does NOT — pick hint-bearing
  names for every semantic unit. (Also needs: ≥100×32 px, not near-full-frame, ≥2 child layers.)
- **Opt out** only for a deliberately flat single-element frame: pass `usePrecomps:false`.
- **If the auto-grouping missed a unit** (non-hint class, too small), or you need to
  (re)group AFTER the build, do it explicitly with `ae_precompose_layers({ compositionName,
  layerNames: [...the card's layers], name: "card-revenue", moveAttributes: true })` —
  a 2-layer pill/badge is NOT too small to bother.
  One precomp per semantic container; name each precomp clearly (`card-revenue`,
  `nav-bar`, `chart-panel`).
- **Order:** build + verify the layers first, THEN precompose, THEN add group-level
  motion (the `data-anim` entrances still apply; precomps let you animate the whole
  group, not just leaves).

---

## When this pipeline is the right choice

- **Consider `ae_build_scene_from_html`** for a whole layout/scene whose full
  structure is faster to write once as HTML/CSS than to place natively — title
  cards, lower-thirds, infographics, dashboards, stat cards, hero frames.
- **The atomic `ae_*` tools** (`ae_create_composition`, `ae_add_shape_layer`,
  `ae_add_text_layer`, `ae_set_keyframe`, `ae_create_text_animator`, ...) are the
  default builder, and the only path for surgical edits to an EXISTING comp.
- **Commit to one path per frame.** Do not hand-re-assemble with atomic tools
  what this pipeline already produced in one call. If `build_scene` fails,
  either fix the pipeline (most often: restart After Effects so the plugin
  reloads its jsx) or build that frame natively — do not interleave the two.

---

## Reference intake — ALWAYS measure with vision_analyze first

**If the request carries a visual reference (an image URL/attachment or a
website), you MUST run `vision_analyze` on it BEFORE authoring the HTML.**
Eyeballed colors, radii, and positions are the #1 cause of "looks off"
results — measure, don't guess.

- **Image reference:** call `vision_analyze` with ONE image and ask for:
  every element's bounding box **as FRACTIONS (0..1) of the image** (vision is
  unreliable at absolute pixels, solid at fractions), exact **hex colors**
  (background, card fill, accents, text tiers — sampled, not named by eye),
  corner radii as fractions of width, font-size tiers as fractions of height,
  and an element inventory (icons named semantically: pencil / briefcase /
  ticket...). Multiply fractions by the comp size to get px for the HTML.
- **Website reference:** screenshot it first (browser tool), then run the
  same `vision_analyze` measurement on the screenshot.
- One image per call — arrays double-stringify and fail (see the
  vision_analyze note below). For a compare, composite first.
- **Sample exact values when reachable:** `vision_analyze` is great for layout
  and an inventory, but for EXACT colours / corner radii / font sizes call
  `ae_measure_reference(url|key, ops:[…])` — it reads the actual pixels
  (returns `rgb:{r,g,b}` 0-1 ready for AE) when the reference is reachable as a
  URL/R2 key. Eyeballed/named values are the #1 cause of "looks off".
- **Close the loop after the build (numbers, then eyes):** when a reference
  exists, run `ae_audit_frame(compositionName, reference_url|reference_key)` —
  it renders the settled frame and scores it against the reference cell-by-cell
  in CIE-Lab. `ok` is the deterministic gate (`flaggedPct ≤ 5%` & `meanDE ≤ 8`);
  `worstCells` localise the drift (render px + ref/render colour) and
  `scanlines`/`stripeCountMismatch` give exact repeating-geometry numbers. THEN
  also view `renderUrl` (or `vision_analyze` a side-by-side) for the semantic
  half — layout/copy/spacing the audit can't see. Fix the HTML and rebuild
  until the gate passes AND a designer wouldn't flag it.

---

## Figma / SVG reference -> faithful AE vectors

Inline `<svg>` in the HTML is the default path (the DOM walk maps `<path>` to
bezier shape layers). But when the reference is **vector artwork exported from
Figma** — logos, illustrated marks, complex glyphs — validate the SVG first; AE
and the walk choke on Figma's raw export.

**Validate the SVG BEFORE import (three blockers):**
- **Flatten boolean ops.** AE cannot read SVG boolean operations (union /
  subtract / intersect / exclude). Flatten every boolean group into a single
  resolved `<path>` in Figma before exporting, or the shape comes through empty.
- **No masks / clip-paths.** Strip `<mask>` and `clipPath` — bake the clip into
  the path geometry instead (AE mask coords are layer-space, see the gotcha below).
- **Flat hierarchy.** Collapse nested `<g>` groups; a deep group tree maps to
  garbled or dropped layers.

**Reference-design workflow (preserve hierarchy through Illustrator):** when you
need the layer structure intact (named groups -> AE layers), don't import the
SVG into AE directly:
1. Export the SVG from Figma (after the flatten/no-mask/flat-hierarchy pass).
2. Open it in **Illustrator** and save as `.ai` — Illustrator preserves the
   layer hierarchy that AE's SVG importer would flatten or rasterize.
3. Import the `.ai` into AE as a **composition** with **"Retain Layer Sizes"** —
   each Illustrator layer lands as its own editable AE layer at its true bounds.

**Post-import validation (catch rasterization drift):** after import, measure the
imported layer bounds against the original and flag drift:
- Compare imported bounds vs the source artwork bounds (px). A mismatch means the
  importer rasterized instead of keeping vectors.
- Confirm fidelity by **edge-pixel sampling** — render the imported frame and run
  `ae_audit_frame(compositionName, reference_url|reference_key)`; soft/fuzzy edge
  cells in `worstCells` (high `meanDE` on contour pixels) signal rasterization.
  True vectors give crisp edges; raster import bleeds. If it rasterized, redo the
  Illustrator `.ai` step (or convert the boolean-flattened path to inline `<svg>`
  in the HTML so the walk re-vectorizes it).

---

## Author-the-whole-frame mandate (applies once this pipeline owns the frame)

**`design.html` IS the complete frame.** Everything visible must be expressed in
the HTML — never built afterward with atomic tools. The pipeline maps each
construct to an editable AE layer:

| You want | Author it as | Why (pipeline behaviour) |
|---|---|---|
| **Icon / glyph** | **Lucide** inline `<svg>` (see below) | the walk maps `path`/`stroke`/`fill` (incl. arcs) to smooth bezier shape layers — **NEVER invent icon paths or hand-build a glyph from `rect`/`ellipse` primitives** |
| **Raster / photo / logo PNG** | `<img src>` | the pipeline imports the image as a footage layer |
| **Soft glow / bloom** | a `<div>` with `mix-blend-mode:screen` | renders as a screen-blended layer (no post effect needed) |
| **Texture (dot-grid, hatch)** | inline SVG `<pattern>` | becomes a tiled shape/footage layer |

**After a SUCCESSFUL build you may ONLY tweak EXISTING layers** (nudge position,
restyle, retime). **NEVER** `ae_add_shape_layer` / `ae_set_keyframe` / recolor-
via-effect something the HTML could have expressed — if it's wrong, fix the HTML
and rebuild. The HTML is the single source of truth for the frame.

### Icons = Lucide (https://lucide.dev — 1500+ icons, ISC)

**Use the Lucide icon set — by name, with its real path data.** Never invent
icon geometry. Write each icon as inline SVG in the canonical Lucide format and
it comes through as smooth, stroked **bezier shape layers** (editable +
animatable; recolor later via `ae_set_shape_fill` stroke/fill):

```html
<svg width="24" height="24" viewBox="0 0 24 24" fill="none"
  stroke="#3fae6b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <!-- icon paths here -->
</svg>
```

Set `stroke` to an EXPLICIT color (not `currentColor`); size/position via
`width`/`height` + absolute positioning. Real Lucide path data (v1.17.0) for
common icons — paste the inner elements into the wrapper above:

```html
<!-- pencil (edit) -->
<path d="M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z"/>
<path d="m15 5 4 4"/>

<!-- briefcase -->
<path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
<rect width="20" height="14" x="2" y="6" rx="2"/>

<!-- ticket -->
<path d="M2 9a3 3 0 0 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 0 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/>
<path d="M13 5v2"/><path d="M13 17v2"/><path d="M13 11v2"/>

<!-- arrow-right -->
<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>

<!-- check -->
<path d="M20 6 9 17l-5-5"/>

<!-- x (close) -->
<path d="M18 6 6 18"/><path d="m6 6 12 12"/>
```

**Raster fallback** — for any Lucide icon whose exact path data you don't know,
reference it by name and let the pipeline rasterize it into an image layer:

```html
<img src="https://unpkg.com/lucide-static@latest/icons/settings.svg" width="24" height="24">
```

Inline SVG is preferred (editable vector layers); the `<img>` fallback is safe
(the bridge downloads + rasterizes SVG to PNG — AE can't import SVG directly)
but yields a raster layer you can't restroke. Pick names from the Lucide set:
pencil, briefcase, ticket, arrow-right, check, x, settings, user, search,
bell, home, heart, play, pause, plus, menu, chevron-right…

---

## `data-anim` contract (author entrances in HTML, never hand-keyframe)

**Every element's entrance is authored as HTML attributes** — the plugin reads
them during the DOM walk and emits the matching keyframes. **Animate via attrs;
never hand-keyframe after the build.** This is the contract the plugin reads, so
treat it as the authoring spec:

| Attribute | Values | What it does |
|---|---|---|
| `data-anim` | `fadeUp` \| `fadeIn` \| `slideIn` \| `scaleIn` \| `chipBounce` \| `count` | the entrance verb for this element |
| `data-anim-delay` | `<seconds>` (e.g. `0.4`) or `stagger` | when it starts; `stagger` defers to the parent's sequence |
| `data-anim-dur` | `<seconds>` (e.g. `0.6`) | entrance duration |
| `data-anim-stagger` | `0.06` (seconds) | put on a **parent** to sequence its children one after another |

```html
<!-- card fades up, then its rows stagger in 60ms apart -->
<div data-anim="fadeUp" data-anim-delay="0.2" data-anim-dur="0.6"
     style="position:absolute;left:760px;top:380px;width:400px">
  <div data-anim-stagger="0.06">
    <div data-anim="slideIn" data-anim-delay="stagger">Row one</div>
    <div data-anim="slideIn" data-anim-delay="stagger">Row two</div>
    <div data-anim="slideIn" data-anim-delay="stagger">Row three</div>
  </div>
  <!-- counts 0 -> the text's numeric value -->
  <div data-anim="count" data-anim-dur="1.2"
       style="font:700 120px Inter;color:#3fae6b">128</div>
</div>
```

This is the structured complement to free-text `userText`: `userText` sets the
overall mood; `data-anim` pins each element's exact entrance. Prefer attributes
when you need per-element control.

### Figma Motion duration tokens -> `data-anim-dur`

Figma's 2026 native **Motion** export ships **duration tokens** — read them off
the reference instead of guessing entrance lengths. Map straight to `data-anim-dur`
(seconds) and, on surgical retimes, to the `ae_set_keyframes` key times:

| Figma token | Value | `data-anim-dur` |
|---|---|---|
| `duration/fast` | 150ms | `0.15` |
| `duration/base` | 250ms | `0.25` |
| `duration/slow` | 400ms | `0.4` |

Use `fast` for chips/icons, `base` for cards/rows, `slow` for hero/headline
reveals. When you instead retime an existing layer with `ae_set_keyframes`, set
the out-key time = entrance start + token seconds (e.g. base = start + 0.25s);
keep the house settle ease (in22/out75).

---

## Batch-then-render cadence

Tight loop to keep renders cheap and avoid blind tweaking:

1. **Batch by category.** Apply ALL edits of one category first (all positions,
   then all colors, then all timings) — don't interleave categories.
2. **Verify a batch with ONE contact sheet.** One
   `ae_export_contact_sheet` at `maxWidth <= 768` to eyeball a whole batch — not
   one render per layer.
3. **Cap previews.** `<= 5` preview renders per rebuild. If you need more, the
   HTML is wrong — fix it and rebuild.
4. **Full-res only the final frame.** Everything before final approval stays at
   preview resolution.
5. **ALWAYS render at a NON-ZERO time.** `t=0` is pre-entrance / empty —
   elements haven't animated in yet. Render at e.g. `t = duration * 0.6` (after
   all entrances have settled) or you'll "see nothing" and chase a phantom bug.

---

## HTML authoring conventions

- **One self-contained `<html>` page sized EXACTLY to the comp** (e.g.
  1920x1080), and **pass matching `compW`/`compH`**. Put the size on `<body>`:
  `<body style="margin:0;width:1920px;height:1080px;background:#0b0b0f">`.
  **If the body has no explicit height the walk sizes the comp to the CONTENT
  bounding box** — a `position:relative` wrapper with no body height collapses the
  comp (observed: **1920×544** instead of 1080). Always set body width+height AND
  pass `compW`/`compH`. Author the frame as you'd mock it in a browser.
- **Absolute positioning, explicit px** `left`/`top`/`width`/`height`. Avoid
  layouts that depend on runtime JS — the walk reads computed layout after
  `fonts.ready`.
- **Background:** set it on `<body>` to colour the comp bg (this also pins the
  comp size — see above). Otherwise the comp bg defaults to black and a full-frame
  stage rect carries the colour.
- **Verified (A/B test, 2026-06-27):** for mappable CSS the builder produces real
  EDITABLE layers — 2-stop gradient → Gradient Ramp, `box-shadow` → Drop Shadow,
  text → editable Text layers (NOT a baked PNG). It only rasterizes the
  un-mappable parts (3+-stop/mesh gradients, `filter`, images) — exactly the
  DRAW-vs-GENERATE line below. So this IS the default builder for mappable
  layouts; reserve the granular `ae_*` tools for surgical edits.
- **Fonts:** Web fonts are fine — the panel waits for `fonts.ready`.
- **Supported + mapped CSS/SVG:**
  | CSS / element | Becomes in AE |
  |---|---|
  | solid fill | shape/text fill |
  | linear / radial gradient | Gradient Ramp effect — **2 stops only** (see Gradients note below) |
  | `border-radius` | rounded shape corners |
  | `box-shadow` | Drop Shadow effect |
  | `filter: blur()` | Gaussian Blur effect |
  | `letter-spacing` | tracking |
  | font weight / size / color | text layer props |
  | SVG `<path>` | shape layer |
  | plain text | text layer |

> **Gradients — BUILD them natively with `ae_apply_gradient`; GENERATE only truly painterly art.** Apply EVERY gradient with **`ae_apply_gradient`** (reliable native Gradient Ramp for 2 stops / 4-Color for 3–4, from **measured** stops, with colour read-back — call it BY NAME even if it's not in your visible tool list). Decide per gradient:
> - **2-stop, 3–4-stop, radial, or 4-corner blend** → **BUILD it natively** with `ae_apply_gradient`. This is virtually every card / plate / pill / background gradient. Do NOT generate it, do NOT "stack 2–3 Ramp solids", and do NOT bake a PNG.
> - **ONLY genuinely painterly artwork** with no clean stop structure — mesh / conic / organic-textured / illustrative (a *rendered* surface, not a colour ramp) — generate-and-cut as a raster `<img>`. That's the single case where generation beats building.
>
> **Do NOT bake a plate/card gradient as a PNG — and do NOT pre-bake it "to rebuild natively later" (build native from the START).** Don't reach for generation when `ae_apply_gradient` would do. The connector now HAS a reliable native gradient engine (`ae_apply_gradient`, with read-back) — the old "no native multi-stop / stack Ramps / generate the rich ones" guidance is **obsolete**.

### Keep text EDITABLE — never nest it inside a rasterized container

The connector build keeps text and gradients **EDITABLE** — it does **NOT** slice or rasterize
complex containers (no html2canvas, no slicer). Every text node → an editable **Text layer**;
every gradient (2-stop, 3–4-stop, radial) → a **native** Gradient Ramp / 4-Color via
`ae_apply_gradient`; shapes → shape layers; a blur/glow → a native effect (Box Blur / Glow). The
**only** thing that becomes a flat image is an actual picture you supplied: an `<img>` tag or a
`background-image: url(...)`. **There is NO "3+-stop gradient / glow / blur container bakes"** —
that was the AE-Vibecode bundle's slicer, which **this connector does not have**.

So to keep text editable:
1. **Build the surface natively** — a shape + `ae_apply_gradient` (ANY stop count), plus border /
   shadow / blur / glow as native effects. The plate AND its text come back as editable layers
   (grouped into the precomp). A rich/multi-stop/rotated gradient does NOT need splitting or baking.
2. **The one real bake risk = a GENERATED picture.** Never put editable text INSIDE an `<img>` /
   `background-image:url(...)` — it becomes part of that picture. If you genuinely need a
   photographic/painterly background, make it its OWN image element and put the text as a
   **separate sibling OVER it**, never wrapped inside it. (DRAW-vs-GENERATE: build chrome + real
   text on top; generate only the wordless graphic.)
2a. **STYLE LOCK for generated pictures:** every image generated for one build shares ONE style —
   write a single style descriptor (render style, palette, lighting, materials, background) once
   and prepend it verbatim to each generation prompt; regenerate off-style results.
   **The lock fixes palette/typography/motion tone — NOT layout:** vary each element's form,
   placement, and scale with its job in the frame; an identical plate on an identical anchor
   everywhere is uniform but dead.


So text only comes back baked if it was nested inside a GENERATED image — never from a gradient,
blur, or glow, which the connector builds natively.

3. **NO EMOJI in the HTML text — they land as no-ink text layers.** AE does not rasterize
   colour-emoji fonts: the layer builds but paints NOTHING (verified in the field — pixel probe
   shows "no ink" where the face should be). Avatars/memoji/decorative emoji must be `<img>`
   elements (e.g. DiceBear `https://api.dicebear.com/9.x/big-smile/png?seed=<name>&size=256`),
   which import as image layers. Same trap for exotic glyphs (→ ↑ ↓): keep them in a font that
   has them (ArialMT) or draw a small shape — and pixel-check the zones after render
   (see the text-layer notes above).

### Large/dense designs — pass the HTML INLINE

The connector takes the HTML as the **inline `html` string only** — there is **no
`htmlPath`/file parameter** (the AE plugin reads `input.html`; a path is silently
ignored). So always pass the full markup in `html`.

For a big frame (dashboard, multi-phone app shot, 3+ dense panels): author the
complete HTML and pass it inline in one `ae_build_scene_from_html` call. If the frame
is too large/complex to emit reliably in one shot, split the WORK, not the file —
build the main layout from HTML first, then add or refine pieces with the atomic
`ae_*` tools (`ae_add_text_layer`, `ae_add_shape_layer`, `ae_import_image`,
`ae_precompose_layers`) on the resulting comp. (`ae_html_to_spec` likewise takes inline
`html`; use it to preview the spec before committing a build.)

---

## userText animation intent

Free text describing the motion you want; it drives per-layer animation marks:

| Say this | Effect |
|---|---|
| "kinetic" / "kinetic typography" | kineticBeat on headings |
| "typewriter" / "type on" | typewriter on text |
| "count" / "counter" / numeric values | number counters |
| "reveal" / "fade up" / "appear" | fadeUp |
| "grow" / "growing bar" / "chart" | chartGrow / trimPath |
| chips / buttons | chipBounce |

`duration` (seconds) bounds the comp; it auto-extends if the animation needs
more time.

---

## Result envelope + what "healthy" looks like

`ae_build_scene_from_html` returns:
```
{ success: bool, layersCreated: int, effectsApplied: int, keyframesSet: int, errors: [] }
```
- **Healthy:** `success: true`, `errors: []`, and
  `layersCreated = 1 (BG) + N spec layers`.
- `effectsApplied: 0` is **normal** when the HTML has no gradients, shadows, or
  filters — it is not a failure.
- **`errors` non-empty = the build is NOT clean.** Even if `success: true` and a
  comp was created, per-layer failures mean some layers/keyframes are wrong.
  REPORT the errors verbatim to the user and treat the result as a partial
  failure — re-inspect with `ae_list_compositions` / `ae_export_frame` and fix
  the HTML, then rebuild. **NEVER** claim layers/keyframes were "set correctly"
  or that the comp is complete while `errors` is non-empty.

---

## Mandatory post-build passes

- **AUTO-GLOW:** the builder auto-applies Deep Glow/Glow to every "vivid accent" rect (saturated
  fill sat ≥ 0.45, alpha ≥ 0.7, size 100–700px), and the glow SHIFTS that plate's rendered colour
  away from the passport. Correct for neon scenes, WRONG for flat design. On a flat reference,
  immediately after the build sweep the saturated plates (`ae_list_effects` per flagged layer →
  `ae_remove_effect` in one `ae_batch`) and re-verify those colours against the passport.
- **Non-Latin text (CJK, hangul) can arrive MANGLED through the HTML build** — encoding issue in
  the pipeline; the native path is unaffected. After building a frame with non-Latin copy, check
  those strings on the render; if broken, delete and rebuild them with `ae_add_text_layer`.
- **Placeholder avatars/people (pairs with STYLE LOCK):** DiceBear PNG via `ae_import_image`:
  `personas` (stylised people) · `open-peeps` (illustrative, supports glasses:
  `accessoriesProbability=100`) · `bottts` (robot/NFT) · `big-smile` (emoji-style faces) —
  `https://api.dicebear.com/9.x/<style>/png?seed=<name>&size=256|512`. Unify them into the
  frame's palette with a **Tritone** duotone on the avatar layer (Highlights/Midtones/Shadows
  from the plate colours). Contract for later replacement: name layers `avatar-*`/`av-*`, keep
  the track matte — swapping the footage keeps the crop and animation.
- **Rotating/scaling unit precomps: put the ANCHOR at the unit's centre** (`ae_modify_layer`
  `anchorPoint`) right after precomposing — fan cards / tilted tiles must pivot around
  themselves, not a corner; extra choreography then lands on the precomp layer directly.

## Troubleshooting

- **"Unknown tool: execute_script"** — `execute_script` is NOT an MCP tool and
  will never appear in `tools/list`; it is the plugin's internal ExtendScript
  runner (a local `evalTS` call inside the panel). This error means that
  ExtendScript engine is **stale**. **Restart After Effects** so it reloads the
  jsx, then re-run `ae_build_scene_from_html`. Do not fall back to atomic
  assembly.
- **Architecture note:** Phase 2 (render + DOM walk) runs INSIDE the CEP panel's
  Chromium (real DOM, hidden iframe) — not in the Worker (which has no DOM).
  Phase 3 generates a self-contained ExtendScript run via the plugin's internal
  `execute_script`. A pixel-perfect PNG reference can optionally be dropped in
  hidden+locked for visual comparison.

---

## Predict-don't-probe gotchas (for the surgical tweaks after a build)

When you DO drop to atomic `ae_*` tools to tweak an existing layer, predict the
contract instead of probing it blindly — these bite on the win-path too:

- **Drop Shadow `"Opacity"` is 0-255, not 0-100.** 15% ≈ `40`, 25% ≈ `64`,
  ~75% ≈ `192`. Passing `25` for "25%" gives ~10% — far too faint.
- **`ae_apply_easy_ease` ERRORS on 2D Position.** For positional ease use
  `ae_set_keyframe_advanced` (set the key + bezier in one call). `easy_ease` only
  re-interpolates scalar props that already have keys.
- **Z-order:** new layers land at index 1 (top). Authoring **bottom-up** (background
  first in the HTML, foreground last) gets z-order right with no extra step — that's
  still preferred. But a reorder tool DOES exist: **`ae_reorder_layers`** (move a layer
  to an absolute index, or above/below another). Don't contort the build to avoid it.
- **Mask coords are LAYER-space, not comp-space.** Don't try to crop with a comp-
  space mask; **bake the crop into the asset's alpha** (export the PNG already
  cropped, or shape the `<img>`/`<div>` clip in the HTML) instead.
- **Glow on light UI clips.** On light backgrounds keep `"Glow Threshold" >= 80`
  and `"Glow Intensity" <= 0.8`, and put the glow on **its own layer** so it
  doesn't bloom the whole frame to white.

---

## Color discipline

**Measure the reference swatch — don't guess.** Real UI accents are **muted**,
not neon: HSL **S 40-65%**, **L 45-60%**. A muted green like `#3fae6b` reads
premium; pure `#00ff66` blows out and looks like a debug color. Sample the actual
pixel from the reference and author that hex in the HTML — over-saturating is the
most common reason a faithful layout still "looks cheap".

---

## vision_analyze note

**`vision_analyze` image ARRAYS double-stringify and fail** — passing
`[ref, render]` silently corrupts. Instead **composite the reference and the
render into ONE side-by-side image** and pass that single image, **once per
compare round**. One image in, one verdict out — no arrays.

---

## Don'ts

- Don't re-build with atomic `ae_*` tools what one `ae_build_scene_from_html`
  call produces.
- Don't treat `effectsApplied: 0` as a failure — it's expected with no
  gradients/shadows/filters.
- Don't chase `execute_script` in `tools/list` — it isn't there by design;
  restart AE to clear the stale-engine error.
- Don't use layouts that need runtime JS — the walk reads static computed
  layout after `fonts.ready`.
- Don't size the HTML to anything but the exact comp dimensions.
- Don't hand-build icons from `rect`/`ellipse` primitives or invent icon paths —
  use Lucide (inline SVG with real path data, or the `<img>` unpkg fallback);
  don't add layers / keyframes / recolor-effects the HTML could
  have expressed.
- Don't hand-keyframe entrances after a build — author them with `data-anim`
  attributes.
- Don't render at `t=0` (pre-entrance / empty) — render at a non-zero time.
- Don't pass image ARRAYS to `vision_analyze` — composite ref+render into one
  side-by-side image.
- Don't author neon accents — measure the reference; UI accents are muted
  (HSL S 40-65%, L 45-60%).
