# AI Engineering Lab: 24-Week AI Engineering Program

> **Find the Signal. Act with Intelligence.** · Developed by [Zorost Intelligence AI Lab](https://zorost.com)

This is the heart of AI Engineering Lab: a 24-week, week-by-week path from Python
fundamentals to production lakehouse AI. Every week has a **section** (the phase),
a **category** (the skill area), a **use case** from the running ZoroLogistics
case study, **runnable notebooks**, and a **checklist** you tick off in the Excel
tracker.

![Seven phases across 24 weeks, and what each one puts in your hands](../assets/diagrams/lab-journey.png)

> **Brand new?** Read [`START-HERE.md`](../START-HERE.md) first, and keep
> [`reference/GLOSSARY.md`](../reference/GLOSSARY.md) one tab away, every term in the program is
> defined there in plain language.

## How the program works

![One week, four beats: study, build, ship, reflect](../assets/diagrams/lab-week.png)

1. **One case study, all 24 weeks.** You are the AI engineering team at
   **ZoroLogistics**, a fictional freight company. The data, the models, and the
   agents you build in Week 1 are reused, improved, and productionized all the way
   to Week 24. By graduation you have a portfolio of interconnected artifacts, not
   24 disconnected demos.
2. **Weekly cadence (≈10 hours/week).**
   - **Mon to Tue · Study**: read the week's README and the linked knowledge-base file.
   - **Wed to Thu · Build**: run the notebook(s), then modify and extend them.
   - **Fri · Use case**: complete the use-case exercise: ship something concrete.
   - **Fri to Sun · Reflect & check off**: update the Excel tracker, push to your fork.
3. **Evals everywhere.** From Week 3 onward, every AI artifact ships with a score
   (a metric or an eval) and an error-analysis note. That is the core AI engineering
   habit this program installs.
4. **Local-first, cloud-later.** Weeks 1 to 13 run on your laptop (no GPU needed until
   Week 8, and even then a small model on CPU works). Weeks 18 to 24 use free/limited
   tiers of the major clouds.

## Prerequisites

- Comfort with any programming language (Python is taught from the ground up)
- Git basics (Week 1 refreshes them)
- A laptop: 16 GB RAM recommended; Apple Silicon or NVIDIA GPU helpful from Week 8
- Optional accounts (created during their weeks): GitHub, Hugging Face, a model
  API key of your choice, free tiers of Azure / Google Cloud / AWS / Databricks

## The 24 weeks at a glance

| Wk | Week title | Section | Category |
|---|---|---|---|
| 1 | Python Foundations & the AI Engineering Landscape | Foundations | Python & Environment |
| 2 | Data Engineering & SQL for AI | Foundations | Data & SQL |
| 3 | Machine Learning Fundamentals | Foundations | Classical ML |
| 4 | Deep Learning with PyTorch | Foundations | Deep Learning |
| 5 | How LLMs Work: Tokens to Transformers | LLM Core | LLM Internals |
| 6 | Prompt Engineering & the Context Window | LLM Core | Prompt & Context |
| 7 | RAG, Vector Search & Knowledge Graphs | LLM Core | Retrieval & Graphs |
| 8 | Open Models & Local Inference: GPUs, Ollama, llama.cpp | LLM Core | Local Models & GPUs |
| 9 | Quantization & Efficient Inference | Model Engineering | Quantization & Serving |
| 10 | Fine-Tuning: LoRA, SFT & DPO | Model Engineering | Fine-tuning |
| 11 | Evals & Error Analysis for AI Systems | Model Engineering | Evaluation |
| 12 | Coding-Agent Harnesses: Claude Code, Cursor, OpenCode, DSH | Harnesses & Loops | Harnesses |
| 13 | Agentic Coding Loops & Spec-Driven Development | Harnesses & Loops | Loops & Specs |
| 14 | Agent Fundamentals: The Loop, Tools & Memory | Agents | Agent Core |
| 15 | Agent Frameworks: LangGraph & the State-Graph Model | Agents | Frameworks |
| 16 | Multi-Agent Systems & MCP | Agents | Multi-Agent & Protocols |
| 17 | OpenClaw, Hermes & Agent Operations | Agents | Personal Agents & Ops |
| 18 | Azure AI Foundry | Cloud AI Platforms | Microsoft |
| 19 | Google Vertex AI & Gemini | Cloud AI Platforms | Google |
| 20 | AWS Bedrock & SageMaker AI | Cloud AI Platforms | AWS |
| 21 | Databricks Day Zero: Unity Catalog & the Lakehouse | Databricks Zero to Hero | Platform & Data |
| 22 | Databricks Data Engineering: PySpark, Streaming & Lakeflow | Databricks Zero to Hero | Pipelines |
| 23 | Databricks ML & GenAI: Training, Serving, Genie | Databricks Zero to Hero | ML & GenAI |
| 24 | Databricks Production: DABs, Governance & the Capstone | Databricks Zero to Hero | Production & Capstone |

Each week folder (`curriculum/week-NN/`) is a complete lesson:

```
week-NN/
├── README.md        # the lesson: problem → deep concepts (tables, diagrams,
│                    #   worked examples, pitfalls, glossary) → notebook
│                    #   walkthrough → use case → sources
├── notebooks/ # 1 to 3 runnable Jupyter notebooks (Python / SQL / PySpark)
├── exercises.md     # graded exercises + hints + the week's checklist
└── quiz.md          # 10-question self-check with answer key (pass 8/10)
```

## The phases

### Phase 1 · Foundations (Weeks 1 to 4)
Python, data engineering, classical ML, and deep learning, taught the AI engineering
way: every model ships with a metric, a split, and an error analysis. Week 1 builds
the ZoroLogistics synthetic-data generator you reuse forever after.

### Phase 2 · LLM Core (Weeks 5 to 8)
How LLMs actually work, tokens, embeddings, attention, KV cache, then the two
engineering superpowers on top: **prompt & context-window engineering** and
**retrieval (RAG + knowledge graphs)**. Week 8 takes you local: open models,
Ollama/llama.cpp/MLX, and GPU setup from CUDA to Apple Metal.

### Phase 3 · Model Engineering (Weeks 9 to 11)
Make models cheaper and yours: quantization formats and serving engines, fine-tuning
with LoRA/SFT/DPO, and the discipline that decides it all, evals and error analysis
(Ng: the single biggest predictor of how fast a team ships an agent).

### Phase 4 · Harnesses & Loops (Weeks 12 to 13)
Become dangerous with coding agents: Claude Code, Cursor, OpenCode, and the DeepSeek
Harness. Learn managed context, rules files, subagents, and the three loops
(agentic coding → developer feedback → external feedback) with a spec, a verifier,
and a blast-radius rule.

### Phase 5 · Agents (Weeks 14 to 17)
From a hand-written ReAct loop to LangGraph state graphs, multi-agent orchestration,
and MCP. Week 17 runs OpenClaw as your personal lab assistant and Hermes-class open
models as agent brains, then adds the ops layer: tracing, evals, and cost.

### Phase 6 · Cloud AI Platforms (Weeks 18 to 20)
The same ZoroLogistics support agent, deployed three ways: Azure AI Foundry
(Microsoft), Vertex AI + AI Studio (Google), Bedrock + SageMaker (AWS). Compare
capabilities, governance, and cost, and learn how to pick.

### Phase 7 · Databricks Zero to Hero (Weeks 21 to 24)
The full Zorost Databricks modernization playbook: Unity Catalog, Delta Lake
medallion, DBSQL, PySpark, streaming, Lakeflow Pipelines & Jobs, MLflow, feature
engineering, Databricks Model Training, Model Serving + Unity AI Gateway,
AI Search (Vector Search), AI functions, Genie, and Agent Bricks, then DABs,
CI/CD, governance, and FinOps, ending in the
**ZoroLogistics Lakehouse Intelligence** capstone.

## Progress tracking

Download `tracking/ai-engineering-lab-24-week-tracker.xlsx` and open it in Excel,
Google Sheets, or LibreOffice. It contains:

- A **Dashboard** sheet: your name, start date, per-week completion bars, and a
  chart of your progress across all 24 weeks.
- **One sheet per week**: every checklist item with a status dropdown
  (☐ Not started · ▶ In progress · ✅ Done · ⏭ Skipped), automatic per-week
  completion percentage, and a notes column.

The workbook is generated from `manifest.json`, see `tracking/README.md`.

## Certification of completion

Finish all 24 weeks (including the Week 24 capstone) and you will have:

- 43 executed notebooks (Python, SQL, PySpark)
- A portfolio: fine-tuned model, RAG agent, multi-agent system, MCP server,
  three cloud deployments, a governed Databricks lakehouse
- An eval harness you built yourself, the artifact that separates AI engineers
  from demo builders

Share your fork and tracker dashboard with your mentor, your team, or
[Zorost Intelligence](https://zorost.com).

---
© 2026 Zorost Intelligence LLC · https://zorost.com
