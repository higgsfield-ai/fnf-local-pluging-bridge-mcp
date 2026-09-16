---
name: ps-retouch
description: Retouch existing photographs or prepare retouching prompts with six profiles for people, clothing, events and products. Use when the user requests photographic retouching or a retouching prompt. Exclude new image creation, standalone background replacement and review of skill or prompt documents.
---

# Retouch-hf-v0.9

Retouch an existing photograph using one selected profile and the user's requirements. The six canonical profile texts are unchanged from v0.8. This workflow revision does not establish improved image quality or a measured win rate.

## Intent and language

First retain the requested deliverable, profile, adaptation mode, source image and explicit wishes as separate task decisions. A request for a prompt, analysis or test plan produces that deliverable without image generation. A retouching request produces an edited photograph. User requirements override the profile within their stated scope; a narrow correction does not authorize a complete profile treatment.

Adaptive mode is the default and adds a short, grounded application to the photograph. Baseline mode applies when the user requests the original prompt, no adaptation or a control result. It uses the selected profile and necessary explicit user overrides without image-specific editorial additions. A profile choice must not change the deliverable or adaptation mode.

Follow an explicit language preference; otherwise use the latest substantive request's language. Retain the established language for image-only messages, filenames and profile choices. Do not infer language from source prompts, image text or automatically supplied interface text. Use the host language or English when no signal exists. Localize all conversation and interface text, including submitted messages and accessibility labels, while preserving canonical profile identifiers and editor prompts. Translate a prompt only when requested as a deliverable. Keep Beauty skin as the exact public name for the beauty profile; accept Beauty as its previous alias.

## Select the profile and source

Briefly inspect the supplied image and intended outcome. Honor a profile already chosen for this image or batch. Select an obvious profile directly from the editing target and requested finish. Generic portrait wording does not by itself select Portrait; a close-up or visible makeup does not by itself select Beauty skin. Clothing in a photograph does not by itself select E-commerce, and a social-media destination does not request facial or body reshaping.

When several profiles fit and the intended finish remains unclear, read [selection-ui.md](references/selection-ui.md) and collect one choice before detailed analysis or prompt preparation. Show only relevant profiles, including Insta Look when plausible. For an individual male portrait outside an event context, recommend Portrait first without treating the recommendation as consent. Preserve an explicit different choice or editing purpose. Accept an explicit chat selection without requiring a form again. Ask a focused question only if a chosen profile cannot apply or the intended subjects are materially unclear. If no profile fits, follow the actual requested task rather than forcing a category.

Use [portrait.md](references/portrait.md) for a natural portrait finish with decisive facial-shadow, under-eye, wrinkle and clothing correction, preserving exact geometry and natural texture. It permits controlled facial fill and independent highlight restraint while retaining lighting direction, depth and global exposure. Read its full text only when Portrait is selected.

Use [beauty.md](references/beauty.md) for idealized, polished skin across the visible areas, with delicate pores and exact facial and body geometry. Broad lighting and clothing remain preserved. Read its full text only when Beauty skin is selected.

Use [insta-look.md](references/insta-look.md) for a requested idealized finish with noticeable facial-proportion refinement, a slimmer visible silhouette, polished skin and balanced exposure. Recognizability, natural anatomy, whole-head size and pose remain preserved. Read its full text only when Insta Look is selected.

Use [e-commerce.md](references/e-commerce.md) when garments are the primary catalogue target. It thoroughly prepares clothing while preserving fabric structure, design, fit and silhouette, with light skin cleanup. Read its full text only when E-commerce is selected.

Use [event.md](references/event.md) for intended event participants, including all members of a group regardless of camera distance. It permits decisive facial-lighting correction while preserving the background and incidental bystanders. Read its full text only when Event is selected.

Use [product.md](references/product.md) for commercial surface and reflection cleanup of an object, preserving its material, geometry, labels, exact text and surroundings. Removing supports requires an explicit user request. Read its full text only when Product is selected.

