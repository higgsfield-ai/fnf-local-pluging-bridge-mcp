# AE Draw-vs-Generate — build the chrome, generate the content

Per the Fidelity Passport (ae-build-orchestration Phase A), mark EACH element **[DRAW]** or **[GEN]**
*before* writing any build code. Default detailed/illustrative → [GEN]; default flat geometry → [DRAW].

> **There is NO third option [CROP]. The reference is a MEASUREMENT source, never an ASSET
> source.** Cutting a piece out of the reference screenshot (crop + inpaint + import) is
> FORBIDDEN as a cost shortcut — it *feels* free but ships garbage: references are low-res/
> compressed screenshots that turn to mush next to crisp native layers (a 552px-wide ref
> scaled ×3.5 has ~7px of real detail per 24px of frame), inpainting leaves artifacts, and the
> result is one dead flat pixel block — non-editable, non-animatable per element, off-style.
> **Saving credits NEVER justifies a worse-looking frame.** The cheap path must be a SMART
> cheap path: recreate natively ([DRAW]/HTML — free AND editable) or generate ([GEN] with
> STYLE LOCK — costs credits; spend them when that's what quality needs). Crop is allowed ONLY
> when the user explicitly hands you a high-res asset and asks to place it verbatim.

## Decision matrix

| Element | Verdict | Why |
|---|---|---|
| Card / panel / sheet background, buttons, pills, dividers, bars, toggles, progress tracks | **DRAW** | flat geometry — clean as AE shapes, fully editable/animatable |
| ALL text — titles, labels, numbers, body, captions | **DRAW** (real text layer) | image-gen CANNOT render real text (produces garbage glyphs); text is always a layer |
| Simple flat icons | **DRAW** (recognize → rebuild from primitives, see ae-build-orchestration (module: ui-rebuilder)) | small flat glyphs build cleanly; tracing a bitmap = garbage |
| Character / mascot / person | **GEN** + composite | shapes can't carry a believable character |
| 3D / glossy / isometric-shaded object, product render | **GEN** | flat shapes look crude next to a shaded ref |
| Detailed illustration (coffee cup with steam, stack of books, fox) | **GEN** | illustrative detail is beyond primitives |
| Map with streets, ornate gauge/dial with many ticks | **GEN** | too much fine detail to hand-build |
| Small label-plate / badge / chip / stat-pill / status tag — **even with a gradient, glow or shadow, and even carrying its own text** | **DRAW** (shape + Gradient Ramp + a SEPARATE text layer) | it's CHROME, not art; small + carries a word = build it, never a flat image |
| Flat **gradient / glow fill** on any surface (card, plate, button, bg) | **DRAW** | a CSS `linear/radial-gradient` → native **Gradient Ramp / 4-Color Gradient** effect on the shape, fully editable — do NOT generate it as a raster |
| Painterly / textured / illustrative artwork (a *rendered* scene or material, NOT a CSS gradient) | **GEN** | real pictorial texture is beyond primitives (see ae-mcp-realities §5) |

**Litmus test:** if a flat-shape version would look crude/approximate next to the ref → GENERATE.
When in doubt and the element has real illustrative detail → GENERATE.

## Hard rules (these prevent the common failures)

1. **NEVER generate text.** Generate the wordless object; place every word as a real `ae_add_text_layer` ON TOP. A generated asset containing legible text = wrong, regenerate it wordless ("no text, no letters, no numbers, no watermark").
2. **NEVER generate the whole card/frame as one flat image** — it can't animate (the interior is baked). Generate only the detailed CONTENT object; BUILD the surrounding CHROME (card bg, frame, buttons, labels) as separate layers so each pops/reveals/parallaxes independently.
3. **Hard cap ~4–6 generated assets per frame.** More = slow + high failure. If you "need" 15, you're generating chrome you should be building.
4. **One clean asset per distinct object** (transparent background), then place / duplicate / scale.
5. **Small ≠ generate.** Badges, chips, stat-pills, status tags, tooltips, lower-thirds, legend swatches look "detailed" but they're CHROME: build the surface as a shape (+ Gradient Ramp / shadow) and put the label in a SEPARATE text layer. Generating one as a single image bakes its text and kills editability — the exact failure where labelled plates come back flat.
6. **A gradient or glow is a DRAW, not a GEN.** A `linear-gradient` / `radial-gradient` background becomes a native **Gradient Ramp** (2-stop / radial) or **4-Color Gradient** (3–4 stop) effect on the shape — editable in AE. NEVER generate a gradient/glow surface as a flat image.
   - **Apply gradients with `ae_apply_gradient` (the reliable native path).** Pass `{compositionName, layerName, stops:[{r,g,b}], type, angleDeg?}` with **measured** stops. It applies a native Gradient Ramp (2 stops) or 4-Color Gradient (3–4) via ExtendScript and **reads the colour back to confirm it landed** — bypassing the bridge bug where setting Ramp `Start Color`/`End Color` through raw `ae_apply_effect`/`ae_modify_effect_properties`/`ae_set_shape_fill` is **silently swallowed** (default black→white ramp = a grey plate). **Do NOT** hand-roll the gradient with raw atomic tools, and **do NOT** fall back to baking a PNG or a flat solid-fill because "gradients don't stick on the bridge" — that's exactly what `ae_apply_gradient` fixes. Apply it to the STATIC shape before keyframing (or precompose then animate) to avoid `setValue on a property with keyframes`.
7. **"Build, don't bake" covers EVERY method — including doing it yourself.** This rule is NOT only about the image model. Do **NOT** render a plate / badge / button / gradient / seal-with-text / any text into a PNG yourself with **Pillow / Python / canvas / a screenshot** and `ae_import_image` it — that is the same baking, and it ships the surface flat and dead. "I'm not generating, I'm just drawing it with Pillow" is the exact rationalization that produces baked plates. The ONLY editable path is real AE layers (shape + Gradient Ramp + a separate text layer). **Pillow is for MEASUREMENT only** (`ae_measure_reference`), never for producing build assets.
8. **NEVER disable or delete a layer because a fill / gradient / effect "didn't apply".** A shape rendering grey/colourless does NOT mean the build failed — the colour set can **silently fail** through the bridge (`ae_set_shape_fill` and effect-colour setters swallow the error and still report success; there is **no read-back** to confirm). Hiding the layer just ships a missing element. Instead: (a) **re-apply via the reliable path** — fills via `ae_set_shape_fill` with a `[r,g,b]` **array** 0–1 (never `{r,g,b}`, which silently defaults to white); gradients via **4-Color Gradient** (`Color 1..4`), not Gradient Ramp colours; (b) **verify with `ae_export_frame`** that the colour actually landed; (c) keep the layer **enabled**. Disabling/deleting to "work around" a non-applied colour is never the fix.

9. **Circular / arc / curved text (a seal, stamp, badge, "text around a logo") is a DRAW — build it with `ae_add_text_on_path`, NEVER bake it and NEVER hand-place per-character text layers.** `build_scene_from_html` can't carry SVG `<textPath>`, so the curved line won't survive the HTML walk — **that is not a licence to bake a PNG or to drop the seal entirely.** It's also not a reason to scatter N single-character `ae_add_text_layer`s around a ring by hand (fragile, un-reflowable, a nightmare to retune). The connector has the native primitive: **`ae_add_text_on_path`** creates ONE editable text layer riding a circular mask (AE's real *Text on a Path*) — the string re-flows when you edit it, `perpendicular:true` gives the seal look, and `spinSeconds>0` makes it rotate. **Build the seal as its own unit and precompose it** so it moves/animates as one object:
   - **One ring:** `ae_add_text_on_path({ compositionName, text, radius, startAngleDeg:0, perpendicular:true, spinSeconds?, precompose:true })`.
   - **Two arcs (classic stamp):** top line `startAngleDeg:0`; bottom line `startAngleDeg:180, reversePath:true` (so it reads upright) — build both with `precompose:false`, then precompose the two layers together into one `seal` comp.
   - The **graphic ring/emblem** behind the text (a wordless badge) may be `[GEN]` or a `[DRAW]` shape; only the **text** must be native curved text. Call `ae_add_text_on_path` **by name** even if it isn't in your visible tool list.

