# Week 02: Exercises & Checklist

## Graded exercises

1. **Easy**: Run `notebooks/01-pandas-cleaning.ipynb` to completion. It prints, at
   the end, the cleaned row count and the number of duplicate rows removed. Record
   both numbers in the Week 2 tracker sheet.

2. **Standard**: Profile the raw dataset and document **five** planted issues: (1)
   duplicate rows, (2) `NaN` weights, (3) `NaN` lane distances, and two more you find
   yourself (look at `delay_hours` for impossible values, `weight_kg` for non-positive
   values, or `status` for rows whose `actual_arrival` contradicts the label). For
   each, write the finding, the evidence (a count or a sample row), and the fix in your
   profile report.

3. **Stretch**: In `notebooks/02-sql-with-duckdb.ipynb`, rewrite the "on-time rate by
   carrier/lane/month" query using a **window function** (e.g. `AVG(...) OVER
   (PARTITION BY carrier_id, lane_id, month ORDER BY month)`) instead of a plain
   `GROUP BY`, and add a cell asserting the two approaches agree within floating-point
   tolerance.

4. **Portfolio**: Advance the **ZoroLogistics data generator + silver dataset**
   milestone (see [`curriculum/projects/README.md`](../projects/README.md)): turn the cleaning
   workflow into a runnable script `data/make_silver.py` that regenerates (or loads)
   the raw data, cleans it, runs the validation suite, and writes `data/silver/`.
   One command, one reproducible silver table.

## Hints

1. **Easy**: The final cell prints two numbers: `CHECKS_PASSED` and
   `SILVER_ROW_COUNT`. Record both; if `CHECKS_PASSED` is not 12, scroll up to the
   first `FAIL` line and fix that decision before re-running.
2. **Standard**: For the two *un*planted issues, profile `delay_hours` (look at its
   `describe()` tail for extreme values) and check the relationship between
   `planned_arrival` and `planned_departure`, a row where arrival precedes departure
   is a structural defect.
3. **Stretch**: A window function keeps every row, so wrap the per-carrier monthly
   rate in a CTE and add `AVG(...) OVER (PARTITION BY carrier_id)`; then assert the
   two approaches agree with `np.allclose`.
4. **Portfolio**: Structure `make_silver.py` as three functions,
   `load_or_generate()`, `clean(df)`, `validate(df) -> bool`, so the script reads as
   the same `raw → clean → validate → save` flow the notebook does, but in one command.

## Checklist (mirrors manifest.json + Excel tracker)

- [ ] Mon: Study data quality concepts; run the pandas refresher exercises.
- [ ] Tue: Run the pandas cleaning notebook; find and document 5 data issues in the generator output.
- [ ] Wed: Write SQL queries in DuckDB: on-time rate by carrier/lane/month, windows, top-lane analysis.
- [ ] Thu: Add a data validation suite (pandera) with at least 10 checks.
- [ ] Fri: Use case: deliver the cleaned silver dataset + profile report; document every cleaning decision.
- [ ] Sat: Take the Week 2 quiz (quiz.md), pass with 8/10; record the score in Notes.
- [ ] Milestone: Update the Excel tracker; commit the silver pipeline script.
