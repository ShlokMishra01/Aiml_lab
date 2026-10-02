# AI Engineering Lab: Glossary

> Every technical term in the program, in plain language. Terms are grouped by theme
> and ordered for reading; within each group, earlier terms build on later ones'
> prerequisites. Each entry ends with where the program teaches it in depth.
>
> **How to use this file:** don't read it cover to cover. When a week uses a word you
> don't know, jump to it (your editor's search is your friend), read the one-paragraph
> definition, and get back to work.

**Part of AI Engineering Lab · Developed by [Zorost Intelligence AI Lab](https://zorost.com) · zorost.com**

---

## Foundations: software & data

**API (Application Programming Interface)**: A way for one program to ask another
program to do something and get an answer back, over a fixed contract. When you "call
a model," your code is making an API request. *Week 1; KB-01.*

**CLI (Command-Line Interface)**: A program you drive by typing commands into a
terminal instead of clicking buttons. Most AI engineering tools (git, Ollama, Claude
Code) are CLIs. *Week 1.*

**Git / GitHub**: Git is version control: it records every change to your files so
you can undo, compare, and collaborate. GitHub is a website that hosts git
repositories so others can see and copy them. This program lives on GitHub. *Week 1.*

**IDE (Integrated Development Environment)**: A code editor with extras: file
browser, terminal, debugger, and extensions in one window. The program uses VS Code;
Cursor is an AI-native IDE. *Week 1; skills/cursor.*

**Jupyter / notebook**: An interactive document that mixes code cells, their output,
and written explanation. The program's hands-on work all happens in notebooks (`.ipynb`
files) so you can run one cell at a time and see what happened. *Week 1.*

**Library / package**: Pre-written code you import instead of writing from scratch.
`pandas` is a data library; `torch` is a deep-learning library. *Week 1.*

**Python**: The programming language of AI engineering, chosen for its readable
syntax and unmatched ecosystem of AI/data libraries. Taught from zero in Week 1.

**Repository ("repo")**: A folder of code tracked by git. This program is a
repository. *Week 1.*

**SQL (Structured Query Language)**: The language for asking questions of tabular
databases: `SELECT column FROM table WHERE condition`. AI engineering runs on data,
and data still speaks SQL. *Week 2; KB-02.*

**Terminal / shell**: The text window where you type commands directly to the
operating system (Terminal on macOS, PowerShell/Windows Terminal on Windows). *Week 1.*

**Virtual environment**: An isolated folder of Python packages for one project, so
one project's library versions can't break another's. You make one in Week 1 and never
think about it again. *Week 1.*

## Machine learning & deep learning

**Model**: A file of learned numbers (parameters) plus the code shape that uses them.
Given input, it produces output: an ETA, a category, or the next token. *Week 3.*

**Training**: The process where a model's parameters are automatically adjusted to
reduce its error on example data. Training is expensive; using a trained model
(inference) is cheap. *Week 3 to 4; KB-02.*

**Inference**: Using a trained model to make predictions on new input. Most of AI
engineering is inference-side: prompting, serving, evaluating. *Week 3; KB-02.*

**Feature**: An input variable you hand to a model: distance, carrier, day of week.
**Feature engineering** is crafting inputs the model can actually learn from. *Week 3;
Week 23.*

**Label / target**: The answer column in training data: the actual ETA, the true
on-time flag. Models learn by comparing predictions to labels. *Week 3.*

**Regression vs. classification**: Regression predicts a number (ETA in hours);
classification predicts a category (on-time vs. delayed). Week 3 builds one of each.

**Train/test split**: Holding out data the model never saw during training, to
measure how it performs on *new* cases, the only performance that matters. *Week 3.*

**Overfitting**: When a model memorizes the training data's noise and performs worse
on new data. The central failure mode of ML; the test split is how you detect it.
*Week 3 to 4; KB-02.*

**Neural network**: A model made of layers of simple units that multiply inputs by
learned weights and pass them through a non-linearity. Depth (many layers) lets it
learn complex patterns. *Week 4.*

**PyTorch**: The dominant open-source deep-learning framework. Week 4 builds a small
neural network in it so the "deep learning" in every LLM stops being magic. *Week 4.*

**Autograd / gradient descent**: The math that makes training work: compute how each
parameter contributed to the error (gradients), then nudge every parameter downhill.
PyTorch's autograd does the calculus for you. *Week 4; KB-02.*

