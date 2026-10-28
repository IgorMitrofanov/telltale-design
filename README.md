<p align="center"><strong>English</strong> · <a href="README.ru.md">Русский</a></p>

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&amp;height=200&amp;color=12304a&amp;text=telltale&amp;fontColor=f8fafc&amp;fontSize=56&amp;fontAlignY=38&amp;desc=Design%20and%20writing%20rules%20for%20coding%20agents&amp;descAlignY=60" alt="telltale: design and writing rules for coding agents" width="100%" />
  <p><strong>A skill for Claude Code · Instructions for Codex · A scanner you can run in CI</strong></p>
  <p>
    <a href="#why">Why</a> ·
    <a href="#what-the-agent-does">What the agent does</a> ·
    <a href="#install">Install</a> ·
    <a href="#scanner">Scanner</a> ·
    <a href="#a-real-run">A real run</a> ·
    <a href="#sources">Sources</a>
  </p>
</div>

## Why

Coding agents now write a lot of interfaces. They work fast, and their pages are easy to recognise: a gradient hero,
the same unexamined palette, glass panels, emoji instead of icons, three cards in a row, a long dash in every sentence, "it's not X, it's Y". <!-- design-tells: ignore --> Each choice is fine on its own. Together they say "nobody
decided anything here", and people trust the page less.

The opposite problem is quieter. Agents skip the plain parts: real screenshots, loading and empty states, errors you can
act on, keyboard focus. And when they report back, they write long summaries where the result is somewhere in the
middle.

telltale is what I now give every agent before it touches an interface. It is a short process, a list of tells with
replacements, the basics that get forgotten, and writing rules for the interface copy and for the agent's own reports.

## What the agent does

| Step | What happens |
| --- | --- |
| **Decide** | Names the subject, the audience and where the page is used. Picks the mode: *Persuade* (landing), *Operate* (admin, dashboard), *Read* (docs) or *Experience* (games). Reads the project's design system first and names strengths to preserve. Writes a five-line plan and reviews defaults against the brief. |
| **Choose colours** | Follows an existing palette or preference. When the direction is open, shows 2–3 palettes on the same interface, narrows the choice with you and records it. Checks contrast separately from taste. |
| **Build a system** | Tokens by role (`--bg`, `--surface`, `--accent`, statuses), dark mode as a second token set, a small type scale, a 4 px spacing scale. |
| **Build the interface** | Hierarchy by weight, colour and space. No cards by default. Every state of every component. Honest data: units, aligned digits, status never by colour alone. Motion only as a change of state. |
| **Write for people** | Principles from ASD-STE100: one word for one meaning, short sentences, one instruction per sentence, condition before action, warning before the step. Reports start with the result and what you need to do. |
| **Verify** | Screenshots at 390, 768 and 1440 px in supported themes; before/after at matching viewport and theme. Evaluates visual appeal and task completion separately. Up to three rounds of fixes, a keyboard pass, the scanner. Reports only checks actually run. |

**Your brief wins.** An explicit instruction or the project's existing design system overrides style defaults. A
deliberate choice stays, with one line saying why. Contrast requirements, design heuristics and personal taste are
separate decisions. No colour combination, pure white or pure black is rejected solely by its name or value.

**Palette choice uses a real screen.** Typography, content, imagery, state, viewport and theme stay fixed while you
compare colours. You can choose, combine or ask for a change in ordinary language. The agent refines the selected
direction and checks the new combination. An established preference or delegated choice skips this extra round.

Start from a brand colour, a reference image or a colour relationship. Keep selected values fixed and generate the
remaining colours; refine with requests such as "warmer" or "less saturated". The agent expands the palette into UI roles
and states, verifies locked values, and retains previous candidates. Adobe Color, Coolors and Colormind are optional
sources of candidates; the dialogue also works with local previews.

**Typography must remain readable when rendered.** The agent checks actual words at their intended size and in
delivered reduced previews. Tight spacing must not merge letters, such as `rn` into `m`. Changes to type or spacing
also require a check of line wrapping around affected responsive breakpoints.

<details>
<summary><strong>About ASD-STE100</strong></summary>

ASD-STE100 Simplified Technical English is an aerospace standard for maintenance documentation. Mechanics read these
texts under time pressure, often in a second language, and a misread step is expensive. The standard has a controlled
dictionary and about sixty writing rules.

