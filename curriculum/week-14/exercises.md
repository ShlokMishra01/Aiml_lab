# Week 14: Exercises & Checklist

## Graded exercises

1. **Easy**: Run `notebooks/01-react-agent-from-scratch.ipynb` end-to-end with the mock
   brain (no API key needed). It prints a scenario score at the end (a number from 0 to 10).
   Record that number in the Week 14 sheet of the Excel tracker.

2. **Standard**: Add a fifth tool, `list_carriers` (returns carrier name, region,
   on-time rate, and fleet size from `zoro.data`), with a proper JSON schema. Register it
   in the tool registry, then add one new scenario that requires it and confirm the trace
   shows the tool being called with the right (no) arguments.

3. **Stretch**: Set `OPENAI_API_KEY` (or `OPENROUTER_API_KEY`), re-run the 10 scenarios
   with the real model, and compare the score against the mock. Open the saved trace and
   find **one** scenario where the real model and the mock disagree; write a markdown cell
   explaining *why* (tool choice, argument format, or refusal behavior).

4. **Portfolio**: Commit the agent, the trace log, and a short `README` block stating:
   the 10 scenarios, the final score, and the exact guardrail thresholds (max steps, cost
   cap, refusal policy). This is the first inspectable agent artifact of the program
   (tracked in [`curriculum/projects/README.md`](../projects/README.md)).

## Hints

1. **Easy**: Run every cell top to bottom; the mock brain needs no key, and the final cell
   prints `FINAL_SCORE` as a fraction between 0 and 1. Record exactly that number.
2. **Standard**: Mirror an existing tool's three-part shape (function, `name`/`description`,
   and `parameters` schema) in the `TOOLS` registry; `list_carriers` takes **no** arguments,
   so its `required` is `[]`. Add a scenario whose `expect` names `list_carriers`.
3. **Stretch**: Diff the real run's trace against the mock's for the *same* scenario ID; look
   for a different `tool`, a different `args` value, or a `refuse` where the mock acted.
4. **Portfolio**: A reviewer reads the `README` block cold, so state the 10 scenarios, the
   score, and the three thresholds (`max_steps`, `cost_cap`, refusal policy) as concrete
   numbers, not adjectives.

## Checklist (mirrors manifest.json + Excel tracker)

- [ ] Mon: Study the agent loop and ReAct (reference/knowledge-base/10-agents-multiagent.md).
- [ ] Tue: Implement the tool-calling loop by hand; wire 2 tools (track shipment, convert units).
- [ ] Wed: Add planning and reflection; log every step, the trace is your debugger.
- [ ] Thu: Add guardrails: refusal, max steps, cost cap; test adversarial inputs.
- [ ] Fri: Use case: the agent solves 10 unseen scenarios; publish the trace log.
- [ ] Sat: Take the Week 14 quiz (quiz.md), pass with 8/10; record the score in Notes.
- [ ] Milestone: Update the Excel tracker; commit the agent and traces.
