# AE Design System

This skill encodes the **invisible rules** that make professional landing pages feel premium. Without these, generated HTML uses random spacing (16px here, 19px there), inconsistent radii, mismatched type sizes — and looks amateur. With them, every value comes from a scale.

Load this BEFORE generating HTML.

---

## §1. Spacing Scale — 8px grid (standard UI convention)

**Only use these values for any spacing** (gap, padding, margin, left/top offsets between elements):

```
SPACE TOKENS:
  4   — tight inline gap (icon→text, between siblings of a chip)
  8   — small gap (between related items in a row)
  12  — compact gap (rows of a list, item internal padding y)
  16  — default gap (between paragraphs, card padding minimum)
  24  — section item gap (between cards in a grid)
  32  — section internal padding (card padding x for premium feel)
  48  — section separation (header → first section)
  64  — major separation (between unrelated sections)
  96  — page-level breathing room (above hero, below hero)
  128 — extreme separation (rare, between major page regions)
```

**Rule of thumb:** if you find yourself using `20px`, `28px`, `40px` — STOP. Round to the nearest token (16, 32, 48). Inconsistent spacing is the #1 amateur tell.

All `position:absolute` coordinates should be multiples of 4 (preferably 8).

---

## §2. Type Scale — hand-tuned display scale (NOT a uniform ratio)

```
TYPE TOKENS:
  10  — micro (legal text, tag, badge subscript)
  11  — caption (label, helper text) — uppercase + tracking 2px for chip labels
  12  — small (table cell, secondary metadata)
  14  — body small (UI default, button text)
  16  — body (paragraph text in landings, recommended reading size)
  20  — body large (intro paragraph, callout)
  24  — h4 (subsection title)
  32  — h3 (section title)
  40  — h2 (page section)
  56  — h1 (hero subtitle / secondary headline)
  72  — display (main hero headline)
  96  — XL display (premium splash hero)
  128 — XXL display (editorial / brutalist hero)
```

> **Not a uniform 1.25 "major third" scale** — the real step ratios vary (~1.1 at small sizes, ~1.33 at display sizes). **Do NOT extend it by multiplying ×1.25** (that breaks the rhythm); to add a new size, pick it by eye to fit the existing progression.

**Weight pairing — never mix more than 3 weights in one design:**
- Display headline: 700 Bold OR 800 ExtraBold
- Subhead: 500 Medium
- Body: 400 Regular
- Captions/labels: 500 Medium (gives them confidence even at small sizes)

**Line-height (leading):**
- Display 56-128pt → line-height: 1.0 (tight, dramatic)
- Headings 24-40pt → line-height: 1.15
- Body 14-20pt → line-height: 1.5
- Captions 10-12pt → line-height: 1.4

---

## §3. Radius Scale — pick a "vibe" and stick to it

```
RADIUS TOKENS:
  0    — brutalist, editorial, "no nonsense" (keynote bullet, magazine)
  2-4  — utilitarian SaaS (dense list items)
  6-8  — modern web default
  12   — premium cards
  16   — soft / friendly (media cards, social)
  24   — mobile-first / playful (iOS app, gaming)
  32+  — very rounded / "cute" (Y2K revival, kids products)
  999  — pill (buttons, tags, chips, search bars)
```

**Rule: ONE primary radius value across the design.** Pick one of {0, 4, 6, 8, 12, 16, 24}. Use it on ALL cards/panels/containers. Then 999 for pills. Two radii max. Three = inconsistent vibe.

---

## §4. Color System — value-driven hierarchy

A landing needs **6-8 colors total**. More = noise. Each color has a role:

```
ROLE                    PATTERN
─────────────────────────────────────────────────
BG (canvas)             very dark / very light, low chroma
SURFACE (cards)         one step closer to mid from BG
SURFACE-2 (elevated)    one more step toward mid
BORDER (1px dividers)   subtle, often 1-2% brighter than surface
TEXT primary            high contrast vs BG (white on dark, dark on light)
TEXT secondary          ~60% opacity of primary, OR brand-muted hex
ACCENT primary          ONE vivid hue — used SPARINGLY (buttons, key highlights)
ACCENT secondary        only if status: green=success, red=error, yellow=warn
```

