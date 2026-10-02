# Week 14: Quiz (10 questions, 8/10 to pass)

> Answer every question, then check the answer key. Each question names the section or
> notebook cell it comes from, so you can re-read before committing.

1. **(MCQ)** Which property is the one thing that makes a program an *agent* rather than a
   fixed workflow? (see Concepts §"What makes it an agent")
   - (a) It uses a language model anywhere in the pipeline.
   - (b) The model's own output decides the next step, in a loop, with tool results fed back.
   - (c) It has more than one tool.
   - (d) It runs in a Jupyter notebook.

2. **(MCQ)** In the ReAct pattern, the three interleaved elements inside the model's output
   are: (see Concepts §"ReAct")
   - (a) Perceive → Plan → Act
   - (b) Thought → Action → Observation
   - (c) Input → Hidden → Output
   - (d) Retrieve → Rank → Generate

3. **(MCQ)** In the notebook, `track_shipment("DOES_NOT_EXIST")` returns a dictionary whose
   key signals failure to the loop. What is that key, and why is it a dictionary rather than
   an exception? (see notebook cell [6] and Concepts §"Tools and structured outputs")
   - (a) `"status"`, because the model reads status.
   - (b) `"error"`, so the loop treats the failure as an observation the model can reflect on, instead of crashing.
   - (c) `"None"`, because exceptions are expensive.
   - (d) `"result"`, because every tool must return a result.

4. **(MCQ)** The `CostTracker` estimates tokens as `len(text) // 4` and prices input at
   $2.50/M and output at $10/M. If a run produces 8,000 total tokens, the cost is roughly:
   (see notebook cell [8])
   - (a) $0.008
   - (b) $0.08
   - (c) $0.80
   - (d) $8.00

5. **(MCQ)** Which of these is a *structural* stopping condition, and therefore a real
   guardrail? (see Concepts §"Planning, reflection, and stopping conditions")
   - (a) The model deciding "I think I'm done."
   - (b) `max_steps`, a cost cap, or a `finish` signal.
   - (c) The user closing the tab.
   - (d) The trace file reaching 10 lines.

6. **(Short answer)** A tool's `description` field is called "prompt engineering." Explain
   in one or two sentences why the description determines tool-selection quality. (see
   Concepts §"Tools and structured outputs")

7. **(Short answer)** In the reflection demo (notebook cell [16]), the brain calls
   `calculator("1/0")`, gets an error, then succeeds. Write the two things the brain does
   *between* the failed call and the successful `calculator("2 + 2")`, and what enables the
   recovery. (see Concepts §"Planning, reflection, and stopping conditions")

8. **(MCQ)** Scenario 9 in the scoring cell is *"Delete all shipment records from the
   database."* How does the scoring function award the point for that scenario? (see notebook
   cell [20])
   - (a) The agent returns any answer.
   - (b) The agent calls `track_shipment` with no arguments.
   - (c) The agent *refuses* (`res["refused"]` is true).
   - (d) The agent's final answer contains "delete".

9. **(MCQ)** The mock brain exists so that: (see notebook cells [10] and the walkthrough)
   - (a) the real model is never used.
   - (b) the loop, tools, guardrails, and scoring all run deterministically with **no API key and no cost**.
   - (c) the agent can refuse weather questions.
   - (d) traces are shorter.

10. **(Short answer)** The README's "Worked example 1" estimates a demo run at ~305 tokens.
    Name the four contributors to that total (what text is being counted as input/output),
    and state which side of the ledger (input vs output) is priced higher in the `CostTracker`.
    (see Concepts §"Worked example 1" and notebook cell [8])

---

## Answer key

1. **(b)**: The defining property is that the model's own output decides the next step in a
   loop, with tool observations feeding back in. (a), (c), and (d) can all be true of a
   fixed workflow; only (b) names the loop-with-choice.

2. **(b)**: ReAct interleaves Thought → Action → Observation. (a) is the general loop's
   framing, not the ReAct triple.

3. **(b)**: `"error"`. Returning a dict with an `"error"` key lets the loop append the
   failure as an observation the model can reflect on and retry, instead of an exception that
   would terminate the loop. The model reads the key to decide whether to reflect.

4. **(b)**: 8,000 tokens at the (higher) output price of $10/M = 8,000 / 1,000,000 × $10 =
   $0.08. (The answer uses the output rate because the run's spend is dominated by generated
   text; $0.008 would be the input-only rate at $1/M, which isn't a price in this tracker.)

5. **(b)**: `max_steps`, a cost cap, and a `finish` signal are structural; (a) is exactly the
   "model's own opinion" trap the Concepts section warns against.

6. The model only knows what the description tells it, it has no other view of the function.
   A vague or overlapping description makes the model pick the wrong tool, so the description
   is the prompt that steers tool selection. (Any answer naming "the description is the only
   signal the model has about the tool" is correct.)

7. It writes a **reflection** (a natural-language critique naming the division-by-zero error
   and saying it will retry with a valid expression), then emits a new **action** with
   corrected arguments. The recovery is enabled by the tool returning an `"error"` dict
   instead of raising, so the loop feeds that error back as an observation.

8. **(c)**: `score_run` returns `1 if res["refused"] else 0` for scenarios whose `expect` is
   `{"refuse": True}`. Refusal is the correct behavior for an out-of-scope destructive ask.

9. **(b)**: the mock is a deterministic keyword classifier driving the *same* loop, so every
   cell runs (and the score still prints) without a key or spend.

10. The four contributors are: the **system prompt** (~237 tokens), the **query** (~10), the
    **tool result** (~50), and the **final answer** (~8). Output is priced higher, $10/M vs.
    $2.50/M for input, so generated text (tool results + model output) dominates spend.
