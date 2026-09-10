---
name: ae-ui-mastery
description: Design knowledge for laying out a net-new frame with no reference — production design tokens, component anatomies with exact pixel specs, spacing/type/radius/shadow scales, 8px-grid and optical correction, colour harmony, typography pairing, visual hierarchy, and copy-ready layout patterns for hero, cards, stats, nav, pricing and footer.
---

# AE UI Mastery — Production Design Library

Production UI reference library: shipped design-system tokens plus ready-to-adapt HTML patterns. Look values up here; never invent them.

When you need to generate HTML for AE Vibecode:
1. Pick the closest **brand archetype** (premium dark tech / financial trust / playful Y2K / editorial / etc.)
2. Use that archetype's **exact tokens** (colors, type, spacing, radii)
3. Adapt the matching **component patterns** below
4. Compose into the user's requested layout

> **Author for editable layers (hard rule).** Every component below is built from real DOM: a styled
> container element + a separate text node. NEVER express a label, badge, chip, stat-pill, button or
> card as an `<img>` / `background-image` whose pixels already contain the text — that bakes the text
> into a flat picture and it can't be edited or animated in AE. Likewise express every gradient/glow as
> a CSS `linear/radial-gradient` (the build turns it into a native Gradient Ramp), not a generated
> image. Reserve generated images strictly for wordless photographic/illustrative content.

---

## §1. BRAND ARCHETYPES (pick one per design)

### A. Modern Dark Tech (best for SaaS, AI, dev tools)
```
PALETTE:
  bg-canvas      #08090b   (deeper than pure black)
  bg-surface     #131418   (cards)
  bg-elevated    #1c1d22   (modals, popovers)
  border-default #26282e   (subtle 1px)
  border-strong  #3a3b42   (hover states)
  text-primary   #fafafa   (off-white)
  text-secondary #a1a1aa   (zinc-400)
  text-muted     #71717a   (zinc-500)
  accent-primary #5e6ad2   (indigo) OR #7c3aed (purple)
  accent-success #10b981   (emerald)
  accent-warning #f59e0b   (amber)
  accent-danger  #ef4444   (red)

TYPE:
  Family: "Inter" (UI), "JetBrains Mono" (code/data)
  Display 72-96pt 700, leading 0.95
  H1 48-56pt 700, leading 1.0
  H2 32-36pt 600
  Body 16pt 400, leading 1.5
  Label 13pt 500 letter-spacing 0
  Tiny/eyebrow 11pt 600 UPPERCASE letter-spacing 1.5

RADIUS:
  Cards: 12px (most common) or 8px (tighter)
  Buttons: 8px
  Pills/chips: 999px (full)
  Inputs: 6px

SPACING (8px grid):
  4, 8, 12, 16, 24, 32, 48, 64, 96, 128

SHADOW (subtle):
  sm  0 1px 2px rgba(0,0,0,0.06)
  md  0 4px 12px rgba(0,0,0,0.12)
  lg  0 16px 48px rgba(0,0,0,0.24)
  glow 0 0 32px rgba(94,106,210,0.35) — on accent CTAs
```

### B. Trustworthy Premium Finance
```
PALETTE:
  bg          #0a2540   (deep navy) or #ffffff (light variant)
  surface     #163753 (on dark) or #f6f9fc (on light)
  border      #1f4068 (dark) or #e3e8ee
  text        #ffffff dark / #0a2540 light
  muted       #adbdcc dark / #425466 light
  accent      #635bff   (violet)
  accent-2    #00d4ff   (cyan)
  green       #00d924
  
TYPE:
  Family: "Sohne", "Inter" — display weight, generous tracking
  Display 64-80pt 700 tight tracking -2px
  Body 18pt 400 (READABLE)

RADIUS:
  Cards: 8px (utilitarian) — NOT 16+ (avoid mobile-app rounded)
  
SIGNATURE TOUCHES:
  Gradient surfaces: linear-gradient(135deg, #00d4ff, #635bff, #00d924)
  3D card hover lifts
  Subtle inner shadows on inputs
```

### C. Minimal Developer Monochrome
```
PALETTE:
  bg          #000000 (pure black) or #ffffff
  surface     #0a0a0a (dark variant)
  border      #1f1f1f / #eaeaea
  text        #ffffff / #000000
  muted       #888 (gray-500)
  accent      MINIMAL — usually monochrome, occasional blue #0070f3

TYPE:
  Family: "Geist Sans", "Inter" — clean, minimal
  Mono: "Geist Mono", "JetBrains Mono"
  
RADIUS:
  4-8px on cards, never 16+ (the archetype is geometric)
  
SIGNATURE: 
  Aggressive monochrome
  Heavy use of "geist mono" for everything numeric
  Single accent color (#0070f3 sparingly)
  Hairline borders #1f1f1f
```

