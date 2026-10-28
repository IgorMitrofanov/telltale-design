"""Run: python tests/test_scanner.py. Find active tells in slop.html, keep clean.html clean, and do not treat palette values alone as defects."""
import contextlib
import importlib.util
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("scanner", os.path.join(HERE, "..", "skills", "telltale", "scripts", "check_design_tells.py"))
scanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scanner)

PLANTED = {"gradient", "gradient-text", "shadow", "offset-shadow", "radius-large",
           "hover-motion", "transition-all", "bounce", "no-zoom", "focus-removed", "eyebrow", "uppercase-label", "emoji",
           "checkmark", "em-dash", "not-x-but-y", "vague-claim"}

import tempfile
# the fixture is marked ignore-file so a scan of this repository stays clean; test a copy without the marker
with tempfile.TemporaryDirectory() as tmp:
    copy = os.path.join(tmp, "slop.html")
    text = open(os.path.join(HERE, "slop.html"), encoding="utf-8").read().replace("design-tells: ignore-file", "")
    open(copy, "w", encoding="utf-8").write(text)
    found, _ = scanner.scan([copy])
    # Markdown: a tell in prose counts, the same text quoted in fenced code does not; line numbers stay right
    doc = os.path.join(tmp, "doc.md")
    open(doc, "w", encoding="utf-8").write("```text\nIt's not a tool, it's a revolution\n```\nIt's not a tool, it's a revolution\n")
    md, _ = scanner.scan([doc])
    # Colour literals do not establish a defect. Keep the full strict CLI path covered
    # so these palettes cannot become CI failures through another output branch.
    palette = os.path.join(tmp, "palette.html")
    palette_source = """<!doctype html><html><head><style>
    .paper { background: #fff; color: #000; }
    .inverse { background-color: black; color: white; }
    .brand { color: #7c3aed; background: #00ffff; }
    .signals { color: #39ff14; border-color: #ff00ff; }
    @media (prefers-reduced-motion: reduce) { .notice { animation: none; } }
    </style></head><body>
    <a class="bg-white text-black purple-500 violet-600 fuchsia-700" href="privacy">Privacy</a>
    <a class="bg-black" href="terms">Terms</a>
    <p aria-busy="true">Loading</p><p>No results</p><p>Error: try again</p>
    </body></html>"""
    open(palette, "w", encoding="utf-8").write(palette_source)
    palette_findings, palette_missing = scanner.scan([palette])
    with contextlib.redirect_stdout(io.StringIO()):
        palette_exit = scanner.main([palette, "--strict", "--json"])
    # Removing hue preferences must not silence an independent accessibility warning.
    open(palette, "w", encoding="utf-8").write(palette_source.replace("</style>", ":focus { outline: none; }</style>"))
    focus_findings, _ = scanner.scan([palette])
    with contextlib.redirect_stdout(io.StringIO()):
        focus_exit = scanner.main([palette, "--strict", "--json"])
    # Icons are counted once per file, not once per <svg>; a line marked ignore is left out of the count.
    icons = os.path.join(tmp, "icons.html")
    open(icons, "w", encoding="utf-8").write("<button><svg></svg>Save</button>\n<button><svg></svg>Copy</button>\n"
                                             "<a><svg></svg>Back</a>\n<i><svg></svg></i> <!-- design-tells: ignore -->\n")
    icon_findings = [f for f in scanner.scan([icons])[0] if f["check"] == "icon-set"]
missing = PLANTED - {f["check"] for f in found}
clean, _ = scanner.scan([os.path.join(HERE, "clean.html")])
md_ok = [(f["check"], f["line"]) for f in md] == [("not-x-but-y", 4)]
palette_ok = not palette_findings and not palette_missing and palette_exit == 0
focus_ok = [f["check"] for f in focus_findings] == ["focus-removed"] and focus_exit == 1
icons_ok = [(f["line"], f["count"]) for f in icon_findings] == [(1, 3)]
if missing or clean or not md_ok or not palette_ok or not focus_ok or not icons_ok:
    print("missing:", sorted(missing), "| false positives on clean.html:", [(f["check"], f["line"]) for f in clean],
          "| markdown:", [(f["check"], f["line"]) for f in md],
          "| palette:", palette_findings, palette_missing, palette_exit,
          "| focus:", [(f["check"], f["line"]) for f in focus_findings], focus_exit,
          "| icons:", [(f["line"], f.get("count")) for f in icon_findings])
    sys.exit(1)
print(f"ok: {len(PLANTED)} planted tells found, clean page clean; palette-only strict pass, "
      "focus strict failure and per-file icon count verified")
