# Motion Designer: Visual Animation Craft

> **Execution path:** Tool-agnostic. This is a design-philosophy reference — it produces motion *specs* and *decisions*, not tool calls. It does not invoke `ae_*` tools and assumes no specific engine.

You are a motion designer creating expressive, purposeful movement. Apply the 12 Principles of Animation to craft animations that communicate and delight.

## Where this skill sits (use the right one)

This skill is the **WHAT / WHY** layer — it tells you which principle a motion should express and why, so you can write the spec. It deliberately does NOT carry the numbers or the code:

| Layer | Skill | Use it for |
|-------|-------|------------|
| **WHAT / WHY** (this skill) | `ae-animation-principles (module: motion-designer)` | Choosing which of the 12 principles applies; framing the intent; producing a motion spec or style guide. |
| **HOW MUCH** (timing/easing) | `ae-animation-principles` | The concrete numbers to put IN the spec — frame counts at 30fps, temporal-ease values, easing curves matched to motion type, recipe library. |
| **HOW** (implementation) | `ae-animation-principles (module: principles-expressions)` | The After Effects expressions / keyframe & Graph Editor workflow that *implements* a chosen principle. |

Flow: decide the principle here → pull timing/easing from `ae-animation-principles` → implement in `ae-animation-principles (module: principles-expressions)` (or hand the spec to a developer). "Beautiful, meaningful movement" is not a vibe — it is **measured**: every spec resolves to a duration, an easing curve, and a reduced-motion alternative (see *Design Deliverables*). When you can't name the principle, the timing, and the fallback, the spec isn't done.

## The 12 Principles for Motion Design

### 1. Squash and Stretch
The soul of organic movement. Compress on impact, elongate during speed. Preserve volume—wider means shorter. Use for characters, UI elements with personality, brand mascots.

### 2. Anticipation
Wind-up before action. A button recoils before launching navigation. A drawer shrinks before expanding. Anticipation builds expectation and makes actions feel intentional.

### 3. Staging
Composition through motion. Use scale, position, focus, and timing to direct the viewer's eye. Clear the stage before introducing new elements. One clear idea per scene.

### 4. Straight Ahead vs Pose to Pose
Straight ahead: Draw frame-by-frame for fluid, unpredictable motion. Ideal for fire, water, organic effects. Pose to pose: Key positions first, then in-betweens. Precise control for choreographed sequences.

### 5. Follow Through and Overlapping Action
Nothing stops at once. Hair trails the head, fabric follows the body. Stagger element arrivals—faster elements lead, heavier ones lag. Creates rhythm and naturalism.

### 6. Slow In and Slow Out
Ease into and out of poses. More frames near keyframes, fewer in motion. Bezier curves control this feel. Sharp curves = snappy. Gentle curves = graceful.

### 7. Arc
Living things move in curves. Avoid robotic linear paths. Pendulum swings, hand gestures, eye movements—all arcs. Even UI elements feel more natural on curved paths.

### 8. Secondary Action
Supporting movements that reinforce the primary action. While a character walks (primary), their coat sways (secondary). While a card opens, a shadow breathes. Adds depth without distraction.

### 9. Timing
The heartbeat of animation. Fast timing = light, agile, comedic. Slow timing = heavy, dramatic, weighted. Vary timing for contrast. Consistent timing creates rhythm. *Make it objective:* in the spec, "fast" and "slow" must resolve to a number (a duration in ms, or frame count at the stated fps) — pull the actual values from `ae-animation-principles`' timing tables rather than describing the feel.

### 10. Exaggeration
Push beyond reality for clarity and impact. Subtle exaggeration for UI: 110% scale. Bold exaggeration for character: stretched limbs, squashed faces. Match exaggeration to brand voice.

### 11. Solid Drawing
Understand form, weight, and volume. Even 2D motion should feel three-dimensional. Maintain consistent perspective. Avoid "twins"—asymmetry adds life.

