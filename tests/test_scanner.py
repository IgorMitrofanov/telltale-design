"""Run: python tests/test_scanner.py. The scanner must find every tell planted in tests/slop.html and nothing in clean.html."""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("scanner", os.path.join(HERE, "..", "skills", "telltale", "scripts", "check_design_tells.py"))
scanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scanner)

PLANTED = {"gradient", "gradient-text", "purple", "neon", "pure-white", "pure-black", "shadow", "offset-shadow", "radius-large",
           "hover-motion", "transition-all", "bounce", "no-zoom", "focus-removed", "eyebrow", "uppercase-label", "emoji",
           "checkmark", "em-dash", "not-x-but-y", "vague-claim"}

import tempfile
# the fixture is marked ignore-file so a scan of this repository stays clean; test a copy without the marker
with tempfile.TemporaryDirectory() as tmp:
    copy = os.path.join(tmp, "slop.html")
    text = open(os.path.join(HERE, "slop.html"), encoding="utf-8").read().replace("design-tells: ignore-file", "")
    open(copy, "w", encoding="utf-8").write(text)
    found, _ = scanner.scan([copy])
missing = PLANTED - {f["check"] for f in found}
clean, _ = scanner.scan([os.path.join(HERE, "clean.html")])
if missing or clean:
    print("missing:", sorted(missing), "| false positives on clean.html:", [(f["check"], f["line"]) for f in clean])
    sys.exit(1)
print(f"ok: {len(PLANTED)} planted tells found, clean page clean")
