#!/usr/bin/env python3
"""AI Engineering Lab, build the program site served by GitHub Pages.

The week list is generated from curriculum/manifest.json, so the page cannot
drift from the curriculum, and the README diagrams are converted to WebP for
the page while the README keeps the PNGs that GitHub renders everywhere.

Usage: python scripts/build_site.py [--check]
  --check  exit 1 if docs/index.html is out of date instead of writing it
"""
from __future__ import annotations

import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
IMG = DOCS / "assets" / "img"
REPO = "https://github.com/zorost/AI-Engineering-Lab"
TREE = f"{REPO}/tree/main"
BLOB = f"{REPO}/blob/main"
SITE = "https://zorost.com"

# Phase accent, in program order, matching the diagram palette.
ACCENT = ["#0E9384", "#4260E8", "#7C4DE0", "#DC3A72", "#E8940C", "#566172", "#F14B21"]

FIGURES = [
    ("lab-journey", "Seven phases across 24 weeks, and what each one puts in your hands."),
    ("lab-week", "One week, four beats: study, build, ship, reflect."),
    ("lab-case", "The same ZoroLogistics tables, revisited six times at a higher level."),
    ("lab-framework", "The four skills and three loops the curriculum implements."),
    ("lab-stack", "Every layer of the stack, and the weeks that install it."),
    ("lab-map", "The repository, top level, and the two places to start."),
]


def clean(s: str) -> str:
    """House style: no em or en dashes in published text."""
    s = re.sub(r"(\d)\s*[\u2013\u2014]\s*(\d)", r"\1 to \2", s)
    s = re.sub(r"\s*[\u2013\u2014]\s*", ", ", s)
    return s


def esc(s: str) -> str:
    return html.escape(clean(str(s)), quote=True)


def week_card(item: dict, accent: str) -> str:
    n = item["week"]
    slug = f"curriculum/week-{n:02d}"
    nb = len(item.get("notebooks", []))
    meta = f"{nb} notebook{'s' if nb != 1 else ''}, use case, quiz" if nb else "use case, quiz"
    return (
        f'<li><a href="{TREE}/{slug}" style="--c:{accent}">'
        f'<span class="wn">W{n:02d}</span><span>'
        f'<span class="wt">{esc(item["title"])}</span>'
        f'<span class="wo">{esc(item["objective"])}</span>'
        f'<span class="wu mono">{meta}</span>'
        f"</span></a></li>"
    )


def phase_block(phase: dict, accent: str, idx: int) -> str:
    weeks = "".join(week_card(i, accent) for i in phase["items"])
    return (
        f'<div class="phase" data-phase="{idx}">'
        f'<h3><span class="n" style="--c:{accent}">Phase {idx}</span>'
        f"{esc(phase['name'])}"
        f'<span class="w mono">Weeks {esc(phase["weeks"])}</span></h3>'
        f"<p>{esc(phase['description'])}</p>"
        f'<ul class="weeks">{weeks}</ul></div>'
    )


def figure(fig_id: str, caption: str, w: int, h: int) -> str:
    return (
        f'<figure><img src="assets/img/{fig_id}.webp" width="{w}" height="{h}" '
        f'loading="lazy" decoding="async" alt="{esc(caption)}">'
        f"<figcaption>{esc(caption)}</figcaption></figure>"
    )


