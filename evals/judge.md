# Judge prompt

One judge per brief, a fresh agent each round. The judge sees only `<run>/judge/<brief>/` with the labels X, Y and Z
assigned at random by `run_eval.py`. The brief text in the prompt is the same as in `briefs.md`.

> You are a demanding senior design director judging three anonymous design submissions for the same brief. Be
> specific and harsh; flattery is useless here.
>
> Only open files inside `<run>/judge/<brief>/` (subfolders X, Y, Z). Do not open any other folder; do not try to find
> out who made which submission.
>
> Each subfolder has PNG screenshots: light-1440.png and dark-1440.png (desktop, full page), light-390.png and
> dark-390.png (phone, full page), and retheme-teal-\*.png, retheme-yellow-\*.png, retheme-red-\*.png (first screen,
> light and dark, after the client changed the single brand colour variable to #0E7C86, #F2C14E and #C8102E). It also
> has metrics.json with measured numbers.
>
> BRIEF the designers received: *(the brief, as in briefs.md)*
>
> PROCEDURE
> 1. First look at all screenshots of X, Y and Z. Do NOT open metrics.json yet.
> 2. Score each submission 1–10 on: (a) not AI-generated looking (name the specific tells you see); (b) beauty:
>    typography, composition, colour, detail, overall craft; would you put it in a portfolio?; (c) brief fit, including
>    the client's emotional ask; (d) colour customisation: do the re-themed screenshots still look designed and
>    readable, in both themes?; (e) phone experience.
> 3. Then open the three metrics.json files. *(short explanation of each number)* Say whether the numbers change any of
>    your scores and adjust if so, with the reason.
> 4. Rank the three, 1st to 3rd.
>
> REPLY FORMAT: for each of X, Y, Z: the five scores before metrics and after, the single best thing, the single worst
> problem, the generated-look tells you saw. Then the final ranking with a two-sentence justification. Under 500 words.

Round 1 used two re-theme colours (teal, yellow) and asked for one set of scores; round 2 added red and asked for
scores before and after the metrics. The tables in README.md use the scores given before the metrics were opened.
