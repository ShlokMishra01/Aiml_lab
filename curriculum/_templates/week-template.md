# Week Template: AI Engineering Lab (Rich Lesson Standard v2)

> This is the spec every week folder must meet. A week is a **lesson**, not a
> pointer: someone with a laptop and this folder alone should be able to study,
> build, and check off the whole week. Contributors must follow this standard
> ([.github/CONTRIBUTING.md](../../.github/CONTRIBUTING.md)).

```
week-NN/
├── README.md # THE lesson: 2,000 to 3,500 words, self-contained study guide
├── notebooks/ # 1 to 3 runnable Jupyter notebooks (see Notebook standards)
├── exercises.md     # graded exercises + hints + the week's checklist
└── quiz.md          # 10 questions with answer key (self-check)
```

## README.md: required sections, in order

1. **Title + header block**: `# Week NN: <Title>` and the "Part of Zorost AI
   Lab · Week NN of 24 · Section · Category" banner, plus the 🎯 use-case line.
2. **The problem** (150 to 300 words), the real-world ZoroLogistics scenario this
   week solves. Why it matters, what goes wrong without it, and a concrete
   before/after (e.g., "without a time-aware split, our model 'predicts' the
   future and looks brilliant until it ships").
3. **Objectives**: 4 measurable, Friday-shaped ("By Friday you can…").
4. **Day-by-day plan**: Mon to Fri table: what to study, what to run, what to ship
   each day, with time estimates.
5. **Concepts**: the heart of the lesson: **1,200 to 2,000 words** of original
   exposition covering every topic in the manifest for that week. Requirements:
   - at least **3 tables** (comparisons, sizing, decision rules)
   - at least **1 Mermaid diagram** (flow, architecture, or decision tree)
   - at least **2 worked examples** with concrete numbers from the ZoroLogistics
     data (e.g., a token budget, a metric calculation, a cost estimate)
   - inline links to the knowledge base for deeper dives (link, don't duplicate)
   - one **"How it breaks"** subsection (the failure modes this week's technique
     prevents or causes)
6. **Notebook walkthrough** (300 to 600 words), what each notebook does section by
   section, which cells to modify, what each final metric means, and what
   "correct" output looks like.
7. **The use case (Friday)**: the concrete deliverable, the Zorost gate
   ("a stranger can inspect it and you can show what it did"), and a stretch
   variant for fast learners.
8. **Common pitfalls**: 6 to 8 named failure modes with the fix for each, as a table.
9. **Glossary**: 8 to 12 terms defined in one sentence each.
10. **Self-check (quiz)**: link to `quiz.md` and the passing bar (8/10).
11. **Exercises**: the four graded exercises (easy/standard/stretch/portfolio)
    with a one-line pointer to `exercises.md` for hints.
12. **Sources**: 5 to 12 URLs: vendor docs, papers, and letters actually consulted.

## quiz.md standard

```markdown
# Week NN, Quiz (10 questions, 8/10 to pass)

<10 questions covering concepts AND notebook code; mix multiple-choice and
short-answer; each question ends with "(see Concepts §X or notebook cell Y)">

## Answer key
<1 to 2 sentence answer per question, with the reasoning>
```

## exercises.md standard

```markdown
# Week NN, Exercises & Checklist

## Graded exercises
1. **Easy**, …
2. **Standard**, …
3. **Stretch**, …
4. **Portfolio**, …

## Hints
<one hint per exercise, direction, never the full solution>

## Checklist (mirrors manifest.json + Excel tracker)
- [ ] Mon: …
- [ ] Tue: …
- [ ] Wed: …
- [ ] Thu: …
- [ ] Fri: …
- [ ] Sat: Take the quiz (8/10 to pass)
- [ ] Milestone: …
```

## Notebook standards (unchanged from v1)

1. First markdown cell = title + `# Requirements: pip install …` + `⚠️ REQUIRES`
   banner where applicable.
2. `zoro` import cell: `import sys, pathlib; sys.path.insert(0, str(pathlib.Path.cwd().parents[1]))`.
3. Deterministic seeds everywhere; final code cell prints a NUMBER.
4. Markdown narration between sections (why before how).
5. nbformat 4.5; code cells `"outputs": [], "execution_count": null`; Python 3.12
   kernelspec; every cell's `source` is a list of lines **ending in `\n`**.
6. API keys via `os.environ` with graceful skip messages; cost warnings before
   paid calls.
