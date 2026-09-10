---
name: ae-liquid-glass
description: The Liquid Glass aesthetic as a parametric nine-layer rig of built-in effects only — glass and lens refraction, displacement ring, dual light-sweep rims, edge shine and edge darkness, frosted backdrop blur, tint and soft shadow — with exact values, single-null animation, and the packaging, background reconnection and in-AE verification that turn the rig into a component that survives being moved, duplicated and re-backgrounded.
---

# AE Liquid Glass — built-in effects only

Port of the reference recipe (no plugins) onto the ae_* surface, re-verified against the video's
on-screen panels (screen values beat narration where they differed). Reference build: **3840×2160
@25 fps, pill 755×469, Roundness 368** — all px values are 4K; **halve them for 1080p**.
Parametric: pill = W×H rounded rect (roundness ≥ H/2 = capsule).

**Target look (what "correct" is):** bright thin arcs on the TOP-LEFT and BOTTOM-RIGHT rims only;
a whisper-subtle light-gray inner rim (NOT a dark outline); background visibly BENDS in a band
along the top and bottom edges and is soft-blurred + slightly magnified (×1.1) across the
interior; a soft shadow floats below. If you see a dark rim, or the interior distorts uniformly
with no edge band — a step below went wrong (see the checklist at the end).

## THE default path: one call

**Two modes — pick by what exists:**
- **An element already exists** (navbar, button, badge, logo, TEXT — any layer with alpha) →
  `ae_build_liquid_glass({compositionName, sourceLayerName:"<that layer>"})`. Its duplicate
  becomes an alpha-clipped adjustment carrying the whole stack (no mattes, follows ANY geometry),
  the refraction rim derives from its own alpha, and a `<name> Controller` null exposes LIVE
  sliders (Refraction 50 / Frost 12 / Glass Opacity 100 / Magnify 120) — tweak look by setting
  slider values, no rebuild. `hideSource:false` keeps the original visible under the glass;
  `rimWidth` (20) sets the bend band.
- **Building the glass from scratch** over a background → pill mode below.

1. Background = ONE layer: if it's several layers (video + text + fills), `ae_precompose_layers`
   them into a single `BG` precomp first (stays live-editable inside).
2. **`ae_build_liquid_glass({compositionName, backgroundLayerName:"BG", width, height, centerX,
   centerY})`** — builds the ENTIRE rig below in one deterministic ExtendScript run: real strokes,
   layer-reference params set by index, pill-tracked refraction-map precomp, CTRL null. Call it BY
   NAME even if it's not in your visible tool list (the roster is platform-cached). Optional
   knobs: `tintColor`/`tintOpacity`, `refraction` (−60 subtle…−160 heavy), `frost` (20/40/60),
   `magnify` (105–115), `shapeType:"ellipse"`, `shadow:false`, `name` prefix for multiple glasses.
   `refractionMode:"radial"` (default) bends the background at ALL edges via two orthogonal ring
   maps — the surface-normal behavior of real glass (per published liquid-glass optics analysis:
   displacement follows the bezel normal, refraction concentrated in the rim, specular ≈ −60°);
   `"vertical"` reproduces the tutorial's top/bottom-only look.
3. **Read the returned report** — every line is a set-value read-back; any `FAILED`/`NOT FOUND`
   names the exact broken step (popup enums like sweep Shape=Smooth and Luminance are the usual
   suspects — fix that one thing via `ae_modify_effect_properties`/`ae_set_effect_expression`).
4. **`ae_export_frame` and CHECK against the target look** (above) + the checklist (below).
   Animate by keyframing ONLY the `<name> CTRL` null's Position/Scale.
5. **Finish it** — package the rig, repair the references packaging breaks, and verify the result
   in AE. See *Finish the build* below; a correct frame at the build position is not a finished
   component, and this step is not optional.

The manual recipe below is the FALLBACK (tool unavailable / partial repair) and the reference for
what the tool builds.

## Prerequisite (manual path)

The glass refracts ONE layer. If the background is several layers (video + text + fills),
`ae_precompose_layers` them into a single `BG` precomp first — it becomes the Bump Map source
and stays live-editable inside.

## The stack (top → bottom; build in this order, then reorder once)