### D. Premium Consumer Polish
```
PALETTE:
  bg light    #fbfbfd
  bg dark     #000000 (true black for OLED-style)
  surface light #ffffff
  surface dark  #1d1d1f
  text-primary #1d1d1f light / #f5f5f7 dark
  text-secondary #6e6e73
  accent      #0071e3 (system blue) — used SPARINGLY
  
TYPE:
  Family: "SF Pro Display" 72pt+ headlines, "SF Pro Text" body
  Mono: "SF Mono"
  
  Display: 96pt 700, tracking -0.005em
  Subheadline 28pt 400
  Body 17pt 400
  
RADIUS:
  Buttons: 980px (full pill)
  Cards: 18px (continuous corner, soft)
  Modal: 24px
  
SIGNATURE:
  Vast negative space (40% of layout is empty)
  Tiny "Learn more →" links in #0071e3
  ALWAYS centered hero text
  Generous 96-128px padding
```

### E. Warm Productivity
```
PALETTE:
  bg-canvas    #191919 dark / #ffffff light
  bg-surface   #2f2f2f / #f7f6f3 (warm gray)
  text         #ffffff / #37352f (signature dark brown-black)
  muted        #9b9a97
  accent       brown #d97706 OR purple #9b59b6 (selectable accents)

TYPE:
  Family: "Inter", "GT Walsheim" — friendly
  Body 16pt with 1.5 leading (READABLE)
  
RADIUS: 4-6px (utilitarian, low key)

SIGNATURE: warm undertones (5-10% brown tint in grays)
```

### F. Vibrant Nostalgia — Glossy Gradient
```
PALETTE:
  Gradients EVERYWHERE (mesh backgrounds)
  Hot magenta #ff3e9d
  Electric cyan #00d4ff
  Acid lime #c8ff5e
  Royal blue #4ea0ff
  Deep purple #7050ff
  
TYPE:
  "Space Grotesk" / "Space Mono" — futuristic
  
SIGNATURE:
  Glassmorphism (use rgba(255,255,255,0.12) bgs with thick borders)
  Big chunky shapes
  Liquid metal / glossy elements
```

### G. Brutalist Editorial
```
PALETTE:
  Off-white #f4f1ea (paper)
  Ink black #0a0a0a
  Single red accent #c8230a
  Ochre #d4a93a
  
TYPE:
  Helvetica Neue Black 144pt headlines
  IBM Plex Mono for metadata 11pt UPPERCASE letter-spacing 3
  
RADIUS: 0 (NEVER round, brutalist is sharp)

SIGNATURE: Asymmetric, harsh contrast, oversized text
```

---

## §2. COMPONENT ANATOMY (exact pixel specs)

### Button — Primary CTA
```
Heights (pick ONE per page): 40 | 44 | 48 | 56          (ae-ui-mastery (module: design-system) §7 owns the token)
Padding-X: 40->24, 44->24, 48->32, 56->32               (grid-safe; NOT height x 0.7 — off-grid)
Radius: 8px (modern web) | 980px (full pill) | 6px (utility)
Font: 14-16pt 500 medium (NOT 600+ for primary — looks shouty)
Color: white text, accent bg

ALWAYS include:
- Hover lift 0 4px 12px rgba(accent, 0.3) — colored shadow
- Active state slightly darker accent

Example (modern-dark-tech indigo CTA):
<div style="position:absolute; left:120px; top:480px; width:180px; height:44px;
  background:#5e6ad2; border-radius:8px; box-shadow:0 8px 32px rgba(94,106,210,0.35);">
  <div style="position:absolute; left:120px; top:493px; width:180px; height:22px;
    font-family:Inter; font-size:14px; font-weight:500; color:#fff; text-align:center;">
    Get started →
  </div>
</div>
```

### Button — Secondary (outlined)
```
Same height/padding as primary
Bg: transparent
Border: 1px solid border-default
Text: text-primary

Example:
border:1px solid #26282e; background:transparent; color:#fafafa;
```

### Card — Surface
```
Padding: 24-32px inside
Radius: 12px (most) | 16px (premium) | 8px (utility)
Border: 1px solid border-default
Shadow: optional 0 1px 2px rgba(0,0,0,0.04) for subtle lift
Background: bg-surface (1 step lighter than canvas)

Anatomy:
- Top label: 11pt 600 UPPERCASE muted, letter-spacing 1.5
- Title: 20-28pt 600 primary
- Body: 14-16pt 400 secondary
- Optional bottom action row
```

