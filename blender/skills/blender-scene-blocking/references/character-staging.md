# Character Staging

## Native actors

Choose Man, Woman, Heavy Man, or Heavy Woman. Preserve each actor's meshes, weights, rest pose, constraints, widgets, and internal references. Use Duplicate Asset to copy the complete native hierarchy with remapped references. Do not reconstruct an actor from primitives or add facial features, clothing, or hair unless requested.

Native actors face negative Y with Z up. Pose coordinates are in armature space, while an asset parented to a room can use room coordinates. Inspect the evaluated world transform before positioning controls or attachments. Move the actor through its whole asset root rather than offsetting unrelated body parts.

## Poses and contacts

Use Selected Asset, Pose Controls for body, head, shoulder, hand, foot, elbow, and knee controls. Pose presets establish a static starting pose; Walk is not a walking animation. Presets reset pose controls, grip, and foot roll, so do not apply one over existing posing or animation without a requested reset.

Establish ground or seat contact, then adjust pelvis and torso balance, limb targets, pole controls, head direction, and hand orientation. Keep knees and elbows bending coherently without stretching limbs. Match head direction to the intended target rather than assuming the body's facing direction is sufficient.

Use Snap to IK or Snap to FK when changing control modes while preserving the current pose. Unsupported FK twists can be rejected with the pose retained; resolve the incompatible pose before switching. A manual IK/FK blend is not equivalent to snapping. Use native Roll and Bank for foot pivots.

Hand Grip supports Open, Hold, and Fist. Rig Details, Fingers provides individual phalanges with Curl and Spread. Use Attach to Hand for held props, then align the grip and the prop's functional direction. The native pistol points along negative Y before additional transforms.

When animation is requested, Key Pose records the actor transform, editable controls, fingers, and custom properties. Animate these controls rather than driven mechanism bones. Keep meaningful keys editable and preserve existing timing unless the request changes it.
