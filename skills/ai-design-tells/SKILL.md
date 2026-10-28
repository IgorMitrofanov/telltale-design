---
name: ai-design-tells
description: Use when designing, building or reviewing a user interface or its copy with a coding agent (landing pages, dashboards, admin panels, web apps, docs sites). A compact design process for agents (decide the mode, plan, build on tokens, verify in a browser) plus the visual and copy patterns that make a page look machine-generated, what to do instead, and the basics agents forget. Includes a scanner for HTML/CSS/JS/TSX/Vue/Svelte/Markdown.
---

<!-- design-tells: ignore-file (this file describes the patterns) -->

# Design for coding agents: process, tells, basics

Agents drift to the same defaults. Each is fine alone; together they make a page look generated and untrusted.
This skill gives a short process that avoids defaults by deciding first, a list of tells to catch what slips
through, and the basics that agents leave out.

**The brief wins.** An explicit instruction from the user, or the project's existing design system, overrides any
rule here. A rule is about defaults nobody chose; a deliberate choice stays, with one line saying why.

## 1. Decide before styling

1. **Subject, audience, place.** What is it, who uses it, where and under what light (an office at noon, a phone in a
   workshop, a control room at night). Pick light or dark from that, not from the category.
2. **Mode of the surface.** It changes almost every later choice.
   - *Persuade* (landing, launch page): one clear idea, bolder type, one signature visual moment.
   - *Operate* (admin, dashboard, internal tool): dense, familiar, fast to scan, one accent, motion only for state.
   - *Read* (docs, articles): measure, rhythm, quiet chrome.
   - *Experience* (games, showcases): immersion; the rules here bend most.
   A page can mix modes by region; decide per region.
3. **Existing system first.** Read the tokens, components, `DESIGN.md`/style guide and current pages. Refining is not
   redesigning: keep the identity, and ask before changing factual copy.
4. **A five-line plan.** One sentence of visual direction; palette (neutral bias + one accent); type roles (text face,
   data/mono face); layout idea; the one detail only this subject would have (its real units, terms, document
   conventions). Then cross out every item that is a category default (see section 5) and replace it.

## 2. Build a system, not a page

- **Tokens by role, not by value.** `--bg`, `--surface`, `--text`, `--text-muted`, `--line`, `--accent`, `--good`,
  `--warn`, `--bad`; type roles `display`, `heading`, `body`, `caption`, `data`. Components use roles only.
- **Dark mode is a second token set**, not an inversion: keep contrast, re-tune the accent, set `color-scheme` (and
  `theme-color` for mobile). No colour defined only inside a theme block.
- **Neutrals with a hue bias** towards the accent. Avoid pure `#fff` grounds and pure `#000`/flat grey text.
- **A small type scale:** 4–5 sizes, ratio about 1.125–1.2 for product UI (larger for Persuade). Body 16 px or more
  for reading, 14 px is acceptable in dense Operate tables. Lines 45–75 characters. `text-wrap: balance` on headings
  (no lone last word). Tabular figures where digits line up.
- **Spacing scale** on a 4 px base. More space above a heading than below it; gaps between groups clearly larger than
  gaps inside them. Group by proximity before adding boxes.
- **One small radius scale**; nested radii concentric (inner = outer minus padding). Pills only for tags and meters.

## 3. Build the interface

- **Hierarchy through weight, colour and space**, not size alone. Secondary text gets a lighter tone or weight. Squint
  test: primary, secondary and groups still read in order.
- **No cards by default.** Sections, lists, dividers and tables first; a card only for a real unit you act on; never
  cards inside cards.
- **Every component has all its states:** default, hover, focus-visible, active, disabled, loading, error, empty; and
  short, typical and very long content (long names, many digits, no data).
- **Interaction basics:** real links for navigation; state that should survive reload lives in the URL; focus is
  managed in dialogs and returns on close; hit targets at least 24 px (44 px on touch); never disable zoom or paste;
  destructive actions confirm in the page or offer Undo; a modal is not the first idea.
- **Data:** numbers right-aligned with tabular figures; units shown; totals that really add up; one finding per view;
  status never by colour alone (word or icon too); colour-blind-safe series; no filler charts.
- **Motion as state:** 150–250 ms in product UI, ease-out, animate `transform` and `opacity` only, never
  `transition: all`, no bounce/elastic easing, no page-load choreography in Operate mode; Persuade may have one
  signature moment. Always honour `prefers-reduced-motion`.
- **Interface copy:** buttons name the action ("Save key", not "Continue"); errors say what happened and how to
  recover; headings say what the block shows ("Last sync"); no design notes or prompt text leaking into the UI.

## 4. Verify, do not assume

1. Render it. Screenshots at about 390, 768 and 1440 px, plus one zoomed out (overall balance) and both themes.
2. List the top three problems, fix them, repeat; up to three rounds.
3. Keyboard pass: tab order, visible focus, Escape closes, Enter submits.
4. Run the scanner (section 7) and go through section 6.
5. Report what was checked and how. Never claim a check you did not run.

