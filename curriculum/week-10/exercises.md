# Week 10: Exercises & Checklist

## Graded exercises

1. **Easy**: Run `notebooks/01-sft-dataset-and-lora-training.ipynb` end-to-end. Record
   the dataset size (~300 examples) and the final training loss it prints at the end in
   the Week 10 sheet of the Excel tracker. If you have no GPU, run the dataset-building
   cells to completion (they are CPU-only) and record the dataset stats, noting the
   training cells were skipped.

2. **Standard**: Rebuild the SFT dataset with a *different* seed and ~50 extra
   hand-written examples of your own (write real instruction/response pairs for
   ZoroLogistics, not copies of the generated ones). Retrain the LoRA adapter, then
   show, with the before/after eval, that the adapter still beats the base model on
   the extraction eval, stating the exact delta.

3. **Stretch**: Swap plain LoRA for **DoRA** by setting `use_dora=True` in PEFT's
   `LoraConfig` (or switch to a 4-bit QLoRA base via bitsandbytes), keeping everything
   else fixed. Compare the before/after eval table against your plain-LoRA run and write
   one sentence on whether the extra mechanism was worth it *for your task*.

4. **Portfolio**: Commit the **LoRA fine-tuned triage + extraction model** milestone
   (tracked in [`curriculum/projects/README.md`](../projects/README.md)): the adapter config
   (`r`, `alpha`, target modules), the loss curve image, the before/after eval table,
   the catastrophic-forgetting check numbers, and your deploy/no-deploy decision with
   its justification.

## Hints

1. **Easy**: The dataset cells (2 to 10) are CPU-only; the training cells need a GPU. On
   no-GPU hardware, record the dataset stats and note the trainer skipped, the final
   `SFT_EXAMPLES` still prints.

2. **Standard**: Write *real* instruction/response pairs for ZoroLogistics (a new
   lane, a customs edge case, a damage claim), not copies of the generated ones. Re-run
   the eval on the *same* held-out set so the delta is comparable.

3. **Stretch**: `use_dora=True` is a one-line change in `LoraConfig`; keep `r`, alpha,
   targets, epochs, and data identical so the only variable is the mechanism. Compare
   the before/after table, not the loss curve.

4. **Portfolio**: The gate wants both columns of the table (new-task *and* generic)
   and an explicit deploy/no-deploy sentence. "Don't deploy" with the numbers is a
   passing result; a decision with no forgetting check is not.

## Checklist (mirrors manifest.json + Excel tracker)

- [ ] Mon: Study fine-tuning theory and the selection order (knowledge-base 06).
- [ ] Tue: Build the SFT dataset (instructions + responses) from the Week 6 corpus.
- [ ] Wed: Train LoRA with TRL/Unsloth (Colab free tier or local GPU); log loss curves.
- [ ] Thu: Create preference pairs; run a small DPO step; compare before/after on the eval.
- [ ] Fri: Use case: publish the before/after eval table; decide deploy vs iterate.
- [ ] Sat: Take the Week 10 quiz (quiz.md), pass with 8/10; record the score in Notes.
- [ ] Milestone: Update the Excel tracker; commit the adapter and eval results.
