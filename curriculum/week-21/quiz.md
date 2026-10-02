# Week 21: Quiz (10 questions, 8/10 to pass)

Answer each, then check against the answer key. Each question ends with a pointer
to the Concepts section (§) or notebook cell it tests.

1. **(MCQ)** In Unity Catalog's three-level namespace `catalog.schema.object`, which
   of the following is a valid *object* type? (see Concepts §UC is governance)

   - A) metastore
   - B) volume
   - C) workspace
   - D) compute plane

2. **(MCQ)** You run `VACUUM` on a Delta table with default settings, then try
   `SELECT * FROM tbl TIMESTAMP AS OF '30 days ago'`. What happens? (see Concepts §Delta gives time travel)

   - A) It always works, VACUUM only compacts files
   - B) It fails, because data files older than 7 days were permanently deleted
   - C) It returns an empty table but no error
   - D) It returns an error only if the table is partitioned

3. **(Short answer)** Why is a Unity Catalog privilege model described as
   "additive-only," and what are the *two* privilege kinds a principal needs to read
   `zrl_.silver.shipments`? (see Concepts §privilege model)

4. **(MCQ)** In notebook `02-medallion-sql.ipynb`, the silver query dedupes with
   `ROW_NUMBER() OVER (PARTITION BY shipment_id ORDER BY planned_departure)` and
   keeps `WHERE rn = 1`. What would break if you partitioned by `carrier_id`
   instead? (see Concepts §medallion; notebook 02 cell 4)

   - A) Nothing, carrier_id is also unique per row
   - B) Distinct shipments from the same carrier would be collapsed
   - C) The imputation would stop working
   - D) Time travel would fail

5. **(MCQ)** Which statement about managed vs. external tables is correct? (see Concepts §Unity Catalog)

   - A) `DROP TABLE` deletes data for both
   - B) `DROP TABLE` deletes data only for managed tables
   - C) External tables cannot be Delta
   - D) Managed tables require a `LOCATION` clause

6. **(Short answer)** Notebook `01-unity-catalog-and-delta-lab.ipynb` ends by
   printing `bronze rows` and `time-travel versions`. Explain why the
   `time_travel_demo` table has exactly **2** versions after the lab runs. (see
   Notebook walkthrough; notebook 01 cells 9 to 12)

7. **(MCQ)** You want a filter column (`carrier_id`) to enable data skipping but you
   anticipate re-keying the layout later. Which feature should you use on a new
   table? (see Concepts §Delta gives time travel)

   - A) Hive partitioning
   - B) `ZORDER BY` only
   - C) Liquid clustering (`CLUSTER BY`)
   - D) `OPTIMIZE` only

8. **(Short answer)** In the worked GRANT example, why must `zrl_analysts` receive
   `USE CATALOG ON CATALOG zrl_` *and* `USE SCHEMA` *and* `SELECT` rather than just
   `SELECT` on the table? (see Concepts §privilege model)

9. **(MCQ)** The notebook `%sql` cell
   `CREATE OR REPLACE TABLE shipments_bronze AS SELECT * FROM read_files('/Volumes/zrl_/zorologistics/raw/shipments.csv', format => 'csv', header => true, inferSchema => true)`
   produces a Delta table because… (see Notebook walkthrough)

   - A) `read_files` only outputs Delta
   - B) Delta is the default table format on Databricks unless you say otherwise
   - C) the CSV was already converted by the generator
   - D) it is a streaming table

10. **(MCQ)** Which of the following is a *consequence* of liquid clustering rather
    than Hive partitioning? (see Concepts §Delta gives time travel)

   - A) You can change clustering keys without rewriting the table
   - B) It makes time travel impossible
   - C) It requires enabling deletion vectors
   - D) It is incompatible with `VACUUM`

## Answer key

1. **B: volume.** A volume is a governed object at the `catalog.schema.object`
   level; the metastore is the registry *above* the catalog, and workspace/compute
   plane are platform concepts, not UC objects.

2. **B: it fails.** VACUUM permanently removes data files older than the retention
   window (default 7 days), so time travel past that window is impossible.

3. **Additive-only means there is no `DENY`**: a principal can only *gain*
   privileges, and the default is "nothing." To read the table a principal needs
   **traversal** (`USE CATALOG zrl_` + `USE SCHEMA silver`) **and action** (`SELECT`
   on the table). Both kinds are required.

4. **B.** Partitioning by `carrier_id` and keeping one row per partition would
   collapse all of a carrier's distinct shipments into one; `shipment_id` is the
   natural key that must stay unique.

5. **B.** `DROP TABLE` deletes data only for managed tables; external tables drop
   metadata only (the data stays in your storage).

6. **Two versions = the `CREATE OR REPLACE` (version 1, 1,000 rows) and the
   `INSERT` (version 2, another 1,000 rows).** Each write appends a new transaction
   log entry, so `DESCRIBE HISTORY` shows exactly two versions, and `VERSION AS OF
   1` reads the 1,000-row state while current reads 2,000.

7. **C: liquid clustering.** `CLUSTER BY` colocates data for skipping *and* lets you
   change keys without a rewrite; `ZORDER BY` alone cannot be re-keyed without
   rewriting.

8. **Privileges inherit down, but traversal and action are separate.** `SELECT` on a
   table is not enough by itself, the principal must first *reach* the container
   with `USE CATALOG` and `USE SCHEMA`. UC requires the traversal chain plus the
   action; a bare `SELECT` grant without `USE` grants on the parents would not
   permit the read.

9. **B.** Delta is the default storage layer, every table created on Databricks is a
   Delta table unless configured otherwise, so `CREATE … AS SELECT FROM read_files`
   lands as a governed Delta table.

10. **A.** Liquid clustering's headline benefit over Hive partitioning/Z-order is
    that you can change the clustering keys without rewriting the table.
