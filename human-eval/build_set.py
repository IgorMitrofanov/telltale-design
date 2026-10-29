#!/usr/bin/env python3
"""Build a set for the human comparison: the page, the anonymised designs, and the private key.

  python build_set.py SPEC.json --out ../docs --key KEY.json

SPEC.json:
  {"set": "2026-10-29",
   "briefs": {"b1": {"telltale": {"page": "run/b1/t/index.html", "shots": "run/shots/b1/t"},
                     "no-skill":  {"page": "run/b1/n/index.html", "shots": "run/shots/b1/n"}, ...}, ...}}

"shots" is the folder that evals/run_eval.py wrote: it needs light-1440.png and light-390.png. Relative paths are
resolved from the folder of SPEC.json.

Writes OUT/index.html, OUT/d/<code>/{index.html,desktop.webp,phone.webp} with a random four-character code per design,
and KEY.json: {"set": ..., "codes": {code: {"brief": ..., "condition": ...}}}. KEY.json is the only place where the
codes are explained. Keep it out of the folder you publish. Needs Pillow.
"""
import json, pathlib, re, secrets, shutil, sys
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
ALPHABET = "abcdefghjkmnpqrstuvwxyz23456789"


def anonymise(html):
    """Drop comments that carry the scanner marker: they would show which designs were built with a skill."""
    html = re.sub(r"/\*[^*]*design-tells[\s\S]*?\*/\s?", "", html)
    html = re.sub(r"<!--[^>]*design-tells[\s\S]*?-->\s?", "", html)
    return html


def main(argv):
    if not argv or argv[0].startswith("--"):
        print(__doc__); return 2
    spec_path = pathlib.Path(argv[0]).resolve()
    out = pathlib.Path(argv[argv.index("--out") + 1]).resolve()
    key_path = pathlib.Path(argv[argv.index("--key") + 1]).resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    base = spec_path.parent

    if out.exists():
        shutil.rmtree(out)
    (out / "d").mkdir(parents=True)
    used, key, designs = set(), {}, {}
    for brief, conditions in spec["briefs"].items():
        designs[brief] = []
        for condition, src in conditions.items():
            while True:
                code = "".join(secrets.choice(ALPHABET) for _ in range(4))
                if code not in used:
                    used.add(code); break
            key[code] = {"brief": brief, "condition": condition}
            designs[brief].append(code)
            target = out / "d" / code
            target.mkdir()
            html = (base / src["page"]).read_text(encoding="utf-8")
            (target / "index.html").write_text(anonymise(html), encoding="utf-8")
            shots = base / src["shots"]
            desk = Image.open(shots / "light-1440.png").convert("RGB").crop((0, 0, 1440, 900)).resize((960, 600), Image.LANCZOS)
            desk.save(target / "desktop.webp", "WEBP", quality=84)
            phone = Image.open(shots / "light-390.png").convert("RGB")
            phone.crop((0, 0, phone.width, min(phone.height, 780))).save(target / "phone.webp", "WEBP", quality=84)

    template = (HERE / "template.html").read_text(encoding="utf-8")
    page = template.replace("__SET__", spec["set"]).replace("__DESIGNS__", json.dumps(designs))
    (out / "index.html").write_text(page, encoding="utf-8")
    key_path.write_text(json.dumps({"set": spec["set"], "note": "Maps design codes to brief and condition. The page does not load it.",
                                    "codes": key}, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"set {spec['set']}: {len(key)} designs in {len(designs)} briefs -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
