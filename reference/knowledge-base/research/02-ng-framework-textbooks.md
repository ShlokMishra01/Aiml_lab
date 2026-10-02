# 02: Andrew Ng's AI Engineering Framework, Key References & Zorost Intelligence

> Research draft for the AI Engineering Lab 24-week AI engineering curriculum.
> Compiled by synthesizing primary sources (DeepLearning.AI / The Batch, Anthropic, OpenAI, Google, Microsoft), publisher pages, and the live https://zorost.com site. Concepts are synthesized in the author's own words; brief quoted definitions carry citations.

---

## A. Andrew Ng's AI Engineering Framework + DeepLearning.AI

### A.1 The AI Engineering Skills Map (The Batch, Aug 2026)

Andrew Ng published **"The AI Engineering Skills Map"** in The Batch (issue 366, dated **2026-08-14**; also posted as an X article the same day). He states two purposes: (1) help developers prioritize *what to learn*, and (2) help employers *hire skilled developers*.

**Methodology.** The map was synthesized from more than 10,000 job postings, dozens of structured interviews with AI experts, hiring managers, and recruiters, plus surveys and other online data. Ng describes the process as analogous to *clustering* over that corpus to surface the skills that matter now and in the near future, he does not present it as a peer-reviewed statistical study, and he says he will keep revising it as AI evolves. Treat it as a living, opinionated synthesis, not a fixed taxonomy.

**Terminology.** Ng writes about **AI engineering skills**, not only the "AI Engineer" job title. His analogy: all developers need cloud skills even though few hold the title "Cloud Engineer." The map therefore applies to full-stack, data, DevOps, ML, and AI engineers alike.

**The four skills (Ng's framing, condensed):**

1. **Building and deploying AI applications.** The defining difference between AI and non-AI software is *unpredictable outputs*: you don't know what an LLM will return, and you don't know what a trained model will predict on a new example. Skilled people know the building blocks (LLMs, context engineering, RAG, agentic workflows, machine learning, deep learning) **and** know how to use statistical techniques to *measure, steer, and govern* those systems toward more predictable behavior. The core practice is a disciplined **evals + error analysis** loop.

2. **Software engineering fundamentals.** Deep understanding of how software works lets you build more effectively. Engineering is a set of tradeoffs among *cost, scalability, reliability, speed*, with *security and privacy* adding further complexity. Fundamentals let you (a) recognize which tradeoffs exist and (b) steer a coding agent in the precise language of software engineering, something a vibe-coder who doesn't know the tradeoffs cannot do.

3. **Using coding agents.** Agentic coding is now a key skill for every developer. This includes a mental model of how agents work, their limits and workarounds, how much to intervene vs. leave alone, managing the agent's context, planning vs. execution tradeoffs, giving the agent verifiers/evals so it can close its own loop, working from a clear spec (and knowing when a formal spec isn't worth it), orchestrating multiple agents, and guarding against a production-database disaster. Because practice changes fast, it also means a routine for trying new tools.

4. **Shaping the build.** Given a clear spec, coding agents are rapidly improving at delivering to it, so the scarce work shifts *upstream* to deciding what belongs in the spec. Engineers should no longer expect a pixel-perfect design to implement. Effective AI engineering requires product sense, business context, and customer goals. AI also grants greater ownership/agency: identify problems, drive the build, know when to ship an MVP for user testing and when to slow down and build carefully.

**Cross-cutting:** continuous learning, a mindset under all four skills, not a fifth skill.

**Precursor (June 2025).** Ng's earlier "GenAI Application Engineer" description bundled three things: (1) AI building blocks (prompting, RAG, evals, agentic workflows, ML), (2) AI-assisted rapid engineering, (3) product/design instincts. The 2026 map is the hiring-and-learning form of that triad, building blocks + evals sit in skill 1, rapid engineering in skills 2 to 3, product instincts in skill 4.

> **Source:** https://www.deeplearning.ai/the-batch/issue-366 · https://x.com/AndrewYNg/status/2088302050706686198

### A.2 Ng's Related Letters (dates & key ideas)

**"Three Key Loops for Building Great Software"** (The Batch, 2026). Ng frames 0-to-1 product building as three loops running on different clocks:

- **Agentic coding loop (minutes).** Give the agent a product spec and optionally a set of evals; it writes code, tests, and iterates until bug-free and spec-compliant. Ng dates the ability for an agent to *close this loop on its own* (e.g., drive a browser to check the build) to roughly late 2025, which lets an agent run much longer without a human in the middle.
- **Developer feedback loop (tens of minutes to hours).** The human examines the product and steers the agent. As agents test their own code, the human's time shifts from manual QA toward higher-level product decisions (features, UI, user flow). Translating vision into a spec the agent can implement is still substantial work; after seeing an implementation, update/clarify the spec; if the same problems repeat, *build evals*.
- **External feedback loop (hours to weeks).** Friends, alpha testers, production usage, A/B tests. This data updates the developer's *vision*, which updates the *spec*, which drives the coding agent.

