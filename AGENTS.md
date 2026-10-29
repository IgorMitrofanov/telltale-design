<!-- design-tells: ignore-file -->
# Design for coding agents (instructions for Codex and other AGENTS.md agents)

When you design, build or review a user interface or its copy, follow `skills/telltale/SKILL.md`. In short:

1. **Decide before styling.** Subject, audience, place; the mode of the surface (Persuade, Operate, Read,
   Experience); the existing design system first. Name the strengths to preserve before refining. Write a five-line
   plan and review defaults against the brief; keep those that fit.
2. **Find the idea.** List five things only the subject has; write three one-sentence concepts and pick one;
   spend one bold move per view and keep the rest quiet; borrow from two references outside the category.
   Restraint without an idea is not good design. Aim for portfolio grade; calm only when the brief asks. The bold move
   carries content (a map, a plan, real data), not just a colour field and a big headline.
3. **Choose a direction together when it is open.** Show two or three directions as rendered UI on the same screen,
   in every supported theme; for palettes, hold layout, type and content fixed. Narrow with plain-language feedback,
   lock accepted values and record the choice in `DESIGN.md`. If the person delegates, choose and proceed.
   Preferences are separate from contrast requirements.
4. **Build a system.** Role tokens (`--bg`, `--surface`, `--text`, `--accent`, statuses), dark mode as a second
   token set, a small type scale and a 4 px spacing scale. Pair each fill with its text colour (`--accent` /
   `--on-accent`) and derive tonal families per theme. No hue, white or black is a defect by itself; check actual
   contrast (WCAG 2.2) and cues beyond colour. No colour literals outside the token blocks;
   derive state tones from the accent and pass the re-theme test (two distant accent hues, contrast rechecked).
5. **Build the interface.** Hierarchy by weight/colour/space, no cards by default, all states of every component,
   interaction basics, honest data display, motion only as state (150–250 ms, transform/opacity, reduced motion),
   copy that names actions. On presentation-led pages, leave optional play discoverable; keep task guidance.
   Typography with character, a grid broken once on purpose,
   art-directed images, committed colour, details that reward a second look.
6. **Review the tells** (section 5) in context; keep deliberate choices with one line explaining why.
7. **Check the basics** (section 6). Terms and privacy only for public products or personal data; for internal
   tools ask the user if unsure.
8. **Write for people** (section 7, principles from ASD-STE100). One word per meaning and a project glossary;
   short sentences (steps 20 words or fewer); one instruction per sentence; imperative, active voice; condition
   before action; warning before the step. Reports to the person start with the result and what they must do,
   then changes, then what was and was not verified.
9. **Verify.** Screenshots at about 390, 768 and 1440 px and all supported themes. Compare the supplied original
   with the new version at matching viewports, themes and comparable states. Evaluate appearance and task completion
   separately; hide the logo and check that the page could not belong to any product in its category. Read actual headings and key text at intended size and in delivered reduced previews; glyphs must remain
   distinct. Recheck wrapping around affected breakpoints after type or tracking changes. Use up to three rounds of fixes,
   a keyboard pass, then
   `python skills/telltale/scripts/check_design_tells.py <changed paths>` and
   `python skills/telltale/scripts/check_contrast.py <page or URL>`. Report each finding as fixed, kept on purpose
   (with the reason), or not applicable. Never claim a check you did not run.

The user's explicit brief and the project's existing design system override style defaults here. Keep measurable
requirements, design heuristics and personal preferences distinct. The source scanner does not measure contrast; `check_contrast.py` does.

To use in another project, copy the `skills/telltale` folder there and add these points to that project's
`AGENTS.md` (or to `~/.codex/AGENTS.md` for every project).
