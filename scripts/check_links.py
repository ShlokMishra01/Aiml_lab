#!/usr/bin/env python3
"""AI Engineering Lab, markdown cross-link checker.

Verifies that relative markdown links (and links to knowledge-base/notebook files)
inside the repo resolve. Skips external http(s) links, anchors, and images.
Exit code 1 if broken links are found.

Usage: python scripts/check_links.py [--verbose]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
issues: list[str] = []
checked = 0


def resolve(md_file: Path, target: str) -> Path | None:
    t = target.split("#")[0].strip()
    if not t or t.startswith(("http://", "https://", "mailto:")):
        return None
    t = unquote(t).split("?")[0]
    if t.startswith("/"):
        return ROOT / t.lstrip("/")
    return (md_file.parent / t).resolve()


def main() -> int:
    global checked
    verbose = "--verbose" in sys.argv
    for md in sorted(ROOT.rglob("*.md")):
        if "reference/knowledge-base/research" in str(md):
            continue # raw working notes, not curated content
        text = md.read_text(errors="ignore")
        # strip fenced code blocks so inline-code spans aren't mistaken for links
        text = re.sub(r"```.*?```", " ", text, flags=re.S)
        for m in LINK_RE.finditer(text):
            target = m.group(1)
            resolved = resolve(md, target)
            if resolved is None:
                continue # external or anchor
            checked += 1
            if not resolved.exists():
                issues.append(f"{md.relative_to(ROOT)} -> {target}")
            elif verbose:
                print(f"ok {md.relative_to(ROOT)} -> {target}")
    print(f"\nChecked {checked} internal markdown links.")
    if issues:
        print(f"{len(issues)} broken:")
        for i in issues:
            print(" -", i)
        return 1
    print("All markdown links resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