| # | Layer | Role | Blend / matte |
|---|---|---|---|
| 1 | `RM-hole` (hidden) | choked pill — inner cutout matte for the ring | — |
| 2 | `Refraction Map` (hidden) | gray ring w/ vertical ramp — displacement source | matte: alphaInverted `RM-hole` |
| 3 | `Edge Shine` | 2× CC Light Sweep rims | **Add** |
| 4 | `ED-hole` (hidden) | choked pill — inner cutout for edge darkness | — |
| 5 | `Edge Darkness` | thin dark blurred rim | **Multiply**, matte: alphaInverted `ED-hole` |
| 6 | `Color` | optional tint | Normal, Opacity ~40% |
| 7 | `Main` (hidden) | the GUIDE pill — geometry source, never carries effects | — |
| 8 | `Effects` (adjustment) | CC Glass + CC Lens + Displacement Map + Transform + Blur | matte: alpha `Main` |
| 9 | `Shadow` | drop shadow only | Normal |
| 10 | `CTRL` (null) | move/scale the whole rig | — |
| 11 | `BG` precomp | what the glass distorts | — |

Every pill layer is `ae_add_shape_layer({shapeType:"rectangle", size:[W,H], roundness: H/2,
position:[x,y]})` at the SAME size/position as `Main` (there is no duplicate-layer tool — create
each; identical geometry is what keeps the rig aligned).

## Build steps (values = the recipe's, verified from the tutorial)

1. **Main** — white pill, then hide it (`ae_modify_layer` has no visibility param — leave it under
   the stack and matte-reference it; if a visible ghost shows, set its Opacity 0). Never put
   effects on Main: it is the geometry/matte source only.
2. **Edge Shine** — pill, fill BLACK, blend `add` (`ae_set_blending_mode`). Apply
   `CC Light Sweep` twice (`ae_apply_effect`, raw matchName):
   - Sweep A: Direction **−64°** (top-left rim), Shape **Smooth**, Width **120**,
     Sweep Intensity **0**, Edge Intensity **60**, Edge Thickness **0.8**, Light Color white.
   - Sweep B: same but Direction **+118°** (bottom-right rim).
   - Glue each Center to the guide: `ae_set_effect_expression({effectName:"CC Light Sweep",
     propName:"Center", expression:'L=thisComp.layer("Main"); L.toComp(L.anchorPoint)'})`.
     (The video pick-whips plain `Main.position` — that works there because ITS rig links, never
     parents. OUR rig parents Main to CTRL, which makes `position` layer-local — toComp is the
     parent-proof equivalent, same value in the unparented case.)
3. **Edge Darkness** — the color is **BRIGHT light-gray `#EAEAEA`** = `{r:0.92,g:0.92,b:0.92}`
   (the video overlays "*bright*" on screen; the narration's "dark tone" is wrong — at Multiply
   a light gray darkens the rim by only ~8%, which is the whole point). A dark fill here
   produces a heavy dark outline — the #1 way this build goes wrong. Pill with that fill,
   `ADBE Gaussian Blur 2` Blurriness **15**, blend `multiply`. Ring it: build `ED-hole` (same
   pill + `ADBE Simple Choker`* Choke Matte **+3**), then
   `ae_set_track_matte({layerName:"Edge Darkness", matteLayerName:"ED-hole", type:"alphaInverted"})`.
   (The original is a 5 px CENTERED stroke clipped by the Main matte → only its inner ~2.5 px
   shows; hence choke 3, not 5–6.)
4. **Shadow** — pill below Main, `ADBE Drop Shadow`: Opacity **30%**, Direction **180°**,
   Distance **30**, Softness **80**, **Shadow Only ON** → only the soft floor shadow renders.
   (The original casts from a 10 px stroke ring, not a filled slab — a filled pill throws a
   slightly fuller shadow; if it reads heavy, drop Opacity to ~20–25%.)
5. **Refraction Map** (the displacement source) — pill, fill gray `{r:0.46,g:0.46,b:0.46}`
   (#767676); `ae_apply_gradient({stops:[{r:0,g:0,b:0},{r:1,g:1,b:1}], type:"linear"})` then
   **pin the ramp to the PILL, not the comp**: set `Start of Ramp` = `[cx, cy − H/2]` and
   `End of Ramp` = `[cx, cy + H/2]` via `ae_modify_effect_properties` — the gradient must run
   black→white across the pill's own height (verified on-screen: ring top is BLACK, ring bottom
   WHITE, centre neutral). A comp-wide default ramp leaves the ring mid-gray → near-zero
   displacement → "no refraction". Then `ADBE Gaussian Blur 2` Blurriness **30**; ring it like
   step 3 with `RM-hole` at Choke Matte **+35** (the original is a 70 px CENTERED gradient
   stroke, matte-clipped to its inner half). Hide the result (Opacity 0 — it must not render).
