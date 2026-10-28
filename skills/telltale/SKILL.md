---
name: telltale
description: Use when designing, building or reviewing a user interface or its copy with a coding agent (landing pages, dashboards, admin panels, web apps, docs sites). A compact design process for agents (decide the mode, find a distinctive idea, plan, build on re-themable tokens, verify in a browser) plus the visual and copy patterns that make a page look machine-generated, what to do instead, the basics agents forget, and plain-writing rules (from ASD-STE100) for interface copy and for the agent's reports to the person. Includes a scanner for HTML/CSS/JS/TSX/Vue/Svelte/Markdown.
---

<!-- design-tells: ignore-file (this file describes the patterns) -->

# Design for coding agents: process, tells, basics

Agents drift to the same defaults. Each is fine alone; together they make a page look generated and untrusted.
This skill gives a short process that avoids defaults by deciding first, a way to find an idea worth building, a
list of tells to catch what slips through, and the basics that agents leave out. Avoiding tells keeps a page
from looking generated; only an idea makes it good.

**Aim for portfolio grade.** The goal is a page a strong designer would be proud to show, not a page with nothing
wrong. Calm and minimal are choices for when the brief asks for them, never the safe fallback. The checks in this
skill are a gate at the end; spend most of the effort on the design itself.

**The brief wins.** An explicit instruction from the user, or the project's existing design system, overrides any
style default here. A deliberate choice stays, with one line saying why. Separate measurable requirements,
design heuristics and personal preferences. A favourite colour does not establish contrast or usability.

## 1. Decide before styling

1. **Subject, audience, place.** What is it, who uses it, where and under what light (an office at noon, a phone in a
   workshop, a control room at night). Use established theme preferences; otherwise recommend a theme from the
   context. State assumptions instead of treating the product category as evidence.
2. **Mode of the surface.** It changes almost every later choice.
   - *Persuade* (landing, launch page): one clear idea, bolder type, one signature visual moment.
   - *Operate* (admin, dashboard, internal tool): dense, familiar, fast to scan, a restrained accent hierarchy,
     motion only for state.
   - *Read* (docs, articles): measure, rhythm, quiet chrome.
   - *Experience* (games, showcases): immersion; the rules here bend most.
   A page can mix modes by region; decide per region.
3. **Existing system first.** Read the tokens, components, `DESIGN.md`/style guide and current pages. Before refining,
   name up to three strengths to preserve and the problems to solve. Keep the identity unless the brief asks for a
   new direction, and ask before changing factual copy.
4. **A five-line plan.** One sentence of visual direction; palette roles and intended character; type roles (text
   face, data/mono face); layout idea; the one detail only this subject would have (its real units, terms, document
   conventions). Review category defaults (section 5) against the brief. Keep those that fit; replace those that do not.

### Find the idea

Do this before the plan is final. Restraint without an idea gives a correct page that nobody remembers.

1. **Mine the subject's world.** List five things only this subject has: objects, materials, documents, units,
   rituals, places (film: slate, timecode, contact sheet; coffee: roast curve, origin label, grind size). One of
   them becomes the visual idea, as structure or content, never as clip art.
2. **Write three concepts, one sentence each,** from different starting points: a structure (the page as a contact
   sheet), a material (ledger paper, enamel sign, newsprint), a gesture (one huge number, one full-bleed photograph).
   Pick the one that fits the brief and the mode, and say why in one line.
3. **Spend one bold move per view.** A jump in scale, one saturated colour field, an oversized photograph, a typeface
   with character, a grid broken on purpose. Keep everything around it quiet. Two bold moves fight; none leaves the
   page anonymous. In Operate mode the move is small: a signature numeral style, one chart done beautifully, a
   crafted empty state. **The bold move carries content:** a map, a plan, a drawing of the real mechanism, real data
   at scale, a photograph cropped hard. A flat colour field with a big headline is the safe default, not a bold move.
4. **Borrow from outside the category.** Name two references from other fields (a magazine, a transit map, a product
   label, an instrument panel) and what you take from each: a grid, a type treatment, a colour habit. Competitors
   show what to avoid copying.

If the person gave references, start from them and say what you take and what you leave.

### Choose a direction with the person

Follow the existing system and stated preferences first. When the direction (layout, type or palette) is open:

1. Show two or three distinct directions as rendered UI on the same representative screen and content. Vary only what
   is being compared: for style directions, vary the approach; for palettes, hold layout, type, content, imagery,
   state and viewport fixed. Include the existing design as a reference when refining. Render every theme the product
   will support. Swatches alone are not a preview.
2. Check contrast (section 2) before presenting. If the original fails, label it and offer a corrected version.
   Explain each direction in one sentence and ask which is closest.
