---
name: ae-design-first
description: Plan After Effects scene geometry and typography before animation, translating visual references or approved designs into native editable components.
---

# Design first

Use the local `fnf-after-effects` MCP tools. Read `ae_catalog` for exact operation arguments before calling `ae_do`; availability depends on server policy and the installed AE version. Load `ae-clean-rig` as the shared construction and delivery standard. User instructions and existing project constraints take precedence over recipe defaults.

Resolve the static design before investing in detailed motion. Read the reference as geometry and hierarchy: output aspect ratio, safe areas, baseline grid, dominant blocks, text wrapping, contrast and layer order. Build a compact scene specification with named components, positions/sizes, typography, colors, media sources and controller intent.

Use this native pipeline: scene specification → catalog discovery → representative component → rendered still → component assembly → motion. An existing HTML preview may help inspect a design, but the local runtime does not provide the cloud bridge's HTML-to-AE scene converter. Do not claim pixel equivalence before comparing native output.

Build native text and shape layers through `ae_do`; inspect font availability, text bounds and nested coordinate spaces. Fix composition-level hierarchy before tiny decorative details. For reference matching, record the reference crop and sampled frame times so comparisons use the same view.

Lottie JSON and this runtime's project JSON are different formats. Never pass Lottie data to `ae_project_import_json`. An external converter requires its own tested adapter and fidelity checks for fonts, masks, mattes, gradients, effects and expressions. Preserve unsupported elements explicitly instead of silently flattening them.

Once the still is sound, load `ae-animation-principles` and animate only the intended elements. Render the native scene after animation changes; motion, masks and sourceRect-driven expressions can break a previously correct layout.
