<!-- design-tells: ignore-file -->
# Design for coding agents (instructions for Codex and other AGENTS.md agents)

When you design, build or review a user interface or its copy, follow `skills/telltale/SKILL.md`. In short:

1. **Decide before styling.** Subject, audience, place; the mode of the surface (Persuade, Operate, Read,
   Experience); the existing design system first; a five-line plan with every category default crossed out.
2. **Build a system.** Role tokens (`--bg`, `--surface`, `--text`, `--accent`, statuses), dark mode as a second
   token set, a small type scale and a 4 px spacing scale.
3. **Build the interface.** Hierarchy by weight/colour/space, no cards by default, all states of every component,
   interaction basics, honest data display, motion only as state (150–250 ms, transform/opacity, reduced motion),
   copy that names actions.
4. **Avoid the tells** (section 5) by default; keep one only as a deliberate choice stated in one line.
5. **Check the basics** (section 6). Terms and privacy only for public products or personal data; for internal
   tools ask the user if unsure.
6. **Verify.** Screenshots at about 390, 768 and 1440 px and both themes, up to three rounds of fixes, a keyboard
   pass, then `python skills/telltale/scripts/check_design_tells.py <changed paths>`. Report each finding as
   fixed, kept on purpose (with the reason), or not applicable. Never claim a check you did not run.

The user's explicit brief and the project's existing design system override any default here.

To use in another project, copy the `skills/telltale` folder there and add these points to that project's
`AGENTS.md` (or to `~/.codex/AGENTS.md` for every project).
