---
name: ae-transition-kit
description: Reusable video transitions and the house .mogrt library for Premiere — the two-placeholder comp template, the boundary-frame invariant, resolution-agnostic expressions that hold at 16:9 and 9:16, worked 3D builds, and the exposed-controls discipline Essential Graphics export requires.
---

# AE Transition Kit — reusable seams (→ .mogrt library)

Premiere's native transition registry is unreliable on recent versions; the premium path is a
house library of AE-authored transitions exported as `.mogrt` (placed in Premiere via
`pr_import_mogrt` on the track above the seam). This skill is how those get BUILT.

## The transition comp template (start every build here)
- One comp, **duration 0.5-0.8s** (12-20 frames at 25/30fps) — transitions are seasoning, not scenes.
- **Two placeholders**: solid `OUT_PLATE` (what's leaving) and solid `IN_PLATE` (what's arriving),
  full-frame, bottom of the stack. Build all motion ABOVE/ON them; in Premiere the plates are
  replaced by (or revealed over) the real clips.
- **Resolution-agnostic by construction:** every position/size as an expression off
  `thisComp.width` / `thisComp.height` (e.g. anchor at `[thisComp.width/2, thisComp.height/2]`),
  never a baked pixel number — one build must work at 1920×1080 AND 1080×1920 (our vertical focus).
- **Boundary-frame invariant:** frame 0 = 100% outgoing plate, last frame = 100% incoming plate —
  no half-state at either end, or the seam pops in Premiere. Verify with `ae_export_frame` at
  first/last frame + `ae_audit_frame` if a reference exists.

## Exposed-controls discipline (what makes it a LIBRARY piece, not a one-off)
- **Parametrize, don't re-bake:** hero tweakables live as **Expression Controls on ONE `CTRL`
  null** — Slider for duration-scale/blur amount/direction, Color for accent tints. Layers
  reference the control via expressions; a style change = one value, zero re-building.
- **Cap at a handful (≤5)** with tasteful defaults — a wall of sliders is worse than none.
- These controls are exactly what gets dragged into **Essential Graphics** for `.mogrt` export —
  name them like a human ("Direction (deg)", "Accent"), they become the template's public UI.
- Give text params stable names across the whole library (one convention → `pr_import_mogrt`'s
  returned `textParams` are predictable for the agent driving them).

## Worked builds (all geometry from comp-relative expressions; cubic bezier ease per ae-animation-principles)
### Door open
Two full-frame layers, each masked to its half of the frame (left/right), **anchors at the OUTER
edges**, 3D on. Y-rotate each to ±90° across the comp — the frame "opens" revealing `IN_PLATE`
behind. Ease: slow-out heavy (doors accelerate); add a subtle exposure dip at the midpoint.

### Card / cube flip
`OUT_PLATE` and `IN_PLATE` as 3D layers parented to one rotating null at frame centre;
`IN_PLATE` pre-rotated 180° (back-to-back). Null Y-rotates 0→180° — out face leaves, in face
arrives. A ~10% scale dip at the mid-rotation sells perspective without a camera.

### Page peel
Use AE's native **CC Page Turn** on `OUT_PLATE` (fold position keyframed corner→opposite corner);
`IN_PLATE` below. Don't hand-build the curl from masks — the effect exists, spend the effort on
the ease and the drop shadow under the curl.

## When NOT to reach for this kit
- Most seams want a **hard cut** (see the Premiere seam grammar) — a 3D transition on every cut
  reads as a 2010 wedding video. One family per project (STYLE LOCK applies to motion too), used
  at chapter changes, not between every shot.
- A plain crossfade/dip need is cheaper served by the Premiere keyframe fallback family
  (premiere-editing-reference Recipe I) — no AE round-trip.
