# Week 22: Quiz (10 questions, 8/10 to pass)

Answer each, then check the answer key. Each question ends with a pointer to the
Concepts section (§) or notebook cell it tests.

1. **(MCQ)** In PySpark, which of the following is an *action* (triggers execution)?
   (see Concepts §laziness)

   - A) `df.select("id")`
   - B) `df.filter(col("x") > 0)`
   - C) `df.count()`
   - D) `df.withColumn("y", col("x") * 2)`

2. **(Short answer)** Why does the notebook's cross-check cell print `match:
   abs(py_avg - sql_avg) < 1e-6` instead of testing exact equality `py_avg ==
   sql_avg`? (see Concepts §PySpark worked example; notebook 01 final cells)

3. **(MCQ)** In Lakeflow Pipelines, which dataset type is *recomputed to reflect
   current state*, making it correct when a dimension changes late? (see Concepts
   §Lakeflow Pipelines)

   - A) streaming table
   - B) materialized view
   - C) temporary view
   - D) external table

4. **(MCQ)** In notebook `02-streaming-and-dlt-pipeline.ipynb`, what does
   `@dp.expect_or_drop("weight_positive", "weight_kg > 0")` do to a row with
   `weight_kg = -5`? (see Concepts §expectations; notebook 02 cell 5)

   - A) Keeps the row and records a warning metric
   - B) Stops the entire pipeline update
   - C) Removes the row and continues the update
   - D) Converts the weight to 0

5. **(Short answer)** A Lakeflow dataset function must not call `collect()`,
   `count()`, `toPandas()`, or `save()`. Explain in one sentence why. (see Concepts
   §Lakeflow Pipelines)

6. **(MCQ)** You run two Structured Streaming queries against the same source but
   point both at one checkpoint location. What happens? (see Concepts §Structured
   Streaming; How it breaks)

   - A) They share state safely and both resume correctly
   - B) Exactly-once resume state corrupts, each query needs its own checkpoint
   - C) Nothing, checkpoints are read-only
   - D) The second query silently becomes batch

7. **(MCQ)** Which Delta sink output mode is **not** supported for streaming writes?
   (see Concepts §Structured Streaming)

   - A) Append
   - B) Complete
   - C) Update
   - D) Append and Complete both work

8. **(Short answer)** In the PySpark KPI aggregation, why is
   `F.when(F.col("is_on_time"), 1.0).otherwise(0.0)` wrapped in `F.avg(...)` rather
   than averaging the boolean column directly? (see Concepts §PySpark worked example;
   notebook 01 cell 7)

9. **(MCQ)** A **Lakeflow Job** task should run only when all of its dependencies
   succeeded. Which Run-if gate is the default that expresses this? (see Concepts
   §Lakeflow Jobs)

   - A) `AT_LEAST_ONE_SUCCESS`
   - B) `NONE_FAILED`
   - C) `ALL_SUCCESS`
   - D) `ALL_DONE`

10. **(MCQ)** Auto Loader (`cloudFiles`) vs. `COPY INTO`: when do you prefer Auto
    Loader? (see Concepts §Structured Streaming)

   - A) For a few thousand files that never change schema
   - B) For millions of files or schemas that evolve
   - C) Only for Kafka topics
   - D) When you want to avoid a checkpoint

## Answer key

1. **C: `df.count()`.** `count`, `show`, `collect`, and `saveAsTable` are actions;
   `select`, `filter`, and `withColumn` are lazy transformations.

2. **Floating-point arithmetic** means two equivalent aggregations can differ in the
   last few decimal places; the tolerance check (`< 1e-6`) tests "the same number"
   without a false negative from a rounding difference.

3. **B: materialized view.** It is recomputed to reflect current state ("always
   correct"); a streaming table processes each record once and does not recompute on
   late dimension changes.

4. **C: removes the row and continues.** `expect_or_drop` discards violating rows;
   `@dp.expect` would warn-and-keep, and `expect_or_fail` would abort the update.

5. **Because those are actions that force eager execution**, which breaks the
   declarative plan the pipeline needs to resolve ordering/retries; a dataset
   function must return a lazy DataFrame untouched.

6. **B.** A checkpoint stores per-query offsets, commits, and state; two queries
   sharing one path corrupt each other's resume. Each query needs its own UC volume
   path.

7. **C: Update.** Delta sinks support Append and Complete, but not Update mode.

8. **A boolean can't be averaged meaningfully**, and `is_on_time` may be a boolean or
   a string depending on inference; casting to 1.0/0.0 turns it into a numeric that
   `avg` turns into a proper on-time rate.

9. **C: `ALL_SUCCESS`.** It is the default Run-if gate: the task runs after every
   dependency succeeds.

10. **B.** Auto Loader is built for scale and schema evolution (millions of files,
    incremental, evolving schemas); `COPY INTO` is simpler for thousands of stable
    files.
