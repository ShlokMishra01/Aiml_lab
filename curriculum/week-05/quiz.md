# Week 05: Quiz (10 questions, 8/10 to pass)

Answer from the concepts and the notebook code. Each question notes where to find it.

1. **(MCQ)** An LLM "answering" a question is best described as: (a) retrieving the closest fact from a knowledge base, (b) sampling the next token from a learned distribution, repeatedly, (c) executing a reasoning plan stored between calls, (d) looking up the prompt in a cache. *(see Concepts §"Tokenization is the front door")*

2. **(Short answer)** In `01-tokenization-lab.ipynb`, why does `enc.encode("ZoroLogistics")` return 4 tokens while `enc.encode("shipment")` returns 1? *(see notebook cell 6)*

3. **(MCQ)** The causal mask exists so that: (a) attention runs faster, (b) a token cannot attend to future positions, (c) embeddings stay normalized, (d) the softmax doesn't overflow. *(see Concepts §"Self-attention")*

4. **(Short answer)** Write the formula `estimate_cost` uses in notebook 1, and compute the per-call cost for 57 input tokens and 60 output tokens at $1.00/$3.00 per Mtok (to the nearest $0.000001). *(see notebook cell 10)*

5. **(MCQ)** In the notebook's chars/token table, a bill of lading tokenizes at about: (a) 5.3 chars/token, (b) 3.0 chars/token, (c) 4.0 chars/token, (d) 1.0 chars/token. *(see notebook cell 8 / Concepts table)*

6. **(Short answer)** In `02-embeddings-and-attention-lab.ipynb`, what is the correct top-1 commodity for the query *"temperature-sensitive medical cargo that must stay cold"*, and why does cosine similarity rank it first? *(see notebook cells 2 & 6)*

7. **(MCQ)** The KV cache turns generation from O(n²) to O(n) per step, at the cost of: (a) more compute, (b) linearly growing memory with sequence length, (c) losing the causal mask, (d) lower temperature. *(see Concepts §"The KV cache")*

8. **(Short answer)** For a 7B-class model (32 layers, 32 heads, head_dim 128) at 4096 context and FP16, compute the KV-cache size in GB using `2 × layers × heads × head_dim × seq_len × bytes_per_param`. *(see Concepts Worked example 2)*

9. **(MCQ)** Which knowledge-acquisition mechanism changes the model's weights? (a) zero-shot ICL, (b) RAG retrieval, (c) fine-tuning, (d) prompt caching. *(see Concepts table)*

10. **(Short answer)** In notebook 1 cell 12, why is the daily cost over 100,000 notes computed from the *average* note token count rather than the first note's count? *(see notebook cells 11 to 12)*

## Answer key

1. **(b)**: the model samples the next token from a learned distribution, repeatedly; "answering" is that loop run until EOS/`max_tokens`.
2. **BPE** builds its vocabulary by merging frequent character pairs, so the common word "shipment" became a single token while the rare brand name "ZoroLogistics" was never merged and splits into subword pieces (`Z`/`oro`/`Log`/`istics`).
3. **(b)**: the causal (lower-triangular) mask zeroes out future positions so a token attends only to itself and earlier tokens, which is also what makes incremental generation possible.
4. `(input_tokens/1e6)·price_in + (output_tokens/1e6)·price_out` → `57/1e6·1.00 + 60/1e6·3.00 = 0.000057 + 0.000180 = $0.000237`.
5. **(b)**: the BoL is ~3.0 chars/token (364 chars, 123 tokens) because its IDs, codes, and numeric fields split into subwords.
6. **pharmaceuticals**: "pharmaceuticals and medical supplies needing cold-chain handling" is semantically closest to "temperature-sensitive medical cargo," so its embedding vector is most aligned (highest cosine) with the query vector.
7. **(b)**: caching past K/V makes each step O(n) but the cache grows linearly (`2·L·H·hd·seq·bpp`), which is the dominant memory cost of long-context serving.
8. `2 × 32 × 32 × 128 × 4096 × 2 bytes = 2,147,483,648 bytes ≈ 2.15 GB`.
9. **(c)**: fine-tuning changes the weights; ICL and RAG leave them untouched, and caching is a serving optimization.
10. The daily figure must represent the *typical* note, not the first one; the first note is longer than average (41 tokens vs. ~30), so using it alone would overstate the daily cost.
