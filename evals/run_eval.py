#!/usr/bin/env python3
"""design-tells: ignore-file

Render, measure and anonymise a comparison run.

  python evals/run_eval.py RUN_DIR [--seed N]

RUN_DIR holds one folder per brief, each with one folder per condition containing index.html:
RUN_DIR/b1/t/index.html, RUN_DIR/b1/f/index.html, ... The script writes:

- RUN_DIR/shots/<brief>/<condition>/*.png: light and dark at 1440 px and 390 px (full page), and the first screen
  after the brand colour is swapped to a dark teal, a light yellow and a red, in both themes.
- RUN_DIR/results.json: per page, distinct failing contrast pairs, minimum ratio and items to check by eye (from
  skills/telltale/scripts/check_contrast.py) at the default brand and after each swap; scanner candidates; colour
  literals outside custom properties; horizontal overflow.
- RUN_DIR/judge/<brief>/<X|Y|Z>/: the screenshots and metrics.json under a random label per brief, for blind judges.
- RUN_DIR/KEY_do_not_show_judges.json: which label is which condition.

Needs Playwright with Chromium (or Chrome / Edge installed).
"""
import importlib.util, json, pathlib, random, re, shutil, sys

HERE = pathlib.Path(__file__).resolve().parent
SCRIPTS = HERE.parent / "skills" / "telltale" / "scripts"
RETHEME = {"teal": "#0E7C86", "yellow": "#F2C14E", "red": "#C8102E"}
LABELS = ["X", "Y", "Z"]


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def literals_outside_tokens(html):
    """Colour values written outside custom-property declarations: each one ignores a brand change."""
    css = re.sub(r"/\*.*?\*/", "", " ".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S)), flags=re.S)
    count = 0
    for decl in re.split(r"[;{}]", css):
        decl = decl.strip()
        if decl and not decl.startswith("--") and ":" in decl:
            count += len(re.findall(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?|oklch|lab|lch)\(", decl.split(":", 1)[1]))
    return count + len(re.findall(r'style="[^"]*(?:#[0-9a-fA-F]{3,8}|rgb\()', html))


def retheme_copy(page, brand):
    html = page.read_text(encoding="utf-8")
    inject = f"<style>html{{--brand:{brand} !important}}</style>"
    html = html.replace("</head>", inject + "</head>", 1) if "</head>" in html else inject + html
    out = page.parent / "work" / f"_retheme_{brand[1:]}.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out


def main(argv):
    run = pathlib.Path(argv[0]).resolve()
    seed = int(argv[argv.index("--seed") + 1]) if "--seed" in argv else 1
    contrast, scanner = load("contrast", "check_contrast.py"), load("scanner", "check_design_tells.py")
    from playwright.sync_api import sync_playwright

    briefs = sorted(p.name for p in run.iterdir() if p.is_dir() and p.name not in {"shots", "judge"}
                    and any((c / "index.html").exists() for c in p.iterdir() if c.is_dir()))
    pages = {(b, c.name): c / "index.html" for b in briefs for c in sorted((run / b).iterdir()) if (c / "index.html").exists()}
    results, variants = {}, {}

    with sync_playwright() as p:
        browser = contrast.launch(p)
        for (b, c), page in pages.items():
            shots = run / "shots" / b / c
            shots.mkdir(parents=True, exist_ok=True)

            def shot(file, theme, width, name, full=True):
                tab = browser.new_page(viewport={"width": width, "height": 900}, color_scheme=theme)
                tab.goto(file.as_uri())
                tab.wait_for_load_state("networkidle")
                tab.evaluate(f"document.documentElement.setAttribute('data-theme', '{theme}')")
                tab.wait_for_timeout(300)
                overflow = tab.evaluate("document.documentElement.scrollWidth") > width
                tab.screenshot(path=str(shots / f"{name}.png"), full_page=full)  # 1x: Chromium caps captures at 16384 px
                tab.close()
                return overflow

            overflow = [f"{t}-{w}" for t in ("light", "dark") for w in (1440, 390) if shot(page, t, w, f"{t}-{w}")]
            variants[(b, c)] = {"default": page}
            for name, brand in RETHEME.items():
                copy = retheme_copy(page, brand)
                variants[(b, c)][name] = copy
                for theme in ("light", "dark"):
                    shot(copy, theme, 1440, f"retheme-{name}-{theme}", full=False)
            html = page.read_text(encoding="utf-8")
            findings, _ = scanner.scan([str(page)])
            results[f"{b}/{c}"] = {"overflow": overflow, "scanner_candidates": len(findings),
                                   "colour_literals_outside_tokens": literals_outside_tokens(html)}
        browser.close()

    # check_contrast starts its own Playwright, so it runs after the browser above is closed.
    for (b, c), files in variants.items():
        pairs, mins, unchecked = {}, {}, {}
        for name, file in files.items():
            found = contrast.check([str(file)], ["light", "dark"], [1440, 390], "data-theme", [])
            items = {(r["theme"], kind, round(i["ratio"], 2)) for r in found for kind in ("text", "fields") for i in r[kind]}
            pairs[name], mins[name] = len(items), min((i[2] for i in items), default=None)
            unchecked[name] = sum(len(r["unchecked"]) for r in found)
        results[f"{b}/{c}"].update(distinct_failing_pairs=pairs, min_ratio=mins, unchecked_to_check_by_eye=unchecked)
        print(f"{b}/{c}", json.dumps(results[f"{b}/{c}"]), flush=True)

    rng, key = random.Random(seed), {}
    if (run / "judge").exists():
        shutil.rmtree(run / "judge")
    for b in briefs:
        conds = sorted(c for (bb, c) in pages if bb == b)
        labels = LABELS[:len(conds)]
        rng.shuffle(labels)
        key[b] = dict(zip(conds, labels))
        for c, label in key[b].items():
            target = run / "judge" / b / label
            shutil.copytree(run / "shots" / b / c, target)
            (target / "metrics.json").write_text(json.dumps(results[f"{b}/{c}"], indent=1))
    (run / "results.json").write_text(json.dumps(results, indent=1))
    (run / "KEY_do_not_show_judges.json").write_text(json.dumps(key, indent=1))
    print("key", key)


if __name__ == "__main__":
    if not sys.argv[1:]:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1:])
