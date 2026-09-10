---
name: ae-build-orchestration
description: Reference-match build procedure — measuring a reference into a fidelity passport of exact values, the per-element draw-versus-generate split, pixel-exact rebuilds of an opaque screenshot, style extraction into a visual passport, scene and camera direction, the hierarchy naming schema, and the numeric audit and finalize gates that close a build.
---

# AE Build Orchestration — the mandatory pipeline (follow IN ORDER)

This is the GLUE the individual AE skills assume but don't enforce. A reference-match or
whole-frame build **must** run these 5 phases in order. Don't jump to building. Don't eyeball.
Don't declare done without the audit. Every tool is invoked via the `custom_mcp` wrapper
(`custom_mcp(action="call", server="adobe_creativeapps", tool="ae_<name>", args={…})`; bare
`ae_<name>({…})` below is shorthand) — see **ae-mcp-realities** for the contract; load it first.

> **Gate rule:** each phase has an objective exit condition. Do NOT advance until it's met. The
> audit (Phase E) is a NUMERIC gate, not a vibe — "looks close" is not a pass.
>
> **Scope of the gates:** the GATES are mandatory, the ceremony is not. For a small build
> (a single card, one badge, a title) phases may be combined into fewer calls — measure and
> build in one pass is fine — as long as every gate is still checked (measured colours, editable
> layers, eased motion, passing audit, finalize). Skip a phase's *work* only when its gate is
> trivially already met, never skip the *check*.

---

## Phase A — MEASURE → write the Fidelity Passport (do this BEFORE any build)

Vision eyeballs pixels badly (coords ±4–8px, radii guessed, gradient stops wrong, fonts
misidentified). So **measure first, with a tool, and write the numbers down** — then build only
from those numbers.

1. If there's a reference image, **measure it with `ae_measure_reference`** (server-side Pillow).
   Mandatory minimum (batch the ops in one call):
   - `{op:"size"}` FIRST (ref pixel space → SCALE = comp_width / ref_width).
   - `{op:"swatch"|"pixel"}` for EVERY fill / stroke / text colour (returns `{r,g,b}` 0-1 — use it, never name a colour by eye).
   - `{op:"radius"}` for EVERY rounded surface.
   - `{op:"gradient", n:5}` for EVERY gradient (real stops + direction).
   - `{op:"fontsize"}` for title / body / caption tiers.
   - `{op:"crop", zoom:6}` + view the URL for any element < 40px (icons, badges, dense text) — never read a tiny element off the full image.
   **Reference has NO fetchable URL/key (chat-only image)?** `ae_measure_reference` can't run — take
   the passport from vision, SAY SO in the passport ("vision-derived"), rescale every coordinate by
   SCALE = comp_width / ref_width, and compensate at Phase E with the numeric SELF-audit of your own
   render (see Phase E). Do not silently skip measuring.
2. **Write the FIDELITY PASSPORT** — a structured list the build phase reads verbatim. One row per element:
   ```
   CANVAS:   ref WxH; comp WxH; SCALE
   PALETTE:  role → {r,g,b} (measured)
   E1  <name>  bbox [x,y,w,h]×SCALE  fill {r,g,b}  radius Npx×SCALE  font <PostScript> Npt  [DRAW|GEN]
   E2  …
   ```
   Mark each element **[DRAW]** (flat geometry/text → build) or **[GEN]** (detailed illustration /
   3D / map / gauge / character / textured art → generate-and-composite) — see **ae-build-orchestration (module: draw-vs-generate)**.
3. **Exit gate:** every element has measured numbers (not guesses) and a DRAW/GEN mark. If you
   used vision instead of `ae_measure_reference`, say so — eyeballed builds drift.

(Supporting skills: **ae-build-orchestration (module: visual-matcher)** for the style passport, **ae-build-orchestration (module: ui-rebuilder)** for the per-element measurement table.)

---

## Phase B — BUILD strictly from the passport

Build from the measured values **verbatim** — do NOT re-measure or re-guess mid-build.
- **DEFAULT — build natively with the atomic `ae_*` tools.** Create the comp and place every element
  from the passport as real shape/text layers. There is no HTML step in the default path and no build
  may be blocked on one. Follow **ae-clean-rig** for the construction rules the native path runs on:
  the simplest representation that preserves the design, semantic precomps, meaningful primitives
  instead of dense traced fragments, and native text for every word.
