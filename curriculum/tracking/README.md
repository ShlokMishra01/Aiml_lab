# AI Engineering Lab: Progress Tracker

The 24-week Excel workbook with check marks and visual dashboards.

## What you get

| Sheet | Purpose |
|---|---|
| **Dashboard** | Your name + start date; per-week status (☐/▶/✅), % bars, an overall completion number, a phase summary, and a progress chart |
| **Week 01 … 24** | Each week's day-by-day checklist (Mon to Fri + Milestone) with a status dropdown, in-cell progress bar, and a Notes column |
| **About** | How to use it |

## How to track your progress

1. Download `ai-engineering-lab-24-week-tracker.xlsx` (File → Download in GitHub).
2. Open in **Microsoft Excel**, **Google Sheets** (File → Import → Upload), or
   **LibreOffice Calc**. All three support the dropdowns, conditional colors, and
   formulas.
3. Fill in your name and start date on the Dashboard.
4. As you finish each week's tasks, set the Status cell to:
   - `☐ Not started`: default
   - `▶ In progress`: working on it (turns amber)
   - `✅ Done`: tick it off (turns green) ← this is your check mark
   - `⏭ Skipped`: deliberately skipped; counts against the week %; explain in Notes
5. The week sheet computes the week % and fills the `█░` progress bar; the Dashboard
   aggregates everything and updates the chart.

## Regenerating the workbook

The workbook is **generated**, not hand-edited. The single source of truth for the
program structure is [`../manifest.json`](../manifest.json).

```bash
pip install openpyxl
python scripts/build_tracker.py
```

To change the program (weeks, tasks, titles), edit `manifest.json` and regenerate,
never edit the `.xlsx` by hand. See [.github/CONTRIBUTING.md](../../.github/CONTRIBUTING.md).

## Tips

- Keep the workbook in your repo fork and commit it weekly, it doubles as a study log.
- The `Notes` column is where the learning actually lives: write the error you hit,
  the eval score you got, the thing that surprised you.
- At the end of the program your Dashboard chart should read 100% across all 24 weeks.
  Screenshot it for your portfolio. 🎓

---
© 2026 Zorost Intelligence LLC · https://zorost.com
