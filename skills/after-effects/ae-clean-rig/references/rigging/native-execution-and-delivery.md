# Native execution and delivery

## Application operations

Read this reference before project changes and again for delivery. Discover the operations available to `ae_do` with `ae_catalog`; operation names inside `ae_do` and `batch.run` are unprefixed, such as `layer.set_track_matte`, and the `ae_` prefix belongs to the MCP tool names. A batch shares one undo group but is not transactional — inspect partial results before retrying a mutation. If a needed operation is not cataloged, report that limitation and preserve any completed preparation rather than claiming a finished AEP.

Prefer cataloged operations. Arbitrary ExtendScript is not available by default: `eval.run` requires `AE_MCP_ENABLE_EVAL=1` on the server, and enabling it to work around a missing operation is not the answer — report the gap instead. Keep any application code inline; this corpus ships prose, never standalone helper scripts. Preserve the user's project in a versioned copy with `ae_save_project` before mutation.

Run one mutation at a time and wait for its actual completion before the next dependent call. A timeout after the request was consumed means completion is uncertain: inspect project state before replaying a mutation. A pre-existing success report is not evidence that the current operation completed.

For native freeform shapes, add `ADBE Vector Shape - Group` beneath `ADBE Vectors Group`, then set its leaf `ADBE Vector Shape`. Match the vertex and tangent arrays. Fill and stroke colors in native scripting use normalized channel arrays; a connector can have a different schema, so read its contract. Reacquire indexed property references after adding effects or contents, and change a locked layer only after unlocking it.

Use track mattes to share an aperture: `layer.set_track_matte` links the content layer to its matte, with alpha for the visible aperture and inverted alpha for holdouts. Keep the matte available to its content while hiding its own rendered appearance. Verify these APIs rather than assuming an older application's layer-order convention. The native continuous-rasterization property for a vector precomposition is `collapseTransformation`. Essential Property enumeration with `getMotionGraphicsTemplateControllerName` is one-based in the verified version.

## Visual and numerical verification

Render the source-matched neutral pose, relevant extremes and intermediate transitions with style distortion and motion blur disabled. For dimensional work test the requested head yaw and pitch, including silhouette and occlusion changes; include body turns and opposing face/body motion only when body controls are in scope. For faces inspect gaze at the boundary, half and full blinks, independent lids, each mouth pose and small-to-large openings. For limbs inspect both hands, sleeve sockets, planted feet, lifted feet and a crouch. Add a parts view when separation needs to be demonstrated.

Evaluate active expressions for errors and non-finite values, reachable-target drift and stable bend direction. Compare shared aperture boundaries and verify matte links. These checks supplement actual pixels: valid paths can still make diamond eyes, wrong thumbs, visible shoulder caps or doubled mouths. Inspect enlarged problem areas and the final nested composition, not only its source.

After changes to nested expressions, compare freshly written frames rather than cached previews. If stale Essential Property renders persist, save the project, purge the application's caches through the verified operation and rerender the affected checks. `project.purge` is the cataloged operation for that; it clears all caches when no narrower target is given. Wait for image writes to finish before judging them. Do not run source-control mutation tests concurrently with asynchronous frame capture.

Verify independent instances when reusable nesting is part of the rig. Restore temporary QA controls and times without deleting user keys. Inspect the actual exported video at rest, extremes and transitions, check duration and frame count against the chosen settings, and decode the complete file to detect corruption or missing output. Judge a promised loop by its boundary poses and motion, not merely by repeating the video player.

## Deliverable

Save the final AEP with a discoverable manual rig and grouped, meaningful controls. Include linked artwork, an animated demonstration, usable video previews and short operating notes with defaults, tested ranges and known limitations. Confirm external assets resolve from the handover folder. A custom controller panel is optional; native controls must remain editable without it. Keep prior versions and recovery checkpoints separate from the current package.

Report what changed, what was actually rendered and inspected, and any incomplete capability. A compilation check, a numeric test or a routing evaluation cannot certify visual rig quality. Do not promise a fully automatic rig for an unseen design when its separation, reconstruction or native deformation remains unverified.