- **OPTIONAL accelerator — HTML:** a frame that is genuinely faster to express as one HTML mock may go
  through **ae-design-first** (`ae_build_scene_from_html`, `usePrecomps:true`), followed by a surgical AE
  pass (text restyle via `ae_style_text`, image swaps, elements HTML can't express). Choose it on speed
  for that specific frame, not by default; batch the atomic calls rather than routing through HTML merely
  to reduce round-trips.
- Pixel-exact opaque screenshot → **ae-build-orchestration (module: ui-rebuilder)** (atomic `ae_*`, measured coords → CENTER positions).
- Colours are `{r,g,b}` 0-1; positions are the layer CENTER; `propertyName` is the Capitalized enum (ae-mcp-realities).
- **Name the hierarchy on the way in (MANDATORY).** Use a depth-encoded schema so the agent can rediscover any comp/layer deterministically without folders, and the project auto-documents itself:
  - `# Main` = the root comp; `## Sequence` = a top-level act/section; `### Scene` = a beat inside a sequence. `#` count encodes depth.
  - `>` denotes a hierarchy/parent link (e.g. `> Card`), `()` adds clarification (e.g. `### Hero (above-fold)`), `//` prefixes a disabled/parked comp (e.g. `// ## Old Intro`).
  - Wildcard `> GlobalAsset` marks a reusable comp pulled into many places (logo, watermark, shared button). Name it once, reference it everywhere.
  - Apply names via **`ae_modify_layer`** (pass `newName`) / the comp name at create time; the scheme scales across projects and lets later phases find elements by name instead of by index. (There is no `ae_rename_layer` — renaming is `ae_modify_layer`.)
- **Exit gate:** the layer set matches the passport's element list (same count, same structure, no invented/missing elements) AND every comp/layer carries a schema name (`#`/`>` encoded, no `Layer 1` / `Comp 1` leftovers).

---

## Phase C — GENERATE only the [GEN] elements (then composite)

For elements marked [GEN], don't crudely fake them with shapes — generate and composite:
- **NO [CROP]:** never cut pieces out of the reference screenshot as assets (crop+inpaint+import) —
  the reference is for MEASURING, not harvesting; low-res crops turn to mush next to native layers
  and ship as dead non-editable blocks. Recreate ([DRAW]) or generate ([GEN]); cost-saving never
  justifies a worse frame (full rule: ae-build-orchestration (module: draw-vs-generate)).
- **STYLE LOCK (house rule — do this FIRST, before any generation):** write ONE style descriptor
  for the whole task — a single reusable sentence derived from the reference/passport covering
  render style (flat vector / 3D clay / photo / watercolour…), palette (key hexes), lighting,
  materials and background treatment. **PREPEND this SAME descriptor verbatim to EVERY
  `generate_*` prompt in the batch** — assets generated from different ad-hoc prompts come back
  in clashing styles and ruin the frame. An asset that returns off-style gets REGENERATED with
  the descriptor tightened — never composited "as is". This applies to every image generated for
  the task, reference-build or not.
- Generate via the **Higgsfield connector** (`generate_*`) with a **transparent-background, wordless**
  prompt that matches the reference's art direction (use the ref crop as a style reference) →
  `ae_import_image({ url })` → clip into its frame with a track matte (ae-mcp-realities §11).
- **CONTENT vs CHROME:** generate ONLY the detailed wordless object; BUILD the surrounding UI
  chrome and ALL text as real layers, so every element stays independently animatable. **Never**
  generate a whole card as one flat image (kills animation), and **never** generate text.
- **Hard cap ~4–6 generated assets** per frame; run them in parallel. (Full rules: **ae-build-orchestration (module: draw-vs-generate)**.)
- **Exit gate:** detailed objects look like the ref; text + chrome are editable layers.

---

## Phase D — MOTION (house reveal + premium easing + precompose)

- **A reference outranks the house defaults.** When a reference shows the motion, fit timing and curves to
  what it actually does (`ae-clean-rig`, module 02): an element the reference does not animate stays still,
  a hard cut stays a hard cut, and a measured bounce keeps its own amplitude and easing. The defaults below
  apply where nothing observed dictates the motion — a described frame, an element the reference never shows
  entering, or a brief with no reference at all.
- **Entrance = the house reveal by default** (**ae-animation-principles (module: reveal-motion)**): rise +42→0, scale 95→100%,
  fast fade, **staggered 0.12–0.18s**, never simultaneous — unless the brief asks for a specific beat or the
  reference shows the element already present.
- **Easing = settle-weighted, not flat** (**ae-animation-principles**): ease OUT of the start key,
  arrive SOFT at the rest key (≈22% out / 75% in), BEZIER on every key. Flat 33/33 reads mechanical.
  A curve fitted to a reference is finished work — do not normalize it back to the house profile.
- **Precompose semantic groups** (`usePrecomps:true` or `ae_precompose_layers`) so each card/section
  animates as a unit.
- **Small label-plates / badges / stat-pills / info-tags / PILL BUTTONS / CTAs do NOT auto-group — precompose them EXPLICITLY.**
  `usePrecomps` only wraps LARGE containers (a class-hinted element ≥200×120px with ≥3 child layers); a small
  labelled plate (bg + 1–2 text/icon layers) falls below that gate and is left as loose flat layers. After
  building each such plate, group its layers (bg shape + Gradient Ramp + the text + any icon) into their own
  precomp with **`ae_precompose_layers`** (pass all the plate's `layerNames`; `moveAttributes` is auto-forced
  for >1 layer) so the plate becomes one movable/animatable unit **with its text still editable inside**. Name
  it (`#`/`>` schema). **A 2-layer unit STILL gets precomposed** — e.g. a gradient **"Contact us" pill = a gradient
  shape + its text** → precompose it; "only 2 layers, not worth it" is NOT a valid skip. The only things left
  un-precomposed are genuinely standalone single layers (a lone bg, a lone heading). Don't ship labelled plates as a
  loose flat stack — and never as a generated image (that bakes the text; see ae-build-orchestration (module: draw-vs-generate)).
- **Precompose threshold (quantified).** If the main comp exceeds **~20 layers**, precompose **by function**
  (one precomp per card/panel/group) — flat 30+ layer comps are unmanageable and re-render the whole stack.
  While working a heavy precomp, set a **region of interest (ROI)** to shrink the rendered area so previews
  stay fast; clear it before the final audit render.
- **Render-order fix (effect-then-mask bug).** AE applies effects AFTER masks on the same layer, so a mask
  on an effected layer clips the *source*, not the effect output (glow/blur bleeds past the mask edge). Recipe:
  **precompose the set → apply the effect to the precomp layer → put the mask in the PARENT comp** (on the
  precomp layer there). The mask now clips the finished effect. Use this any time a glow/blur/ramp must be
  contained inside a rounded card or shaped frame.
- **Shape strategy — parametric vs Bezier (pick on purpose).** Parametric shapes (Rectangle/Ellipse with
  Size/Roundness params) **animate smoothly** — keyframe Size, Roundness, or path-trim cleanly. Bezier paths
  (converted, editable vertices) allow **per-point editing** for custom silhouettes but morph poorly. Default to
  parametric for anything that must animate (growing bars, expanding cards, morphing corners); only convert to
  Bezier when the shape needs hand-tuned points and won't be path-animated.
- **Exit gate:** every entering element is keyed + eased + staggered; nothing linear on spatial motion; comps
  over ~20 layers are precomposed by function; **every labelled small plate / badge / stat-pill is its own
  precomp (not loose flat layers), text editable inside**; any masked-effect element uses the parent-mask recipe.
- **Parametrize, don't re-bake:** values the user will predictably tweak (accent colour, duration scale,
  direction) live as Expression Controls on one CTRL null referenced by expressions — a style change is one
  value, not a rebuild. Cap at a handful; this is also exactly what Essential Graphics / `.mogrt` export
  needs (see ae-transition-kit for the library discipline).