def convert_diagrams() -> dict[str, tuple[int, int]]:
    """Copy the README diagrams into the site as WebP. Returns logical sizes."""
    from PIL import Image

    IMG.mkdir(parents=True, exist_ok=True)
    sizes: dict[str, tuple[int, int]] = {}
    wanted = {fid for fid, _ in FIGURES}
    for src in sorted((ROOT / "assets" / "diagrams").glob("lab-*.png")):
        if src.stem not in wanted:
            continue
        im = Image.open(src).convert("RGB")
        im.save(IMG / f"{src.stem}.webp", "WEBP", quality=88, method=6)
        sizes[src.stem] = (im.width // 2, im.height // 2)
    return sizes


def course_ld(m: dict) -> str:
    """Course structured data, the object an answer engine looks for.

    The @id and url point at zorost.com, the canonical page this one already
    declares, so search and AI crawlers read both surfaces as one program
    rather than two competing copies.
    """
    weeks = [w for p in m["phases"] for w in p["items"]]
    notebooks = sum(len(w.get("notebooks", [])) for w in weeks)
    page = f"{SITE}/ai-engineering-lab"
    data = {
        "@context": "https://schema.org",
        "@type": "Course",
        "@id": f"{page}#course",
        "name": "AI Engineering Lab",
        "url": page,
        "description": clean(
            f"A free, open, self paced {len(weeks)} week AI engineering program: Python, "
            f"machine learning, large language models, retrieval, fine-tuning, agents, "
            f"three public clouds, and a governed Databricks lakehouse. "
            f"{notebooks} runnable notebooks and one continuous case study. MIT licensed."
        ),
        "provider": {
            "@type": "Organization",
            "name": "Zorost Intelligence AI Lab",
            "url": f"{SITE}/ai-lab",
        },
        "educationalProgramMode": "part-time",
        "educationalLevel": "Beginner to advanced",
        "inLanguage": "en",
        "isAccessibleForFree": True,
        "license": "https://opensource.org/licenses/MIT",
        "codeRepository": REPO,
        "timeRequired": f"P{len(weeks)}W",
        "teaches": [clean(p["name"]) for p in m["phases"]],
        "keywords": ", ".join([
            "free AI engineering course", "AI engineering curriculum",
            "LLM engineering course", "RAG tutorial", "fine-tuning course",
            "AI agents course", "MCP tutorial", "Databricks learning path",
            "open source AI course", "AI engineer roadmap",
        ]),
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "category": "Free"},
        "hasCourseInstance": {
            "@type": "CourseInstance",
            "courseMode": "online",
            "courseWorkload": "PT10H",
            "url": "https://zorost.github.io/AI-Engineering-Lab/",
            "courseSchedule": {
                "@type": "Schedule",
                "duration": "PT10H",
                "repeatFrequency": "weekly",
                "repeatCount": len(weeks),
            },
        },
        "syllabusSections": [
            {
                "@type": "Syllabus",
                "position": i + 1,
                "name": clean(f"Week {w['week']}: {w['title']}"),
                "description": clean(w["objective"]),
                "timeRequired": "PT10H",
                "url": f"{TREE}/curriculum/week-{w['week']:02d}",
            }
            for i, w in enumerate(weeks)
        ],
    }
    return (
        '<script type="application/ld+json">'
        + json.dumps(data, separators=(",", ":"))
        + "</script>"
    )


def render(m: dict, sizes: dict[str, tuple[int, int]]) -> str:
    phases = m["phases"]
    chips = "".join(
        f'<button class="chip" type="button" aria-pressed="false" data-f="{i + 1}">'
        f'<span class="d" style="--c:{ACCENT[i]}"></span>{esc(p["name"])}</button>'
        for i, p in enumerate(phases)
    )
    blocks = "".join(phase_block(p, ACCENT[i], i + 1) for i, p in enumerate(phases))
    figs = {fid: figure(fid, cap, *sizes.get(fid, (900, 600))) for fid, cap in FIGURES}
    nav = [
        ("#program", "Program"),
        ("#weeks", "Week by week"),
        ("#rhythm", "How a week works"),
        ("#case", "Case study"),
        ("#start", "Start"),
    ]
    links = "".join(f'<li><a class="l" href="{h}">{t}</a></li>' for h, t in nav)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Engineering Lab, a free 24 week AI engineering program | Zorost Intelligence</title>
<meta name="description" content="A free, open, self paced 24 week training program that takes you from your first Python notebook to an AI system in production. Seven phases, 43 runnable notebooks, one continuous case study. MIT licensed, no signup.">
<link rel="canonical" href="{SITE}/ai-engineering-lab">
<meta property="og:title" content="AI Engineering Lab, first notebook to production in 24 weeks">
<meta property="og:description" content="A free, open, self paced AI engineering program from Zorost Intelligence AI Lab. Seven phases, 43 runnable notebooks, one continuous case study.">
<meta property="og:type" content="website">
<meta property="og:image" content="{BLOB}/assets/diagrams/social-preview.png?raw=true">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="assets/style.css">
{course_ld(m)}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<div class="nav"><div class="wrap">
<a class="mark mono" href="#top">AI ENGINEERING <span>LAB</span></a>
<ul>{links}</ul>
<a class="gh mono" href="{REPO}">GitHub</a>
</div></div>

<header class="hero" id="top">
<div class="tex" aria-hidden="true"></div><div class="scrim" aria-hidden="true"></div>
<div class="wrap">
<span class="eyebrow mono">Zorost Intelligence AI Lab &middot; Training 01</span>
<h1>First notebook to a system in <em>production</em>, in 24 weeks</h1>
<p class="lede">AI Engineering Lab is a free, open, self paced training program. Seven phases,
43 runnable notebooks, one fictional company whose data carries every week, and a
number on every artifact you ship.</p>
<div class="cta">
<a class="btn p" href="{TREE}/curriculum/week-01">Start Week 1</a>
<a class="btn s" href="{BLOB}/START-HERE.md">Read START-HERE first</a>
</div>
<div class="facts">
<div><span class="n">24 weeks</span><span class="l mono">About ten hours a week</span></div>
<div><span class="n">43</span><span class="l mono">Runnable notebooks</span></div>
<div><span class="n">$0</span><span class="l mono">MIT licensed, no signup</span></div>
</div>
</div>
</header>

