---
name: blender-scene-blocking
description: Block out a Blender scene with the bundled Blockstage add-on: draw parametric rooms with doors and windows, furnish them from a 42-piece library, stage four rigged characters with IK/FK, hand grips and held props, and set the camera to match a reference image or written brief. Installs and enables the add-on on first use. Use when the scene should be blocked quickly from ready-made, adjustable parts; for geometry modelled from scratch use blender-modeling or blender-greybox. Not for character modeling, rig construction, add-on development or skill authoring.
---

# Blockstage Reference Layout

Build editable scenes with the bundled Blockstage 0.3.0 assets and controls. Match the requested composition and level of detail while keeping the scene practical to adjust in Blender.

## Start with Blender

At the beginning of each invocation, inspect the available Blender connection and enabled Blockstage version. Immediately install or enable the bundled dependency when needed by following [Add-on Installation](references/addon-installation.md). Reuse an enabled, complete 0.3.0 installation without reinstalling it. Installing the skill folder alone does not execute Blender operations; dependency setup runs when the agent uses this skill.

Identify the active file, scene, collection, camera, frame range, and existing animation before editing. Use the supplied reference or written brief and the user's requested output location. Preserve a recoverable copy before replacing substantial existing work or switching files. Keep unrelated objects and animation intact. Ask only for information that materially blocks construction; resolve ordinary layout choices yourself.

## Establish the composition

For an image, identify its aspect ratio, perspective, camera height, subject proportions, overlaps, contact points, and dominant shapes. Match framing with coarse native assets before adding smaller objects. For a written brief, establish a clear room arrangement, circulation route, and camera position appropriate to the requested action.

Use a dedicated collection for a new setup inside an existing file. Keep native asset hierarchies together and check where the add-on places newly generated objects. Use English names for scene elements. During a local correction, preserve the established camera unless the correction requires a framing change.

## Construct through native controls

Load [Layout and Assets](references/layout-and-assets.md) when constructing rooms, openings, furniture, colors, or lighting. Build architecture and major furniture first, then add the secondary props needed for the composition. Use native editable controls instead of replacing supported assets with improvised geometry.

Load [Character Staging](references/character-staging.md) when adding, duplicating, posing, or attaching props to actors. Keep characters at the native blockout detail level unless the user requests additional detail. Add keyframes only when animation is requested; preserve the requested duration and frame rate.

Load [Live Construction](references/live-construction.md) when the user requests visible progress or records the screen. Otherwise, use the available Blender tools directly without unnecessary interface changes.

## Save the scene

Save the requested editable blend file with working asset roots, rig controls, camera, and scene organization. Keep newly introduced external resources available through packed data or portable relative paths. Produce images or video only when requested. Report the saved location and any actual unresolved limitation briefly.
