# Week 22: Exercises & Checklist

## Graded exercises

1. **Easy**: Run `notebooks/01-pyspark-data-engineering.ipynb` to completion. It prints the final on-time rate and a `match: True/False` comparing the PySpark aggregation against the SQL version. Record both in the Week 22 tracker sheet.

2. **Standard**: In `01-pyspark-data-engineering.ipynb`, add a window function that ranks carriers by on-time rate *within each month*. Identify the most-improved and the most-declined carrier across consecutive months, and write one sentence hypothesizing why (join in `carrier_name` and `region`).

3. **Stretch**: In `02-streaming-and-dlt-pipeline.ipynb`, add a third expectation on the silver materialized view, e.g. `@dp.expect_or_fail("non_negative_delay", "delay_hours >= 0")`, re-run the pipeline, and describe (in a markdown cell) what happens to the update when the constraint is violated, versus a `@dp.expect_or_drop`.

4. **Portfolio**: Advance the **ZoroLogistics streaming pipeline** milestone: wrap the pipeline in a scheduled **Lakeflow Job** (task type Pipeline, run-if `ALL_SUCCESS`), and capture the pipeline DAG screenshot plus your monitoring query for the portfolio.

## Hints

1. **Easy**: Run notebook 01 top to bottom; the numbers to record are in the *final*
   cell (`final on-time rate` and `enriched rows`), and `match: True/False` is the
   cross-check cell just before it. If `match` is `False`, diff your PySpark `agg`
   against the SQL `CASE`.
2. **Standard**: The window already exists (`rank_in_month`); to find the
   most-improved/declined carrier, join each month's `rank_in_month = 1` to the prior
   month's on `carrier_id` and diff `on_time_rate`.
3. **Stretch**: Add the `@dp.expect_or_fail` decorator *above* the others on `silver`,
   drop a `delay_hours < 0` row into `events/`, and re-run. Contrast: `expect_or_fail`
   aborts the update; `expect_or_drop` would have removed the row and continued.
4. **Portfolio**: A Lakeflow Job's **Pipeline** task type wraps the pipeline; set the
   run-if to `ALL_SUCCESS` on any downstream task, and capture both the DAG screenshot
   and the `system.lakeflow.jobs` monitoring query.

## Checklist (mirrors manifest.json + Excel tracker)

- [ ] Mon: PySpark lab: transform shipment data with DataFrames; compare with SQL.
- [ ] Tue: Write a DLT pipeline in Python (or SQL) with expectations on data quality.
- [ ] Wed: Add a streaming table for live shipment events (Auto Loader/streaming source).
- [ ] Thu: Create a Lakeflow Job: schedule and orchestrate the pipeline; check runs and lineage.
- [ ] Fri: Use case: the streaming KPI pipeline passes quality gates; publish a monitoring query.
- [ ] Sat: Take the Week 22 quiz (quiz.md), pass with 8/10; record the score in Notes.
- [ ] Milestone: Update the Excel tracker; commit the pipeline code.
