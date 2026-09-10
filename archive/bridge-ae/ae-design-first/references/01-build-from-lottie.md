# AE Build-from-Lottie (Lottie JSON → native moving scene)

**Why:** the HTML path builds the static frame in one call; THIS path builds the *motion* in one
call. You author one Lottie/Bodymovin JSON (the same format AE exports via Bodymovin) and
`ae_build_scene_from_lottie` rebuilds it as native comps, shape/text/solid layers, transform
keyframes and eases — all editable afterwards with the normal `ae_*` tools. One authored JSON
replaces dozens of keyframe calls. *(Authoring contract below adapted in part from Diffusion
Studio's text-to-lottie spec map, MIT.)*

## The call

```
ae_build_scene_from_lottie({ lottie: <JSON string or object>, compositionName?: "hf_logo-reveal" })
→ { composition, layersBuilt, keyframes, precomps, skipped: [...] }
```
**Read `skipped` EVERY time** — unsupported features are never silently dropped, they are listed
there. Fix what matters with atomic tools (e.g. re-apply a gradient via `ae_apply_gradient`).

## Authoring contract (the subset that converts 1:1)

**Document:** `{ v, nm, fr, ip, op, w, h, assets: [], layers: [] }` — `ip` inclusive, `op`
exclusive (`ip:0, op:90, fr:30` = 3s). Times are FRAMES; the converter divides by `fr`.

**Properties:** static `{ "a": 0, "k": value }` · animated `{ "a": 1, "k": [keyframes] }`,
keys sorted by `t`. Keyframe: `{ "t": frame, "s": [value], "o": {"x":[..],"y":[..]},
"i": {"x":[..],"y":[..]}, "h"?: 1 }`. `h:1` = hold key.

**Easing mapping (approximation — know it):** AE temporal ease is derived from the HANDLE X
only: out-influence = `o.x·100`, in-influence = `(1−i.x)·100`, speeds 0. So ease-out ≈
`o.x:[0.2], i.x:[0.2]` → fast out / very soft landing; house settle ≈ `o.x:[0.22], i.x:[0.25]`
(≈ in22/out75 after conversion). `y`-overshoot (`i.y > 1`) does NOT convert — for overshoot add
an explicit settle-back keyframe past the target instead (that converts perfectly).

**Layers (`ty`):** `4` shape · `5` text · `1` solid (`sc` hex, `sw`/`sh`) · `3` null ·
`0` precomp (via `refId` → `assets[]`; nest freely). Layer fields: `nm` name, `ind` index,
`parent` (ind), `st` start frame, `ip`/`op` in/out, `ks` transform
(`a` anchor, `p` position, `s` scale [100,100], `r` rotation deg, `o` opacity 0-100), `hd` hidden.
Colours are 0-1 floats. Y grows DOWN (same as AE).

**Shapes (inside `layers[].shapes`):** group `gr` (with its `tr` transform) · rect `rc`
(`p` centre, `s` size, `r` roundness) · ellipse `el` · path `sh` (`ks.k = {c, v, i, o}` —
closed, vertices, in/out tangents) · fill `fl` (`c`, `o` 0-100) · stroke `st` (`c`, `w`, `o`) ·
**trim `tm`** (`s`/`e`/`o`) — the draw-on primitive: animate `e` 0→100 to draw a line/icon in.

## NOT converted (comes back in `skipped` — plan around it)

- **Gradients (`gf`/`gs`)** → solid fill from the first stop; re-style after with
  `ae_apply_gradient` (Ramp) on that layer if the gradient matters.
- **Masks / track mattes / image layers / expressions / text animators / repeaters** → skipped.
  Images: import separately (`ae_import_image`) and composite after the build.
- **Animated paths** and **split positions** (`p.s:true`) → static first key.
- **Time-remap / time-stretch** → ignored.

## Workflow

1. Design the choreography per **ae-animation-principles** (reveal grammar, orchestration,
   timing defaults) — Lottie is just the serialization of those decisions.
2. Author ONE self-contained JSON: real text as `ty:5` layers (editable), semantic `nm` names
   everywhere, precomp repeated units via `assets`.
3. `ae_build_scene_from_lottie` → read `skipped` → fix what matters with atomic tools.
4. **Verify like any build:** `ae_audit_motion(composition)` (expect pos/fades/anim > 0),
   `ae_export_frame` at a settled time — eyes on the render. The ease conversion is an
   approximation: if a move feels off, retune with `ae_set_temporal_ease` (that's cheap now —
   the keys already exist).
5. `ae_finalize_build` still applies if you want the house settle-weighted polish pass.

## When NOT to use this path

- Static/layout-heavy frame (dashboard, card, poster) → **ae-design-first** (HTML) — better
  text/layout fidelity, auto-precomps.
- One-property tweaks on an existing comp → atomic `ae_*` calls.
- Heavy raster/photo composition → build chrome via HTML/atomic, generate imagery, composite.
