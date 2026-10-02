# Week 09: Exercises & Checklist

## Graded exercises

1. **Easy**: Run `notebooks/01-quantization-lab.ipynb` end-to-end. It prints a
   perplexity ladder and a triage-accuracy table (and a quality-vs-VRAM summary number
   at the end). Record the FP16 / 8-bit / 4-bit perplexity and triage accuracy in the
   Week 9 sheet of the Excel tracker. On CPU-only hardware, run the fallback path and
   record the *estimated* ladder, clearly labelled as an estimate.

2. **Standard**: In a markdown cell of the quantization notebook, reproduce the VRAM
   table by hand for a 7B, 8B, and 13B model: apply the bytes-per-param rule
   (FP16 ≈ 2, INT8 ≈ 1, INT4 ≈ 0.5) and name a GPU that fits each size, using
   [`reference/knowledge-base/06-model-engineering.md`](../../reference/knowledge-base/06-model-engineering.md)'s
   table as the source of truth. Your numbers must match the rule, not be copied.

3. **Stretch**: Extend `notebooks/02-vllm-serving-and-benchmarks.ipynb` to a third
   engine. Install SGLang (or TGI), serve the *same* model (`Qwen/Qwen2.5-1.5B-Instruct`),
   and re-run the latency/throughput benchmark at the same batch sizes. Add the new
   engine as a column to the comparison table and write one sentence on which engine you
   would pick for (a) high-QPS serving and (b) a workload where every request shares a
   long system prompt.

4. **Portfolio**: Write `week-09-quality-vs-cost-report.md` and commit it as the first
   artifact of the **quantized triage service** milestone (tracked in
   [`curriculum/projects/README.md`](../projects/README.md)). It must contain: the measured
   perplexity ladder, the triage accuracy per precision on the 30-ticket golden set, the
   vLLM-vs-Ollama benchmark table, and a one-sentence production recommendation whose
   numbers support it.

## Hints

1. **Easy**: Run the notebook as-is; the final cell prints `QUALITY_RETENTION_PCT`.
   If your device reports only FP16 live, record the *estimate* rows from cell 25 and
   label them as estimates, exactly as the cell says.

2. **Standard**: Your hand table is `params × (bits/8)` for 7B / 8B / 13B across
   FP16 (×2), INT8 (×1), INT4 (×0.5). Start from the rule, not from a copied value;
   the point is that the numbers *follow from* the bytes-per-param constant.

3. **Stretch**: Hold the model (`Qwen/Qwen2.5-1.5B-Instruct`) and batch sizes
   fixed, and only swap the server. SGLang's equivalent is
   `python -m sglang.launch_server`; its prefix cache is what you weigh for the
   shared-system-prompt workload.

4. **Portfolio**: The gate wants both the *quality* numbers (perplexity ladder +
   triage accuracy) and the *cost* numbers (serving table), read together into one
   sentence. A recommendation with only one side is half a deliverable.

## Checklist (mirrors manifest.json + Excel tracker)

- [ ] Mon: Study numeric formats and quantization methods (knowledge-base 06).
- [ ] Tue: Quantize a 7 to 8B model with bitsandbytes; measure quality on the triage eval.
- [ ] Wed: GGUF sweep with llama.cpp: Q4/Q5/Q8; record perplexity and speed.
- [ ] Thu: Serve with vLLM (OpenAI-compatible API); benchmark latency and throughput.
- [ ] Fri: Use case: publish the quality-vs-cost report; pick the production quantization.
- [ ] Sat: Take the Week 9 quiz (quiz.md), pass with 8/10; record the score in Notes.
- [ ] Milestone: Update the Excel tracker; commit the report.
