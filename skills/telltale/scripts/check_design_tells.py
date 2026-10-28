#!/usr/bin/env python3
"""design-tells: ignore-file

Find AI design tells in UI source files (HTML, CSS, JS/TS/JSX/TSX, Vue, Svelte, Markdown).

  python check_design_tells.py PATH [PATH ...] [--strict] [--json]

Heuristic: every finding is a candidate with file:line for a person or agent to judge (fix, keep on purpose, or not
applicable). It never edits files. A line that contains `design-tells: ignore` is skipped (a deliberate use). --strict exits 1 when anything is found; --json prints machine-readable findings.
"""
import json
import os
import re
import sys

EXTENSIONS = {".html", ".htm", ".css", ".scss", ".sass", ".less", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".md", ".mdx"}
SKIP_DIRS = {".git", "node_modules", "dist", "build", ".next", "vendor", "coverage", "__pycache__"}

# (id, title, regex, flags, what to do)
CHECKS = [
    ("gradient", "Gradient", r"(?:linear|radial|conic)-gradient\(|bg-gradient-to-|from-\w+-\d{3}\s+to-", re.I,
     "Flat colour; keep a gradient only if it carries meaning (a scale)"),
    ("glass", "Glassmorphism / blur", r"backdrop-filter|backdrop-blur|filter:\s*blur\(", re.I, "Solid surfaces"),
    ("purple", "Purple/violet accent", r"#(?:7c3aed|8b5cf6|a855f7|6d28d9|9333ea|a78bfa|c084fc)\b|\b(?:purple|violet|fuchsia)-\d{3}\b", re.I,
     "Derive the accent from the subject"),
    ("neon", "Neon colour", r"#(?:0ff|00ffff|39ff14|ff00ff|f0f|00ff00)\b", re.I, "Muted, subject-derived colours"),
    ("pure-white", "Pure white background", r"background(?:-color)?\s*:\s*(?:#fff\b|#ffffff\b|white\b)|\bbg-white\b", re.I,
     "Off-white or tinted neutral; also a dark theme"),
    ("shadow", "Box shadow", r"box-shadow\s*:|\bshadow-(?:sm|md|lg|xl|2xl)\b", re.I, "Border or spacing; shadow only for real elevation"),
    ("radius-large", "Large/pill corner radius", r"border-radius\s*:\s*(?:1[2-9]|[2-9]\d|\d{3,})px|border-radius\s*:\s*(?:9999px|50%)|\brounded-(?:2xl|3xl|full)\b", re.I,
     "One small radius scale; pills only for tags"),
    ("left-stripe", "Coloured stripe on the left", r"border-left(?:-width)?\s*:\s*\d+px|border-left-color|inset\s+\d+px\s+0\s+0|\bborder-l-[2-8]\b", re.I,
     "Full thin border in the status colour, or a status word in the text"),
    ("hover-motion", "Hover motion (lift/scale/glow)", r":hover[^{]*\{[^}]*(?:transform|scale|translate|box-shadow)|hover:(?:scale|-?translate|shadow)", re.I | re.S,
     "Hover changes colour/underline only"),
    ("no-reduced-motion", "Animation without prefers-reduced-motion", r"@keyframes|animation\s*:", re.I,
     "Wrap or disable under @media (prefers-reduced-motion: reduce)"),
    ("default-font", "Default generated-UI typeface", r"\b(?:Inter|Geist|Space Grotesk)\b(?=[\"',;\s)])", 0,
     "Choose a typeface for the subject"),
    ("uppercase-label", "Uppercase letter-spaced labels", r"text-transform\s*:\s*uppercase|\buppercase\s+tracking-", re.I,
     "Sentence-case labels"),
    ("icon-set", "Default icon set", r"lucide|heroicons|react-icons|<svg\b", re.I, "Icons only where they help scanning"),
    ("sparkle", "Sparkle/AI decoration", r"sparkle|[\"'\s.-]blob[\"'\s-]|radial-glow|glow-orb|dot-grid|bg-dots|feTurbulence", 0, "Real content instead of decoration"),
    ("emoji", "Emoji", r"[\U0001F300-\U0001FAFF☀-⛿✀-➿]", 0, "No emoji as icons or bullets"),
    ("checkmark", "Checkmark bullets", r"[✓✔☑✅]", 0, "Plain list, or a table of what is included"),
    ("em-dash", "Long dash in copy", r"(?<![\"'`>(])—(?![\"'`<)])", 0, "Full stop, colon or comma; keep only where grammar requires (a lone \"—\" as an empty-value marker is not counted)"),
    ("gradient-text", "Gradient text", r"background-clip\s*:\s*text|bg-clip-text", re.I, "Solid text colour"),
    ("pure-black", "Pure black text or ground", r"(?:^|[;{\s])color\s*:\s*(?:#000\b|#000000\b|black\b)|background(?:-color)?\s*:\s*(?:#000\b|#000000\b|black\b)|\btext-black\b|\bbg-black\b", re.I, "Tinted near-black from the palette"),
    ("transition-all", "transition: all", r"transition\s*:\s*all\b|\btransition-all\b", re.I, "Transition only transform/opacity (or the one property that changes)"),
    ("bounce", "Bounce/elastic easing", r"cubic-bezier\([^)]*(?:-0?\.\d+|1\.[1-9])[^)]*\)|ease-?(?:out|in)?-?(?:back|elastic|bounce)|animate-bounce", re.I, "ease-out, 150-250 ms"),
    ("no-zoom", "Zoom disabled", r"user-scalable\s*=\s*no|maximum-scale\s*=\s*1(?:\.0)?\b", re.I, "Never disable zoom"),
    ("focus-removed", "Focus outline removed", r"outline\s*:\s*(?:none|0)\b", re.I, "Keep a visible :focus-visible style"),
    ("eyebrow", "Eyebrow/kicker label", r"class=\"[^\"]*\b(?:eyebrow|kicker|overline)\b|\b(?:eyebrow|kicker)\b\s*[:=]", re.I, "A plain heading that names the thing"),
    ("offset-shadow", "Hard offset shadow", r"box-shadow\s*:\s*-?\d+px\s+-?\d+px\s+0(?:px)?\s+(?:#|rgb|var|black)", re.I, "Border or a soft layered shadow for real elevation"),
    ("paste-blocked", "Paste blocked", r"onpaste\s*=|addEventListener\(\s*['\"]paste['\"][^)]*preventDefault", re.I, "Never block paste"),
    ("not-x-but-y", "\"Not X, but Y\" construction", r"\b(?:it'?s not|not just|isn'?t)\b[^.\n]{1,60},\s*(?:it'?s|but)\b|\bне\s+[^.\n<>]{1,50},\s*(?:а|это)\s", re.I,
     "Say what it is, directly"),
    ("vague-claim", "Vague marketing claim", r"\b(?:seamless(?:ly)?|next-gen(?:eration)?|revolutionary|supercharge|effortless(?:ly)?|cutting-edge|game-changing)\b|бесшовн|революционн|нового поколения", re.I,
     "A concrete fact: number, limit, example"),
    ("fake-social-proof", "Testimonials / trusted-by blocks", r"testimonial|trusted by|отзывы клиентов|нам доверяют", re.I, "Real quotes with permission, or nothing"),
    ("pricing-tiers", "Pricing tiers", r"pricing-tier|plan-card|\b(?:Starter|Pro|Enterprise)\b.*\b(?:Starter|Pro|Enterprise)\b", re.I, "Only plans that exist"),
    ("terminal-mock", "Terminal window mockup", r"terminal-window|window-dots|traffic-lights|class=\"[^\"]*terminal", re.I, "A real command with real output, or nothing"),
]

