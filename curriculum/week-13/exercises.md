# Week 13: Exercises & Checklist

## Graded exercises

1. **Easy**: Run `notebooks/01-loop-log-and-eval-gates.ipynb` end-to-end. It prints a
   verifier pass rate at the end (a number from 0 to 1). Record that number in the Week 13
   sheet of the Excel tracker. If any unit check fails, fix the classifier and re-run,
   the goal is a passing verifier, not a screenshot of a red cell.

2. **Standard**: Add one more unit check (for the `billing` category) and one more
   edge-case eval row (e.g. a ticket with two shipment ids). Re-run the verifier and record
   the before/after pass rate in the loop log. Write one sentence explaining which layer,
   the binary unit check or the statistical eval, caught more defects, and why.

3. **Stretch**: Run a *real* headless agent loop. If `claude` is installed, use
   `claude -p '…'` against the notebook as shown in the agentic-loop cell; otherwise use
   your harness's equivalent headless mode. Capture the output, then log the actual tokens
   and any defect it produced. Note the difference between the seeded example rows and real
   data.

4. **Portfolio**: Commit the Support Bot MVP, the loop log (all three loops), and the
   spec-v1-vs-v2 diff to your fork. Add a short retrospective: what you believed at the
   start, what the developer and external loops corrected, and how you knew. This is the
   artifact that proves you can run a measured loop, not just steer one harness.

## Hints

1. **Easy**: The pass rate is the number the final cell prints; if any unit check is red,
   fix the keyword list *first*, the goal is a passing verifier, not a screenshot of a red
   cell.
2. **Standard**: The billing category keywords are in `CATEGORY_KEYWORDS`; write an assertion
   whose expected category matches a ticket that contains a billing keyword, and note which
   layer (unit vs eval) actually catches your new edge case.
3. **Stretch**: `claude -p` (or your harness's headless mode) is the same agent, scripted;
   capture stdout, then compare the real token count and defects against the seeded example
   rows in §4.
4. **Portfolio**: The retrospective needs three parts: the belief you started with, what each
   loop corrected, and the evidence (the pass-rate before/after) that told you it changed.

## Checklist (mirrors manifest.json + Excel tracker)

- [ ] Mon: Study the three loops and verifier patterns (knowledge-base 01).
- [ ] Tue: Spec the support bot MVP; define the verifier (eval suite + unit tests).
- [ ] Wed: Agentic loop session: build → test → fix until the verifier passes; log the loop.
- [ ] Thu: Developer loop: review with fresh eyes, update the spec, add missed edge cases.
- [ ] Fri: Use case: external loop, have someone real use the bot; file issues; update spec + evals.
- [ ] Sat: Take the Week 13 quiz (quiz.md), pass with 8/10; record the score in Notes.
- [ ] Milestone: Update the Excel tracker; commit the MVP and loop log.
