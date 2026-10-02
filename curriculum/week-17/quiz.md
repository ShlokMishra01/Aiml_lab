# Week 17: Quiz (10 questions, 8/10 to pass)

> Each question names its source section or notebook cell. Answer, then check the key.

1. **(MCQ)** OpenClaw's memory model is "the model only remembers what gets saved to disk."
   Which file holds *stable preferences*, and which holds *durable facts/decisions*? (see
   Concepts §"OpenClaw: a personal assistant runtime" and `reference/agents/openclaw.md` §2.6)
   - (a) `MEMORY.md` for preferences; `USER.md` for facts.
   - (b) `USER.md` for preferences; `MEMORY.md` for facts.
   - (c) `DREAMS.md` for both.
   - (d) There is no file-based memory.

2. **(MCQ)** The OpenClaw permission tier, ordered least → most permissive, is: (see Concepts
   §"OpenClaw: a personal assistant runtime")
   - (a) `full → auto → ask → allowlist → deny`
   - (b) `deny → allowlist → ask → auto → full`
   - (c) `ask → deny → auto → full → allowlist`
   - (d) `allowlist → deny → full → auto → ask`

3. **(MCQ)** "Hermes" names two distinct things from Nous Research. Which statement is correct?
   (see Concepts §"Hermes: one name, two artifacts")
   - (a) Hermes is only a model; the framework is unrelated.
   - (b) Hermes the *model* is the brain you run; Hermes Agent is the *framework* that runs a model with a learning loop, gateway, and subagents.
   - (c) Hermes Agent is a model; Hermes is a benchmark.
   - (d) They are two names for the same artifact.

4. **(MCQ)** Why does pointing OpenClaw at Ollama's `/v1` endpoint break tool calling? (see
   Concepts §"Hermes" and `reference/agents/openclaw.md` §6)
   - (a) The `/v1` endpoint is slower.
   - (b) OpenClaw talks to Ollama's **native `/api/chat`**; `/v1` is the OpenAI-compatible endpoint and breaks tool calls.
   - (c) `/v1` requires a cloud subscription.
   - (d) It doesn't; `/v1` is required.

5. **(MCQ)** In the observability notebook, a **span** is: (see notebook cell [4] and Concepts
   §"Agent operations")
   - (a) one instrumented step with inputs, outputs, latency, and tokens, linked into a trace.
   - (b) the entire run's final answer.
   - (c) a model's parameter count.
   - (d) a message in a chat channel.

6. **(Short answer)** The cost dashboard prices `hermes-4-14b` at $0.00 per token. What *do* you
   pay for a local model instead, and why does the runbook still track it in the dashboard? (see
   notebook cell [9] and Concepts §"Worked example 1")

7. **(MCQ)** The production-eval sampling cell decides SHIP vs HOLD against a threshold of 0.85.
   If the sampled pass rate `p` is below 0.85, the decision printed is: (see notebook cell [11])
   - (a) SHIP
   - (b) HOLD, investigate before shipping
   - (c) RETRY with a larger sample
   - (d) No decision is printed

8. **(Short answer)** The final cell prints `COVERAGE` as `instrumented / total_ops` over 100
   operations, 85% of them traced. Explain what the *other* 15% represents and why the runbook
   targets 100% coverage rather than accepting 0.85. (see notebook cell [14] and Concepts
   §"Worked example 2")

9. **(MCQ)** Which is the single most common first-run OpenClaw failure, per
   `reference/agents/openclaw.md` §9.1? (see Concepts §"How it breaks")
   - (a) The Gateway port is always free.
   - (b) Tool calling breaks when pointed at Ollama's `/v1` endpoint.
   - (c) Skills always fire.
   - (d) The model remembers everything automatically.

10. **(Short answer)** Name the four things the ops runbook states, and explain in one sentence
    why a runbook is "a standing discipline" rather than documentation. (see notebook cell [13]
    and Concepts §"Agent operations")

---

## Answer key

1. **(b)**: `USER.md` holds stable preferences (who you are, how you like answers); `MEMORY.md`
   holds durable facts/decisions to persist.

2. **(b)**: `deny → allowlist → ask → auto → full`, from least to most permissive.

3. **(b)**: The model (Hermes 2/3/4) is the brain; Hermes Agent is the separate framework.
   They're independent artifacts you can mix and match.

4. **(b)**: OpenClaw uses Ollama's native `/api/chat`; the `/v1` endpoint is the
   OpenAI-compatible surface and breaks tool calling.

5. **(a)**: A span is one instrumented step (model call or tool call) with inputs, outputs,
   latency, and tokens; the trace is the sequence of spans for a run.

6. You pay in **hardware and latency** (the model runs on your machine), not per-token API
   spend. The dashboard still tracks it because an always-on assistant's *resource* cost and
   latency matter for the runbook's latency/cost alerts even at $0 marginal token cost.

7. **(b)**: HOLD (below 0.85): investigate before shipping.

8. The other 15% are operations that **bypass the tracer** (`untraced_step`). The runbook
   targets 100% because a failure in uninstrumented traffic is invisible, the 15% you don't
   trace is exactly where a silent regression will hide, so the metric is the honest "how much
   do we actually see?"

9. **(b)**: Tool calling breaking when pointed at Ollama's `/v1` endpoint is the most common
   first-run failure.

10. The runbook states: **thresholds** (pass rate, cost/day, latency, coverage), **dashboards to
    watch**, and **what-to-do-when** steps (for pass-rate drops, cost spikes, latency spikes, and
    low coverage). It is a standing discipline because it encodes the recurring decisions and
    thresholds you act on every day, not a one-time description you write and forget.