> **Symptom self-check — run BEFORE declaring done.** Open the result: if any TEXT is non-editable (baked into a picture) or any GRADIENT is a flat raster you can't retune, then you GENERATED an image where you should have BUILT. The build pipeline never bakes text or gradients on its own — baked = it arrived as a generated image. Fix it: regenerate that asset **wordless / empty** and rebuild the text as `ae_add_text_layer` + the gradient as a CSS gradient (→ Gradient Ramp).

## The generate-and-composite pipeline (canon-native)

Generation is the **Higgsfield connector**, not this editing server (ae-mcp-realities §11):
1. **Style-anchor:** crop the element region from the reference and use it as the generator's style
   reference so the asset matches the ref's art direction (not a generic render).
2. **Generate wordless, transparent bg:** `generate_*` with a prompt describing ONLY the object +
   "transparent background, no text, no letters, no watermark, exact same art style as reference".
   - **Vector-look content goes to the vector model.** Flat icon / logo / pictogram / sticker /
     badge art / flat-illustration content → **Recraft V4.1** (`recraft_v4_1`,
     `model_type: "vector"`; exact palette via `colors: ["#RRGGBB", …]`, flat `background_color`) —
     it holds clean edges and exact brand hexes where raster models smear. Characters / 3D-look /
     photo / textured illustration → the connector's default image model as before.
