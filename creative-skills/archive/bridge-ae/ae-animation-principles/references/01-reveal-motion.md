# AE Reveal Motion — the house entrance recipe

**Execution path:** this is a pure-ExtendScript recipe — paste/run the functions below in a direct
AE ExtendScript context (`layer.property(...)`, `setValueAtTime`, `setTemporalEaseAtKey`). It does
NOT call `ae_*` tools. To reproduce the same reveal via ae-mcp instead, set each key
with `ae_set_keyframe` (compositionName, layerName, propertyName, time, value) and
apply a **settle-weighted** bezier with `ae_set_temporal_ease`: leave the START key
with pace (influenceOut≈22) and arrive SOFT at the rest key (influenceIn≈75) — plain 33/33 reads
mechanical. See the timing tables and easing values in this skill.

**Reference frame rate: 30 fps.** All timing values below (0.15 s stagger, 0.21 s / 0.33 s opacity
times, the 0.70 s window) were authored against a 30 fps comp — the author's "0.15 s ≈ 4–5 frames"
note only holds at 30 fps (0.15 × 30 ≈ 4.5). At other rates, keep the SECONDS values (they are
fps-independent); do NOT re-derive them from frame counts.

Extracted verbatim from the user's hand-keyed `Heart Rate` layer in the `Fitness Dashboard` comp
(read via ae-mcp). This is the interpolation + keying the user explicitly approved. Use it as the
DEFAULT for everything that enters frame. **The ground-truth values are already inlined in the
table below, so the `Fitness Dashboard` source comp is NOT needed to apply this recipe** — it is
cited only for provenance.

## The exact ground-truth (what the user set)

`Heart Rate` card layer, on entrance:

| Property | Key 1 | Key 2 | Interp |
|----------|-------|-------|--------|
| Position | t=0.15s → y = baseY **+42** | t=0.73s → y = **baseY** | BEZIER (Easy Ease) |
| Scale    | t=0.15s → **95 %**         | t=0.73s → **100 %**     | BEZIER (Easy Ease) |
| Opacity  | t=0.33s → **0**            | t=0.43s → **100**       | BEZIER (Easy Ease) |

Neighbouring card `Step Distance` starts at t=0.30 (vs 0.15) → **stagger ≈ 0.15 s (~4–5 frames)**.
Every keyframe is `KeyframeInterpolationType.BEZIER` with a **settle-weighted** temporal ease
(leave the start key with pace ~22 % out, arrive soft at the rest key ~75 % in; plain 33/33 reads
mechanical). NO linear keys. NO hold. Spatial props (Position) take a **length-1** ease array —
never length-3 (that throws and silently leaves Position LINEAR — the "crude motion" bug).

## The recipe (normalised, per element, local entrance time `t0`)

**MANDATORY (the reveal "shape" — do not change these):**

1. **Scale** — start at **95 %**, settle to **100 %**. `t0 → t0 + 0.70 s` window. Easy Ease.
2. **Opacity** — **0 → 100**, fast (≈0.12 s), starting **0.21 s AFTER `t0`** (so it fades in while
   the element is already lifting/scaling — never a hard pop). Easy Ease. In code this is
   `t0 + 0.21` → `t0 + 0.33`; treat **0.21 s as the authoritative offset** (an earlier draft said
   "~0.18 s" — that was prose rounding; the code value wins).
3. **BEZIER interpolation on every key, settle-weighted `in22/out75`** — pace OUT of the start key
   (`influenceOut ≈ 22`), arrive SOFT at the rest key (`influenceIn ≈ 75`). Flat 33/33 reads
   mechanical. NO linear, NO hold.

**OPTIONAL / scalable to the element:**

4. **Position rise** — start **+42 px BELOW** final, settle to final, same `t0 → t0 + 0.70 s`
   window, Easy Ease. The **+42 px is a default, not sacred**: scale the rise to element size if
   needed (≈ 6–10 % of element height). The rise may even be dropped for elements where a lift
   reads wrong — but keep scale 95 %→100 % and the fast fade, which are the mandatory core.
5. **Stagger** — successive elements start **+0.15 s** apart (`t0 = start + i * 0.15`). Tune within
   0.12–0.18 s for the beat; this is a feel knob, not a fixed value.

Feel: a soft "lift, grow a touch, and fade up into place." Restrained and premium.

## Stagger formula & settlement phases (sequencing the whole entrance)

The stagger is a single linear formula — each element's local entrance time is:

