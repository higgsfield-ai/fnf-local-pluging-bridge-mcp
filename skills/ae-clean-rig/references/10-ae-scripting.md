# AE bridge and expression reliability

## AE scripting details that prevent broken rigs

Use supported, discovered bridge/API capabilities. Prefer stable property match names over ordinal effect indices when available; AE versions can insert controls and shift the indices. Do not assume an app version, project ID, or local bridge port from another session. Reacquire indexed property-group references after adding/removing properties. Build Shape vertex and tangent arrays completely before assigning them; preserve vertex count/order between intended morph poses. Use actual comp frame duration for frame-aligned ranges. Save, render, and verify the resulting AE project rather than relying only on an external approximation of its appearance.

For paragraph text, inspect `boxTextPos` and the anchor point before treating Position as the top-left of the text box; a centred box origin can shift or clip an otherwise valid layout. Media Cover/Fit calculations must account for source and composition pixel aspect ratios. Preserve verified source metadata rather than forcing square pixels merely to hide incorrect fitting.

When adding text programmatically, explicitly reset or assign character styles and capitalization; new layers can inherit prior AE text settings even when the source string has mixed case. Verify the rendered weight and case. Verify shape-group stacking in a rendered pose: appending a group can put the new detail behind the existing fill. Inspect effect defaults, especially Repeat Edge Pixels and blur bounds, before using a blur for soft light. Preserve working native effect defaults unless a change is needed and verified. Do not blindly reassign undocumented popup values from a property dump; validate blend/composite behavior on a coloured test background to catch dark fringes or unintended shadows. Check effect point-control coordinates in a native render after parenting or recentering shape paths; an effect may not use the same origin as the vector path.

When simplifying keys, use bounded loops and verify the key count changes. For separated Position dimensions, edit the X/Y/Z follower properties; do not repeatedly remove keys from the separation leader. Save incremental progress and keep the bridge responsive during large mutations. Treat a bridge timeout as an unknown operation state: inspect before retrying, so a retry cannot duplicate or compound a partial edit.

For native 3D work, verify transform conventions against AE-rendered points rather than assuming a solver’s Euler rotation order matches AE. Check compound-path holes and depth ordering in the actual 3D renderer; a correct 2D fill does not prove the extruded result is correct. If a renderer needs a sampled motion-blur effect, inspect fast text-bearing surfaces for repeated outlines and use an appropriate shutter and enough samples.

## Scripting access is not expression access

Do not assume that an ExtendScript property-access method works in the AE expression language. A script may use `.property(...)`; an expression for a shape often uses the expression facade such as `content(...)`. In the agent rig, using the wrong access method in an eye-roundness expression produced square eyes. For the specific structure where the first group contains the first rectangle path, the working expression was:

```javascript
var s = content(1).content(1).size;
Math.min(s[0], s[1]) / 2;
```

This is a structure-dependent example, not a universal selector. Prefer deliberate stable names in new expression rigs, inspect the actual hierarchy, verify `expressionError`, and render the changing eye height. A script completing successfully does not establish that every embedded expression evaluated successfully.

Compute shared gaze/phase values once on a helper control when multiple body and eye expressions need them, rather than repeatedly evaluating a large motion calculation independently. Preserve keyframe ownership and a clean manual path. After a structural edit, verify expression references, instance overrides and packaged dependencies in the actual parent comp.