<main id="main">

<section id="program">
<div class="wrap">
<div class="k mono">The program</div>
<h2>A curriculum, not a playlist</h2>
<p class="sub">This is the sequence the Lab would hand a new engineer joining a generative AI,
applied machine learning, or Databricks modernization team. Every week ends in something that
runs, and from Week 3 on, nothing counts as finished until it carries a metric and an honest
note about where it failed.</p>
<p class="sub">Nothing is dropped when a phase ends. The dataset you generate in Week 1 is the
same dataset behind the governed feature tables in Week 23, which is why the order matters
more than any single topic.</p>
{figs["lab-journey"]}
</div>
</section>

<section id="weeks">
<div class="wrap">
<div class="k mono">Week by week</div>
<h2>All 24 weeks, open in a click</h2>
<p class="sub">Every week folder holds a README with the plan, the runnable notebooks, a Friday
use case, and a ten question quiz. Filter by phase, then open the week you want to read.</p>
<div class="filters" role="group" aria-label="Filter weeks by phase">
<button class="chip" type="button" aria-pressed="true" data-f="all">All 24 weeks</button>
{chips}
</div>
{blocks}
</div>
</section>

<section id="rhythm">
<div class="wrap">
<div class="k mono">How a week works</div>
<h2>Every week runs the same four beats</h2>
<p class="sub">The rhythm is the method. About ten hours, split across four beats, then the next
week starts on what you shipped in the last one.</p>
{figs["lab-week"]}
<table>
<thead><tr><th>Beat</th><th>When</th><th>What you do</th></tr></thead>
<tbody>
<tr><td>Study</td><td>Mon to Tue</td><td>The week README and the one knowledge base file it points to.</td></tr>
<tr><td>Build</td><td>Wed to Thu</td><td>Run the notebooks, then change them and break one thing on purpose.</td></tr>
<tr><td>Ship</td><td>Friday</td><td>The use case exercise: one artifact, one number, one honest note.</td></tr>
<tr><td>Reflect</td><td>Fri to Sun</td><td>Ten question quiz, pass at eight, then tick the tracker row.</td></tr>
</tbody>
</table>
<div class="note"><span class="l">The invariant</span><p>From Week 3 onward, no artifact is
finished until it carries a metric and a short note on where it failed. A finished imperfect
artifact beats a perfect plan, and the habit is the part an employer can actually see.</p></div>
</div>
</section>

<section id="case">
<div class="wrap">
<div class="k mono">One continuous case study</div>
<h2>One company's data carries all 24 weeks</h2>
<p class="sub">You are the AI engineering team at ZoroLogistics, a fictional freight operator
with shipments, carriers, lanes, support tickets, and policy documents. The data is generated
from seeded code in the repository: no API key, no network, the same rows on every machine.</p>
<p class="sub">Freight is the classroom because it is regulated, traceable, and full of messy
operational text. The same skills move to aviation, manufacturing, pharma, and finance.</p>
{figs["lab-case"]}
</div>
</section>

<section id="framework">
<div class="wrap">
<div class="k mono">The framework</div>
<h2>Four skills, three loops, one systems spine</h2>
<p class="sub">The curriculum implements Andrew Ng's AI Engineering Skills Map. Zorost adds the
part the map leaves out: skills do not ship, systems do. The Skills Map is Ng's synthesis,
published in The Batch in 2026, and this program is an independent implementation that is not
affiliated with or endorsed by Andrew Ng or DeepLearning.AI.</p>
{figs["lab-framework"]}
{figs["lab-stack"]}
</div>
</section>

<section id="start">
<div class="wrap">
<div class="k mono">Start</div>
<h2>Four commands and a first week</h2>
<p class="sub">You need a computer you can install software on, about ten hours a week, and
basic computer literacy. You do not need prior Python, a GPU, or a paid API key for the
required path.</p>
<pre><code><span class="c"># clone, install, and open the first week</span>
git clone {REPO}.git
cd AI-Engineering-Lab
python -m pip install -r requirements.txt
open curriculum/week-01/README.md</code><button class="copy mono" type="button"
data-clip="git clone {REPO}.git
cd AI-Engineering-Lab
python -m pip install -r requirements.txt">Copy</button></pre>
<ol class="steps">
<li><h4>Read the orientation</h4><p>Open <a href="{BLOB}/START-HERE.md">START-HERE.md</a> if you
are new to programming or to AI. It names the tools, the order, and what to do when something
breaks.</p></li>
<li><h4>Set up your machine in Week 1</h4><p><a href="{TREE}/curriculum/week-01">curriculum/week-01</a>
installs the environment and generates the dataset every later week reuses. No GPU needed for
the first eight weeks.</p></li>
<li><h4>Open the tracker</h4><p>The 24 week Excel workbook in
<a href="{TREE}/curriculum/tracking">curriculum/tracking</a> holds one row per week and a
progress dashboard.</p></li>
<li><h4>Ship Friday's use case</h4><p>Then take the quiz, tick the tracker, and start the next
week. Twenty four times.</p></li>
</ol>
{figs["lab-map"]}
</div>
</section>

