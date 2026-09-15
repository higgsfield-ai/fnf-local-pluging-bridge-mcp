---
name: blender-camera-led-assembly
description: Use when the user asks for a scene or product breakdown, build-up, or assembly animation. Create or revise editable Blender animations with expressive staged appearance, overlapping construction, and temporary internal assembly while preserving the agreed final look. Include camera or whole-product motion when requested. Exclude written scene analysis, static modeling, unrelated camera-only work, and animation outside Blender.
---

# Camera-Led Assembly

Apply this skill automatically to scene or product breakdown, build-up, and assembly animation requests, without requiring the user to name the skill. Interpret breakdown in this context as an animated construction or appearance effect; an explicit request for written analysis alone falls outside this scope.

Create an expressive, coherent appearance animation from the existing scene. Develop a visual idea specific to its construction, materials, and camera view. Keep the result editable and recover the agreed final appearance exactly within measured rendering limits.

## Scope and live state

Preserve existing geometry, materials, UVs, normals, placement, lighting, visibility, and camera behavior by default. Apply explicit changes to the identified scene only and establish the revised baseline before judging preservation. Temporary construction geometry may strengthen the effect; remove its visible, shadow, reflection, and instance contributions before the final state.

Read [blender-scene](../blender-scene/SKILL.md) for the local session contract, or load it with `bl_get_skill(name: "blender-scene")`, and follow its routing for the modules actually needed. Check `bl_health` and `bl_get_scene_summary` before edits. Prefer specific callable tools; use Blender Python for topology analysis, bulk animation, and checks when those operations require it. Report unavailable dependencies and choose a supported route within the authorized scope.

Recheck the live file and active scene after user steering. Record unsaved state, camera, frame range, frame rate, aspect, and neighboring scenes. Locate the requested project from that evidence and the supplied files. If the source or a necessary final-state decision remains unresolved, ask for that missing input before dependent edits. Preserve a recovery copy before broad changes. An older checkpoint must not replace unrelated live edits; an isolated revision can be appended as a separate scene.

This server drives a dedicated background Blender process and cannot see an open desktop window. When the user refers to an asset they just opened on screen, that file is not the session's file: ask for its path and open it with `bl_open_project`, rather than assuming the background scene already holds it. Save .blend files before disconnecting; unsaved state is lost on reconnect. Preserve and transfer the actual selected asset before replacing its environment with a procedural substitute.

Read [Blender mechanics](references/blender-mechanics.md) before copying or reparenting scene data, handling instances, or changing animation channels. Record the protected source state and capture its evaluated camera view before editing.

## Choose the construction idea

Distinguish a single hero product from an environment with many visual subjects, independently of object count. Load [Product assembly](references/product-assembly.md) for a hero product or temporary internal construction. Load [Environment assembly](references/environment-assembly.md) for architecture, vegetation, or repeated scene assemblies.

Consider distinct concepts and choose the strongest readable one autonomously. Record the chosen idea, dominant connections, protected elements, duration, mechanism families, and completion criteria in a compact working plan. Define whether the requested empty start covers the subject or the whole visible scene. Existing fixed backgrounds can remain when that matches the shot.

Derive parts from construction, seams, materials, connected geometry, and attachment points. Each repeated family shares a construction method; timing and emphasis may vary. Part count is useful only when it improves the visible assembly.

## Choreograph overlapping motion

Build local dependencies and overlapping events across visible regions. Supporting structures must be ready when contact occurs, while approaching components may already be moving. Keep one dominant connection readable as supporting motion continues. Choose duration and final hold from the shot, then convert timing using its actual frame rate.

Match motion to physical role. Rigid modules approach at working size, align, retain a readable gap, and seat smoothly. Structural members extend from attachments. Hinged surfaces rotate around their connections. Flexible components unfold or unbend according to their support and material. Repeated details join in overlapping waves. Short materialization may establish a part, but the subsequent assembly must remain visually distinct across these mechanisms.

Use semantic controllers and record each event's source, family, attachment, final transform, interval, motion, and temporary status. Compute contacts against the support's evaluated pose. Preserve smooth velocity through intermediate keys and retain intentional timing accents. Judge continuity by visible movement and attention, not merely by the existence of active curves.

Use the existing camera unless its revision is requested. Load [Camera choreography](references/camera-choreography.md) when changing camera motion, framing, or whole-subject travel. Coordinate these changes with local assembly and the agreed endpoint.

## Verify and deliver

Plan and inspect through the evaluated camera. Keep approaching panels and foreground surfaces clear of important connections. Projected bounds locate suspect intervals; rendered views resolve actual occlusion. Recheck the complete affected interval after changes to paths, pivots, timing, or camera motion.

Load [Validation and delivery](references/validation-delivery.md) for final comparison, sequential rendering, export, and transmission. Finish with the agreed native scene, a verified preview in the requested shading, and the authorized deliverables. State the meaningful changes, preservation result, and any unresolved limitation.

When the user also requests a process case study inside an existing media template, read [Case-template handoff](references/case-template-handoff.md). This is an optional delivery step, not a reason to alter every assembly task or publish to an external channel automatically.
