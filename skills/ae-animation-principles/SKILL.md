---
name: ae-animation-principles
description: Design and refine intentional After Effects animation with timing, easing, staging, anticipation, follow-through and loop validation.
---

# Animation principles

Use the local `fnf-after-effects` MCP tools. Read `ae_catalog` for exact operation arguments before calling `ae_do`; availability depends on server policy and the installed AE version. Load `ae-clean-rig` as the shared construction and delivery standard. User instructions and existing project constraints take precedence over recipe defaults.

## Motion specification

Describe what moves, what stays still, when each beat starts, where it settles and why the viewer should notice it. Reference motion takes precedence over generic animation recipes. Do not add idle wobble, breathing or drift to stationary elements unless requested.

Measure timing in seconds and actual composition frames. At 30 fps, 2–4 frames can read as a snap, 4–6 as anticipation, 8–12 as a quick transition, 18–30 as a slower entrance, and 6–10 as settling. These are examples, not universal durations; adapt to distance, scale, style and readability. Keep holds long enough to read the real text.

Use sparse meaningful keyframes. Ease when the object accelerates or settles; preserve deliberate linear movement. Distinguish temporal interpolation from spatial path tangents. Discover keyframe and property operation schemas before setting them; influence ranges and property dimensions must match the native API.

Anticipation prepares the direction of an action. Overshoot and follow-through should share a physical logic and decay into a stable endpoint. Parent parts that belong to a shared gesture rather than giving each an unrelated clock. Use stagger for reading order without making the composition feel slow.

## Reveal and layout

Set an explicit hidden/offscreen state before delayed reveals so layers do not appear prematurely. Keep typography bounds, anchor points and masks stable during text changes. Use trim paths for a drawn line and native masks/mattes for a reveal where appropriate. Avoid stretching glyphs when the reference asks for rigid text motion.

## Expressions

Prefer native controls with clear units and defaults. Gate optional automatic motion so manual keys remain usable. Avoid unbounded time-driven randomness and magic references to unrelated comps. Expression APIs differ from ExtendScript; inspect expression errors after application. Use positive modulo for loops that permit negative control values: `((x % n) + n) % n` with `n > 0`.

## Proof

Check start, anticipation, fastest motion, overshoot, settle and last visible frame. For loops, compare the seam and its velocity; do not add a duplicate held endpoint accidentally. Verify motion blur at delivery settings. Render at actual timing, not only static keyframes. A sampled preview demonstrates only the tested intervals; do not claim the whole animation is verified from one still.
