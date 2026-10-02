# Week 06: Exercises & Checklist

## Graded exercises

1. **Easy**: Re-run `01-prompt-suite-bol-extraction.ipynb` with a different model (set `OPENAI_MODEL` or `OPENROUTER_MODEL`) and report the version-3 score delta.
2. **Standard**: Add a 4th prompt version with chain-of-thought ("think step by step about the cargo block first"). Compare its accuracy and token cost against version 3.
3. **Stretch**: In `02-context-engineering.ipynb`, add a *tiered* eviction policy: label each budget claimant as pinned / compressible / disposable, then re-run the worksheet with a 3× longer document and show what gets cut first.
4. **Portfolio**: Save the prompt suite as `projects/bol_extractor.py` with a JSON eval log (version → score → note) and a gate that fails below 90% per-field accuracy.

## Hints

1. **Easy**: Set `OPENAI_MODEL` (or `OPENROUTER_MODEL`) before running; re-run only version 3 and diff its `OVERALL` row against the default model's score.
2. **Standard**: Add a `version == 4` branch to `make_prompt` that prepends a "reason about the cargo block first" line; compare its accuracy *and* its token cost (the CoT text is extra input tokens).
3. **Stretch**: Give each worksheet claimant a tier label (`pinned`/`compressible`/`disposable`) and, when the document triples, evict in that order before re-measuring the total against the ceiling.
4. **Portfolio**: Wrap the three `make_prompt` versions and the grader in a function, dump `{version: score}` to JSON, and `sys.exit(1)` when the best score < 0.90.

## Checklist (mirrors manifest.json + Excel tracker)

- [ ] Mon: Study prompt engineering and context engineering (knowledge-base 04).
- [ ] Tue: Build the BoL extraction prompt suite; run it against 20 synthetic documents.
- [ ] Wed: Add structured outputs and few-shot examples; improve per-field accuracy.
- [ ] Thu: Context engineering: budgets, compaction, caching, measure tokens and latency.
- [ ] Fri: Use case: reach 90%+ field accuracy on the eval set; document the failure cases.
- [ ] Sat: Take the Week 6 quiz (quiz.md), pass with 8/10; record the score in Notes.
- [ ] Milestone: Update the Excel tracker; commit the prompt suite and eval results.
