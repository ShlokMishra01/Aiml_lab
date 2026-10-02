# Source Repo Analysis: `panteamkhh/llm-engineering-lab`

> Analysis for **AI Engineering Lab** curriculum planning. This is original critical analysis, not a copy of the source repository's content.

## Overview

The upstream repository **`panteamkhh/llm-engineering-lab`** (https://github.com/panteamkhh/llm-engineering-lab) brands itself as **"Generative AI Engineering: From Scratch → Understanding → Production Thinking."** It is a compact, ten-lesson learning path whose central thesis is that you should understand *how* generative AI works by building the primitive yourself (with plain Python, no framework) *before* reaching for the SDK or a framework.

**Stated purpose** (from `README.md`): a structured path to understand how generative AI actually works "by building everything step by step, before using any framework." The explicit learning philosophy is a four-stage loop: **Build It → Understand It → Use It → Ship It**.

**Prerequisites:** The README does **not** state formal prerequisites. They are implicit throughout the docs and code: working Python knowledge, a shell environment, and an OpenAI-compatible API key (`OPENAI_API_KEY`). Code samples assume `pip install openai` / `tiktoken` (sometimes with `--break-system-packages`, suggesting a Linux/system-Python assumption). There is no stated guidance on model access cost, GPU requirements (none are needed, all "Use It" work is hosted API calls), or an expected time budget.

**How it organizes learning:** ten numbered lessons, each a self-contained folder with three subdirectories, `docs/` (a single `en.md` lesson), `code/` (two scripts), and `outputs/` (one reusable markdown artifact). Each lesson follows a fixed six-stage internal structure (see below).

The repo is a **single-commit snapshot** (`git log` shows one commit: `docs: cross-link lesson references in markdown files`), with **43 tracked files**. It reads as a deliberately polished, near-static curriculum rather than an actively iterating project.

## Structure

### Full directory tree (2 to 3 levels)

```
llm-engineering-lab/
├── README.md
├── link_lessons.py                # cross-link maintenance utility
├── .gitignore
├── 01-foundations-of-generative-ai-and-llms/
│   ├── docs/en.md
│   ├── code/{tokenizer_from_scratch.py, real_tokenizer_and_completion.py}
│   └── outputs/model-selection-checklist.md
├── 02-responsible-generative-ai/
│   ├── docs/en.md
│   ├── code/{content_safety_check.py, harm_probe_harness.py}
│   └── outputs/responsible-ai-review-template.md
├── 03-prompt-engineering-fundamentals/
│   ├── docs/en.md
│   ├── code/{prompt_template_from_scratch.py, prompt_engineering_openai.py}
│   └── outputs/prompt-engineering-cheatsheet.md
├── 04-advanced-prompt-engineering/
│   ├── docs/en.md
│   ├── code/{prompt_evaluator_from_scratch.py, advanced_prompting_openai.py}
│   └── outputs/advanced-prompt-patterns.md
├── 05-building-text-generation-apps/
│   ├── docs/en.md
│   ├── code/{generation_loop_from_scratch.py, text_generation_app.py}
│   └── outputs/text-generation-parameter-guide.md
├── 06-building-chat-applications/
│   ├── docs/en.md
│   ├── code/{chat_session_from_scratch.py, chat_app.py}
│   └── outputs/chat-app-metrics-dashboard-spec.md
├── 07-search-apps-and-vector-databases/
│   ├── docs/en.md
│   ├── code/{semantic_search_from_scratch.py, rag_pipeline.py}
│   └── outputs/rag-architecture-diagram-and-checklist.md
├── 08-building-image-generation-apps/
│   ├── docs/en.md
│   ├── code/{image_prompt_builder_from_scratch.py, image_generation_app.py}
│   └── outputs/image-prompt-style-guide.md
├── 09-low-code-function-calling-and-ux/
│   ├── docs/en.md
│   ├── code/{function_calling_dispatcher_from_scratch.py, function_calling_openai.py}
│   └── outputs/ai-app-ux-checklist.md
└── 10-security-lifecycle-agents-and-fine-tuning/
    ├── docs/en.md
    ├── code/{react_agent_from_scratch.py, fine_tuning_workflow.py}
    └── outputs/production-readiness-checklist.md
```

**Consistent anatomy per lesson:**
- **`docs/en.md`**: the single source of truth for the lesson.
- **`code/`**: exactly two files: one `*_from_scratch.py` (the "Build It" toy implementation) and one SDK-based script (the "Use It" real version).
- **`outputs/`**: exactly one markdown deliverable, typically a checklist, reference card, or spec.

### Internal lesson structure (the six stages)

Every `docs/en.md` follows an identical header skeleton:

| Stage | Markdown header | Role |
|---|---|---|
| Framing | `# Lesson NN , Title` + a one-line `>` motto | Title + memorable thesis |
| Motivation | `## The Problem` | Why this matters in real systems |
| Theory | `## The Concept` (with `###` subsections) | Intuition before code |
| Primitive | `## Build It` | From-scratch implementation, no SDK |
| Production | `## Use It` | Real API / framework version |
| Deliverable | `## Ship It` | Names the `outputs/` artifact |
| Practice | `## Exercises` | 2 routine + 1 "Challenge" task |

## Module summaries

| # | Lesson | What it teaches | Key deliverable (`outputs/`) |
|---|---|---|---|
| 01 | Foundations of GenAI & LLMs | History, foundation model vs. LLM, open vs. proprietary, tokenization, deployment-strategy decision axis | `model-selection-checklist.md` |
| 02 | Responsible AI | Safety/risk taxonomy, harm probing, content filtering, incident response | `responsible-ai-review-template.md` |
| 03 | Prompt Engineering Fundamentals | Zero/one/few-shot, prompt anatomy (instruction/context/input/output-indicator), a template engine | `prompt-engineering-cheatsheet.md` |
| 04 | Advanced Prompt Engineering | Persona, chain-of-thought, delimiters, structured output, prompt evaluation | `advanced-prompt-patterns.md` |
| 05 | Text Generation Apps | Sampling parameters, streaming, error handling and retry | `text-generation-parameter-guide.md` |
| 06 | Chat Applications | Session state, memory, context-window management, chat metrics | `chat-app-metrics-dashboard-spec.md` |
| 07 | Search & Vector Databases | Embeddings, cosine similarity, RAG pipeline, chunking | `rag-architecture-diagram-and-checklist.md` |
| 08 | Image Generation Apps | Diffusion basics, image prompt grammar, a prompt-builder spec | `image-prompt-style-guide.md` |
| 09 | Function Calling & UX | Tool calling, function registry/dispatcher, AI-app UX patterns | `ai-app-ux-checklist.md` |
| 10 | Security, Lifecycle, Agents, Fine-tuning | Prompt injection, LLMOps, ReAct agents, fine-tuning workflow | `production-readiness-checklist.md` |

### Deep read of three modules

**Lesson 01: Foundations.** Teaches the conceptual substrate: a short history (ELIZA → statistical ML → Transformers/attention), the foundation-model vs. LLM distinction, an open-vs-proprietary comparison table, model categories, service-vs-self-host deployment, and tokenization as "text → numbers." The *Build It* script is a toy whitespace/regex tokenizer; the *Use It* script uses `tiktoken` (real BPE) plus a `gpt-4o-mini` completion call. Doc structure uses prose paragraphs, bullet lists, a numbered list, one markdown comparison table, and two fenced Python blocks. Style: concept-first prose, light on diagrams (text-only), heavy on "mental model" framing.

**Lesson 03: Prompt Engineering.** Teaches prompt anatomy (instruction/context/input/output-indicator), zero/one/few-shot, and a set of practical techniques (specificity, persona, task decomposition, output format, iteration). The *Build It* script is a `PromptTemplate` dataclass that renders few-shot examples; the *Use It* script compares zero-shot vs. few-shot through the OpenAI API. Notably, the doc opens with a "Quick recap" section that cross-links back to Lesson 01, evidence of the inter-lesson linking that `link_lessons.py` maintains. Structure: motto → Problem → Concept (with `###` subsections) → Build It → Use It → Ship It → Exercises. Style: prose + bullets + numbered lists + two code blocks.

**Lesson 10: Security / Lifecycle / Agents / Fine-tuning.** The capstone, and by far the densest doc (162 lines). Its *Concept* section is split into four parts: (1) security (prompt injection, data leakage, excessive agency, output abuse), (2) LLMOps lifecycle (experiment → evaluate → deploy → monitor → iterate), (3) AI agents (ReAct loop, tool integration, memory; and an explicit "agent vs. plain function-calling" decision), and (4) fine-tuning (when to fine-tune vs. RAG vs. prompt, and a 7-step workflow). *Build It* is a from-scratch ReAct agent loop with a `FUNCTION_REGISTRY` decorator and a fake planner; *Use It* is an OpenAI fine-tuning job (JSONL → upload → create → poll). Style: the most checklist- and taxonomy-heavy lesson, with numbered procedures, lots of cross-links to earlier lessons, and safety annotations inline in code comments.

### `link_lessons.py`: what it does

`link_lessons.py` is a **cross-linking maintenance utility**, not a teaching artifact. It enforces the "lessons reference each other by number" convention that runs through every `docs/en.md`.

- It holds a hard-coded map of `lesson_number → folder_name` and a `REPO_URL` base (`https://github.com/panteamkhh/llm-engineering-lab/tree/main`).
- It walks every `*/docs/*.md` file and applies **two regex passes**:
  1. **`fix_existing_links`**: finds existing markdown links whose text is a lesson number (`[Lesson 07](...)` or `[07](...)`) whose target "looks local" (a relative path, not already the canonical GitHub URL or any external `http(s)` URL), and rewrites the target to the canonical GitHub folder URL.
  2. **`link_plain_text`**: finds bare-text references like `Lesson 03`, `Lessons 01-09`, or `درس` (Arabic), and wraps each number in a markdown link to its lesson folder, **except** when it would self-link (same lesson number) or when the number is already inside a link.
- It supports `--dry-run` (preview only) and `--root` (repo root) flags, prints a per-file change summary, and reports a total.
- The `SEP` regex handles ranges/lists using `-`, en-dash, em-dash, comma, `and`, and `&`.

In short: it turns prose like "see Lesson 07" into clickable GitHub links and keeps them pointing at the canonical `main`-branch URLs, so docs stay navigable if the repo moves or relative paths drift. The single git commit is literally titled "docs: cross-link lesson references in markdown files," indicating this script produced that commit.

## Teaching patterns worth adopting

These are the source repo's genuinely strong, reusable design decisions:

1. **Numbered, sequential lessons with an explicit roadmap.** The README table maps `# → Lesson → Focus` and each lesson links back to its predecessors. Learners always know where they are in the arc (01 → 10 builds a narrative from "what is a token" to "how do I ship and operate this").

2. **The three-directory split: `docs/` + `code/` + `outputs/`.** Separates *explanation* (docs) from *executable proof* (code) from *reusable deliverable* (outputs). This is the single most transferable structural idea. The "outputs" artifacts are especially clever: each lesson ends by *producing a tool the learner keeps* (a checklist, a reference card, a spec), which reinforces the production mindset and gives a tangible portfolio trail.

3. **"Build It → Use It": from-scratch before SDK.** Every lesson teaches the primitive in dependency-free Python *first* (toy tokenizer, `PromptTemplate` dataclass, `FUNCTION_REGISTRY` ReAct loop, hand-rolled cosine similarity), then shows the same idea through the real API/framework. This de-mystifies the framework and encodes the philosophy "understand the mechanism before the abstraction."

4. **One-line motto per lesson.** Each doc opens with a single memorable sentence (`"Text in, tokens out…"`, `"The prompt is the interface…"`). These act as retrieval hooks and give every lesson a crisp, quotable thesis.

5. **The six-stage fixed template** (Problem → Concept → Build It → Use It → Ship It → Exercises). Uniformity lowers the cognitive cost of starting each new lesson and makes the curriculum feel coherent and predictable.

6. **Checklist/decision-guide artifacts.** The outputs are consistently operational ("run this before you ship"), not theoretical, a rare and valuable bias toward *decision-making* over *explanation*.

7. **Cross-linked lesson graph** maintained programmatically (`link_lessons.py`), so the material references itself as a coherent web rather than isolated pages.

8. **"Challenge" tier in every exercise set.** Each lesson closes with two routine exercises plus one open-ended, portfolio-grade challenge (e.g., "write unit tests for your prompt library"), which supports differentiated depth.

## Gaps vs. a 2026 AI engineering curriculum

The repo is a solid **2024-era LLM app primer**, but it stops well short of what a 2026 AI *engineering* program must cover. The gaps are structural, not cosmetic:

| Area | What the source does | What a 2026 curriculum must add |
|---|---|---|
| **Evals** | Mentions "evaluation" in LLMOps (Lesson 10) but ships no working eval harness | A first-class evals module: golden datasets, LLM-as-a-judge, rubric scoring, regression gates, A/B and diff testing, eval-as-CI. Evals should be a *cross-cutting spine*, not a bullet point. |
| **Agent frameworks** | A toy ReAct loop (Lesson 10) only | Real frameworks (LangGraph, AutoGen, Strands, OpenAI Agents SDK, Anthropic SDK), multi-agent orchestration, tool-use protocols, agent observability/tracing. |
| **MCP (Model Context Protocol)** | Absent entirely | MCP servers/clients, building and hosting custom MCP tools, tool auth, registry/curation. |
| **Harnesses** | A "prompt-evaluation harness" is named but is a 20-line stub | Agent/eval harnesses as infrastructure: deterministic test loops, sandboxed code execution, tracing (OpenTelemetry/LangSmith-style), reproducibility. |
| **Cloud AI platforms** | OpenAI API + one Azure OpenAI mention | Bedrock, Vertex AI, Azure AI Foundry (incl. Agents + Content Safety), multi-provider routing, cost/rate-limit management, model gateway patterns. |
| **Databricks** | Absent | Databricks Mosaic AI / Agent Framework, Unity Catalog governance, MLflow GenAI eval, serving endpoints, DLT pipelines, AI/BI, a whole "enterprise lakehouse AI" track. |
| **GPU / local stacks** | Zero local inference; all "Use It" is hosted | Ollama, llama.cpp, vLLM, quantization (GGUF/AWQ), local embeddings, running open weights end-to-end, hardware sizing. |
| **Excel / spreadsheet tracking** | Absent | The practical ops habit of tracking experiments, eval runs, and prompt versions in spreadsheets/CSV, a real-world engineering ritual the repo ignores. |
| **Streaming & structured output** | Streaming mentioned; no JSON-schema/structured-output enforcement | Streaming UX, JSON mode / structured outputs / function-call schemas enforced in production. |
| **Real vector DBs** | `fake_embed` + cosine similarity toy; no actual vector store | pgvector, Pinecone, Weaviate/Qdrant, hybrid search, reranking, chunking at scale, index maintenance. |
| **Observability / monitoring depth** | Lesson 06 ships a *spec* for a dashboard, no implementation | Actual tracing, latency/cost/quality dashboards, alerting, prompt-version telemetry, drift detection. |
| **Security depth** | Good taxonomy, but no OWASP LLM Top 10 reference, no hands-on red-teaming tooling | OWASP LLM Top 10, adversarial testing, guardrails SDKs, secret/tenant isolation, model-output validation pipelines. |
| **Open-weight fine-tuning** | OpenAI fine-tuning API only | LoRA/QLoRA on open models, dataset curation/formatting, Hugging Face/`unsloth`/`axolotl` workflows, RLHF/DPO awareness. |
| **Multimodal beyond images** | Image generation only | Vision/audio input, multimodal RAG, voice agents, document parsing (OCR/PDF) pipelines. |
| **Testing & reliability** | A few "write unit tests" hints | Systematic testing of nondeterministic systems: property tests, golden sets, replay, confidence calibration, failure-mode catalogs. |

The clearest summary: **the repo teaches "how to call a model and structure a prompt" extremely well, but it does not teach "how to make an AI system that is measured, versioned, governed, and safe at scale."** For 2026, the missing center of gravity is *evaluation-driven engineering* (evals + harnesses + observability), the *agent/MCP tooling layer*, and the *enterprise platform surface* (cloud AI platforms + Databricks), exactly the domains AI Engineering Lab is positioned to own.

## Adoption recommendations

For the AI Engineering Lab curriculum, **adopt the structural DNA, but rebuild the content ceiling.**

**Adopt as-is:**
1. The `docs/` + `code/` + `outputs/` three-way split, make it a hard standard for every module.
2. The numbered, roadmap-driven lesson sequence with an explicit focus table in the root README.
3. The fixed six-stage lesson template (Problem → Concept → Build It → Use It → Ship It → Exercises), it gives the whole program a uniform, predictable rhythm.
4. The "Build It (from-scratch) → Use It (real SDK/platform)" pairing, keep the no-framework-first philosophy as a differentiator.
5. One-line motto per lesson and checklist/decision-guide "outputs" artifacts as the terminal deliverable of each module.
6. Programmatically maintained cross-links (the `link_lessons.py` idea), generalize it into a curriculum-wide "module reference graph" tool.

**Extend / modernize (close the 2026 gaps):**
7. Insert an **evals module early** (by lesson 2 to 3) and treat eval harnesses as recurring infrastructure across all later modules, not a late add-on.
8. Add dedicated modules for **agent frameworks**, **MCP**, **cloud AI platforms**, **Databricks**, and **local GPU stacks**, these are the subjects the source repo omits entirely.
9. Make **"outputs" production-grade**: ship a runnable eval harness, a tracing config, an observability dashboard (not just a spec), and a spreadsheet/CSV tracking template for experiment logging.
10. Replace toy stubs (`fake_embed`, `fake_planner`, `fake_model_call`) with **real local tooling** (Ollama/vLLM for offline work, a real vector DB) so lessons run without a paid API key and teach real infrastructure.
11. Weave **Excel/CSV experiment tracking** into the workflow as a daily engineering ritual, matching how practitioners actually log runs alongside code.
12. Keep the security/Lifecycle module but **upgrade it to OWASP LLM Top 10 + hands-on red-teaming + guardrails**, and split agents/fine-tuning into their own deep modules rather than one catch-all capstone.

**Avoid copying:** do not lift prose, code, or artifacts verbatim, the analysis here is for structure and pedagogy only. The one-line mottos, the exact lesson titles, and the code samples are all the upstream author's work and must be re-authored in Zorost's own voice.

---

## Sources

- Upstream repository: https://github.com/panteamkhh/llm-engineering-lab (local clone at `/tmp/llm-engineering-lab`)
- Primary docs consulted (all read in full):
  - `README.md`
  - `01-foundations-of-generative-ai-and-llms/docs/en.md`
  - `03-prompt-engineering-fundamentals/docs/en.md`
  - `10-security-lifecycle-agents-and-fine-tuning/docs/en.md`
  - `link_lessons.py`
  - `01-foundations-of-generative-ai-and-llms/outputs/model-selection-checklist.md`
  - `10-security-lifecycle-agents-and-fine-tuning/outputs/production-readiness-checklist.md`
- Supporting scans (headers/mottos/artifacts/code sampled, not fully read): all remaining `docs/en.md` files (02, 04, 05, 06, 07, 08, 09), and representative `code/` files (`02-.../harm_probe_harness.py`, `07-.../semantic_search_from_scratch.py`).
