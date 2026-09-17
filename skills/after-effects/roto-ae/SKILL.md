---
name: roto-ae
description: Create, refine, review, and deliver AI-assisted rotoscoping in After Effects using local footage and available models. Use for subject extraction, matte correction, temporal cleanup, AE sequence delivery, or explicitly requested matting-model fine-tuning. Does not cover tracking-only work or editable mask animation.
---

# Rotoscoping for After Effects

Produce a source-faithful moving matte and a usable, verified After Effects project for the requested range. Follow the user's chosen processing route and delivery format. Preserve an established local-model workflow unless there is a concrete reason to change it. Raster mattes are the default; editable paths require a different implementation.

## Establish the current task

Inspect available source footage, the current AE project, result records, and recent user corrections before asking for missing information. Establish the intended subject and exclusions, native dimensions, source timing, requested range, delivery alpha convention, and current parent result. Include requested accessories and genuinely disconnected visible material; do not invent hidden connections.

Reconcile handoff notes with newer files and actual running processes. Reuse completed work instead of rerunning a stale checkpoint. Keep one owner for AE mutations and heavy accelerator work; independent source inspection, CPU review, and isolated preparation can proceed in parallel. Existing user authorization remains applicable within its scope.

## Select the work

For runtime discovery, segmentation, recurrent processing, native tiled inference, or moving to another machine, read [Local processing](references/local-processing.md). This skill supplies knowledge, not installed models or executable processing tools. Confirm the available implementation and its contract before choosing a route.

For missing material, retained background, hair, contact apertures, motion blur, color contamination, or temporal seams, read [Matte and color correction](references/edge-correction.md). Diagnose a representative difficult interval with adjacent source frames, then compare a bounded correction before extending it through the feature's actual visibility.

For explicitly requested training or fine-tuning, read [Model training](references/model-training.md). Improving this skill, adding source guides, processing a clip, and editing a matte do not update model weights. State which operation is actually running.

Before accepting or delivering a shot, read [Review and AE delivery](references/review-and-delivery.md). Distinguish completed computation, source-guide inspection, candidate review, assembled-output review, pixel-transfer verification, and saved delivery. None substitutes for the others.

When a result is unexpectedly weak or a tempting parameter change lacks a clear cause, consult [Observed failure patterns](references/observed-lessons.md). These are conditional lessons from actual work, not universal presets or evidence that a new shot is clean.

## Finish and retain useful knowledge

Preserve original footage, prior accepted versions, and raw model results. Keep editorial corrections visibly identified. Continue through the authorized range and unresolved demonstrated defects; do not call a locally improved sample a finished shot. Save a separate versioned AEP with accessible media and report actual coverage, remaining limitations, and usable paths.

Maintain transient job status and exact evidence bindings in the project. Add a lesson to this skill only after its observation, scope, outcome, and limitations are understood. Keep failed trials when they explain a useful decision, but condense the lesson instead of copying experiment logs. New user feedback can reopen acceptance.