### Card — Pricing Tier
```
Width: 320-400px, Height: 480-600px
Inside structure (top to bottom):
  Top tier name + price area (height ~140px)
  Divider 1px
  Feature list 24px spacing between items (~280px)
  Divider 1px
  CTA button at bottom (height ~56px)

Highlighted/recommended tier:
  Border: 2px solid accent (not 1px)
  Inner glow: box-shadow 0 0 40px rgba(accent, 0.2)
  Small badge "Most popular" at top
```

### Input Field
```
Height: matches button height (40 | 44 | 48)
Padding: 12px 16px
Border: 1px solid border-default
Background: bg-surface OR transparent (border-only)
Radius: 6-8px (matches button radius)
Focus: border-color → accent, box-shadow ring 0 0 0 3px rgba(accent, 0.15)
Placeholder: muted
Font: 14-15pt 400
```

### Nav — Top Bar
```
Height: 64-72px (modern) | 56px (compact)
Padding: 24-32px horizontal
Layout: logo left, nav center OR right, CTA far right
Border-bottom: 1px solid border-default (subtle)
Background: bg-canvas (often) or rgba(canvas,0.7) with backdrop-blur(20px)

Logo area: max-width 120-160px on left
Nav items: 14pt 500, gap 32px between, color muted (active = primary)
Right cluster: search input + avatar + CTA → 40px gap from each other
```

### Sidebar — Vertical Nav
```
Width: 240-280px (standard) | 64-72px (icon-only collapsed)
Padding: 16-24px
Background: bg-canvas (deeper than main content)
Border-right: 1px solid border-default

Item structure:
  Height: 36-40px each
  Icon 20x20 + label 14pt 500, gap 12px
  Padding: 8px 12px
  Radius: 6px on hover bg
  Active state: bg accent at 15% alpha, text accent color
```

### Modal / Dialog
```
Width: 480px (small) | 640px (medium) | 800px (large)
Padding: 32-40px inside
Radius: 12-16px
Background: bg-surface
Border: 1px solid border-default
Shadow: 0 24px 80px rgba(0,0,0,0.5) — heavy elevation
Backdrop: rgba(0,0,0,0.7) full-screen behind

Inside (top to bottom):
  Header: title 20-24pt 600 + close X (24x24 hit area)
  Divider (optional)
  Body content with 24px top margin
  Footer: button row right-aligned, 24px top margin
```

### Stat Card
```
Min height: 120px
Padding: 20-24px
Layout:
  Top: label "REVENUE" 11pt 600 UPPERCASE muted letter-spacing 1.5
  Center: BIG number 32-48pt 700 mono (JetBrains Mono / SF Mono)
  Bottom: trend pill ↑ +24.8% green + "vs last month" muted
```

### Trend Chip / Status Pill
```
Size: 60-100px width × 24-28px height
Padding: 4px 10px
Radius: 999px (full pill) or 6px (rectangle)
Background: rgba(<accent>, 0.15) — LOW alpha tint
Border: optional 1px solid rgba(<accent>, 0.3)
Text: 11-12pt 600 in solid <accent> color
Icon: ↑ ↓ for trends, filled dot for status
```

### Avatar
```
Sizes: 24 | 32 | 40 | 48 | 64 (pick one per context)
ALWAYS circular: border-radius = size / 2
If colored: bg linear-gradient(135deg, color1, color2) with initials in white
If image: object-fit cover
Optional 2px white/bg border for "stacked avatars" group
```

### Section Divider
```
Height: 1px
Color: border-default
Vertical margin: 24-48px depending on density
Optional center label: small text on dark with 16px horizontal padding cutting through the line
```

---

## §3. LAYOUT PATTERNS (copy + adapt)

### Pattern: Hero with Code Visual
```
Layout: split horizontal — title left, code window right (60/40 or 55/45 split)

LEFT (text column, ~880px):
- Eyebrow chip "NEW · Multi-region support" small pill
- 96pt headline 3 lines (2 white + 1 gradient-fill accent line)
- 20pt subtitle muted, max-width 640px
- Button row: primary + secondary, 16px gap
- Optional logo strip "Trusted by ..." 1140px wide muted

RIGHT (code window, ~720x540):
- macOS-style title bar with 3 traffic lights + filename
- 12-line code block with syntax highlighting
- Floating shadow 0 32px 80px rgba(0,0,0,0.5)
```

### Pattern: Feature Grid (3-up or 4-up)
```
Container width: 1200-1440px max-width centered
Grid: 3 columns 1fr, gap 24-32px

Each feature card:
- Padding 32px
- Icon at top (48x48 colored accent shape)
- Title 20pt 600 (4-6 words)
- Body 14pt 400 muted (2-3 lines max)
- Optional "Learn more →" link at bottom
```

