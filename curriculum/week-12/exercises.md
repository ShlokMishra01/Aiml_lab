# Week 12: Exercises & Checklist

## Graded exercises

1. **Easy**: Run `notebooks/01-harness-setup-and-comparison.ipynb` to the final cell and
   record its harness-readiness score (0 to 3) in the Week 12 sheet of the Excel tracker. If
   it is below 2, install one more harness following its `reference/skills/` guide and re-run.

2. **Standard**: Copy the `SPEC.md` template from the notebook into
   `specs/eta-cli-SPEC.md`, fill in every bracket (including the one refused tradeoff),
   then drive your first harness to build the CLI from it. Run the six-point test plan and
   paste the pass/fail line into the tracker.

3. **Stretch**: Run the *same* `SPEC.md` through a second harness and fill every cell of
   the comparison worksheet in the notebook (plan, tokens, cost, quality). Write the
   one-page comparison: which harness produced the better plan, at what cost, and which one
   you would pick for a team, and why.

4. **Portfolio**: Commit the working `eta-cli` (tests green), the filled `SPEC.md`, and
   the 1-page harness comparison to your fork. Add a `README` note stating which harness
   built it, how many tokens/dollars it cost, and the one tradeoff you refused. This is the
   first "I steered an agent from spec to shipped tool" artifact of the program.

## Hints

1. **Easy**: The score is `shutil.which` over `claude`/`opencode`/`dsh`; a missing tool
   prints a graceful skip, so don't force an install just to make the number higher, install
   one you'll actually use this week.
2. **Standard**: Start from the refused-tradeoff line: state the one thing the CLI must
   *never* do (invent an ETA), then write the test-plan point that would catch it (unknown id
   → exit `2`).
3. **Stretch**: Use the *identical* `SPEC.md` for harness B; the only thing you change is
   the harness. Fill all six worksheet columns, a comparison with blanks is a vibe.
4. **Portfolio**: The `README` note needs three facts: which harness, how many tokens/dollars,
   and the one tradeoff you refused. Those three are the whole "steered an agent" story.

## Checklist (mirrors manifest.json + Excel tracker)

- [ ] Mon: Install and authenticate 2 harnesses (Claude Code + OpenCode or DSH); read the skill guides.
- [ ] Tue: Write SPEC.md for the ETA CLI: user, constraints, one refused tradeoff, test plan.
- [ ] Wed: Drive the agent to build the CLI; run the tests; iterate until green.
- [ ] Thu: Repeat the same task in a second harness; compare plans, cost, and code quality.
- [ ] Fri: Use case: ship the CLI; write the 1-page harness comparison for your team.
- [ ] Sat: Take the Week 12 quiz (quiz.md), pass with 8/10; record the score in Notes.
- [ ] Milestone: Update the Excel tracker; commit the CLI and comparison.