```
t0 = startDelay + (elementIndex * staggerDuration)
```

- `staggerDuration` — **40–60 ms per child** (0.04–0.06 s) for tight UI groups (rows, list items,
  stat cells, icon clusters). This is the **fast micro-stagger** tier and the new default for
  same-group children. The house `0.15 s` value stays the default for **distinct cards/panels**
  that read as separate beats (e.g. `Heart Rate` → `Step Distance`) — pick the tier by grouping,
  not by habit.
- `startDelay` — when the group as a whole begins (usually `0` or a small lead-in).
- **Cap the whole sequence under 2 s.** With N children at 40–60 ms you have budget for the full
  per-element 0.70 s window plus the cascade; if `startDelay + (N-1)*staggerDuration + 0.70 ≥ 2 s`,
  shrink `staggerDuration` (toward 40 ms) before you stretch the window.

**Settlement-phase breakdown** (one element, from its own `t0`):

| Phase | Window (from element `t0`) | What happens |
|-------|----------------------------|--------------|
| Primary move | **0–400 ms** | the element's own rise + scale carry most of the distance |
| Child overlap | **30–60 ms stagger** | next child begins while the parent is still mid-move (the cascade) |
| Settle | ends **~600 ms total** | motion fully damped, element at rest — matches the 0.70 s house window |

So a clean group reads: primary element does its 0–400 ms move, children peel in on a 30–60 ms
stagger, and the whole thing is visually settled by ~600 ms — never a synchronized pop, never a
laggard tail past 2 s.

**Looping reveals — negative-start pattern.** For a reveal that must loop seamlessly, set
`startDelay = -totalDuration` so the first cycle's entrance is already mid-flight at `t=0` and the
sequence is settled when the loop seam arrives. Apply it to the group start (the `start` arg of
`staggerReveal`), not to individual `t0` math — the per-element offset still adds on top.

## Paste-ready ExtendScript (use these verbatim)

```javascript
// Easy Ease (BEZIER) on EVERY key of a property — the user's interpolation.
// CRITICAL: the temporal-ease array LENGTH is decided by propertyValueType, NOT value.length.
// Spatial props (Position = TwoD/ThreeD_SPATIAL), OneD and Color take a length-1 array;
// only NON-spatial multidim props (Scale, non-uniform) take length = dims. Passing a length-3
// array to Position THROWS → the catch swallows it → Position stays LINEAR (the "crude motion" bug).
function easeArity(prop) {
  try {
    var T = PropertyValueType;
    if (prop.propertyValueType === T.TwoD || prop.propertyValueType === T.ThreeD) {
      var v = prop.value; return (v && typeof v.length === "number") ? v.length : 1;
    }
  } catch (e) {}
  return 1; // OneD, Color, TwoD_SPATIAL, ThreeD_SPATIAL
}
// Premium settle profile: leave the first key with pace (out≈22), arrive soft at the last (in≈75).
function easeIO(prop) {
  if (!prop || !prop.numKeys) return;
  var arity = easeArity(prop), n = prop.numKeys;
  for (var k = 1; k <= n; k++) {
    try { prop.setInterpolationTypeAtKey(k, KeyframeInterpolationType.BEZIER, KeyframeInterpolationType.BEZIER); } catch (e) {}
    var inInf  = (k === 1) ? 0.1 : (k === n ? 75 : 60);
    var outInf = (k === n) ? 0.1 : (k === 1 ? 22 : 60);
    var ein = [], eout = [];
    for (var d = 0; d < arity; d++) { ein.push(new KeyframeEase(0, inInf)); eout.push(new KeyframeEase(0, outInf)); }
    try { prop.setTemporalEaseAtKey(k, ein, eout); } catch (e) {}
  }
}

// The house entrance: rise +42, scale 95→100, fast fade — Easy Ease, exactly like Heart Rate.
// Call AFTER the layer is positioned at its FINAL position/scale (it reads current value as target).
function revealRise(layer, t0, rise, dur) {
  rise = (rise == null ? 42 : rise);
  dur  = (dur  == null ? 0.70 : dur);
  var tr = layer.property("Transform");
  var P = tr.property("Position"), S = tr.property("Scale"), O = tr.property("Opacity");
  var pf = P.value, sf = S.value;
  var pStart = (pf.length > 2) ? [pf[0], pf[1] + rise, pf[2]] : [pf[0], pf[1] + rise];
  var sStart = (sf.length > 2) ? [sf[0]*0.95, sf[1]*0.95, sf[2]] : [sf[0]*0.95, sf[1]*0.95];
  P.setValueAtTime(t0, pStart);        P.setValueAtTime(t0 + dur, pf);
  S.setValueAtTime(t0, sStart);        S.setValueAtTime(t0 + dur, sf);
  O.setValueAtTime(t0 + 0.21, 0);      O.setValueAtTime(t0 + 0.33, 100);
  easeIO(P); easeIO(S); easeIO(O);
  layer.motionBlur = true;
}

// Stagger a set of layers (cards/rows/etc.) the way the dashboard does it.
function staggerReveal(layers, start, step, rise, dur) {
  start = (start == null ? 0.15 : start);
  step  = (step  == null ? 0.15 : step);
  for (var i = 0; i < layers.length; i++) revealRise(layers[i], start + i * step, rise, dur);
}
```

