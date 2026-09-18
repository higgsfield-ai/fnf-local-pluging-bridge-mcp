# Photographic media: sourcing, generation and packaging

## What this server does and does not do

This server drives After Effects only. It does not generate images or video, does not download cloud results, and holds no provider account. Everything below describes what to do with media once it exists locally, and how to obtain it when a generation provider happens to be connected in the same session.

So the first decision is not "which model" — it is **where the plate comes from**:

1. **The user supplied it.** Use it. Never regenerate approved media during an unrelated correction.
2. **It already exists in the project.** Reuse the footage item; replace only what the request names.
3. **It must be created, and an image/video generation provider is connected in this session.** Follow the defaults below, after confirming the model is actually available.
4. **It must be created and no provider is connected.** Say so plainly, name the shots you need, and ask the user to supply or generate them. Continue every part of the AE work that does not depend on those plates. Do not substitute a screenshot, a placeholder solid presented as final, or a still standing in for requested motion.

## Defaults when a provider is connected

These are the user's saved preferences for new media, not a licence to regenerate anything already approved:

| Need | Default |
| --- | --- |
| Moving footage | Seedance 2.5 at 1080p |
| Still images | Nano Banana Pro at 2K |
| Explicitly requested override | Soul 2.0 at 2K, when the current task asks for it |

Verify the exact model and resolution in the connected provider's own catalogue before submitting. If the configuration is unavailable, report that and resolve the alternative with the user — do not silently swap model, provider, resolution, or replace moving footage with a still. Model names change; treat this table as the user's preference, not as a guarantee that those identifiers still exist.

## Describing the shot

Describe each needed plate from the reference: framing, subject, composition, light, camera movement, subject movement, duration, and entry and exit poses. Generate a clean plate with no baked-in UI, logos or typography — those belong in AE as native editable layers above the media.

For moving footage, preserve the observed motion. A generated still with invented pan or zoom is not an equivalent substitute for a real camera move. Review the whole returned clip for unwanted motion and temporal defects, and verify the actual downloaded dimensions and duration rather than trusting the wording of the prompt.

## Packaging

Import approved results into named replaceable media precomps, with editable text and graphics above them. Choose framing and aspect ratio for the actual placeholder: keep faces, subjects and important details inside the intended crop, and review the asset inside the animated card before accepting it. When replacing only an image, preserve the card's text, corner radius, shading and timing.

A portable project needs a media manifest listing, per asset: the local relative filename, its purpose or card or shot, the actual provider and model, the requested configuration, the returned dimensions and duration, a generation identifier when one exists, and source information. Never put credentials, access tokens or expiring signed URLs into the manifest. Keep font names and their redistribution terms separate from generated imagery.

Generated scene content is rasterized. State that limitation plainly and keep ordinary media replacement practical.