**Embedding**: A dense vector of numbers representing meaning, so similar things land
near each other in vector space. Used inside LLMs and, separately, to power semantic
search. *Week 5; KB-03.*

## LLM core

**LLM (Large Language Model)**: A very large neural network trained to predict the
next token in text. That single capability, scaled, produces summarization, extraction,
reasoning, and dialogue. *Week 5; KB-03.*

**Token**: The chunk of text a model actually reads, roughly ¾ of an English word.
Costs, context limits, and speed are all measured in tokens. *Week 5; KB-03.*

**Tokenizer**: The component that cuts text into tokens and maps each to an integer
ID. Different models tokenize differently, so always measure with the actual model's
tokenizer. *Week 5.*

**Transformer**: The neural architecture behind every modern LLM: a stack of blocks,
each mixing self-attention (tokens gathering information from each other) with a small
feed-forward network. *Week 5; KB-03.*

**Attention / self-attention**: The mechanism that lets each token weigh which other
tokens matter to it ("it" in a sentence attending back to its noun). The Q·K·V
projection dance is explained visually in Week 5. *Week 5; KB-03.*

**Context window**: The maximum number of tokens a model can consider at once: your
instructions, the conversation, retrieved documents, and the model's own output all
compete for it. Managing it is *context engineering*. *Week 6; KB-04.*

**KV cache**: A serving optimization that stores each token's key/value vectors so
the model doesn't recompute attention for the whole prompt on every generated token.
Why the first token is slow and the rest stream fast. *Week 5; KB-03.*

**Temperature**: A sampling dial: low temperature makes output more predictable
(pick the most likely token); high temperature makes it more varied. Extraction tasks
run near zero. *Week 5 to 6.*

**Hallucination**: When a model states something false with full confidence, because
its job is producing plausible text, not verified fact. The engineering answers are
retrieval (give it the facts), structured output, and evals. *Week 6 to 7; KB-03.*

**Prompt**: Everything you put in front of the model: system instructions, examples,
the user's request, retrieved evidence. *Week 6.*

**System prompt**: The standing instructions sent with every request: role, policy,
output format, guardrails. It is a policy layer, not a security layer. *Week 6; KB-04.*

**Few-shot prompting**: Including 1 to 3 worked input→output examples in the prompt so
the model copies the *pattern*. One good example beats three mediocre ones. *Week 6.*

**Chain-of-thought**: Asking the model to reason step by step before answering.
Helps multi-step problems; costs tokens on every call. *Week 6; KB-04.*

**Structured output**: Constraining the model's answer to a schema (usually JSON) so
code, not a human, can consume it. Remember: a schema constrains shape, never truth.
*Week 6; KB-04.*

**Prompt injection**: An attack where instructions hidden in *content the system
reads* (a web page, a document field) hijack the model. OWASP's #1 LLM risk; defenses
live outside the prompt. *Week 6; KB-04.*

**Prompt caching**: A provider feature that reuses the processed prefix of repeated
requests, cutting cost and latency when your system prompt and context are stable.
*Week 6; KB-04.*

**RAG (Retrieval-Augmented Generation)**: Retrieve relevant documents, put them in
the context window, and ask the model to answer *from them*, with citations. The
default cure for hallucination and stale knowledge. *Week 7; KB-05.*

**Vector database**: A database that stores embedding vectors and finds the nearest
neighbors to a query vector fast. The retrieval half of RAG. *Week 7; KB-05.*

**Chunking**: Splitting documents into pieces small enough to embed and retrieve
usefully. Chunk size and overlap are among the highest-leverage RAG decisions. *Week 7.*

**Reranking**: A second-pass model that re-orders the vector search's top candidates
by true relevance. Cheap accuracy for RAG pipelines. *Week 7; KB-05.*

**Knowledge graph**: Data stored as entities and relationships (shipment, *carried_by*→
carrier), enabling multi-hop questions vector search can't answer. Week 7 builds one.

## Model engineering

**Open-weight model**: A model whose parameter files you can download and run
yourself (Llama, Qwen, Mistral, DeepSeek…). "Open source" in common speech, though
licenses vary. *Week 8; KB-06.*

**Foundation model**: A large model trained on broad data that you adapt to tasks,
by prompting, RAG, or fine-tuning, rather than training from scratch. *Week 8; KB-06.*

