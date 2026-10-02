# Week 09: Quiz (10 questions, 8/10 to pass)

Answer on your own first, then check the answer key. Each question notes where the
answer lives, so you can re-read the exact section or cell you missed.

## Questions

1. **(MCQ)** A model has 13B parameters. How much *weight-only* VRAM does it need in INT4, and which rule gives you the answer? (see Concepts §"One number per format")
   - A) ~26 GB, 13B × 2 bytes
   - B) ~13 GB, 13B × 1 byte
   - C) ~6.5 GB, 13B × 0.5 bytes
   - D) ~3.25 GB, 13B × 0.25 bytes

2. **(MCQ)** Under integer quantization with `scale ≈ 0.0039` and `zero_point = 0`, the float `0.5` maps to which integer? (see Concepts §Worked example 2)
   - A) 128
   - B) 255
   - C) 0
   - D) 64

3. **(Short answer)** Why does the knowledge base say perplexity is "a screen, not a verdict"? Give the specific ZoroLogistics failure a near-flat perplexity ladder can hide. (see Concepts §"Perplexity is a screen, not a verdict")

4. **(MCQ)** On the 7B triage model, Q2_K loses ~8 F1 points vs FP16 while its perplexity looks only slightly worse. What is the correct production decision, and why? (see Concepts §Worked example 3)
   - A) Ship Q2_K, it is the smallest and cheapest
   - B) Ship Q4_K_M, it keeps most F1 at a fraction of VRAM; avoid Q2_K
   - C) Ship FP16, any quantization is too risky
   - D) Ship Q8_0, it is the only near-lossless option

5. **(MCQ)** In `notebooks/01-quantization-lab.ipynb`, what does the `perplexity()` helper (cell 12) actually compute? (see notebook cell 12)
   - A) `exp(mean cross-entropy loss)` over the note's tokens
   - B) The triage accuracy over 30 tickets
   - C) The bytes-per-parameter of each format
   - D) The fraction of tokens that decode correctly

6. **(Short answer)** In the lab notebook, what is the difference between `LIVE_FP16` and `LIVE_QUANT`, and what hardware condition sets each to `True`? (see notebook cell 4)

7. **(MCQ)** Which mechanism explains why vLLM sustains higher throughput than a naive batcher under mixed-length load? (see Concepts §"Serving")
   - A) It quantizes every model to INT4 automatically
   - B) PagedAttention + continuous batching back-fill idle GPU time with new tokens
   - C) It always uses a batch size of 1
   - D) It runs the model in FP32 for accuracy

8. **(MCQ)** In `notebooks/02-vllm-serving-and-benchmarks.ipynb`, why does the same OpenAI SDK client work against both vLLM and Ollama? (see notebook cell 14)
   - A) Both engines were trained on the same data
   - B) Both expose an OpenAI-compatible `/v1` surface; only `base_url` changes
   - C) The notebook patches the SDK for each engine
   - D) Ollama imports vLLM under the hood

9. **(Short answer)** You measure: FP16 triage accuracy 0.92, INT8 0.92, INT4 0.89, with INT4 at 25% of FP16 VRAM. Write the one-sentence production recommendation the Friday report requires, with the numbers. (see Concepts §Worked example 3 + Friday gate)

10. **(MCQ)** Which failure mode does the "How it breaks" section attribute to weight-only quantization on GPU? (see Concepts §"How it breaks")
    - A) It always makes the model larger
    - B) It reliably shrinks memory but is not automatically faster without fused kernels
    - C) It removes the KV cache
    - D) It requires Apple MPS to run

## Answer key

1. **C)** INT4 is 4 bits = 0.5 bytes/param, so 13B × 0.5 = 6.5 GB. The rule is "roughly 1 GB per billion parameters at 4-bit," and `bytes = params × (bits / 8)`.

2. **A)** `q = round(0.5 / 0.0039) = round(128.2) = 128`. The scale is `(max − min) / 255 = 1.0 / 255 ≈ 0.0039`.

3. **Perplexity is a fast proxy for fluency, not for the specific job.** A quantized model can have near-identical perplexity yet miss a named entity, emit broken JSON, or route a billing ticket to claims. You must run the task eval (e.g., 30-ticket triage accuracy) to make the shipping decision.

4. **B)** Q4_K_M keeps triage F1 at ~0.897 (a ~1.5-point loss) for ~3.5× less VRAM and ~3.4× lower cost; Q2_K's 8-point F1 drop (0.912 → 0.831) would silently misroute a meaningful share of tickets, so it is the avoid zone.

5. **A)** It computes `math.exp(total_loss / total_tokens)`, the exponentiated mean cross-entropy over each note's tokens, averaging loss across notes so short and long notes contribute equally.

6. **`LIVE_FP16 = (DEVICE in ("cuda", "mps"))`**: FP16 runs on NVIDIA and Apple Silicon. **`LIVE_QUANT = (DEVICE == "cuda")`**, bitsandbytes 8/4-bit needs CUDA only. On MPS only FP16 runs live; on CPU both are `False` and the fallback path runs.

7. **B)** Continuous batching admits new requests token-by-token and evicts finished ones immediately, and PagedAttention's fixed-size KV pages eliminate fragmentation, so the GPU back-fills a straggler's idle time with new work.

8. **B)** Both expose an OpenAI-compatible `/v1/chat/completions` endpoint; the notebook only changes `base_url` (vLLM on :8000, Ollama on :11434) and the model name, which is the interoperability superpower.

9. **A passing answer names the trade and the ship/no-ship line.** E.g., "Ship INT4: it keeps 96.7% of FP16 triage accuracy (0.89 vs 0.92) at 25% of the VRAM, and here are the tickets it misfiles." (Your numbers must come from your run, not the estimate.)

10. **B)** Weight-only quants shrink memory reliably, but the speed win depends on fused kernels, without them you get smaller but not quicker.
