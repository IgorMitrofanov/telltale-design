#!/usr/bin/env python3
"""design-tells: ignore-file

Measure WCAG 2.2 contrast on a rendered page (Playwright + Chromium).

  python check_contrast.py PAGE [PAGE ...] [--themes light,dark] [--widths 1440,390]
                           [--theme-attr data-theme|none] [--field SELECTOR ...] [--json] [--strict]

PAGE is a file path or a URL. For each theme the page gets `prefers-color-scheme` and, unless --theme-attr none,
the attribute `data-theme="<theme>"` on <html>. Checks:

- text: every visible element with its own text, and the value of inputs and textareas, against the solid colour
  behind it. 4.5:1, or 3:1 for large text (24 px, or 18.66 px bold). Success criterion 1.4.3.
- field: the boundary of inputs, textareas, selects, [contenteditable], [role=textbox|combobox|searchbox] and any
  --field SELECTOR. The control's own border (an underline counts), a wrapper outlined on all four sides (up to
  2 levels up), or the fill must reach 3:1 against the colour outside it. Success criterion 1.4.11.

Disabled controls are exempt. Listed as unchecked, not passed, to check by eye: text over an image or gradient, and
a field with no visible boundary (not a 1.4.11 failure, but people may not see where to type).
Not measured: opacity and filters on ancestors, text in pseudo-elements, focus and hover states, text inside images.
A pass is necessary, not sufficient: it does not prove the page is readable or pleasant.
"""
import json
import pathlib
import sys

JS = r"""
(extraFields) => {
  const parse = c => { const m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(/[\s,\/]+/).filter(Boolean).map(Number); return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1]; };
  const lum = ([r, g, b]) => { const f = v => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const over = (top, under) => [0, 1, 2].map(i => top[i] * top[3] + under[i] * (1 - top[3])).concat(1);
  // Solid colour behind an element; null when an image or gradient is in the way.
  const behind = el => { const layers = [];
    for (let e = el; e; e = e.parentElement) { const cs = getComputedStyle(e);
      if (cs.backgroundImage !== 'none' || ['IMG', 'VIDEO', 'CANVAS'].includes(e.tagName)) return null;
      const c = parse(cs.backgroundColor); if (c && c[3] > 0) { layers.push(c); if (c[3] >= 1) break; } }
    return layers.reduceRight((base, c) => over(c, base), [255, 255, 255, 1]); };
  const visible = el => { const cs = getComputedStyle(el); const r = el.getBoundingClientRect();
    return cs.visibility !== 'hidden' && cs.display !== 'none' && r.width > 0 && r.height > 0; };
  const disabled = el => el.matches(':disabled, [aria-disabled="true"]') || !!el.closest('[aria-disabled="true"], fieldset:disabled');
  const name = el => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
    [...el.classList].slice(0, 2).map(c => '.' + c).join('');
  const text = [], fields = [], unchecked = [];

  for (const el of document.querySelectorAll('body *')) {
    const isField = el.matches('input:not([type=hidden]):not([type=checkbox]):not([type=radio]), textarea');
    const own = [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim();
    const sample = isField ? (el.value || '').trim() : own;
    if (!sample || !visible(el) || disabled(el)) continue;
    const cs = getComputedStyle(el), bg = behind(el);
    if (!bg) { unchecked.push({element: name(el), text: '(image or gradient behind) ' + sample.slice(0, 30)}); continue; }
    const size = parseFloat(cs.fontSize), large = size >= 24 || (parseInt(cs.fontWeight) >= 700 && size >= 18.66);
    const r = ratio(over(parse(cs.color), bg), bg), need = large ? 3 : 4.5;
    if (r < need) text.push({element: name(el), text: sample.slice(0, 40), ratio: +r.toFixed(2), need, size});
  }

  const sel = ['input:not([type=hidden])', 'textarea', 'select', '[contenteditable=""]', '[contenteditable="true"]',
    '[role=textbox]', '[role=combobox]', '[role=searchbox]'].concat(extraFields).join(',');
  for (const el of document.querySelectorAll(sel)) {
    if (!visible(el) || disabled(el)) continue;
    if (el.matches('input[type=checkbox], input[type=radio]') && getComputedStyle(el).appearance !== 'none') continue;
    // The boundary is the control's own border (an underline counts) or a wrapper outlined on all four sides;
    // a one-sided border on a wrapper is a divider, not the field's edge.
    const borders = e => { const cs = getComputedStyle(e);
      return ['Top', 'Right', 'Bottom', 'Left'].filter(s => parseFloat(cs['border' + s + 'Width']) > 0)
        .map(s => parse(cs['border' + s + 'Color'])).filter(c => c && c[3] > 0); };
    let box = borders(el).length ? el : null;
    for (let e = el.parentElement, i = 0; !box && e && i < 2; e = e.parentElement, i++) {
      if (borders(e).length === 4) box = e;
    }
    const fillOf = e => { const c = parse(getComputedStyle(e).backgroundColor); return c && c[3] > 0 ? c : null; };
    if (!box && fillOf(el)) box = el;
    if (!box) { unchecked.push({element: name(el), text: '(no visible boundary: is the field easy to find?)'}); continue; }
    const outside = behind(box.parentElement);
    if (!outside) { unchecked.push({element: name(el), text: '(field over image)'}); continue; }
    const borderR = Math.max(1, ...borders(box).map(c => ratio(over(c, outside), outside)));
    const fill = fillOf(box), fillR = fill ? ratio(over(fill, outside), outside) : 1;
    const best = Math.max(borderR, fillR);
    if (best < 3) fields.push({element: name(el), boundary: name(box), ratio: +best.toFixed(2), need: 3});
  }
  return {text, fields, unchecked};
}
"""


