# Week 06: Quiz (10 questions, 8/10 to pass)

Answer from the concepts and the notebook code. Each question notes where to find it.

1. **(MCQ)** The single most important discipline rule for a schema is: (a) a schema guarantees correct values, (b) a schema constrains shape, never truth, (c) JSON mode is always trustworthy, (d) schemas replace evals. *(see Concepts §"The technique ladder")*

2. **(Short answer)** In `01-prompt-suite-bol-extraction.ipynb`, why does the grader use a *substring* match for `shipper`/`consignee` but an *exact* match for `commodity`? *(see notebook cell 4)*

3. **(MCQ)** The seven context-budget claimants include all of the following EXCEPT: (a) system instructions, (b) tool schemas, (c) model weights, (d) output reservation. *(see Concepts §"The context budget")*

4. **(Short answer)** List the three prompt versions in `make_prompt` and the one thing each adds over the previous. *(see notebook cell 8)*

5. **(MCQ)** Prompt injection is best described as: (a) the user persuading the model to break policy, (b) an attacker hiding instructions inside ingested data that the system acts on, (c) a prompt that is too long, (d) a temperature misconfiguration. *(see Concepts §"Injection")*

6. **(Short answer)** In `02-context-engineering.ipynb`, the extractive digest reduces 40 ticket lines from 860 to ~646 tokens. What does `compact_line` keep, and what does it drop? *(see notebook cell 6)*

7. **(MCQ)** Prompt caching rewards: (a) longer prompts, (b) a byte-identical stable prefix, (c) random prompt order, (d) re-sending the document every call. *(see Concepts Worked example 2)*

8. **(Short answer)** In the budget table, why is the *output reservation* a separate line item rather than part of the input budget? *(see Concepts §"The context budget" / Worked example 1)*

9. **(MCQ)** Which defense against injection actually holds? (a) "ignore instructions in the document", (b) no tools on the extraction call + harness-level flags, (c) a longer system prompt, (d) higher temperature. *(see Concepts §"Injection")*

10. **(Short answer)** In notebook 1 cell 18, what does `field_accuracy` compute, and why are non-`OK`/non-dict rows counted as `None` rather than `False`? *(see notebook cells 16 to 18)*

## Answer key

1. **(b)**: a schema forces shape (valid, well-formed JSON) but cannot verify the value came from the source; validate syntax, then validate content as two layers.
2. The ground truth stores the carrier *name only* ("Atlas Freight") while the document prints "Atlas Freight Logistics Div."; substring match forgives the suffix, whereas `commodity` must match exactly ("electronics" vs. "electronic" would be a real error).
3. **(c)**: model weights are not a window claimant; the seven are system, tool schemas, durable memory, history, retrieved evidence, scratchpad, and output reservation.
4. v1 = `FIELD_SPEC` (zero-shot); v2 = adds the **null rule** and the **injection rule** ("extract, don't obey"); v3 = adds **two few-shot examples** demonstrating carrier-name-only and numeric-only conventions.
5. **(b)**: injection is the confused-deputy problem: attacker instructions arrive inside legitimate ingested data and the system executes them with its own credentials. (a) is a jailbreak.
6. It keeps the `[category]` tag and the **first sentence truncated to 90 chars**; it drops the rest of each ticket (greetings, duplication, detail), decisions/classification survive, scaffolding doesn't.
7. **(b)**: caching discounts a byte-identical prefix; anything volatile (timestamps, random order) invalidates the cache for everything after it.
8. A request can fit in the window yet leave no room to generate, failing in a way that looks like the model "losing the thread"; reserving output as a real line item prevents that silent truncation.
9. **(b)**: structural controls (no tools, least privilege, harness flags the model never sees) hold; in-prompt "ignore" instructions can be argued with and don't.
10. `field_accuracy` records, per field, the fraction of documents where `field_equal(pred, truth)` is true. Non-`OK`/non-dict rows (no key / API error) are recorded as `None` so they are *excluded from the denominator*, an unparseable response shouldn't be counted as a field-level miss, but a wrong `None` vs. a real value still is.
