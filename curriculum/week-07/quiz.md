# Week 07: Quiz (10 questions, 8/10 to pass)

Answer from the concepts and the notebook code. Each question notes where to find it.

1. **(MCQ)** RAG exists primarily to provide, in production order: (a) speed, cost, scale; (b) grounding, freshness, permissions; (c) fewer tokens, longer context, lower temperature; (d) fine-tuning, quantization, caching. *(see Concepts §"The seven-stage pipeline")*

2. **(Short answer)** Name the seven stages of the RAG pipeline in order. *(see Concepts diagram / KB §2)*

3. **(MCQ)** In `01-rag-policy-bot.ipynb`, `section_aware_chunks` splits on: (a) every 256 tokens, (b) `## ` headings, (c) sentence boundaries, (d) embedding-similarity drops. *(see notebook cell 4)*

4. **(Short answer)** Given a 10-question golden set, vector-only retrieval hits 7 questions and hybrid+rerank hits 9. Write both recall@5 values and explain what the delta means. *(see Concepts Worked example 1)*

5. **(MCQ)** RRF fuses ranked lists by: (a) averaging the raw scores, (b) summing 1/(k+rank) across lists, (c) taking the max score, (d) multiplying ranks. *(see Concepts Worked example 2)*

6. **(Short answer)** In `02-knowledge-graph-lab.ipynb`, what does the `SERVES` edge's `cost` attribute equal, and how is the graph kept connected despite planted NaN distances? *(see notebook cell 4)*

7. **(MCQ)** The single highest-leverage retrieval upgrade for answer quality is: (a) a bigger embedder, (b) reranking with a cross-encoder, (c) a longer chunk, (d) more questions in the eval set. *(see Concepts §"Hybrid search and reranking")*

8. **(Short answer)** Why must retrieval (recall@k) and generation (groundedness) be measured separately? What does each failure point to? *(see Concepts §"Retrieval evals")*

9. **(MCQ)** A question best answered by a knowledge graph rather than vector RAG is: (a) "what is the late-delivery refund?", (b) "which carriers reach Long Beach, and at what cost?", (c) "define dangerous goods", (d) "summarize the customs policy". *(see Concepts §"Knowledge graphs")*

10. **(Short answer)** In notebook 1 cell 8, why does `recall_at_k` check whether *any* of the top-k chunk `doc_id`s matches a relevant `doc_id`, rather than requiring the exact chunk? *(see notebook cells 7 to 8)*

## Answer key

1. **(b)**: grounding (citable text), freshness (re-index not retrain), permissions (filter the index before retrieval).
2. **ingest → chunk → embed → index → retrieve → rerank → generate** (with citations).
3. **(b)**: it splits on `## ` section headings so each chunk is one coherent policy section carrying its `doc_id` and section name as citation metadata.
4. **vector-only recall@5 = 0.70; hybrid+rerank recall@5 = 0.90.** The delta (2 recovered questions) shows the keyword arm + reranker fetched the right document for queries vector-only missed; recall says nothing about answer quality.
5. **(b)**: `1/(60+rank_vec) + 1/(60+rank_kw)`; agreement across signals outranks one strong signal, and no score normalization is needed.
6. `cost = carrier base_rate_usd_per_km_ton × lane distance_km`; NaN distances (and transit days) are filled with defaults (900 km / 3 days) so every lane remains connected.
7. **(b)**: a cross-encoder reranker re-scores query and passage together; it is cheap relative to generation and moves the best chunk to the top.
8. Low recall@k is an indexing/chunking problem (fix the data path); low groundedness with high recall is a prompt/generation problem (fix the instruction/citations). A single end-to-end score hides which layer is broken.
9. **(b)**: it is a constrained traversal over an explicit `SERVES`/`ARRIVES_AT` relationship (shortest/cheapest path), which chunk retrieval only approximates. The others are lookup/definition questions vector RAG handles.
10. Recall@k is about *did we surface the right document*, not the exact chunk, a relevant document may be split across several chunks, and `k` would have to be huge to guarantee the exact passage. The doc_id check is the standard recall definition.
