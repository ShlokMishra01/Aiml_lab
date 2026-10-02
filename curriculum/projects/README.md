# AI Engineering Lab: Projects

Portfolio projects that span multiple weeks. The program's weekly use cases build
toward these; each project has an inspectable artifact with a number attached,
that is the Zorost gate: *a stranger can use it, and you can show them what it did.*

## The capstone: ZoroLogistics Lakehouse Intelligence (Weeks 21 to 24)

The graduation project, deployed on Databricks:

- **Data**: medallion lakehouse (bronze → silver → gold) from the Week 1 dataset
- **Pipelines**: streaming shipment events with quality expectations (Week 22)
- **ML**: point-in-time ETA model registered in MLflow, served behind the AI Gateway (Week 23)
- **GenAI**: policy RAG via Vector Search + a Genie space for ops analysts (Week 23)
- **Production**: deployed end-to-end as a Databricks Asset Bundle with CI/CD,
  row/column governance, and a FinOps dashboard (Week 24)

See [`reference/platforms/databricks/capstone/`](../../reference/platforms/databricks/capstone/) (added in Week 21)
and [`curriculum/week-24/`](../week-24/).

## Milestone projects by phase

| Project | Built in | Artifact |
|---|---|---|
| ZoroLogistics data generator + silver dataset | Weeks 1 to 2 | Seeded generator + validated CSV/Parquet |
| ETA prediction (ML → DL) with model cards | Weeks 3 to 4 | Model card v2 with error analysis |
| BoL extraction suite + RAG policy bot | Weeks 6 to 7 | Prompt suite + eval scores |
| Local triage model (quantized, fine-tuned, served) | Weeks 8 to 10 | Quality-vs-cost report |
| ZoroEval, the eval harness | Week 11 | CI-gated eval script |
| ETA CLI + Support Bot MVP via coding agents | Weeks 12 to 13 | Deployed CLI + loop log |
| Support triage multi-agent team over MCP | Weeks 14 to 16 | A/B report vs single agent |
| ZoroLab personal assistant (OpenClaw + Hermes-class model) | Week 17 | Skills + ops runbook |
| The same support agent on Azure / Google / AWS | Weeks 18 to 20 | Three-cloud comparison matrix |

## How to make projects count

1. Give every project a **public URL** (GitHub repo, deployed endpoint, published
   dashboard), an artifact someone else can inspect.
2. Attach **numbers**: eval scores, cost per task, p95 latency, recall@k.
3. Write the **limitation honestly**, what the artifact cannot do, and what you
   would do next. That sentence is worth more than the demo.

---
© 2026 Zorost Intelligence LLC · https://zorost.com
