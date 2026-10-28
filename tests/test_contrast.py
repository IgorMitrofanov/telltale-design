"""Run: python tests/test_contrast.py. Needs Playwright and a Chromium; prints "skipped" without them."""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("contrast", os.path.join(HERE, "..", "skills", "telltale", "scripts", "check_contrast.py"))
contrast = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contrast)

if importlib.util.find_spec("playwright") is None:
    print("skipped: playwright is not installed")
    sys.exit(0)
try:
    results = contrast.check([os.path.join(HERE, "contrast.html")], ["light", "dark"], [800], "data-theme", [".custom"])
except SystemExit as e:  # no browser available
    print(f"skipped: {e}")
    sys.exit(0)

by_theme = {r["theme"]: r for r in results}
def ids(theme, kind, key="element"):
    return sorted(f[key].split("#")[1].split(".")[0] for f in by_theme[theme][kind] if "#" in f[key])

expected = {
    ("light", "text"): ["fail-faint", "fail-oklch"],
    ("dark", "text"): ["fail-dark"],
    ("light", "fields"): ["custom-select", "weak", "weak-relative"],
    ("dark", "fields"): ["weak-relative"],
    ("light", "unchecked"): ["divided", "svg-fail", "svg-pass", "unchecked"],
    ("dark", "unchecked"): ["divided", "svg-fail", "svg-pass", "unchecked"],
}
problems = []
for (theme, kind), want in expected.items():
    got = ids(theme, kind)
    if got != want:
        problems.append(f"{theme} {kind}: expected {want}, got {got}")
# Passes: a wrapper outlined on four sides, an underline. Not a failure: a one-sided divider (listed as unchecked)
# and a disabled input.
for theme in ("light", "dark"):
    for f in by_theme[theme]["fields"]:
        if f["element"].startswith(("textarea#wrapped", "textarea#divided", "input#underlined", "input#off")):
            problems.append(f"{theme}: {f['element']} should not fail")

with open(os.devnull, "w") as null:
    stdout, sys.stdout = sys.stdout, null
    try:
        strict = contrast.main([os.path.join(HERE, "contrast.html"), "--widths", "800", "--strict"])
    finally:
        sys.stdout = stdout
if strict != 1:
    problems.append(f"--strict should exit 1 on failures, got {strict}")

if problems:
    print("\n".join(problems))
    sys.exit(1)
print("ok: text, large text, theme-only, field boundary, wrapper, custom field, underline, divider, oklch and relative colour, overlapping layer, SVG text listed, disabled and unchecked cases verified")
