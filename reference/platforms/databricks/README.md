# Databricks: Zero to Hero

> Part of AI Engineering Lab · Developed by Zorost Intelligence AI Lab · https://zorost.com
> The most comprehensive module in the program: Databricks AI engineering from
> day zero to production, mirroring Zorost's own Databricks Modernization Practice
> (Legacy BI Migration · ETL Conversion → Lakeflow/Spark/DLT · Unity Catalog
> Governance · Model Serving · FinOps).

This module is the backbone of **Weeks 21 to 24** of the 24-week program and stands
alone as a complete Databricks learning path. Notebooks live in
[`curriculum/week-21/`](../../../curriculum/week-21/) through `week-24/`; the files
below are the concept deep-dives.

## The path

| # | File | What you learn | Week |
|---|---|---|---|
| 00 | [00-day-zero-setup.md](00-day-zero-setup.md) | Account, workspace, CLI auth, first notebook | 21 |
| 01 | [01-unity-catalog.md](01-unity-catalog.md) | Metastore, catalogs, schemas, volumes, grants, lineage | 21 |
| 02 | [02-compute.md](02-compute.md) | Clusters, SQL warehouses, serverless, DBU pricing | 21 |
| 03 | [03-delta-lake.md](03-delta-lake.md) | ACID, time travel, VACUUM/OPTIMIZE, liquid clustering, medallion | 21 |
| 04 | [04-dbsql.md](04-dbsql.md) | Databricks SQL, SQL editor, AI/BI dashboards | 21 |
| 05 | [05-pyspark.md](05-pyspark.md) | PySpark DataFrames, performance, Photon | 22 |
| 06 | [06-pipelines-jobs.md](06-pipelines-jobs.md) | Lakeflow Pipelines (DLT), streaming, Lakeflow Jobs, Connect | 22 |
| 07 | [07-mlflow-experiments.md](07-mlflow-experiments.md) | MLflow tracking, model registry, autologging | 23 |
| 08 | [08-feature-engineering.md](08-feature-engineering.md) | UC feature tables, FeatureLookup, point-in-time joins | 23 |
| 09 | [09-model-training.md](09-model-training.md) | Classic ML, AutoML, Databricks Model Training | 23 |
| 10 | [10-model-serving.md](10-model-serving.md) | Serving endpoints, AI Gateway, external models | 23 |
| 11 | [11-vector-search-rag.md](11-vector-search-rag.md) | Vector Search indexes, Delta Sync, RAG patterns | 23 |
| 12 | [12-ai-functions-genie.md](12-ai-functions-genie.md) | AI functions (ai_query…), Genie spaces | 23 |
| 13 | [13-agents.md](13-agents.md) | Agent Framework (Mosaic AI), Agent Bricks, Agent Evaluation | 23 to 24 |
| 14 | [14-apps-dashboards.md](14-apps-dashboards.md) | AI/BI dashboards, Databricks Apps | 24 |
| 15 | [15-dabs-ci-cd.md](15-dabs-ci-cd.md) | Asset Bundles, CLI, Git folders, CI/CD | 24 |
| 16 | [16-governance-security.md](16-governance-security.md) | Row filters, column masks, dynamic views, audit | 24 |
| 17 | [17-finopps-cost.md](17-finopps-cost.md) | Billing system tables, cost dashboards, FinOps | 24 |
| 18 | [18-certification-path.md](18-certification-path.md) | Databricks certifications and the hero's recap | 24 |

## The capstone

[`capstone/`](capstone/), **ZoroLogistics Lakehouse Intelligence**: the full
stack from Weeks 21 to 23 (medallion lakehouse, streaming pipeline, point-in-time ETA
model, Vector Search RAG, Genie space) shipped as a Databricks Asset Bundle with
CI/CD, governance, and a FinOps dashboard.

## How to use this module

1. **Weeks 21 to 24 give you the schedule**: follow the weekly checklists in the
   Excel tracker; each week links here for concept depth.
2. **Upload, don't rewrite**: the weekly notebooks run in any Databricks
   workspace (workspace files → Repos), or run the SQL parts in the SQL editor.
3. **Everything here is verified against the official Databricks documentation**
   (docs.databricks.com), cited in each file's Sources section. Databricks renames
   features at a brisk pace; each file notes "verify against live docs" where it
   matters.
4. **Free tier reality**: Databricks offers a free trial with serverless SQL and
   notebooks; keep the cost notes in file 17 in mind from day one.

## Related

- [Knowledge base: Databricks overview](../../knowledge-base/13-databricks-overview.md)
- [Week 21: Day Zero](../../../curriculum/week-21/) · [Week 22](../../../curriculum/week-22/) ·
  [Week 23](../../../curriculum/week-23/) · [Week 24](../../../curriculum/week-24/)
- [Zorost Databricks Modernization Practice](https://zorost.com)

---
© 2026 Zorost Intelligence LLC · https://zorost.com
