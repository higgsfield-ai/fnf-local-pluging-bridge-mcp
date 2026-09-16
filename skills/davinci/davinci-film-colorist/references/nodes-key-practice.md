# Nodes and Keys

## Processing and scope

A Corrector can contain several operations, but the skill's chosen task separation must correspond to real processing. Labels and badges are aids, not evidence of operation or order. The Corrector has a fixed internal order: an OFX CST and an assigned LUT occupy different stages, and HSL curves and Color Warper can act after the assigned LUT. When separating an existing Corrector, preserve each operation's position relative to the transform and transfer individual operations rather than duplicating the whole grade. Confirm the current manual's order for the actual tool and version.

Trace RGB connections and key connections separately. A node's index and screen position do not determine order. The last Clip node may still feed Group, Timeline, or managed output processing. Changing a node's processing space or gamma changes control behavior; it is not an explicit image conversion equivalent to a CST.

Local and Remote describe grade-version relationships, while Clip identifies graph scope. Remote grading can share changes among source instances across timelines. Local in a Master Timeline has special relationships and is not sufficient evidence of isolation. Shared-node locking prevents editing without unlinking. Copying a still or converting a remote grade to local can retain Shared references.

## Mixers and domains

Serial processing feeds the preceding result into the next operation. Independent Parallel branches receive a common source and combine corrections without input priority; do not assume a simple average of RGB values. Layer mixing introduces compositing priority and modes. In ordinary composition its lower input has priority, determined by connections to ports rather than screen placement. Check other Composite Modes individually.

Keep all RGB inputs of a mixer in compatible gamut, gamma, and processing stages. A mixer does not automatically reconcile camera log and a displayed image. A shared upstream change can affect every branch and its selection, even when the branches do not alter one another's selection input.

Splitter copies a chosen channel into its branch's internal channels; Combiner extracts its assigned channels to reconstruct RGB. It is not a combination of three full-color grades or three masks. Inspect channel-specific work against the actual source defect and the node's processing domain.

## Matte processing

Key Mixer combines masks rather than color images. Trace the source and exact input link before changing Matte, Input Invert, or Output Invert. Confirm clean selected, excluded, overlapping, and outside areas in the matte view. Do not extrapolate unverified equations for soft alpha from binary regions.

At a Corrector, the incoming key normally intersects the internal qualifier, which normally intersects the window. Mask modes alter the relevant combination. Check the receiver's internal selections and inversions rather than assuming that an upstream matte alone defines the result. A serial RGB connection does not carry a previous node's subject mask into later corrections.

An Outside node reuses the previous key with input inversion. A receiver's additional Window or Qualifier further affects that key. Input inversion is not final-output inversion. For specialized matte refinement, a key can feed a neutral Corrector's RGB input and its processed grayscale result can feed a recipient's key input; the recipient's color input stays on the main RGB path. Verify a neutral baseline before applying a matte change.

Key Output Gain attenuates a Corrector's contribution, not the image's brightness by the same proportion. Values above unity affect partially weighted key areas without guaranteeing an equivalent multiplication of the grade. Regulate branch contribution on its Corrector and inspect each OFX alpha and Blend contract. Do not attenuate technical normalization to solve exposure.

## Animation and restoration

Record graph, version, node, subtrack, and Auto-Keyframe before animation. All and Color track selections have different scope. For a single Window, place a static or dynamic keyframe on the intended Window subtrack; merely expanding that track does not select the keyframe target. Turning Auto-Keyframe off does not prevent modification of existing keys. Clip and Timeline animation are separate.

Disable preserves parameters; Reset changes them. Global bypass may leave managed transforms active and can affect more than the selected node. Reenabling all nodes may enable nodes that were intentionally disabled before the test. Read back individual enabled states and evaluate the saved baseline, including keys and animation.
