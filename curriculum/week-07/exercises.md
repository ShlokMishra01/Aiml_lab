# Week 07: Exercises & Checklist

## Graded exercises

1. **Easy**: Re-run `01-rag-policy-bot.ipynb` with `k=3` and `k=10`; report how recall changes and write one sentence on what recall@k rewards.
2. **Standard**: Add two questions to the golden eval set (make one span two policy documents); re-measure recall and fix any miss you can.
3. **Stretch**: In `02-knowledge-graph-lab.ipynb`, add a `via` constraint: cheapest route *through* a chosen port, returning the full path with total cost.
4. **Portfolio**: Package the RAG bot as `projects/policy_bot.py` (CLI: question in → cited answer out), with the golden eval set and a saved recall number.

## Hints

1. **Easy**: Re-run `recall_at_k(vector_search, k=3)` and `k=10`; recall@k is monotone non-decreasing in k, so explain *why* it rewards larger k even when precision falls.
2. **Standard**: Add two `(question, [doc_ids])` tuples to `QUERIES`; make one question answerable only by combining `POL-001` and `POL-002`. Re-run both recall functions and inspect which arm (vector vs. keyword) recovered each.
3. **Stretch**: Filter candidate `SERVES` edges so the path passes through a chosen port node; you'll need to traverse `carrier → lane → port → lane → port` and sum the two leg costs, not just one edge.
4. **Portfolio**: Wrap the chunk→embed→index→hybrid→generate chain in a function that takes a question string and returns `(answer, [citations])`; save `recall_hybrid` to a JSON file and print it on `--eval`.

## Checklist (mirrors manifest.json + Excel tracker)

- [ ] Mon: Study retrieval fundamentals (knowledge-base 05).
- [ ] Tue: Chunk and embed the policy corpus; build a vector index; measure baseline retrieval accuracy.
- [ ] Wed: Add hybrid search and reranking; cite sources in answers; measure groundedness.
- [ ] Thu: Build the carrier-lane-port graph in Neo4j; query shortest and cheapest routes.
- [ ] Fri: Use case: the RAG bot answers 10 unseen questions with citations; log retrieval misses.
- [ ] Sat: Take the Week 7 quiz (quiz.md), pass with 8/10; record the score in Notes.
- [ ] Milestone: Update the Excel tracker; commit RAG and graph labs.
