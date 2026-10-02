# Week 10: Quiz (10 questions, 8/10 to pass)

Answer on your own first, then check the answer key. Each question notes where the
answer lives, so you can re-read the exact section or cell you missed.

## Questions

1. **(MCQ)** What is Ng's selection order, and where does fine-tuning sit? (see Concepts §"the last lever")
   - A) Fine-tune → RAG → prompt → agentic
   - B) Prompt (with eval) → RAG → agentic → fine-tune last
   - C) RAG → fine-tune → prompt → agentic
   - D) Fine-tune first, because weights always beat context

2. **(MCQ)** For a LoRA module of shape `(in=1536, out=1536)` with rank `r=16`, how many trainable parameters does LoRA add to that one module? (see Concepts §Worked example 1)
   - A) 1536
   - B) 49,152
   - C) 700,416
   - D) 1.54 billion

3. **(Short answer)** In the LoRA worked example, the total trainable parameters come to ~0.70M of ~1.54B, about 0.05%. Why does that tiny fraction matter for the budget? (see Concepts §Worked example 1)

4. **(MCQ)** In `notebooks/01-sft-dataset-and-lora-training.ipynb`, what is the assistant turn of each extraction example? (see notebook cell 6)
   - A) A one-word category
   - B) The ground-truth JSON of `bol["fields"]`
   - C) An empty string
   - D) The system prompt

5. **(Short answer)** Why does the knowledge base say "a few hundred clean, diverse, on-task examples beat tens of thousands of noisy ones"? (see Concepts §"SFT: imitation learning")

6. **(MCQ)** What distinguishes DPO from classic RLHF? (see Concepts §"SFT → DPO → RLVR")
   - A) DPO needs a separately trained reward model
   - B) DPO folds the preference signal directly into a supervised objective on `(prompt, chosen, rejected)` pairs
   - C) DPO requires a verifiable reward like a unit test
   - D) DPO freezes the entire model and trains nothing

7. **(MCQ)** In `notebooks/02-dpo-and-before-after-evals.ipynb`, what is the "forgetting check"? (see notebook cell 6)
   - A) A held-out set of 5 generic questions the model should already know, graded before and after
   - B) A test that the adapter still fits in VRAM
   - C) A check that the loss curve decreased
   - D) A comparison of two different base models

8. **(Short answer)** Compute the net gain: before = {extraction 0.60, triage 0.72, generic 0.95}; after = {extraction 0.88, triage 0.91, generic 0.93}. What is `net = extraction_delta + triage_delta − forgetting_cost`, and does it deploy? (see Concepts §Worked example 2)

9. **(MCQ)** Your fine-tune raises the new-task eval but drops the generic check from 0.95 to 0.80. What is the correct action per the "How it breaks" section? (see Concepts §"How it breaks")
   - A) Ship it, the specialist gain is what matters
   - B) Don't deploy; reduce rank/alpha or add a fraction of general data back
   - C) Add more epochs
   - D) Ignore the generic check

10. **(MCQ)** Why must facts that change (e.g., last quarter's prices) *not* be stored in weights? (see Concepts §"When fine-tuning pays")
    - A) Weights cannot hold numbers
    - B) Retrieved knowledge is wrong for volatile facts, retrieve, don't memorize
    - C) Fine-tuning always deletes old facts
    - D) Facts are too small to matter

## Answer key

1. **B)** The order is managed-API prototype → prompt/context with an eval → RAG → agentic → fine-tune last. Fine-tuning is the final, most expensive, hardest-to-undo lever.

2. **B)** LoRA adds `r × (in + out) = 16 × (1536 + 1536) = 49,152` per module. That is one attention projection; the full `q/k/v/o` set is `4 × 49,152 = 196,608`.

3. **Because LoRA trains almost nothing, the adapter is a few MB and the fine-tune needs a fraction of full-training memory.** QLoRA puts the base in 4-bit, so a 1.5B (or 7 to 8B) run fits a free Colab T4 or a 16 GB laptop instead of a datacenter.

4. **B)** The assistant turn is `json.dumps(bol["fields"], sort_keys=True)`, the ground-truth structured fields the model learns to imitate (the label).

5. **A small model internalizes whatever pattern dominates the data.** If most examples are off-target or contradictory, that is exactly what you teach. Coverage of *behavior* (diversity, edge cases) matters more than row count.

6. **B)** DPO folds the preference signal directly into a supervised-style objective on `(prompt, chosen, rejected)` pairs, simpler and more stable than RLHF's reward model + PPO loop. (RLVR, not DPO, uses a verifiable reward.)

7. **A)** The forgetting check is the 5 generic questions (`GENERIC_QA`) graded before and after, it catches the adapter un-teaching general competence.

8. **net = (0.88−0.60) + (0.91−0.72) − (0.95−0.93) = 0.28 + 0.19 − 0.02 = +0.45.** Positive, so the specialist gains earned the tiny generic regression → deploy. (If the forgetting cost exceeded the gains, the answer would be don't deploy.)

9. **B)** A generic drop that large means catastrophic forgetting. Don't ship; lower the learning rate, add a small fraction of general data back, or reduce rank/alpha, never add epochs.

10. **B)** Weights are the wrong place for facts that change; the model would already be wrong next quarter. New knowledge is RAG's job, retrieve it, and use fine-tuning for *behavior* (style, format, vocabulary).