### Pattern: Stats Strip (single row hero supplement)
```
Container: full-width strip
Padding: 80px 0
Background: surface OR transparent

4 columns evenly spaced:
- BIG number 48-72pt 700 mono with accent
- Tiny label below 12pt UPPERCASE muted

Examples:
"99.99%"  →  "UPTIME SLA"
"45M+"    →  "API CALLS/DAY"
"30+"     →  "EDGE REGIONS"  
"<50ms"   →  "P99 LATENCY"
```

### Pattern: Pricing Table
```
3 tiers centered, equal widths 360px each, gap 24px
Middle tier elevated (border:2px accent, +scale 1.05, "Popular" badge)

Each tier:
- Tier name top
- BIG price center (48pt 700) + period subscript
- Divider
- Feature checklist 8 items (check icon + text 14pt)
- CTA at bottom
```

### Pattern: Footer (4-column link grid)
```
Background: bg-surface (slightly elevated from main)
Padding: 64-96px top, 48px bottom

Top row: 4 columns (Product/Company/Resources/Legal)
Each column has heading 12pt 600 UPPERCASE muted + list of links 14pt 400 with 12px gap

Bottom strip:
- Logo + copyright left
- Social icons right (24x24 each, muted)
```

### Pattern: Testimonial Block
```
Centered, max-width 720px
Big curly quote " 96pt 200 muted accent (decoration)
Quote text 28-32pt 400 italic primary
Author block below:
  Avatar 48x48 + Name 14pt 600 / Title 12pt muted
```

### Pattern: Logo Wall ("Trusted by")
```
Small label centered top "TRUSTED BY ENGINEERING TEAMS AT" 11pt 500 UPPERCASE muted letter-spacing 2
Row of 6 logos evenly spaced, muted color (40% opacity)
Each logo as wordmark text 18-22pt 600 muted (or actual SVG)
Total row width 1140-1280px
```

---

## §4-5. Hierarchy and composition -> ae-ui-mastery (module: design-system)

Visual hierarchy, optical centering, vertical rhythm, asymmetric balance and negative space are
owned by **ae-ui-mastery (module: design-system) §6**. Do not restate or re-derive them here.

## §6. COLOR HARMONY rules

### Building a palette from one accent:
1. Pick ONE vivid accent color (e.g., #5e6ad2 indigo)
2. Derive surface from accent at 4% saturation, 12% lightness → #16181f
3. Derive border at 8% saturation, 18% lightness → #26282e
4. Text white #fafafa
5. Muted = white at 50% opacity → equivalent #71717a
6. DONE — 5-color palette, harmonious

### Contrast minimums (WCAG):
- Body text on bg: ≥ 4.5:1 (AA)
- Large text (24pt+): ≥ 3:1
- For dark themes: body text #fafafa on #08090b is 18.7:1 (passes)
- Muted text MIN: #71717a on #08090b is 4.8:1 (passes)
- NEVER use less than 4.5:1 for paragraphs

### Status colors (universal)
- Success/positive: #22c55e (emerald) or #10b981
- Warning: #f59e0b (amber) or #f97316 (orange)
- Danger/negative: #ef4444 (red) or #f87171
- Info: accent color OR #3b82f6 (blue)
- NEVER reuse status colors as accents (pure status semantic)

---

## §7. TYPOGRAPHY PAIRINGS that work

| UI font | Numbers/code font | Use case |
|---|---|---|
| Inter | JetBrains Mono | Modern SaaS / B2B dashboard |
| SF Pro Display | SF Mono | Premium consumer |
| Helvetica Neue | IBM Plex Mono | Editorial / brutalist |
| Roboto | Roboto Mono | Android |
| Space Grotesk | Space Mono | Y2K / futuristic |
| IBM Plex Sans | IBM Plex Mono | Corporate / financial |

### Type scale (modular 1.25 — "major third")
```
10 → 12 → 14 → 16 → 20 → 24 → 32 → 40 → 56 → 72 → 96 → 128
```

### Weight pairing (max 3 weights per design)
- Display headline: 700 OR 800
- Subhead: 500 Medium
- Body: 400 Regular
- Labels/captions: 500 (gives them confidence at small sizes)

### Line-height
- Display 48-128pt: 1.0 to 1.1 (tight, dramatic)
- Heading 24-40pt: 1.15-1.25
- Body 14-20pt: 1.5 (READABILITY)
- Captions 10-12pt: 1.4

### Letter-spacing
- Display 48pt+: -0.02em to -0.04em (negative — looks tighter, premium)
- Body: 0 (default)
- Eyebrow/labels small UPPERCASE: +0.1em to +0.2em (positive — readability)

---

## §8-9. Anti-patterns and the pre-output check -> ae-ui-mastery (module: design-system)

The amateur-tell list and the pre-output gate are owned by **ae-ui-mastery (module: design-system) §9-10**. Run them
from there before emitting HTML.
