---
name: ae-depth-space
description: 2.5D depth recipes for a server with no 3D layers and no camera — null-rig parallax slider ladders, single-image displacement-map parallax with px budgets, exponential atmosphere and haze, defocus via lens-blur maps, grounding shadows, perspective floors, motion-blur speed budgets, and the diagnostic list for why a scene reads flat.
---

# AE Depth & Space — 2.5D recipes on the real tool surface

No 3D layers, no camera, no lights on this server. Everything below runs on: position/scale
keyframes (`ae_set_keyframes`), transform expressions (`ae_set_expression` — 5 transform props only),
effect keyframes/expressions (`ae_set_effect_keyframe` / `ae_set_effect_expression`), sliders
(`ae_add_expression_control`), effects by matchName (`ae_apply_effect`), masks/mattes/blend modes,
`ae_set_motion_blur`, `ae_apply_gradient`, `ae_precompose_layers`. matchNames marked `*` are not in
the registered-effects list — pass as raw matchName; if a call errors, verify via `ae_describe_tool`
once, then drop that recipe (never loop retries).

## 0. The consistency law (why scenes read as sliding cardboard)

One depth coefficient per plane: **p = zoom/(zoom + z)** (use zoom = 2666.67 for a 1920-wide comp,
= 1.3889 × comp width). From ONE p derive ALL THREE: parallax speed multiplier = p, relative scale
= p, atmosphere amount ∝ (1 − p). A layer at 50% scale moving at 80% speed = flat collage. Screen
size ∝ 1/distance, so: 2× farther = 50% size = 50% speed = one more haze step. Never let the
ladders disagree.

- **Plane count:** 3 = floor, **5 = sweet spot**, >8 adds nothing (speed deltas fall below what the
  eye separates). Adjacent planes must differ 2–4× in speed; 10% steps merge.
- **Occlusion is cue #1 and free** (layer order): plane silhouettes must physically OVERLAP, never
  just touch edges.
- **Blur is double-edged (measured):** defocus REDUCED depth discrimination d′ 1.56→1.22 in a
  controlled study. Keep perspective-line planes and occlusion edges SHARP; blur only the extreme
  FG occluder and geometry-free sky/atmosphere. Heavy top+bottom blur gradient = tilt-shift
  miniature — the scene turns into a toy.

## 1. Null-rig parallax (the workhorse)

ONE null "CAM" at comp centre is the only thing animated. Do NOT parent the planes (parenting is
for group moves; this rig is for per-plane ratios).

1. `ae_add_null_layer(name:"CAM")` — leave at centre.
2. Per plane: `ae_add_expression_control({layerName, controlType:"slider", name:"Parallax"})`,
   then `ae_set_expression` on **Position**:
```javascript
center = [thisComp.width, thisComp.height]/2;
leader = thisComp.layer("CAM");
offset = leader.position - center;
value + offset*effect("Parallax")("Slider")/100;
```
3. **Slider ladder:** sky **0** / far mountains **5–10** / hills **15–30** / mid **40–70** /
   focal plane **100** / FG **120–150** (hero fly-through up to 200–300). Keep slow-to-fast spread
   3–5×.
4. **Scale = slider:** slider 72.7 → the plane is scaled to 72.7% of focal-plane size (that IS p).
   Slider 57.1 → 57.1%. Enforce for every plane.
5. **Infinity plane s=0 strictly** — the far plane never moves a frame. A creeping sky reads as a
   bug.
6. Keep alive: `wiggle(1,2)` on CAM Position — constant micro-parallax stops the stack freezing
   back into a postcard.
7. Animate ONLY the CAM null (`ae_set_keyframes` on its Position; 2–4 batched calls per build).

**Movement grammar:** lateral pan = offsets down the ladder, FG runs OPPOSITE to BG (counter-motion
reads as orbit around the mid subject). **Push-in = NO translation**, counter-scale only:
FG Scale 100→110–115%, BG 100→90–95% over 3–5 s, easy ease, mid nearly static; anchor each plane at
its ground-contact point (or the vanishing point). Exact dolly form: scale_mult = z/(z−Δ) with
virtual depths fg 0.5Z / mid 1Z / bg 2Z / sky 4Z (Z = zoom): push Δ=0.1Z → fg ×1.25, mid ×1.111,
bg ×1.053, sky ×1.026. Zoom-in ever needed → exponential, never linear:
`ae_set_expression` on Scale `s=v1*Math.exp(Math.log(v2/v1)/T*time); [s,s]`.