The dictionary and the exact rule text are English and belong to ASD (free on request). telltale copies neither. It
takes the principles that work in any language and that also make an agent easier to work with:

- one term for one thing, kept in a project glossary;
- steps of 20 words or fewer, descriptions of 25 or fewer;
- one instruction per sentence, in the imperative;
- active voice with the actor named;
- the condition before the action, the warning before the step.

For reports the skill adds a fixed order: the result and what you must do, then the changes, then what was verified
and what was not.

</details>

<details>
<summary><strong>Legal pages: when they apply</strong></summary>

A public product or any form that collects personal data needs terms of use and a privacy policy. An internal tool behind
staff login usually does not. If the audience is unclear, the agent asks you. It does not add legal pages or flag their
absence by default.

</details>

## Install

**Claude Code.** Copy the skill folder:

```bash
# for all projects
cp -r skills/telltale ~/.claude/skills/
# or for one project
cp -r skills/telltale <project>/.claude/skills/
```

Claude picks it up when the task is about an interface. You can also call it directly: `/telltale`.

**Codex and other agents that read `AGENTS.md`.** Copy `skills/telltale` into the project and add the points from
[`AGENTS.md`](AGENTS.md) to the project's `AGENTS.md` (or to `~/.codex/AGENTS.md` for every project).

## Scanner

```bash
python skills/telltale/scripts/check_design_tells.py path/to/project
python skills/telltale/scripts/check_design_tells.py page.html --strict   # exit 1 if anything is found
python skills/telltale/scripts/check_design_tells.py src --json           # for CI and agents
```

It reads HTML, CSS, JS, TS, JSX, TSX, Vue, Svelte and Markdown and prints candidates with file and line. It never edits
anything. A candidate is a place to look at, not a verdict: a row of number tiles is right in an operations dashboard
and may be wrong on a landing page. Colour literals alone are not findings; this source scanner does not measure
rendered contrast or visual appeal.

Mark a deliberate use on its line with `design-tells: ignore`, or a whole file (a style guide) with
`design-tells: ignore-file`. Python 3.8 or newer, no dependencies.

```text
"Not X, but Y" construction [not-x-but-y]: 1  ->  Say what it is, directly
  landing.html:1  <h1>It's not a tool, it's a revolution ...

Basics not found (check whether they apply):
  - Empty state [empty-state]
  - Error state [error-state]

23 candidate(s), 6 basic(s) not found.
```

## A real run

The first target was an internal admin panel: 2,155 lines of HTML, CSS and JS written by agents over several weeks.

| | Before | After |
| --- | --- | --- |
| Candidates | 127 | 17, each kept on purpose |
| Long dashes in copy | 41 | 0 |
| Coloured left stripes | 7 | 0, now full borders |
| Uppercase letter-spaced labels | 4 rules | 0, sentence case |
| Gradients, glass, purple, emoji | none | none |

The 17 that stayed are deliberate: radii on tags and meters, a pulsing "online" dot that respects reduced motion, and a
dash as the "no value" mark in table cells. No legal pages: this is an internal tool.
These historical counts use the earlier rule set; the current scanner omits hue-only checks. Candidate counts do not measure visual quality.

## Repository

| Path | Purpose |
| --- | --- |
| [`skills/telltale/SKILL.md`](skills/telltale/SKILL.md) | The skill: process, tells, basics, writing rules |
| [`skills/telltale/scripts/check_design_tells.py`](skills/telltale/scripts/check_design_tells.py) | The scanner |
| [`AGENTS.md`](AGENTS.md) | The same rules in short form for Codex |
| [`tests/`](tests) | A page with planted tells, a clean page, and `python tests/test_scanner.py` |

## Sources

All ideas are paraphrased; no text was copied. Anthropic `frontend-design` and `canvas-design` skills (Apache-2.0),
Impeccable by Paul Bakaus (Apache-2.0), taste-skill (MIT), Vercel Web Interface Guidelines (MIT), the OpenAI note on
frontend design with GPT-5.4, Refactoring UI, Laws of UX, WCAG 2.2 (criteria by number), Apple HIG, Material Design and
ASD-STE100 (principles only). The first list of tells came from a community post.

## Licence

[MIT](LICENSE). Issues and pull requests with new tells are welcome. Please include a real example and what to do
instead.

---

**Decide first. Check in the browser. Write so people can act.**
