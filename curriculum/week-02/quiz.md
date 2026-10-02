# Week 02: Quiz (10 questions, 8/10 to pass)

Answer all ten, then check against the answer key. *(see Concepts §X)* points at a README subsection; *(see notebook cell Y)* points at a cell in `01-pandas-cleaning.ipynb` or `02-sql-with-duckdb.ipynb`.

1. **Multiple choice.** Under seed 42, the raw shipments table has 100,200 rows and the cleaning notebook's final silver row count is 100,000. What accounts for the 200-row difference? *(see Concepts §6, Step 4)*
   a. 200 `NaN` weights were dropped
   b. 200 duplicate rows were removed with `drop_duplicates()`
   c. 200 non-positive weights were dropped
   d. 200 bad transit rows were dropped

2. **Short answer.** Why does the notebook impute `NaN` `weight_kg` with the **median per commodity** rather than the global median? *(see Concepts §2, Step 4)*

3. **Multiple choice.** Which single SQL expression computes the company-wide on-time rate? *(see notebook "on-time rate" cell)*
   a. `COUNT(is_on_time)`
   b. `SUM(is_on_time) / COUNT(*)`
   c. `AVG(CAST(is_on_time AS INT))`
   d. `MAX(is_on_time)`

4. **Short answer.** Explain the difference between `GROUP BY` and a window function, in one sentence each. *(see Concepts §4)*

5. **Multiple choice.** In the window-function query, what does `QUALIFY rnk <= 2` do? *(see notebook "window functions" cell)*
   a. Limits the whole result to 2 rows
   b. Filters to rows whose window-computed rank is 2 or less, the top 2 carriers per month
   c. Sorts carriers alphabetically
   d. Deduplicates the `monthly` CTE

6. **Short answer.** Name three of the 12 validation checks in Step 5, and state the property each guards. *(see notebook Step 5)*

7. **Multiple choice.** What is **referential integrity** in this dataset, and which check enforces it? *(see Concepts §5)*
   a. Every `weight_kg` is positive, enforced by `(ships["weight_kg"] > 0).all()`
   b. Every `shipments.carrier_id`/`lane_id` matches an existing master key, enforced by `isin(...)`
   c. Every `shipment_id` is unique, enforced by `duplicated().sum() == 0`
   d. Every `delay_hours` is within range, enforced by `between(-48, 240)`

8. **Multiple choice.** DuckDB runs SQL directly over the registered pandas DataFrames. What does `con.register("shipments", ships)` accomplish? *(see notebook "register" cell)*
   a. Writes the DataFrame to a permanent `.db` file
   b. Exposes the in-memory DataFrame as a queryable table named `shipments`
   c. Converts the DataFrame to Parquet
   d. Starts a DuckDB server process

9. **Short answer.** A rate is a mean of a boolean. Given 100,000 silver rows with 79,566 on-time, what is the on-time rate (to 3 decimals), and what does the *complement* (≈20.4%) mean for Week 3's classification problem? *(see Concepts §6, Step 3)*

10. **Short answer.** Why does the cleaning workflow need to be a **re-runnable recipe with a gate**, rather than a one-off script? *(see Concepts §5 to 6)*

## Answer key

1. **b.** The generator plants ~0.2% duplicate rows (200 of 100,200); `drop_duplicates()` removes them, leaving 100,000. The defensive drops (non-positive weight, bad transit) remove 0 rows because those defects are not present.

2. **Weight varies by cargo type**, so a per-commodity median is a more honest estimate than one global number; the notebook uses `groupby("commodity")["weight_kg"].transform("median")`. The habit (impute within groups) matters even when the medians happen to be close.

3. **c.** Casting the boolean to `INT` (0/1) and averaging yields the fraction on time: `AVG(CAST(is_on_time AS INT))` → ≈0.7957. Options a, b, d do not compute a rate.

4. **`GROUP BY` collapses rows into one row per group** and reduces them (count/avg/sum). **A window function computes a value across a group while keeping every original row**, e.g. ranking each carrier within its month.

5. **b.** `RANK() OVER (PARTITION BY month ORDER BY on_time_rate DESC)` assigns a per-month rank; `QUALIFY rnk <= 2` keeps only ranks 1 to 2, the top two carriers *within each month*.

6. Any three of: no duplicate rows; no `NaN` `weight_kg`; all weights positive; no `NaN` `delay_hours`; no `NaN` `is_on_time`; `value_usd` non-negative; `carrier_id`/`lane_id` referential integrity; `is_on_time` boolean; `delay_hours` in `[-48, 240]`; arrival after departure; lanes have no `NaN` distance. Each guards one invariant the "silver" contract requires.

7. **b.** Referential integrity means every foreign-key value (`carrier_id`, `lane_id`) points to a real master record; the `isin(carriers["carrier_id"])` / `isin(lanes["lane_id"])` checks enforce it.

8. **b.** `con.register` binds the in-memory DataFrame to a table name so SQL `FROM shipments` works with no file or server; the data stays in memory.

9. **0.796** (79.6%). The complement is the **late share ≈ 20.4%**, which means Week 3's "on-time vs late" target is imbalanced, a classifier that always says "on time" would be ~79.6% accurate while missing every late shipment, so accuracy is banned as the headline metric.

10. **Data keeps arriving**, so a one-off fix decays into a dirty table on the next batch. A recipe + gate (the 12-check suite) lets anyone re-run `raw → silver` and *prove* the result is clean; a check that can't be re-run is a hope, not an artifact.
