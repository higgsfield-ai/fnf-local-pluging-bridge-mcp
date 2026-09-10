---
name: ae-animation-principles
description: Motion construction — 30fps timing tables, temporal-ease influence values, easing curves matched to motion type, staggers, the house entrance reveal, a pattern library and expression cookbook, and the 12 principles of animation as AE expressions, as broadcast delivery constraints, and as spec-writing concepts.
---

# AE Animation Principles

**Value contract:** colors are {r,g,b} 0-1 (not hex), position is the layer CENTER, and effect keys / property names are case-sensitive. This skill calls `ae_set_keyframe`, `ae_set_temporal_ease`, `ae_apply_easy_ease`, and `ae_set_expression`. Every call's first param is `compositionName` (the exact comp name string), and `propertyName` is the Capitalized enum: `"Position"` | `"Scale"` | `"Rotation"` | `"Opacity"` | `"Anchor Point"`.

This skill is the **motion brain**. It enforces three rules:

1. **No linear keyframes on spatial / hero motion.** Every Position and Scale keyframe pair (and any hero reveal) must have an ease. **Pick the easing tool by property type: `ae_apply_easy_ease` ERRORS on 2D `Position` — for spatial properties (`Position`, and the multi-value `Scale` / `Anchor Point`) ease with `ae_set_temporal_ease` (re-interpolates existing keys) or `ae_set_keyframe_advanced` (key + bezier in one call). Reserve `ae_apply_easy_ease` for the scalar props (`Opacity`, `Rotation`).** Linear = robotic = broken. **Exception:** an Opacity *fade* may stay linear (a fade reads fine with no ease), and looped wiggle frames are linear by nature.
2. **Timing is rhythm, not randomness.** Use the timing table below — every animation has an anticipation, action, and settle phase, with frame counts chosen from the table.
3. **Animations narrate.** A scene reads left-to-right, big-to-small, BG-to-FG. Stagger reveals; don't fire everything at once.

---

## Timing table (assume 30fps unless noted)

| Phase | Frames | Seconds | Use for |
|---|---|---|---|
| Snap | 2-4f | 0.07-0.13s | Cut-style transitions, flash, bullet-hit |
| Anticipation | 4-6f | 0.13-0.2s | Pre-roll before main action (squash before jump) |
| Quick action | 8-12f | 0.27-0.4s | Hero reveals, smash zooms, slide-ins |
| Cinematic action | 18-30f | 0.6-1.0s | Slow text reveals, camera moves, big transitions |
| Settle | 6-10f | 0.2-0.33s | After-bounce, residual motion |
| Loop period | 60-240f | 2-8s | Ambient loops (wiggle, breath, orbit, drift) |
| Hold | 30-90f | 1-3s | Time to read text |

**Default scene duration cheat:**
- Logo reveal: 60-90 frames (2-3s)
- Title card with intro animation: 120-180 frames (4-6s)
- Looping ambient scene: 240 frames (8s)
- Brand reel beat: 90 frames per beat × N beats

---

## Two easing tools — pick the right one

These are **two different tools**; do not conflate them:

- **`ae_apply_easy_ease`** = the simple uniform ease. Signature: `{ compositionName, layerName, propertyName, influence }` where `influence` is 0-100 (default 33). It applies one uniform bezier ease to **ALL** keyframes of that property on that layer (there is **no** direction — no `easeType`, no `"IN"`/`"OUT"`/`"BOTH"`), and it only re-interpolates keys that **already exist** — set them with `ae_set_keyframe` first. **It ERRORS on 2D `Position` — use it only on the scalar props (`Opacity`, `Rotation`); for `Position` / `Scale` / `Anchor Point` ease with `ae_set_temporal_ease` or `ae_set_keyframe_advanced` instead.** Use this for scalar reveals where the same ease on every key is fine.
- **`ae_set_temporal_ease`** = the per-keyframe, directional influence/speed tool. Signature: `{ compositionName, layerName, propertyName, time? | keyIndex?, speedIn=0, influenceIn=33, speedOut=0, influenceOut=33 }`. Use it whenever you need a *direction* (ease-OUT = high `influenceOut`, low `influenceIn`; ease-IN = the reverse) or when individual keyframes need *different* influence/speed (overshoot bounce, punch-in). The influence/speed table below feeds this tool.

## Easing curves (ae_set_temporal_ease influence/speed values)

The `ae_set_temporal_ease` tool takes `influenceIn`, `speedIn`, `influenceOut`, `speedOut` per keyframe (target the key via `time` or `keyIndex`). Defaults below produce industry-standard curves. Influence is 0-100, Speed is unitless (use 0 unless creating a specific velocity match). Notation `inInf/outInf` below maps to `influenceIn`/`influenceOut`.

| Curve name | When to use | influenceIn | influenceOut | Notes |
|---|---|---|---|---|
| **Linear** | Only opacity fades + looped wiggle frames | 0 | 0 | Robotic — forbidden for spatial / hero motion (position, scale) |
| **Ease Out 70** | Default hero reveal | 0 | 70 | Quick start, soft landing — most common |
| **Ease Out 85** | Cinematic premium | 0 | 85 | Premium keynote feel, decelerating push |
| **Ease In 70** | Exits, anticipation | 70 | 0 | Slow start, accelerating off-screen |
| **Ease In-Out 60** | Smooth A→B with no emphasis | 60 | 60 | Camera moves, parallax |
| **Ease In-Out 85** | Heavy cinematic move | 85 | 85 | Big camera push with slow-mo feel |
| **Snap (overshoot bounce)** | Playful UI, bounce | 0 | 95 on first kf; 75 on settle | + 1 extra settle keyframe at 105% scale before final |
| **Punch in then ease out** | Smash zoom | 0 (speed on outgoing); settle 70 | — | First kf has speed, ease out into final |

For a uniform (non-directional) ease, use `ae_apply_easy_ease` with just `influence` (e.g. `influence: 70`). When you need direction (ease-out vs ease-in), use `ae_set_temporal_ease` and set `influenceOut` high for reveals, both high for camera, `influenceIn` high for exits.

