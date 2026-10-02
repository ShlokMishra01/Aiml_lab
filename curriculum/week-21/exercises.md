# Week 21: Exercises & Checklist

## Graded exercises

1. **Easy**: Run `notebooks/01-unity-catalog-and-delta-lab.ipynb` end-to-end. It prints, at the end, the bronze row count and the number of time-travel versions. Record both numbers in the Week 21 tracker sheet.

2. **Standard**: In `notebooks/02-medallion-sql.ipynb`, verify your silver layer passes two invariants: (1) no duplicate `shipment_id` values, and (2) no `NULL` `weight_kg` or `distance_km`. Add a markdown cell that documents the imputation values you used (weight mean, distance mean) and your one-sentence rationale for each.

3. **Stretch**: Add a second gold artifact (table or view) that ranks the **top 5 worst lanes by on-time rate per month** using a window function (`ROW_NUMBER() OVER (PARTITION BY month ORDER BY on_time_rate)`). State which lane/carrier combination you would fix first and why, in one sentence.

4. **Portfolio**: Advance the **ZoroLogistics lakehouse** milestone (see [`curriculum/projects/README.md`](../projects/README.md)): publish the gold dashboard query as an AI/BI dashboard (SQL editor → run → "Create dashboard"), and capture the Catalog Explorer **lineage** graph (bronze → silver → gold) to include in your portfolio.

## Hints

1. **Easy**: Run the notebook top to bottom; if `spark.version` or `current_user()`
   errors, you are not attached to compute yet. The two numbers to record are in the
   *final* cell, not the `%sql` count cells.
2. **Standard**: Copy the silver quality-check query into a new `%sql` cell; a
   passing silver has `null_weights = 0` and `distinct_shipments = rows`. If
   `null_weights > 0`, your `COALESCE` is missing a column, re-read cell 4.
3. **Stretch**: A "worst lanes per month" ranking needs a window *after* the gold
   aggregation; nest the `ROW_NUMBER() OVER (PARTITION BY month ORDER BY
   on_time_rate)` outside your gold query, not inside `GROUP BY`.
4. **Portfolio**: The AI/BI dashboard needs the *dashboard-ready* query (the rolling
   3-month one in notebook 02), not the raw gold table; lineage lives on the table's
   **Lineage** tab in Catalog Explorer, not in the SQL editor.

## Checklist (mirrors manifest.json + Excel tracker)

- [ ] Mon: Create the Databricks account/workspace (free trial); tour the UI.
- [ ] Tue: Unity Catalog lab: create catalog/schema/volume; load CSV data; grant rights.
- [ ] Wed: Delta Lake lab: create tables, time travel, VACUUM, OPTIMIZE, liquid clustering.
- [ ] Thu: Medallion in SQL: bronze raw → silver clean → gold aggregates for shipments.
- [ ] Fri: Use case: governed silver/gold tables with lineage; build a first AI/BI dashboard.
- [ ] Sat: Take the Week 21 quiz (quiz.md), pass with 8/10; record the score in Notes.
- [ ] Milestone: Update the Excel tracker; commit the SQL notebooks.
