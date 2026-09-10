# Video Motion Graphics

Apply the 12 Principles of Animation to After Effects, Premiere Pro, and video motion design, with a focus on broadcast/video delivery (framerate standards, motion blur, safe areas, export).

Assumes a direct AE ExtendScript / Premiere context — the techniques below are expression strings and keyframe workflows, not `ae_*` tool calls.

> **Premiere Pro note:** Premiere has no expression engine, so the expression recipes here (Overshoot, Stagger, `wiggle`, `loopOut`, etc.) are **After Effects-only**. In Premiere, reproduce the same feel with keyframe interpolation — Ease In/Out, Temporal/Spatial interpolation, and the velocity graph — not expressions. The principles, timing ranges, and export/safe-area guidance still apply in both apps.

**Related skills (differentiate, don't merge):**
- **`ae-animation-principles`** — the canonical timing tables (exact frames at 30fps), `set_temporal_ease` curve values, and the recipe library for animating *via the ae-mcp tools*. Use it when driving After Effects through MCP. This skill instead frames the same principles as raw ExtendScript and adds the broadcast/Premiere/export layer.
- **`ae-animation-principles (module: principles-expressions)`** — general After Effects authoring/setup. This skill is the motion-graphics craft layer (the 12 principles + delivery), not the app-setup layer.

## Quick Reference

| Principle | Motion Graphics Implementation |
|-----------|-------------------------------|
| Squash & Stretch | Overshoot expressions, elastic motion |
| Anticipation | Pre-movement, wind-up keyframes |
| Staging | Composition, depth, focus pulls |
| Straight Ahead / Pose to Pose | Frame-by-frame vs keyframe animation |
| Follow Through / Overlapping | Delayed layers, expression lag |
| Slow In / Slow Out | Graph editor curves, easing |
| Arc | Motion paths, rotation follows path |
| Secondary Action | Environment response, particle systems |
| Timing | 24/30/60fps considerations |
| Exaggeration | Scale beyond reality, dramatic motion |
| Solid Drawing | Z-space, 3D consistency, parallax |
| Appeal | Smooth, professional, emotionally resonant |

## Principle Applications

**Squash & Stretch**: Use scale property with different X/Y values. Overshoot expressions create elastic motion. Shape layers deform more naturally than pre-comps for organic squash.

**Anticipation**: Add 2-4 frames of reverse motion before primary action. Wind-up for reveals—slight scale down before scale up. Position anticipation: move opposite direction first.

**Staging**: Use depth of field to direct focus. Vignettes frame important content. Motion blur on secondary elements. Composition leads eye to focal point.

**Straight Ahead vs Pose to Pose**: Traditional frame-by-frame for character animation. Keyframe-based for graphic animation. Most motion graphics are pose-to-pose with expression refinement.

**Follow Through & Overlapping**: Use `valueAtTime()` expressions for lag. Stagger layer animation with offset. Secondary elements continue 4-8 frames past primary stop. Parent/child relationships with delayed response.

**Slow In / Slow Out**: Master the Graph Editor—never use linear keyframes. Easy Ease is starting point, customize curves. Bezier handles control acceleration. Speed graph shows velocity.

**Arc**: Enable motion path editing. Auto-orient rotation to path. Add roving keyframes for smooth arcs. Natural motion rarely travels in straight lines.

**Secondary Action**: Particles respond to primary motion. Shadows and reflections follow. Background elements shift with parallax. Audio waveforms drive visual elements.

**Timing**: 24fps: Cinematic feel, motion blur essential. 30fps: Broadcast standard, smoother. 60fps: Digital-first, very smooth. Hold frames (2s, 3s) for stylized timing.

**Exaggeration**: Motion graphics can push further than reality — but in THIS house style, keep it SUBTLE. A tactile entrance overshoot is **~+2–8%** (e.g. scale settles 100→104→100), NOT 120–150% (that cartoonish bounce is banned for text/chrome — see ae-animation-principles / ae-animation-principles (module: reveal-motion)). Rotation may extend slightly past final; color/effects can punctuate. Reserve big scale moves for a deliberate hero beat, never as the default overshoot.

**Solid Drawing**: 3D layers maintain spatial consistency. Parallax creates depth hierarchy. Consistent light direction across elements. Z-positioning creates believable space.

**Appeal**: Smooth interpolation, no jarring cuts. Color grading unifies composition. Typography has weight and personality. Motion feels intentional and professional.

## After Effects Techniques

### Overshoot Expression
```javascript
// Elastic overshoot. Via MCP (ae_set_expression) apply to a TRANSFORM property ONLY
// (Position/Scale/Rotation/Opacity/Anchor Point) — Source Text & effect props can't be
// set via MCP. Pasting directly in the AE UI has no such limit.
freq = 3;     // oscillation frequency (Hz): how many bounces per second. Safe range ~1-6.
              //   lower = slow, weighty wobble; higher = tighter, springier ring.
decay = 5;    // decay rate: how fast the oscillation dies out. Safe range ~2-12.
              //   lower = lingers/bouncier; higher = settles fast (snappy, almost critically damped).
n = 0;
if (numKeys > 0) {
    n = nearestKey(time).index;
    if (key(n).time > time) n--;
}
if (n > 0) {
    t = time - key(n).time;
    amp = velocityAtTime(key(n).time - .001);
    w = freq * Math.PI * 2;
    value + amp * (Math.sin(t * w) / Math.exp(decay * t) / w);
} else {
    value;
}
```

> `nearestKey()`, `key()`, `numKeys`, and `velocityAtTime()` are **standard, valid After Effects expression methods** evaluated by AE's own expression engine — they are not unsafe code. The only prerequisite is that the property already exists and has keyframes (the `numKeys > 0` guard handles the no-keyframe case). When automating, set this whole block as an **expression string** on the property (e.g. via `ae_set_expression`, or by pasting into the AE expression field directly) — note `ae_set_expression` accepts **only the 5 transform properties** (Position/Scale/Rotation/Opacity/Anchor Point); for Source Text or an effect property, paste it in the AE UI instead. It reacts to the velocity going into the last keyframe, so it needs at least one keyframe to overshoot from.

### Stagger Expression
```javascript
// Apply delay based on layer index
delay = 0.1;
d = delay * (index - 1);
time - d;
```

## Timing Reference

Quick broadcast/video defaults below. **These are rough ranges for motion-graphics delivery; the canonical, exact 30fps timing tables and `set_temporal_ease` curve values live in `ae-animation-principles`.** If a value here differs from that skill, prefer `ae-animation-principles` as the source of truth — these durations assume 30fps and should be rescaled for 24/60fps (see Timing principle above).

| Element | Duration | Easing |
|---------|----------|--------|
| Text reveal | 15-25 frames | Ease out |
| Logo animation | 30-60 frames | Custom curve |
| Transition | 10-20 frames | Ease in-out |
| Lower third in | 12-18 frames | Ease out |
| Lower third out | 8-12 frames | Ease in |

## Export Considerations

- Preview at final framerate
- Enable motion blur for fast motion
- Check timing at 1x speed, not RAM preview
- Account for broadcast safe areas
- Test on target display format