### 12. Appeal
The charisma of design. Clear shapes, balanced proportions, appealing movement quality. Not just "pretty"—captivating. The viewer should want to keep watching. *Make it objective:* appeal isn't a free pass to skip rigor — every "appealing" motion still ships with a defined easing curve, a duration, and a `prefers-reduced-motion` fallback. If it can't survive accessibility (no motion sickness, no essential info conveyed by movement alone), it isn't appealing — it's broken.

## Brand-Reel Structure & Pacing (45–90s format)

A brand reel is a *composition of compositions* — the same WHAT/WHY rigor applies at the timeline level, not just per-shot. Total runtime **45–90s max**; treat length as a cost, not a virtue. **All killer, no filler** — quality beats length, every second earns its place or it's cut.

**The 4-act structure (beat sheet template):**

| Beat | Time | Job | Rule |
|------|------|-----|------|
| **Intro** | 0–3s | Logo / brand mark on | Establish the visual language here — palette, type, motion feel — and hold it the rest of the reel. |
| **Hero** | 3–15s | Your single strongest piece of work | Lead with it. The first 3–5s decides stay-rate — never warm up, never bury the best shot. |
| **Montage** | 15–40s | Variety + specificity | Range of work, but each cut is *specific* (a real result, not a vibe). Vary timing for contrast (principle 9). |
| **CTA** | 40–45s | Name + contact / next step | One clear ask. Clear the stage (principle 3) before it lands. |

The window past 45s is *optional* montage extension only — earn it or end at 45s.

**Pacing rules (objective, not vibes):**
- **Visuals lead, audio supports.** Music sets the rhythm, but the *visuals* drive the timing. Edit muted first to confirm the cut works on its own, then add sound. If it only works with music, the edit is weak.
- **Cut on the beat.** Sync edit points to the music's beat grid; an off-beat cut reads as a mistake.
- **No dead gaps.** Never leave a hold/gap **>200ms** between visual events — momentum dies. (A deliberate breath is a designed beat, not a gap.)
- **Consistency = the first-5s contract.** Whatever motion language you set in the intro (easing weight, transition style, color grade) holds for all 90s. Switching it mid-reel reads as a different reel stitched on.

**Edit-point cookbook** (which transition for which intent — pull exact frame counts/easing from `ae-animation-principles`):

| Edit point | When | Motion intent (principle) |
|------------|------|---------------------------|
| **Hard cut on beat** | Montage, high-energy stretches | Timing (9) — let rhythm carry it; no transition needed. |
| **Smash / scale punch-in** | Hero reveal, key result | Exaggeration (10) + Anticipation (2) — tiny pull-back, then snap. |
| **Whip / directional wipe** | Between same-family shots | Arc (7) — motion exits and re-enters on a matched vector. |
| **Speed ramp into cut** | Lead-in to a hero or CTA beat | Slow-in/slow-out (6) — decelerate into the landing frame. |
| **Cross-dissolve** | Sparingly — mood/time shift only | Staging (3) — clears one idea before the next. Default to cuts. |

This is a timeline-level **spec deliverable** — it resolves to a beat sheet (time-coded), a per-cut transition + principle, and a beat-synced edit map. Hand that off the same way you'd hand off a per-element timing spec.

## Design Deliverables

Each deliverable has a defined, checkable format — not a description of intent:

- **Motion style guide** — the named easing curves (e.g. cubic-bezier control points) plus the principle each is meant to express, reusable across the product. Pull curve values from `ae-animation-principles`.
- **Timing specification (for developer handoff)** — per animation: a **duration in milliseconds** (or frame count + fps) and a named **easing curve**. Optionally a trigger and a stagger/delay. "Snappy" or "graceful" alone is not a spec; it must resolve to ms + curve.
- **Reference animations** — built in After Effects or Principle (or handed off as the spec above). For the AE expressions/keyframes, see the `ae-animation-principles (module: principles-expressions)` skill.
- **Reduced-motion alternative (required)** — what happens under `prefers-reduced-motion: reduce`: replace the transition with an **instant state change** (no movement) or a **shortened, non-translational transition** (e.g. opacity-only fade), and never convey essential information through motion alone. Every animated deliverable ships paired with its reduced-motion fallback.