def launch(p):
    for kwargs in ({}, {"channel": "chrome"}, {"channel": "msedge"}):
        try:
            return p.chromium.launch(**kwargs)
        except Exception:
            continue
    raise SystemExit("No Chromium found. Run: python -m playwright install chromium")


def check(pages, themes, widths, theme_attr, extra_fields):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit("Playwright is required: pip install playwright && python -m playwright install chromium")
    results = []
    with sync_playwright() as p:
        browser = launch(p)
        for page_ref in pages:
            url = page_ref if "://" in page_ref else pathlib.Path(page_ref).resolve().as_uri()
            for theme in themes:
                for width in widths:
                    page = browser.new_page(viewport={"width": width, "height": 900}, color_scheme=theme)
                    page.goto(url)
                    page.wait_for_load_state("networkidle")
                    if theme_attr != "none":
                        page.evaluate("([a, t]) => document.documentElement.setAttribute(a, t)", [theme_attr, theme])
                    found = page.evaluate(JS, extra_fields)
                    results.append({"page": page_ref, "theme": theme, "width": width, **found})
                    page.close()
        browser.close()
    return results


def merge(results):
    """Same finding at several widths -> one line with the widths listed."""
    merged = {}
    for r in results:
        for kind in ("text", "fields", "unchecked"):
            for f in r[kind]:
                key = (r["page"], r["theme"], kind, json.dumps(f, sort_keys=True))
                merged.setdefault(key, {"page": r["page"], "theme": r["theme"], "kind": kind, **f, "widths": []})
                if r["width"] not in merged[key]["widths"]:
                    merged[key]["widths"].append(r["width"])
    return list(merged.values())


def option(argv, flag, default):
    return argv[argv.index(flag) + 1] if flag in argv and argv.index(flag) + 1 < len(argv) else default


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    themes = option(argv, "--themes", "light,dark").split(",")
    widths = [int(w) for w in option(argv, "--widths", "1440,390").split(",")]
    theme_attr = option(argv, "--theme-attr", "data-theme")
    extra = [argv[i + 1] for i, a in enumerate(argv) if a == "--field" and i + 1 < len(argv)]
    takes_value = {"--themes", "--widths", "--theme-attr", "--field"}
    pages = [a for i, a in enumerate(argv) if not a.startswith("--") and (i == 0 or argv[i - 1] not in takes_value)]
    if not pages:
        print(__doc__)
        return 2
    items = merge(check(pages, themes, widths, theme_attr, extra))
    failures = [i for i in items if i["kind"] != "unchecked"]
    if "--json" in argv:
        print(json.dumps({"failures": failures, "unchecked": [i for i in items if i["kind"] == "unchecked"]},
                         ensure_ascii=False, indent=1))
    else:
        for i in items:
            where = f"{i['page']} [{i['theme']}, {'/'.join(map(str, i['widths']))} px]"
            if i["kind"] == "text":
                print(f"text   {i['ratio']}:1 < {i['need']}:1  {where}  {i['element']}  \"{i['text']}\"")
            elif i["kind"] == "fields":
                print(f"field  {i['ratio']}:1 < 3:1  {where}  {i['element']} (boundary: {i['boundary']})")
            else:
                print(f"check by eye  {where}  {i['element']}  \"{i['text']}\"")
        unchecked = len(items) - len(failures)
        print(f"\n{len(failures)} contrast failure(s), {unchecked} unchecked item(s). "
              f"Themes: {', '.join(themes)}; widths: {', '.join(map(str, widths))} px.")
    return 1 if "--strict" in argv and failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
