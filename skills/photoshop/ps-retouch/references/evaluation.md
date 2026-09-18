# Baseline and adaptive evaluation

Use this protocol only for an explicitly requested comparison or pilot plan. Evaluate adaptation separately from automatic profile selection. A proposed smoke test uses three photographs with distinct challenges; a later preliminary pilot can cover twelve to eighteen photographs across all profiles. The user's requested scope determines actual generations. A plan alone does not authorize image editing.

## Fix the conditions

Before generation, fix each original photograph, exact user request, manually selected profile and explicit scope overrides. Baseline uses the canonical profile with only those necessary overrides. Adaptive uses the identical effective baseline plus a grounded addition frozen before any candidate is generated or inspected. Keep permitted edits and correction strength equal. Never revise an adaptation in response to a candidate within the same case.

Start every run from the original, using the same tool and exposed model and settings. When authorized, generate two independent outputs per condition per photograph, giving twelve outputs for the three-photo smoke test. Match predetermined seeds between conditions only if the tool exposes seed control. Otherwise record its absence and do not claim reproducibility. Do not infer hidden settings.

## Preserve the evidence

Record case and run identifiers, source references, exact user requirements and overrides, skill and profile versions, and a SHA-256 hash of the exact canonical profile bytes including line endings. Record the exact adaptation, empty for baseline, and the complete prompt actually sent with any wrapper instructions. Capture actual exposed tool details, settings, call identifiers, output identifiers and returned paths, marking unavailable information as unknown or not exposed.

Preserve every unchanged generated original, failures, extra outputs and protocol deviations. Do not replace poor candidates or quietly regenerate them. If permitted safety recovery occurs, record every attempt, actual prompt, outcome and reduction of scope. A reduced-scope fallback is outside the planned condition and must be reported separately rather than scored in its matched pair. Retain all planned successful candidates and fix their pairing before scoring.

## Compare and score

Pair the first planned baseline output with the first adaptive output, and the second with the second. Randomize left and right independently for each pair. Give candidates opaque identifiers; keep the condition mapping, prompts and randomization record outside the evaluator's gallery until scores are fixed. If an evaluator has seen which condition produced an image, label their assessment unblinded. An anonymous gallery does not restore blinding. A blinded comparison needs an evaluator who has not seen the mapping.

Show the original and fixed requested outcome beside each pair. Inspect both normal-size views and corresponding detail views, retaining access to unmodified originals. Judge achieved correction strength and finish separately from preservation of identity, anatomy, expression, permanent marks, materials, clothing or product design, text, framing and profile-specific lighting or background constraints. Record the pair outcome as a left win, right win, tie or both unacceptable, and record critical defects for each candidate even when it wins.

Report adaptive wins, baseline wins, ties, both-unacceptable pairs and candidate-level critical defects by condition. State each percentage's denominator. If reporting wins over decisive pairs, separately report excluded ties and both-unacceptable pairs. Break down outcomes by photograph and profile so repeated outputs are not treated as independent photographs. Label smoke tests and preliminary pilots accurately; neither establishes statistical significance or a general advantage. State unknown settings, deviations and coverage limits, and retain losing outputs for later analysis.