<section id="questions">
<div class="wrap">
<div class="k mono">Common questions</div>
<h2>Before you clone it</h2>
<div class="g2">
<div class="card"><h4>What does it cost?</h4><p>Nothing. The repository is MIT licensed and
there is no signup. Weeks 1 to 13 have a free path using local models or free tiers, and the
cloud weeks tell you how to stay inside the free tiers.</p></div>
<div class="card"><h4>Do I need a GPU?</h4><p>Not until Week 8, and even then the local model
work has a hosted alternative. The first eight weeks run on an ordinary laptop.</p></div>
<div class="card"><h4>I already know Python and machine learning.</h4><p>Test out of Phase 1 by
shipping its four Friday use cases, then start at Week 5. The case study is cumulative, so
skipping a later phase means backfilling it.</p></div>
<div class="card"><h4>What happens when I fall behind?</h4><p>Nothing. It is self paced and
there is no cohort to miss. Pick up at the week you stopped, because the tracker and the
dataset are both still there.</p></div>
<div class="card"><h4>Is there a certificate?</h4><p>No. What you finish with is a portfolio of
interconnected artifacts: a fine tuned model, an eval harness, a multi agent system, three
cloud deployments, and a governed lakehouse capstone.</p></div>
<div class="card"><h4>How do I ask a question?</h4><p>Open an issue on the repository with the
week number, what you ran, and the traceback. For anything else, write
<a href="mailto:info@zorost.com">info@zorost.com</a>.</p></div>
</div>
</div>
</section>

</main>

<footer>
<div class="wrap">
<div class="top">
<div><div class="brand mono">ZOROST INTELLIGENCE</div><div class="dom mono">zorost.com</div></div>
<nav>
<a href="{REPO}">Repository</a>
<a href="{SITE}/ai-engineering-lab">Program page</a>
<a href="{SITE}/ai-lab">Zorost AI Lab</a>
<a href="{SITE}/ai-lab/fieldwork">AI Fieldwork</a>
<a href="{BLOB}/reference/GLOSSARY.md">Glossary</a>
<a href="mailto:info@zorost.com">info@zorost.com</a>
</nav>
</div>
<div class="rule"></div>
<div class="fine">
<span>Developed by Zorost Intelligence AI Lab, Washington, DC.</span>
<span>MIT licensed. Learn freely, build freely.</span>
<span>&copy; 2026 Zorost Intelligence LLC</span>
</div>
</div>
</footer>

<script>
document.querySelectorAll(".filters .chip").forEach(function (b) {{
  b.addEventListener("click", function () {{
    var f = b.dataset.f;
    document.querySelectorAll(".filters .chip").forEach(function (o) {{
      o.setAttribute("aria-pressed", String(o === b));
    }});
    document.querySelectorAll(".phase").forEach(function (p) {{
      p.hidden = f !== "all" && p.dataset.phase !== f;
    }});
  }});
}});
document.querySelectorAll(".copy").forEach(function (b) {{
  b.addEventListener("click", function () {{
    navigator.clipboard.writeText(b.dataset.clip).then(function () {{
      var t = b.textContent;
      b.textContent = "Copied";
      setTimeout(function () {{ b.textContent = t; }}, 1600);
    }});
  }});
}});
</script>
</body>
</html>
"""


def main() -> int:
    m = json.loads((ROOT / "curriculum" / "manifest.json").read_text())
    check = "--check" in sys.argv
    sizes = {} if check else convert_diagrams()
    if check:
        from PIL import Image

        for p in sorted(IMG.glob("lab-*.webp")):
            im = Image.open(p)
            sizes[p.stem] = (im.width // 2, im.height // 2)
    out = DOCS / "index.html"
    new = render(m, sizes)
    if check:
        if not out.exists() or out.read_text() != new:
            print("docs/index.html is out of date. Run: python scripts/build_site.py")
            return 1
        print("docs/index.html is up to date.")
        return 0
    DOCS.mkdir(exist_ok=True)
    (DOCS / ".nojekyll").touch()
    out.write_text(new)
    weeks = sum(len(p["items"]) for p in m["phases"])
    print(f"wrote {out.relative_to(ROOT)}: {len(m['phases'])} phases, {weeks} weeks, "
          f"{len(sizes)} figures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