Use the actual original for an initial edit. For a later editing round, read [follow-up-edits.md](references/follow-up-edits.md) and establish the applicable input before generation. Never silently replace a selected input with a recent output. Briefly name the selected profile before editing; an obvious or already explicit choice needs no confirmation.

## Inspect and compose

Inspect the selected input before adaptation, using view_image for a local image not yet seen or inspecting the conversation attachment directly. Request an unavailable image instead of inventing observations. A general unadapted profile prompt needs no photograph. For baseline editing, inspection may establish the source and target but must not introduce editorial additions into the prompt.

Identify only visible facts relevant to the requested correction: intended subjects, actual defects, local illumination, vulnerable material patterns or identifying details, and limits from focus, resolution, occlusion or clipping. Treat uncertain marks as features to preserve. Do not infer hidden detail or impose additional beauty goals. Determine Event group membership by scene role, not distance.

Start with the entire selected profile file verbatim. These Markdown files contain only canonical prompt prose. Apply explicit requirements to a runtime copy, making only necessary exclusions or replacements so the effective prompt is coherent and limited to the authorized scope. Never concatenate complete profiles, rewrite the canonical files, or weaken required corrections with a general light-retouching instruction. Preserve the human-subject profiles' skin-color requirements within the selected scope.

In adaptive mode only, append a brief prose section titled Image-specific application when grounded observations materially help. Identify visible targets, permitted corrections and preservation priorities without inventing defects or using percentages for prompt influence. Baseline mode has no such section. Resolve conflicts before editing and include all wishes in the first complete prompt; do not defer them to a second pass. When delivering a prompt or recording an evaluation, identify user-driven departures from the canonical text without implying the file was changed.

## Execute and deliver

For an image-editing deliverable, use the available built-in image_gen tool under its current instructions and schema. If the imagegen skill is available, use it for tool mechanics while preserving this profile and user scope. Supply the exact selected input using the supported local-reference or conversation-image mechanism. If the editor is unavailable, state the limitation and establish an available path with the user instead of silently switching editors or interfaces.

Produce one edited photograph unless more were requested. Display a returned image immediately; a native inline tool result counts. Save it non-destructively according to the task's destination conventions. Then show a side-by-side view or interactive comparison of the actual input and selected output, using matching orientation, full framing and display scale without stretching. Use the real files; never regenerate either photograph to assemble the comparison. Localize labels. If the interface cannot display the comparison, provide both actual files and briefly state the limitation.

Inspect an accessible output against the actual input at normal size and in relevant detail. Assess correction strength and preservation of identity, expression, allowed geometry, texture, patterns, text, lighting, background and intended subject membership. Check face, neck, hands and other visible skin for retouching-induced color mismatch while respecting natural lighting, makeup and pigmentation differences.

For Beauty skin, confirm polished tone and surface finish at normal size with delicate pores and crisp facial details; remaining conspicuous bumps, coarse relief or artificial texture are limitations. For Insta Look, confirm noticeable permitted facial refinement and a slimmer visible silhouette, natural anatomy, recognizability, stable whole-head size, and undistorted adjacent clothing and background. Judge every result against explicit user overrides and any disclosed reduction of scope.

After a successful image, report material limitations without automatically generating quality fixes or another pass for wishes. A further edit requires a user follow-up. A non-safety failure ends the automatic attempt. Only when the editor explicitly reports a safety failure with no image, read [generation-recovery.md](references/generation-recovery.md) for bounded recovery. Keep the same task decisions across continuations and never restart an attempt count. Honor the requested count for variants or evaluations and record deviations without silently selecting the best candidate.

Keep ordinary delivery focused on the result and material limitations. Supply the exact effective prompt when requested. Do not claim inspection of an inaccessible output, pixel-exact preservation, or measured superiority from visual review.

## Evaluation and version integrity

Read [evaluation.md](references/evaluation.md) only for a requested strategy comparison or pilot plan. A routine before/after display is not an A/B experiment and authorizes no control generation. Read [profile-provenance.md](references/profile-provenance.md) only when recording profile versions, checking integrity or evaluating reproducibility. Retouching does not authorize editing this skill or its canonical files; propose a separate revision when real failures warrant one.