**Premium default = settle-weighted, NOT flat.** For a hero reveal, leave the START key with pace (low `influenceIn` ≈ 20) and arrive SOFT at the REST key (high `influenceIn` ≈ 75). Flat 33/33 on both keys reads mechanical; the asymmetric settle (ease-out into the landing) is what makes motion feel intentional — this is the `ae-animation-principles (module: reveal-motion)` profile and the house default for everything that enters.

---

## Spatial vs temporal easing (orthogonal — do not conflate)

These are **two independent axes** on a keyframe; a property can ease differently on each:

- **TEMPORAL easing** = value *speed over time* — how fast the property's value changes between keys. This is what the **value graph** (speed/influence) controls. `ae_set_temporal_ease`, `ae_apply_easy_ease`, and the influence/speed table above are ALL temporal-only.
- **SPATIAL easing** = *motion-path curvature* — the SHAPE of the path a layer travels through space (only meaningful for `Position` / `Anchor Point`, since they trace a 2D path). This is the **motion graph** (the path overlay in the comp). It is set by the spatial interpolation type per keyframe (Linear path = straight segments / sharp corners; Bezier path = curved, smooth turns with editable tangent handles), NOT by `ae_set_temporal_ease`.

They are genuinely independent: e.g. a layer can move with **linear TEMPORAL** (constant speed, no accel/decel) along an **ease-out SPATIAL** path (a curved arc), or constant-speed temporal along a perfectly straight spatial line, or any combination.

**Spatial-interpolation recipe (path curvature):**
```
Sharp / mechanical corner (robot, UI snap):  Linear spatial → the path turns at a hard vertex
Smooth arc (organic, character, drift):       Bezier spatial → tangent handles round the corner
A layer that curves IN and lands soft:        Bezier spatial path + ease-out TEMPORAL on arrival
```
A common bug: a hero element with a perfect temporal ease that still looks "robotic" through a turn — the fix is SPATIAL (round the path), not more temporal influence. ae-mcp exposes temporal control directly (`ae_set_temporal_ease`); for spatial path curvature set the position keys via `ae_set_keyframe_advanced` (key + bezier in one call) — `ae_set_temporal_ease` will NOT change the path shape.

---

## Easing semantics matrix (intent → easing)

Easing is **SEMANTIC, not decorative** — the curve communicates *meaning* about the action. Pick the family from the action's intent, then a specific curve from the bezier table below.

| Intent / feeling | Easing family | Why | Typical actions | Specific curve |
|---|---|---|---|---|
| Responsive / affirmation / snappy | **ease-OUT** (fast start, slow end) | Object arrives eager, settles confident | Button feedback, entrance reveals, success/confirm states | Quart-out or Back-out (slight overshoot) |
| Reluctance / hesitation | **ease-IN** (slow start, fast end) | Object resists, then leaves | Error states, dismissals, exits, off-screen departures | Quart-in (e.g. a confirm-button dismiss/exit = Quart ease-in) |
| Neutral / informational | **ease-IN-OUT** | No emotional emphasis, balanced | Camera moves, parallax, A→B repositions, status changes | Sine-in-out or Cubic-in-out |
| Mechanical (avoid) | **LINEAR** | Reads robotic / unfinished | — (only opacity fades + looped wiggle) | none |

Decision rule: *entrance / "yes" → ease-OUT; exit / "no" → ease-IN; just moving info → ease-IN-OUT; never LINEAR on hero motion.* Map the chosen family to influence on `ae_set_temporal_ease` — ease-OUT = `influenceOut` high / `influenceIn` low; ease-IN = the reverse; ease-IN-OUT = both high (and read the matching control points from the bezier table to size the influence).

---

## Cubic-bezier curve library (control points)

Web/CSS `cubic-bezier(x1, y1, x2, y2)` curves, ported as the reference for picking influence. Higher `influenceOut` ≈ a flatter-tailed out-curve (Quart/Quint > Cubic > Quad > Sine); `Back`/`Elastic`/`Bounce` need a settle keyframe (see overshoot/bounce below) because AE temporal bezier can't go past the end value on its own.

| Curve | ease-in (x1,y1,x2,y2) | ease-out (x1,y1,x2,y2) | ease-in-out | Maps to ~influence |
|---|---|---|---|---|
| **Sine** | .12,0,.39,0 | .61,1,.88,1 | .37,0,.63,1 | out ≈ 55 |
| **Quad** | .11,0,.5,0 | .5,1,.89,1 | .45,0,.55,1 | out ≈ 65 |
| **Cubic** | .32,0,.67,0 | .33,1,.68,1 | .65,0,.35,1 | out ≈ 70 (house default) |
| **Quart** | .5,0,.75,0 | .25,1,.5,1 | .76,0,.24,1 | out ≈ 80 |
| **Quint** | .64,0,.78,0 | .22,1,.36,1 | .83,0,.17,1 | out ≈ 85 |
| **Expo** | .7,0,.84,0 | .16,1,.3,1 | .87,0,.13,1 | out ≈ 90 |
| **Circ** | .55,0,1,.45 | 0,.55,.45,1 | .85,0,.15,1 | out ≈ 88 |
| **Back** | .36,0,.66,-.56 | .34,1.56,.64,1 | .68,-.6,.32,1.6 | overshoot — add settle kf |
| **Elastic** | (springy in) | (springy out) | — | use overshoot expr |
| **Bounce** | (decaying drops) | (decaying drops) | — | use bounce expr |

The negative / >1 Y components on Back/Elastic/Bounce are why a plain temporal ease can't reproduce them — they require an explicit overshoot/settle keyframe or an inertial expression (next section).

**Standard UI-system durations (port to frames @30fps):** micro-interactions (toggles, button press, ripple) = **100–200ms = 3–6f**; transitions / reveals / page moves = **300–500ms = 9–15f**. These match the timing table: micro ≈ Snap/Quick, transition ≈ Quick/Cinematic.

---

## Spring physics → AE inertial expressions

