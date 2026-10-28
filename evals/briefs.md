<!-- design-tells: ignore-file (prompts for the comparison; quoted client words) -->
# Prompts used in the comparison

Every builder got the same text: the opening, one method line, one brief, the technical rules. Only the method line
and the output path differ. Builders were not told that they were being compared.

## Opening

> You are designing a web page for a client. Work like a senior product designer who also writes the code.

## Method line (one per condition)

| Condition | Method line |
|---|---|
| `t` telltale | Design method: before you start, read the design skill at `<path>/skills/telltale/SKILL.md` completely and follow it, including its scripts in the same folder (`scripts/check_design_tells.py` and `scripts/check_contrast.py`). Do not modify the skill files. |
| `f` frontend-design | Design method: before you start, invoke the Skill tool with the skill named `frontend-design` and follow its guidance. If that skill cannot be loaded, say so in your reply and continue without it. |
| `n` no skill | Design method: use your own judgment. Do not load or use any skill. |

## Briefs

**B1, landing page (Persuade).** Client: Polder & Plot, a community-supported urban farm in Rotterdam. They sell a
weekly vegetable box grown on a 2-hectare farm on a former harbour site. Page: the public landing page. Audience: city
households, 25–55, who care about food but are busy. The page must: explain how the box works (choose a size, weekly
pickup at one of 4 points or delivery by cargo bike, pause any week), show this week's box contents, show prices
(Small €17/week, Large €27/week, cargo-bike delivery +€4), introduce the farm and its growers briefly, answer 4 FAQs,
and end with a clear sign-up action. The client said: "We don't want to look like every other organic brand: no kraft
paper, no leaves everywhere. We want people to stop scrolling." Brand colour today: #2F6B3A.

**B2, dashboard (Operate).** Client: the pharmacy of St. Elisabeth, a 300-bed hospital. Page: the morning stock screen
pharmacists open at 7:00, on a desktop and sometimes on a phone. It must show: items below minimum stock (current,
minimum, daily use, days left), items expiring within 30 days (batch, expiry date, quantity, ward), today's open orders
from wards (ward, items, priority urgent/normal, requested time), and supplier deliveries expected today. Provide
realistic data: at least 8 low-stock rows, 6 expiring, 7 orders, 3 deliveries. It must be obvious within 5 seconds what
needs action first. The head pharmacist said: "Everyone's dashboards look the same. Ours should feel like it was made
for this pharmacy, but it must stay calm and fast to read." Brand colour today: #1F5FAD.

**B3, checkout form.** Client: Overhang, a bouldering gym in Leeds. Page: buy a pass online. Passes: day pass £14,
10-visit card £120, monthly membership £58/month (cancel any time). The flow is on one page: choose a pass, choose a
start date, enter name, email and date of birth (under-18s must add a guardian's name), accept the waiver, and pay
(show a summary with the total; the card form itself can be a static placeholder block). Show validation messages for
at least 2 fields in a static error state, so the error design is visible. The owner said: "Climbers hate corporate.
Make it feel like our wall, not like a bank." Brand colour today: #E4572E, but they are rebranding next year and the
colour will change.

After each brief:

> The client will judge four things: it looks hand-made by a designer rather than AI-generated; it is genuinely
> beautiful; it does everything the brief asks; the colour customisation works.

## Technical rules (same for every builder)

- One self-contained file: `<run>/<brief>/<condition>/index.html`. Google Fonts allowed; no other network resources (no
  images from the internet, no JS libraries). Any imagery must be made with CSS, inline SVG or type.
- Must work at 1440 px and 390 px wide without horizontal scroll (B2: wide tables may scroll inside their own box).
- Light and dark theme: follow prefers-color-scheme, and also honour `data-theme="light"` / `data-theme="dark"` on `<html>`.
- Brand colour: the client will change it later. Define it as one CSS custom property `--brand` on `:root`. Changing
  that one value must re-theme the page and keep it readable.
- Interface copy in English. Invent realistic content; no lorem ipsum.
- You may render the page with Python Playwright to look at screenshots and iterate. Put helper files in the `work/`
  subfolder next to index.html.
- Do not look at other folders of the run.

When finished, reply with: the file path, a 3-sentence description of your design idea, and what you checked.