**Ollama / llama.cpp / MLX**: The three local-inference stacks the program uses:
Ollama for convenience, llama.cpp for control and GGUF, MLX for Apple Silicon. *Week 8;
skills/ollama-llamacpp; KB-08.*

**GGUF**: The file format llama.cpp uses for quantized models, one file you can
download and run anywhere. *Week 8 to 9.*

**Quantization**: Storing model weights at lower precision (16-bit → 8/6/5/4-bit) to
shrink memory and speed up inference, at a small quality cost. Q4_K_M is the classic
sweet spot. *Week 9; KB-06.*

**VRAM**: GPU memory. The hard wall for local models: the model's weights, the KV
cache, and the runtime must all fit. Week 8 to 9 teach you to size it before downloading.

**vLLM**: A high-throughput open-source serving engine for LLMs (paged attention,
continuous batching). What you graduate to when one user becomes fifty. *Week 9; KB-08.*

**Fine-tuning**: Continuing a model's training on your data to change its behavior:
tone, format, domain vocabulary. *Week 10; KB-06.*

**SFT (Supervised Fine-Tuning)**: Fine-tuning on input→ideal-output examples. The
first rung of behavior change. *Week 10.*

**LoRA (Low-Rank Adaptation)**: Fine-tuning a small set of added matrices instead of
all parameters: cheap, fast, and the resulting "adapter" file is tiny. *Week 10; KB-06.*

**DPO (Direct Preference Optimization)**: Training on pairs of "better vs. worse"
answers to align behavior with preferences, without a separate reward model. *Week 10.*

**Distillation**: Training a small model to imitate a big model's outputs, trading
capability for speed and cost. *KB-06.*

**Eval (evaluation)**: A repeatable measurement of a model or system's quality on a
fixed set of cases, producing a *score*. The discipline that separates AI engineers
from demo builders. *Week 11; KB-07.*

**Golden set**: The curated set of inputs with known-good answers that an eval scores
against. Fix the golden set before touching the prompt. *Week 6, 11.*

**LLM-as-judge**: Using a strong model to grade another system's outputs against a
rubric, when correctness is fuzzy (summaries, answers). Cheap and scalable, but must be
calibrated against human grades. *Week 11; KB-07.*

**Error analysis**: Reading real failures by hand, clustering them into categories,
and fixing the largest category first. The highest-ROI habit in the program. *Week 11;
KB-07.*

## Harnesses, loops & agents

**Harness (coding-agent harness)**: The software wrapper that lets an LLM act on your
computer: read files, run commands, edit code, with permissions, rules files, and
context management around it. Claude Code, Cursor, OpenCode, and the DeepSeek Harness
are the four the program compares. *Week 12; KB-09; reference/skills*

**Rules file**: The persistent instruction file a harness reads every session
(`CLAUDE.md`, `AGENTS.md`, `.cursor/rules`): project conventions, commands, and
boundaries. *Week 12; reference/skills*

**Subagent**: A spawned helper agent with its own context window, given a narrow job
(research, review) so the main agent's window stays clean. *Week 12; KB-09.*

**Verifier**: Anything that checks the agent's work automatically: tests, linters,
type checks, evals. Closing the loop means the agent runs its verifier itself. *Week 13.*

**Spec-driven development**: Writing the specification first and steering the agent
to it, so quality is judged against an explicit contract instead of vibes. *Week 13;
KB-01.*

**Agent**: A model in a loop with tools: observe → think → act → observe…, until done
or stopped. Agents handle tasks where the steps aren't known in advance. *Week 14;
KB-10.*

