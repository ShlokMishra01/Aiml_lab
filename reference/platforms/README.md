> **Part of AI Engineering Lab · Developed by Zorost Intelligence AI Lab · [zorost.com](https://zorost.com)**

# Platforms

> **Find the Signal. Act with Intelligence.** · Weeks 18 to 24

The `reference/platforms/` section is where the program stops being "local-first" and goes to the
cloud. Weeks 1 to 17 run on your laptop; Weeks 18 to 24 put the same ZoroLogistics artifacts on
enterprise platforms. Each module is a guided, code-first tour of one vendor, following one
shared pattern so you can compare platforms apples-to-apples.

## What's here

| Module | Path | Vendor | Week | Focus |
|---|---|---|---|---|
| Azure AI Foundry | [ai-foundry/README.md](ai-foundry/README.md) | Microsoft | 18 | Hub/project model, serverless endpoints, Agent Framework, AI Gateway |
| Google Vertex AI | [google-vertex/README.md](google-vertex/README.md) | Google | 19 | AI Studio vs Vertex, Gemini, Agent Builder/Engine + ADK, BigQuery ML |
| AWS Bedrock | [aws-bedrock/README.md](aws-bedrock/README.md) | AWS | 20 | Converse API, Knowledge Bases, Agents + Guardrails, SageMaker |
| Databricks | [databricks/README.md](databricks/README.md) | Databricks | 21 to 24 | Unity Catalog, PySpark, Lakeflow, AI Search, Genie, DABs |

> The Databricks module is a four-week "zero-to-hero" arc (Weeks 21 to 24), not a single-week
> tour like the three clouds. It reuses the same ZoroLogistics lakehouse and ships a full
> production deployment, see its own README for that structure.

## How these map to Weeks 18 to 24

Phase 6 (Weeks 18 to 20) is deliberately repetitive: **the same ZoroLogistics support agent,
deployed three ways.** Because the product is constant, the platform becomes the variable,
which is exactly the judgment call a client or employer asks of you ("Azure, GCP, or AWS?").

| Week | Platform | The ZoroLogistics use case |
|---|---|---|
| 18 | Azure AI Foundry | Deploy the support agent with online evaluation and AI Gateway rate limits |
| 19 | Google Vertex AI | A multimodal bill-of-lading pipeline (Gemini OCR → structured JSON → BigQuery) + the agent rebuilt with ADK |
| 20 | AWS Bedrock | A RAG support agent with Guardrails, plus the three-cloud comparison matrix |
| 21 to 24 | Databricks | The ZoroLogistics lakehouse: governed medallion tables, pipelines, ML, Genie, and a DAB-deployed capstone |

The three cloud weeks feed a single Week 20 deliverable: the **Great Platform Comparison
matrix**. If you keep a running note of "how do I do X here" (deploy a model, build an
agent, do RAG, run evals, set a cost cap) as you go, that matrix writes itself.

## The shared pattern every platform module follows

Each of the three cloud READMEs follows the same seven sections, in the same order. Learn
the shape once and you can skim any vendor's docs the same way:

1. **Overview**: the platform's mental model and *when to use it* (vs. the other clouds).
2. **Day-0 setup**: account, credentials, and the "before you can call a model" ceremony
   (hub/project, gcloud + quota, or IAM + model access).
3. **Core lab**: the minimal "hello world" model call for that platform's SDK.
4. **Agent or RAG**: building the ZoroLogistics support agent (Agent Framework / ADK +
   Agent Engine / Bedrock Agents + Knowledge Bases).
5. **Evals**: how the platform measures quality (tracing, LLM-as-judge, model evaluation).
6. **Governance & cost**: rate limits, content safety, budgets, and pricing reality.
7. **Sources**: the official docs to verify against.

Each README also points at the Week's notebooks (`curriculum/week-NN/notebooks/`), which are
the runnable artifacts; the README is the map, the notebooks are the terrain.

## Cost-safety notes (read before you spend anything)

The three clouds all have generous free/limited tiers, and this program is built to run
mostly inside them, **but only if you set guardrails before you type.** The rules:

1. **Always set a budget and an alert first.** In Azure, a budget + alert on the
   subscription; in Google Cloud, a billing budget on the project; in AWS, a billing alarm
   and (ideally) an AWS Budgets action. Do this in Week 18's Day-0 and reuse the habit.
2. **Use the free tier, don't trust it.** Google AI Studio's free tier is the easiest
   "hello world" in the industry but has daily request quotas. Azure and AWS free trials
   carry time and credit limits. Read the current limits in each module's cost section.
3. **Prefer pay-as-you-go, avoid reserved capacity.** Provisioned throughput (Azure PTUs,
   Bedrock Provisioned Throughput) is for steady production load, it bills whether you use
   it or not. Learners should stay on on-demand/serverless per-token billing.
4. **Delete or stop what you finish.** Endpoints, provisioned capacity, and managed
   inference instances meter even when idle. Tear down Day-0 resources you aren't using.
5. **Never send sensitive data through a free tier.** Google AI Studio may use data to
   improve products by default; treat every free/experiment tier as non-private. The
   ZoroLogistics dataset is synthetic, so it's safe, but the *habit* of segregating
   sensitive data is the real lesson.

The program's rule of thumb: **if a step would surprise you on a bill, it's a step too
far.** Check the live pricing page linked in each module before anything you aren't sure
about.

## How to use this section

1. Read [reference/knowledge-base/12-cloud-platforms.md](../knowledge-base/12-cloud-platforms.md)
   first for the three-cloud mental models and the big comparison table.
2. Each week, read that platform's README here, then run the week's notebooks.
3. Keep the running comparison note; it becomes the Week 20 matrix.

---

© 2026 Zorost Intelligence LLC · [zorost.com](https://zorost.com)
