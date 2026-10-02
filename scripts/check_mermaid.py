#!/usr/bin/env python3
"""AI Engineering Lab: mermaid diagram checker.

Every ```mermaid block must open with the shared init line, which pins a light
theme and navy text so the diagram stays legible on the light and the dark
GitHub page. Every node and edge label holding a character the flowchart grammar
treats as syntax must be wrapped in double quotes, otherwise GitHub renders a
parse error box in place of the diagram.
Exit code 1 if any block fails either rule.

Usage: python scripts/check_mermaid.py [--fix] [--verbose]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# fontFamily is read from the top level of the config. In themeVariables it is
# accepted and ignored, and the diagram silently falls back to Trebuchet.
INIT_LINE = (
    '%%{init:{"theme":"base",'
    '"fontFamily":"Helvetica Neue,Helvetica,Arial,sans-serif",'
    '"flowchart":{"curve":"basis","padding":14,'
    '"nodeSpacing":45,"rankSpacing":55},"themeVariables":'
    '{"fontSize":"15px",'
    '"background":"#FFFFFF","primaryColor":"#EEF2F7","primaryTextColor":"#14213D",'
    '"primaryBorderColor":"#14213D","secondaryColor":"#FFF1E3",'
    '"secondaryTextColor":"#14213D","tertiaryColor":"#E7F4F1",'
    '"tertiaryTextColor":"#14213D","lineColor":"#64748B","textColor":"#14213D",'
    '"edgeLabelBackground":"#FFFFFF","clusterBkg":"#F5F8FC",'
    '"clusterBorder":"#94A3B8","nodeBorder":"#14213D","mainBkg":"#EEF2F7",'
    '"titleColor":"#14213D"}}}%%'
)

# The pipe closes an edge label and a word-char followed by @ opens a mermaid 11
# link id, so both break a diagram from inside an unquoted label.
UNSAFE_CHARS = '():;#%&{}"|@'
END_WORD = re.compile(r"\bend\b", re.IGNORECASE)

# Styling lines carry colours such as fill:#EEF2F7 that would read as labels.
SKIP_LINE = re.compile(r"^\s*(classDef|class\s|style\s|linkStyle|click\s|direction\s|%%)")

DASH_LABEL = re.compile(r"^--\s+(?P<t>\S.*?)\s+--[->]")
DOT_LABEL = re.compile(r"^-\.(?P<t>[^.\n]+)\.->")
EQ_LABEL = re.compile(r"^==\s*(?P<t>\S.*?)\s*==>")

# Longest openers first, so [( is never read as a plain [.
PAIRS = [("[(", ")]"), ("([", "])"), ("[[", "]]"), ("((", "))"), ("{{", "}}"),
         ("[/", "/]"), ("[\\", "\\]")]

issues: list[str] = []
blocks = 0


def needs_quotes(inner: str) -> bool:
    s = inner.strip()
    if not s:
        return False
    if s.startswith('"') and s.endswith('"') and len(s) > 1:
        return False
    return any(c in UNSAFE_CHARS for c in s) or bool(END_WORD.search(s))


def match_nested(line: str, start: int, open_ch: str, close_ch: str) -> int:
    depth = 0
    for i in range(start, len(line)):
        if line[i] == open_ch:
            depth += 1
        elif line[i] == close_ch:
            depth -= 1
            if depth == 0:
                return i
    return -1


def scan_labels(line: str) -> list[str]:
    """Return the inner text of every node and edge label in a mermaid statement."""
    if SKIP_LINE.match(line):
        return []
    found: list[str] = []
    i = 0
    while i < len(line):
        rest = line[i:]
        pair = next((p for p in PAIRS if rest.startswith(p[0])), None)
        if pair:
            j = line.find(pair[1], i + len(pair[0]))
            if j != -1:
                found.append(line[i + len(pair[0]) : j])
                i = j + len(pair[1])
                continue
            i += len(pair[0])
            continue
        ch = line[i]
        if ch in "[{":
            j = match_nested(line, i, ch, "]" if ch == "[" else "}")
            if j != -1:
                found.append(line[i + 1 : j])
                i = j + 1
                continue
        elif ch == "(" and i and (line[i - 1].isalnum() or line[i - 1] == "_"):
            j = match_nested(line, i, "(", ")")
            if j != -1:
                found.append(line[i + 1 : j])
                i = j + 1
                continue
        elif ch == "|":
            j = line.find("|", i + 1)
            if j != -1:
                found.append(line[i + 1 : j])
                i = j + 1
                continue
        elif ch in "-=":
            m = DASH_LABEL.match(rest) or DOT_LABEL.match(rest) or EQ_LABEL.match(rest)
            if m:
                found.append(m.group("t"))
                i += m.end()
                continue
        i += 1
    return found


def find_blocks(lines: list[str]) -> list[tuple[int, int]]:
    """Return (fence index, closing fence index) for every ```mermaid block."""
    spans = []
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith("```mermaid"):
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("```"):
                j += 1
            spans.append((i, j))
            i = j + 1
        else:
            i += 1
    return spans


def main() -> int:
    global blocks
    fix = "--fix" in sys.argv
    verbose = "--verbose" in sys.argv
    fixed = 0

    for md in sorted(ROOT.rglob("*.md")):
        if "reference/knowledge-base/research" in str(md):
            continue  # raw working notes, not curated content
        lines = md.read_text(errors="ignore").split("\n")
        spans = find_blocks(lines)
        if not spans:
            continue
        rel = md.relative_to(ROOT)
        before = len(issues)
        inserts = []

        for fence, close in spans:
            blocks += 1
            body = range(fence + 1, close)
            if not any(lines[k] == INIT_LINE for k in body):
                if any(lines[k].lstrip().startswith("%%{init") for k in body):
                    issues.append(f"{rel}:{fence + 1} init line is not the shared one")
                elif fix:
                    inserts.append(next((k for k in body if lines[k].strip()), fence + 1))
                else:
                    issues.append(f"{rel}:{fence + 1} missing init line")
            for k in body:
                for label in scan_labels(lines[k]):
                    if needs_quotes(label):
                        issues.append(f"{rel}:{k + 1} unquoted label: {label}")

        for k in sorted(inserts, reverse=True):
            lines.insert(k, INIT_LINE)
            fixed += 1
        if inserts:
            md.write_text("\n".join(lines))

        if len(issues) > before:
            print(f"FAIL {rel} ({len(issues) - before})")
        elif verbose:
            print(f"ok   {rel} ({len(spans)} blocks)")

    print(f"\nChecked {blocks} mermaid blocks.")
    if fixed:
        print(f"Inserted {fixed} missing init lines.")
    if issues:
        print(f"{len(issues)} problems:")
        for i in issues:
            print(" -", i)
        return 1
    print("All mermaid blocks are themed and parse-safe.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