---

## Phase E — AUDIT (numeric gate) → fix → re-audit

Don't ship on vibes. Close the loop:
1. `ae_audit_frame(compositionName, reference_url|reference_key)` at a non-zero time (after entrances settle). It scores ref↔render cell-by-cell in CIE-Lab.
   **No reference URL/key (e.g. the reference only exists as a chat image)?** Don't skip the gate —
   run the numeric SELF-audit instead: `ae_export_frame` → `ae_measure_reference` **on your own
   render's URL** with swatch/pixel/fontsize/gradient probes at the passport's key points, and
   compare every reading against the passport values. Same discipline, different comparator.
   This also catches silent no-ink failures (emoji, missing glyphs — see ae-mcp-realities §4).
2. **Gate:** `ok` == (`flaggedPct ≤ 5%` AND `meanDE ≤ 8`). If `ok` → done.
3. If not: fix the **specific `worstCells`** (the colour pair says what's wrong, the box says where — re-measure that region if you mis-measured) and any `stripeCountMismatch` (copy the exact stripe centres/widths). Then re-audit.
4. Also VIEW the `renderUrl` yourself for the half the audit can't score (layout sense, copy, spacing). Repeat up to ~6 passes; if `meanDE` stops dropping, re-measure the region instead of nudging.

**Motion-semantic regression (run this even when the pixel audit passes).** `ae_audit_frame` scores a single
still — it cannot tell that motion moves *wrong*. **Run `ae_audit_motion(compositionName)` first** — it
samples Position/Opacity/Scale over 0.3-5.7s (post-expression, recursing into precomps) and returns
`AUDIT pos=<px> fades=<#> loops=<#> anim=<#>`. If a comp that should move comes back `pos~0 fades=0`, the
motion didn't land: fix it, and if entrances are still missing call **`ae_reveal_floor(compositionName)`**
(deterministic house rise+fade on un-animated non-BG layers) as a safety net. Then the manual checks:
1. **Keyframe-graph diff.** Extract each animated property's keyframe times/values + ease (influence/speed) and
   compare timing + curve against the design spec — not just end pose. House baseline is settle-weighted
   ~in22/out75; flag anything left at flat 33/33 or LINEAR on spatial props. Where the curve was fitted to a
   reference, the reference is the spec: a deliberate curve reading as something other than in22/out75 is a
   pass, not a finding.
2. **Critical-beat frame sampling.** Render and eyeball 4 frames per animation: **0%** (rest before), the
   **ease-in peak** (fastest mid-motion), the **ease-out start** (settle begins), **100%** (final rest). Compare
   each against the intended look — overshoot, clipping, and mid-flight glitches only show here.
3. **Stagger validation.** Measure inter-element delays across a reveal group. Flag **>150ms** (sluggish, drags)
   or **<30ms** (no settlement, reads simultaneous); house range is ~120–180ms (0.12–0.18s).
4. **Timing gate.** Penalize any single animation **>2s** (too slow / loses attention) and any micro-interaction
   **<100ms** (imperceptible, looks like a jump). Re-time to fit the window.

**Structure validation.** Confirm the build's craft holds: every comp/layer carries a schema name (`#`/`>`
encoded — no `Comp 1` / `Layer 1`), comps over ~20 layers are precomposed by function, ROI is cleared for the
final render, and animated shapes are parametric (not frozen Bezier).
- **Exit gate:** audit `ok` is true AND the vision pass is clean AND the motion-semantic check passes (graphs match spec, beats look right, stagger in range, no out-of-window timing) AND structure validation passes.

