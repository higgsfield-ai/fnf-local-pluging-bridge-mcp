# Native Layers

## Shapes and compositing

Use editable native shapes for vectors and footage for original raster media. Preserve separate paint regions, winding, holes, stroke alignment and paint order. Use parametric rectangles or ellipses only when their geometry matches the source; reconstruct asymmetric or smoothed corners from resolved paths. Resolved boolean geometry represents the visible result once; its operands remain provenance unless independently visible.

Obtain normalized cubic paths through supported source geometry operations or derive them from the complete source path. Convert quadratic segments to cubic controls and preserve subpath closure. After Effects tangent values are offsets from their vertices, not absolute control points. Do not replace unsupported path segments with straight lines.

Preserve sibling stacking and mask scope. A matte and the layers it affects must share the required composition context; duplicate a matte only for a necessary boundary and record its purpose. Apply isolated group opacity once. Keep collapse transformations disabled when enabling it would change clipping, opacity or effects.

Retain every gradient color and opacity stop and its geometry. Two-color approximations cannot silently replace richer gradients. Preserve group effects at their original compositing scope. Use a verified native equivalent for shadows, blur and blend modes; report unsupported behavior and affected nodes before choosing a fallback.

## Editable text

Use native text with the source content, installed font identity, size, fills, paragraph settings, baseline placement and styled ranges. Inspect the selected connection's text capabilities before relying on range styling. Missing fonts or unsupported mixed styling require a reported resolution; separate editable runs are acceptable only when their layout and behavior meet the requested result.

Distinguish point-text baselines from box origins. Check measured text bounds against the source line box without normalizing the text. Convert pixel letter spacing to native tracking by dividing by font size and multiplying by 1000; convert percentage spacing by multiplying by 10. Apply required integer rounding and inspect readback. Preserve line height and kerning independently.

## Native path assignment

Use this operation only when the chosen connection accepts inline After Effects scripting and its native path operation cannot express the required geometry. Supply an existing static path property owned by this import, equal-length arrays of finite two-dimensional vertices and relative tangents, and a Boolean closure value. Resolve these inputs from the mapped source; never interpolate unescaped source strings. The operation assigns one editable native path. It does not parse source geometry, create fills or validate rendered appearance.

```javascript
function assignNativePath(pathProperty, vertices, inTangents, outTangents, closed) {
    if (!pathProperty || pathProperty.numKeys || pathProperty.expressionEnabled) {
        throw new Error("A static import-owned path property is required.");
    }
    if (!vertices || !inTangents || !outTangents || vertices.length < 2 ||
        vertices.length !== inTangents.length || vertices.length !== outTangents.length ||
        typeof closed !== "boolean") {
        throw new Error("Complete matching path arrays and closure are required.");
    }
    var arrays = [vertices, inTangents, outTangents];
    for (var a = 0; a < arrays.length; a++) {
        for (var i = 0; i < arrays[a].length; i++) {
            var point = arrays[a][i];
            if (!point || point.length !== 2 ||
                typeof point[0] !== "number" || typeof point[1] !== "number" ||
                !isFinite(point[0]) || !isFinite(point[1])) {
                throw new Error("Path coordinates must be finite two-dimensional numbers.");
            }
        }
    }
    var shape = new Shape();
    shape.vertices = vertices;
    shape.inTangents = inTangents;
    shape.outTangents = outTangents;
    shape.closed = closed;
    pathProperty.setValue(shape);
}
```

When adding native property groups, reacquire properties invalidated by collection changes before assignment. Execute through the discovered evaluator's actual contract, then read back the assigned path. If neither a suitable native operation nor inline evaluation is available, report the missing path capability.
