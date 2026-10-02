# Databricks for AI Engineering: Zero to Hero Deep Dive

> **Purpose:** This is the backbone reference for the AI Engineering Lab **Databricks zero-to-hero** module. It spans platform fundamentals → compute → data → SQL → Spark/pipelines → MLOps → GenAI → governance → cost → certification → how Zorost's Databricks Modernization Practice maps to it all.
>
> **Scope & provenance:** Facts are synthesized in original wording from official documentation (`docs.databricks.com`) and `databricks.com`, verified against the live docs as of **August 2026**. Databricks has renamed many products recently; every rename is flagged inline and consolidated in the quick-reference below. **Always teach the current name and note the legacy name.**
>
> **Source of truth for further lookup:** the machine-readable docs index at `https://docs.databricks.com/llms.txt`.

---

## 0. Naming quick-reference (current → formerly)

Databricks shipped a wave of renames through 2024 to 2026. The most important ones for a zero-to-hero learner:

| Current name | Formerly known as | Notes |
|---|---|---|
| **Lakeflow Pipelines** | Delta Live Tables (DLT) | Built on the open-source **Apache Spark Declarative Pipelines (SDP)**; Python module `dlt` → `pyspark.pipelines` (import as `dp`) |
| **Lakeflow Jobs** | Workflows / Jobs | Sidebar entry is now "Jobs & Pipelines" |
| **Lakeflow Connect** | Databricks Ingest / Ingestion | Managed + standard connectors for SaaS/databases/files/streams |
| **Declarative Automation Bundles (DABs)** | Databricks Asset Bundles | Still abbreviated "DABs" |
| **OpenSharing** | Delta Sharing | Open project now at `opensharing.io` |
| **AI Search** | Vector Search | Managed vector retrieval |
| **Unity AI Gateway** | AI Gateway | Governance control plane for LLM/agent/MCP traffic |
| **Genie Agents** | Genie Spaces | Natural-language data Q&A configured by analysts |
| **Genie One** | Databricks One | Simplified business-user UI |
| **AI/BI dashboards** | Lakeview dashboards | Legacy "DBSQL dashboards" are archived |
| **Data quality monitoring** | Lakehouse Monitoring | Anomaly detection + data profiling |
| **SQL warehouses** | SQL endpoints | Renamed 2023 |
| **Models in Unity Catalog** | MLflow Model Registry | Registry "stages" → movable **aliases** (`@prod`, `Champion`/`Challenger`) |
| **Git folders** | Repos | Built-in Git client |
| **Databricks AI assistive features** | DatabricksIQ | The AI-engine brand was folded into the Genie family |
| **Standard / Dedicated access mode** | Shared / Single-user access mode | Compute access modes |
| `APPLY CHANGES` (CDC) | n/a | Superseded by **`AUTO CDC`** (same syntax) |
| `Trigger.Once` | n/a | Superseded by **`Trigger.AvailableNow`** |

The **"Mosaic AI"** prefix has largely been retired across the docs (e.g., "Mosaic AI Model Serving" → "Model Serving", "Mosaic AI Model Training" → "Databricks Model Training"), though it still appears in some marketing material.

---

## 1. Platform fundamentals

### 1.1 The Data Intelligence Platform

Databricks is a unified, open analytics platform for building, deploying, and governing data, analytics, and AI. It runs **inside your cloud account** (integrating with your cloud storage and security) while Databricks manages the infrastructure on your behalf. Databricks layers **AI on top of the lakehouse** to understand data semantics and automatically optimize performance and infrastructure.

Two conceptual planes define the architecture:

| Plane | What runs there | Where it lives |
|---|---|---|
| **Control plane** | Backend services, web UI, identity, job scheduling, workspace metadata | Databricks-managed (in the Databricks account) |
| **Compute plane** | Actual data processing (Spark executors, SQL engines) | Two variants: **classic** (your AWS/Azure/GCP account) and **serverless** (Databricks-managed) |

- **Classic compute** runs in *your* virtual network → natural network isolation and control (customer-managed VPCs).
- **Serverless compute** runs in a Databricks-managed **serverless compute plane**, created in the same region, inside a network boundary that isolates customer workspaces.
- Workspaces have **workspace storage** (notebooks/queries/dashboards + internal "system data"). **DBFS root / DBFS mounts are a deprecated legacy pattern**, Databricks recommends Unity Catalog for all data access.

### 1.2 Lakehouse

