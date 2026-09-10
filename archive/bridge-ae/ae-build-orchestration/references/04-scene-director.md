# AE Scene Director

Owns creative DIRECTION of a whole comp. `ae-mcp-realities (module: mcp-reference)` owns tool paths; `ae-design-first` owns layout construction.

**Prerequisite: load `ae-mcp-realities` first.** Every hex code below is a design note — convert to `{r,g,b}` 0-1 before any call.

## Routing

- **Use** when the brief describes a scene aesthetically (mood, vibe), implies camera + light + motion together, or names an aesthetic frame ("keynote", "cyberpunk", "Swiss", "Y2K", "brutalist").
- **Do NOT use** for a single low-level operation ("add a wiggle to layer 3", "opacity to 80%"). Those go straight to `ae_*` tools.
- **Defer layout** to `ae-design-first` for any frame mockable as HTML (title card, lower-third, dashboard, stat card, hero frame), then layer this skill's direction on the resulting comp.
- **Multi-plane depth** (parallax ladders, atmosphere, push-in math, px budgets) → load `ae-depth-space`.
- When the brief nearly matches a recipe below, say which one and swap parameters — do not re-derive structure.

## Chapterization gate (before directing)

- **Split into chapters** when the brief carries more than one idea (long text, feature list, multiple stats, timeline, before/after, problem→solution, walkthrough). One readable idea per chapter; each gets ONE job (hook / setup / claim / proof / contrast / payoff / CTA) and a readable hold before its seam.
- **Keep ONE beat** for a single logo lockup, one CTA, one stat card, one microinteraction, or a calm hero whose settle IS the payoff.
- Two structure modes: **repeated armature** (same layout+motion, content swaps) vs **evolving layout** (elements carry into new positions).
- Never place a paragraph at once — rewrite long text into short authored beats.

## The 7-step process

Walk in order; each step constrains the next. On a simple scene steps collapse into one pass, but every decision (intent, hierarchy, camera, light, easing, loop) must be MADE, not defaulted.

### 1. Treatment (before any tool call)

```
SCENE:     [one sentence — what the viewer sees]
MOOD:      [3 adjectives]
PALETTE:   [2-4 hex codes anchored to the mood]
DURATION:  [seconds — default 5s, 10s reels, 15s brand]
LOOP:      [yes/no — default yes for ambient scenes]
```

Default: dark background, cool palette, single hard key light. No warm tones unless the brief says warm.

### 2. Layer groups (4-7, never a flat stack)

| Group | Purpose | Typical content |
|---|---|---|
| **BG** | atmosphere, grade | solid + levels + noise + `"CC Vignette"` (raw) |
| **ENV** | environmental detail | grid, scanlines, particles, gradient sweep |
| **CONTENT** | hero element | text, logo, UI mockup, charts |
| **EFFECTS** | secondary motion | falling chars, glitch streaks, scan beams |
| **LIGHT** | bloom, glow, flares | adjustment layer + glow + `"CC Light Sweep"` (raw) |
| **CAMERA** | depth + move | Null layer parent (no camera tool exists) |
| **GRADE** | final look | adjustment layer + levels + tint + noise |

BG, CONTENT, LIGHT, GRADE are always required.

### 3. ONE dominant camera mode (never mix vocabularies)

| Mode | For | Easing |
|---|---|---|
| Slow elegant cinematic | keynote, product reveal, premium tech | ease-out ~70 (`influenceOut ≈ 70`, low `influenceIn`) |
| Hyperkinetic | brand chaos, gaming, sports | `influenceIn ≈ 30`, `influenceOut ≈ 90` |
| Motion-control roboarm | dystopian, AI-product, surveillance | near-linear, low `influenceOut` |
| Static + element motion | terminals, dashboards, UI demos | no camera moves at all |

Terminal → static. Logo reveal → slow elegant. Brand reel → slow elegant unless briefed otherwise.

### 4. Beat sheet

5s scene = 4 beats, 10s = 6, 15s = 9. Every layer's keyframes anchor to a beat; no floating animation.

```
0.0 - 0.5s  HOOK   — first element appears (cold open)
0.5 - 2.0s  BUILD  — layers stack in, camera starts move
2.0 - 3.5s  HERO   — key moment, full composition visible
3.5 - 4.5s  HOLD   — settles, ambient motion only
4.5 - 5.0s  TAIL   — silent hold for loop blend or transition out
```

### 5. Expressions over keyframes

If a value is "always moving subtly", it is an expression, not a keyframe.

| Need | Expression | MCP-settable |
|---|---|---|
| Ambient drift | `wiggle(0.5, 8)` on Position | yes |
| Camera breath | `wiggle(0.2, 3)` on Null Position | yes |
| BG parallax | fraction of camera Position | yes |
| Spinning seal / emblem ring | `time*12` on Rotation (8-15 deg/s, never reveal-and-stop) | yes |
| Loop anything keyframed | `loopOut("cycle")` | yes |
| Pulse glow threshold | effect property | NO — keyframe it |
| Typewriter / falling chars / counters | Source Text | NO — `ae_create_text_animator`, `numberEffect`, or author in AE |

