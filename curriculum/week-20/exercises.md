# Week 20: Exercises & Checklist

## Graded exercises

1. **Easy**: Run `notebooks/01-bedrock-converse-and-knowledge-bases.ipynb` to completion.
   It runs the Week 6 prompt suite across Bedrock models with the Converse API and queries a
   Knowledge Base for RAG, ending by printing recall and groundedness. Record both numbers
   in the Week 20 tracker sheet.

2. **Standard**: Add a *third* Bedrock model to the prompt-suite comparison (for example
   Nova Lite vs Claude vs Llama). Add a markdown cell with a three-row table of accuracy,
   latency, and estimated token cost, and state the delta each model gains or loses against
   the others.

3. **Stretch**: Apply the Guardrail to the **Knowledge Base response path** (not only the
   agent). Run an off-topic query set through `retrieve_and_generate` with the guardrail
   attached, and show how the blocked/allowed counts move compared to the unguarded run.

4. **Portfolio**: Publish the **three-cloud comparison matrix** (Foundry vs Vertex vs
   Bedrock) to [`curriculum/projects/`](../projects/README.md). Every cell must trace to a measured
   number from Weeks 18 to 20; add a cost row and close with a one-paragraph "which cloud for
   which job" recommendation. This is the Phase 6 capstone, the matrix *is* the deliverable.

## Hints

1. **Easy**: Record `RECALL` and `GROUNDEDNESS`; the dry-run local retriever prints the
   *target* values (`1.000 / 1.000`), a live Knowledge Base must meet or beat them.
2. **Standard**: Add a third model ID to `MODELS`, call `accuracy_for` on it, and state the
   delta in accuracy, latency, and estimated token cost against the other two.
3. **Stretch**: Attach the guardrail to `retrieve_and_generate` (pass the guardrail config
   in the KB call), then run an off-topic query set and compare blocked/allowed counts.
4. **Portfolio**: Build the matrix row-by-row from your Weeks 18 to 20 guides; a cell with no
   printed number is a gap, leave it blank and honest rather than guessing.

## Checklist (mirrors manifest.json + Excel tracker)

- [ ] Mon: Set up the AWS account and IAM least-privilege role; enable Bedrock models.
- [ ] Tue: Converse API lab: run the Week 6 prompt suite across Bedrock models.
- [ ] Wed: Build a Knowledge Base (RAG) for shipping policies; query with citations.
- [ ] Thu: Create a Bedrock Agent + Guardrails; test blocked prompts.
- [ ] Fri: Use case: publish the 3-cloud comparison matrix (Foundry vs Vertex vs Bedrock) with cost.
- [ ] Sat: Take the Week 20 quiz (quiz.md), pass with 8/10; record the score in Notes.
- [ ] Milestone: Update the Excel tracker; commit the AWS guide and matrix.
