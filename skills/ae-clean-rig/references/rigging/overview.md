# Character rig: face, body, puppet and delivery

This is the complete pipeline for building or repairing a 2D character rig. It owns artwork separation, face and body controls, native Puppet, dimensional turns and the rendered rig test. Read it first for any rig request; `references/11-character-production.md` adds the production wrap around it — motion measured before rigging, reference playback, compositing passes — and `references/characters/overview.md` owns animating the finished character.

## Outcome and inputs

Produce an editable After Effects character project whose separated artwork, controls and demonstrated motion preserve the supplied design. Continue through native rendering and inspection; a generated animation alone does not satisfy a rig request. Reuse the user's reference, previous approvals, requested movement and existing project. Determine whether the task covers the face, body, soft parts or an existing defect before changing artwork.

Inspect the actual source at its original dimensions and the relevant existing project. If neither an accessible reference nor a sufficient character brief exists, obtain the missing input before inventing a design. For a brief-only request, create a reference within the requested scope using an available image-generation capability, then inspect it before rigging. Preserve an already accepted design. Study supplied tutorials through accessible video content or transcripts and distinguish observed techniques from inferences; a title alone is not evidence of having studied a video.

## Prepare and choose the rig

Inspect the project with `ae_project_info`, `ae_comp_info` and `ae_layer_info`, discover the operations available to `ae_do` with `ae_catalog`, and render frames with `ae_render_frame`. Verify the installed application version with `ae_version_info`. Follow [native execution and delivery](native-execution-and-delivery.md) before project changes. Preserve the existing project and user animation in a versioned copy.

For a new image, changed topology or inadequate overlap, follow [artwork preparation](artwork-preparation.md) before creating deformers. For a repair, inspect and correct the affected dependency chain while retaining unaffected controls and artwork. Recheck separation where the repair exposes previously hidden areas.

Use [face construction](face-construction.md) when facial controls are in scope and [body construction](body-construction.md) for articulated limbs or torso movement. For a new rig, default to limited dimensional face and body turns where the visible anatomy supports them, unless the user requests a flat rig. Follow [volume and instance ownership](volume-and-instances.md) for these turns; independent yaw and pitch must alter form and occlusion. Do not invent a full body for a portrait-only request. For flexible parts requiring Puppet, use [native Puppet](native-puppet.md) after preparation. Rigid pieces can use pivots and parenting. Requested Puppet requires verified native deformation, not renamed transform controls.

## Animate and finish

Keep a clean manual rest rig and a separate animated demonstration. Choose a short performance that visibly exercises the requested controls, with readable holds, deliberate timing and restrained secondary motion. Make stylistic line variation adjustable when requested. Expose only controls meaningful for this character, with clear names, neutral values and tested limits.

Complete the native pose, independent-instance and rendered-media checks in [native execution and delivery](native-execution-and-delivery.md). Correct observed failures and rerender affected output. Deliver the saved project, necessary artwork, usable controls, previews and concise operating notes. State actual turn limits and any incomplete capability; never label uncreated pins, an unrendered project or a routing-only test as a finished character rig.