## 2. Single-image parallax: Displacement Map (`ADBE Displacement Map`*)

Depth from ONE flat image. The warp IS a stereo shift, so stereo px limits apply.

- **Neutral contract:** displaces symmetrically around 50% gray. Neutral = **exactly RGB(128,128,128)**
  in 8bpc (127 "looks 50%" but the whole frame drifts once Max > ~100 px).
- **Budget:** full B/W map gives spread = 2 × Max slider. Keep total spread ≤ 1.5–3% of frame width
  → **Max Horizontal Displacement 15–29 px @1080p**; ±58 px is the red line. Locked far plane:
  author map FAR=128 gray, NEAR=255 white (spread = 1 × Max).
- **Pre-blur the map** (`ADBE Gaussian Blur 2`, Blurriness ≈ Max Displacement, 20–30 @1080p), then
  precompose map. Hard silhouette steps = tearing (neighbouring pixels shift opposite ways).
  Two-pass refinement: vertical-only blur 1.5–2× stronger than horizontal.
- **Banding:** 16bpc project + 3–5% mono noise (`ADBE Noise2`) on the map + pre-blur. AI maps
  (Depth Scanner / Photoshop Neural Filters) come low-res: scale the map precomp to comp size
  FIRST, then blur — else upscale stairs become displacement bands.
- **Animate camera-less:** keyframe **Max Horizontal Displacement −D → +D** (D = 15–29 px) over
  3–5 s via `ae_set_effect_keyframe`; loop via `ae_set_effect_expression`:
  `amp*Math.sin(time*2*Math.PI/period)`. Max Vertical = 0 or ≤ D/3.
- **Threshold to cutouts:** displacement only PULLS pixels — it cannot reveal what's behind an
  edge. Needed spread > ~2–3% width (>40–58 px @1920) → cut the image into depth planes instead
  (mask each plane +10–15 px, fill holes behind FG before animating) and run the §1 rig.
- **One map, three cues** (all consistent because one source): (a) Camera Lens Blur with
  Blur Map = the depth precomp → DOF; (b) map as luma matte on a haze-coloured solid → atmosphere;
  (c) keyframe Blur Focal Distance → rack focus.

## 3. Atmosphere (exponential, never linear)

Aerial perspective belongs to VISTA planes (>30 m equivalent) — haze on a near plane reads as fog,
not distance. Per plane back, move all four axes together monotonically: value toward sky, contrast
down, hue toward sky colour, edges softer. FG is the inversion: darkest shadows, max saturation,
sharpest edges.

- **Saturation ladder:** 0 / −15 / −30 / −50 front-to-back (`ADBE HUE SATURATION`).
- **"Flash the blacks":** pure black in a far plane is physically impossible — the loudest fake
  tell. Adjustment layer with a vertical `ae_apply_gradient` ramp layer as **luma matte**
  (`ae_set_track_matte`), Levels (`ADBE Easy Levels2`*) raising **Output Black**, stronger on
  farther planes.
- **Blue shift:** Curves blue channel ~Input 114 → Output 102 per plane (10–12 level steps).
  Far-mountain reference colour **#a6c8d8**.
- **Tint, NOT Opacity:** fading far layers by Opacity breaks on overlaps (background shows
  through). Haze = colour convergence to sky colour → `ADBE Tint` amount on the same distance
  curve.
- **Exponential for free:** equal haze solids between equal depth steps auto-compound the
  exponential: 4 pale-blue solids at **15% opacity** between 5 planes → far plane behind 48%
  haze, mid 28%, near 15%. Dense mood 20–25%/step, clear day 5–8%.
- **Fog planes:** solid + `ADBE Fractal Noise` — Fractal Type Cloudy, Noise Type Soft Linear,
  Contrast 20, Transform Scale Width **500** / Height **200** (stretch = fog bank, not cloud),
  Complexity 10, blend **Screen 25–35%**, mask lower third with huge feather (~440 px @1080p).
  Animate Evolution `time*150` via `ae_set_effect_expression`. 2–3 offset overlapping copies —
  the stagger itself creates volume. Interleave 4–6 masked fog solids BETWEEN depth planes.

