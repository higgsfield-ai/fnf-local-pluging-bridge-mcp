# Localized translation and typography

## Terminology and fonts

Build a project glossary for named vessels, characters, products, and objects. Distinguish official names, transliteration, literal meaning, and approved creative adaptation. Do not claim established cultural or literary usage without a source. Resolve material uncertainty using authoritative context and the user's preferred approach. Approved glossary entries take precedence over a new transliteration; project-specific naming conventions must not become universal rules.

Verify the actual font family, PostScript name, style, installation in After Effects, and glyph coverage for the required characters. A font filename or layer font label does not prove that substitution is absent. Check mixed styles and animated text states. Search the user's specified font source first; install only needed and authorized fonts, preserve existing fonts, and do not accept paid terms without approval. For new free fonts, use official sources and check their licenses.

Match replacements to the source's letter shape, weight, width, density, and typographic role. Coverage of one script does not establish coverage of another. Check the actual font file before asserting unsupported characters or unavailable weights. Explain substitution as a missing glyph in the selected font, rather than claiming an entire language is unsupported.

## Fitting multilingual text

When the user requests options before editing, show the problem and offer a small set of meaningful wording or layout choices. Wait for a choice when it changes the design. Make routine local adjustments within an approved style autonomously.

Prioritize meaning and natural phrasing before font size and line breaks. Preserve weight, hierarchy, color, strokes, backgrounds, and safe margins. Avoid disproportionate horizontal scaling. Evaluate visible weight and line spacing in the actual frame, not only nominal font size. Do not apply a fixed size reduction, tracking value, or leading adjustment to an entire language.

Preserve locale-appropriate punctuation and meaningful word groups. Adjust spacing around Latin text and numbers locally, without inserting spaces into protected identifiers. Do not apply Latin tracking conventions indiscriminately to Chinese, Japanese, or Korean text.

Treat browser typography advice as a visual goal only when relevant to the AE frame. Diagnose actual fonts, tracking, leading, text bounds, and rendered output; do not introduce CSS or claim browser or operating-system validation from an AEP inspection.

## Optical alignment and animated text

Identify the intended anchor: the entire line, the number itself, a number with an image, a key label, or a card. The geometric center of the text box may differ from the visual center of its content. Infer the user's correction from the current approved example and apply the same anchor in the target language.

For counters, separate or independently position the prefix, numeric value, and suffix when needed to preserve the intended numeric center. Account for digit count, separators, and glyph widths. Check at least the start, middle, and end of the count. Preserve the control value and animation instead of replacing them with static text.

A request to change spacing around a dynamic number concerns its separators or adjoining blocks. Preserve rounding, numeric formatting, speed, and unrelated tracking. Check any narrower spacing with the actual AE font rather than redesigning the line.

Anchor typewriter text to its intended full state or another stable reference so the line does not jump with each character. For key labels, check the key's background relative to the glyph and spacing to neighboring words. Account for anchor point, position, scale, parenting, 3D transforms, and camera projection. Compare before and after at the same viewing scale, including entrance, hold, and exit. Apply the entrypoint's dependency-scope rule when isolating a local correction; check that its boundaries introduce no jump. Do not recenter an entire list or chat for a change to one item.