6. **Effects** — `ae_add_adjustment_layer`, position it just above Shadow,
   `ae_set_track_matte(type:"alpha", matteLayerName:"Main")`, then stack IN THIS ORDER:
   - **`CC Glass`***: Surface → Bump Map = the `BG` precomp layer, Property **Lightness**,
     Softness **50**, Height stays default **25**, Displacement **100**; Light → Intensity **65**,
     Height **60**; Shading → Ambient **70**, Diffuse **60** (Specular/Roughness/Metal stay
     default).
   - **`CC Lens`***: Center — same toComp expression as step 2; Size — expression
     `s=thisComp.layer("Main").content("Rectangle 1").content("Rectangle Path 1").size; Math.max(s[0],s[1])*0.025`
     multiplier is **0.025** — CC Lens Size is in its OWN units, not px (default 18.5; the
     final on-screen value is 18.9 for a 755×469 pill). A mid-video panel briefly shows a manual
     probe of ~500 — that state is REPLACED by the expression; do not scale k to "cover the
     corners" in pixels. Tune k only 0.02–0.04. Convergence **80**.
   - **`ADBE Displacement Map`***: Displacement Map Layer = `Refraction Map`, source
     **Effects & Masks**, Max Horizontal **0**, Max Vertical **−110** → the refracting rim.
     (Original panel: Use For Vertical = **Luminance**; with a grayscale map the default Green
     channel is numerically identical — leave the enum alone if setting it fails.)
   - **Transform (`ADBE Geometry2`)**: Anchor Point AND Position — the toComp expression from
     step 2; Scale **110** → subtle magnification of what's behind the glass.
   - **`ADBE Gaussian Blur 2`**: Blurriness **40**, added LAST (after Transform) — the frosted
     backdrop blur that blends the distortion. Effect ORDER in this stack matters: Glass → Lens
     → Displacement → Transform → Blur.
7. **Color** (optional tint) — pill just above Main, fill **white** (the recipe's default; any
   brand color works), Opacity **~40%**, no matte — this is what sells "frosted" on dark
   backgrounds.
