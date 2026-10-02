# Week 13: Quiz (10 questions, 8/10 to pass)

Answer from memory first, then check the key. Each question names the section or cell it
tests, so a miss tells you exactly what to re-read.

## Questions

1. **(MCQ)** Which loop runs on a minutes-scale cadence and closes against the verifier?
   (see Concepts, "The three loops")
   - A) External feedback
   - B) Developer feedback
   - C) Agentic coding
   - D) The configuration-management loop

2. **(MCQ)** The unit checks and the mini eval are two *different* verifier layers because…
   (see Concepts, "The verifier has layers")
   - A) unit tests are statistical and evals are binary
   - B) the eval measures accuracy as a rate over many examples and catches whole classes the hand-written checks missed
   - C) evals are cheaper to run than unit tests
   - D) unit tests replace the need for an eval

3. **(Short answer)** Write the exact formula the notebook's final cell uses to compute the
   verifier pass rate. (see notebook cell §7)

4. **(MCQ)** In spec-driven development, when feedback finds a gap, the fix goes… (see
   Concepts, "SPEC.md patterns")
   - A) into the code first, then the spec if there's time
   - B) into the spec first, then the code, then the test/eval case
   - C) into a chat message to the agent, then lost
   - D) only into the eval set

5. **(Short answer)** Name all six categories the Support Bot classifier distinguishes. (see
   notebook cell §1)

6. **(MCQ)** A blast-radius rule calibrates autonomy per action. Which action needs the
   tightest leash? (see Concepts, "Blast-radius rules")
   - A) reading a scratch file
   - B) editing the repo on a branch
   - C) writing production data
   - D) running the unit tests

7. **(Short answer)** What does `classify_ticket('hello')` return, and why? (see notebook
   cell §1 and the `_check_unknown` unit check)

8. **(MCQ)** A `PreToolUse` hook exists to… (see Concepts, "Harness primitives")
   - A) summarize the diff after editing
   - B) enforce or block a policy *before* a tool runs (e.g. refuse `data/raw/` writes)
   - C) load a skill on demand
   - D) spawn a subagent

9. **(Short answer, with numbers)** Three agentic cycles total 12,000 input tokens and 3,000
   output tokens at $3.00/1M input and $15.00/1M output. Show the arithmetic and give the
   total cost in dollars. (see Concepts, "Worked example 1")

10. **(MCQ)** The right way to convert an external-loop bug report into lasting change is…
    (see Concepts, "Worked example 2")
    - A) fix the code and move on
    - B) file it, then add a spec line and a new eval case so it cannot silently regress
    - C) ask the user to stop using that input
    - D) log it in the loop log and do nothing else

## Answer key

1. **C.** Agentic coding runs in minutes: write → test → read the failure → fix, until the
   verifier passes. Developer feedback is tens of minutes to hours; external feedback is
   hours to weeks.

2. **B.** The 6 unit checks are binary and hand-written; the 60-ticket eval reports accuracy
   as a rate and can surface a whole class (e.g. customs) the hand-written checks never named.

3. **`verifier_pass_rate = (unit_passed + eval_correct) / (unit_total + eval_total)`**, printed
   as `round(verifier_pass_rate, 3)`, i.e. `(unit checks passed + eval correct) / (unit
   checks + eval cases)`.

4. **B.** Spec first, then code, then the test/eval case, that ordering keeps the loops from
   drifting; the spec is the source of truth, the code its current implementation.

5. **tracking, damage, refund, documents, customs, billing** (plus a fallback `'unknown'` when
   no keyword matches).

6. **C.** Writing production data causes real customer harm and is hard to undo, it needs
   manual approval. Reading a scratch file is nearly free to get wrong.

7. **`'unknown'`.** `'hello'` matches no keyword, so every category scores 0; `classify_ticket`
   returns the best category only when its score is `> 0`, otherwise `'unknown'`.

8. **B.** A `PreToolUse` hook runs before a tool call and can block it, turning "please
   remember not to touch X" into something the harness enforces.

9. **$0.081.** Input: 12,000 × $3.00 / 1,000,000 = $0.036. Output: 3,000 × $15.00 / 1,000,000
   = $0.045. Total = $0.036 + $0.045 = $0.081.

10. **B.** File it, then decide spec-vs-eval and add the failing input to the eval set, that
    is the triage rule that makes feedback permanent rather than a one-off fix.