Key idea: humans retain a **context advantage**, they know more than current AI about the users and the operating context, which is why the developer loop doesn't fully automate. Ng prefers "context advantage" to "taste," because it gives a concrete path to making the AI better. AI-native teams increasingly use AI to *gather* usage data, summarize feedback, and do competitive analysis.

> **Source:** https://www.deeplearning.ai/the-batch/three-key-loops-for-building-great-software

**"Make All Your Tokens (and Your Brainwork) Count"** (The Batch). Organizing principle: **AI tokens are cheap; human tokens are gold.** Concrete practices: for large, hard-to-change systems, spend human time on architecture first (database, service boundaries, third-party lock-in, API contracts); for quick 0-to-1 work in an unfamiliar domain, write a short "inferior" spec, let the agent build for minutes, examine the result, refine, repeat, do **not** turn spec-driven development into a waterfall gate. Early code can be thrown away; the learning from seeing it is the value. When you make a key decision, have the agent write it into `SPEC.md` (or the project equivalent), because agents still forget after context compaction, rediscovering an AI-found fact wastes cheap tokens, but re-telling a *human* decision wastes gold ones. This is the letter that most directly elaborates **shaping the spec** as a skill.

> **Source:** https://www.deeplearning.ai/the-batch/make-all-your-tokens-and-your-brainwork-count