8. **Order + animation** — `ae_reorder_layers` to the stack above; `ae_add_null_layer` `CTRL`;
   parent Main, Edge Shine, Edge Darkness, Color, Refraction Map, RM/ED holes, Shadow, Effects
   to it (`ae_modify_layer parentLayerName`). Animate ONLY the null: Position / Scale keyframes
   (`ae_set_keyframes`) + easy ease. The toComp expressions keep sweeps/lens/transform glued.
   - Corner-morph animation (animating Roundness over time) is NOT MCP-reachable (shape-path
     properties can't be keyframed through the tools) — set Roundness at build time; a morphing
     variant is an author-in-AE note for the user.
9. **Verify visually** — `ae_export_frame` mid-animation (~0.5 s in): the rim must show BOTH
   sweeps, the ring refraction must bend the background at the edges, and the interior must be
   blurred + slightly magnified. No refraction → check step 6's Displacement Map layer
   reference and that Refraction Map sits at the same position/size as Main.

## Look levers (what to change per brief)

- **Frost amount** = final Gaussian Blur (20 subtle / 40 recipe / 60 heavy).
- **Backdrop saturation** — real glass materials BOOST saturation behind them (~130%); the tool does
  this by default (`saturation` param; 100 = off). Without it frosted glass reads gray/dead.
- **Refraction strength** = Max Vertical Displacement (−60 subtle … −160 heavy) + ring thickness
  (RM-hole choke 20–45).
- **Glass "thickness"** = CC Lens Convergence (60–95) + Transform Scale (105–115).
- **Rim light** = Edge Intensity (40–80) / Width (80–160); flip Directions for a different key
  light. Keep BOTH sweeps — single-rim glass reads as plastic.
- **Dark UI**: on light backgrounds drop Edge Darkness opacity to ~50%; on dark backgrounds
  raise the tint layer instead.

## Finish the build: package, reconnect, verify (mandatory)

A rig that renders correctly once is not the deliverable. The deliverable is a component that keeps working after it is moved, duplicated, nested and put over different content. Do not report the glass done until the four gates below pass. This is where `ae-clean-rig`'s editable-rig requirements and its delivery checks apply to this rig specifically; the doctrine there governs, this section is only how it lands here.

### 1. Package it as one named unit

- Precompose the whole stack — Main, the `Effects` adjustment, the Refraction Map, the tint and shadow layers — into one semantic precomp named for what the component is. Keep the source element editable inside it: text stays a text layer, an icon stays its own layer.
- Keep the `<name> CTRL` null inside the package and expose Refraction, Frost, Glass Opacity and Magnify on the parent instance through Essential Properties, so the look is adjustable from outside without opening the precomp.
- The background stays OUTSIDE the package. A glass component that carries its own background is a picture of glass, and it cannot be placed over anything else.

### 2. Packaging breaks two things — repair both on purpose

Both are silent. Neither shows up as an error, and both survive a build-time frame check, so repair them as part of packaging rather than waiting for the look to fail.

- **Layer-reference params are index-based.** `CC Glass` Bump Map and the `ADBE Displacement Map` layer are set by integer index. Precomposing, reordering, duplicating or importing shifts every index in the comp, so those references quietly point at the wrong layer or at none. After any structural move, set them again and read them back with `ae_list_effects`; a swallowed set still reports success.
- **`thisComp.layer("Main")` and `toComp()` resolve against the containing comp.** Nesting the rig changes what `thisComp` refers to and which comp space `toComp` maps into, so the sweep centres, the lens centre and the Transform anchor drift off the pill. Move the whole rig together as one unit, then re-render and confirm the rims still sit on the edges.

### 3. Connect a new background

The rig refracts ONE layer, so putting it over different content is a reconnection, not a rebuild.

- Replace the contents of the `BG` precomp, or re-point the Bump Map at the new background layer. If the new background is several layers, `ae_precompose_layers` them into one first.
- Re-point the Refraction Map source and re-pin its ramp to the pill's current position and size, or the bend band will sit where the old pill was.
- Needing a rebuild to change what is behind the glass means the rig was not packaged. Fix the packaging rather than rebuilding.

### 4. Verify in AE, on the composition, after the change

The build-time report and a preview frame prove only that the rig assembled. Export frames from the actual composition after each change and read them:

- one frame over the NEW background — confirm the rim band bends that background, not a remembered one;
- one frame with the CTRL null moved to a different position — confirm the sweeps, lens and magnification travel with it and nothing clips at the pill edge;
- one frame after a real content edit inside the package, such as a longer word or a different icon — confirm the alpha-derived refraction follows the new shape.

A tool call that returned success is not evidence, and a rig that only holds at its original position and its original background has not met this gate.

## "Doesn't look right" checklist (symptom → the step that went wrong)

| Symptom | Cause → fix |
|---|---|
| Heavy dark outline around the pill | Edge Darkness fill is dark — it must be **#EAEAEA** at Multiply (step 3) |
| No background bending at the rims | Ramp on Refraction Map left comp-wide (mid-gray ring) → pin Start/End to the pill's top/bottom (step 5); or Displacement Map layer reference didn't stick (NEEDS-LIVE-VERIFY) |
| Distortion covers the WHOLE frame | `Effects` adjustment lost its alpha matte to Main (step 6) |
| Interior warps uniformly, no lens feel | CC Lens Size expression missing or k scaled to pixels (hundreds) — k must be **0.025** in CC Lens's own units (step 6) |
| Rim shine on one side only | Second CC Light Sweep missing or Direction not flipped to +118° |
| Glass reads flat/plastic | Final Gaussian Blur 40 missing, or Transform ×110 magnification missing |
| Effects visibly clip at pill edge during moves | toComp expressions missing on sweep Centers / lens Center / Transform anchor+position |

## NEEDS-LIVE-VERIFY (undocumented contracts — check on first run, don't assume)

- Layer-reference effect params (`CC Glass` Bump Map, `ADBE Displacement Map` layer) via
  `ae_modify_effect_properties` — pass the target layer's INDEX (integer). If the set is
  silently swallowed, read back with `ae_list_effects`/`ae_get_layer_info` and report the gap.
- Enum params as integers (Property=Lightness, Behavior=Effects & Masks).
- `ADBE Simple Choker` matchName; CC Lens/CC Glass presence (Cycore ships with AE, same family
  as CC Light Sweep which is already proven on this server).
