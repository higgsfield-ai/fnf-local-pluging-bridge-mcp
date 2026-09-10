---
description: |
  Drives Adobe After Effects through the Adobe connector (server
  "adobe_creativeapps"; tools called via custom_mcp(action="call",
  server="adobe_creativeapps", tool="ae_<name>", args={…})): building comps and
  editable layers, reconstructing a reference, typography, gradients and native
  effects, motion and easing, controlled rigs, generated media, audits and
  delivery. The live After Effects session is the only place work counts — a
  described frame is not a deliverable.
  Load `ae-clean-rig` — that ONE skill, and nothing else ahead of it. It is the
  core procedure and router, and the only skill here that carries a trigger: the
  start-of-task checks, the construction and motion-fidelity doctrine (simplest
  representation that preserves the design, semantic precomps and exposed
  controls, motion only where the reference shows it, sparse intentional keys),
  its own ten reference modules, and the table naming any further module a
  request reaches.
  Beyond it, load ONLY what its table names for the request at hand. Modules are
  normative, not advisory: an order, gate or convention inside one binds like a
  rule, and where a module contradicts the router's doctrine the doctrine wins.
  BUILDING NATIVELY WITH THE ATOMIC ae_* TOOLS IS THE DEFAULT for any frame,
  layout, scene, UI, title card, lower third or dashboard — the server builds
  editable shape/text layers directly and needs no HTML detour. `ae-design-first`
  holds the optional one-call authoring routes (HTML, Lottie); neither is
  required and no build may be blocked on one.
  NOT for: AI text-to-video generation (use media/video-generation),
  Premiere-only edits, or web / CSS animation.
skills:
  - ae-clean-rig: The entry skill — core procedure, doctrine and router. Start-of-task checks, construction and editability rules, motion fidelity, and ten reference modules covering construction, reference motion, typography, gradients and effects, generated media, editable rigs, controlled sliders, characters, validation and delivery, and scripting reliability. Load this one; nothing routes ahead of it.
  - ae-animation-principles: Motion construction — 30fps timing tables, temporal-ease influence values, easing curves by motion type, staggers, the house entrance reveal, a pattern library and expression cookbook, and the 12 principles as AE expressions, delivery constraints and spec-writing concepts.
  - ae-ui-mastery: Design knowledge for a net-new frame with no reference — production design tokens, component anatomies with pixel specs, spacing/type/radius/shadow scales, grid and optical correction, colour harmony, typography pairing, hierarchy, and copy-ready layout patterns.
  - ae-design-first: Optional one-call authoring routes — a whole layout written as one HTML document, or a whole animated vector scene written as one Lottie JSON, built into editable AE layers in a single call. Not required; the native atomic build produces the same layers with no authoring detour.
  - ae-depth-space: 2.5D depth recipes for a server with no 3D layers and no camera — null-rig parallax ladders, displacement-map parallax budgets, exponential atmosphere, defocus maps, grounding shadows, perspective floors, and the flat-scene diagnostic list.
  - ae-liquid-glass: The Liquid Glass aesthetic as a parametric nine-layer rig of built-in effects — refraction, displacement ring, light-sweep rims, edge shine and darkness, frosted backdrop blur and tint — with exact values and single-null animation.
  - ae-transition-kit: Reusable video transitions and the house .mogrt library for Premiere — the two-placeholder comp template, the boundary-frame invariant, resolution-agnostic expressions, worked 3D builds, and the exposed-controls discipline.
---

# After Effects skills — index

Load `ae-clean-rig` — that one skill, and nothing else ahead of it. It is the
core procedure and router, and the only skill here that claims a trigger. Its own
ten reference modules come with it; beyond those it names the module(s) below,
and only what the request touches gets read. Modules are normative, not advisory.

`ae-mcp-realities` and `ae-build-orchestration` remain loadable by explicit name
but nothing routes to them.

- `ae-animation-principles` — timing, easing, staggers, entrances, expressions, the 12 principles.
- `ae-ui-mastery` — design tokens, component specs and layout patterns for net-new UI.
- `ae-design-first` — optional one-call HTML / Lottie authoring routes.
- `ae-depth-space` — 2.5D parallax, atmosphere, defocus and grounding.
- `ae-liquid-glass` — refractive frosted-glass rig.
- `ae-transition-kit` — transition template and `.mogrt` export discipline.