3. Accept a choice, a mix or plain feedback ("warmer", "less busy"). Turn it into targeted changes and say what
   changed. Lock accepted values and roles; regenerate only what is open. Tell an exact value from a flexible
   preference ("keep it blue"). Keep the previous candidate so the person can go back; reopen rejected directions
   only when asked.
4. Record chosen tokens, locks, preferences and rejected directions in `DESIGN.md` or the existing design record.
   Stop when the direction is clear. If the person delegates, choose, explain and proceed. Do not make this an
   approval step for routine work; without a response, use a clearly provisional choice and continue.

### Generate palette candidates

- **Anchor and harmony:** start from an approved colour; try monochromatic, analogous, complementary or
  split-complementary relationships.
- **Reference image:** extract dominant and accent colours as starting points. They do not decide which colour is fit
  for text, controls or backgrounds.
- **Lock and complete:** keep chosen colours fixed and fill in the rest; in later rounds change only what was asked.

Expand seeds into tonal families (lighter and darker accent and neutral shades), then pick the tones each role needs.
A seed is an input, not necessarily the action fill; a locked role value stays exact. If a locked colour fails contrast
in its role, explain the conflict and offer another use or a derived shade. Work locally in a space with separate
lightness, chroma and hue (OKLCH), map results to the target gamut, and check the rendered pairs. No palette service or
account is needed; the services in Sources show interaction patterns only.

## 2. Build a system, not a page

- **Tokens by role, not by value.** `--bg`, `--surface`, `--text`, `--text-muted`, `--line`, `--accent`, `--good`,
  `--warn`, `--bad`; type roles `display`, `heading`, `body`, `caption`, `data`. Components use roles only.
- **Pair foreground and fill roles.** Define text/icon colours for the surfaces they sit on, such as `--on-accent`
  with `--accent`. Add a quieter `--accent-container` / `--on-accent-container` pair only when needed. A foreground
  that passes on one fill is not automatically valid on another. Keep role mappings consistent across breakpoints.
- **Re-themable by construction.** Every colour a component uses comes from a role token; no colour literals outside
  the token blocks (photographs and media excepted). Derive hover, pressed, container and focus tones from the accent
  with `color-mix()` or relative colour (`oklch(from var(--accent) calc(l - 0.08) c h)`), so a new brand colour updates
  them. Keep the palette in one documented token block. **Re-theme test:** swap the accent for distant hues (at least
  a light yellow, a dark teal and a red), render, rerun the contrast check and look at the screenshots: every large
  field must still look intended, not muddy or garish. Fix the derivation, not the components.
- **Supported themes have complete token sets.** Select suitable tones for each role in each supported theme;
  for dark mode, re-tune contrast and accents instead of inverting colours. Set `color-scheme` (and `theme-color`
  for mobile).
- **Colour relationships are starting points.** Try one hue at different lightnesses, neighbouring hues, or a
  contrasting pair. Neutral and tinted surfaces, including white, black and grey, are all valid. Start with calmer
  large surfaces and a clear primary action accent; adjust saturation and area to the intended character. Extra
  accents need a role. Semantic status and data-series colours are separate from the interaction accent hierarchy.
- **Check colour where it is used.** Apply WCAG 2.2: text at least 4.5:1 (3:1 for qualifying large text); visual
  information needed to identify controls, states or meaningful graphics at least 3:1 against adjacent colours,
  subject to the criteria's exceptions. Check actual foreground/background pairs, transparency, image backgrounds
  and relevant states. Do not require decorative borders or the difference between hover and default to meet 3:1.
  Convey status and selection with a visible word, shape or icon as well as colour. A contrast pass does not prove taste.
- **A small type scale:** 4–5 sizes, ratio about 1.125–1.2 for product UI (larger for Persuade). Body 16 px or more
  for reading, 14 px is acceptable in dense Operate tables. Lines 45–75 characters. `text-wrap: balance` on headings
  (no lone last word). Tabular figures where digits line up.
- **Keep letterforms distinct.** Start from the typeface's normal spacing; tighten only after reading the actual
  rendered words. Check ambiguous combinations such as `rn`/`m`, `cl`/`d` and `I`/`l`/`1` where they occur.
  Adjust spacing, weight or typeface when glyphs merge. Fit narrow layouts through size or wrapping without
  sacrificing legibility. There is no universal safe negative tracking value for every font and size.
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

### Make it memorable

- **Typography carries the voice.** Choose the display face for character (structure, width, contrast, era), then a
  text face that differs in structure and agrees in proportion. Use the range the faces offer: real scale contrast
  (ratio 1.25–1.5 for Persuade), weights far apart, optical sizes where they exist. Break headlines by sense, not by
  width. Use real quotes and apostrophes, and the dashes the language requires.