3. **Import:** `ae_import_image({ url })` (it imports image OR video).
4. **Clip into its frame** if needed: place the media ABOVE a shape and `ae_set_track_matte({ layerName:<media>, matteLayerName:<shape>, type:"alpha" })` (a rounded-rect matte gives a rounded thumbnail). *(A dedicated background-cutout (`rembg`) step is a connector tool-gap — for now lean on a transparent-bg prompt + the matte.)*
5. **Run jobs in parallel** (all generates fired together), don't serialize — keeps a multi-asset frame fast.
   - **STYLE LOCK:** before the batch, write ONE style descriptor (render style, palette hexes,
     lighting, materials, background) and prepend it VERBATIM to every generation prompt — all
     [GEN] assets of a task must land in ONE unified style. Off-style result → regenerate with the
     descriptor tightened; never composite clashing styles.
   - **The generation batch is ONLY `[GEN]` wordless content** (characters, avatars, illustrations, a wordless seal). **Plates / pills / badges / buttons are `[DRAW]` — they must NEVER enter the generation batch**, not even as a "prep it now while jobs run, rebuild natively later" shortcut. That bake-then-rebuild-and-delete loop is wasted work AND risks a baked plate slipping through. Classify `[DRAW]/[GEN]` UP FRONT (Phase A) and build every `[DRAW]` plate **natively from the start** with `ae_apply_gradient` (reliable Ramp/4-Color + colour read-back — call it BY NAME even if it's not in your visible tool list). There is no reason to bake a gradient as a hedge: the native path works, so go native directly.

## Blend the GEN asset into the built chrome

A generated object dropped on built chrome reads as "pasted" until it's blended in linear light and
graded with an adjustment layer. Two moves:

1. **Linearize the blend.** Composition > Color Management > **Blend Colors Using 1.0 Gamma** (linear
   blending). Do this BEFORE compositing high-contrast generated assets against built chrome — it kills
   the dark/bright halos and color fringing you get when AE blends in the working gamma at hard edges
   (glow rims, drop shadows, antialiased cutouts).
2. **Grade with an adjustment layer, not on the asset.** Place an adjustment layer ABOVE the GEN layer,
   then pick a blend mode for what you want: **Screen** to brighten / add a glow, **Multiply** to darken
   / seat it into shadow, **Overlay** to push detail and contrast. Tune the adjustment layer's Opacity
   to dial strength — don't bake the grade into the asset, so it stays re-tunable per frame.

**Render order matters:** within a layer, effects render bottom-to-top; the adjustment layer's blend
mode is applied AFTER all of that layer's effects resolve — so the grade sits on the finished, effected
asset, not the raw source.

**Workflow:** import generated asset → set its color space to linear → drop an adjustment layer above →
apply Screen / Multiply / Overlay → tune Opacity to taste.

## Then animate
Each [GEN] object is its own layer → give it the house reveal (ae-animation-principles (module: reveal-motion)) like any other
element, and precompose it with its chrome if it's a self-contained unit (ae-build-orchestration Phase D).

## Native texture / background cookbook — build geometry, NEVER generate a PNG for it
If the ref's background/surface shows a **repeating geometric texture** (crosshatch/grid, scanlines,
vignette, film grain, dotted grid, clouds, starfield) do **NOT** generate it as an image — diffusion
gets the geometry wrong and it can't be edited. Build it natively with built-in effects (measure
size/spacing FROM the ref — count cells across the canvas):
- **Diagonal crosshatch / grid:** solid in bg colour → `ADBE Grid` `{Size From=2 (Width-Slider), Width=px-between-lines, Border=1-2, Color=line colour, Opacity=1}` → rotate the SOLID 45° (size it `sqrt(w²+h²)` so corners stay covered) → layer Opacity 30-60%. Straight grid = same, no rotation.
- **Scanlines:** solid + `ADBE Venetian Blinds` `{Transition Completion=50, Direction=0, Width=2-8}`, layer opacity 10-30%.
- **Vignette:** adjustment layer + `CC Vignette` `{Amount 15-40}`. (No CC? radial `ADBE Ramp` black→transparent, blend Multiply.)
- **Film grain:** adjustment layer + `ADBE Noise2` `{Amount of Noise 2-6%, Noise Type=0}`, opacity 30-50%.
- **Soft ambient glow blob:** small solid (NOT full-frame) in glow colour + `ADBE Box Blur2` radius 100-150, opacity 4-10%, where the ref light is.
- **Dotted grid:** `ADBE Grid` with Border≈Width*0.9 (reads as dots) at low opacity.
- **Clouds / organic field:** `ADBE Fractal Noise` `{Fractal Type=Basic, Contrast 120, Brightness -30, Scale 150-300}`, blend Screen 5-15%; animate Evolution `time*30` for life.
- **Starfield:** 6-14 tiny rounded rects (2-8px) + occasional 4-point sparkle (two crossed thin rects); twinkle = per-star Opacity `wiggle(0.5, 30)`.

**Decision rule (`data-pattern` vs `data-gen`):** a repeating geometric texture → approximate it in CSS for the pixel audit AND tag the div `data-pattern='{"type":"grid-diagonal","size":56,"lineWidth":1,"color":"#262840","opacity":0.5}'` so the pipeline builds it natively (types: `grid`, `grid-diagonal`, `scanlines`, `vignette`, `noise`). Reserve `data-gen` / raster generation for genuinely **photographic/pictorial** content (never text, never glows, never a flat geometric texture).
