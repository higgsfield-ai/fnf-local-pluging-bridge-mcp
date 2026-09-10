---
name: ae-build-orchestration
description: Plan and execute multi-step native After Effects builds with small verified batches, stable references, recoverable checkpoints and editable delivery.
---

# Build orchestration

Use the local `fnf-after-effects` MCP tools. Read `ae_catalog` for exact operation arguments before calling `ae_do`; availability depends on server policy and the installed AE version. Load `ae-clean-rig` as the shared construction and delivery standard. User instructions and existing project constraints take precedence over recipe defaults.

1. Inspect the existing project and collect dimensions, fps, duration, assets, fonts and the user's constraints. Classify work as new build, reference match or local correction; preserve unrelated content.
2. Make a scene plan: comp hierarchy, layer names, independent content sources, visual tokens, controllers and motion beats. Separate constant layout values from animated controls. Prefer the smallest useful rig.
3. Discover the categories needed for that plan. Read schemas before constructing calls; do not assume operation outputs can be interpolated into a later operation inside `batch.run`.
4. Create and verify one representative component first. Inspect native bounds and render the intended state before cloning a flawed pattern across a scene.
5. Build in dependency order: sources, component geometry, hierarchy, controls, expressions, keys, effects. Batch small coherent edits where the catalog supports it. Check each result, stop on failure and inspect partial work.
6. Animate shared components through parents/controllers. Test dependencies at zero, fractional, typical and extreme control values. Keep manual editing independent of optional demonstration playback.
7. Render representative frames at the real comp fps. Verify nested comps, alpha, fonts, edge clipping and motion seams. Save/package the requested deliverable with dependencies and state what was actually verified.

Choose native construction for text, logos with clean vector sources, simple UI and diagrams. Use supplied or explicitly generated media for photographs and footage. A screenshot is a visual reference, not a reason to create hundreds of tracing fragments. Match the largest geometry and rhythm before microdetails.

For a reference recreation, create an evidence list: viewport/crop, object bounds, typography, palette, motion start/stop times and stationary elements. Mark inferred details as inference. For a UI build, use `ae-ui-mastery`; for visual planning, use `ae-design-first`; for motion, use `ae-animation-principles`.
