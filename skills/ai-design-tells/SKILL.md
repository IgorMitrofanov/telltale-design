---
name: ai-design-tells
description: Use when designing, building or reviewing a user interface or its copy with a coding agent (landing pages, dashboards, admin panels, web apps, marketing pages, README visuals). Lists the visual and copy patterns that make a page look machine-generated, what to do instead, and the basics agents tend to forget (real product shots, loading/empty/error states, legal pages, accessibility). Includes a scanner script for HTML/CSS/JS/TSX/Vue/Svelte files.
---

<!-- design-tells: ignore-file (this file describes the patterns) -->

# AI design tells

Pages built by coding agents drift towards the same defaults. Each default is fine alone; together they make a page
look generated and untrusted. Use this list while designing, and run the scanner before handing work over.

**Judge by purpose, not by rule.** A KPI tile row is right on an operations dashboard and wrong on a landing page.
A tell is a problem when it is a default nobody chose. If a pattern is a deliberate, justified choice, keep it and
say why in one line.

## 1. Visual: do not reach for these by default

| Tell | Why it reads as generated | Do instead |
|---|---|---|
| Hard gradients (buttons, headings, backgrounds) | The single most common agent default | Flat colour; one accent; a gradient only if it carries meaning (a scale, a heat map) |
| Purple + black, neon colours, generic pastels, rainbow palettes | Stock "AI startup" palettes | Derive a palette from the subject (brand, material, domain); 1 accent + neutrals with a slight hue bias |
| Pure white background (#fff) everywhere | Unconsidered default | An off-white or tinted neutral; design a dark theme too |
| Shadows on everything | Flattens hierarchy | Use a border or spacing; a shadow only for real elevation (menus, dialogs) |
| Soft large corner radii on every element | Everything looks the same "friendly" blob | One small radius scale; square tables and data |
| Coloured stripe on the left of cards/banners | Template tell for "callout" | A full thin border in the status colour, or a status word/icon in the text |
| Glassmorphism ("liquid glass"), backdrop blur | Trendy default, hurts contrast | Solid surfaces |
| Radial glowing spheres, blobs, dot grids, sparkle icons, animated arrows | Decoration without information | Real content: product screenshots, data, diagrams of the real mechanism |
| Emoji as icons or bullets | Cheap, inconsistent across platforms | No icon, or one consistent icon set used sparingly |
| Default icon set sprinkled on every heading (e.g. Lucide everywhere) | Icon soup | Icons only where they help scanning or recognition |
| Hover animations on everything (lift, scale, glow) | Motion without purpose | Hover changes colour/underline; animation only for state changes; honour `prefers-reduced-motion` |
| Inter / Geist / Space Grotesk as the unexamined default | The default stack of generated UIs | Choose a typeface for the subject; pair a text face and a data/mono face |
| Bento grids, "3 feature cards in a row", checkmark bullet lists | The template landing page | Structure from the content: a sequence, a comparison table, a real example |
| Terminal-window mockups as decoration | Signals "dev tool" without showing anything | A real command with its real output, or nothing |
| 3 pricing tiers by default | Invented business model | Only the plans that exist |
| Uppercase letter-spaced micro labels everywhere | Dashboard template tell | Sentence-case labels; uppercase only for very short codes |

## 2. Copy: do not write these

| Tell | Do instead |
|---|---|
| Long dashes (—) as the main punctuation | Full stop, colon or comma; keep a dash only where the grammar of the language needs it |
| "It's not X, it's Y" / «это не X, это Y» constructions | Say what it is, directly |
| Fake testimonials, invented logos, invented numbers | Real quotes with permission, or nothing |
| Vague claims ("powerful", "seamless", "next-generation") | A concrete fact: a number, a limit, an example |
| Triplets of adjectives, rhetorical questions as headings | One plain heading that names the thing |

## 3. Basics agents forget: check these are present

| Basic | What "done" looks like |
|---|---|
| Real product demo | Screenshots or a short video of the actual product, not illustrations |
| Loading states | Skeletons or reserved space for content that loads; no layout jump |
| Empty and error states | Every list/table says what to do when it is empty; every request failure is visible and actionable |
| Terms of use and privacy policy | Needed for public products and anything that collects personal data: linked from the footer and from such forms. Usually not needed for internal tools (admin panels, dashboards behind login for staff). If the audience is unclear, ask the user; do not add legal pages or flag their absence by default |
| Accessibility | Contrast AA, keyboard focus visible, labels on inputs, `prefers-reduced-motion`, no text in images |
| Responsive layout | Works at 360–400 px without horizontal scroll |

## 4. How to use

1. While designing: pick palette, type and layout from the subject before writing code; avoid section 1 and 2 by default.
2. Before handing over: run the scanner and go through section 3.

```bash
python scripts/check_design_tells.py path/to/project            # report
python scripts/check_design_tells.py path/to/file.html --strict  # exit 1 if any finding
```

The scanner is a heuristic: it finds candidates (file:line) for a person or agent to judge. It never edits files.
Mark a deliberate use on its line with a `design-tells: ignore` comment.
Report each finding as fixed, kept on purpose (with the reason), or not applicable.
