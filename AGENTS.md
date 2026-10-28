<!-- design-tells: ignore-file -->
# AI design tells (instructions for Codex and other AGENTS.md agents)

When you design, build or review a user interface or its copy, follow `skills/ai-design-tells/SKILL.md`:

1. Before writing UI code, choose palette, typeface and layout from the subject of the product, not from defaults.
2. Avoid by default the visual tells (section 1) and copy tells (section 2); a tell is acceptable only as a deliberate,
   justified choice, stated in one line.
3. Check the basics (section 3): real product shots, loading/empty/error states, accessibility, responsive layout;
   terms and privacy only for public products or personal data (for internal tools ask the user if unsure).
4. Before handing work over, run `python skills/ai-design-tells/scripts/check_design_tells.py <changed paths>` and
   report each finding as fixed, kept on purpose (with the reason), or not applicable.

To use in another project, copy the `skills/ai-design-tells` folder there and add these four points to that
project's `AGENTS.md` (or to `~/.codex/AGENTS.md` for every project).
