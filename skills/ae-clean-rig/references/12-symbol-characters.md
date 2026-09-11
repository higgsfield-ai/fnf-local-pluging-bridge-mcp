# Symbol characters, pose catalogues and typographic scenery

Use this module when glyphs form an animal/object, when text assembles into a figure, or when the reference displays a sheet of changing poses. These are designed figures made from parts; treating them as arbitrary multiline ASCII strings often loses their anatomy and motion.

## Establish the visual vocabulary

Read [reference and motion](02-reference-motion.md) for reliable frame selection and cut mapping. Measure clean, held poses before fast intermediate ones. Separate body parts, labels, counters, selection blocks and scenery. Record each visible glyph's role, font/weight, bounds, baseline, orientation and colour. Verify the glyph in an actual native render: an unavailable character can leave a blank region without an expression error. Replace an unsuitable glyph with a small semantic path when necessary, such as a three-point knee or a simple rounded neck corner.

Use a stable character root and meaningful contact/attention anchors. Fit authored components once; do not continually centre or scale the whole figure from its changing `sourceRectAtTime` bounds. Bent ears, a blink or new legs must not shift the entire character unless the reference moves it.

The environment needs its own vocabulary. A V-shaped stem, an arrow stem, three round dots and a single sprout are different motifs, even if all read as flowers. Likewise, a biography table is not interchangeable with code. Match the content type, hierarchy, clusters, density, relative scale and negative space before animating it. Use distinct measured motif families instead of one repeated generic symbol.

## Model complete states, then connect them

Give each part a stable identity across states. Store only the attributes that change: position, rotation, scale, visibility, and sometimes the glyph itself. A compact table of a few authored poses is useful; an expression containing a drawing for every source frame is still dense animation.

Distinguish three independent things:

- **Construction:** which semantic parts are present as the figure assembles.
- **Pose:** the complete arrangement of the currently visible anatomy.
- **Root motion:** where the figure moves as a whole, including lift and contact.

For text-to-character assembly, carry the same parts through the line wraps and final arrangement. Avoid swapping to an unrelated whole-string drawing at the last moment. Preserve intentionally stepped changes with HOLD keys; use continuous curves only for continuous movement seen in the reference.

A compressed frog, released legs, full extension, airborne shortening and a landing can require different glyph combinations and connections. Stretching one long leg string cannot reproduce that vocabulary. Coordinate root lift with the actual feet and body pose; compare foot contact, body position and the outgoing-to-incoming handoff together. Use brief head/body offsets only where measured, such as a turtle head lagging its shell at landing.

For assembly, explicitly bound visibility before the first part and after the final part. For later uses, provide a complete pose library separate from the build animation; see [editable rigs](06-editable-rigs.md). A montage sampling time zero must not unexpectedly receive an empty or partial construction.

## Pose sheets and catalogues

Inspect the actual displayed states before choosing how many poses to author. Different columns may show asymmetric ears, a wink, a profile, bent wings or a different gait. Cycling two or three approximations across many labelled columns does not reproduce a catalogue with a larger vocabulary. Conversely, do not invent extra states because the layout has many cells.

Drive row labels and all character rows from a common phase/index when the reference advances them together. Derive row-specific poses through a deliberate mapping. Distinguish the pose index, the time represented by that index, movement of the sheet, and any framing/scale cut. Keep authored foot or body anchors stable across a row. Expose manual phase and useful row sizes without requiring edits to each copy.

Measure row count, ordering, pitch, crop, numbering, reveal order and final hold. Edge cropping may be intentional in a moving sheet; a hero figure unexpectedly leaving the frame is a different defect. Validate the selected hero pose as it becomes one column of the sheet. Check the last catalogue frame against the first biography/next-scene frame, including any one-frame overlay.

## Scenery assembly and large glyphs

Use measured births and state changes for plants, bubbles, bugs and seeds. Their first-frame population, growth stages and held end state matter. Do not add drifting, blinking or periodic motion merely because the motif suggests it.

When many symbols build a larger numeral or word, match its coarse silhouette, occupied cells, motif families and stroke weight before tuning births. Keep meaningful strokes, corners, seeds and blossoms independently editable if the reference changes them separately. Repeating one whole-cell pop can miss an assembly made of several independent parts.

Distinguish fixed reference artwork from a general text generator. A controller named Number should actually regenerate that number; otherwise label the value as reference information and expose a working Build/Phase control. Do not advertise arbitrary text or number replacement for an authored fixed mosaic.

## Evidence and limits

Render the nested main comp, not only isolated sources. Check initial assembly, completed pose, one asymmetric/extreme pose, a manual override, and the cut to the next scene. Inspect later consumers of the same sources. Use [validation](09-validation-delivery.md) to separate visual fidelity from technical control checks.

The DevDay study supplied these failure cases and repairs: partial spiders caused by reusing an entrance at time zero; missing knee glyphs; body/leg drift from incomplete pose logic; duplicated catalogue states; generic arrows replacing several flower families; code replacing biographies; and a six-frame early catalogue exit. These are diagnostic examples, not fixed animal counts, scene lengths, font choices or a claim that the reconstruction became pixel-identical.