**MCP expression limit (ae-mcp-realities §7): `ae_set_expression` accepts ONLY the 5 transform properties.** Anything returning a STRING or targeting an effect property is an author-in-AE note, never an `ae_set_expression` call. Effect-property motion is keyframed via `ae_set_keyframes` (its `propertyName` accepts an effect path like `"Effects.Glow.Glow Threshold"` — not introspectable, verify on a live comp).

**wiggle units:** Position in pixels (2-10), Rotation in degrees (0.5-3), Scale in percent (1-3).

### 6. Easing — never accept linear

Percentages are `ae_set_temporal_ease` influence values (0-100), not preset names. **`ae_apply_easy_ease` ERRORS on 2D `Position` (ae-mcp-realities §6)** — use it only on scalar `Opacity`/`Rotation`; ease `Position`/`Scale` with `ae_set_temporal_ease` or `ae_set_keyframe_advanced`.

- **Entrances:** `influenceOut ≈ 80`, `influenceIn ≈ 10`
- **Exits:** `influenceIn ≈ 75`, `influenceOut ≈ 10`
- **Continuous moves:** `influenceOut ≈ 30`
- **Settle / overshoot:** there is NO spring or bounce preset. Either add a Position key that overshoots then returns, or push `influenceOut ≥ 90` on the settle key. For a true spring use `ae_apply_expression_template` with `overshoot` or `bounce`.

Curve values live in `ae-animation-principles`.

### 7. Glow + grade are mandatory

**LIGHT adjustment layer** (above CONTENT): `glow` (→ ADBE Glo2) Radius 30, Threshold 70, Intensity 1.2 · `"CC Light Sweep"` (raw) for one subtle diagonal pass per loop.

**GRADE adjustment layer** (topmost): `levels` (→ ADBE Levels2) crush blacks / lift mids via `"Input Black"` / `"Gamma"` / `"Output Black"` · `tint` (→ ADBE Tint) mapping Black to a deep blue `#0a1428` or neutral `#0a0a0a` · `noise` (→ ADBE Noise) 2-3% monochromatic. `addGrain` is the film-grain-reading alternative to `noise`.

**Values that bite (stated once, apply everywhere below):** `Glow Threshold` is 0-100, NOT 0-1. `curves` exists but its curve POINTS are NOT MCP-settable — grade with `levels` or `colorBalance`. All colours stay `{r,g,b}` 0-1 objects.

## Recipe library

Match the brief to a recipe and swap parameters rather than building from scratch.

**Futuristic terminal** — 1920×1080, 30fps, 5s, BG `#000000`.
BG solid + noise 3% + `"CC Vignette"` Amount −60 (raw; it has ONLY `"Amount"`, negative = darker corners — no inner/outer params) · ENV digit-grid text at 8% opacity with a scrolling-Y expression, scanlines via `"CC Light Burst"` 2.5 (raw) · CONTENT mono title, typewriter, `#5fb3d4`; secondary log lines at 60% · EFFECTS 8-12 text layers of random ASCII, Y = `time*speed − delay`, opacity flicker via wiggle · LIGHT glow radius 25 threshold 60 tinted `#5fb3d4` · CAMERA locked · GRADE levels `"Input Black"` ~13, tint Black→`#0a1428` White→`#5fb3d4`, noise 2% · LOOP via `time` + `loopOut`.

**Logo reveal (premium keynote)** — 1920×1080, 30fps, 5s, BG `#000000`, LOOP no (hold final frame).
BG solid + `gradient` (→ ADBE Ramp) radial to `#0a0e14` · LOGO imported, Scale [0,0]→[100,100] settling at 1.2s (no elastic preset — fake overshoot per step 6), slight upward float · EFFECTS `"CC Light Sweep"` diagonal pass at 1.5s. `"CC Particle World"` is NOT registered and needs the plugin installed — verify live; stock substitutes for a particle burst: `"CC Light Burst"` (raw) radial streaks, `fractalNoise` at small Scale masked to the logo with animated Evolution, many small dot shape layers parented to the logo with staggered outward drift, or `"CC Light Rays"` · LIGHT glow radius 40 threshold 60 animating 0→max at hero · GRADE levels lift/crush, no tint, 1% noise.

**Kinetic typography** — 1080×1920, 30fps, 3s per phrase, BG `#f5edf5` or `#000000`.
TEXT one phrase, large bold sans, character-level entrance staggered 0.05s via `ae_create_text_animator` (`typewriter` / `scaleInChars` / `slideInChars`); entrance Scale [0,0]→[100,100], Opacity 0→100, Y offset 50→0, `influenceOut ≈ 85` · HIGHLIGHT shape behind one keyword, width 0→full at the hero beat · LIGHT glow on the highlighted keyword only · GRADE slight tint, mild noise · LOOP cycles the word stack.