- **Composition with tension.** Choose a grid, then break it once on purpose: asymmetry, a strong axis, a wide margin
  on one side, a photograph cropped hard or running off the edge, an element crossing a boundary. Vary the rhythm so
  sections differ in height and layout. Give each view one large thing for the eye to land on.
- **Art-direct the images.** One treatment for all photographs (crop, colour, framing). Crop to the detail that tells
  the story. Real product shots and real data beat illustration. With no images, let type, data or a diagram carry
  the page; never leave grey placeholders.
- **Commit to the colour.** A quiet palette is a choice, not a default. When the brief allows, give the accent real
  area: a coloured section, tinted photography, a field behind real content. Keep one idea and check contrast where
  text sits. **Large fields never use the raw brand value.** Derive the field tone per theme with clamped lightness
  and chroma. A light brand (such as yellow) turns muddy when darkened: keep it as a light field with dark text, or
  put a dark neutral field behind it and use the brand only as accent. Check every large field by eye with a yellow,
  a teal and a red brand.
- **Fill the whole page, not only the first screen.** A side panel or colour field that stops where its content
  stops leaves an empty half beside a long form. Make it sticky, let a summary follow the form, or let the visual
  continue. Check the zoomed-out full-page screenshot for dead areas.
- **Enough visual material.** On a Persuade page every major section has its own composed visual: a drawing, a
  diagram, a map, data drawn at scale, a type composition. Text, rules and buttons alone read as a wireframe. Vary
  the visuals; do not repeat one device in every section.
- **Details that reward a second look.** Optical alignment (icons, quotes and round letters nudged until they look
  aligned), one stroke width for icons and rules, digits that line up, a crafted empty state, focus rings in the
  palette.

## 4. Verify, do not assume

1. Render it. Screenshots at about 390, 768 and 1440 px, plus one zoomed out (overall balance) and all supported themes.
   For before/after, use the supplied original and the new version at the same viewport, theme and comparable state.
   When comparing palettes, also hold typography, content, media and layout fixed.
   Read the actual headings, actions and key numbers at their intended size and in any reduced preview being delivered.
   Correct text in the DOM is not proof of readable letterforms. Check wrapping just above and below affected breakpoints
   after changing type or tracking; inspect the rendered result, not only overflow measurements.
2. **Critique the beauty first, twice.** Before any accessibility or scanner fixes, look at the full-page screenshot
   as a design director: where is the page flat, empty, generic or timid? Push scale contrast, the bold move and the
   visual material; then render and look again. Fix accessibility afterwards without flattening the design: change a
   tone, a size or a backing, keep the move.
   Evaluate visual appeal and task completion separately. Recheck the strengths chosen for preservation. List the
   top three problems, fix them, repeat; up to three rounds. Scanner counts are not an aesthetic score.
   **Distinctiveness test:** hide the logo and name. If the page could belong to any product in its category, make
   the idea from section 1 stronger; do not add decoration. Name the one thing a designer would screenshot from the
   page. If there is none, the bold move is missing. Run the re-theme test (section 2) when colours are customisable.
3. Keyboard pass: tab order, visible focus, Escape closes, Enter submits.
4. Run the scanner and the contrast check (section 8), go through section 6 and reread the copy against section 7.
5. Report what was checked and how. Never claim a check you did not run.

## 5. Tells: catch what slipped through

Visual tells. Fine as a deliberate choice; wrong as a default. Removing a tell must not leave a hole: replace it
with something specific to the subject, not with nothing.

| Tell | Do instead |
|---|---|
| Gradients without a role: a gradient hero, a glow behind the logo, gradient text | Flat colour by default. Keep a gradient when it carries meaning (a scale, a data range) or belongs to an approved identity; check text across it |
| Stock palettes nobody chose: purple + black, neon, near-black + cyan, cream + terracotta, stock pastels, rainbow | A palette from the brief, content and preferences; compare alternatives when the direction is open |
| Text or controls hard to tell from their surface; grey text on a coloured ground | Check the actual pairs; adjust lightness, chroma, foreground or surface |
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

## 7. Write for people (principles from ASD-STE100)

ASD-STE100 Simplified Technical English is an aerospace standard for maintenance texts. People read them under
pressure, often in a second language, and a wrong reading costs money or safety. The standard itself (its dictionary
and exact rules) is English-only and belongs to ASD; it is free on request. Only the principles below transfer, and they
work in any language.

Apply them to interface copy, error messages, help and procedures, and to everything you write to the person you work
with: a handover, a summary of a change, a question.

