# Human comparison: which design do people prefer?

Real people compare designs from the [blind comparison](../evals) and rank them. This matters more than the model
judges: the judges were models, and these answers come from the people the designs are for.

## What people see

Six tasks. Each shows **three or four anonymous variants** in a random order that differs for every person. A person can:

- open a variant as a live page inside the window, switch between computer and phone width, and between the light and
  dark theme, or go to the next variant;
- rank the variants (1 = best), flag the ones that look made by a neural network, and write a note;
- download one JSON file with the answer, or copy the same text.

Nobody is told which variant comes from which approach.

| Task | Kind of page |
| --- | --- |
| 1. Urban farm landing page | marketing page |
| 2. Hospital pharmacy stock screen | dense working screen |
| 3. Gym pass checkout | form |
| 4. Magazine long read | long text |
| 5. Household budget overview | working screen with charts |
| 6. Festival programme and tickets | timetable and tickets |

## The variants

| Condition | What it is | Tasks |
| --- | --- | --- |
| `telltale-r2` | built with this skill | 1–6 |
| `telltale-r1` | built with this skill before the round 2 changes (shows whether the changes help) | 1–3 |
| `frontend-design` | built with the `frontend-design` skill | 1–6 |
| `no-skill` | built without a skill | 1–6 |

## Share it

The page is in [`../docs/`](../docs): `index.html` and the designs in `d/`. Pick one way:

1. **GitHub Pages (a link).** In the repository: Settings, Pages, Build and deployment. Source: Deploy from a branch.
   Branch: `human-eval`, folder: `/docs`. Save. After a minute the page is at
   `https://<user>.github.io/telltale-design/`. Only `docs/` is published; `human-eval/` with the key is not.
2. **A zip of `docs/`.** People unzip it and open `index.html` in a browser. Everything works offline except the web
   fonts. When the page is opened from a file, some browsers hide the theme switch in the viewer.

## Collect the answers

Each person sends back a JSON file (`eval-<set>-<name>-<id>.json`). Put every file into [`answers/`](answers) and keep
them in the repository: they are the results.

```json
{
 "schema": "human-design-eval/1",
 "set": "2026-10-29",
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
with `complete: false` is left out of the counts, so a person may answer only some of the six.

## Restore who is who

The page shows only random four-character codes. [`KEY.json`](KEY.json) maps each code to its task and condition.

```bash
python tally.py answers/ KEY.json
```

For every condition the output has:

- **avg rank**: the average place (1 = best). Tasks with three and four variants are mixed, so a rank of 2 means
  different things in them;
- **score 0-1**: the place rescaled so that the best place is 1 and the worst is 0. It is comparable between tasks with
  three and four variants; use it to compare conditions;
- how often the condition was ranked first, how often people flagged it as AI-made, how often it was opened;
- the average rank per task and the number of votes behind it, and every written note.

Add `--set <id>` to count one set when `answers/` holds several. On a Windows console, set `PYTHONIOENCODING=utf-8` to
print Cyrillic notes.

**Blindness.** `KEY.json` is in this repository, but the page never loads it and GitHub Pages does not publish it. People
who only open the page or the zip cannot see it. Someone who browses the repository can. If that matters, remove
`KEY.json` from the branch before you share the link and keep it somewhere private: `tally.py` takes the path as an
argument.

## A new set

[`build_set.py`](build_set.py) builds a set from a JSON file that lists, per task, the page and the screenshots of each
condition (the screenshots come from `evals/run_eval.py`):

```bash
python build_set.py SPEC.json --out ../docs --key KEY.json
```

It writes the page and the designs with fresh random codes, removes scanner comments that would show which designs
came from a skill, and writes the key. Give a new set its own `set` id so old answers stay separate. The page itself is
[`template.html`](template.html).
