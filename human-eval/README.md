# Human comparison: which design do people prefer?

Real people compare the nine-plus pages from the [blind comparison](../evals) and rank them. This matters more than
the model judges: the judges were models, and these answers come from the people the designs are for.

## What people see

Three tasks (a farm landing page, a hospital stock screen, a gym checkout). Each task shows **four anonymous
variants** in a random order that differs for every person. A person can:

- open a variant as a live page inside the window, switch between computer and phone width, and between the light and
  dark theme, or go to the next variant;
- rank the four variants (1 = best, 4 = worst), flag the ones that look made by a neural network, and write a note;
- download one JSON file with the answer, or copy the same text.

Nobody is told which variant comes from which approach.

## The four variants per task

| Condition | What it is |
| --- | --- |
| `telltale-r2` | built with this skill, after the round 2 changes |
| `telltale-r1` | built with this skill, before the round 2 changes (shows whether the changes help) |
| `frontend-design` | built with the `frontend-design` skill |
| `no-skill` | built without a skill |

## Share it

The page is `site/index.html` with the designs in `site/d/`. Send people one of these:

1. **A link**, if you serve `site/` from any web host (for example GitHub Pages on this branch). Theme switching in the
   viewer works when the page is served over http.
2. **A zip of the `site/` folder.** People unzip it and open `index.html` in a browser. Everything works offline except
   the web fonts. On some browsers the theme switch in the viewer is hidden when the page is opened from a file.

## Collect the answers

Each person sends back a JSON file (`eval-<set>-<name>-<id>.json`). Put every file into [`answers/`](answers) and keep
them in the repository: they are the results.

```json
{
 "schema": "human-design-eval/1",
 "set": "2026-10-28",
 "id": "93ngzc",
 "who": "Anna",
 "device": { "width": 390, "touch": true, "dark": true },
 "briefs": {
  "b1": {
   "complete": true,
   "shown_order": ["97fk", "t9b8", "q5k7", "4myg"],
   "ranking": ["t9b8", "97fk", "4myg", "q5k7"],
   "ai_flagged": ["q5k7"],
   "opened": ["t9b8", "97fk", "q5k7"],
   "note": "..."
  }
 }
}
```

`ranking` lists the codes from best to worst. `opened` shows which variants the person actually looked at. A task
with `complete: false` is left out of the counts.

## Restore who is who

The page shows only random four-character codes. [`KEY.json`](KEY.json) maps each code to its task and condition.

```bash
python tally.py answers/ KEY.json
```

The output is the average rank of each condition (1 = best, 4 = worst), how often it was ranked first, how often people
flagged it as AI-made, how often it was opened, and every written note. Add `--set <id>` to count one set when
`answers/` holds several. On a Windows console, set `PYTHONIOENCODING=utf-8` to print Cyrillic notes.

**Blindness.** `KEY.json` is in this repository, but the page never loads it. People who only open the page or the zip
cannot see it. Someone who browses the repository can. If that matters, remove `KEY.json` from the branch before you
share the link and keep it somewhere private: `tally.py` takes the path as an argument.

## A new set

To compare new designs, build a new set with fresh random codes and a new set id, so old answers stay separate. The
code in `site/index.html` reads the set id from its `SET` constant; answers of other sets are skipped by `tally.py`.