**Dark theme recipe:**
- BG `#0d0e12` or `#0a0a0c` — true dark with subtle tint
- Surface `#16181f` (+~5% lightness)
- Surface elevated `#1d2028` (+~10%)
- Border `#2a2d38` (+~17%, still subtle)
- Text `#fafafa` (off-white, easier on eyes than #fff)
- Muted `#8b8e98` (60% lightness)
- Accent (single): one vivid hex like `#6366f1` (indigo), `#a855f7` (purple), `#10b981` (emerald), `#f59e0b` (amber), `#ef4444` (red)

**Light theme recipe:**
- BG `#fafafa` or `#ffffff`
- Surface `#f5f5f7`
- Surface elevated `#ffffff` with shadow
- Border `#e5e5e7`
- Text `#0a0a0c`
- Muted `#6b6f78`
- Accent: same vivid hexes

**60-30-10 rule:** 60% BG, 30% surface/text, 10% accent. If you see big areas of accent color, you're doing it wrong.

**Contrast floor (accessibility — verify, don't assume):** body text ≥ 4.5:1 vs its background; large text (≥24pt) and UI/icons ≥ 3:1. Check secondary/muted text against the **surface it sits on, not the canvas** — ~60%-opacity secondary text and muted grays (e.g. `#8b8e98`, `#6b6f78`) often pass on the canvas but FAIL AA on a mid surface. Bump lightness until it passes.

---

## §5. Shadow Scale — depth without noise

```
SHADOW TOKENS:
  none   — flat (brutalist, editorial)
  xs     — 0 1px 2px rgba(0,0,0,0.1)              — subtle elevation (form inputs)
  sm     — 0 2px 4px rgba(0,0,0,0.08)             — table rows, hover
  md     — 0 4px 12px rgba(0,0,0,0.12)            — default cards
  lg     — 0 8px 24px rgba(0,0,0,0.16)            — elevated cards, modals
  xl     — 0 16px 48px rgba(0,0,0,0.24)           — hero cards, dropdowns
  glow   — 0 0 32px rgba(<accent>,0.4)             — neon accent for CTAs in dark themes
```

**Rule: max 2 shadow levels per design.** Default cards = `md`. Hero/elevated = `lg`. Don't stack 5 different shadow depths.

---

## §6. Layout Principles — what makes a page feel "designed"

### 6.1 8px grid alignment
Every element's `left`, `top`, `width`, `height` should be divisible by 8 (or at least 4). When designing:
- Don't position `left: 37px` — make it `left: 32px` or `left: 40px`
- Sizes: prefer 240, 320, 400, 480, 560, 640, 720, 800 etc — multiples of 80

### 6.2 Content max-width
Avoid full-width text columns. Body text should max-width ~640-720px for readability. For dashboards, max-width of "main content" region usually 1280-1440px even on 1920px-wide layouts (center it).

### 6.3 Optical centering, not mathematical
Triangular icons (a play glyph) need to be shifted RIGHT by 1-2px for the visual center to align with the geometric center of a circle.
Text in a button: vertical-align by line-height (line-height = button-height for single-line buttons).

### 6.4 Vertical rhythm
Stack elements with **multiplied gaps**. Inside a card: header → 24px → body → 16px → footer. Between cards: 32px. Between sections: 64px. This creates rhythm.

### 6.5 The "3-2-1" rule for visual hierarchy
A landing page hero should have **at most**:
- 3 elements competing for attention (giant headline, key visual, primary CTA)
- 2 supporting elements (subtitle, secondary CTA)
- 1 accent color used for the primary CTA

More than this = visually noisy.

### 6.6 Asymmetric balance > centered everything
Most pro landings use asymmetric balance: big element on left, smaller stack on right. OR offset the hero off-center. Pure horizontal centering reads as default-template amateur.

### 6.7 Negative space is a feature
30-50% of any well-designed page is empty. Resist the urge to fill space. Add `padding: 96px` to hero containers, `margin-top: 64px` to next sections.

---

## §7. Component Anatomy — anatomical correctness

### Button (primary CTA)
- Height: 40, 44, 48, or 56 (pick one for the page)
- Padding x: use a grid-safe token — height 40→24, 44→24, 48→32, 56→32. (The formula `height × 0.7` is a rough guide only; it yields off-grid values like 33.6px that violate the §6.1 8px grid — prefer the token values.)
- Radius: page radius token OR 999 for pill
- Background: solid accent color OR `linear-gradient(135deg, accent, accent-dark)`
- Text: white, 500 Medium, 14-16pt
- NO drop shadow (modern), OR `glow` shadow with accent color

### Card
- Background: surface color (1 step lighter than BG)
- Border: 1px solid border color (subtle)
- Radius: page radius token (8, 12, or 16)
- Padding: 24-32px inside
- Shadow: optional `md` for elevation

### Input
- Height: matches button height
- Padding: x = 16, y = (height - fontSize) / 2
- Border: 1px border color
- Radius: matches buttons (page radius OR 999 pill)
- Background: surface OR transparent with border

### Avatar
- Always circular (radius = size / 2)
- Sizes: 24, 32, 40, 48, 64 (pick one per context)
- Initials text: bold, color = white OR contrast-of-bg

### Pill / Tag
- Height: 22-32 (small UI element)
- Radius: 999 (always pill for tags)
- Padding x: 8-12, padding y: 2-4
- Background: 10-15% opacity of the tag color
- Border: 1px solid 40% opacity of the tag color
- Text: solid tag color, 11-12pt UPPERCASE 500 Medium

### Divider
- Height: 1px
- Color: border token (very subtle)
- Margin y: 16-32 (depends on context density)

---

## §8. Hierarchy of decisions (the actual workflow)

When designing any region of a landing:

1. **Pick page radius.** One value: {4, 8, 12, 16, 24}. Stick to it.
2. **Pick comp BG color.** Then derive surface (1 step lighter), surface-2, border. From scale.
3. **Pick the accent.** ONE vivid hex.
4. **Pick the font pairing.** Sans + mono OR sans + serif. Maximum 2 families.
5. **Pick the type scale top.** What's the biggest text in the design? 56? 72? 96? Pick one — that's hero.
6. **Pick the spacing rhythm.** Inside cards: 24. Between cards: 32. Between sections: 64.
7. **Pick the shadow depth.** None / md / lg. One value for the design.
8. **NOW START LAYING OUT** — and every value you write down must come from these tokens.

Mid-way through layout, if you're tempted to write `padding: 22px`, ask: "is 22 in my scale?" If no, round to 24.

---

## §9. Anti-patterns — visible amateur signs

DON'T:
- Use 5 different border-radius values
- Mix `padding: 20px` and `padding: 24px` in the same design
- Use 4 different font weights
- Apply drop-shadow to text (almost never works in pro design)
- Center everything horizontally (lazy, looks like a template demo)
- Use full-width body text columns (eye fatigue)
- Place a button right against the edge of a card (no breathing room)
- Use accent color for more than 10% of pixels
- Have 2+ glow shadows on different elements
- Position elements at random pixel values (37px, 113px) — always grid-snap

DO:
- Snap everything to 4px or 8px grid
- Pick token values from §1 (spacing) and §2 (type) and §3 (radius)
- Use white text at 100% on dark, but BG-text-secondary should be muted gray, not pure gray
- Use one font family for UI, one for code/numbers if applicable
- Leave generous padding around hero elements
- Repeat the same accent color in 3 places (creates rhythm)

---

## §10. Quick check before outputting HTML

Before declaring the HTML ready, mentally check:

```
[ ] Every spacing value is in {4, 8, 12, 16, 24, 32, 48, 64, 96}
[ ] Every type size is in {10, 11, 12, 14, 16, 20, 24, 32, 40, 56, 72, 96, 128}
[ ] Every radius is one of {0, 4, 6, 8, 12, 16, 24, 999}
[ ] At most 2 radii used (primary + pill 999)
[ ] At most 2 font families
[ ] At most 3 font weights
[ ] At most 2 shadow depths
[ ] 1 accent color, used sparingly (~10% of pixels)
[ ] No element positioned at non-divisible-by-4 coordinate
[ ] Negative space is generous (page feels "breathable")
[ ] Visual hierarchy is clear: hero element is OBVIOUSLY largest
[ ] Every label/badge/chip/stat-pill is a styled <div> + a text node — NEVER an <img>/background-image with the text baked into the picture (text must stay an editable AE layer)
[ ] Every gradient/glow is a CSS gradient (→ native Gradient Ramp), NOT a generated raster image
```

If you can't tick all these, fix the HTML before output.