## 4. DOF without a camera: `ADBE Camera Lens Blur`

- **Blur Map = hand z-buffer:** precomp where each plane is filled flat gray = its depth
  (0 near / 128 mid / 255 far). Blur Focal Distance is calibrated 0–255 — keyframe it via
  `ae_set_effect_keyframe` = **rack focus between 2D planes with no camera** (rack focus is itself
  a depth cue: it proves the scene has planes). Mid-gray focus ≈ 154 (NEEDS-LIVE-VERIFY).
- **Blur ladder saturates — 4:6:7, not 1:2:3:** planes at 2×/4×/8× subject distance get 0.5/0.75/
  0.875 of max blur (e.g. mid 0 / near-BG 8 / far-BG 12 / sky 14 px). FG flying objects may exceed
  the BG max (20–30 px).
- Iris Roundness 100 = round bokeh; Diffraction Fringe 500 = soap-bubble rim, 0 = flat disc.
  Highlight Threshold works 0–1: start at 1, lower until ONLY true speculars bloom.
- Static scene shortcut: map = `ae_apply_gradient` ramp (white on far planes AND extreme FG, black
  on subject plane).

## 5. Grounding + perspective floor

- **Double shadow** (standard elevation values): contact pass `ADBE Drop Shadow` distance 2–4 px,
  softness 4–8, opacity 20%; ambient pass distance 8–16, softness 24–48, opacity 12–14%. One soft
  shadow = floating object.
- **On a perspective floor:** shadow-only duplicate, Scale **[100, −30]** at the contact point,
  blur 10–20 px, 20–30% opacity, Multiply. Dark contact core + wide weak skirt = "touches the
  floor" → the floor exists as a plane.
- **Floor itself:** `ADBE Corner Pin` stretches texture LINEARLY = "tilted wall". Use
  **`CC Power Pin`* with Perspective ON** — texture rows compress as 1/z. Trapezoid geometry: far
  edge width = near edge × z_near/z_far (floor spanning 2–10 m → far edge 20% width); far edge
  sits below the horizon (horizon = eye height, y 380–540 @1080p standing). Example @1920×1080,
  horizon y=430: near pins (0,1080),(1920,1080), far pins (768,560),(1152,560).
- **Floor light (inverse square):** radial `ae_apply_gradient` under the source, brightness
  stations quarter-per-doubling: 100% @1 m → 25% @2 m → 6% @4 m (in floor-texture space, BEFORE
  the pin). Linear gradient = airbrush; quarter-per-doubling = physics.

## 6. Motion blur (mandatory — FG planes at 1.2–1.5× strobe without it)

- **Two switches:** `ae_set_motion_blur({compositionName, layerName, enabled:true})` per moving
  plane (it auto-enables the comp switch). Comp default: also pass `shutterAngle:180`.
  (Shutter Phase is not settable via MCP — AE default applies; at angle 180 the ideal is −90.)
- **Speed budget (7-second rule):** max travel of the FASTEST plane = compWidth/(7 × fps).
  Budget the CAM null by the fastest ratio: CAM_max = compWidth/(7 × fps × maxRatio) —
  ≈ **7.6 px/frame** @1920/24fps with FG at 1.5×. Faster needed → shutterAngle 270–360 buys
  ×1.5–2 speed (smear reads as speed; judder reads as broken playback).
- **Expression rigs blur free** — AE samples expressions at sub-frame times, so the §1 rig gets
  correct per-plane blur with zero keyframes. wiggle() is time-coherent and safe; unseeded
  random() flickers.
- **Never scroll with `ADBE Offset`** — it renders sharp regardless of switches, and a sharp BG
  under a blurred FG inverts the depth cue. Use Motion Tile (`ADBE Tile`*) animating Tile Center,
  or real Position. Movement inside a precomp is invisible to the parent's blur — enable the
  switches inside the precomp, or collapse transformations.

## 7. Edges & unification (the glue — planes must look shot by one lens)