## Via ae-mcp — the same reveal as tool calls

The ExtendScript above is the direct-AE path. Through ae-mcp, `ae_apply_easy_ease` ERRORS on 2D Position, so ease Position/Scale with `ae_set_temporal_ease`:

```
// x / baseY = the element's FINAL position; comp at 30fps
ae_set_keyframe({ compositionName, layerName, propertyName: "Position", time: t0,        value: [x, baseY + 42] })
ae_set_keyframe({ compositionName, layerName, propertyName: "Position", time: t0 + 0.70, value: [x, baseY] })
ae_set_keyframe({ compositionName, layerName, propertyName: "Scale",    time: t0,        value: [95, 95] })
ae_set_keyframe({ compositionName, layerName, propertyName: "Scale",    time: t0 + 0.70, value: [100, 100] })
ae_set_keyframe({ compositionName, layerName, propertyName: "Opacity",  time: t0 + 0.21, value: 0 })
ae_set_keyframe({ compositionName, layerName, propertyName: "Opacity",  time: t0 + 0.33, value: 100 })
// settle-weighted bezier: pace OUT of the start key, arrive SOFT at the rest key
ae_set_temporal_ease({ compositionName, layerName, propertyName: "Position", keyIndex: 1, influenceIn: 1,  influenceOut: 22 })
ae_set_temporal_ease({ compositionName, layerName, propertyName: "Position", keyIndex: 2, influenceIn: 75, influenceOut: 1 })
ae_set_temporal_ease({ compositionName, layerName, propertyName: "Scale",    keyIndex: 1, influenceIn: 1,  influenceOut: 22 })
ae_set_temporal_ease({ compositionName, layerName, propertyName: "Scale",    keyIndex: 2, influenceIn: 75, influenceOut: 1 })
```
Stagger N elements by setting `t0 = start + i * 0.15`. (Opacity may keep a uniform ease.)

## Rules

- This is the DEFAULT entrance for EVERY element that appears — use it even when nothing specific
  is requested. Only deviate when the brief explicitly calls for a different motion (e.g. smash
  zoom, glitch, draw-on) — and even then, keep the **BEZIER Easy-Ease interpolation** (never linear).
- For an EXIT, mirror it: drop +42 / scale to 95 % / fade to 0 over ~0.4 s, Easy Ease.
- **Follow-through / overshoot is for PANELS and MODALS only** — a panel or modal entering may
  carry a tiny overshoot past its rest value before damping back. **Text and small chrome (icons,
  badges, labels, rows) get NONE** — they arrive on the plain settle-weighted ease and stop. Adding
  overshoot to small/text elements reads jittery, not premium; keep them on the in22/out75 settle.
- **Exception — a circular seal / emblem / round stamp-text badge does NOT reveal-and-stop:** it gets a
  slow CONTINUOUS rotation for the whole shot (the ring keeps turning). Fade it in, but spin it forever —
  see the "Rotating Seal" recipe (R16) in **ae-animation-principles**. Static seal = a missed detail.
- **Motion blur is PER-REVEALED-LAYER**, not comp-wide: `revealRise` sets `layer.motionBlur = true`
  on each layer it animates. For that per-layer flag to actually render, the comp's master
  "Enable Motion Blur" switch must also be on — so turn the comp switch ON once, then let each
  revealed layer opt in via its own flag (the recipe does this automatically). Do NOT force motion
  blur on every layer in the comp; only the revealed ones get it.
- When many elements share a beat, stagger by 0.12–0.18 s — never reveal them all on the same frame.