Designers coming from Framer / web springs describe motion as `mass / stiffness / damping` (Hooke's Law: restoring force `F = -k·x`, where `k` = stiffness). AE has no native spring, so cross-map the spring to the inertial-bounce/overshoot expression below.

| Spring preset | mass | stiffness (k) | damping | Feel | AE overshoot params (amp px, freq, decay) |
|---|---|---|---|---|---|
| Framer default | 1 | 100 | 10 | gentle settle, slight overshoot | amp 8, freq 2, decay 4 |
| Bouncy | 1 | 300 | 10 | fast + multiple overshoots | amp 10, freq 3, decay 2 |
| Smooth (no bounce) | 1 | 100 | 20 | critically damped, no overshoot | use ease-out 80, no expression |

Mapping rules: **stiffness → freq** (stiffer = higher freq = faster oscillation); **damping → decay** (more damping = higher decay = settles sooner, fewer bounces; damping high enough relative to stiffness = critically damped = no overshoot at all, so just use ease-out); **mass** stretches the period (heavier = slower, nudge freq down). A Framer-spring `{stiffness:300, damping:10}` reproduces in AE as the bouncy overshoot expression with `freq=3, decay=2`.

---

## Overshoot & bounce expressions (velocity-matched)

Two canonical inertial expressions. Apply via `ae_set_expression` on a **transform property only** (`Position` / `Scale` / `Rotation` — never `Source Text` or effect props). Both assume the property has keyframes; the expression adds residual motion AFTER the last keyframe by reading its post-key velocity.

**(1) OVERSHOOT** (single decaying sine — the spring/settle):
```
amp = 80;          // px — overall reach (but see SUBTLE rule below)
freq = 3;          // oscillations/sec  (1–3 typical)
decay = 4;         // settle rate       (1–5; higher = settles faster)
n = nearestKey(time).index;
if (key(n).time > time) n--;
if (n == 0) t = 0; else t = time - key(n).time;
if (t > 0 && n == numKeys) {
  v = velocityAtTime(key(n).time - thisComp.frameDuration/10);
  value + v * (amp/100) * Math.sin(t * freq * Math.PI * 2) / Math.exp(t * decay);
} else value;
```
**sin vs cos selection:** use **`sin`** when the property arrives *with* velocity and should overshoot PAST the target then swing back (the spring continues the motion) — this is the default for slides/entrances. Use **`cos`** when the property should start its wobble already displaced at t=0 (e.g. a struck/plucked element that begins at max deflection), since `cos(0)=1`.

**(2) BOUNCE** (parabolic drops with elastic restitution — a ball settling):
```
e = 0.7;           // elasticity / restitution (0.7 = each bounce ~70% of prior height)
g = 5000;          // gravity (px/s²)
nMax = 9;          // max bounces to compute
n = nearestKey(time).index;
if (key(n).time > time) n--;
if (n > 0 && n == numKeys) {
  v = -velocityAtTime(key(n).time - thisComp.frameDuration/10) * e;
  vl = length(v); vu = (vl > 0) ? normalize(v) : [0,0];
  tCur = time - key(n).time; tb = 2 * vl / g; tNext = tb;
  nb = 1;
  while (tCur > tNext && nb <= nMax) { vl *= e; tb = 2 * vl / g; tNext += tb; nb++; }
  if (nb <= nMax) {
    tPrev = tNext - tb; t2 = tCur - tPrev;
    value + vu * (vl * t2 - g * t2 * t2 / 2);
  } else value;
} else value;
```

**Worked overshoot example (slide-in with 2–5 frame offset):** R3 slides a layer to `target_x` over 18f. Apply the OVERSHOOT expression to `Position` with `amp 8, freq 2, decay 4` — the layer reaches `target_x`, overshoots ~6px past it, swings back, and settles. The overshoot peak lands **2–5 frames** after the keyframe arrival (the first sine half-cycle), which is the offset that reads as "weight." Want a snappier settle → raise `decay` to 5; want a longer ring → lower to 2.

**SUBTLE rule — overshoot is 3–10px ONLY.** Despite `amp=80` in the formula (it's scaled by post-key velocity, so the *visible* overshoot is much smaller), tune so the actual on-screen overshoot stays **3–10px**. More than ~10px reads cheap / cartoonish / "PowerPoint." For Scale, keep the overshoot to ~+2–5% (e.g. 100% → 103% → 100%, matching R2's micro-bounce). Restraint is the difference between premium and toy.

---

## Tool-call cheat sheet — recipe notation → real ae-mcp calls

The recipes below are **pseudocode**. Translate them into real calls like this:

- **Property names** map directly to the `propertyName` field, Capitalized: `"Position"`, `"Scale"`, `"Opacity"`, `"Rotation"`, `"Anchor Point"`.
- **`time` is in seconds**, not frames. Convert frame counts at the comp fps: at 30fps, `12f` → `time: 0.4`, `18f` → `time: 0.6`.
- **Value formats (§6):** `Position` → `[x, y]` TUPLE (px, comp top-left origin); `Scale` → `[percentX, percentY]` TUPLE so **pass `130` not `1.3`** (e.g. `130%` → `[130, 130]`, `100%` → `[100, 100]`); `Opacity` → a plain number `0`–`100`; `Rotation` → degrees.
- **Every call needs `compositionName`** (the exact comp name string) as its first param.
- **Ease is a separate call after both keyframes exist.** Use `ae_apply_easy_ease` (`influence` 0-100) for a uniform ease across all keys; use `ae_set_temporal_ease` (`influenceIn`/`influenceOut`) when you need direction or per-keyframe influence/speed (overshoot/punch).

Recipe R1 (Fade-Up Hero Text) becomes:
```
// Opacity 0% → 100% over 12f (= 0.0s → 0.4s)
ae_set_keyframe({ compositionName: "Main", layerName: "title", propertyName: "Opacity", time: 0.0, value: 0 })
ae_set_keyframe({ compositionName: "Main", layerName: "title", propertyName: "Opacity", time: 0.4, value: 100 })

// Position Y: base_y + 30 → base_y, where base_y = the layer's current Y
// (read it from ae_get_layer_info, or use the layout Y you measured for the build).
// e.g. base_y = 540 — value is an [x, y] TUPLE:
ae_set_keyframe({ compositionName: "Main", layerName: "title", propertyName: "Position", time: 0.0, value: [960, 570] })
ae_set_keyframe({ compositionName: "Main", layerName: "title", propertyName: "Position", time: 0.4, value: [960, 540] })

// Directional ease-out across the position keys (opacity fade may stay linear — see rule 1):
ae_set_temporal_ease({ compositionName: "Main", layerName: "title", propertyName: "Position", influenceIn: 0, influenceOut: 70 })
// (Do NOT use ae_apply_easy_ease on Position — it ERRORS on 2D Position.
//  For a uniform, non-directional spatial ease either set the keys with ae_set_keyframe_advanced
//  (key + bezier influence in one call) or call ae_set_temporal_ease with influenceIn ≈ influenceOut.)
```

**Undefined recipe variables** (`base_y`, `target_x`, `start_z`, `layer_width`) are **not literals** — they are the layer's current/base value or a measured layout value the agent computes: read the current transform with `ae_get_layer_info`, or take the target X/Y/width from your own measurement of the layout. Resolve them to concrete numbers before the call.

---

## Recipe Library — copy-paste-ready

Each recipe = the property keyframes + ease + the optional expression. Apply via `ae_set_keyframe` (for keyframes) and `ae_set_expression` (for expressions — **transform properties only**, never `"Source Text"`; see the note in R13). Then ease: for scalar `Opacity`/`Rotation`, `ae_apply_easy_ease` gives a uniform curve; for **spatial `Position`/`Scale` use `ae_set_temporal_ease` or `ae_set_keyframe_advanced`** (`ae_apply_easy_ease` ERRORS on 2D Position). See the cheat sheet above for how the notation maps to real calls — scale values are passed as `[130,130]` not `1.3`, time is in seconds, every call needs `compositionName`.

### R1. Fade-Up Hero Text (most common reveal)
```
Layer: text
Properties:
  Opacity:    [0%@0f] → [100%@12f]                ease: easeOut
  Position Y: [base_y + 30 @0f] → [base_y @12f]   ease: easeOut
Duration: 12f (0.4s)
Hold: keep visible until end of comp
```

### R2. Smash Zoom Entry
```
Layer: text or logo
Properties:
  Scale: [130%@0f] → [100%@8f] → [102%@12f] → [100%@16f]   (pass scale as [130,130]/[100,100]/[102,102] — NOT 1.3)
         applies easeOut on KF1→KF2 (smash), easeInOut KF2→KF3→KF4 (micro-bounce)
  Opacity: [0%@0f] → [100%@4f]                   ease: linear OK (opacity fade — see rule 1 exception)
Duration: 16f (0.53s)
```

### R3. Slide-In From Left
```
Layer: any
Properties:
  Position X: [-layer_width @0f] → [target_x @18f]   ease: easeOut 80
  Opacity:    [0%@0f] → [100%@8f]                    ease: easeOut 70 (opacity fade — linear also OK)
Duration: 18f (0.6s)
```
`layer_width` = the layer's width (from `ae_get_layer_info`) so it starts fully off the left edge; `target_x` = its final on-screen X (the layout X you measured, or its current X). Pass the resolved numbers as the X in the `[x, y]` position TUPLE.

### R4. Typewriter Reveal
```
Use ae_create_text_animator. Signature:
  ae_create_text_animator({ compositionName, layerName, animatorType, duration=1.5 })
animatorType is an enum — exactly one of:
  typewriter | fadeInChars | scaleInChars | slideInChars | randomize | wave
For a typewriter, pass animatorType: "typewriter". duration is in SECONDS (default 1.5);
size it to the text — e.g. char_count × 2 frames at 30fps converted to seconds
(20 chars → ~1.3s). There is NO startValue / rangeSelector / delay param — do not invent them.
After typing finishes, add a blinking caret = separate shape layer with opacity expression:
  opacity = (time * 2) % 1 < 0.5 ? 100 : 0
```

### R5. Logo Reveal (3-phase: anticipation + action + settle)
```
Frames:
  0   - 4f:  Scale 90% → 92%        (anticipation, easeOut)
  4   - 16f: Scale 92% → 105%       (action, easeOut)
  16  - 24f: Scale 105% → 100%      (settle, easeInOut)
  0   - 8f:  Opacity 0 → 100        (fade)
Duration: 24f (0.8s)
Optional: add the glow effect (ae_apply_effect({ compositionName, layerName, effect: "glow" })
— "glow" is a registered friendly key, not "Glow"), then animate its "Glow Intensity" property
0 → 1.5 over frames 8-16 (effect property names are real case-sensitive AE strings passed via
ae_set_keyframe on the effect property; they are not MCP-introspectable — verify in AE).
```

### R6. Parallax Push (multi-layer depth)
```
BG layer:       Scale [100% → 105%] over comp duration, easeOut   (scale TUPLE [100,100]→[105,105])
MID layer:      Scale [100% → 110%] over comp duration, easeOut
FG layer:       Scale [100% → 120%] over comp duration, easeOut
+ Depth push: there is NO camera-layer tool — parent all layers to a Null and animate
  the Null's Scale [100,100] → [108,108] over duration (ease-out), or push each layer's Scale
  per-layer as above. (See R15 — add_camera_layer does NOT exist; use a Null.)
Creates depth-driven push without per-layer keyframes when driven from the Null.
```

### R7. Snap Rotate (90°/180° hard rotation)
```
Property: Rotation
  [0° @0f] → [+90° @6f]   ease: easeOut 95   (snap)
+ Optional after-bounce: add KF at 8f at +85°, then 10f at +90° (settle), easeInOut on settle.
Duration: 10f (0.33s)
```

### R8. Breathing Loop (subtle ambient)
```
Property: Scale
Expression (ae_set_expression on propertyName "Scale"):
  freq = 0.5;          // breaths per second
  amp = 1.5;           // % amplitude
  s = value[0] + Math.sin(time * Math.PI * 2 * freq) * amp;
  [s, s]
No keyframes needed. Loops forever.
```

### R9. Wiggle (organic instability)
```
Property: Position
Expression:
  wiggle(2, 8)         // 2Hz, 8px amplitude — subtle handheld
  wiggle(4, 20)        // jittery / nervous
  wiggle(0.5, 3)       // slow drift / atmospheric
For Rotation:
  wiggle(2, 2)         // 2° wobble
For Opacity (flicker):
  Math.random() > 0.95 ? 30 : 100  // rare flicker
```

### R10. Orbit (camera or layer around a point)
```
Property: Position
Expression:
  center = [960, 540];
  radius = 200;
  speed = 0.2;         // rev per second
  ang = time * Math.PI * 2 * speed;
  [center[0] + Math.cos(ang) * radius, center[1] + Math.sin(ang) * radius]
```

### R11. Glitch Stutter (1-2 frames every N seconds)
```
Property: Position
Expression:
  if (Math.random() > 0.985) {
    [value[0] + (Math.random()-0.5)*40, value[1] + (Math.random()-0.5)*10]
  } else value;
posterizeTime(15);   // chunky 15fps feel for glitch
```

### R12. Reveal With Mask (wipe-on)
```
Use shape layer or solid as mask source. Animate via Track Matte:
  - Place a white solid above the content layer (ae_add_solid_layer)
  - Set the content layer's track matte to the solid above with:
      ae_set_track_matte({ compositionName, layerName: "content", matteLayerName: "WhiteSolid", type: "alpha" })
    (type enum: "alpha" | "alphaInverted" | "luma" | "lumaInverted")
  - Animate the solid's Position X from off-screen → on-screen with a directional ease-out
    (ae_set_temporal_ease influenceOut: 80) — value is an [x, y] TUPLE
  - Layer is revealed left-to-right as the solid covers it
  Alternative: a mask on the layer (ae_add_mask) or an alpha precomp also works.
```

### R13. Counter (number animating up)
```
NOT applicable via MCP. ae_set_expression only accepts the 5 transform properties
(Position/Scale/Rotation/Opacity/Anchor Point) — it CANNOT target "Source Text", and there is
NO MCP tool that sets text content. A live numeric counter must be
authored DIRECTLY in the After Effects UI: create the text layer with ae_add_text_layer, then
in AE alt-click the Source Text stopwatch and paste this expression:
  target = 1234;
  startFrame = 0;
  endFrame = 60;
  t = clamp((timeToFrames(time) - startFrame) / (endFrame - startFrame), 0, 1);
  e = 1 - Math.pow(1 - t, 3);   // easeOut
  Math.round(target * e).toString();
What you CAN drive via MCP: animate the layer's Scale/Position/Opacity, or use
ae_create_text_animator for a per-character reveal (it animates characters, not the number).
```

### R14. Smash Cut (instant change with motion blur)
```
For a hard cut between two states:
  - Place both layers, the "after" layer starts after the cut frame
  - Enable motion blur with ae_set_motion_blur:
      ae_set_motion_blur({ compositionName, layerName: "incoming", enabled: true })   // per-layer
      ae_set_motion_blur({ compositionName, enabled: true })                          // omit layerName = comp switch
    (for a directional streak instead, apply the "directionalBlur" effect — ADBE Motion Blur — on the layer)
  - Animate Scale on incoming layer from [105,105] to [100,100] over 4 frames, ease-out (scale TUPLE)
  - Add a flash: white solid Opacity [0 → 100 → 0] over 2 frames at cut moment
```

### R15. Camera Push-In (cinematic)
```
There is NO camera-layer tool — add_camera_layer does NOT exist (CONFIRMED). Do NOT call it.
  Do the push-in with a Null instead:
    - Add a Null (ae_add_null_layer) and parent the content to it (ae_modify_layer parentLayerName)
    - Animate the Null's Scale for the push-in:
        ae_set_keyframe({ compositionName, layerName: "PushNull", propertyName: "Scale", time: 0,        value: [100, 100] })
        ae_set_keyframe({ compositionName, layerName: "PushNull", propertyName: "Scale", time: <dur>,    value: [120, 120] })  // scale TUPLE
      then ae_set_temporal_ease({ compositionName, layerName: "PushNull", propertyName: "Scale", influenceIn: 85, influenceOut: 85 })
    - For a positional drift instead/also, animate the Null's Position ([x, y] TUPLE) the same way.
Optional handheld feel: add a Position wiggle on the Null:
  ae_set_expression({ compositionName, layerName: "PushNull", propertyName: "Position", expression: "wiggle(0.5, 4)" })
```

### R16. Rotating Seal / Emblem / Circular-Text Badge (continuous spin)
```
A circular seal / emblem / round stamp-text badge is a LIVE accent — give it a slow CONTINUOUS
rotation (the ring turns forever), NOT the house-reveal-and-stop. Leaving it static reads as a
missed detail (the AE-Vibecode bundle always spins these).
Build it with the NATIVE tool: ae_add_text_on_path({ compositionName, text, radius, perpendicular:true,
spinSeconds:<sec/rev>, precompose:true }) — ONE editable text layer riding a circular mask (the whole
ring turns as a unit, text stays editable, spinSeconds bakes the rotation). Do NOT hand-build the
ellipse-mask / Path Options yourself and NEVER place it per-character. (If a seal already exists as a
single path-text layer, you can also just spin it via the Rotation expression below.)
Spin the Rotation (a transform prop → ae_set_expression IS allowed):
  ae_set_expression({ compositionName, layerName: "Seal", propertyName: "Rotation", expression: "time*12" })
    // ~12°/s ≈ one rev / 30s. Use 8–15°/s for a premium slow turn; negate ("time*-10") for CCW.
  Keyframed alternative (loop-safe): Rotation [0°@0s] → [360°@~15s], then wrap the last key with
    loopOut("cycle"). Rotation is scalar → ease with ae_apply_easy_ease, or leave linear for a
    constant-speed turn (a steady spin should NOT ease — linear is correct here).
Entrance: a quick Opacity fade-in is fine, but the spin runs continuously for the whole shot.
Match direction + speed to the reference.
```

---

## Kinetic typography recipe suite

Four canonical text-motion techniques. Most build on `ae_create_text_animator` (R4) or transform keyframes — remember `ae_set_expression` CANNOT touch `Source Text`, so per-word/number content must be authored in the AE UI (see R13).

**(1) TYPEWRITER — `20–50ms per char`.** Use `ae_create_text_animator({ animatorType: "typewriter", duration })`; size `duration` = `chars × (0.02–0.05)s`. At 30fps that's `0.6–1.5 frames/char` — e.g. 24 chars × 30ms ≈ 0.72s. Add the blinking caret per R4. Fast end of the range (20ms) feels like live terminal typing; slow (50ms) feels deliberate/dramatic.

**(2) MASK REVEAL — `300–600ms (9–18f) ease-out`.** Wipe the type on behind a moving matte (R12 mechanism): white solid track-matte over the text, animate the solid's Position from off → on over 9–18f with `ae_set_temporal_ease({ influenceOut: 75 })`. Reads as clean, premium, editorial. Pair the SPATIAL path straight (linear) for a hard architectural wipe.

**(3) SCALE POP — bounce + slight Y-offset (energetic).** `Scale [70,70]@0f → [105,105]@5f → [100,100]@8f` with the R2 micro-bounce ease, AND a tiny `Position Y` offset (`base_y + 6 → base_y` over the same 8f) so the word "drops" into place. The combined scale-up + small Y settle is what gives it punch — without the Y-offset it reads flat. Use the OVERSHOOT expression (amp small, freq 2, decay 4) for the settle.

**(4) AUDIO-SYNC — drive motion from a waveform.** Convert audio to keyframes (AE UI: *Keyframe Assistant → Convert Audio to Keyframes* creates an "Audio Amplitude" layer with a slider), then on a transform property:
```
ae_set_expression on "Scale":
  amp = thisComp.layer("Audio Amplitude").effect("Both Channels")("Slider");
  s = 100 + amp.valueAtTime(time) * 0.5;   // 0.5 = sensitivity
  [s, s]
```
Use `valueAtTime` to sample at the current time (or offset it to anticipate the beat). Sensitivity 0.3–0.8 for type that pulses to a track.

**Source-text driving patterns (author in AE UI — not via MCP):**
```
thisComp.layer("data").text.sourceText           // mirror another layer's text
"SCORE: " + Math.round(value)                     // string concatenation with a number
"LVL " + thisComp.layer("ctrl").effect("Level")("Slider").value.toFixed(0)   // slider binding
```

**Font guidance.** Geometric / grotesque sans animate CLEARLY at speed — **Futura, Montserrat, Bebas Neue** (also Helvetica/Inter): clean counters, even weight, legible in motion blur. AVOID decorative / script / high-contrast serif faces — fine strokes shimmer and disappear during fast moves. **Keep a kinetic-type reel under 3 minutes** — kinetic type is dense; past ~3min the audience fatigues and retention drops.

---

## loopOut() pattern — for any ambient loop

Apply via `ae_set_expression` on the `propertyName` you want to loop. The property must have ≥2 keyframes.

```
loopOut("cycle")     // default — restart from KF1 after last KF
loopOut("pingpong")  // ping-pong (use for breathing, oscillation)
loopOut("offset")    // each cycle continues from last value (use for continuous orbit)
loopOut("continue")  // extrapolates velocity from last two keyframes (use for infinite slide)
```

**Where to apply loopOut:**
- Rotation (continuous spin): `loopOut("offset")` with 2 keyframes 0° → 360° over the cycle period
- Position (orbit): `loopOut("cycle")` after one orbit cycle keyframed
- Opacity (flicker pattern): `loopOut("cycle")`
- Evolution (Fractal Noise): `loopOut("offset")` with kf 0 → 360 over loop duration → seamless

---

## posterizeTime() — for stepped / stylized motion

Apply at the start of any expression to lock animation to a slower framerate:

```
posterizeTime(12);
wiggle(8, 30)        // wiggle steps in chunks of 12fps — "stop-motion" feel
```

Use for:
- Stop-motion aesthetic
- Glitch (5-8fps)
- Toy/cardboard feel (15fps)
- Limited animation style (12fps)

---

## Scene-level animation choreography

For a multi-layer scene, sequence reveals **never simultaneously**:

```
Frame  0:  BG appears (instant cut, no fade — establishes the canvas)
Frame  4:  BG ambient motion starts (wiggle, parallax)
Frame  8:  ENV elements stagger in (grid, scanlines fade up over 16f)
Frame 20:  Hero CONTENT enters (smash zoom or fade-up, see R1/R2)
Frame 36:  Secondary CONTENT (subtitle, supporting elements)
Frame 50:  EFFECTS punch in (glow ramp up, sweep)
Frame 60:  GRADE settles (Curves/Vignette already applied, no animation needed)
Frame 60+: All loop expressions active, scene breathes forever
```

Stagger = 8-16 frames between layer reveals. Never reveal everything at frame 0.

---

## Stagger & offset timing patterns

For a GROUP of repeated elements (menu items, cards, list rows, grid cells, loader dots), compute each element's start from its index — never hand-place every keyframe.

**Formula:** `delay = startDelay + (elementIndex * staggerDuration)`

**Params:**
- `staggerDuration` = **50–100ms per element = ~1.5–3f @30fps** for menus/cards — this is the premium feel.
- **Avoid `> 150ms` (>4.5f)** per element — the cascade reads sluggish and the user waits.
- Keep the **total sequence < 2s** (60f) — for N elements, `staggerDuration ≤ 2000/N` ms. 12 cards → use ~80ms; 30 cells → drop to ~50ms or stagger by row/diagonal instead of per-cell.

**Three patterns:**
1. **Sequential** — `startDelay = 0`, each element offset by the increment: 0, 100ms, 200ms, … Standard top-down cascade. (At 30fps: keyframe element *i* to begin at `time = i * staggerDuration`.)
2. **Negative start (seamless loops)** — set `startDelay = -totalDuration` so the cycle BEGINS mid-animation with no dead wait at the front of a loop. Eliminates the empty first cycle on `loopOut` ambient groups.
3. **From-origin (directional cascade)** — order `elementIndex` by distance from a chosen origin (**first / center / last**) instead of DOM/layer order, so the wave radiates from that point — center-out, edges-in, or last-first for a reverse sweep.

**Worked example — 3-dot loader:** 3 dots, `staggerDuration = 200ms`, total `600ms` (each dot does one 600ms pulse cycle). Dot *i* delay = `startDelay + i*200ms`. Set `startDelay = -600` (= one full cycle negative) so when the loop starts the animation is already mid-flight — no dead beat, the three dots are immediately phase-offset and the loader reads alive from frame 0. With `loopOut("cycle")` on each dot's Scale/Opacity, this runs forever, seamlessly.

---

## Motion taste — orchestration, reveal grammar, review beats

**Per-property orchestration — choose HOW properties coordinate, not just each curve:**
- **Locked** (all properties start/end together) — UI panels, buttons, mechanical/synced state.
- **Lead/follow** — one property leads by a few frames, others follow — logo/hero/organic motion.
- **Primary/secondary** — one property carries the move, others support subtly.
- **Early-opacity / late-settle** — opacity resolves fast while position/scale keeps settling (readability).
- **Single-property overshoot** — only Scale (or Rotation) overshoots; Position stays controlled.
Hierarchy rule: only the FOCAL element gets the strongest personality (pop/overshoot/snap);
support gets quiet settles; accents never steal the read.

**Timing defaults by deliverable (convert to your fps):** UI microinteraction 0.2–0.5s ·
state/feedback icon 0.5–1.25s (+ short hold) · logo mark 0.75–2s · lower third in 0.75–1.5s,
out 0.5–1s · typography reveal 0.75–2.5s · one promo message 1.5–3s · loops 1–2s seamless.

**Reveal grammar:** default spine = **build → settle → hold** (the hold is where the message
registers). Reveal in reading/importance order — hero lands first, labels/stats/metadata after.
Prefer mask-wipes, draw-ons (trim/stroke), marker sweeps and purposeful cuts over uniform
opacity fades for premium scenes. **One main flourish per beat** — several competing reveals
in one beat destroy hierarchy.

**Typography choreography:** treat kinetic type as PHRASE performance, not uniform entrances —
assign anchor / support / **active word**; the active word carries the strongest motion; offset
each word's properties so words relate to the phrase; preserve reading order. Reject motion
where every word shares identical entrance timing (unless a minimal reveal is the brief).

**Data & figure motion:** animate data by its own logic — bars grow from the baseline, lines
draw left→right, rings sweep, dots populate; count-ups near-linear with an ease-out landing;
labels/units arrive AFTER the number resolves and sync to the geometry (a point label lands as
the line reaches it). Serious data = calm ease-out, no bounce.

**Camera:** ONE dominant camera move per scene (push / pull / pan / follow / parallax); camera
easing always SMOOTHER than the objects inside; never a pan/zoom that makes text unreadable.

**Motion economy:** motion must reinforce the same hierarchy as the final frame. Animate fewer
properties when it reads clearer; stillness gives motion contrast. If the scene feels busy —
simplify the LAYOUT first; effects/camera/stagger never compensate for weak composition.

**Final review beats (scrub, don't trust endpoints):** inspect frame 0 · first meaningful beat ·
midpoint · settle start · final frame · loop seam · every semantic beat (number resolves, word
lands, logo locks, CTA appears). Checks: the MIDPOINT must communicate what's happening (not
just transition blur); the FINAL settle must land in the strongest composition (not merely stop);
the last 10–20% of motion must feel intentional, not numerical drift; loop seams invisible
unless a reset is deliberate.

---

## Don'ts

- Don't keyframe at frame 0 AND have the layer enter from offscreen — pick one entrance style.
- Don't animate Opacity AND Position to enter simultaneously without offset (do Position 0-12f, Opacity 0-6f, so opacity finishes mid-slide for natural rhythm).
- Don't use linear easing on hero motion.
- Don't animate Scale and Opacity to enter and Rotation and Position simultaneously — too busy.
- Don't forget loopOut for ambient elements — static layers in a "looping" scene break immersion.
- Don't end an animation on the same frame everything starts — stagger exits too.
- Don't use wiggle(20, 50) — too violent. Default to wiggle(2, 8) and increase only if intent is glitch/distress.

---

## Ported bundle recipes — copy-ready ExtendScript (run via `execute_script`)

These are the AE-Vibecode bundle's signature motion helpers, verbatim. Where a recipe maps to a
transform property, the **`ae_set_expression` path** is preferred (pulseLoop, addOvershoot); the
Trim-Path / Slider / Source-Text ones (drawOn, progressRing, countUp) have **no atomic-tool
equivalent**, so run them through `execute_script`. They all assume the shared `easeIO` helper.

```jsx
// SHARED easing — converts every key to BEZIER + a settle-weighted temporal ease (in 22 / out 75),
// matching ae-animation-principles (module: reveal-motion)'s easeIO. (Flat 33/33 reads mechanical — see line 62 — so it is NOT used here.)
// Treats spatial Position/Anchor as dim 1 on purpose (a 2-elem ease array throws → caught →
// Position stays linear-spatial); do NOT "fix" that. countUp/drawOn/progressRing/shimmer call it.
function easeIO(prop){ if(!prop||!prop.numKeys)return; var dim=1; try{ var T=PropertyValueType; if(prop.propertyValueType===T.TwoD||prop.propertyValueType===T.ThreeD){ var v=prop.value; if(v&&typeof v.length==="number")dim=v.length; } }catch(e){} for(var k=1;k<=prop.numKeys;k++){ var skip=false; try{ skip=(prop.keyInInterpolationType(k)===KeyframeInterpolationType.BEZIER && prop.keyOutInterpolationType(k)===KeyframeInterpolationType.BEZIER); }catch(e){ skip=false; } if(!skip){ try{prop.setInterpolationTypeAtKey(k,KeyframeInterpolationType.BEZIER,KeyframeInterpolationType.BEZIER);}catch(e){} } var a=[],b=[]; for(var d=0;d<dim;d++){a.push(new KeyframeEase(0,22));b.push(new KeyframeEase(0,75));} try{prop.setTemporalEaseAtKey(k,a,b);}catch(e){} } }

// (1) COUNTER — keyframe a Slider 0→target (eased), expression only FORMATS digits.
// writes a LIVE Source Text expression — the bundle's own rule bans Source-Text expressions
// (AE-2026 crash vector). SAFER default: keyframe the Slider and bake the formatted text per beat
// (Hold keys on Source Text) instead of the live expression. Use this for dashboard metrics.
function countUp(textLayer,t0,dur,target,opts){ opts=opts||{}; var dec=opts.decimals||0,pre=opts.prefix||"",suf=opts.suffix||""; var grp=(opts.thousands!==false); var fx=textLayer.property("ADBE Effect Parade").addProperty("ADBE Slider Control"); fx.name="Count"; var s=fx.property("ADBE Slider Control-0001"); s.setValueAtTime(t0,0); s.setValueAtTime(t0+dur,target); easeIO(s); var e='var v=effect("Count")("Slider"); var dec='+dec+';\nvar n=(dec>0)? v.toFixed(dec) : Math.round(v).toString();\n'; if(grp){ e+='var pa=n.split("."), ip=pa[0], o="";\nfor(var i=0;i<ip.length;i++){ if(i>0 && (ip.length-i)%3===0) o+=","; o+=ip.charAt(i); }\nn=o+(pa[1]?("."+pa[1]):"");\n'; } e+='"'+pre+'"+n+"'+suf+'";'; textLayer.property("Source Text").expression=e; }

// (2) DRAW-ON — a stroked shape draws itself 0→full (line icons, underlines, connectors). Needs a STROKE.
function drawOn(shapeLayer,t0,dur){ var c=shapeLayer.property("ADBE Root Vectors Group"); var tp=c.addProperty("ADBE Vector Filter - Trim"); var end=tp.property("ADBE Vector Trim End"); end.setValueAtTime(t0,0); end.setValueAtTime(t0+dur,100); easeIO(end); }

// (3) PROGRESS RING — an ellipse STROKE (no fill) fills 0→pct, starting at 12 o'clock.
function progressRing(shapeLayer,t0,dur,pct){ pct=(pct==null?100:pct); var c=shapeLayer.property("ADBE Root Vectors Group"); var tp=c.addProperty("ADBE Vector Filter - Trim"); var end=tp.property("ADBE Vector Trim End"); end.setValueAtTime(t0,0); end.setValueAtTime(t0+dur,pct); easeIO(end); try{ tp.property("ADBE Vector Trim Offset").setValue(-90); }catch(e){} }

// (4) SHIMMER — a light band (tall thin solid ~18°, opacity ~35) sweeps across; one keyed sweep + loopOut.
function shimmer(bandLayer,x0,x1,y,dur){ var P=bandLayer.property("Transform").property("Position"); P.setValueAtTime(0,[x0,y]); P.setValueAtTime(dur,[x1,y]); easeIO(P); P.expression='loopOut("cycle")'; }

// (5) PULSE — scale breathes forever (live dots, badges). ae_set_expression equivalent: put this
//     expression string on "Scale" via ae_set_expression (no execute_script needed).
function pulseLoop(layer,minS,maxS,period){ minS=(minS==null?96:minS); maxS=(maxS==null?108:maxS); period=(period==null?1.2:period); layer.property("Transform").property("Scale").expression='p='+period+'; lo='+minS+'; hi='+maxS+';\nm=(lo+(hi-lo)*(0.5+0.5*Math.sin(time/p*2*Math.PI)))/100;\nvar r=[]; for(var i=0;i<value.length;i++) r[i]=value[i]*m; r;'; }

// easeSnap — SYMMETRIC snap KeyframeEase(0,85) (premium keynote feel). Call after setting keys.
//   For smooth camera/opacity. Do NOT also addOvershoot on the same property.
function easeSnap(prop){ try{ if(!prop||prop.numKeys<2)return; var apple=new KeyframeEase(0,85); var dim=1; try{ var v=prop.value; if(v&&typeof v.length==="number")dim=v.length; }catch(_){} for(var k=1;k<=prop.numKeys;k++){ var inE=[],outE=[]; for(var d=0;d<dim;d++){inE.push(apple);outE.push(apple);} try{ prop.setTemporalEaseAtKey(k,inE,outE); }catch(e){ for(var dd=1;dd<=3;dd++){ if(dd===dim)continue; var i2=[],o2=[]; for(var dx=0;dx<dd;dx++){i2.push(apple);o2.push(apple);} try{ prop.setTemporalEaseAtKey(k,i2,o2); break; }catch(_){} } } } }catch(e){} }

// addOvershoot — playful ELASTIC pop on Scale/Position (card drop-in, badge bounce, name-plate).
//   ae_set_expression equivalent: assign the expression below to Scale/Position. Keys must already exist.
//   Do NOT also easeSnap the same property (this overwrites .expression).
function addOvershoot(prop,amp,freq,decay){ try{ amp=amp||0.10; freq=freq||2.6; decay=decay||5.5; prop.expression="amp="+amp+"; freq="+freq+"; decay="+decay+";\nn=0; if(numKeys>0){ n=nearestKey(time).index; if(key(n).time>time) n--; }\nif(n>0 && n===numKeys){ t=time-key(n).time; v=velocityAtTime(key(n).time-thisComp.frameDuration/8);\n  value + v*(amp*Math.sin(freq*t*2*Math.PI)/Math.exp(decay*t)); } else { value; }"; }catch(e){} }
```

**When to reach for each (match the ref, don't add what isn't there):** countUp → counting stat/metric; drawOn → line icon / underline / connector draws in; progressRing → circular gauge/percentage; shimmer → skeleton-loader / placeholder; pulseLoop → live dot / badge / recording indicator; addOvershoot → tactile pop on a drop-in/bounce; easeSnap → smooth camera/opacity snap.
