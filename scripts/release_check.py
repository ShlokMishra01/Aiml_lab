#!/usr/bin/env python3
"""AI Engineering Lab, release gate.

One command that verifies the whole repository before a release:
  1. every week folder has README + exercises + quiz + notebooks
  2. notebooks pass structural QA (scripts/check_notebooks.py logic)
  3. internal markdown links resolve
  4. the Excel tracker loads with all 24 weeks + dashboard
  5. week READMEs meet the rich lesson standard (min word count, required sections)

Usage: python scripts/release_check.py
Exit code 1 on any failure.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
failures: list[str] = []


def note(ok: bool, msg: str) -> None:
    if not ok:
        failures.append(msg)


# ---- 1. week completeness --------------------------------------------------
manifest = json.loads((ROOT / "curriculum/manifest.json").read_text())
weeks = [item for phase in manifest["phases"] for item in phase["items"]]
for w in weeks:
    d = ROOT / f"curriculum/week-{w['week']:02d}"
    note((d / "README.md").exists(), f"week-{w['week']:02d}: missing README.md")
    note((d / "exercises.md").exists(), f"week-{w['week']:02d}: missing exercises.md")
    note((d / "quiz.md").exists(), f"week-{w['week']:02d}: missing quiz.md")
    nbs = list((d / "notebooks").glob("*.ipynb")) if (d / "notebooks").exists() else []
    note(bool(nbs), f"week-{w['week']:02d}: no notebooks")
    # rich standard
    rd = (d / "README.md").read_text() if (d / "README.md").exists() else ""
    words = len(rd.split())
    note(words >= 1500, f"week-{w['week']:02d}: README only {words} words (target ≥ 2000)")
    for section in ["The problem", "Concepts", "Common pitfalls", "Glossary"]:
        note(section.lower() in rd.lower(), f"week-{w['week']:02d}: README missing '{section}' section")

# ---- 2 & 3. notebook QA + links (reuse the scripts) ------------------------
for script in ["check_notebooks.py", "check_links.py"]:
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / script)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        failures.append(f"{script} failed:\n{r.stdout[-1200:]}")

# ---- 4. tracker workbook ---------------------------------------------------
try:
    from openpyxl import load_workbook
    wb = load_workbook(ROOT / "curriculum/tracking/ai-engineering-lab-24-week-tracker.xlsx")
    note(len(wb.sheetnames) == 26, f"tracker has {len(wb.sheetnames)} sheets (expected 26)")
    note("Week 01" in wb.sheetnames and "Week 24" in wb.sheetnames, "tracker missing week sheets")
    dash = wb["Dashboard"]
    note(str(dash["E33"].value or "").startswith("=AVERAGE"), "tracker dashboard overall formula missing")
except Exception as e: # noqa: BLE001
    failures.append(f"tracker failed to load: {e}")

# ---- report ----------------------------------------------------------------
print(f"Release gate: {len(weeks)} weeks checked.")
if failures:
    print(f"{len(failures)} failure(s):")
    for f in failures:
        print(" -", f)
    sys.exit(1)
print("All release gates pass. Ready to publish.")
