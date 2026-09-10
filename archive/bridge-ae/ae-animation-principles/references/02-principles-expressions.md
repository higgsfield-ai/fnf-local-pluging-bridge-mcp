# After Effects Animation Principles

This skill is the **12-Principles-of-Animation + After Effects expression cookbook**: for each principle it gives the concrete AE expression, keyframe, or Graph Editor technique to achieve it by hand.

> **Scope & related skills (differentiate — don't confuse):**
> - **This skill** = AE *expressions and UI techniques* per principle (ExtendScript expression strings you paste onto a property; F9 / Graph Editor workflows). It does **not** call ae-mcp tools.
> - For the **ae-mcp tool recipe** version of these principles (the same ideas expressed as `ae_*` keyframe/ease/expression calls), see **`ae-animation-principles`**.
> - **`ae-animation-principles (module: video-motion-graphics)`** = higher-level motion-graphics composition/sequencing guidance; **`ae-animation-principles (module: motion-designer)`** = design-direction / craft judgment. This skill is narrower: the per-principle AE-expression mechanics they both lean on.
>
> Assumes direct AE ExtendScript / expression context, not ae-mcp tools.


> **fps context:** All frame counts below (e.g. "0-10f", the Timing table) assume a **30 fps** composition unless you change the comp frame rate (see §9 Timing — 24 fps reads more cinematic, 30 fps smoother). Scale the frame numbers proportionally if your comp runs at a different rate.

## 1. Squash and Stretch

```javascript
// Expression for automatic squash/stretch — paste onto the Scale property.
// You keyframe the vertical scale (Y); X is derived to preserve volume.
s = transform.scale[1];          // s = current vertical scale % (the value you animate)
x = 100 + (100 - s) * 0.5;        // x = horizontal scale %: as Y drops below 100, X grows above it
[x, s]                            // Scale is a [scaleX, scaleY] array → return [x, s]
```

`s` reads the Y scale you keyframe; `x` is the compensating X scale; the returned `[x, s]` is the two-element Scale value AE expects (`[scaleX%, scaleY%]`).

Or manually:
- Keyframe Scale X and Y inversely
- When Y compresses, X expands
- Maintain volume (X * Y ≈ constant)

## 2. Anticipation

Timeline structure:
- **0-10f**: Wind-up (crouch, pull back)
- **10-12f**: Transition
- **12-30f**: Main action
- **30-40f**: Settle

Use Easy Ease on anticipation keyframes for smooth wind-up.

## 3. Staging

Techniques:
- Use depth of field (Camera > Depth of Field)
- Apply blur to background layers
- Use vignettes to direct focus
- Adjust opacity of secondary elements
- Light the main subject brighter

## 4. Straight Ahead / Pose to Pose

**Pose to Pose (recommended):**
1. Set keyframes at key poses
2. Fill in breakdowns
3. Use Graph Editor to adjust timing

**Straight Ahead:**
- Animate frame-by-frame
- Use Onion Skin (Layer > Onion Skin)

## 5. Follow Through and Overlapping Action

```javascript
// Delay expression for child layers — paste onto the child's Position.
// "Parent" is a PLACEHOLDER: replace it with the exact name of the layer you
// want this one to trail behind. At 30 fps, 0.05s ≈ 1.5 frames of lag.
thisComp.layer("Parent").transform.position.valueAtTime(time - 0.05)
```

Or:
- Offset child keyframes by 2-5 frames
- Use parenting with delayed wiggle
- Apply spring expression to end values

## 6. Slow In and Slow Out

- Select keyframes > F9 (Easy Ease)
- Graph Editor > Adjust bezier handles
- Steeper curve = faster movement
- Flatter curve = slower movement

```javascript
// Custom ease expression.
// ease() is AE's built-in interpolation function: ease(t, tMin, tMax, value1, value2)
// — it maps t from the range [tMin, tMax] onto [value1, value2] with an ease-in-AND-out
// (slow at both ends) curve. (linear() is the no-easing variant; easeIn()/easeOut() ease
// only one side.) Here t=time, the range is the layer's [inPoint, outPoint] in seconds,
// and the output animates from startValue to endValue.
ease(time, inPoint, outPoint, startValue, endValue)
```

## 7. Arc

Techniques:
- Draw motion path with Pen tool
- Use Position property's bezier handles
- Layer > Transform > Auto-Orient
- Apply path from shape layer to position

## 8. Secondary Action

- Animate main action first
- Add secondary on separate layer/property
- Offset timing slightly
- Secondary should complement, not compete

Example: Character waves → Hair follows → Clothing shifts

## 9. Timing

**`ae-animation-principles` is the single source of truth for timing** (the per-motion-type frame table at 30fps — snap / anticipation / action / settle / loop). Don't maintain a competing table here; if a value seems to differ, trust `ae-animation-principles`. Quick feel reference only: 2-4f snappy · 6-8f quick · 12-15f normal · 20-30f heavy · 40f+ dramatic. Frame counts assume **30 fps** (24fps cinematic plays the same count slightly faster — scale accordingly).

## 10. Exaggeration

```javascript
// Overshoot expression
amp = 15;
freq = 3;
decay = 5;
t = time - key(numKeys).time;
if (t > 0) {
  value + amp * Math.sin(t * freq * Math.PI * 2) / Math.exp(t * decay);
} else {
  value;
}
```

Push values 20-50% beyond realistic:
- Larger scales
- Wider rotations
- More dramatic timing

## 11. Solid Drawing

- Use 3D layers for depth
- Apply cameras with perspective
- Animate Z position
- Use light and shadow
- Consider volume in all poses

## 12. Appeal

Design principles:
- Clear silhouettes at every pose
- Smooth curves over sharp angles
- Consistent character proportions
- Pleasing timing patterns
- Clean, readable motion paths

## Essential Expressions

```javascript
// Wiggle
wiggle(frequency, amplitude)

// Loop
loopOut("cycle")

// Time remap
timeRemap = linear(time, 0, duration, 0, 1)

// Bounce
n = 0;
if (numKeys > 0) {
  n = nearestKey(time).index;
  if (key(n).time > time) n--;
}
if (n == 0) t = 0;
else t = time - key(n).time;
amp = 80; freq = 3; decay = 8;
value + amp*Math.sin(freq*t*2*Math.PI)/Math.exp(decay*t);
```

## Export Options

- **Lottie** *(OPTIONAL — only if you need a Lottie/JSON output)*: via the **Bodymovin** extension, a separate third-party plugin you install yourself (not part of stock After Effects); it exports the comp to a Lottie JSON file.
- **GIF**: Media Encoder
- **Video**: H.264, ProRes
- **Sprite Sheet**: Scripts > Render Sprite Sheet
