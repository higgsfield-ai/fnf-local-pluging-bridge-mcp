# Practical editability and exposed controls

## Make normal edits practical

Native layers alone do not establish editability. Give each meaningful component a clear source for its wording, colour, geometry, or replaceable media; name those sources and put shared movement on the object rig. Link visual construction copies to one editable source when they represent the same word or object. Independently meaningful elements must remain individually selectable.

Where normal content changes affect layout, make bounds, cursors, anchors, padding and media fitting follow the content. Expose only useful controls; avoid requiring the user to repair many hidden copies or dependent keys for a routine edit. Preserve deliberate framing and motion when adding automatic fitting.

Before delivery, test a representative real edit in a temporary duplicate: use a longer word or phrase, change an object's colour or dimensions, or replace a photograph as appropriate. Render it during an animated state and verify dependent elements still align, then retain the intended original content. Report any fixed layout or baked material that limits editing. A field of independently moving particles may legitimately contain many simple circles; distinguish that from building one object's surface out of tiny traced fragments.

## A usable controller is part of the design

Use a clearly named null with native Slider, Color, Checkbox and other appropriate controls. Put the few everyday controls first; document units, defaults and the useful range. Offer Essential Properties on the parent instance when supported. Explain whether a control is a source default or an instance override: changing the source may appear ineffective when that instance already overrides it.

Separate manual control from optional demonstration playback. A user animating Slide, Look or Blink must not fight a hidden time-driven expression. Preserve their existing keys during cosmetic fixes. Shared phase controls should drive parts of one gesture; do not make each sublayer run an unrelated timer.

Preserve unique media/source identity where independent editing is requested. Duplicating the master comp does not automatically duplicate its nested sources. Use separate CONTENT comps for independent sets, and retain shared sources only where changes are intended to propagate. Test this by replacing one item and checking another.

Keep the main comp readable: semantic object precomps, a small number of clearly named controls, a camera if relevant, and scene/background layers. Within a component, keep independently meaningful body parts, captions and media easy to find. Keep technical helpers unobtrusive without hiding the controls the user needs.

Package an internal shared motion library as an actual project dependency when one is used. Do not rely on a comp-name expression alone to make another comp portable; verify that exporting or importing the character/rig retains its required source comps. Avoid unexplained hard-coded references to unrelated projects.