**"Coding Agents Accelerate Some Software Tasks More Than Others"** (The Batch). Acceleration is **uneven**, most to least: (1) **frontend** (agents are fluent in common web stacks and can close the loop by driving a browser; visual design is still weak), (2) **backend** (more human steering for corner cases, security, and migrations; skilled developers still outproduce novices-with-agents), (3) **infrastructure** (limited model knowledge of complex tradeoffs; don't trust agents for critical infra decisions), (4) **research** (agents speed code/experiment bookkeeping, but hypothesis, interpretation, and iteration stay mostly human). Practical consequence for planning: do not promise infra or research work at frontend speed.

> **Source:** https://www.deeplearning.ai/the-batch/coding-agents-accelerate-some-software-tasks-more-than-others

**"Improve Agentic Performance with Evals and Error Analysis" (Parts 1 & 2)** (The Batch). Ng calls a disciplined evals + error-analysis process **the single biggest predictor of how rapidly a team makes progress building an AI agent**. Key ideas:

- **Evals first**: define what an error *is* before analyzing errors. Don't invent the metric in the abstract: build a prototype, manually inspect a handful of outputs, then build datasets/metrics for the dimensions you actually care about. Use deterministic code metrics when possible; use LLM-as-judge when the dimension is subjective; tune the eval as new failure modes appear (more iterative for agentic workflows than supervised learning).
- **Error analysis second**: an eval gives a number; error analysis tells you *which step* to improve. On a multi-step agent, read the traces of bad outputs and compare each step to **human-level performance (HLP)**; invest in the step that most often produces something materially worse than a human would.
- **Change the workflow, not only the step.** With LLMs, workflow shape iterates fast. A common move: rip out scaffolding and let a stronger model absorb the step (e.g., drop a separate HTML-cleaning call if a stronger model handles messy HTML directly). Spot this when a *chain of steps* collectively underperforms a human even though each step looks fine, the chain is too rigid.

> **Source:** https://www.deeplearning.ai/the-batch/improve-agentic-performance-with-evals-and-error-analysis-part-1 · https://www.deeplearning.ai/the-batch/improve-agentic-performance-with-evals-and-error-analysis-part-2

### A.3 DeepLearning.AI Course Catalog: relevance for a training curriculum

DeepLearning.AI's catalog (free short courses + Coursera specializations) maps cleanly onto Ng's four skills. Below, each course is annotated with instructor, topic, and *why it matters* for a 24-week curriculum.

**LLM internals & foundations (skill 1 building blocks):**

- **How Transformer LLMs Work**: *Jay Alammar & Maarten Grootendorst* (2025). Tokenization, embeddings, transformer blocks, attention, KV cache, mixture-of-experts, with code. *Why:* the correct mental model of how an LLM computes, which underpins context engineering, cost reasoning, and debugging. (https://www.deeplearning.ai/short-courses/how-transformer-llms-work/)
- **Large Language Models with Semantic Search**: *Jay Alammar & Luis Serrano* (DeepLearning.AI × Cohere, 2023). Embeddings, dense retrieval, reranking, and semantic search as an application primitive. *Why:* retrieval is the foundation of RAG; this is the canonical "how embeddings actually work" course.
- **Generative AI with LLMs**: *Antje Barth, Chris Fregly, Shelbee Eigenbrode, Mike Chambers* (DeepLearning.AI × AWS). The flagship deep-dive: transformer architecture, prompting, fine-tuning (PEFT/LoRA), RLHF, and deployment tradeoffs. *Why:* the most complete single "how foundation models work and how to tune them" survey.
- **Machine Learning Specialization** and **Deep Learning Specialization**, *Andrew Ng*. *Why:* the classical ML/deep-learning substrate that Ng says helps developers adapt to generative AI faster (supervised-learning evaluation intuitions transfer).

**Python & software engineering fundamentals (skill 2):**

- **AI Python for Beginners**: *Andrew Ng*. A modern, LLM-assisted introduction to Python (the course itself uses an LLM as a coding tutor). *Why:* lowers the entry barrier so domain specialists can reach the coding baseline needed for everything else. (https://www.deeplearning.ai/courses/ai-python-for-beginners)

**Building systems / APIs (skills 1 & 2):**

- **Building Systems with the ChatGPT API**: *Isa Fulford & Andrew Ng*. Chaining calls, token/cost accounting, classification, moderation, and assembling a customer-service bot. *Why:* the canonical "turn a model API into a *system*" course, the difference between a demo and an application. (https://www.deeplearning.ai/courses/chatgpt-building-system/)

**Evals, debugging, quality (skill 1, the evals/error-analysis core):**

- **Evaluating and Debugging Generative AI**: *Andrew Ng & Carey Phelps (Weights & Biases)*. Instrumenting LLM apps, logging traces, and using them to debug. *Why:* direct teaching of the evals + error-analysis loop that Ng ranks as the top predictor of team velocity. (https://learn.deeplearning.ai/courses/evaluating-debugging-generative-ai/)
- **Automated Testing for LLMOps**: (DeepLearning.AI). CI-style testing for LLM apps. *Why:* turns evals into a repeatable engineering gate rather than a one-off.

**RAG & retrieval (skill 1):**

- **Building and Evaluating Advanced RAG**: *Jerry Liu (LlamaIndex) & Anupam Datta (TruEra)*. Sentence-window retrieval, auto-merging, reranking, and RAG *evaluation* (the "triad" of context relevance, groundedness, answer relevance). *Why:* bridges retrieval architecture and retrieval evaluation. (https://www.deeplearning.ai/courses/building-evaluating-advanced-rag)
- **Vector Databases: from Embeddings to Applications**: *Sebastian Witalec (Weaviate)*. Vector search, hybrid search, and building a RAG app. *Why:* hands-on with the retrieval store that powers RAG at scale. (https://www.deeplearning.ai/courses/vector-databases-embeddings-applications)
- **Knowledge Graphs for RAG**: *Andreas Kollegger (Neo4j)*. Graph-structured retrieval for multi-hop questions. *Why:* teaches when vector-only retrieval is insufficient. (https://www.deeplearning.ai/courses/knowledge-graphs-rag)
- **Preprocessing Unstructured Data for LLM Applications**: *Matt Robinson (Unstructured)*. Extracting and cleaning text, tables, and layout from PDFs/HTML/Office. *Why:* RAG quality is bounded by ingestion quality, the "garbage in" guardrail. (https://community.deeplearning.ai/t/new-course-enroll-in-preprocessing-unstructured-data-for-llm-applications/607757)

**Agents, LangGraph, MCP (skills 1 & 3):**

- **AI Agents in LangGraph**: *Harrison Chase (LangChain)*. Persistence, human-in-the-loop, state machines for agent control. *Why:* the reference framework for building *controllable* agents, the "govern" half of measure/steer/govern. (https://www.deeplearning.ai/courses/ai-agents-in-langgraph)
- **Long-Term Agentic Memory With LangGraph**: *LangChain team*. Memory architectures for agents. *Why:* agent context/memory engineering, a live frontier topic.
- **LangChain for LLM Application Development** and **Functions, Tools and Agents with LangChain**, *Harrison Chase*. *Why:* tool-calling and function routing are the mechanical heart of agents.
- **MCP: Build Rich-Context AI Apps with Anthropic**: *Anthropic × DeepLearning.AI*. The Model Context Protocol for giving agents standard tool/data access. *Why:* MCP is the emerging interoperability layer for agent tools, directly relevant to skills 1 & 3. (https://learn.deeplearning.ai/courses/mcp-build-rich-context-ai-apps-with-anthropic/)

**Fine-tuning & open models (skill 1):**

- **Fine-tuning & RL for LLMs: Intro to Post-training**: (DeepLearning.AI, intermediate). SFT, preference tuning, RL for LLMs. *Why:* covers when to fine-tune (after the eval says prompt+RAG isn't enough) and how. (https://www.deeplearning.ai/courses/fine-tuning-and-reinforcement-learning-for-llms-intro-to-post-training/)
- **Finetuning Large Language Models**: *Sharon Zhou*. Practical LoRA/PEFT fine-tuning. *Why:* hands-on efficient fine-tuning.
- **Open Source Models with Hugging Face**: *Maria Khalusova, Younes Belkada, Marc Sun*. Using the Hub for text/audio/image/multimodal tasks. *Why:* open-weight models are central to sovereign/air-gapped deployments (highly relevant to Zorost's federal work). (https://www.deeplearning.ai/courses/open-source-models-hugging-face)

**LLMOps & deployment (skills 1 & 2):**

- **LLMOps**: *with Google Cloud (Erwin Huizenga)*. Data pipelines, fine-tuning, deployment, and monitoring on Vertex AI. *Why:* the production-operations layer of shipping an LLM app. (https://www.deeplearning.ai/courses/llmops)
- **Generative AI for Everyone**: *Andrew Ng*. Non-technical-but-real introduction to gen AI concepts. *Why:* onboarding stakeholders and framing business value.

> **Catalog root:** https://www.deeplearning.ai/courses/

### A.4 Vendor Agent Frameworks & Best-Practice References

These are the "how to build agents" canon from the major labs; the curriculum should treat them as primary reference material for skills 1 and 3.

- **Anthropic, "Building Effective Agents"** (Dec 2024). The most-cited agent-design essay. Core thesis: build the *simplest thing that works*, workflows (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer) before autonomous agents, and add agency only when the complexity buys reliability. Emphasizes augmenting LLMs with retrieval, tools, and memory, and separating "workflows" (code-orchestrated) from "agents" (model-directed). (https://www.anthropic.com/engineering/building-effective-agents)
- **Anthropic, "Claude Code Best Practices"** (2025). Practical guidance for *agentic coding*: write `CLAUDE.md` project instructions, work incrementally, keep a plan, use CLAUDE.md to prevent context re-explanation, and let the model verify its own work. Directly operationalizes Ng's skill 3 (using coding agents). (https://code.claude.com/docs/en/best-practices)
- **OpenAI, "A Practical Guide to Building Agents"** (2025). A ~34-page practitioner PDF covering single-agent vs. multi-agent design, the agent loop (reason → act → observe), tool design, guardrails, evals, and the Agent SDK. Complements Anthropic's essay with an SDK-and-deployment orientation. (https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
- **Google, "Agents" whitepaper** (2024, Kaggle; authors Julia Wiesinger, Patrick Marlow, Vladimir Vuskovic). Defines an agent as an application that uses an LLM plus **tools** and **orchestration** to achieve a goal, and walks through the cognitive architecture (model → orchestration → tools), extensions, functions, and data stores. (https://www.kaggle.com/whitepaper-agents)
- **Google, "Multi-Agent Systems" paper/whitepaper** (2025, Kaggle). A follow-up focused on multi-agent architectures and evaluation; part of Google's expanding agent-whitepaper series (Agents → Agents Companion → Multi-Agent Systems). Useful for the curriculum's advanced agent-design module. (https://www.kaggle.com/whitepaper-multi-agent-systems)
- **Microsoft, agent framework guidance** (Microsoft Agent Framework / Semantic Kernel / AutoGen, 2025). Microsoft's .NET "Microsoft Agent Framework" and the surrounding ecosystem (Semantic Kernel, AutoGen) document multi-agent orchestration, observability, and enterprise integration patterns. Represents the "agents inside enterprise platforms" perspective alongside Databricks/LangGraph. (https://learn.microsoft.com/en-us/dotnet/ai/ai-agents-dotnet)

---

## B. Key AI Engineering Textbooks & Major References

Each entry: what it contributes to a training curriculum.

### Core textbooks

- **Chip Huyen, *AI Engineering: Building Applications with Foundation Models* (O'Reilly, 2025).** The field-defining reference for the applied side of foundation models: how to build, evaluate, and operate products on top of LLMs. It systematically covers evals, RAG, agents, fine-tuning, and deployment, mapping almost one-to-one onto Ng's skill 1 and the evals/error-analysis core, and frames AI engineering as an *engineering* discipline (systems, tradeoffs, operations), not just prompting. This is the natural spine text for a 24-week applied curriculum. (O'Reilly; ISBN 978-1-098-16630-4)
- **Louis-François Bouchard & Louie Peters, *Building LLMs for Production* (2024).** A practical, chapter-by-chapter "make an LLM reliable in production" handbook covering prompting, RAG, fine-tuning, and deployment with concrete code. It's the practitioner's complement to Huyen: shorter, code-forward, and organized around the specific abilities (grounding, tool use, safety) that move an LLM from demo to production. Useful for the curriculum's "ship something real" weeks.
- **Jay Alammar & Maarten Grootendorst, *Hands-On Large Language Models* (O'Reilly, 2024).** The best *visual* guide to how LLMs work, from embeddings and attention through fine-tuning and deployment, with abundant diagrams and runnable notebooks. It builds the intuition (what the model actually computes) that Ng's skill 1 presumes, and pairs naturally with the authors' DeepLearning.AI course *How Transformer LLMs Work*. Ideal for the "internals" weeks.
- **Aurélien Géron, *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow*, 3rd ed. (O'Reilly, 2022).** The canonical classical-ML/neural-networks text: end-to-end ML project workflow, data prep, model selection, evaluation, and deep learning. *Why it matters now:* Ng argues ML/deep-learning evaluation instincts (metrics, test distributions, error analysis) transfer directly to generative AI, and classical ML is still the right tool for many tabular/structured problems (relevant to Zorost's forecasting, optimization, and decision-support work). This book supplies that foundation.

### Patterns, evals & practitioner essays

- **Eugene Yan, Bryan Bischof, Charles Frye, Hamel Husain, Jason Liu & Shreya Shankar, "What We Learned from a Year of Building with LLMs" (applied-llms, 2024; later an O'Reilly book, 2025).** The definitive synthesis of production LLM lessons across ~50 practitioners and dozens of companies, organized as ~42 tactics over tactics→operations→strategy. Its recurring themes, evals before features, the "long tail" of failure modes, RAG tradeoffs, prompt-and-context engineering, and measuring what matters, are the empirical backbone of the curriculum's applied modules. (https://applied-llms.org/ · https://github.com/eugeneyan/applied-llms · https://eugeneyan.kit.com/posts/what-we-ve-learned-from-a-year-of-building-with-llms)
- **Hamel Husain, "Your AI Product Needs Evals" (2024).** A short, influential essay arguing that evals, not model upgrades, are the highest-leverage investment for LLM products, with a practical taxonomy (unit tests for models, LLM-as-judge, and the "LMSys-style" intuition of testing on real tasks). It operationalizes the Ng evals-first message into a concrete engineering practice. (https://hamel.dev/blog/posts/evals/)
- **Chip Huyen, *Designing Machine Learning Systems* (O'Reilly, 2022).** The pre-foundation-model sibling of *AI Engineering*: data engineering, feature pipelines, training/eval/deploy, monitoring, and the human/organizational side of ML systems. Provides the *systems thinking* that skill 2 (software engineering fundamentals) and the "operations" half of an AI engineering program require.

### The agentic-coding evaluation landscape

These benchmarks define how "coding agents" (Ng's skill 3) are measured; the curriculum's evals modules should teach them as *concepts*, not just leaderboards.

- **SWE-bench / SWE-bench Verified** (Princeton, 2023 to 2024). A benchmark of real GitHub issues from popular Python repositories; an agent must produce a patch that makes hidden tests pass. **SWE-bench Verified** is a 500-task human-validated subset (a filtering step to remove under-specified issues) that became the standard leaderboard metric for coding agents in 2024 to 2026. *What it teaches:* how to measure "can an agent fix real bugs," and why a *validated* eval set matters. (https://www.swebench.com/ · paper arXiv:2310.06770)
- **Terminal-Bench** (Stanford/Laude Institute, 2025). A benchmark that runs agents against *terminal/CLI* tasks (shell, file systems, package management, config) rather than repository patches. *What it teaches:* coding agents are increasingly evaluated on end-to-end *computer use*, not just diffs, a broader and harder signal. (https://www.tbench.ai/ · paper arXiv:2504.06051)
- **τ-bench / τ²-bench** (Sierra Research, 2024 to 2025). Benchmarks for **tool-agent-user interaction** in realistic domains (retail, airlines) where an agent must use APIs and converse with a (simulated) user to satisfy a goal. *What it teaches:* evaluation of *agentic conversation + tool use*, the territory beyond code generation that dominates real AI products. (https://github.com/sierra-research/tau-bench · paper arXiv:2406.12045)

### Other major 2024 to 2026 references worth including

- **"What We Learned from a Year of Building with LLMs"** (see above), the single highest-signal practitioner reference.
- **Anthropic, "Building Effective Agents"** (see A.4), the canonical agent-design taxonomy.
- **Google's agent whitepaper series** (Agents, 2024; Agents Companion & Multi-Agent Systems, 2025), the canonical *definitions* and *architectures* for agents and multi-agent systems.
- **OpenAI, "A Practical Guide to Building Agents"** (2025), SDK-level agent construction and evaluation.
- **Microsoft Agent Framework / Semantic Kernel docs** (2025), enterprise multi-agent orchestration and observability.

---

## C. Zorost.com: Company Summary

*(Fetched live from https://zorost.com; content is server-rendered and fully captured.)*

### Identity, tone & focus

- **Tagline:** *"Find the Signal. Act with Intelligence."* Secondary positioning: *"Your trusted partner in enterprise AI."*
- **Location:** Washington, DC. Contact: info@zorost.com.
- **Self-description:** *"An engineering firm that builds, ships, and operates its own AI and data platforms."* The site's stance is **"built, not pitched"**, *"We don't pitch slide decks. We show you what we've already built in your domain, then engineer what your mission requires."*
- **Focus:** **regulated / mission-critical industries** where *"accuracy, traceability, and compliance are non-negotiable"*: aviation, freight & logistics, manufacturing, pharmaceutical research, finance, and government. The site repeatedly signals a **"calibration-first"** philosophy, *"honest uncertainty, not just accuracy"*, and emphasizes verification, audit trails, and provenance as first-class design goals.

### Services

**Commercial:** Generative & Agentic AI · Applied ML & Predictive Intelligence · Databricks Modernization Practice · Cloud Modernization & Data Engineering · AI Strategy, Governance & Responsible AI · Enterprise IT, API & Platform Engineering · Simulation, Digital Twin & Decision Support · Startups & Web Platforms.

**Federal** (SAM.gov registered; NAICS 541511 · 541512 · 541715 · 518210): Federal Decision Support Systems · Air-Gapped & Sovereign AI Deployments · Government Compliance & GovCon Operations · Geospatial & Decision Intelligence · Aviation & Transportation Intelligence · Legacy Reporting & Data Modernization · Government Contracting. Framed as *"calibration-first AI for federal missions, deployable in sovereign environments, engineered with governance and auditability from day one."*

### Databricks Modernization Practice

A **"Trusted Databricks Partner"** running a dedicated modernization practice: *"Legacy BI Migration · ETL Conversion → Lakeflow / DLT · Unity Catalog Governance · Mosaic AI & Agent Framework · Streaming & Dimensional Modeling · Cost Optimization & FinOps · Lakehouse-Native."* The stated promise: *"One governed platform for SQL, ML, streaming, and agentic AI."* Service is described end-to-end (*"Assessment to migration to operations"*), staffed by certified practitioners, in-house certifications listed: Data Engineer Professional, Machine Learning Professional, Generative AI Engineer, Data Engineer Associate, Spark Developer Associate. Expanded offering list: Legacy BI Migration; ETL Conversion → Lakeflow/Spark/DLT; Dimensional Modeling on Delta Lake; Streaming Pipelines; Unity Catalog Governance; Feature Engineering & MLOps; Mosaic AI · Vector Search · Serving · Gateway; Agentic Workflows on Databricks; Power BI / Tableau Modernization; Cost Optimization & FinOps.

### The AI Lab: six capabilities ("LAB/01 … LAB/06")

- **LAB/01 · Fusion**: the one capability detailed on the homepage: *"Six federal feeds, one regime-aware feature space."* Live surveillance, flow management, weather, and a 253K-report safety corpus are aligned on entity and time and re-scored on a 60-second lattice; a **regime detector** conditions every downstream model on the actual state of the airspace. Methods: entity resolution, temporal alignment, regime detection, semantic embedding. Scale figures: 6 federal feed families, 60s re-score cycle, 100M+ flight records, 253K+ safety reports embedded. Named feeds: FAA SWIM (SFDPS·TBFM·TFMS), ADS-B, Weather (METAR·TAF·NOAA), DOT/BTS, Safety Corpus (NTSB·ASRS), Advisories (NOTAM·PIREP·SIGMET).
- **LAB/02 · Modeling**: (named; detail on the capability page).
- **LAB/03 · Prediction**: (named).
- **LAB/04 · Optimization**: (named).
- **LAB/05 · Agents**: (named).
- **LAB/06 · Retrieval**: (named).

The Lab is pitched as *"six capabilities · seven applications · in production."*

### The seven applications ("built in the lab · run in production")

- **APP/01 · AeroFarr (Aviation Intelligence)**: *"The intelligence layer behind aviation decisions."* Fuses live surveillance, weather, and years of flight records into calibrated forecasts, verified causal chains, and executive briefings, with cascade prediction across the National Airspace System, re-scored continuously.
- **APP/02 · EvidAI (Pharma & Medical Affairs)**: *"The all-in-one evidence platform, from search to submission."* The full evidence lifecycle: dozens of literature sources + internal docs → PRISMA 2020 packages, GRADE profiles, manuscripts, and HEOR value dossiers. Orchestrated by auditable AI agents with **dual-reviewer enforcement**, living reviews, and an append-only audit trail.
- **APP/03 · AlchemyLake (Databricks-Native)**: *"Truth, made visible."* Open-core, governed creative production from lakehouse-trusted data: analyst chat, deep research, reports, presentations, infographics, and video/audio briefings. **Unity Catalog lineage** binds the numbers; every asset ships sealed with provenance. Databricks-native by design.
- **APP/04 · SPCio (Manufacturing)**: *"Quality intelligence from the factory line, even fully offline."* AI agents that understand SPC methodology and automotive standards: real-time X̄-R and I-MR control charts with Nelson rules, capability studies, Gage R&R, and AI-assisted PFMEA/control plans. Built for IATF 16949 and ISO 9001; air-gapped ready.
- **APP/05 · FreightCortex (Freight & Logistics)**: *"The intelligence layer for national freight."* An AI analyst over every freight flow, commodity, and corridor; plain-English queries, a simulation suite (cross-elasticity to economic shock), anomaly detection, and board-ready reporting.
- **APP/06 · ComplyGrid (Government Contracting)**: *"Compliance operations, in one grid."* DCAA-aligned timekeeping, contract/document intelligence, regulatory monitoring, and governance records for audit-ready GovCon operations.
- **APP/07 · Sigma Axion (Quantitative Finance)**: *"Quantitative. Systematic. Disciplined."* A quantitative trading platform for systematic event/equity strategies: research, execution, and risk in one surface, with layered risk controls, hard stops, pre-trade checks, fractional-Kelly sizing, and an append-only audit log.

### Research & open source

- **Aquil** (Monitoring), *"Global monitoring and decision support, from open signals to executive briefings."*
- **FreightCortex Consultant** (Consulting), analyst workspaces, scenario building, and client-ready reporting for freight consultancies.
- **DocPrep-AI** (OSS / RAG), *"Document intelligence that prepares enterprise knowledge for retrieval, local-first."*
- **MarkForge** (OSS / Publishing), *"Professional document conversion. Markdown in, publication-grade output."*
- **Weaviate Local UI** (OSS / Vector Data), *"A desktop studio for local vector databases and RAG prototyping."*
- **DevOps Monitor** (OSS / Observability), *"A ready-to-run observability stack for any application fleet."*

### AI Fieldwork program

*"The Lab above ships production platforms. AI Fieldwork is the open test bench beside it: we put models, agents, and AI tools through real work, publish live experiments anyone can enter, and record what held, what broke, and which calls stayed human. Numbered in sequence, dated, and honest about the limits."* Categories: Models · Agents · Tools · Experiments. Each entry has a Field Report/Experiment, a "Field Register" stating **The question / The subject / Not a claim about** (an explicit honesty boundary). Examples (numbered FW-01 → FW-07): **FW-07 Aerolex / Aircraft Encyclopedia** (265-aircraft-type catalog); **FW-06 "The Pupil"** (cosmology visualization; AI next to unsolved physics); **FW-05 yt2textbook** (YouTube → illustrated textbook, local, BYO key); **FW-04 Generative Flow Engine** (multi-agent physics/math visualization with architect/builder/auditor/verifier roles); **FW-03 Shadow Blade Duel** (Kimi K3 agentic game build through playtest-driven revision); **FW-02 River Strike: AI Campaign** (three-model relay: GLM-5.2 implement, GPT 5.6 Sol audit, Claude Fable 5 direct); **FW-01 Defy the Vector** (GPT 5.6 Sol WebGL flight experience under human review gates). The program is a live, public demonstration of Ng's coding-agent and external-feedback loops in practice.

### Signals blog (notable for this curriculum)

The **Signals** blog includes a post titled **"The AI Engineering Skills Map, turned into a training plan"** (16 AUG 2026), directly relevant to this curriculum effort. Other recent posts: "OneRead, a compiler for Simplified Technical English" (12 AUG 2026), "Running Kimi K3 locally: activation sparsity as architecture" (12 AUG 2026), "What a federal capability statement should actually say," "How a generated asset stays tied to the data it came from," "Comparing freight policy alternatives without a month-long study," "Architecture decisions to settle before approving AI at scale," "Geospatial AI for transportation and mobility," and "GeoParquet and the cloud-native geospatial stack" (all 24 JUL 2026). Blog categories: Aviation Intelligence, Manufacturing & Quality, Pharmaceutical Research, Freight & Logistics, Quantitative Finance, Geopolitical Intelligence, Government & Federal, Databricks Modernization, Agentic AI Engineering, Open Source.

---

## Sources

**Andrew Ng / DeepLearning.AI**

- Ng, *The AI Engineering Skills Map*, The Batch issue 366, 2026-08-14: https://www.deeplearning.ai/the-batch/issue-366 · https://x.com/AndrewYNg/status/2088302050706686198
- Ng, *Three Key Loops for Building Great Software*: https://www.deeplearning.ai/the-batch/three-key-loops-for-building-great-software
- Ng, *Make All Your Tokens (and Your Brainwork) Count*: https://www.deeplearning.ai/the-batch/make-all-your-tokens-and-your-brainwork-count
- Ng, *Coding Agents Accelerate Some Software Tasks More Than Others*: https://www.deeplearning.ai/the-batch/coding-agents-accelerate-some-software-tasks-more-than-others
- Ng, *Improve Agentic Performance with Evals and Error Analysis, Part 1*: https://www.deeplearning.ai/the-batch/improve-agentic-performance-with-evals-and-error-analysis-part-1
- Ng, *Improve Agentic Performance with Evals and Error Analysis, Part 2*: https://www.deeplearning.ai/the-batch/improve-agentic-performance-with-evals-and-error-analysis-part-2
- DeepLearning.AI course catalog: https://www.deeplearning.ai/courses/
- *How Transformer LLMs Work*: https://www.deeplearning.ai/short-courses/how-transformer-llms-work/
- *Large Language Models with Semantic Search* (Cohere): https://www.deeplearning.ai/short-courses/large-language-models-semantic-search/
- *AI Python for Beginners*: https://www.deeplearning.ai/courses/ai-python-for-beginners
- *Building Systems with the ChatGPT API*: https://www.deeplearning.ai/courses/chatgpt-building-system/
- *Evaluating and Debugging Generative AI*: https://learn.deeplearning.ai/courses/evaluating-debugging-generative-ai/
- *Building and Evaluating Advanced RAG*: https://www.deeplearning.ai/courses/building-evaluating-advanced-rag
- *Vector Databases: from Embeddings to Applications*: https://www.deeplearning.ai/courses/vector-databases-embeddings-applications
- *Knowledge Graphs for RAG*: https://www.deeplearning.ai/courses/knowledge-graphs-rag
- *AI Agents in LangGraph*: https://www.deeplearning.ai/courses/ai-agents-in-langgraph
- *Long-Term Agentic Memory With LangGraph*: https://www.deeplearning.ai/courses/long-term-agentic-memory-with-langgraph
- *MCP: Build Rich-Context AI Apps with Anthropic*: https://learn.deeplearning.ai/courses/mcp-build-rich-context-ai-apps-with-anthropic/
- *Fine-tuning & RL for LLMs: Intro to Post-training*: https://www.deeplearning.ai/courses/fine-tuning-and-reinforcement-learning-for-llms-intro-to-post-training/
- *Open Source Models with Hugging Face*: https://www.deeplearning.ai/courses/open-source-models-hugging-face
- *LLMOps* (Google Cloud): https://www.deeplearning.ai/courses/llmops
- *Preprocessing Unstructured Data for LLM Applications*: https://community.deeplearning.ai/t/new-course-enroll-in-preprocessing-unstructured-data-for-llm-applications/607757

**Vendor agent frameworks**

- Anthropic, *Building Effective Agents*: https://www.anthropic.com/engineering/building-effective-agents
- Anthropic, *Claude Code Best Practices*: https://code.claude.com/docs/en/best-practices
- OpenAI, *A Practical Guide to Building Agents*: https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- Google, *Agents* whitepaper (2024): https://www.kaggle.com/whitepaper-agents
- Google, *Multi-Agent Systems* whitepaper (2025): https://www.kaggle.com/whitepaper-multi-agent-systems
- Microsoft, Agent Framework (.NET / Semantic Kernel): https://learn.microsoft.com/en-us/dotnet/ai/ai-agents-dotnet

**Textbooks & references**

- Chip Huyen, *AI Engineering* (O'Reilly, 2025), ISBN 978-1-098-16630-4: https://www.oreilly.com/library/view/ai-engineering/9781098166298/
- Bouchard & Peters, *Building LLMs for Production* (2024): https://www.oreilly.com/library/view/building-llms-for/9798324731472/
- Alammar & Grootendorst, *Hands-On Large Language Models* (O'Reilly, 2024): https://www.oreilly.com/library/view/hands-on-large-language/9781098150952/
- Géron, *Hands-On Machine Learning*, 3rd ed. (O'Reilly, 2022): https://www.oreilly.com/library/view/hands-on-machine-learning/9781098125967/
- Yan, Bischof, Frye, Husain, Liu & Shankar, *What We Learned from a Year of Building with LLMs*: https://applied-llms.org/ · https://github.com/eugeneyan/applied-llms
- Hamel Husain, *Your AI Product Needs Evals*: https://hamel.dev/blog/posts/evals/
- SWE-bench / SWE-bench Verified: https://www.swebench.com/ · arXiv:2310.06770
- Terminal-Bench: https://www.tbench.ai/ · arXiv:2504.06051
- τ-bench / τ²-bench: https://github.com/sierra-research/tau-bench · arXiv:2406.12045

**Zorost**

- Zorost Intelligence homepage: https://zorost.com