## 5. Tells: catch what slipped through

Visual tells. Fine as a deliberate choice; wrong as a default.

| Tell | Do instead |
|---|---|
| Hard gradients; gradient text | Flat colour; a gradient only if it carries meaning (a scale); an image or a scrim behind text |
| Purple + black, neon, near-black + cyan, cream + terracotta, stock pastels, rainbow | Palette from the subject; 1 accent + biased neutrals |
| Pure white ground; pure black text; grey text on a coloured ground | Tinted neutrals; text tinted from the surface hue |
| Shadows everywhere; "ghost card" (1 px border under a wide soft shadow); hard offset shadows | Border or spacing; a layered shadow only for real elevation (menus, dialogs) |
| Large soft radius on everything | One small radius scale, concentric when nested |
| Coloured stripe on the left of cards/banners | A full thin border in the status colour, or a status word |
| Glassmorphism, backdrop blur | Solid surfaces |
| Glowing spheres, blobs, dot grids, grain/noise, grid or stripe backgrounds, sketch-style illustrations, sparkle icons, animated arrows | Real content: product shots, data, a diagram of the real mechanism |
| Emoji as icons or bullets; a default icon set on every heading; an arrow on every link | No icon, or one consistent set used where it helps scanning |
| Hover lift/scale/glow on everything | Hover changes colour or underline |
| Inter / Geist / Space Grotesk as the unexamined default on brand surfaces | A face chosen for the subject; a familiar sans is fine for dense Operate UI if chosen |
| Monospace as a "technical" costume | Mono only for code, IDs and aligned data |
| Bento grids, "3 feature cards in a row", checkmark bullet lists, section numbers 01/02/03 without a real sequence | Structure from the content: a sequence, a comparison table, a real example |
| Eyebrow labels and "New" pills above headings; one word of a headline styled differently | A plain heading that names the thing |
| Hero-metric template (huge number, tiny label, three supporting stats) on a page that is not a dashboard | The fact in a sentence, or a real chart |
| Terminal-window mockups as decoration | A real command with its real output |
| 3 pricing tiers by default; fake dashboards of grey bars and rings | Only plans and data that exist |
| Uppercase letter-spaced labels everywhere | Sentence case; uppercase only for short codes or column heads in dense tables |
| Everything centred | Left-aligned reading order; centre only short, single statements |
| Unstyled browser defaults (focus ring removed, selection, scrollbars) | Style them to the palette; never remove focus without a replacement |

Copy tells.

| Tell | Do instead |
|---|---|
| Long dashes (—) as the main punctuation | Full stop, colon or comma; keep a dash only where the language's grammar needs it |
| "It's not X, it's Y" / «это не X, это Y» | Say what it is |
| Fake testimonials, invented logos, invented numbers | Real quotes with permission, or nothing |
| Vague claims ("powerful", "seamless", "next-generation") | A concrete fact: a number, a limit, an example |
| Triplets of adjectives; rhetorical questions as headings; middle-dot meta strings | One plain sentence |

## 6. Basics agents forget

| Basic | Done when |
|---|---|
| Real product demo | Screenshots or a short video of the actual product, not illustrations |
| Loading states | Skeletons or reserved space; no layout jump |
| Empty and error states | Each list says what to do when empty; each failure is visible and actionable |
| Terms of use and privacy policy | Needed for public products and anything that collects personal data, linked from the footer and such forms. Usually not needed for internal tools behind staff login. If the audience is unclear, ask the user; do not add legal pages or flag their absence by default |
| Accessibility | WCAG 2.2 AA contrast (APCA optional), visible focus (2.4.7), target size (2.5.8), labels on inputs, no text in images |
| Responsive | Works at 360–400 px without horizontal scroll; tables and code scroll in their own box |

## 7. Scanner

```bash
python scripts/check_design_tells.py path/to/project             # report
python scripts/check_design_tells.py page.html --strict           # exit 1 if anything is found
python scripts/check_design_tells.py src --json                   # for CI and agents
```

It finds candidates (file:line) for a person or agent to judge; it never edits files. Mark a deliberate use on its
line with a `design-tells: ignore` comment, or a whole file (a style guide) with `design-tells: ignore-file`.
Report each finding as fixed, kept on purpose (with the reason), or not applicable.

## Sources

Paraphrased in our own words: Anthropic `frontend-design` and `canvas-design` skills (Apache-2.0); Impeccable by Paul
Bakaus (Apache-2.0); taste-skill (MIT); Vercel Web Interface Guidelines (MIT); OpenAI, "Designing delightful frontends
with GPT-5.4" (ideas only); Refactoring UI (ideas only); Laws of UX (named principles); WCAG 2.2 (success criteria by
number); Apple HIG and Material Design (ideas only). The original list of tells came from a community post.
