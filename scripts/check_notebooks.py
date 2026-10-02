#!/usr/bin/env python3
"""AI Engineering Lab, notebook QA.

Validates every.ipynb in the repo:
  1. parses as JSON with nbformat 4
  2. has the required metadata block
  3. first cell is markdown with a title + requirements line
  4. ends with a code cell that prints a number (metric discipline)
  5. no non-empty outputs committed (clean notebooks)

Usage: python scripts/check_notebooks.py [--verbose]
Exit code 1 if any notebook fails.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
issues: list[str] = []


def check(nb_path: Path) -> None:
    name = str(nb_path.relative_to(ROOT))
    try:
        nb = json.loads(nb_path.read_text())
    except Exception as e:
        issues.append(f"{name}: not valid JSON ({e})")
        return
    if nb.get("nbformat") != 4:
        issues.append(f"{name}: nbformat != 4")
        return
    cells = nb.get("cells", [])
    if not cells:
        issues.append(f"{name}: no cells")
        return
    # metadata
    md = nb.get("metadata", {})
    if md.get("kernelspec", {}).get("language") != "python":
        issues.append(f"{name}: missing python kernelspec")
    # first cell markdown w/ title
    first = cells[0]
    first_src = "".join(first.get("source", []))
    if first.get("cell_type") != "markdown":
        issues.append(f"{name}: first cell is not markdown")
    elif "#" not in first_src:
        issues.append(f"{name}: first cell has no markdown heading")
    if "Requirements" not in first_src:
        issues.append(f"{name}: first cell missing '# Requirements' line")
    # last code cell prints a number
    last_code = next((c for c in reversed(cells) if c.get("cell_type") == "code"), None)
    if last_code is None:
        issues.append(f"{name}: no code cells")
    else:
        src = "".join(last_code.get("source", []))
        if "print" not in src:
            issues.append(f"{name}: last code cell does not print a metric")
    # no committed outputs
    for i, c in enumerate(cells):
        if c.get("cell_type") == "code" and c.get("outputs"):
            issues.append(f"{name}: cell {i} has committed outputs")
    # code cells must be syntactically valid Python (skip magic-first cells)
    import ast
    for i, c in enumerate(cells):
        if c.get("cell_type") != "code":
            continue
        src = "".join(c.get("source", []))
        first = src.strip().splitlines()[0] if src.strip() else ""
        if first.startswith(("%", "!")):
            continue
        try:
            ast.parse(src)
        except SyntaxError as e:
            issues.append(f"{name}: cell {i} is not valid Python ({e.msg})")


def main() -> int:
    verbose = "--verbose" in sys.argv
    nbs = sorted(ROOT.glob("**/*.ipynb"))
    for nb in nbs:
        check(nb)
        if verbose:
            print(f"checked {nb.relative_to(ROOT)}")
    print(f"\nChecked {len(nbs)} notebooks.")
    if issues:
        print(f"{len(issues)} issue(s):")
        for i in issues:
            print(" -", i)
        return 1
    print("All notebooks pass QA.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