- **Light wrap (kills the "sticker" look):** duplicate the BG on top → Fast/Box Blur ~70, Repeat
  Edge Pixels ON → matte it to the FG silhouette → keep only a 5–10 px rim → **Screen 70–75%**.
  Cutout hygiene: 1 px alpha Channel Blur* on every cutout edge; feather-then-choke 1–2 px.
- **Grain — ONE pass over the whole stack** (adjustment on top): `ADBE Noise2` Amount ~8% (the
  registered, always-present effect; Add Grain is version-unreliable). Never grain planes
  individually — shared noise frequency = one sensor.
- **Vignette:** black solid + inverted ellipse `ae_add_mask`, Mask Feather **350–500 px** @1080p,
  opacity 20–40%; centre slightly above frame centre (floor darkens faster than sky). As a subtle
  depth element: 10%/200 px.
- **Lens contract (one number for the whole stack):** `ADBE Optics Compensation` on a comp-sized
  adjustment — FOV **40** forward = soft wide-lens curvature, **60** = action-cam barrel; same FOV
  for every element (undistort plates Reverse ON / re-distort composites forward). Chromatic
  aberration lives in CORNERS only: total R↔B split 0.5–0.75% of width (10–14 px @1920), zero at
  centre. Pick ONE anamorphic squeeze S and derive everything: Camera Lens Blur Iris Aspect
  Ratio = 1/S, streak length ∝ S, crop to 2.35:1 AFTER the artifacts. One artifact without its
  siblings = filter; a correlated set = a lens.
- **Tele vs wide contract:** telephoto scene = small speed deltas + strong haze; wide scene =
  large speed/scale deltas + light haze. Mixing the vocabularies is a subtle but fatal
  inconsistency.

## 8. Vertical 9:16 (1080×1920) — different budgets

- **Lateral parallax de-rated:** narrow FOV amplifies horizontal motion → ≤ **1.5% ≈ 16 px** for
  continuous movement (32–36 px only for one slow reveal). **Vertical axis is the star:** 3% of
  1920 = **57.6 px** budget — use tilt, pedestal, push-in; avoid pans.
- **Y-rig:** one Y-slider on the null, per-plane k = 0.2 / 0.5 / 0.8 / 1.0 / 2.0 via
  `value + [0, slider*k]`.
- **Horizon slots:** y = **640** (high horizon → 1020 px of receding ground = max texture-gradient
  depth) or y = **1280** (low → near band + sky scale); never dead centre without intent.
  Vanishing point x = 540 ± 90.
- **Safe depth core:** anchors that carry the depth read (VP, subject eyes, occlusion nodes)
  inside **900×1400 centred** (y 260–1660) and inside the 4:5 crop core (y 285–1635); outer bands
  are sacrificial garnish (grass tips, canopy) under platform UI.

## 9. "Why it reads flat" checklist (top offenders → fix)

| Symptom | Fix |
|---|---|
| Planes slide like cardboard | One p per plane: slider 72.7 ⇒ scale 72.7%; adjacent speeds 2–4× apart |
| Stickers on a background | Light wrap Screen 70–75% + 1 px alpha blur + choke; one grain pass on top |
| Far plane too contrasty/black | Flash the blacks (Levels Output Black via ramp matte); sat 0/−15/−30/−50; 15%/step haze |
| Push-in looks like digital zoom | Counter-scale (FG 110–115 vs BG 90–95, 3–5 s) or exponential scale; never linear, never lateral drift |
| Strobing on the move | Both MB switches + angle 180; speed ≤ compWidth/(7×fps×maxRatio); faster → angle 270–360 |
| Scene looks miniature | Soften the DOF gradient (4:6:7 ladder); keep geometry planes sharp |
| Fog is a milky sheet | Haze only on far planes; equal 15% solids between planes; Tint not Opacity |
| Objects float | Double shadow (contact 2–4 px/20% + ambient 8–16 px/12%); flattened Multiply dupe on floors |
| Floor reads as tilted wall | CC Power Pin + Perspective; far edge = near × z_near/z_far; quarter-per-doubling light |
| Sky creeps | Infinity plane s=0, always |
| Parallax freezes in stills | `wiggle(1,2)` on the CAM null |
| Depth dies in 9:16 | Vertical moves ≤57.6 px, lateral ≤16 px; horizon y 640/1280; anchors in 900×1400 core |
