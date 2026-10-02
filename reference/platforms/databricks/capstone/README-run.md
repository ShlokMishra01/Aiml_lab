# Capstone: Run Instructions

> Part of AI Engineering Lab · Developed by Zorost Intelligence AI Lab · [zorost.com](https://zorost.com)

Step-by-step runbook to reproduce the ZoroLogistics Lakehouse Intelligence bundle from a
clean checkout. Goal: `validate` → `deploy` → `run` → verify the three tables.

---

## 0. Prerequisites

- A Databricks workspace (free trial is fine; serverless pipelines need a serverless-capable
  region).
- The **Databricks CLI** (unified, ≥ v0.281 recommended), `databricks --version`.
- The **Week-01 `shipments.csv`** (generate locally with
  `python -c "from zoro import data; data.save_all('data', seed=42)"`).

## 1. Authenticate (OAuth U2M)

Create a CLI profile for the bundle's `dev` target (`zrl-dev`):

```bash
databricks auth login --profile zrl-dev --host https://<your-workspace-host>
```

This opens a browser OAuth (U2M) flow and stores the profile in `~/.databrickscfg`. Confirm:

```bash
databricks auth env --profile zrl-dev   # prints DATABRICKS_HOST / DATABRICKS_TOKEN
```

> **CI note:** for automation (GitHub Actions), use OAuth **M2M** (service principal) or OIDC
> federation instead of U2M, see [`../15-dabs-ci-cd.md`](../15-dabs-ci-cd.md).

## 2. Create catalog, schema, and volume; upload the CSV

The pipeline expects a Unity Catalog volume at `/Volumes/zrl_/zorologistics/raw/`.

```bash
# Catalog + schema + managed volume (idempotent; errors if they already exist are fine)
databricks catalogs create --json '{"name": "zrl_"}' --profile zrl-dev
databricks schemas create --json '{"name": "zorologistics", "catalog_name": "zrl_"}' --profile zrl-dev
databricks volumes create --json '{
  "catalog_name": "zrl_",
  "schema_name": "zorologistics",
  "name": "raw",
  "volume_type": "MANAGED"
}' --profile zrl-dev
```

Upload the CSV (note the `dbfs:` prefix is required even for volume paths):

```bash
databricks fs cp data/shipments.csv \
  dbfs:/Volumes/zrl_/zorologistics/raw/shipments.csv \
  --profile zrl-dev --overwrite
```

Verify it landed:

```bash
databricks fs ls dbfs:/Volumes/zrl_/zorologistics/raw/ --profile zrl-dev
```

> **Where the CSV lives:** `data/shipments.csv` is the Week-01 generator output
> (`zoro.data.save_all`). If you changed the dev target's catalog, update the volume path in
> `src/pipeline.sql` (`/Volumes/<catalog>/zorologistics/raw/`) to match.

## 3. Validate and deploy the bundle

```bash
cd capstone

# Validate strictly (warnings become errors)
databricks bundle validate --strict -t dev --profile zrl-dev

# Deploy: creates/updates the pipeline + job in the workspace
databricks bundle deploy -t dev --profile zrl-dev

# See what's deployed where
databricks bundle summary --profile zrl-dev
```

`validate --strict` exiting 0 is **Gate G1**.

## 4. Run the pipeline

```bash
# Runs the ETL job (which runs the pipeline)
databricks bundle run etl_job -t dev --profile zrl-dev
```

`bundle run` blocks and streams the run result. To watch a pipeline update directly:

```bash
databricks pipelines list-pipeline-events $(databricks bundle summary --profile zrl-dev -o json | jq -r '.resources.pipelines.medallion.id') --profile zrl-dev
```

(Or open the pipeline in the UI → **Pipelines** → "ZoroLogistics Medallion".) The first
serverless update cold-starts for a few minutes, do not kill it.

## 5. Verify the tables (Gate G3)

Query from a SQL warehouse or notebook:

```sql
USE CATALOG zrl_;
USE SCHEMA zorologistics;

SELECT 'bronze' AS layer, COUNT(*) AS rows FROM bronze_shipments
UNION ALL SELECT 'silver', COUNT(*) FROM silver_shipments
UNION ALL SELECT 'gold',   COUNT(*) FROM gold_on_time_kpis;

-- Silver should be ≤ bronze (duplicates + bad rows dropped by expectations)
-- Gold aggregates by carrier + month:
SELECT * FROM gold_on_time_kpis ORDER BY on_time_pct DESC LIMIT 10;
```

Expectation metrics (how many rows each constraint dropped) are visible in the pipeline
update's **data quality** panel, confirm the `DROP ROW` constraints fired on the planted
null `weight_kg` rows (**Gate G2**).

## 6. Continue the capstone

With G1 to G3 green, the remaining gates build on these tables:

- **G4 to G5**: train the ETA model from `silver_shipments` (point-in-time features), register
  in UC, serve as `zrl-eta-model`, add a gateway rate limit (`../10-model-serving.md`).
- **G6**: index `policy_chunks` in AI Search and build the RAG chain (`../11-vector-search-rag.md`).
- **G7 to G8**: Genie space + on-time AI/BI dashboard on `gold_on_time_kpis`.
- **G9 to G10**: governance (mask/filter/audit) and FinOps (`../16-...`, `../17-...`).

Uncomment the `dashboards` resource in `databricks.yml` and re-deploy once you export
`src/dashboards/ontime.lvdash.json` from the AI/BI editor.

## 7. Tear down

```bash
databricks bundle destroy -t dev --profile zrl-dev   # removes bundle-deployed resources
```

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `cannot configure default credentials` | Pass `--profile zrl-dev` or run `databricks auth login` first |
| Pipeline stuck `INITIALIZING` | Normal serverless cold start, wait a few minutes |
| `Cannot create streaming table from batch query` | The bronze source must be `STREAM read_files(...)` (with `STREAM`) |
| Bronze has 0 rows | Volume path mismatch, check `databricks fs ls dbfs:/Volumes/zrl_/zorologistics/raw/` |
| `PERMISSION_DENIED` on volume | Grant yourself `READ VOLUME` / `WRITE VOLUME` on the volume |
| `bundle validate` fails on a path | `resources/` files use `../src`, `databricks.yml` uses `./src` |

---

## Sources

- Declarative Automation Bundles: https://docs.databricks.com/dev-tools/bundles/
- Databricks CLI (auth, volumes, fs): https://docs.databricks.com/dev-tools/cli/
- Unity Catalog volumes: https://docs.databricks.com/volumes/
- Lakeflow Pipelines (DLT): https://docs.databricks.com/ldp/

> *Original AI Engineering Lab writing; CLI flags and bundle schema change, run
> `databricks bundle validate --strict --debug` and check `https://docs.databricks.com/llms.txt`.*

---

© 2026 Zorost Intelligence LLC · [zorost.com](https://zorost.com)