**ReAct**: The foundational agent pattern: interleave *reasoning* ("what should I do
next?") with *actions* (tool calls) in one loop. Week 14 builds one from scratch.

**Tool (function calling)**: A function the model can ask the harness to run:
`track_shipment(id)`. The model emits structured intent; your code executes it and
returns the result. *Week 14; KB-10.*

**Guardrails**: The hard limits around an agent: max steps, cost caps, refusal rules,
human approval for irreversible actions. *Week 14; KB-10.*

**Trace / observability**: A recorded log of every step an agent took, prompts, tool
calls, outputs, costs, so failures are debuggable and evaluable. *Week 17; KB-07, KB-10.*

**LangGraph**: A framework that models agents as explicit state graphs: nodes (steps),
edges (transitions), checkpoints (resumability). *Week 15; KB-10.*

**Multi-agent system**: Splitting work across specialized agents (router, tracker,
refunds) coordinated by an orchestrator. A measured trade, not a default. *Week 16;
KB-10.*

**MCP (Model Context Protocol)**: An open standard for exposing tools and data to AI
agents: one server, many compatible clients. Week 16 builds an MCP server for
ZoroLogistics. *Week 16; KB-11.*

**A2A (Agent-to-Agent)**: Google's protocol for agents delegating tasks to other
agents across boundaries; complements MCP's agent-to-tools focus. *KB-11.*

**OpenClaw**: An open-source personal-agent framework the program uses in Week 17 to
run a 24/7 assistant wired into the Week-16 MCP server. *Week 17; agents/openclaw.*

**Router / OpenRouter**: A service that fronts hundreds of models behind one API key,
so you can swap models, compare cost/quality, and use `:free` variants. *Week 12;
skills/openrouter.*

## Cloud platforms & Databricks

**Azure AI Foundry**: Microsoft's platform for building, evaluating, and deploying AI
apps and agents, with a model catalog and enterprise governance. *Week 18; KB-12.*

**Google Vertex AI**: Google Cloud's ML/GenAI platform: Gemini models, Agent Builder,
evaluation services, and MLOps. *Week 19; KB-12.*

**AWS Bedrock**: Amazon's managed service offering foundation models (Claude, Llama,
Nova…) via one API, plus Knowledge Bases, Agents, and Guardrails. *Week 20; KB-12.*

**Serverless endpoint**: Model hosting where you pay per request and never manage
servers; the opposite of provisioning a GPU instance yourself. *Week 18 to 20.*

**Lakehouse**: A data platform combining a data lake's cheap open storage with a data
warehouse's reliability and SQL performance. Databricks' core idea. *Week 21; KB-13.*

**Delta Lake**: The open storage layer (tables on object storage with ACID
transactions, time travel, schema enforcement) under the lakehouse. *Week 21.*

**Unity Catalog**: Databricks' governance layer: one place for data, model, and
permission management with lineage. *Week 21; platforms/databricks/01.*

**Medallion architecture**: Organizing data in bronze (raw) → silver (cleaned) →
gold (business-ready) tables. *Week 21 to 22.*

**PySpark**: The Python API for Apache Spark, the distributed compute engine that
processes data across a cluster. *Week 22.*

**Lakeflow (DLT & Jobs)**: Databricks' declarative pipeline and orchestration
tooling: declare the tables; it handles dependencies, retries, and monitoring.
*Week 22.*

**MLflow**: The open-source experiment-tracking and model-registry system: every
training run logged with parameters, metrics, and artifacts. *Week 23.*

**Feature store**: A governed home for computed features so training and serving use
identical definitions. *Week 23.*

**Model serving**: Putting a model behind an endpoint that applications call.
Databricks Model Serving, Foundry endpoints, and Vertex endpoints are the managed
versions. *Week 23; KB-12.*

**Vector Search / AI Search**: Databricks' managed vector database for RAG,
governed by Unity Catalog. *Week 23.*

**Genie**: Databricks' natural-language interface over governed data: ask in English,
get a governed SQL answer. *Week 23.*

**Agent Bricks**: Databricks' tooling for building and evaluating agents on platform
data. *Week 23 to 24.*

**DABs (Databricks Asset Bundles)**: Infrastructure-as-code for Databricks: the whole
project, jobs, pipelines, endpoints, declared in YAML and deployed with one command.
*Week 24.*

**CI/CD (Continuous Integration / Continuous Deployment)**: Automatically testing and
deploying code on every change, so production is never a manual leap of faith. *Week 24.*

**FinOps**: The discipline of measuring and controlling cloud/AI spend: budgets,
alerts, cost-per-query dashboards. *Week 24; platforms/databricks/17.*

**Governance**: The controls that make data and AI usable *safely* at scale:
permissions, lineage, audit, quality rules. The thread that runs through Week 21 to 24.

---

*Missing a term? That's a bug, open an issue or add it (see
[`.github/CONTRIBUTING.md`](../.github/CONTRIBUTING.md)).*

© 2026 Zorost Intelligence LLC · [zorost.com](https://zorost.com)