The [data lakehouse](https://docs.databricks.com/lakehouse/) combines data-lake economics (cheap open-format storage of any data) with warehouse governance/performance, on standard cloud object storage. Three pillars plus Spark:

- **Apache Spark**: massively scalable engine with decoupled compute and storage.
- **Delta Lake**: optimized storage layer (ACID, schema enforcement/evolution, time travel).
- **Unity Catalog**: unified fine-grained governance (access control, lineage, audit, discovery).

A common implementation pattern is the **medallion architecture** (bronze → silver → gold), covered in §3.

### 1.3 Accounts vs. workspaces

- A **workspace** is a single Databricks deployment, where your team works with notebooks, jobs, clusters, SQL warehouses, and data.
- A **Databricks account** is the top-level entity containing **multiple workspaces**. At account level you manage identity (users/groups/service principals, SSO/SCIM), workspace creation across regions, **Unity Catalog metastores**, and billing.
- The **account console** (`accounts.cloud.databricks.com`) is where account admins configure account settings, subscription/billing, serverless quotas, and workspaces.

Two workspace deployment types:

| Type | Description |
|---|---|
| **Serverless workspace** | Pre-configured serverless compute + Databricks-managed default storage; can still attach your own cloud storage. Best for Genie One, AI/BI dashboards, Apps, serverless pipelines, most AI features. |
| **Classic workspace** | Storage + compute in your own cloud account. Needed for legacy Spark RDD code, Scala/R-first teams, direct on-prem/private connectivity. Serverless is still available inside classic workspaces. |

**Metastore ↔ region:** an account can hold multiple **Unity Catalog metastores**; a single metastore can attach to **multiple workspaces in the same region**, giving them the same governed view.

### 1.4 Regions & clouds

Workspaces run on **AWS, Azure, and Google Cloud**, each with its own supported-region list. Not every feature is available in every region (see "Features with limited regional availability"). Some features ("**Designated Services**") use **Databricks Geos**, groups of regions giving predictable data-residency guarantees.

### 1.5 Unity Catalog core object model

Unity Catalog (UC) is the unified governance layer for **data and AI**, automatically enabled for all workspaces created after Nov 8, 2023, and also available as an open-source project. Objects use a **three-level namespace**:

```
metastore
 └── catalog
      └── schema (database)
           ├── table | view | volume | function | model
```

| Object | Purpose |
|---|---|
| **Metastore** | Account-level metadata registry; one can attach to many workspaces in a region |
| **Catalog** | Top-level container for isolating/organizing data |
| **Schema** (database) | Holds tables, views, volumes, functions, models |
| **Table** | Governs tabular data (Delta by default) |
| **View** | Saved query (incl. materialized views, dynamic views) |
| **Volume** | Governs non-tabular data (files) |
| **Function / Model** | UDFs and MLflow-packaged models, also governed securables |

Other UC securables sit directly under the metastore: **storage credentials**, **external locations**, **connections**, and **shares** (OpenSharing).

**Managed vs. external vs. foreign tables:**

| | Managed | External | Foreign |
|---|---|---|---|
| Data lifecycle | UC manages | You manage | External system manages |
| Storage | UC-managed | You specify | External system |
| `DROP TABLE` deletes data? | Yes | No (metadata only) | No |
| Formats | Delta, Apache Iceberg | Delta (rec.), CSV/JSON/Avro/Parquet/ORC/Text | System-dependent |
| Best for | Production (default, recommended) | Existing data / external clients | Migration / temporary federation |

Legacy **Hive metastore** (and Hive tables, DBFS root) remains only for backward compatibility, migrate to UC.

### 1.6 OpenSharing (formerly Delta Sharing)

**OpenSharing** securely shares **live** data and AI assets outside your organization, whether or not recipients use Databricks. Core concepts: a **share** (read-only collection of tables, and for Databricks recipients, views/volumes/models/notebooks), a **provider**, and a **recipient**. Two protocols:

1. **Databricks-to-Databricks**: between UC-enabled workspaces (no bearer token; full governance/audit).
2. **Databricks-to-Open**: to any platform (Spark, pandas, Power BI…) via bearer tokens or OIDC federation.

Adjacent sharing features: **Databricks Marketplace** (data-product exchange) and **Clean Rooms** (privacy-preserving collaboration).

### 1.7 Personas

| Persona | Goal | Tools |
|---|---|---|
| **Data engineer** | Reliable, governed ETL/ELT | Lakeflow Pipelines, Lakeflow Jobs, Auto Loader, Lakeflow Connect, Spark/Structured Streaming, DABs |
| **Data analyst / BI** | Query & visualize curated data | SQL warehouses, SQL editor, AI/BI dashboards, Genie, Catalog Explorer, alerts |
| **Data scientist / ML engineer** | Train/track/deploy models | DBR ML, MLflow (experiments + Models in UC), Feature Store, Model Serving, AI Playground, AutoML |
| **Administrator** | Govern platform, identity, compute, cost | Account console, workspace settings, Unity Catalog, compute policies, instance pools, budgets, system tables |

Admin roles split into **account admin** (whole account), **workspace admin** (single workspace), and **feature-specific roles** (Metastore admin, Billing admin, Marketplace admin).

---

## 2. Compute

Three broad families: **serverless** (on-demand, auto-managed), **classic** (provisioned all-purpose/job clusters), and **SQL warehouses** (analytics-optimized).

### 2.1 All-purpose vs. job clusters

| | All-purpose (interactive) | Job cluster |
|---|---|---|
| Created by | User (UI/CLI/API) | Job scheduler, per run |
| Lifecycle | Manual terminate/restart; shared | Created when job runs, terminated when done; cannot restart |
| Use | Interactive notebooks, ad-hoc analysis | Scheduled/automated production |
| Billing | "Interactive" workload | "Automated/job" workload, cheaper per DBU |

### 2.2 Cluster config essentials

- **Databricks Runtime (DBR)**: Spark + Databricks optimizations. Variants: standard, **DBR for ML** (ML/DL libraries + GPU), and **Long-Term Support (LTS)** (recommended for production).
- **Driver + worker nodes**: one driver, zero or more workers (one executor each). Pick instance types per node, or **fleet types** that auto-resolve. **Single-node** runs Spark locally on the driver.
- **Photon**: Databricks' native C++ vectorized query engine (default on SQL warehouses and serverless; default-on classic DBR 9.1 LTS+). Billed at a different DBU rate.
- **Access modes**: `Standard` (shared, recommended) vs. `Dedicated` (single user/group).

### 2.3 Cluster policies

A **compute policy** is a set of rules admins use to **limit what users can configure**: fix/hide settings, limit cluster count, **cap cost (max DBU/hour)**, enforce library installs and **tags** for cost attribution. Policies inherit from **policy families**; admins can enforce compliance on existing clusters. Without the "unrestricted cluster creation" entitlement, users can only create compute via policies.

### 2.4 Autoscaling

- **Optimized autoscaling** (Premium+): scales up in ≤2 events; down based on shuffle state + utilization windows.
- **Standard autoscaling** (Standard plan): adds 8 nodes then grows exponentially; down after 10 min low activity.
- Do **not** enable Spark Dynamic Allocation alongside Databricks autoscaling (conflicts cause churn/`NODES_LOST`).
- **Serverless** scales automatically and transparently.

### 2.5 Serverless compute

Databricks-managed on-demand compute for **notebooks, jobs, and Lakeflow Pipelines**. No compute in your cloud account; "**versionless**" (always latest runtime, auto-upgraded); billed under serverless SKUs. Separate serverless infrastructure powers SQL warehouses, Model Serving, data quality monitoring, and predictive optimization. Serverless notebooks have a default **2.5 h** execution timeout (overspend protection).

### 2.6 SQL warehouses

| Type | Compute | Photon | Predictive I/O | IWM | Startup |
|---|---|---|---|---|---|
| **Serverless** | Databricks | ✓ | ✓ | ✓ (AI autoscaling) | ~2 to 6 s |
| **Pro** | Your cloud | ✓ | ✓ | n/a | ~4 min |
| **Classic** | Your cloud | ✓ | n/a | n/a | ~4 min |
| **Lakehouse Real-Time (Beta)** | Serverless | ✓ | n/a | n/a | sub-second reads |

- **Intelligent Workload Management (IWM)** predicts resource needs and dynamically scales serverless warehouses.
- Classic/pro scale ~1 cluster per 10 concurrent queries; serverless autoscales clusters of a chosen size.
- **Auto Stop** default **10 min** idle (min 5 via UI, 1 via API); idle still accrues DBUs.
- **Channels**: **Current** (production) and **Preview** (test upcoming versions).

### 2.7 DBU pricing

A **DBU (Databricks Unit)** is a unit of *processing capability per hour, based on the VM instance type*. Billing is **pay-as-you-go at per-second granularity**; **Committed Use Contracts** give discounts. Rates vary by **SKU (workload), cloud, and region**; Photon instances bill differently.

| SKU tier | Applies to |
|---|---|
| **Jobs Compute** | Automated/job workloads (also a "Jobs Light" variant) |
| **All-Purpose Compute** | Interactive/notebook workloads (higher rate) |
| **SQL** | Databricks SQL warehouses (`CLASSIC`/`PRO`; serverless billed separately) |
| **Serverless** | Serverless jobs, notebooks, Lakeflow Pipelines |

Other billed products (tracked in `system.billing.usage` by `billing_origin_product`): Lakeflow Pipelines (DLT `CORE/PRO/ADVANCED`), Model Serving, AI Search, Unity AI Gateway, Lakeflow Connect, AI Functions, Lakebase, etc.

### 2.8 Cost controls

- **Budgets & alerts** (account-wide or filtered by team/project/workspace).
- **Cluster auto-termination** (10 to 10,000 min inactivity) and **SQL warehouse auto-stop**.
- **Spot instances** for latency-tolerant workers (driver always on-demand).
- **Instance pools**: pre-warmed idle instances (pay cloud cost, **no DBUs** while idle) for faster start/scale.
- **Compute policies + tags** for cost caps and chargeback.

---

## 3. Data & Delta Lake

### 3.1 Delta Lake fundamentals

Delta Lake is the **default storage layer**; unless configured otherwise, **all tables on Databricks are Delta tables**. It extends Parquet with a file-based **transaction log** providing ACID transactions and scalable metadata, fully compatible with Spark (incl. Structured Streaming, one copy of data for batch + streaming).

**ACID:** each SQL statement is its own atomic transaction; multi-statement transactions via `BEGIN ATOMIC … END`. Concurrency uses **optimistic concurrency control**; reads get **snapshot isolation**, writes get **write-serializable** isolation. PK/FK constraints are **informational only** (not enforced).

**Schema enforcement & evolution:** writes are validated against the schema (safe casts attempted); schemas can evolve via `ALTER TABLE` (add/reorder/rename/type-widening) or implicitly (`mergeSchema` / `spark.databricks.delta.schema.autoMerge.enabled`).

**Time travel:** every write creates a new table version. Query a prior state with `VERSION AS OF` / `TIMESTAMP AS OF` or `@`-syntax; `RESTORE TABLE` rolls back. Retention: `logRetentionDuration` (default 30 days), `deletedFileRetentionDuration` (default 7 days).

**VACUUM:** permanently removes data files older than the retention threshold (default 7 days). `DRY RUN` previews; `VACUUM … LITE` (DBR 16.4 LTS+) is a faster log-based variant. After VACUUM, time travel past the retention window is impossible. Soft-deletes (deletion vectors / dropped columns) are physically applied with `REORG TABLE … APPLY (PURGE)` first.

**OPTIMIZE + Z-ORDER:** `OPTIMIZE` compacts/bin-packs files; `ZORDER BY (col)` colocates related data for data-skipping on high-cardinality filter columns. **Z-order and Hive partitioning are now superseded by liquid clustering.**

**Liquid clustering:** `CLUSTER BY (cols)` automatically organizes data and lets you **change keys without rewriting**. GA for Delta on DBR 15.4 LTS+; `CLUSTER BY AUTO` (automatic) lets Databricks adapt keys from workload. Recommended for all new tables.

**Deletion vectors:** mark rows deleted in metadata instead of rewriting the whole Parquet file (accelerates DELETE/UPDATE/MERGE). Enable with `delta.enableDeletionVectors = true`; reads DBR 12.2 LTS+; all-optimized writes DBR 14.3 LTS+. Iceberg **v3** tables include them by default.

**Change data feed (CDC):** tracks row-level changes between versions (`table_changes()` / `readChangeFeed`; metadata `_change_type`, `_commit_version`, `_commit_timestamp`). Two approaches: **Automatic CDF** (Public Preview, DBR 18 LTS+; computed at query time) and **legacy CDF** (materialized at write; `delta.enableChangeDataFeed = true`).

### 3.2 Medallion architecture

A progressive data-quality pattern (recommended best practice, not a requirement):

| Layer | Purpose | Consumers |
|---|---|---|
| **Bronze (raw)** | Ingest raw, unvalidated data; append-only; preserve source fidelity (store as `STRING`/`VARIANT`/`BINARY`) | Data engineers, compliance/audit |
| **Silver (validated)** | Clean, dedupe, normalize, enforce schema, handle nulls/late data, joins | Data engineers, analysts, data scientists |
| **Gold (enriched)** | Aggregated, dimensional-modeled, business-aligned | BI, analysts, ML, executives |

### 3.3 Lakehouse Federation

Governed, **read-only** access to external data through UC **foreign catalogs**, with automatic query pushdown and table-level access control. Two variants: **query federation** (JDBC pushdown to databases like MySQL/PostgreSQL/Oracle/Snowflake/BigQuery…) and **catalog federation** (query external catalogs, Hive, AWS Glue, Snowflake Horizon, directly in object storage). Setup for query federation: UC **connection** (credentials + URL) → **foreign catalog** → grant privileges → query.

### 3.4 Lakeflow Connect (managed ingestion)

Connectors to ingest from enterprise apps, databases, cloud storage, message buses, and files, powered by serverless Lakeflow Pipelines and governed by UC. Layered from custom → managed:

- **Managed connectors** (fully managed): **SaaS** (Salesforce, Workday, ServiceNow, GA4, HubSpot, Confluence, NetSuite, Dynamics 365…), **database CDC** (SQL Server; PostgreSQL/MySQL CDC in preview; query-based Oracle/Teradata/Snowflake/Redshift/Synapse/BigQuery), **file sources** (SharePoint, Google Drive, SFTP…), **streaming** (Kafka, Kinesis, Pub/Sub, Pulsar).
- **Standard connectors** and **community/custom connectors** for more control.

**Rule of thumb:** Lakeflow Connect **copies** data into governed Delta tables; Lakehouse Federation **queries in place** without copying.

### 3.5 Volumes, Auto Loader, COPY INTO

- **Volumes** govern non-tabular data at `catalog.schema.volume`; access via `/Volumes/<catalog>/<schema>/<volume>/<path>`. **Managed** (UC-owned storage, 7-day delete retention) vs. **external** (existing object storage). Use for raw landing, staging, unstructured data, and library/checkpoint files.
- **Auto Loader** (`cloudFiles` source) incrementally processes new files with **exactly-once** semantics (RocksDB progress store in the checkpoint), schema inference/evolution, and two detection modes: **directory listing** (default) vs. **file notification** (recommended).
- **COPY INTO** idempotently/incrementally loads files into Delta via SQL. Use `COPY INTO` for thousands of files; **Auto Loader** for millions+ or evolving schemas.

---

## 4. Databricks SQL & AI/BI

### 4.1 Databricks SQL (DBSQL)

A cloud data warehouse on lakehouse architecture (ANSI SQL + Delta extensions): **SQL warehouses** (Serverless recommended / Pro / Classic), the **SQL editor** (Genie Code-assisted), saved **queries** (with "Run as viewer/owner" credential modes), **query history** (backed by `system.query.history`), and **alerts** (scheduled queries with conditions → email/Slack/webhooks; statuses `OK`/`TRIGGERED`/`ERROR`).

### 4.2 AI/BI dashboards & Genie

**AI/BI** is Databricks' compound-AI BI product: **dashboards**, **Genie Agents**, and **Unity Catalog semantics (metric views)**.

- **AI/BI dashboards** (formerly Lakeview dashboards): low-code AI-assisted dashboards with datasets, cross-filtering, custom calculations, scheduling/subscriptions, embedding, Git/source-control.
- **Legacy "DBSQL dashboards"** are **archived**, no new ones can be created; migrate via **"Clone a legacy dashboard to an AI/BI dashboard."**
- **Genie family**: **Genie Agents** (analyst-configured NL→SQL chat), **Genie One** (simplified business-user UI), **Genie Code** (developer AI assistant).

### 4.3 AI Functions (SQL)

Built-in SQL/PySpark functions that apply LLMs or Databricks research models to data in place, no endpoint/API key to manage. **Requirements (Aug 2026):** serverless compute required (not on Pro/Classic warehouses), Databricks Runtime **18.2+**.

| Function | What it does |
|---|---|
| `ai_query` | General-purpose: run a prompt against any supported Foundation Model API endpoint |
| `ai_classify` | Classify input text into labels you provide |
| `ai_extract` | Extract structured fields from documents/text using a schema you define |
| `ai_gen` | Free-form generation from a prompt |
| `ai_summarize` | Generate a concise summary (optional `max_words`) |
| `ai_mask` | Mask/redact specified entity types (PII) |
| `ai_similarity` | Semantic similarity score between two strings (0.0 to 1.0) |
| `ai_parse_document` | Parse unstructured documents (PDF/Office/images) into text, tables, figures, layout |
| `ai_prep_search` (Beta) | Transform parsed output into search-ready chunks for AI Search/RAG |
| `ai_fix_grammar` | Correct grammatical errors |
| `ai_analyze_sentiment` | Sentiment (positive/negative/neutral/mixed) |
| `ai_translate` | Translate to a target language |
| `ai_forecast` | Table-valued function forecasting time-series to a horizon (with bounds) |

Newer Beta additions beyond the core list: **`ai_search`** (ranked, deduplicated retrieval + grounded answer), **`ai_top_drivers`** (rank dimensions driving a metric change), and **`vector_search`** (query an AI Search index).

---

## 5. PySpark & pipelines

### 5.1 Spark DataFrame API essentials

PySpark's primary abstraction is the **DataFrame** (named columns, immutable). Key mental model, **lazy evaluation**:

- **Transformations** (select, filter, join, groupBy/agg, withColumn, orderBy, union) are **lazy**, they build a logical plan.
- **Actions** (show/display, count, take, collect, saveAsTable) trigger execution.
- In production, **the write is usually the only action**; extra actions interrupt optimization.

**Reading** (`spark.read`): `.format()`, `.option()`, `.schema()`, then `.load(path)` / `.table(name)`. **Writing** (`df.write`): `.mode("append"|"overwrite"|"error"|"ignore")`, `.saveAsTable()` / `.save()`. Formats: Delta, Parquet, CSV, JSON, Avro, ORC, XML, text, Excel, streaming connectors.

**Common transformations:**

| Op | Example |
|---|---|
| select / filter | `df.select("id").filter(col("amount") > 0)` |
| withColumn | `df.withColumn("total", col("qty") * col("price"))` |
| join | `df.join(dim, "id", "inner")` (inner/left/right/full/semi/anti) |
| groupBy/agg | `df.groupBy("state").agg(sum("amount").alias("sales"))` |
| distinct | `df.dropDuplicates(["id"])` |
| orderBy | `df.orderBy(col("amount").desc())` |

**Window functions** (`pyspark.sql.Window` with `partitionBy()`/`orderBy()`) compute across related rows without collapsing (e.g., `row_number()` for "latest per customer").

**Caching:** the automatic **disk cache** (Databricks-managed Parquet cache, no code needed) is distinct from manual Spark `cache()`/`persist()`.

**Broadcast joins:** copy the small side to all executors. AQE auto-converts joins to broadcast; hint with `df.join(F.broadcast(small_df), "key")`.

**Partitioning:** `spark.sql.shuffle.partitions` sets post-shuffle partitions (tune to 1 to 2× executor cores); `repartition(n)` reshuffles, `coalesce(n)` reduces without full shuffle; AQE coalesces automatically.

**Spark SQL:** `df.createOrReplaceTempView("t")` then `spark.sql("SELECT …")`.

### 5.2 Structured Streaming

Near-real-time engine with end-to-end fault tolerance and **exactly-once** guarantees, using the same DataFrame API as batch.

- **Sources:** Auto Loader (`cloudFiles`), Kafka, Delta change streams, Kinesis/Pub/Sub/Pulsar.
- **Sinks:** Delta (`toTable`), Kafka, files, console/memory, `foreachBatch` (arbitrary per-micro-batch logic, e.g. `MERGE` upserts).
- **Output modes** (stateful queries only): **Append** (default, emit only final rows), **Update** (rows that changed), **Complete** (full result). Delta sinks support append/complete, **not** update.
- **Triggers:** unspecified (~3 to 5 s), `processingTime`, **`availableNow`** (one-shot incremental; replaces `Trigger.Once`), **real-time mode** (sub-second, Public Preview). Serverless supports `AvailableNow`/`Once` only.
- **Watermarks** (`withWatermark("ts", "10 minutes")`) bound state and drop late data; windows: **tumbling**, **sliding**, **session**. Watermarks are **mandatory** for stream-stream outer joins; recommended for inner joins and dedup.
- **Checkpoints** store offsets, commits, state, and metadata for exactly-once resume, **each query needs its own checkpoint location** (use a UC volume path).
- **Stateful ops:** streaming aggregations, `distinct`/`dropDuplicates`, stream-stream joins, custom state (`mapGroupsWithState`, `transformWithState`). Databricks recommends the **RocksDB state store** with changelog checkpointing.

### 5.3 Lakeflow Pipelines (formerly Delta Live Tables)

Declarative batch + streaming pipelines in SQL or Python, with automatic orchestration (correct order, max parallelism, progressive retry).

**Dataset types:**

| Type | Semantics | Use when |
|---|---|---|
| **Streaming table** | Each record processed once; incremental; append-only source | Streaming ingestion |
| **Materialized view** | Recomputed to reflect current state ("always correct") | Aggregations/joins; dimension changes |
| **View** | Evaluated on demand, not persisted | Intermediate checks |

Streaming tables don't recompute on late dimension changes; materialized views do. All pipeline tables are Delta tables with ACID/time travel.

**SQL** (`STREAM`/`read_files` for streaming; `CREATE OR REFRESH … MATERIALIZED VIEW` for batch; `CREATE PRIVATE …` for pipeline-private views). **Python** uses `from pyspark import pipelines as dp` with `@dp.table`, `@dp.materialized_view`, `@dp.temporary_view` decorators (dataset functions must return a DataFrame and must **not** call actions like `collect()`/`count()`/`toPandas()`/`save()`).

**Expectations (data quality):** boolean constraints with three actions, **warn** (default; keep rows, record metrics), **drop** (`ON VIOLATION DROP ROW`), **fail** (`ON VIOLATION FAIL UPDATE`).

**CDC:** `AUTO CDC` (replaces `APPLY CHANGES`) computes **SCD Type 1** (latest only) or **Type 2** (versioned history with `__START_AT`/`__END_AT`) from a CDC feed.

**Medallion in pipelines:** bronze (Auto Loader → streaming table) → silver (expectations + joins) → gold (materialized views), with the DAG resolved automatically.

### 5.4 Lakeflow Jobs (formerly Workflows)

Workflow orchestration: a **job** schedules/coordinates **tasks** as a **DAG**.

**Task types:** Notebook, Python script, Python wheel, SQL (query/file/dashboard/alert), dbt, **Pipeline** (Lakeflow Pipeline), JAR, Run Job, **If/else** (conditional), **For each** (loop), and more.

**DAG orchestration:** `depends_on` relationships with **Run if** gating, `ALL_SUCCESS` (default), `AT_LEAST_ONE_SUCCESS`, `NONE_FAILED`, `ALL_DONE`, `AT_LEAST_ONE_FAILED`, `ALL_FAILED`.

**Parameters:** job-level parameters pushed to tasks via `{{job.parameters.<name>}}`; notebooks read `dbutils.widgets.get()`.

**Scheduling:** triggers include **Scheduled** (cron), **Periodic**, **File arrival**, **Table update**, **Continuous**. Min 10 s between runs.

**Resilience:** per-task **retries**, **repair** (re-run failed tasks), per-task **timeout**.

**Compute:** **job clusters** (reused across tasks; recommended), existing/all-purpose clusters, or **serverless** (omit cluster config).

---

## 6. MLOps & machine learning

Databricks' ML stack: **MLflow** (tracking + registry + GenAI eval) → **Models in Unity Catalog** → **Feature Engineering** → **Model Training** → batch (Spark UDF) or real-time (Model Serving), all governed by UC.

### 6.1 MLflow

Experiments → runs → models. Two logging mechanisms: **autologging** (`mlflow.<flavor>.autolog()`) or the explicit **logging API** (`log_param`/`log_metric`/`log_artifact`/`log_model`). MLflow 3 adds GenAI observability/evaluation/prompt management, **Logged Models**, and **Deployment Jobs**; in MLflow 3 the default registry is `databricks-uc` (UC by default).

### 6.2 Models in Unity Catalog (formerly Model Registry)

- Registered models use `<catalog>.<schema>.<model>`; require a **model signature**.
- **Stages are deprecated** → use **aliases** (mutable named references): `models:/<catalog>.<schema>.<model>@<alias>`. Common convention: **`Champion`/`Challenger`** or `@prod`.
- Lineage via `mlflow.log_input()`; sharing across workspaces in the same metastore; cross-account via OpenSharing.

### 6.3 Unity Catalog Feature Engineering (Feature Store)

A central registry for features with governance, lineage, **point-in-time joins**, and cross-workspace sharing: using features at train time eliminates training/serving skew.

- **Feature tables** (GA): a Delta table in UC with a **primary key**; you own the pipeline.
- **Feature Views** (Public Preview, recommended): declarative `Feature` objects; Databricks computes/materializes the pipeline.

Core API: `FeatureEngineeringClient` + **`FeatureLookup`** → `create_training_set()` → `fe.log_model()` → **`fe.score_batch()`** for batch inference with automatic feature lookup.

**Point-in-time joins:** a **time-series feature table** declares a timestamp key (`timeseries_columns`); `timestamp_lookup_key` drives an **AS OF** join at the label timestamp, preventing data leakage.

**Online store (Lakebase):** `fe.create_online_store()` provisions a Lakebase instance; `fe.publish_table()` syncs offline features. Publish modes: `TRIGGERED` (incremental), `CONTINUOUS` (streaming), `SNAPSHOT` (one-time).

**Feature serving:** `FeatureSpec` + `FeatureFunction` → `create_feature_serving_endpoint()` exposes features to external apps.

### 6.4 Databricks Model Training (formerly Mosaic AI Model Training)

- **Distributed training:** **TorchDistributor** (PyTorch as Spark jobs), **DeepSpeed** (memory/pipeline optimization), **Ray** (parallel compute), **Spark ML** (`pyspark.ml.connect`, DBR 17.0+).
- **Hyperparameter tuning:** **Optuna** (recommended single-node), **Ray Tune** (distributed), **Hyperopt** (deprecated, absent after DBR 16.4 LTS ML).
- **AutoML:** classification/regression/forecasting; generates per-trial source notebooks + SHAP. Note: not built-in after DBR 18.0 ML+ (install `databricks-automl-runtime`).
- **Foundation Model Fine-tuning is deprecated** (removal Aug 2026) → migrate to **AI Runtime**.

### 6.5 Classic ML on Spark

- **scikit-learn** (single-node): train in pandas, tune with Optuna/Ray, score at scale via **pandas UDF** or `mlflow.pyfunc.spark_udf`.
- **XGBoost**: single-node `xgboost` package; distributed via **`xgboost.spark`** (DBR 12.0 ML+).
- **Spark MLlib** (`pyspark.ml`): distributed Pipelines API for classification/regression/clustering.

### 6.6 Deep learning

- **PyTorch / TensorFlow** pre-installed in DBR ML; multi-node via TorchDistributor, DeepSpeed, or Ray; track with `mlflow.pytorch.autolog()`.
- **GPU compute**: GPU instances with GPU-aware scheduling + CUDA/cuDNN/NCCL.
- **AI Runtime** (serverless GPU): no cluster config; 1×A10, 1×H100, or **8×H100** (`@distributed` decorator); DDP/FSDP/DeepSpeed; Ray support; recommended for LLM fine-tuning (LoRA/QLoRA/full), CV, recommenders.
- **Ray on Databricks**: Ray 2.3.0+ on Spark clusters (Tune/Train/Data); serverless GPU via "Ray on AI Runtime".

---

## 7. GenAI & serving

Everything is a governed UC object, and every LLM call can route through one control plane (**Unity AI Gateway**).

### 7.1 Model Serving

Unified real-time/batch serving as a REST API on **serverless**, auto-scaling (>25k queries/sec, <50 ms overhead). Three model types:

| Type | What it is |
|---|---|
| **Custom models** | MLflow PyFunc (scikit-learn/XGBoost/PyTorch/HF); **agents are custom models** |
| **Databricks-hosted foundation models** | Foundation Model APIs (e.g. Llama), **pay-per-token** or **provisioned throughput** |
| **External models** | Third-party (OpenAI, Anthropic, Bedrock, Vertex AI, Cohere…) with centralized credentials |

**Foundation Model APIs** are OpenAI-compatible. **Pay-per-token** (incl. "priority mode" for latency-sensitive traffic) for experimentation; **provisioned throughput** (dedicated capacity + performance guarantees) for production/fine-tuned models. **Agents** (LangChain/LangGraph, OpenAI Agents SDK) are served by wrapping them in MLflow's **`ResponsesAgent`** interface.

### 7.2 Unity AI Gateway (formerly AI Gateway)

Centralized governance for AI traffic, built on UC. Governs three dimensions:

| Dimension | What it governs |
|---|---|
| **Asset** | Models, MCP servers, functions, connections as UC securables |
| **Traffic** | Central routing, **rate limits**, **budgets**, usage tracking, cost observability |
| **Behavior** | **Service policies** (guardrails): `ALLOW` / `DENY` / `ASK` per request/response |

It also governs **external coding agents** (Claude Code, Cursor, Codex, Gemini CLI) and **external MCP servers**.

**Service policies (guardrails, Beta):** SQL-UDF "content" policies evaluated **ON CALL** (request) and **ON RESULT** (response); built-in checks (`block_unsafe_content`, `block_jailbreak`, `block_hallucination`) are LLM-as-a-judge; evaluation is **fail-closed**.

### 7.3 AI Search (formerly Vector Search)

Managed vector search in UC. Create an **index from a Delta table**, query via REST/SDK.

- **Algorithms:** ANN via **HNSW** (L2; cosine via normalized embeddings), keyword **BM25**, **hybrid search** (Reciprocal Rank Fusion).
- **Index types:** **Delta Sync** (auto-syncs; managed or self-managed embeddings) vs. **Direct Vector** (manual upsert).
- **Endpoints:** **Standard** (up to ~320M vectors) vs. **Storage-optimized** (1B+ vectors, cheaper).
- **RAG pattern:** embed query → similarity search → retrieve docs → append to prompt → generate.

### 7.4 Agent Framework & Agent Bricks

- **Agent Framework** (code-first): wrap any framework in **`ResponsesAgent`** (streaming, multi-agent, tracing).
- **Tools:** managed MCP servers (Genie, AI Search, DBSQL, UC functions), external MCP servers, custom MCP servers (Apps), UC function tools, structured/unstructured retrieval.
- **Agent Bricks:** **Knowledge Assistant** (document Q&A with citations, "Instructed Retriever") and **Supervisor Agent / Supervisor API** (multi-agent orchestration with built-in access controls).
- **Evaluation:** MLflow 3 `mlflow.genai.evaluate()` with built-in/custom judges, the **Review App** (human feedback), and production monitoring.
- **Deploy:** Model Serving (agent serving, `deploy()`), or **Databricks Apps**, now the recommended path for new use cases.

### 7.5 Genie, Databricks Apps, AI/BI

- **Genie Agents**: analyst-configured NL→SQL chat (datasets, example SQL, instructions, business semantics); **Genie One**, business-user UI; **Genie Code**, developer assistant.
- **Databricks Apps**: custom data/GenAI apps on serverless (Python: Streamlit/Dash/Gradio/FastAPI; Node.js: React/…), deployed via DABs/CLI with CI/CD.
- **AI/BI dashboards**: AI-assisted dashboards + Genie for self-service analytics.

---

## 8. Engineering & governance

### 8.1 Declarative Automation Bundles (DABs) + `databricks.yml`

Infrastructure-as-code for data/AI projects: source files + resource definitions (jobs, pipelines, dashboards, serving endpoints, MLflow models) + tests, deployed as a unit. `databricks.yml` declares the bundle name, **`targets`** (dev/staging/prod), **`variables`**, and **`resources`** (or `include:`).

Lifecycle: `databricks bundle init | validate | deploy -t <target> | run <resource> | destroy`.

### 8.2 Databricks CLI & Python SDK

- **CLI** wraps the REST API. Auth: **OAuth U2M** (interactive user), **OAuth M2M** (service principal client/secret), **OIDC/token federation** (CI/CD), PATs (legacy). **Profiles** in `.databrickscfg` switch workspaces/credentials. Command groups: workspace, compute, jobs, pipelines, ml, serving, catalogs/schemas/tables/grants, bundle, apps, etc.
- **Python SDK** (`databricks-sdk`): typed `WorkspaceClient`/`AccountClient`; same unified auth.

### 8.3 Git folders (Repos) & workspace files

**Git folders** = built-in Git client (GitHub/GitLab/Bitbucket/Azure DevOps). **Workspace files** = arbitrary files in the workspace (`.py`, `.sql`, `.yml`, dashboards, etc.). Source-control options from lightest → fullest: **Git-with-jobs** → **Git folders** → **Declarative Automation Bundles** (recommended).

### 8.4 Unity Catalog security

- **GRANT/REVOKE privilege model** (additive only, no DENY): need traversal (`USE CATALOG`/`USE SCHEMA`) + action (`SELECT`, `MODIFY`, `READ VOLUME`, `EXECUTE`) privileges; privileges inherit down the hierarchy. One **owner** per object (prefer groups); `MANAGE` delegates grant admin; `BROWSE` = metadata-only.
- **Fine-grained:** **row filters** (BOOLEAN UDF, `SET ROW FILTER`), **column masks** (`ALTER COLUMN … SET MASK`), **dynamic views** (use `current_user()`/`is_account_group_member()` in the view's WHERE/CASE).
- **ABAC + governed tags:** attribute-driven access from centralized **policies** (row-filter, column-mask, GRANT policies).
- **Data lineage:** automatic table/column lineage in Catalog Explorer and `system.access.table_lineage`/`column_lineage`.
- **Service policies for AI securables** (Beta): guardrails via Unity AI Gateway (see §7.2).

### 8.5 System tables

Read-only operational data in the `system` catalog (free; query compute billed). Key schemas: `system.access.audit` (audit events), `system.access.table_lineage`/`column_lineage`, `system.billing.usage`/`list_prices`, `system.compute.*`, `system.lakeflow.jobs`/`pipelines`, `system.query.history`, `system.serving.*`, `system.ai_gateway.*`, `system.information_schema.*`. Most retain **365 days**.

### 8.6 Monitoring & data quality

- **Query history** (UI + `system.query.history`), **alerts**, **AI/BI dashboards on system tables**.
- **Lakeflow Pipelines expectations** = in-pipeline data quality (warn/drop/fail).
- **Data quality monitoring** (formerly Lakehouse Monitoring): **anomaly detection** (freshness/completeness) + **data profiling** (drift detection) on serverless.

### 8.7 CI/CD

Reference flow: Version (Git) → Build → Deploy (bundles via GitHub Actions/Azure DevOps) → Test → Run → Monitor. **Environment promotion** = bundle `targets` (dev → staging → prod). **Workload identity federation (OIDC)** exchanges CI platform tokens for Databricks OAuth (no stored secrets).

---

## 9. Cost & operations

### 9.1 DBU & serverless vs. classic

- **DBU** = normalized unit of compute/hour. Cost ≈ (DBU rate × workload SKU) × instances × duration.
- **Classic** compute: predictable VMs, spot/pools/VPC/policies, but you pay for idle time and manage patching/scaling.
- **Serverless**: near-instant start, auto-scaling, no idle cost, minimal ops; **premium DBU rate** but often lower TCO by eliminating idle/over-provisioning. Limitations: no custom data sources (Federation only), no cluster/spot policies, customer-managed VPC/keys don't apply.

### 9.2 Instance pools & spot

**Instance pools** = pre-warmed idle instances (no DBUs while idle) to cut start/scale time; Databricks now recommends **serverless instead of pools** where supported. **Spot instances** cut cost for latency-tolerant workers (driver always on-demand; use fleet types).

### 9.3 Performance tuning

- **Photon**: vectorized query engine; default on SQL warehouses/serverless; accelerates SQL/DataFrame/ETL/stateless streaming. No UDFs, no RDD/Dataset, no stateful streaming.
- **Liquid clustering**: replaces partitioning + Z-order (`CLUSTER BY`, `CLUSTER BY AUTO`).
- **Other:** disk caching, dynamic file pruning, low-shuffle merge, **AQE**, cost-based optimizer (fresh stats), predictive I/O. Prefer built-ins over UDFs; tune `spark.sql.shuffle.partitions`.

### 9.4 Cost monitoring

- **`system.billing.usage`**: granular DBU records (`sku_name`, `usage_quantity`, `usage_metadata`, `custom_tags`, `billing_origin_product`); join `system.billing.list_prices` for cost.
- **Budgets** (account-wide/filtered) with alerts; **tags** for chargeback; **Governance Hub** (cost page); **usage dashboards** (import official AI/BI cost dashboards).

---

## 10. Certifications & learning paths

### 10.1 Certifications (current)

Role-based certifications (Associate/Professional), plus accreditations and a Spark-specific exam:

| Certification | Assesses |
|---|---|
| **Data Analyst Associate** | Data analysis with Databricks SQL (queries, visualizations, dashboards) |
| **Data Engineer Associate** | Introductory data engineering on the Data + AI Platform |
| **Data Engineer Professional** | Advanced data engineering tasks |
| **Machine Learning Associate** | Basic ML tasks on Databricks |
| **Machine Learning Professional** | Advanced ML in production |
| **Generative AI Engineer Associate** | Design, build, deploy GenAI solutions with Databricks |
| **Context Engineer Associate** | Design, assemble, govern context for AI agent systems |
| **Associate Developer for Apache Spark** | The Spark DataFrame API |

Plus **accreditations** (free badges): **Databricks Fundamentals** (Lakehouse) and **Generative AI Fundamentals**. The **Hadoop Migration Architect** exam was retired Aug 1, 2024.

### 10.2 Academy & learning paths

Official training is on the **Databricks Academy** (`customer-academy.databricks.com`). Role-based **learning pathways** exist for Data Analyst, Data Engineer, ML Engineer, Generative AI Engineer, Context Engineer, and a Platform Administrator specialty pathway. Each pathway culminates in the corresponding certification exam.

### 10.3 Zero-to-hero 3 to 4 week sequence

A practical sequencing for a motivated engineer (mirrors Zorost's "zero to hero" framing):

| Week | Focus | Key artifacts/skills |
|---|---|---|
| **Day 0** | Setup | Free trial/workspace, Unity Catalog metastore, CLI + SDK auth (OAuth U2M), a Git repo, a DAB scaffold |
| **Week 1** | Data engineering | Delta Lake, medallion (bronze→silver→gold), Auto Loader, Lakeflow Pipelines (expectations, AUTO CDC), Lakeflow Jobs orchestration |
| **Week 2** | DBSQL & analytics | SQL warehouses, SQL editor, AI/BI dashboards, Genie Agents, AI Functions, alerts |
| **Week 3** | ML | MLflow experiments, Models in UC (aliases), Feature Engineering (point-in-time joins), AutoML / scikit-learn / XGBoost, batch inference |
| **Week 4** | GenAI & production | Model Serving (foundation + custom/agents), AI Search + RAG, Agent Framework + evaluation, Unity AI Gateway guardrails, CI/CD with DABs, cost monitoring |

---

## 11. Zorost relevance: mapping the Modernization Practice to this curriculum

Zorost Intelligence is a **Trusted Databricks Partner** with a **Databricks Modernization Practice**. Each practice offering maps directly onto this curriculum:

| Zorost offering | Curriculum section | What it maps to |
|---|---|---|
| **Legacy BI Migration** | §4 (DBSQL/AI/BI), §3.3 (Federation) | Migrate legacy warehouses/BI → Databricks SQL + AI/BI dashboards + Genie |
| **ETL Conversion → Lakeflow/Spark/DLT** | §5 (Spark, Lakeflow Pipelines) | Re-platform ETL to Spark DataFrames, Structured Streaming, Lakeflow Pipelines |
| **Dimensional Modeling on Delta Lake** | §3 (Delta, medallion), §3.2 | Star/snowflake schemas + gold-layer modeling on governed Delta tables |
| **Streaming Pipelines** | §5.2 (Structured Streaming), §3.4 (Connect) | Auto Loader/Kafka → streaming tables, watermarks, checkpoints, CDC |
| **Unity Catalog Governance** | §1.5, §8.4 to 8.5 | Metastores, catalogs/schemas/tables/volumes, GRANT/REVOKE, row filters/masks, lineage, audit |
| **Feature Engineering & MLOps** | §6 (MLflow, Feature Store, Model Training) | Feature tables/views, point-in-time joins, model lifecycle + aliases |
| **Mosaic AI Vector Search / Serving / Gateway** | §7.1 to 7.3 | (Now) AI Search + Model Serving + Unity AI Gateway |
| **Agentic Workflows on Databricks** | §7.4 to 7.5 | Agent Framework, Agent Bricks (Knowledge Assistant/Supervisor), Apps |
| **Power BI / Tableau Modernization** | §4, §1.6 (OpenSharing), §3.3 | BI tools over SQL warehouses / OpenSharing / Federation |
| **Cost Optimization & FinOps** | §9 | DBU/SKU analysis, system.billing dashboards, budgets, serverless migration, pools/spot |

This document is the teaching backbone that lets a Zorost engineer move from a legacy stack to a governed, serverless lakehouse AI platform in roughly four weeks, the same arc the Modernization Practice runs for clients.

---

## Sources

**Platform & compute**
- https://docs.databricks.com/introduction/
- https://docs.databricks.com/getting-started/concepts/
- https://docs.databricks.com/getting-started/high-level-architecture/
- https://docs.databricks.com/lakehouse/
- https://docs.databricks.com/data-governance/unity-catalog/
- https://docs.databricks.com/database-objects/
- https://docs.databricks.com/tables/types
- https://docs.databricks.com/opensharing/
- https://docs.databricks.com/data-sharing/
- https://docs.databricks.com/resources/supported-regions
- https://docs.databricks.com/admin/admin-concepts/
- https://docs.databricks.com/compute/
- https://docs.databricks.com/compute/configure
- https://docs.databricks.com/compute/serverless/
- https://docs.databricks.com/compute/photon
- https://docs.databricks.com/compute/sql-warehouse/
- https://docs.databricks.com/compute/sql-warehouse/warehouse-types
- https://docs.databricks.com/admin/clusters/policies
- https://docs.databricks.com/compute/pool-index
- https://www.databricks.com/product/pricing

**Data & Delta Lake**
- https://docs.databricks.com/delta/
- https://docs.databricks.com/lakehouse/acid
- https://docs.databricks.com/tables/schema-enforcement
- https://docs.databricks.com/tables/update-schema
- https://docs.databricks.com/tables/history
- https://docs.databricks.com/tables/operations/vacuum
- https://docs.databricks.com/tables/operations/optimize
- https://docs.databricks.com/tables/data-skipping
- https://docs.databricks.com/tables/clustering
- https://docs.databricks.com/tables/features/deletion-vectors
- https://docs.databricks.com/tables/features/change-data-feed
- https://docs.databricks.com/lakehouse/medallion
- https://docs.databricks.com/tables/managed
- https://docs.databricks.com/tables/external
- https://docs.databricks.com/tables/foreign
- https://docs.databricks.com/query-federation/
- https://docs.databricks.com/connect/uc-connections/
- https://docs.databricks.com/ingestion/overview
- https://docs.databricks.com/ingestion/lakeflow-connect/
- https://docs.databricks.com/ingestion/cloud-object-storage/auto-loader/
- https://docs.databricks.com/volumes/

**SQL & AI/BI**
- https://docs.databricks.com/sql/
- https://docs.databricks.com/sql/user/sql-editor/
- https://docs.databricks.com/sql/user/queries/query-history
- https://docs.databricks.com/sql/user/alerts/
- https://docs.databricks.com/ai-bi/
- https://docs.databricks.com/dashboards/
- https://docs.databricks.com/sql/user/dashboards/
- https://docs.databricks.com/genie/
- https://docs.databricks.com/genie-agents/
- https://docs.databricks.com/large-language-models/ai-functions

**PySpark & pipelines**
- https://docs.databricks.com/pyspark/
- https://docs.databricks.com/spark/
- https://docs.databricks.com/getting-started/dataframes/
- https://docs.databricks.com/optimizations/disk-cache
- https://docs.databricks.com/optimizations/aqe
- https://docs.databricks.com/structured-streaming/concepts
- https://docs.databricks.com/structured-streaming/output-mode
- https://docs.databricks.com/structured-streaming/triggers
- https://docs.databricks.com/structured-streaming/watermarks
- https://docs.databricks.com/structured-streaming/stateful-streaming
- https://docs.databricks.com/structured-streaming/checkpoints
- https://docs.databricks.com/ldp/
- https://docs.databricks.com/ldp/concepts
- https://docs.databricks.com/ldp/expectations
- https://docs.databricks.com/ldp/cdc
- https://docs.databricks.com/ldp/developer/sql-dev
- https://docs.databricks.com/ldp/developer/python-ref
- https://docs.databricks.com/jobs/
- https://docs.databricks.com/jobs/configure-task
- https://docs.databricks.com/jobs/scheduled
- https://docs.databricks.com/jobs/run-if

**MLOps & ML**
- https://docs.databricks.com/mlflow/
- https://docs.databricks.com/mlflow/tracking
- https://docs.databricks.com/machine-learning/manage-model-lifecycle/
- https://docs.databricks.com/mlflow3/genai
- https://docs.databricks.com/mlflow3/genai/eval-monitor/
- https://docs.databricks.com/machine-learning/feature-store/
- https://docs.databricks.com/machine-learning/feature-store/feature-views
- https://docs.databricks.com/machine-learning/feature-store/train-models-with-feature-store
- https://docs.databricks.com/machine-learning/feature-store/time-series
- https://docs.databricks.com/machine-learning/feature-store/online-feature-store
- https://docs.databricks.com/machine-learning/feature-store/feature-function-serving
- https://docs.databricks.com/machine-learning/train-model/
- https://docs.databricks.com/machine-learning/train-model/distributed-training/
- https://docs.databricks.com/machine-learning/automl-hyperparam-tuning/
- https://docs.databricks.com/machine-learning/automl/
- https://docs.databricks.com/machine-learning/train-model/scikit-learn
- https://docs.databricks.com/machine-learning/train-model/xgboost
- https://docs.databricks.com/machine-learning/model-inference/
- https://docs.databricks.com/compute/gpu
- https://docs.databricks.com/machine-learning/ai-runtime/
- https://docs.databricks.com/machine-learning/ray/

**GenAI & serving**
- https://docs.databricks.com/machine-learning/model-serving/
- https://docs.databricks.com/machine-learning/foundation-model-apis
- https://docs.databricks.com/machine-learning/foundation-models/external-models/
- https://docs.databricks.com/agents/custom-agents/model-serving/deploy-agent
- https://docs.databricks.com/ai-gateway/
- https://docs.databricks.com/ai-gateway/ai-governance/
- https://docs.databricks.com/data-governance/unity-catalog/service-policies/
- https://docs.databricks.com/ai-search/ai-search/
- https://docs.databricks.com/agents/
- https://docs.databricks.com/agents/custom-agents/author-agent
- https://docs.databricks.com/agents/mcp-tools/
- https://docs.databricks.com/agents/agent-bricks/knowledge-assistant
- https://docs.databricks.com/agents/agent-bricks/multi-agent-supervisor
- https://docs.databricks.com/genie-one/
- https://docs.databricks.com/dev-tools/databricks-apps/

**Engineering, governance & cost**
- https://docs.databricks.com/dev-tools/bundles/
- https://docs.databricks.com/dev-tools/cli/
- https://docs.databricks.com/dev-tools/sdk-python
- https://docs.databricks.com/dev-tools/auth/
- https://docs.databricks.com/dev-tools/ci-cd/
- https://docs.databricks.com/dev-tools/auth/oauth-federation-provider/
- https://docs.databricks.com/repos/
- https://docs.databricks.com/files/workspace
- https://docs.databricks.com/data-governance/unity-catalog/access-control
- https://docs.databricks.com/data-governance/unity-catalog/filters-and-masks
- https://docs.databricks.com/data-governance/unity-catalog/abac/
- https://docs.databricks.com/admin/governed-tags/
- https://docs.databricks.com/data-governance/unity-catalog/data-lineage
- https://docs.databricks.com/admin/system-tables/
- https://docs.databricks.com/admin/system-tables/billing
- https://docs.databricks.com/data-governance/unity-catalog/data-quality-monitoring/
- https://docs.databricks.com/admin/usage
- https://docs.databricks.com/optimizations/
- https://docs.databricks.com/tables/clustering

**Certification & learning**
- https://www.databricks.com/learn/certification
- https://www.databricks.com/learn/training
- https://docs.databricks.com/resources/glossary

**Docs index**
- https://docs.databricks.com/llms.txt
