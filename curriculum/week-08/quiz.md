# Week 08: Quiz (10 questions, 8/10 to pass)

Answer from the concepts and the notebook code. Each question notes where to find it.

1. **(MCQ)** "Open weights" means: (a) the model is OSI open-source, (b) the trained weights are published so you can run/quantize/fine-tune them, (c) there is no license, (d) it is free of all legal restrictions. *(see Concepts §"Open vs. closed")*

2. **(Short answer)** For a commercial ZoroLogistics shipping tool, why is Apache-2.0/MIT the safe license default, and what must you do before shipping a Llama or Gemma model? *(see Concepts table / KB §1)*

3. **(MCQ)** The weights-only memory of a 7B model at 4-bit (Q4) is about: (a) 14 GB, (b) 7 GB, (c) 3.5 GB, (d) 1 GB. *(see notebook cell 2 / Concepts table)*

4. **(Short answer)** In `02-vram-sizing-and-model-selection.ipynb`, write the formula `kv_cache_gb` uses and compute it for 32 layers, 32 heads, head_dim 128, seq_len 4096, at 2 bytes/param. *(see notebook cell 6)*

5. **(MCQ)** If `-ngl` (layers offloaded to GPU) is 0, the model is: (a) fully on GPU, (b) silently running on CPU, (c) using MLX, (d) quantized to 4-bit. *(see Concepts §"GPU setup")*

6. **(Short answer)** In `01-local-model-playground.ipynb`, what does the Modelfile set, and what does `--format json` do differently from a prompt that says "answer in JSON"? *(see notebook cell 7)*

7. **(MCQ)** Which runtime is usually fastest on Apple Silicon, and why? (a) llama.cpp, CPU only; (b) MLX, unified memory; (c) Ollama, smaller; (d) LM Studio, GUI. *(see Concepts §"The local stack")*

8. **(Short answer)** In notebook 2 cell 10, why does the picker recommend a *3B* model for the 8 GB Windows laptop but an *8B* model for the 16 GB MacBook? What is the `0.8` comfort factor doing? *(see notebook cells 8 & 10)*

9. **(MCQ)** Changing the picker's `task` from `"triage"` to `"reasoning"` on a 16 GB box returns `None`. This is because: (a) reasoning models don't exist, (b) the smallest reasoning-class model in the catalog needs more than the ~12.8 GB budget at Q4, (c) the license forbids it, (d) the OS reserve is too small. *(see Concepts Worked example 2)*

10. **(Short answer)** What two numbers should you report when someone asks "how fast is your local model", and which one does the user feel? *(see Concepts §"GPU setup" / KB §10)*

## Answer key

1. **(b)**: open *weights* are published; the license (which may not be OSI open source) decides what you may legally do. (a) conflates distribution with licensing.
2. Apache-2.0/MIT are permissive and allow commercial use with only attribution/notices; Llama and Gemma are usable commercially but carry recorded terms (e.g. a ~700M-MAU scale cap, prohibited-use list), so you must record the license and terms in the compliance file before shipping.
3. **(c)**: `7B × 0.5 bytes/param ≈ 3.5 GB` of weights.
4. `2 × layers × heads × head_dim × seq_len × bytes_per_param` → `2 × 32 × 32 × 128 × 4096 × 2 = 2,147,483,648 bytes ≈ 2.15 GB`.
5. **(b)**: with no layers offloaded, llama.cpp runs on CPU; you can have "installed CUDA" while the GPU does none of the work.
6. The Modelfile sets `FROM <model>`, a triage `SYSTEM` prompt, and `PARAMETER temperature 0`. `--format json` is a *generation-time constraint* (JSON mode) that forces valid JSON, whereas a prompt "answer in JSON" is only a request the model can ignore.
7. **(b)**: MLX runs over Apple's unified memory (no host↔device copies), which is often the fastest local path on M-series chips.
8. The picker returns the largest model whose `total_footprint` fits under `available_gb × 0.8` (the comfort factor reserves 20% for headroom beyond the OS reserve); 8 GB × 0.8 = 6.4 GB only fits a 3B at Q4 (~4.7 GB), while 16 GB × 0.8 = 12.8 GB fits an 8B at Q4 (~8.6 GB).
9. **(b)**: `MIN_PARAMS["reasoning"] = 13.0` excludes the 3B to 8B models, and the 14B at Q4 totals ~14 GB, over the 12.8 GB budget, so no option fits.
10. **Prefill speed** (prompt tokens/sec) and **decode speed** (generation tokens/sec); the user feels **decode**, the rate at which new tokens stream out.