---

## Phase F — FINALIZE (deterministic, run once at the end): `ae_finalize_build`

After the build animates and passes the audit, call **`ae_finalize_build({ compositionName })`** ONCE — once per
BUILD, not once per request. A later addition or correction to a finished composition does not re-enter this
phase: finalize again only if that change itself produced new mechanical motion, and never to tidy a comp the
user has already accepted. It
runs native ExtendScript that deterministically (no model guesswork) does three things the build used to
get wrong:
1. **Brands the comp** — renames the auto-named `Vibecode_<ts>` to **`hf_<ts>`** (`brandPrefix`, default `hf_`).
2. **Repairs mechanical easing, and only that** — BEZIER with the value-type-correct **spatial arity** + a
   settle-weighted **in22/out75** profile, applied to keyed transform properties that are still LINEAR or at
   AE's untouched 33.3333 default, recursing into precomp sources. This kills the #1 "robotic/crude motion"
   bug: Position is SPATIAL, so a wrong-arity ease array silently leaves it LINEAR. **It does not overwrite a
   curve that was deliberately shaped, and does not smooth HOLD keys into transitions**, so motion fitted to a
   reference survives finalize intact — the result line reports how many properties were eased versus
   preserved. Pass `easingPolicy:'preserve'` to touch no curve at all; `'force'` restores the old blanket
   rewrite and will destroy fitted curves, so reserve it for a deliberately mechanical build.
3. **Floors motion blur** — on layers with animated Position/Scale whose mechanical curves it just repaired,
   and not on a layer whose deliberate timing it preserved: whether that layer blurs belongs to the same
   decision as its curves. A reference showing a crisp stepped move therefore keeps it crisp.

It's idempotent and only touches keyed transform props. After it runs, refer to the comp by its new `hf_<ts>` name.

**Rig space** — if the built content sits off-frame (you parented layers to a Null/precomp and keyed them in
comp space instead of parent space, so the stack teleports), call **`ae_rig_rebase({ compositionName })`**. It's
self-gated (acts only when on-frame coverage <50% with the comp-space-key signature; otherwise no-ops), so it's
safe to call speculatively after `ae_finalize_build`.

---

## The one-line contract
MEASURE (don't eyeball) → BUILD from the passport → GENERATE the hard parts + composite → MOTION
(house reveal, settle ease, precomp) → AUDIT to a number, fix the worst cells → FINALIZE with
`ae_finalize_build` (brand + deterministic easing/blur). Skipping a phase is the reason a build
"isn't close to the reference".
