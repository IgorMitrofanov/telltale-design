<!-- design-tells: ignore-file -->
# Design for coding agents (instructions for Codex and other AGENTS.md agents)

When you design, build or review a user interface or its copy, follow `skills/telltale/SKILL.md`. In short:

1. **Decide before styling.** Subject, audience, place; the mode of the surface (Persuade, Operate, Read,
   Experience); the existing design system first. Name the strengths to preserve before refining. Write a five-line
   plan and review defaults against the brief; keep those that fit.
2. **Choose colours together when needed.** Follow established preferences. Otherwise show two or three palettes
   on the same rendered interface, holding layout, type, content, media, state, viewport and theme fixed. Include
   the original palette when refining. Narrow with ordinary-language feedback and save the chosen role tokens.
   Start from a brand colour, a supplied reference or colour relationships. Lock accepted values and roles; change
   only open choices. Expand seed colours into UI roles and verify exact locks after generation. Calculate adjustments
   locally and check the rendered result; no palette-service API or account is required.
   If the person delegates, choose and proceed. Palette preferences are separate from contrast requirements.
3. **Build a system.** Role tokens (`--bg`, `--surface`, `--text`, `--accent`, statuses), dark mode as a second
   token set, a small type scale and a 4 px spacing scale. Derive tonal families and pair fill roles with their text/icon
   colours; choose suitable tones per supported theme. Colour harmony and tinted neutrals are starting points;
   no hue, white or black is a defect by itself. Check actual contrast and visible cues beyond colour.
4. **Build the interface.** Hierarchy by weight/colour/space, no cards by default, all states of every component,
   interaction basics, honest data display, motion only as state (150–250 ms, transform/opacity, reduced motion),
   copy that names actions.
5. **Review the tells** (section 5) in context; keep deliberate choices with one line explaining why.
6. **Check the basics** (section 6). Terms and privacy only for public products or personal data; for internal
   tools ask the user if unsure.
7. **Write for people** (section 7, principles from ASD-STE100). One word per meaning and a project glossary;
   short sentences (steps 20 words or fewer); one instruction per sentence; imperative, active voice; condition
   before action; warning before the step. Reports to the person start with the result and what they must do,
   then changes, then what was and was not verified.
8. **Verify.** Screenshots at about 390, 768 and 1440 px and all supported themes. Compare the supplied original
   with the new version at matching viewports, themes and comparable states. Evaluate appearance and task completion
   separately. Read actual headings and key text at intended size and in delivered reduced previews; glyphs must remain
   distinct. Recheck wrapping around affected breakpoints after type or tracking changes. Use up to three rounds of fixes,
   a keyboard pass, then
   `python skills/telltale/scripts/check_design_tells.py <changed paths>`. Report each finding as fixed, kept on purpose
   (with the reason), or not applicable. Never claim a check you did not run.

The user's explicit brief and the project's existing design system override style defaults here. Keep measurable
requirements, design heuristics and personal preferences distinct. The source scanner does not measure contrast.

To use in another project, copy the `skills/telltale` folder there and add these points to that project's
`AGENTS.md` (or to `~/.codex/AGENTS.md` for every project).
