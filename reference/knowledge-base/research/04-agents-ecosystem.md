# AI Agents & Multi-Agent Systems: Research Notes

> AI Engineering Lab · Knowledge Base · Research
> Synthesized from official documentation, vendor engineering blogs, and primary GitHub READMEs. All claims cite original sources (see [Sources](#sources)). Written for an engineering audience building agentic systems in production.

---

## A) Agent Fundamentals

### A.1 The agent loop

An AI agent is a program that uses a language model to choose and execute actions toward a goal, rather than producing a single text answer. At its core an agent runs a loop:

1. **Perceive**: ingest the current state: the user's message, tool results, conversation history, and any retrieved context.
2. **Reason / plan**: the model decides what to do next (answer, ask a clarifying question, or call a tool) and, if needed, decomposes the goal into steps.
3. **Act**: the runtime executes the chosen action: a tool call, an API request, a code execution, a message send.
4. **Observe**: the result of the action is appended to context and fed back into the model.
5. **Repeat** until a **stopping condition** is met, then return a final answer to the user or caller.

The distinction that makes something an *agent* (versus a one-shot LLM call or a fixed pipeline) is that the model's own output determines the next step in a loop, with tools providing feedback. Anthropic's guidance is to reserve the word "agent" for systems where the LLM dynamically directs its own process and tool use, and to call deterministic, fixed-step LLM flows "workflows" instead ([Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)).

### A.2 ReAct: reasoning + acting

**ReAct** ("Reasoning and Acting," Yao et al., 2022) is the foundational prompting technique behind most modern agents. Instead of separating "think" from "do," ReAct interleaves *thought → action → observation* inside the model's output:

- **Thought**: the model narrates its reasoning about the current situation and what to try next.
- **Action**: the model emits a structured command (e.g., `Search[query]`, `Lookup[keyword]`).
- **Observation**: the tool's result is returned and becomes part of the prompt for the next cycle.

The key insight is that interleaving reasoning with external actions grounds the model in real data, reduces hallucination, and improves performance on knowledge-intensive and decision-making tasks compared to reasoning alone or acting alone. The original work is described in the Google Research blog post [ReAct: Synergizing Reasoning and Acting in Language Models](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/) (paper: arXiv:2210.03629).

### A.3 Tool / function calling

Tool calling is the runtime mechanism that turns the model's "action" into real execution. The flow:

1. A tool is declared to the model with a name, a JSON Schema describing its arguments, and a human-readable description.
2. When the model decides to act, it emits a **structured tool call** (a name + arguments), not free text.
3. The runtime validates the arguments, executes the function (or returns a validation error), and passes the result back as a new message.
4. The model continues reasoning with the result.

Important production nuances: tool descriptions are *prompt engineering* (the model only knows what you tell it), argument validation should fail fast with a clear error the model can self-correct from, and tool results consume context so they should be trimmed or summarized when large. OpenAI, Anthropic, Google, and open-weight runtimes (Ollama, vLLM) all expose function-calling APIs; open-weight models must be specifically instruction-tuned for tool use to emit reliable calls.

### A.4 Structured outputs

Structured outputs constrain the model to emit valid, schema-conformant data (JSON) instead of prose, essential for feeding agent decisions into code, APIs, and databases. Approaches include:

- **JSON Schema + function calling**: the model returns a tool call whose arguments conform to a declared schema (the most common approach).
- **Grammar-constrained decoding**: the sampler is restricted to tokens that keep output valid (used by vLLM, llama.cpp, Outlines, and provider "structured outputs" modes).
- **Pydantic-style validation**: the emitted JSON is parsed into typed objects and re-prompted on failure (the approach [Pydantic AI](https://ai.pydantic.dev) is built around).

### A.5 Planning

Planning techniques improve multi-step reasoning:

- **Chain-of-Thought (CoT)**: prompt the model to reason step-by-step before answering. Cheap, ubiquitous, and the default for decomposition.
- **Tree of Thoughts (ToT)**: generalize CoT to a tree: generate multiple candidate "thoughts," evaluate each, and search the tree (breadth/depth/backtracking) to find a path to the solution. Deliberate and more powerful, but far more expensive and usually reserved for hard search/planning problems ([Tree of Thoughts, arXiv:2305.10601](https://arxiv.org/abs/2305.10601)).
- **Plan-and-execute / planner-executor**: a planner model writes a task list, then an executor works through it; useful when the plan is stable and the executor is a weaker/cheaper model.

In practice, many production agents do *implicit* planning via CoT plus tool loops rather than explicit ToT-style search.

### A.6 Reflection / self-correction

**Reflexion** (Shinn et al., 2023) adds verbal self-feedback to the loop: after a failed attempt, the agent writes a *reflection*, a natural-language critique of what went wrong and what to do differently, stores it in memory, and retries with that reflection in context. This is a form of "verbal reinforcement learning" that improves performance on coding, reasoning, and decision tasks without weight updates ([Reflexion, arXiv:2303.11366](https://arxiv.org/abs/2303.11366); reference implementation at [noahshinn/reflexion](https://github.com/noahshinn/reflexion)). Common production forms: a "critic" step that reviews a draft before it is finalized, self-correction on tool-error feedback, and multi-turn retry loops with an explicit budget.

### A.7 Stopping conditions

A loop without a good termination rule is the classic agent failure mode. Standard stopping conditions include:

- **Explicit completion signal**: the model calls a `finish`/`submit` tool with a final answer.
- **Max iterations / max tool calls**: a hard safety cap.
- **Token / cost budget**: stop when context or spend exceeds a threshold.
- **No-progress detection**: terminate (or escalate) when repeated turns produce identical or non-advancing output.
- **Timeout**: wall-clock limits for interactive or long-running tasks.

### A.8 Guardrails & human-in-the-loop (HITL)

For agents that take consequential actions (payments, deploys, destructive ops), safety comes from layering controls:

- **Permission / allowlist policies**: only pre-approved commands or tools may run; everything else is denied or escalated.
- **Approval gates (HITL)**: a human must approve high-impact actions; often tiered (low-risk auto, medium-risk ask, high-risk require explicit sign-off).
- **Sandboxing**: run untrusted code or tool output in an isolated container/VM.
- **Input/output filters**: treat all inbound content as untrusted; scrub secrets; validate outputs against policy before they leave the system.
- **Audit trails / traces**: record every decision and tool call for post-hoc review and compliance.

The essential pattern is **least privilege + human checkpoint on irreversibility**. OpenClaw's permission modes (Section C) are a concrete reference implementation of this tiering.

### A.9 Context engineering for agents

"Context engineering" is the discipline of deciding *what the model sees* each turn, increasingly the highest-leverage part of agent work, since it shapes every decision.

- **System prompt**: the standing instructions: role, rules, tool-use policy, output format, guardrails. Should be stable, imperative, and as short as possible.
- **Short-term memory (in-context)**: the live conversation and tool results inside the current window. Fast and precise but bounded by the window and lost when the session ends.
- **Long-term / vector memory**: facts, preferences, and past decisions persisted outside the window (a database, vector store, or plain files) and *retrieved* into context when relevant. Enables cross-session recall at the cost of retrieval quality.
- **Context compaction**: when the window fills, summarize older turns into a compact block so the conversation can continue. Anthropic's compaction docs describe summarizing earlier messages and keeping recent ones intact, with a quality guard to preserve required details ([Compaction](https://platform.claude.com/docs/en/build-with-claude/compaction)). OpenClaw implements the same idea as auto-compaction plus a manual `/compact` (Section C).
- **Context editing**: surgically replace or remove stale blocks (e.g., a superseded file read, an outdated instruction) instead of a full summarize ([Context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)).
- **"Context loops"**: the repeated feedback cycle where tool output re-enters context and shapes the next decision. Two failure signatures: *context bloat* (irrelevant history accumulates and drowns the signal) and *context starvation* (important state was compacted away). Managing the loop, what to keep, summarize, and retrieve, is the heart of context engineering. Anthropic's "Effective harnesses for long-running agents" discusses running a stable agent over long horizons by managing state, compaction, and recovery ([Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)).

A useful mental model: **memory is what you persist; context is what you load.** A well-engineered agent keeps a small, curated long-term memory and lets retrieval/compaction decide what enters the window.

### A.10 Agent evaluation

Evaluating agents is harder than evaluating single LLM calls because the space of possible trajectories is huge and the output is a *process*, not just a final answer.

- **Traces**: full structured logs of the run: each step, tool call, arguments, result, and decision. Traces are the raw material for debugging and evals, and are the backbone of observability platforms (LangSmith, Langfuse, Phoenix/Arize, Braintrust, Weave, etc.).
- **Evals**: scripted tests with known-good answers, scored by exact match, LLM-as-judge, or rubric. Standard practice is a *suite*: unit evals per tool, end-to-end task evals, and safety/guardrail evals.
- **LLM-as-judge**: using a model to grade free-form outputs against a rubric; cheap and scalable but needs calibration against human labels.

Key public benchmarks:

| Benchmark | What it measures | Notes / source |
|---|---|---|
| **τ-bench / τ²-bench** (Sierra) | Agent ↔ tool ↔ *user* interaction in realistic domains (retail, airline, telecom): the agent must converse with a simulated user, call domain tools, and follow policy while satisfying the user | Simulated "user" model, double-checkable answers; [sierra-research/tau-bench](https://github.com/sierra-research/tau-bench) |
| **Terminal-Bench** (Stanford) | An agent's ability to solve tasks in a terminal/CLI environment (shell commands, file editing, package installs) | Complements SWE-bench by testing raw shell/CLI autonomy; [StanfordCRFM/terminal-bench](https://github.com/StanfordCRFM/terminal-bench) |
| **SWE-bench** (Princeton) | Coding agents: resolve real GitHub issues in real repositories; graded by hidden tests | De-facto standard for coding agents; [princeton-nlp/SWE-bench](https://github.com/princeton-nlp/SWE-bench), [swebench.com](https://www.swebench.com) |

---

## B) Multi-Agent Systems

### B.1 Why multi-agent (and when not to)

A **multi-agent system** splits a task across more than one model/agent, each with its own instructions, tools, and (often) context window. The benefits are real but conditional:

- **Context isolation**: each agent sees only what it needs, keeping windows small and focused.
- **Role specialization**: a researcher, a coder, and a reviewer each get prompts and tools tuned to one job.
- **Parallelism**: independent subtasks run concurrently, reducing wall-clock latency.
- **Failure isolation**: one agent's error or a poisoned context is contained rather than corrupting a single shared thread.

**The strong caveat (Anthropic's advice):** don't reach for multi-agent first. Start with a single, well-prompted agent plus good tools; add *workflows* (deterministic orchestration, prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer) before introducing multiple *agents*. Multi-agent adds coordination overhead, latency, cost, and new failure modes (bad handoffs, inconsistent context), so it is only justified when the isolation/specialization/parallelism benefits clearly outweigh that cost ([Building multi-agent systems](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them), [Common workflow patterns](https://claude.com/blog/common-workflow-patterns-for-ai-agents-and-when-to-use-them)).

### B.2 Orchestration patterns

- **Manager-worker / supervisor**: one orchestrator decomposes the task and delegates to specialist workers, then synthesizes their results. Simple, centralizes control, but the manager can become a bottleneck and its context can balloon.
- **Sequential pipeline**: agents pass work downstream in a fixed order (extract → transform → validate → publish). Deterministic and easy to reason about; a *workflow*, not a true multi-agent system.
- **Handoffs**: control passes from one agent to another mid-conversation (e.g., a triage agent hands a refund request to a billing agent). Preserves a single conversational thread with changing expertise (the model in OpenAI's Agents SDK).
- **Debate / peer-review**: multiple agents independently solve or critique, then reconcile. Improves correctness/reliability on hard reasoning tasks at several times the cost.
- **Swarm**: a large number of mostly homogeneous agents cooperate with emergent coordination (often research/demo territory; hard to control in production).
- **Hierarchical**: supervisors of supervisors; scales roles but compounds coordination cost and latency.

**Shared memory vs. message passing** is the core architectural fork: agents either coordinate through a *shared store* (blackboard/database that all read and write, flexible, decoupled, but with consistency and stale-read problems) or through *direct messages* (explicit agent-to-agent calls or a protocol like A2A, typed and auditable, but tighter coupling). Most production systems use a hybrid: message passing for control flow, a shared store for durable state.

### B.3 Communication protocols

#### MCP: Model Context Protocol

**MCP** (introduced by Anthropic in late 2024, now an open standard) standardizes how applications give models access to external **tools, resources, and prompts**, think "USB-C for AI integrations." Before MCP, every model↔tool integration was bespoke; MCP defines one client-server protocol so any MCP client can use any MCP server ([MCP architecture spec](https://modelcontextprotocol.io/specification/2025-03-26/architecture)).

Architecture roles:

- **Host**: the application that runs the LLM and initiates connections (e.g., Claude Desktop, an IDE, an agent framework).
- **Client**: lives inside the host; maintains one connection per server.
- **Server**: exposes capabilities (tools/resources/prompts) over the protocol; typically one per external system.
- **Primitives**: *Tools* (model-invoked functions), *Resources* (context/data the model can read), *Prompts* (reusable prompt templates).

Transports are typically **stdio** (local subprocess) or **streamable HTTP** (remote). Popular servers include: **filesystem**, **git/GitHub**, **memory/knowledge-graph**, **Postgres/SQLite** and other databases, **web search** (Brave/Tavily), **Puppeteer/browser**, **Slack**, **Google Drive**, and cloud SDKs (AWS, Azure, GCP). Registries/awesome-lists aggregate them (e.g., [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)). Most frameworks in Section E ship MCP client support.

#### A2A: Agent2Agent Protocol (Google)

**A2A** (announced by Google, April 2025) standardizes *agent-to-agent* interoperability: how one agent discovers, describes, and delegates work to another agent, including agents built by different vendors on different frameworks. Key primitives: an **Agent Card** (a JSON manifest describing the agent's capabilities, endpoints, and auth), **tasks** (long-running work units with lifecycle), and **messages/artifacts** for exchanging results ([Announcing the Agent2Agent Protocol (A2A)](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/), [a2a-protocol.org](https://a2a-protocol.org)).

**When to use which:**

- **MCP** = giving a *single* agent access to *tools/data* (capability layer: "connect my agent to this API/database").
- **A2A** = letting *agents talk to other agents* across systems (interop layer: "delegate this to a third-party agent").
- They are **complementary**, not competing: a common pattern is MCP for the tools an agent uses locally, A2A when it must hand work to another agent over a network. Microsoft AG2 ships native A2A support, and multiple vendors have adopted the protocol.

#### AGNTCY and other emerging standards (brief)

- **AGNTCY**: an open project (originated at Cisco/Outshift, donated to the **Linux Foundation** in 2025) to standardize multi-agent *infrastructure*: agent discovery, identity, connectivity, and observability, an "Internet of Agents" layer so agents from different vendors can find and work with each other ([Linux Foundation press release](https://www.linuxfoundation.org/press/linux-foundation-welcomes-the-agntcy-project-to-standardize-open-multi-agent-system-infrastructure-and-break-down-ai-agent-silos), [AGNTCY docs](https://docs.agntcy.org)).
- **AP2 / ACP / other drafts**: various agent-communication efforts exist; MCP and A2A are the two with the broadest adoption, while AGNTCY targets the orchestration/governance layer above them. Treat the rest as fast-moving and cite the specific spec before depending on it.

---

## C) OpenClaw (open-source personal AI assistant)

### C.1 What it is, and the naming history (verify carefully)

**OpenClaw** is an open-source **personal AI assistant that runs on your own devices and meets you in the messaging channels you already use** (WhatsApp, Telegram, Discord, Slack, Signal, iMessage, and a built-in WebChat). It is designed for a **single operator**, and it connects models, tools, messaging channels, and optional companion apps through one **Gateway** ([OpenClaw README](https://github.com/openclaw/openclaw)).

**Naming history** (important to get right, since it changed several times):

1. **Clawdbot**: the original viral project (late 2025).
2. **Moltbot**: renamed in January 2026; the project mascot is **"Molty," a space lobster**.
3. **OpenClaw**: the current name (a third rename, driven in part by trademark/impersonation pressure and crypto-scam squatting of earlier names).

The project was created by **Peter Steinberger (steipete)** and a large community; it is now developed in the open by the **OpenClaw Foundation** (a non-profit), licensed **MIT**, and built for "Molty the space lobster" ([TechCrunch naming history](https://techcrunch.com/2026/01/27/everything-you-need-to-know-about-viral-personal-ai-assistant-clawdbot-now-moltbot/), [OpenClaw README](https://github.com/openclaw/openclaw)). **Do not confuse** it with Anthropic's Claude, nor with any "OpenClaude" project, OpenClaw is an independent third-party open-source project; it is a *consumer of* LLM APIs (Anthropic, OpenAI, Google, local models), not an Anthropic product.

Repo: `github.com/openclaw/openclaw` · Docs: `docs.openclaw.ai` · Site: `openclaw.ai`.

### C.2 Key concepts

- **Gateway**: the local control plane (a daemon). It owns all messaging surfaces (WhatsApp via Baileys, Telegram via grammY, Slack, Discord, Signal, iMessage, WebChat, Google Chat), maintains provider connections, and exposes a typed **WebSocket** API on `127.0.0.1:18789`. Control clients (CLI, web UI, macOS app) and device **Nodes** (macOS/iOS/Android) connect to the same WS server ([Gateway architecture](https://docs.openclaw.ai/concepts/architecture)).
- **Channels**: the messaging services that bring the assistant to the user: WhatsApp, Telegram, Slack, Discord, Signal, iMessage, WebChat, Google Chat, and more.
- **Skills**: Markdown instruction files (`SKILL.md` with YAML frontmatter + a markdown body) that teach the agent *how and when* to use tools. Loaded from layered sources (workspace → project → personal → managed → bundled) with defined precedence, and filterable by environment/config ([Skills](https://docs.openclaw.ai/tools/skills)).
- **Plugins**: larger extension units built on a **plugin SDK**, distributed via **ClawHub** (`clawhub.ai`), the community registry for skills and plugins.
- **Agents model**: OpenClaw separates **provider** (auth/discovery) → **model** (the selected model) → **agent runtime** (the low-level loop that executes a turn) → **channel**. Runtimes include the built-in embedded `openclaw` loop plus harnesses like `codex`/`copilot`, and CLI backends (`claude-cli`). It supports **sub-agents** for isolated parallel workstreams ([Agent runtimes](https://docs.openclaw.ai/concepts/agent-runtimes)).
- **Memory**: plain Markdown files in the workspace: `USER.md` (stable preferences), `MEMORY.md` (durable facts/decisions), `memory/YYYY-MM-DD.md` (daily running notes), and `DREAMS.md` (an optional dream-diary/summary log). "The model only remembers what gets saved to disk; there is no hidden state" ([Memory](https://docs.openclaw.ai/concepts/memory)).
- **Context loop**: context is "everything OpenClaw sends to the model for a run": the OpenClaw-built system prompt, conversation history, and tool calls/results + attachments. It's bounded by the model's window; `/status`, `/context list|detail|map`, and `/usage tokens` inspect it. When the window fills, **compaction** summarizes older turns (keeping recent ones and tool-call/result pairs intact), auto-compaction is on by default, with a manual `/compact` and a "safeguard" quality mode ([Context](https://docs.openclaw.ai/concepts/context), [Compaction](https://docs.openclaw.ai/concepts/compaction)).

### C.3 Security model

- **Inbound messages are treated as untrusted input.** DM-capable channels pair unknown senders by default; a pairing request is approved with `openclaw pairing approve <channel> <code>`.
- **Permission modes** for host command execution (`tools.exec.mode`), a clear tiering reference: `deny` (block all) → `allowlist` (only listed commands) → `ask` (allowlist + prompt a human on misses) → `auto` (allowlist + auto-reviewer decides misses, falls back to human) → `full` (no prompts, trusted host only). A separate `tools.exec.host` setting chooses *where* commands run (host vs. sandbox) ([Permission modes](https://docs.openclaw.ai/tools/permission-modes)).
- **Sandboxing**: tools run on the host for the main session unless sandboxing is configured; the docs direct you to the sandboxing and exposure-runbook guides before connecting other users or exposing the Gateway remotely.

### C.4 Self-hosting & local models (Ollama)

Installers support macOS, Linux, Windows, and WSL2 (`curl -fsSL https://openclaw.ai/install.sh | bash`, or `npm install -g openclaw` for a managed Node install). Other paths include Docker and Nix ([Installation](https://docs.openclaw.ai/install)).

**Ollama support**: OpenClaw talks to Ollama's **native `/api/chat`** (not the `/v1` OpenAI-compatible endpoint, using `/v1` breaks tool calling). It supports three modes: **Cloud + Local**, **Cloud only**, and **Local only**; the canonical config is `baseUrl: "http://host:11434"` (no `/v1`). Onboarding auto-discovers installed local models that support tool calling with a ≥16K context window ([Ollama provider](https://docs.openclaw.ai/providers/ollama)).

### C.5 Step-by-step setup (condensed)

1. **Install**: run the install script (`curl -fsSL https://openclaw.ai/install.sh | bash`) or `npm install -g openclaw@latest`.
2. **Onboard**: `openclaw onboard --install-daemon` (verifies model access, creates the workspace, configures the Gateway). Pick a model provider; choose **Ollama** for local models.
3. **Verify the Gateway**: `openclaw gateway status`.
4. **Open the Control UI**: `openclaw dashboard`; send a message to confirm the assistant works.
5. **Connect a channel**: follow the [channels guide](https://docs.openclaw.ai/channels) for WhatsApp/Telegram/Discord/etc., then approve pairing requests for DM-capable channels.
6. **Extend**: add skills/plugins (from ClawHub or your own `SKILL.md` files), tune permission modes (`openclaw config set tools.exec.mode auto`), and read the [security guide](https://docs.openclaw.ai/gateway/security) before exposing it beyond yourself.

See the [Getting started guide](https://docs.openclaw.ai/start/getting-started) for the full, current walkthrough.

---

## D) "Hermes": model family vs. agent framework (disambiguate)

"Hermes" in an AI-agents context most plausibly refers to two related-but-distinct things from **Nous Research**. Distinguish them:

### D.1 Hermes: open-weight model family

Nous Research's **Hermes** models are instruction-tuned, open-weight LLMs strongly oriented toward instruction-following, function/tool calling, and agentic use.

- **Hermes 2** (early 2024), a broad family on several bases (Llama 3, Mistral, Mixtral, Yi); the "Hermes 2 Pro" line added reliable function calling and JSON/structured-output modes.
- **Hermes 3** (Aug 2024), instruction-tuned on **Llama 3.1** (8B, 70B, 405B); marketed for function calling, structured outputs, roleplaying, and long-context, using the ChatML format ([NousResearch/Hermes-3-Llama-3.1-405B](https://huggingface.co/NousResearch/Hermes-3-Llama-3.1-405B)).
- **Hermes 4** (late 2025), the current generation: **14B and 70B**, built on **Qwen3** bases, licensed **Apache 2.0**, with a "hybrid mode" reasoning toggle and strong agentic/function-calling orientation ([NousResearch/Hermes-4-14B](https://huggingface.co/NousResearch/Hermes-4-14B), [NousResearch/Hermes-4-70B](https://huggingface.co/NousResearch/Hermes-4-70B)).

**Running Hermes models:**

- **Ollama**: `ollama run hermes4` (or `hermes3`, `hermes2`) once the model is pulled; Ollama serves the GGUF quantizations.
- **vLLM**: serve the HF weights (`NousResearch/Hermes-4-14B`, etc.) with a compatible engine for high-throughput API serving.
- **Hugging Face / Transformers**: load the weights directly for fine-tuning or experimentation.

The Hermes *models* are the thing you'd pick as the "brain" inside an agent framework (including Hermes Agent or any other framework in Section E).

### D.2 Hermes Agent: the agent framework

**Hermes Agent** (`NousResearch/hermes-agent`, MIT) is Nous Research's **open-source, self-improving AI agent**. It is a *framework/application*, not a model. Highlights from the README ([NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent), [hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com)):

- **A closed learning loop**: creates *skills from experience*, self-improves them, nudges itself to persist knowledge, searches its own past conversations (FTS5 + LLM summarization), and builds a model of the user across sessions (via [Honcho](https://github.com/plastic-labs/honcho)); compatible with the [agentskills.io](https://agentskills.io) open standard.
- **One gateway process** reaching Telegram, Discord, Slack, WhatsApp, Signal, and CLI; includes a TUI, voice transcription, and cross-platform continuity.
- **Delegation & parallelism**: spawns isolated **subagents**, and can call tools via RPC from Python scripts to collapse multi-step pipelines into low-context-cost turns.
- **Model-agnostic**: use Nous Portal, OpenRouter, OpenAI, or your own endpoint; switch with `hermes model`.
- **Runs anywhere**: seven terminal backends (local, Docker, SSH, Singularity, Modal, Daytona, Vercel Sandbox), with serverless hibernation on some.
- **A2A support**: documented A2A (Agent-to-Agent) messaging, enabling Hermes to interoperate with other A2A-compliant agents ([Hermes A2A docs](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/a2a)).
- **Hermes Desktop**: a companion desktop app (artifacts, plugin SDK, quick-entry) in the same repo.

### D.3 Related: Nous Chat

**Nous Chat** is Nous Research's hosted chatbot product (the first release debuted access to **Hermes 3-70B**), distinct from both the open-weight models and the Hermes Agent framework ([VentureBeat: Nous Research launches first chatbot](https://venturebeat.com/ai/unrestricted-ai-group-nous-research-launches-first-chatbot-with-guardrails)).

**Summary disambiguation:** Hermes = (1) open-weight *models* (Hermes 2/3/4) you run via Ollama/vLLM/HF, and (2) the *Hermes Agent* *framework* (a self-improving, multi-surface agent runtime). Hermes Agent can use Hermes models, but they are independent artifacts.

---

## E) Agent Frameworks: Comparison & Selection

### E.1 Comparison table

| Framework | Language(s) | Best fit | Learning curve | MCP support | Multi-agent support |
|---|---|---|---|---|---|
| **LangGraph** | Python, JS/TS | Low-level control over complex, stateful, cyclic workflows; production-grade persistence | High (you build the graph yourself) | Yes (client via `langchain-mcp-adapters`) | Yes (subgraphs, supervisor patterns; manual) |
| **CrewAI** | Python (TS in beta) | Role-based "crews" of agents for business/ops automation | Low-moderate (declarative) | Yes | Yes (core value: crews, hierarchical) |
| **AutoGen → AG2 / Microsoft Agent Framework** | Python (AG2), Python/.NET (Agent Framework) | Multi-agent conversations, research, enterprise Azure/AI Foundry | Moderate | Yes (both) | Yes (core strength) |
| **OpenAI Agents SDK** | Python, TS | Lightweight agents on OpenAI models; handoffs, guardrails, tracing | Low | Yes (client) | Yes (handoffs + agents as tools) |
| **smolagents** | Python | Minimal, hackable agents; "code as actions" | Low | Yes (client) | Basic (managed agents) |
| **Pydantic AI** | Python | Type-safe, validated agents for engineers who want structured I/O | Low-moderate | Yes (client + server) | Limited (multi-agent via tool/agent composition) |
| **Mastra** | TypeScript | TS-native agents + workflows + RAG, framework-agnostic models | Moderate | Yes (client + server) | Yes (networks/agents) |
| **LlamaIndex Workflows** | Python (+ TS) | Event-driven, async orchestration over data/RAG pipelines | Moderate | Yes (via integrations) | Yes (nested workflows/agents) |

### E.2 Framework notes

- **LangGraph**: models agents as explicit **state graphs** (nodes = steps, edges = transitions) with first-class **checkpointing/persistence** for durability, human-in-the-loop interrupts, and time-travel. Most control, most boilerplate. Official docs: [LangGraph](https://docs.langchain.com/oss/python/langgraph), [Checkpointers](https://docs.langchain.com/oss/python/langgraph/checkpointers).
- **CrewAI**: role-based agents with goals/backstories assembled into **crews** with tasks; high-level and fast to prototype, with process modes (sequential/hierarchical). [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI), [docs.crewai.com](https://docs.crewai.com).
- **AutoGen lineage**: Microsoft's original **AutoGen** (multi-agent "conversations") evolved and was eventually **retired/deprecated in favor of Microsoft Agent Framework**; **AG2** is the community-maintained fork that continues AutoGen's API and adds native **A2A** support. Choose **AG2** for the open community path or **Microsoft Agent Framework** for Azure/AI Foundry integration ([AG2](https://github.com/ag2ai/ag2), [Microsoft Agent Framework](https://learn.microsoft.com/agent-framework)).
- **OpenAI Agents SDK**: a minimalist, production-lean SDK: **agents**, **handoffs**, **guardrails**, **sessions**, and built-in **tracing**; batteries-included if you're on OpenAI models ([openai/openai-agents-python](https://github.com/openai/openai-agents-python)).
- **smolagents**: Hugging Face's "barebones" library; two agent types, **CodeAgent** (expresses actions as executable Python, a strong, token-efficient pattern) and **ToolCallingAgent**; great for learning and for keeping full control ([huggingface/smolagents](https://github.com/huggingface/smolagents), [docs](https://huggingface.co/docs/smolagents)).
- **Pydantic AI**: agent framework built around **Pydantic** type safety: every input/output is validated, structured results and dependency injection are first-class; excellent for engineers who want guarantees at the type boundary ([pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai), [ai.pydantic.dev](https://ai.pydantic.dev)).
- **Mastra**: TypeScript framework for agents, **workflows** (durable, typed steps), RAG, and evals; model-agnostic; strong MCP client+server support ([mastra-ai/mastra](https://github.com/mastra-ai/mastra), [mastra.ai](https://mastra.ai)).
- **LlamaIndex Workflows**: **event-driven, async-first, step-based** orchestration where steps emit/consume events; lightweight and composable, and the basis of the `llama-agents` multi-agent service layer ([Workflows 1.0 announcement](https://www.llamaindex.ai/blog/announcing-workflows-1-0-a-lightweight-framework-for-agentic-systems), [run-llama/llama-agents](https://github.com/run-llama/llama-agents)).

### E.3 Selection guidance

1. **Start simplest.** For most tasks, a single agent with good tools beats a multi-agent system. Pick a framework that adds the *least* machinery: OpenAI Agents SDK (if on OpenAI), smolagents or Pydantic AI (Python), Mastra (TypeScript).
2. **Need durable, auditable, cyclic control flow** (checkpoint/resume, human approval mid-flow) → **LangGraph**.
3. **Want role-based team abstraction and fast prototyping** → **CrewAI**.
4. **Deep multi-agent research / enterprise Azure** → **AG2** or **Microsoft Agent Framework**.
5. **Heavy data/RAG pipelines with event-driven orchestration** → **LlamaIndex Workflows** (+ `llama-agents`).
6. **Require MCP everywhere** → most frameworks support MCP clients; verify server-side needs against LangGraph, Pydantic AI, Mastra, or smolagents.
7. **Language constraint is often the deciding factor**: TypeScript teams default to Mastra (or LangGraph.js); Python teams have the widest field.

---

## Sources

**Agent fundamentals & multi-agent guidance**
- Anthropic, Building Effective Agents: https://www.anthropic.com/engineering/building-effective-agents
- Anthropic, Building multi-agent systems (when and how): https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them
- Anthropic, Common workflow patterns for AI agents: https://claude.com/blog/common-workflow-patterns-for-ai-agents-and-when-to-use-them
- Anthropic, Effective harnesses for long-running agents: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Anthropic, Compaction: https://platform.claude.com/docs/en/build-with-claude/compaction
- Anthropic, Context editing: https://platform.claude.com/docs/en/build-with-claude/context-editing
- Google Research, ReAct (blog): https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/ (paper: arXiv:2210.03629)
- Tree of Thoughts (Yao et al.): https://arxiv.org/abs/2305.10601
- Reflexion (Shinn et al.): https://arxiv.org/abs/2303.11366 · https://github.com/noahshinn/reflexion

**Evaluation & benchmarks**
- τ-bench / τ²-bench (Sierra): https://github.com/sierra-research/tau-bench
- Terminal-Bench (Stanford): https://github.com/StanfordCRFM/terminal-bench
- SWE-bench (Princeton): https://github.com/princeton-nlp/SWE-bench · https://www.swebench.com

**Communication protocols**
- MCP specification, Architecture: https://modelcontextprotocol.io/specification/2025-03-26/architecture · https://modelcontextprotocol.io
- Google, Announcing the Agent2Agent Protocol (A2A): https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/ · https://a2a-protocol.org
- AGNTCY, Linux Foundation press release: https://www.linuxfoundation.org/press/linux-foundation-welcomes-the-agntcy-project-to-standardize-open-multi-agent-system-infrastructure-and-break-down-ai-agent-silos · https://docs.agntcy.org

**OpenClaw**
- Repository: https://github.com/openclaw/openclaw
- Docs: https://docs.openclaw.ai (Gateway architecture: /concepts/architecture · Context: /concepts/context · Compaction: /concepts/compaction · Memory: /concepts/memory · Skills: /tools/skills · Permission modes: /tools/permission-modes · Agent runtimes: /concepts/agent-runtimes · Ollama: /providers/ollama · Getting started: /start/getting-started)
- Naming history (TechCrunch): https://techcrunch.com/2026/01/27/everything-you-need-to-know-about-viral-personal-ai-assistant-clawdbot-now-moltbot/
- Site: https://openclaw.ai

**Hermes (Nous Research)**
- Hermes-4-14B model card: https://huggingface.co/NousResearch/Hermes-4-14B
- Hermes-4-70B model card: https://huggingface.co/NousResearch/Hermes-4-70B
- Hermes-3 (Llama 3.1) model card: https://huggingface.co/NousResearch/Hermes-3-Llama-3.1-405B
- Hermes Agent framework: https://github.com/NousResearch/hermes-agent · https://hermes-agent.nousresearch.com (A2A: /docs/user-guide/messaging/a2a)
- Nous Research: https://nousresearch.com
- Nous Chat (VentureBeat): https://venturebeat.com/ai/unrestricted-ai-group-nous-research-launches-first-chatbot-with-guardrails

**Frameworks**
- LangGraph: https://docs.langchain.com/oss/python/langgraph · https://docs.langchain.com/oss/python/langgraph/checkpointers
- CrewAI: https://github.com/crewAIInc/crewAI · https://docs.crewai.com
- AG2: https://github.com/ag2ai/ag2
- Microsoft Agent Framework: https://learn.microsoft.com/agent-framework
- OpenAI Agents SDK: https://github.com/openai/openai-agents-python
- smolagents: https://github.com/huggingface/smolagents · https://huggingface.co/docs/smolagents
- Pydantic AI: https://github.com/pydantic/pydantic-ai · https://ai.pydantic.dev
- Mastra: https://github.com/mastra-ai/mastra · https://mastra.ai
- LlamaIndex Workflows: https://www.llamaindex.ai/blog/announcing-workflows-1-0-a-lightweight-framework-for-agentic-systems · https://github.com/run-llama/llama-agents
