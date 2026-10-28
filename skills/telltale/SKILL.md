---
name: telltale
description: Use when designing, building or reviewing a user interface or its copy with a coding agent (landing pages, dashboards, admin panels, web apps, docs sites). A compact design process for agents (decide the mode, plan, build on tokens, verify in a browser) plus the visual and copy patterns that make a page look machine-generated, what to do instead, the basics agents forget, and plain-writing rules (from ASD-STE100) for interface copy and for the agent's reports to the person. Includes a scanner for HTML/CSS/JS/TSX/Vue/Svelte/Markdown.
---

<!-- design-tells: ignore-file (this file describes the patterns) -->

# Design for coding agents: process, tells, basics

Agents drift to the same defaults. Each is fine alone; together they make a page look generated and untrusted.
This skill gives a short process that avoids defaults by deciding first, a list of tells to catch what slips
through, and the basics that agents leave out.

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

### Choose the palette with the person

Follow the existing palette and established preferences first. When the colour direction is open:

1. Show two or three distinct palettes on the same representative interface. Include the existing palette as a
   reference when refining. Keep layout, typography, content, imagery, state, viewport and theme unchanged. Compare undecided light
   and dark themes separately before narrowing colours. Use rendered UI, not swatches alone.
2. Include surfaces, text, actions, focus and relevant semantic states. Check the applicable contrast requirements
   below before presenting an option. If the original fails a check, label that reference and offer a corrected
   variant. Explain each direction in one sentence and ask which is closest.
3. Accept a choice, a combination or ordinary-language feedback. Refine the selected direction with a few focused
   variants. Lock explicitly accepted values and roles; generate only what remains open. Distinguish an exact colour
   from a flexible preference such as "keep it blue". Translate feedback such as "warmer" or "less saturated" into
   targeted changes and say what changed. Preserve accepted choices; reopen rejected directions only when asked.
   Recheck any mixture and retain the previous candidate so the person can return to it.
4. Record chosen role tokens, exact locks, flexible preferences and rejected directions in `DESIGN.md` or the existing design record.
   Stop narrowing when the direction is clear. If the person delegates the choice, choose, explain and proceed.

Build a concrete preview before asking for a choice. Reuse preferences already given; do not make palette selection
a mandatory approval step for routine work. If no response is available, use a clearly provisional choice and continue.

### Generate useful palette candidates

Choose a starting method from the available inputs:

- **Anchor and harmony.** Start with an approved brand colour or supplied value. Explore a few relationships such as
  monochromatic, analogous, complementary or split-complementary; select candidates that fit the brief.
- **Reference image.** Extract a few dominant and accent colours from a supplied image. Use them as starting points;
  an image's palette does not determine which colours are suitable for text, controls or backgrounds.
- **Lock and complete.** Keep selected colours fixed and suggest the remaining colours around them. Change only the
  requested qualities in later rounds instead of regenerating the whole palette.

Expand these seed colours into role tokens and state variants. A generator's number or order of swatches does not
define the UI system. Evaluate the actual colour areas and foreground/background pairs on the representative screen.
Verify exact locks after generation. If a locked colour fails contrast in its intended
role, explain the conflict and offer a different use or a derived shade; keep the approved value unchanged.

Perform the palette operations locally. Use a colour space with separate lightness, chroma and hue controls, such as
OKLCH, for deliberate adjustments. Keep hue while varying lightness/chroma for monochromatic candidates; explore nearby
hues or an opposite hue for other relationships. These are candidate-generation heuristics, not guarantees of appeal.
Preserve locked source values exactly, map derived colours to the target gamut, and check the resulting rendered pairs.
Use CSS or a small local script when calculation helps. The workflow requires no palette-service API or account;
the services in Sources illustrate interaction patterns only.

## 2. Build a system, not a page

- **Tokens by role, not by value.** `--bg`, `--surface`, `--text`, `--text-muted`, `--line`, `--accent`, `--good`,
  `--warn`, `--bad`; type roles `display`, `heading`, `body`, `caption`, `data`. Components use roles only.
- **Supported themes have complete token sets.** For dark mode, re-tune contrast and accents instead of inverting
  colours. Set `color-scheme` (and `theme-color` for mobile); define every colour role in each supported theme.
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

## 4. Verify, do not assume

1. Render it. Screenshots at about 390, 768 and 1440 px, plus one zoomed out (overall balance) and all supported themes.
   For before/after, use the supplied original and the new version at the same viewport, theme and comparable state.
   When comparing palettes, also hold typography, content, media and layout fixed.
   Read the actual headings, actions and key numbers at their intended size and in any reduced preview being delivered.
   Correct text in the DOM is not proof of readable letterforms. Check wrapping just above and below affected breakpoints
   after changing type or tracking; inspect the rendered result, not only overflow measurements.
2. Evaluate visual appeal and task completion separately. Recheck the strengths chosen for preservation. List the
   top three problems, fix them, repeat; up to three rounds. Scanner counts are not an aesthetic score.
3. Keyboard pass: tab order, visible focus, Escape closes, Enter submits.
4. Run the scanner (section 8), go through section 6 and reread the copy against section 7.
5. Report what was checked and how. Never claim a check you did not run.

## 5. Tells: catch what slipped through

Visual tells. Fine as a deliberate choice; wrong as a default.

| Tell | Do instead |
|---|---|
| Gradients applied without a role; unreadable gradient text | Keep a gradient that supports the chosen identity, hierarchy or data; verify legibility across it |
| A stock palette applied without reference to the brief | Use the identity, content and preferences; compare alternatives when the direction is open |
| Text or controls become hard to distinguish on their surfaces | Check the actual combinations; adjust lightness, chroma, foreground or surface treatment |
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

## 8. Scanner

```bash
python scripts/check_design_tells.py path/to/project             # report
python scripts/check_design_tells.py page.html --strict           # exit 1 if anything is found
python scripts/check_design_tells.py src --json                   # for CI and agents
```

It finds candidates (file:line) for a person or agent to judge; it never edits files. Mark a deliberate use on its
line with a `design-tells: ignore` comment, or a whole file (a style guide) with `design-tells: ignore-file`.
Report each finding as fixed, kept on purpose (with the reason), or not applicable. Hue choices, pure white and
pure black are not findings by themselves. The source scanner does not measure rendered contrast; check it separately.

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
