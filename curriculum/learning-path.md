# AI Engineering Lab: Learning Path

The program is one continuous arc, not 24 separate courses. Here is the visual
map, and the skill map underneath it.

## The arc

![Seven phases across 24 weeks, from Foundations to the Databricks capstone](../assets/diagrams/lab-journey.png)

The same arc as a live diagram (renders on GitHub):

```mermaid
%%{init:{"theme":"base","fontFamily":"Helvetica Neue,Helvetica,Arial,sans-serif","flowchart":{"curve":"basis","padding":14,"nodeSpacing":45,"rankSpacing":55},"themeVariables":{"fontSize":"15px","background":"#FFFFFF","primaryColor":"#EEF2F7","primaryTextColor":"#14213D","primaryBorderColor":"#14213D","secondaryColor":"#FFF1E3","secondaryTextColor":"#14213D","tertiaryColor":"#E7F4F1","tertiaryTextColor":"#14213D","lineColor":"#64748B","textColor":"#14213D","edgeLabelBackground":"#FFFFFF","clusterBkg":"#F5F8FC","clusterBorder":"#94A3B8","nodeBorder":"#14213D","mainBkg":"#EEF2F7","titleColor":"#14213D"}}}%%
flowchart TB
    subgraph P1["Phase 1 · Foundations (W1 to 4)"]
        W1["W1 Python + AI Engineering Landscape"]
        W2["W2 Data Engineering & SQL"]
        W3["W3 Machine Learning"]
        W4["W4 Deep Learning (PyTorch)"]
        W1 --> W2 --> W3 --> W4
    end
    subgraph P2["Phase 2 · LLM Core (W5 to 8)"]
        W5["W5 Tokens → Transformers"]
        W6["W6 Prompt & Context Engineering"]
        W7["W7 RAG · Vectors · Graphs"]
        W8["W8 Open Models · GPUs · Ollama"]
        W5 --> W6 --> W7 --> W8
    end
    subgraph P3["Phase 3 · Model Engineering (W9 to 11)"]
        W9["W9 Quantization & Serving"]
        W10["W10 Fine-Tuning (LoRA/DPO)"]
        W11["W11 Evals & Error Analysis"]
        W9 --> W10 --> W11
    end
    subgraph P4["Phase 4 · Harnesses & Loops (W12 to 13)"]
        W12["W12 Coding-Agent Harnesses"]
        W13["W13 Agentic Loops & Specs"]
        W12 --> W13
    end
    subgraph P5["Phase 5 · Agents (W14 to 17)"]
        W14["W14 Agent Fundamentals"]
        W15["W15 LangGraph & Frameworks"]
        W16["W16 Multi-Agent & MCP"]
        W17["W17 OpenClaw · Hermes · Ops"]
        W14 --> W15 --> W16 --> W17
    end
    subgraph P6["Phase 6 · Cloud AI Platforms (W18 to 20)"]
        W18["W18 Azure AI Foundry"]
        W19["W19 Google Vertex AI"]
        W20["W20 AWS Bedrock"]
        W18 --> W19 --> W20
    end
    subgraph P7["Phase 7 · Databricks Zero to Hero (W21 to 24)"]
        W21["W21 Unity Catalog & Lakehouse"]
        W22["W22 PySpark · Streaming · Lakeflow"]
        W23["W23 Model Training · Serving · Genie"]
        W24["W24 DABs · Governance · Capstone"]
        W21 --> W22 --> W23 --> W24
    end
    P1 --> P2 --> P3 --> P4 --> P5 --> P6 --> P7
    P7 --> GRAD["🎓 Graduate: portfolio + eval harness + governed lakehouse"]
```

## The skill map underneath (Andrew Ng, *The AI Engineering Skills Map*, 2026)

The four skills are not four separate weeks, they layer on top of each other:

| Ng skill | Primary weeks | You practice it as… |
|---|---|---|
| **Building & deploying AI applications** (blocks + evals/error analysis) | 3 to 11, 14 to 16, 21 to 23 | Every model and agent ships with a metric, an eval, and error analysis |
| **Software engineering fundamentals** (named tradeoffs) | 1 to 2, then every week | Each use case names cost, scale, reliability, speed, security, privacy tradeoffs |
| **Using coding agents** (managed context, verifiers, loops) | 12 to 13, then every week | From Week 12 you build *with* agents: spec, rules file, verifier, loop |
| **Shaping the build** (user, spec, refused tradeoff) | 12 to 13, 24 | Every use case starts with: who is the user, what is the spec, what we refuse |

And the three loops run continuously:

```mermaid
%%{init:{"theme":"base","fontFamily":"Helvetica Neue,Helvetica,Arial,sans-serif","flowchart":{"curve":"basis","padding":14,"nodeSpacing":45,"rankSpacing":55},"themeVariables":{"fontSize":"15px","background":"#FFFFFF","primaryColor":"#EEF2F7","primaryTextColor":"#14213D","primaryBorderColor":"#14213D","secondaryColor":"#FFF1E3","secondaryTextColor":"#14213D","tertiaryColor":"#E7F4F1","tertiaryTextColor":"#14213D","lineColor":"#64748B","textColor":"#14213D","edgeLabelBackground":"#FFFFFF","clusterBkg":"#F5F8FC","clusterBorder":"#94A3B8","nodeBorder":"#14213D","mainBkg":"#EEF2F7","titleColor":"#14213D"}}}%%
flowchart LR
    A["🤖 Agentic coding loop<br/>(minutes)"] --> B["🧑‍💻 Developer feedback loop<br/>(hours)"]
    B --> C["🌍 External feedback loop<br/>(days to weeks)"]
    C -->|"updates vision & spec"| A
```

- **Agentic coding loop**: from Week 12: agent writes → tests → you verify against spec.
- **Developer feedback loop**: every Friday use case: you review, steer, and update the spec.
- **External feedback loop**: Weeks 13, 17, 24: share the artifact with someone real,
  capture what breaks, and feed it back into the spec and the evals.

## The ZoroLogistics case study arc

```mermaid
%%{init:{"theme":"base","fontFamily":"Helvetica Neue,Helvetica,Arial,sans-serif","flowchart":{"curve":"basis","padding":14,"nodeSpacing":45,"rankSpacing":55},"themeVariables":{"fontSize":"15px","background":"#FFFFFF","primaryColor":"#EEF2F7","primaryTextColor":"#14213D","primaryBorderColor":"#14213D","secondaryColor":"#FFF1E3","secondaryTextColor":"#14213D","tertiaryColor":"#E7F4F1","tertiaryTextColor":"#14213D","lineColor":"#64748B","textColor":"#14213D","edgeLabelBackground":"#FFFFFF","clusterBkg":"#F5F8FC","clusterBorder":"#94A3B8","nodeBorder":"#14213D","mainBkg":"#EEF2F7","titleColor":"#14213D"}}}%%
flowchart LR
    D["Week 1<br/>Synthetic shipment data"] --> C["Week 2<br/>Clean, profile, SQL"]
    C --> M["Week 3 to 4<br/>ETA prediction (ML → DL)"]
    M --> L["Week 5 to 8<br/>LLM: docs, prompts, RAG, local model"]
    L --> Q["Week 9 to 11<br/>Quantize, fine-tune, evaluate"]
    Q --> A["Week 14 to 16<br/>Support agent + multi-agent team"]
    A --> O["Week 17<br/>OpenClaw personal assistant"]
    O --> X["Week 18 to 20<br/>Same agent on Azure / Google / AWS"]
    X --> DB["Week 21 to 24<br/>ZoroLogistics Lakehouse Intelligence on Databricks"]
```

Every artifact feeds the next phase, the dataset from Week 1 becomes the feature
table in Week 23; the Week 11 eval harness gates the Week 18 cloud deployment.

---
© 2026 Zorost Intelligence LLC · https://zorost.com