**Neural / network map** — 1920×1080, 30fps, 8s loop, BG `#000000`.
NODES ~20 ellipse layers, randomized positions, `wiggle(0.3, 5)` on Position, glow on · EDGES thin stroked shapes or `"CC Light Rays"` (raw) pairing nodes, opacity pulsing on `sin(time*2)` (no registered "Beam" key) · DATA small labels, staggered fade · LIGHT glow on adjustment layer with animated threshold · CAMERA parent nodes to a Null, animate Null Rotation Z linear 0→360 over the loop, `wiggle(0.2, 2)` on Null Position for breath · GRADE cool tint White→`#5fb3d4`, heavy crush, 3% noise · LOOP the Null Z rotation must return to the start frame.

**HUD dashboard** — 1920×1080, 30fps, 10s loop, BG `#000814`, primary `#00d4ff`, alert `#ff4d4d`, panels `#1a2332`.
PANELS rounded rectangles — `ae_add_shape_layer` rectangle + `roundness`; there is NO stroke param, use a faint fill · GRID via `"ADBE Grid"` raw match name on a solid · BARS Scale driven by `sin(time*freq + phase)` · RADAR Rotation = `time * 60` · COUNTERS via `numberEffect`, not Source Text · LIGHT glow radius 20 · GRADE levels crush, cyan tint, noise 2%.

## Data-visualization motion

**Governing rule: every motion must ENCODE or CLARIFY the data.** If an animation doesn't make a value, trend or comparison easier to read, cut it. There is no native chart object — a bar is a Scale-Y'd rectangle, a dot is a positioned ellipse, and you compute every value→pixel mapping before the call.

| Pattern | Encodes | Mechanics | Easing |
|---|---|---|---|
| Tweening (morph) | same data, new view | reposition/rescale the SAME layers between layouts (bar→line→pie); keep element identity 1:1 | `influenceOut ≈ 70` on Position + Scale |
| Animated sorting (bar race) | rank change over time | hold bar COUNT fixed; animate Position.y (row) and Scale.x (value) with OVERLAPPING windows so bars slide past each other | near-linear, `influence ≈ 25` both sides; never snap |
| Spatial motion | geographic data | marker Position along a route on a static map, Scale-pulse on arrival | `influenceOut ≈ 30` |
| Uncertainty | forecast confidence | `wiggle(0.4, 1.5)` on band-edge Position, amplitude ∝ band width, 2-6px so it reads "unsure" not "broken" | expression-driven; no easing — the oscillation IS the encoding |
| Temporal (scatter) | trend over time | keyframe each dot from its t0 to its t1 Position; reveal in time order via staggered Opacity | `influenceOut ≈ 60`, `influenceIn ≈ 15` |

- Anchor each bar's **Anchor Point at its LEFT edge** so Scale.x grows rightward (position is the CENTRE).
- House stagger 0.05-0.08s per element, entrance 0.3-0.4s, settle-weighted ease in22/out75.
- Stagger by DATA order, not layout order — the reveal sequence carries meaning.
- Reuse the same `layerName` across morphs and sorts so the audience tracks each datum.
- Parent each label to its bar (`ae_modify_layer parentLayerName`) so name and value ride along.

## Call sequence (order is load-bearing)

```
1.  ae_create_composition       { name, width, height, frameRate, duration, backgroundColor }
2.  ae_import_image             assets, if any
3.  layers BOTTOM-UP            solid (BG) → ENV → text/shape (CONTENT) → EFFECTS
4.  ae_add_adjustment_layer     LIGHT, between CONTENT and GRADE
5.  ae_add_adjustment_layer     GRADE, always topmost
6.  ae_add_null_layer + parent  only if a camera-style move is required (no camera tool)
7.  ae_set_keyframe             layer by layer
8.  ae_set_temporal_ease        easing on every key just set
9.  ae_set_expression           transform props only
10. ae_apply_effect             glow on LIGHT; levels + tint + noise on GRADE
11. loop expressions            loopOut("cycle") or template loopCycle
12. ae_export_frame             verify the look (AE handles its own saving)
```

If a step fails, stop and report — never build on a broken layer.

## Generated assets (only if a Higgsfield MCP is connected)

Gated on the connection. Not connected → build from solids/shapes/text/effects or ask for assets; never block. When available: generate → `ae_import_image` (handles image AND video) → continue with ENV/EFFECTS/LIGHT/GRADE on top. Use whatever model the connected server actually exposes.

## Never

- Flat single-stack comps (minimum 4 layer groups).
- Naked linear easing.
- Floating animation not tied to a beat.
- Default colours — everything flows from the step-1 palette.
- Skipping GRADE.
- Continuing after a failed call.
- Mixing camera vocabularies.
- Music inside the comp — score belongs in Premiere.

## Response shape before building

```
**Scene Treatment** — description, mood, palette, camera mode, duration + loop
**Composition Blueprint** — layer groups
**Beat Sheet** — timeline beats
```

Then execute the call sequence. Report failures and ask before improvising.