# Basics that should exist somewhere in a public product; reported as "not found" (missing), not as tells.
BASICS = [
    ("loading-state", "Loading state (skeleton/placeholder)", r"skeleton|aria-busy|loading|загрузк|загружа", re.I),
    ("empty-state", "Empty state", r"empty|пусто|нет данных|ничего не найдено|no results", re.I),
    ("error-state", "Error state", r"error|ошибк|не удалось|failed", re.I),
    ("privacy", "Privacy policy link", r"privacy|конфиденциальн", re.I),
    ("terms", "Terms of use link", r"terms|условия использования|пользовательское соглашение|оферт", re.I),
    ("reduced-motion", "prefers-reduced-motion", r"prefers-reduced-motion", re.I),
]


def files_of(paths):
    for path in paths:
        if os.path.isfile(path):
            yield path
            continue
        for root, dirs, names in os.walk(path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for name in names:
                if os.path.splitext(name)[1].lower() in EXTENSIONS:
                    yield os.path.join(root, name)


def line_of(text, index):
    return text.count("\n", 0, index) + 1


def scan(paths):
    findings, seen_basics, ui_files = [], {b[0]: False for b in BASICS}, 0
    for path in files_of(paths):
        try:
            text = open(path, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        if "design-tells: ignore-file" in text[:2000]:
            continue  # a file that describes the patterns (this skill, a style guide)
        if os.path.splitext(path)[1].lower() not in {".md", ".mdx"}:
            ui_files += 1
        else:
            # Fenced code in docs quotes commands and output; blank it out, keeping line numbers.
            text = re.sub(r"```.*?```", lambda m: re.sub(r"[^\n]", " ", m.group()), text, flags=re.S)
        for bid, _, pattern, flags in BASICS:
            if re.search(pattern, text, flags):
                seen_basics[bid] = True
        for cid, title, pattern, flags, advice in CHECKS:
            if cid == "no-reduced-motion":
                if re.search(pattern, text, flags) and not re.search(r"prefers-reduced-motion", text, re.I):
                    m = re.search(pattern, text, flags)
                    findings.append({"check": cid, "title": title, "file": path, "line": line_of(text, m.start()),
                                     "excerpt": text[m.start():m.start() + 80].splitlines()[0], "advice": advice})
                continue
            for m in re.finditer(pattern, text, flags):
                start = text.rfind("\n", 0, m.start()) + 1
                end = text.find("\n", m.end())
                if "design-tells: ignore" in text[start:end if end >= 0 else len(text)]:
                    continue  # a deliberate use, marked on its line
                excerpt = text[max(0, m.start() - 30):m.end() + 30].replace("\n", " ").strip()
                findings.append({"check": cid, "title": title, "file": path, "line": line_of(text, m.start()),
                                 "excerpt": excerpt[:120], "advice": advice})
    # The basics are about an interface: with no UI file scanned (docs only) nothing can be missing.
    missing = [{"check": bid, "title": title} for bid, title, _, _ in BASICS if not seen_basics[bid]] if ui_files else []
    return findings, missing


def main(argv):
    # A Windows console (cp1251, cp437) cannot print emoji from excerpts; replace them instead of crashing.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    strict, as_json = "--strict" in argv, "--json" in argv
    paths = [a for a in argv if not a.startswith("--")] or ["."]
    findings, missing = scan(paths)
    if as_json:
        print(json.dumps({"findings": findings, "missing_basics": missing}, ensure_ascii=False, indent=1))
    else:
        by = {}
        for f in findings:
            by.setdefault((f["check"], f["title"], f["advice"]), []).append(f)
        for (cid, title, advice), items in sorted(by.items(), key=lambda kv: -len(kv[1])):
            print(f"\n{title} [{cid}]: {len(items)}  ->  {advice}")
            for f in items[:8]:
                print(f"  {f['file']}:{f['line']}  {f['excerpt']}")
            if len(items) > 8:
                print(f"  ... and {len(items) - 8} more")
        if missing:
            print("\nBasics not found (check whether they apply):")
            for m in missing:
                print(f"  - {m['title']} [{m['check']}]")
        print(f"\n{len(findings)} candidate(s), {len(missing)} basic(s) not found.")
    return 1 if strict and (findings or missing) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
