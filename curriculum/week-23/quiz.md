# Week 23: Quiz (10 questions, 8/10 to pass)

Answer each, then check the answer key. Each question ends with a pointer to the
Concepts section (§) or notebook cell it tests.

1. **(MCQ)** Why are the old MLflow Registry "Staging/Production" stages deprecated
   in favor of aliases? (see Concepts §aliases)

   - A) Aliases are faster to query
   - B) Aliases are mutable, so you can hold several named references (Champion, Challenger, `@prod`) and promote by re-pointing a pointer
   - C) Stages never worked with XGBoost
   - D) Aliases require a model signature

2. **(Short answer)** In `01-mlflow-feature-engineering-training.ipynb`, the
   `carrier_daily_stats` table declares `timeseries_columns=["metric_date"]` and the
   lookup sets `timestamp_lookup_key="planned_departure"`. What would leak into
   training if you *removed* the timestamp key and joined the daily table directly on
   `carrier_id`? (see Concepts §feature engineering; notebook 01 cell 9)

3. **(MCQ)** Which AI Search search mode fuses vector similarity with keyword (BM25)
   matching via Reciprocal Rank Fusion? (see Concepts §AI Search)

   - A) ANN
   - B) semantic
   - C) hybrid
   - D) direct upload

4. **(MCQ)** AI functions like `ai_classify` and `ai_extract` require which runtime
   environment? (see Concepts §AI functions)

   - A) Any classic all-purpose cluster
   - B) Serverless compute and DBR 18.2+
   - C) A dedicated GPU cluster only
   - D) Pro SQL warehouse with Photon

5. **(Short answer)** Why does the notebook compute groundedness as the fraction of
   the answer's tokens that appear in the retrieved context, rather than just
   printing "the answer looks good"? (see Concepts §worked RAG example; notebook 02
   cell 13)

6. **(MCQ)** In the champion/challenger comparison, the challenger is trained after
   dropping the `daily_*` columns. What does a positive
   `champion_MAE < challenger_MAE` (i.e., a positive "point-in-time gain") tell you?
   (see Concepts §worked example; notebook 01 final cell)

   - A) The time-series feature is hurting the model
   - B) The time-series feature adds predictive value beyond static features
   - C) The model is overfitting
   - D) The training set is too small

7. **(MCQ)** You want a low-traffic ETA endpoint that costs $0 while idle. Which
   serving setting is correct? (see Concepts §Serving)

   - A) `min_provisioned_throughput > 0`
   - B) `scale_to_zero_enabled: true`
   - C) provisioned throughput
   - D) an external-model endpoint

8. **(Short answer)** What is the difference between `ai_mask` (an AI function) and a
   Unity Catalog column mask? (see Concepts §AI functions; How it breaks)

9. **(MCQ)** Genie Agents cannot exceed the *caller's* grants because… (see Concepts
   §Genie)

   - A) Genie only runs pre-written SQL
   - B) Genie's SQL runs as the viewer against tables they can already read
   - C) Genie disables all SQL functions
   - D) Genie routes through an external model

10. **(MCQ)** In `02-vector-search-rag.ipynb`, the Delta Sync index uses
    `embedding_vector_column="embedding"` (self-managed). What is the *managed*
    alternative? (see Concepts §AI Search; notebook 02 cell 5)

   - A) Provide `embedding_source_column` + an `embedding_model_endpoint_name` and let the index embed
   - B) Upload vectors one by one with `upsert`
   - C) There is no managed alternative
   - D) Store embeddings in a CSV

## Answer key

1. **B.** Aliases are mutable named references, so you can hold Champion, Challenger,
   and `@prod` simultaneously and promote by re-pointing one alias, stages forced a
   single linear state.

2. **Future carrier statistics would leak.** Joining `carrier_daily_stats` on
   `carrier_id` alone pulls the carrier's *latest* stats (possibly after the shipment
   departed); the timestamp key makes the join AS OF `planned_departure`, so only
   history before departure is used.

3. **C: hybrid.** Hybrid combines ANN vector search with BM25 keyword search via
   Reciprocal Rank Fusion.

4. **B: serverless compute and DBR 18.2+.** AI functions will not run on
   Pro/Classic warehouses.

5. **Groundedness must be measured, not asserted.** Token overlap is a cheap,
   reproducible proxy that checks whether the answer is built from retrieved text
   rather than the model's prior, an answer that *sounds* right but invents a clause
   would score low.

6. **B.** The champion (with the AS-OF time-series feature) beats the static-only
   challenger, so the point-in-time feature carries predictive signal; the gain is
   that measured margin.

7. **B: `scale_to_zero_enabled: true`** (with `min_provisioned_throughput: 0`) lets
   the endpoint scale to zero replicas while idle, costing nothing until a request
   cold-starts it.

8. **`ai_mask` is a content transform**: it rewrites free text once (redacting named
   PII entities) as a batch operation. A **column mask** is a deterministic governance
   policy enforced at query time that controls *who sees* a column's value, not a
   text rewrite.

9. **B.** Genie's generated SQL executes as the *viewer* with the viewer's Unity
   Catalog grants, so it cannot read tables or see unmasked values the caller cannot.

10. **A.** Managed embeddings let Databricks compute vectors from a text column using
    an `embedding_model_endpoint_name`; self-managed means you pre-computed and stored
    the `embedding` column yourself.
