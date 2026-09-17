# Model Training and Evaluation

## Define what is being learned

Start weight training only within an explicit user request. State whether the operation changes a base model, decoder, selected backbone blocks, source guides, editorial mattes, or this skill's instructions. Inference, added negative points, local alpha repair, and AE color finishing are not weight updates. Do not describe a manually repaired result as unmodified model output.

For a small specialized dataset, use an available pretrained model as a starting point when compatible with the task. A handful of clips can support a pilot and targeted fine-tuning; success on their frames does not establish generalization to unrelated footage. Do not promise a universal clean result or a fixed number of training rounds.

## Data and separation

Establish actual source provenance and the user's rights or authorization for the intended training use. Commercial editing permission and permission to train are different questions. Preserve a user's stated authorization instead of repeatedly requesting it. When unresolved terms matter, verify the relevant model, weights, dataset, and service conditions; do not infer permission from open-source branding or generated-media provenance alone.

Keep original source RGB, source-derived guides, and accepted editorial alpha as separate data. Preserve native timing, dimensions, precision, and label provenance. Editorial acceptance is a practical production judgment, not measured physical alpha. Guide masks, reference mattes, color-finished composites, and raw model predictions are not interchangeable targets.

Split by shot or source identity before creating neighboring frames, overlapping crops, or augmentations. Keep held-out material out of optimization, teacher construction, hyperparameter tuning, and checkpoint selection. Final diagnostic review may reveal a held-out failure; a separate editorial delivery repair does not turn that result into training data. Retire or redesign a test set explicitly before using its outcomes to select future models.

## Reproducible continuation

Bind each run to its source inventory, training split, preprocessing, trimap semantics, crop schedule, loss definitions, checkpoint, and trainable parameter set. Resume optimizer state, step counters, and random state when continuing an experiment. Starting from weights alone is a different run. Preserve frozen parameters and normalization buffers as intended. Do not add step counts from alternative branches into one fictitious training history.

Known trimap labels can disagree with editorial targets. Measure those disagreements separately from uncertain-region errors. Keep old teacher supervision distinct from newly accepted labels. A teacher should not silently preserve the omission that current supervision is intended to fix.

Use a bounded comparison to test a specific failure hypothesis before committing to a longer run. Stronger background or known-region loss can reduce leakage while damaging opaque shoes, ribbons, or skin. Lower aggregate loss is insufficient when material density, narrow gaps, or temporal stability regress. Reject unsuccessful candidates without overwriting the retained checkpoint.

## Evaluate the intended deployment

Evaluate native tiled inference with the same RGB sampling, trimap construction, tile support, blending, output mode, and color convention intended for delivery. Crop evaluation and full-frame overlap blending can expose different failures. Source-hint changes must be evaluated as input interventions, not attributed to newly learned weights.

Report foreground undercoverage, background leakage, edge behavior, and temporal observations alongside aggregate error. Separate per-shot and difficult-region outcomes so large easy backgrounds do not hide small critical defects. Numerical variation without source correspondence does not prove flicker. Inspect actual source, alpha, and composites before selecting a checkpoint.

After bounded checks pass, evaluate the complete intended shot range and verify AE delivery separately. Keep raw inference, source-guided inference, and editorially corrected output identifiable. Report the best observed checkpoint and remaining failures honestly; further training is justified by evidence, not by an arbitrary update count.
