# Hermes: Model Family vs. Agent Framework

> Part of AI Engineering Lab · Developed by Zorost Intelligence AI Lab · zorost.com

"Hermes" is overloaded, and getting it wrong causes real confusion. In an agents context
it refers to **two related-but-distinct things from Nous Research**:

1. **Hermes: the open-weight model family** (the "brain" you download and run).
2. **Hermes Agent: the agent framework** (the runtime that *uses* a model).

This guide covers both, clearly labeled, then shows how to run Hermes models locally and
use one as your ZoroLogistics triage-agent brain.

> **Note on fast-moving facts.** Model sizes, base architectures, and licenses change as
> new generations ship. Everything marked *"verify against live docs"* should be checked
> against the model cards and repos before citing.

---

## Part A: Hermes, the open-weight model family

Nous Research's **Hermes** models are instruction-tuned, open-weight LLMs strongly oriented
toward **instruction-following, function/tool calling, and agentic use**, plus a
reputation for strong roleplay/character and long-form generation.

### A.1 The generations

- **Hermes 2** (early 2024), a broad family across several bases (Llama 3, Mistral,
  Mixtral, Yi). The "Hermes 2 Pro" line added reliable function calling and
  JSON/structured-output modes.
- **Hermes 3** (Aug 2024), instruction-tuned on **Llama 3.1** (8B, 70B, 405B); marketed
  for function calling, structured outputs, roleplaying, and long context, using the
  ChatML format ([Hermes-3-Llama-3.1-405B](https://huggingface.co/NousResearch/Hermes-3-Llama-3.1-405B)).
- **Hermes 4** (late 2025), the current generation: **14B and 70B**, built on **Qwen3**
  bases, licensed **Apache 2.0**, with a "hybrid mode" reasoning toggle and strong
  agentic/function-calling orientation ([Hermes-4-14B](https://huggingface.co/NousResearch/Hermes-4-14B),
  [Hermes-4-70B](https://huggingface.co/NousResearch/Hermes-4-70B)).

> Verify the current Hermes 4 sizes, base model, and license against the live model cards,
> these are exactly the fast-moving facts that drift between generations.

### A.2 Strengths as an agent brain

- **Function/tool calling**: the whole point: Hermes models are tuned to emit reliable
  structured tool calls, which is the hard requirement for an agent loop.
- **Structured outputs**: JSON/format modes for feeding decisions into code.
- **Instruction-following and roleplay**: makes them comfortable in a persona'd assistant
  (e.g., a support-triage agent with a defined tone).
- **Apache 2.0 (Hermes 4)**: permissive, which matters for self-hosting and redistribution.

The tradeoff: small open models are **not frontier models**. Expect weaker long-horizon
reasoning and self-correction than a frontier API model, which is exactly what Week 17's
comparison measures.

### A.3 ChatML and the tool-calling lineage

Hermes models historically use the **ChatML** message format (distinct `<|im_start|>` /
`<|im_end|>` role delimiters), which matters for two practical reasons:

- **Correct templating**: you must apply the right chat template when serving or
  fine-tuning, or the model underperforms for no visible reason.
- **The "Pro" line**: the Hermes 2 Pro and later tool-calling tuning is what made reliable
  *function calling* (not just chat) a headline feature; that lineage carries through to
  Hermes 3/4 and is the main reason these are called "agentic" models.

When you use Ollama, the chat template is handled for you; when you serve raw HF weights
with vLLM, apply the model card's template explicitly.

### A.4 Hermes 4 "hybrid mode" reasoning

Hermes 4 advertises a **"hybrid mode" reasoning toggle**, the model can shift between
quick reflexive answers and more deliberate step-by-step reasoning. In agent terms this
maps onto the planning-vs-acting tradeoff from
[`reference/knowledge-base/10-agents-multiagent.md`](../knowledge-base/10-agents-multiagent.md) §2:
reserve the deliberative mode for the hard decomposition step and the fast mode for
routine tool calls, rather than paying reasoning cost on every turn. The exact toggle
mechanism is a model-specific detail, verify it against the model card.

---

## Part B: Hermes Agent, the agent framework

**Hermes Agent** (`NousResearch/hermes-agent`, MIT) is Nous Research's **open-source,
self-improving AI agent**, a *framework/application*, not a model
([repo](https://github.com/NousResearch/hermes-agent), [site](https://hermes-agent.nousresearch.com)). Highlights:

- **A closed learning loop**: creates *skills from experience*, self-improves them, nudges
  itself to persist knowledge, searches its own past conversations (FTS5 + LLM
  summarization), and builds a model of the user across sessions (via
  [Honcho](https://github.com/plastic-labs/honcho)); compatible with the
  [agentskills.io](https://agentskills.io) open standard.
- **One gateway process** reaching Telegram, Discord, Slack, WhatsApp, Signal, and CLI;
  includes a TUI, voice transcription, and cross-platform continuity.
- **Delegation & parallelism**: spawns isolated **subagents**, and can call tools via RPC
  from Python scripts to collapse multi-step pipelines into low-context-cost turns.
- **Model-agnostic**: use Nous Portal, OpenRouter, OpenAI, or your own endpoint; switch
  with `hermes model`.
- **Runs anywhere**: seven terminal backends (local, Docker, SSH, Singularity, Modal,
  Daytona, Vercel Sandbox), with serverless hibernation on some.
- **A2A support**: documented A2A (Agent-to-Agent) messaging, so Hermes can interoperate
  with other A2A-compliant agents ([Hermes A2A docs](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/a2a)).
- **Hermes Desktop**: a companion desktop app (artifacts, plugin SDK, quick-entry).

### B.1 Related: Nous Chat

**Nous Chat** is Nous Research's hosted chatbot product (its first release debuted access
to **Hermes 3-70B**): distinct from both the open-weight models and the Hermes Agent
framework ([VentureBeat](https://venturebeat.com/ai/unrestricted-ai-group-nous-research-launches-first-chatbot-with-guardrails)).

### B.2 The disambiguation in one line

> **Hermes the model** = the brain you run via Ollama/vLLM/HF. **Hermes Agent** = the
> framework that runs a model and gives it a learning loop, a gateway, and subagents. Hermes
> Agent *can* use Hermes models, but they are independent artifacts, you can put a Hermes
> model inside LangGraph, OpenClaw, or any other framework.

---

## Part C: Running Hermes models locally

### C.1 Ollama

The fastest path. Pull and run the GGUF quantizations:

```bash
ollama pull hermes4      # Hermes 4 (verify exact tag; hermes3 / hermes2 also exist)
ollama run hermes4
```

Ollama serves the model with function-calling support. This is the drop-in path for both
OpenClaw (§6 of [`openclaw.md`](openclaw.md)) and a local triage agent.

### C.2 vLLM

For high-throughput, OpenAI-compatible serving of the HF weights:

```bash
# serve NousResearch/Hermes-4-14B (or -70B) on an OpenAI-compatible endpoint
vllm serve NousResearch/Hermes-4-14B --max-model-len 16384
```

vLLM gives you batching, PagedAttention, and the tool-calling endpoint that a production
agent loop expects.

### C.3 Hugging Face / Transformers

Load the weights directly for fine-tuning or experimentation, the same path you learned
in Week 10.

### C.4 Expected hardware

A rough VRAM budget (verify exact quantization sizes against the model cards):

| Model | Quantization | Approx. VRAM | Fits on |
|---|---|---|---|
| Hermes 4 14B | Q4 (GGUF) | ~9 to 10 GB | 16 GB Apple Silicon / 12 GB GPU |
| Hermes 4 14B | FP16 | ~28 to 30 GB | 32 GB GPU |
| Hermes 4 70B | Q4 (GGUF) | ~40 GB | 48 GB GPU (or CPU with patience) |
| Hermes 4 70B | FP16 | ~140 GB | Multi-GPU |

Rule of thumb from Week 8: the **14B at Q4** is the sweet spot for a local agent brain on
a laptop; the **70B** needs a server-class GPU or a cloud endpoint.

### C.5 Evals

Judge a Hermes model the same way you judge any agent brain, on **your task, not the
leaderboard**:

1. Run the Week-11 **ZoroEval** golden sets (extraction, RAG, triage) against it.
2. Measure **tool-call accuracy** (does it emit the right tool + valid args?), the
   Hermes-specific strength.
3. Measure **self-correction** (does it recover from a tool error?), where small open
   models usually trail frontier APIs.
4. Track tokens/sec and cost as separate axes, a slower free model can still win if it's
   accurate enough for triage.

### C.6 Public evals & benchmarks

Open models ship with published benchmark numbers (e.g., on the Hugging Face **Open LLM
Leaderboard** and the model card's own table). Use them as a **filter, not a verdict**:

- They tell you roughly which size class is plausible for your task (can a 14B even *do*
  tool calling well? does the 70B justify its hardware cost?).
- They do **not** tell you how the model will behave on *your* triage task, with *your*
  tools, under *your* SLO. That is what ZoroEval is for (C.5).

A common mistake: citing a leaderboard score to justify a model swap, then discovering the
model's tool-call format or self-correction behavior doesn't fit the agent loop. Always
close the loop with a task eval.

---

## Part D: When Hermes-class models make good agent brains

Use a Hermes-class (or any strong tool-tuned open) model when:

- **You need local/private inference**: shipment data stays on-prem (a ZoroLogistics
  compliance constraint in some lanes).
- **The task is narrow and tool-shaped**: classification, extraction, tracking lookups,
  policy Q&A, where instruction/function-calling strength matters more than frontier
  reasoning.
- **Cost/latency at the edge**: many small calls beat one big model.

Reach for a frontier API model instead when the task needs **long-horizon planning,
hard self-correction, or multi-step reasoning under ambiguity**, the frontier gap is
largest exactly there.

A quick decision checklist:

- [ ] **Narrow and tool-shaped?** → strong case for a Hermes-class local model.
- [ ] **Privacy/compliance requirement** (data stays local)? → open model wins by default.
- [ ] **High call volume at the edge?** → local inference beats API per-call cost.
- [ ] **Long-horizon reasoning / hard self-correction?** → frontier API, or a much larger
      open model on a server.
- [ ] **Either way, run ZoroEval** → the decision is a measurement, not a preference.

---

## Part E, ZoroLogistics connection: Hermes as the triage brain

Week 17's experiment: run a Hermes model as the **triage-agent brain**, then compare it
against a frontier API model.

1. **Baseline first**: run the Week-16 triage agent with your frontier API model and
   record ZoroEval scores, latency, and cost on the same golden set.
2. **Swap the brain**: point the same agent loop at a local **Hermes 4 14B** (Ollama or
   vLLM). Change *only* the model, keep the prompt, tools, and MCP server identical.
3. **Measure the deltas** across three axes:
   - **Quality**: triage accuracy + tool-call validity + self-correction rate.
   - **Latency**: tokens/sec on local hardware vs. the API.
   - **Cost/privacy**: $0 marginal inference and data stays local vs. API spend.
4. **Decide like an engineer**: if Hermes is accurate enough on triage (a narrow,
   tool-shaped task, so it often is), the local model can win on cost and privacy; if the
   accuracy gap breaks the SLO, keep the frontier API and reserve Hermes for offline/edge
   lanes.

The deliverable is not "which model is better" in the abstract, it's **a measured,
task-specific decision with the data to defend it**, which is the whole discipline this
program installs.

---

## Sources

- Hermes-4-14B model card: https://huggingface.co/NousResearch/Hermes-4-14B
- Hermes-4-70B model card: https://huggingface.co/NousResearch/Hermes-4-70B
- Hermes-3 (Llama 3.1) model card: https://huggingface.co/NousResearch/Hermes-3-Llama-3.1-405B
- Hermes Agent framework: https://github.com/NousResearch/hermes-agent · https://hermes-agent.nousresearch.com (A2A: /docs/user-guide/messaging/a2a)
- Nous Research: https://nousresearch.com
- Nous Chat (VentureBeat): https://venturebeat.com/ai/unrestricted-ai-group-nous-research-launches-first-chatbot-with-guardrails

---

© 2026 Zorost Intelligence LLC · https://zorost.com
