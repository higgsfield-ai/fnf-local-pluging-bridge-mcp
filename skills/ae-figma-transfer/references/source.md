# Source Capture

## Complete source

Read the complete selected subtree without modifying, detaching or flattening the source. Capture node identities, local dimensions, transforms, child order, visibility, paint stacks, vector geometry, text and styled ranges, masks, effects and original media references. Include hidden nodes and boolean operands for provenance even when they do not produce separate layers. Preserve text and line breaks before applying style offsets.

Prefer resolved fill and stroke geometry for booleans and outlined strokes. Retain vector paths or networks when native reconstruction needs them. An exported image of a frame cannot replace its geometry. Obtain a separate visual reference of the exact selected root for final comparison.

Resolve read errors and missing geometry before construction. Inspect the actual connection's payload limits. Use its supported pagination or complete artifact retrieval when needed; do not reconstruct a supposedly complete capture from truncated responses. Keep one consistent source revision across reads, and recapture if it changes during extraction.

## Original media

Resolve original bytes for every image paint used by visible content, including strokes, text fills and patterns. Verify nonempty data, image dimensions and content identity. Store required footage in a durable per-transfer location readable by the After Effects host. A temporary remote URL or a path on another host is not an imported footage file. Reference captures may support review but must not substitute for original photographs.

## Transfer plan and identity

Before mutation, classify each node as native content, footage, a retained container, a structural node, a boolean operand, an intentional hidden omission or an unsupported feature. Match required operations to actual source features; resolve material unsupported cases before building affected content.

Record the source file, root and node identities, representation, fingerprints, child order, media dependencies and limitations. After construction, bind them to actual composition and layer identities returned by the application. Distinguish source state from verification state. Keep this map in supported project metadata or a prose Markdown sidecar; do not depend on a bundled converter or an external structured-data manifest. Save the source reference and original media as workflow outputs outside the skill package.
