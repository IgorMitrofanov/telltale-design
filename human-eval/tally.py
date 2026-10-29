#!/usr/bin/env python3
"""Count the answers people sent back from the comparison page.

  python tally.py answers/ KEY.json [--set 2026-10-28]

answers/   a folder of the JSON files people sent (or one file). Files of other sets are skipped.
KEY.json   maps each design code to its brief and condition: {"set": "...", "codes": {"abcd": {"brief": "b1", "condition": "telltale-r2"}}}.
           Keep it out of the page you share, or the comparison is no longer blind.

Prints, for every condition: the average rank (1 = best), a score from 0 (worst place) to 1 (best place) that stays
comparable between tasks with three and four variants, how often it was ranked first, how often people flagged it as
AI-made, how often people opened it, and the written notes. A task that a person did not finish is left out for that
person.
"""
import collections, glob, json, os, sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="replace")  # a Windows console cannot print every note

args = [a for a in sys.argv[1:] if not a.startswith("--")]
if len(args) != 2:
    print(__doc__)
    sys.exit(2)
want_set = sys.argv[sys.argv.index("--set") + 1] if "--set" in sys.argv else None
key = json.load(open(args[1], encoding="utf-8"))
codes, set_id = key["codes"], want_set or key["set"]
paths = [args[0]] if os.path.isfile(args[0]) else sorted(glob.glob(os.path.join(args[0], "*.json")))

ranks, scores, firsts, ai, opened, notes = (collections.defaultdict(list), collections.defaultdict(list), collections.Counter(),
                                            collections.Counter(), collections.Counter(), collections.defaultdict(list))
people, seen_ids, skipped = 0, set(), []
for path in paths:
    try:
        answer = json.load(open(path, encoding="utf-8"))
    except ValueError:
        skipped.append((path, "not JSON")); continue
    if answer.get("schema") != "human-design-eval/1" or answer.get("set") != set_id:
        skipped.append((path, "other set or schema")); continue
    if answer["id"] in seen_ids:
        skipped.append((path, "same id as an earlier file; keep the later one")); continue
    seen_ids.add(answer["id"]); people += 1
    for brief, data in answer["briefs"].items():
        for code in data.get("opened", []):
            if code in codes: opened[(brief, codes[code]["condition"])] += 1
        for code in data.get("ai_flagged", []):
            if code in codes: ai[(brief, codes[code]["condition"])] += 1
        if data.get("note"):
            notes[brief].append(f"{answer.get('who') or 'anon'}: {data['note']}")
        if not data.get("complete"):
            continue
        for place, code in enumerate(data["ranking"], 1):
            cond = codes[code]["condition"]
            ranks[(brief, cond)].append(place)
            scores[(brief, cond)].append((len(data["ranking"]) - place) / (len(data["ranking"]) - 1))
            firsts[(brief, cond)] += place == 1

conditions = sorted({v["condition"] for v in codes.values()})
briefs = sorted({v["brief"] for v in codes.values()})
print(f"set {set_id}: {people} person(s), {len(skipped)} file(s) skipped")
for path, why in skipped:
    print(f"  skipped {path}: {why}")
print(f"\n{'condition':18} {'avg rank':>9} {'score 0-1':>10} {'1st':>5} {'AI-made':>8} {'opened':>7}   per brief: avg rank (votes)")
for cond in conditions:
    allr = [r for b in briefs for r in ranks[(b, cond)]]
    avg = f"{sum(allr) / len(allr):9.2f}" if allr else f"{'-':>9}"
    alls = [x for b in briefs for x in scores[(b, cond)]]
    sc = f"{sum(alls) / len(alls):10.2f}" if alls else f"{'-':>10}"
    per = "  ".join(f"{b} {sum(ranks[(b, cond)]) / len(ranks[(b, cond)]):.2f} ({len(ranks[(b, cond)])})"
                    if ranks[(b, cond)] else f"{b} -" for b in briefs)
    print(f"{cond:18} {avg} {sc} {sum(firsts[(b, cond)] for b in briefs):5} {sum(ai[(b, cond)] for b in briefs):8} "
          f"{sum(opened[(b, cond)] for b in briefs):7}   {per}")
for b in briefs:
    if notes[b]:
        print(f"\nNotes, {b}:")
        for n in notes[b]:
            print(f"  - {n}")
