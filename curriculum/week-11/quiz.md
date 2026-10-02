# Week 11: Quiz (10 questions, 8/10 to pass)

Answer on your own first, then check the answer key. Each question notes where the
answer lives, so you can re-read the exact section or cell you missed.

## Questions

1. **(MCQ)** Ng's claim about evals + error analysis is a claim about *what*, exactly? (see Concepts intro + the KB's "Why this file matters")
   - A) Being more ethical
   - B) Velocity, teams that can measure failure ship faster
   - C) Reducing GPU cost
   - D) Replacing code review

2. **(MCQ)** Why does the knowledge base insist golden sets be drawn from *real* inputs rather than invented ones? (see Concepts §"Golden sets")
   - A) Real inputs are easier to generate
   - B) Invented cases encode your beliefs; real cases encode the problem
   - C) Real inputs need no labels
   - D) Invented cases are always too short

3. **(MCQ)** Which metric family fits "generation with a correct-but-variable answer"? (see Concepts §task-metric table)
   - A) Accuracy
   - B) Recall@k
   - C) LLM-as-judge with a rubric
   - D) Schema conformance only

4. **(Short answer)** In `notebooks/01-zoroeval-harness.ipynb`, what does the groundedness rubric's level "3" catch, and why is the rubric anchored this way? (see notebook cell 12 + Concepts §"LLM-as-judge")

5. **(MCQ)** A judge returns the same score on 9 of 10 doubled samples, but on one grounded answer (human label 5) it returns 1. What do these two facts tell you? (see Concepts §Worked example 1)
   - A) The judge is perfect
   - B) Self-agreement is high but the judge still misses that dimension, recalibrate or fall back to human review
   - C) The rubric is too vague to use
   - D) Calibration is irrelevant

6. **(MCQ)** In the workshop notebook, what does HLP classify as "upstream" rather than "fixable"? (see notebook cell 10)
   - A) Any failure a human would also make, given the same information
   - B) Any failure on ticket triage
   - C) Failures that happen more than 5 times
   - D) Failures with a `trace_id`

7. **(Short answer)** In the seed-42 run log, clustering the 34 wrong traces gives `field_date_format` (8) and `hallucinated_rate` (8) tied at the top. What is the top fixable class's coverage, and why do we fix the *largest* class first? (see Concepts §Worked example 2)

8. **(MCQ)** In `notebooks/02-error-analysis-workshop.ipynb`, `ci_gate(score, threshold)` returns `False` when the extraction score is 0.88 and the threshold is 0.90. What is the point of a gate that can say "no"? (see notebook cell 15 + Concepts §"evals in CI")
   - A) It makes the pipeline run faster
   - B) A number nobody is willing to block on is a number nobody trusts
   - C) It guarantees the model is never deployed
   - D) It replaces the eval set

9. **(MCQ)** Which is a **code metric** (not a model metric)? (see Concepts §code vs model table)
   - A) "Is the answer grounded in the passage?"
   - B) "Was the ticket routed to the right queue?"
   - C) "Did the endpoint return valid JSON in under 2 seconds?"
   - D) "Does the summary capture every claim?"

10. **(Short answer)** List the five steps of the error-analysis loop, and state *why* the fifth step (add the failure class back to the eval set) is the one that makes the loop a ratchet. (see Concepts §"The error-analysis loop")

## Answer key

1. **B)** Ng's claim is about *velocity*: measuring failure lets a team ship faster, because every change either moves a number or it does not. It is not a soft claim about being "data-driven."

2. **B)** Invented cases encode your *beliefs* about the problem; real cases encode the problem itself. One real customer ticket can be worth ten invented ones.

3. **C)** When the answer can be phrased many ways, string matching fails, so you grade with an LLM-as-judge and a rubric (often paired with a similarity score).

4. **Level 3 catches "the core answer is supported, but it includes at least one claim (a number, date, or policy detail) not present in the passage."** The rubric is anchored, each level names a concrete failure, so a "3 vs 1" is defensible and worth investigating instead of shrugging off.

5. **B)** Self-agreement 0.90 means the rubric is stable, but stability is not correctness: a systematic miss (human 5 → judge 1) means the judge is unreliable on that dimension, so you recalibrate or fall back to human review. A judge you have not calibrated is a second unverified model.

6. **A)** Upstream = even a competent human, given the same information, would fail, so the fix is the data/intake, not the model (e.g., a schema contract both model and human need).

7. **Coverage ≈ 8 / 34 ≈ 24%** of the wrong traces. We fix the largest class first because **frequency matters more than cleverness**, the biggest class is the one change worth making this week, and it is the class you add back to the eval set.

8. **B)** The gate's authority comes from being willing to block: a number nobody is willing to block on is a number nobody will trust. Here the extraction score failing its bar blocks the release.

9. **C)** A code metric measures the deterministic plumbing (schema/parse/latency), runs fast and cheap on every commit. The other three measure the model's probabilistic output.

10. **Read traces → cluster failures → prioritize by frequency → fix → add the failure back to the eval set.** Step five is the ratchet: putting the failing cases (and the fix's behavior) into the eval set ensures that class can never silently regress, turning error analysis from a one-off into a permanent improvement loop.