| Rule | Example |
|---|---|
| One word for one meaning, one meaning for one word | Pick "Delete" or "Remove" and keep it in buttons, docs and messages |
| Keep a glossary | A short `GLOSSARY.md` (or a section in `DESIGN.md`) with the product's terms; read it before you write, add new terms to it |
| Short sentences | Steps: 20 words or fewer. Descriptions: 25 words or fewer. One topic per paragraph |
| One instruction per sentence | "Stop the service. Copy the file." Not "Stop the service and then copy the file after checking it" |
| Numbered steps when the order matters | 1. Open Settings. 2. Select Keys. 3. Click "Add key" |
| Imperative for instructions | "Restart the service", not "you may want to restart" or "it is recommended to restart" |
| Active voice, the actor named | "The scanner found 17 items", not "17 items were found" |
| Condition before the action | "If the build fails, open the log" |
| Warning before the step, with the reason | "Do not delete the volume. It has no backup." Then the step |
| Concrete words, numbers with units | "Takes about 2 min", not "takes a while" |
| No noun stacks | "Limit of requests for each key", not "key request rate limit setting" |
| Parallel lists | Every item starts the same way (all verbs or all nouns) |
| No idioms, irony or metaphors | They fail in translation and for non-native readers |

**Reports to the person.** Write so they can act without asking back.

1. First line: the result (done, not done, blocked) and what the person must do, if anything.
2. Then what changed: one item per line, with file paths or links.
3. Then what you verified and how, and what you did not verify. Never write "should work".
4. Put each question on its own line. Give options when you can.
5. Use the person's terms. If you add a term, define it once.

The scanner does not check these rules. Reread the text against the table before you hand it over.

## 8. Scanner and contrast check

```bash
python scripts/check_design_tells.py path/to/project             # report
python scripts/check_design_tells.py page.html --strict           # exit 1 if anything is found
python scripts/check_design_tells.py src --json                   # for CI and agents
```

It finds candidates (file:line) for a person or agent to judge; it never edits files. Mark a deliberate use on its
line with a `design-tells: ignore` comment, or a whole file (a style guide) with `design-tells: ignore-file`.
Report each finding as fixed, kept on purpose (with the reason), or not applicable. Hue choices, pure white and
pure black are not findings by themselves. Icons are reported once per file with a count. The source scanner does
not measure rendered contrast; the contrast check below does.

```bash
python scripts/check_contrast.py page.html                        # light and dark, 1440 and 390 px
python scripts/check_contrast.py http://localhost:3000 --strict   # exit 1 on a failure
python scripts/check_contrast.py page.html --field .my-select     # add a custom control to the field check
```

It renders the page in Chromium (needs `pip install playwright` and `python -m playwright install chromium`). For
each theme it sets `prefers-color-scheme` and `data-theme` on `<html>` (`--theme-attr none` turns the attribute off).
It measures text against the solid colour behind it (1.4.3) and the boundary of inputs and similar fields (1.4.11).
Overlapping layers count, not only ancestors. Disabled controls are exempt. Text over an image or gradient, text
inside SVG and a field with no visible boundary are listed to check by eye. It does not see opacity, filters, pseudo-element text or hover and focus states. A pass is necessary,
not sufficient.

## Sources

Paraphrased in our own words: Anthropic `frontend-design` and `canvas-design` skills (Apache-2.0); Impeccable by Paul
Bakaus (Apache-2.0); taste-skill (MIT); Vercel Web Interface Guidelines (MIT); OpenAI, "Designing delightful frontends
with GPT-5.4" (ideas only); Refactoring UI (ideas only); Laws of UX (named principles); WCAG 2.2 (success criteria by
number); Apple HIG and Material Design (ideas only); ASD-STE100 Simplified Technical English (principles only, no
dictionary or rule text copied). The original list of tells came from a community post.

Colour checks: WCAG [text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html),
[non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html), and
[use of colour](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html).

Palette workflow references: Adobe Color [colour wheel](https://color.adobe.com/create/color-wheel) and
[image extraction](https://color.adobe.com/create/image); Coolors [generate and lock colours](https://coolors-help.zendesk.com/hc/en-us/articles/360010581980-Generate-a-palette);
Colormind [generation tips](https://colormind.io/). Local colour operations: CSS Color 4
[Oklab and OkLCh](https://www.w3.org/TR/css-color-4/#ok-lab) and
[gamut mapping](https://www.w3.org/TR/css-color-4/#gamut-mapping).
Tonal families and paired roles: Material [dynamic colour scheme](https://github.com/material-foundation/material-color-utilities/blob/main/concepts/dynamic_color_scheme.md)
and [colour roles](https://m3.material.io/styles/color/the-color-system).
