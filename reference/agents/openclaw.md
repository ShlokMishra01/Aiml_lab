# OpenClaw: Practical Guide

> Part of AI Engineering Lab · Developed by Zorost Intelligence AI Lab · zorost.com

OpenClaw is the personal-AI-assistant track of Week 17: an open-source assistant that
runs on *your* devices and meets you in the messaging channels you already use. This guide
walks through what it is, how it's architected, how to install and run it, how to point it
at a local model, and how to wire it to your Week-16 MCP server.

> **Note on fast-moving facts.** OpenClaw renamed itself several times, and its config keys
> and channel list change frequently. Everything marked *"verify against live docs"* below
> should be checked at [docs.openclaw.ai](https://docs.openclaw.ai) before you rely on it.

---

## 1. What OpenClaw is

**OpenClaw** is an open-source **personal AI assistant that runs on your own devices and
meets you in the messaging channels you already use**, WhatsApp, Telegram, Discord, Slack,
Signal, iMessage, and a built-in WebChat. It is designed for a **single operator**, and it
connects models, tools, messaging channels, and optional companion apps through one
**Gateway** ([OpenClaw README](https://github.com/openclaw/openclaw)).

Key facts to keep straight:

- **License:** MIT.
- **Creator:** originally created by **Peter Steinberger (steipete)** and a large
  community; now developed in the open by the **OpenClaw Foundation**, a non-profit.
- **Mascot:** "Molty," a space lobster.
- **Repo:** `github.com/openclaw/openclaw` · **Docs:** `docs.openclaw.ai` · **Site:** `openclaw.ai`.

### 1.1 The naming history (get it right)

The project was renamed several times, and the history matters because older tutorials
still use the old names:

1. **Clawdbot**: the original viral project (late 2025).
2. **Moltbot**: renamed in January 2026; the "Molty the space lobster" mascot dates from here.
3. **OpenClaw**: the current name (a third rename, driven in part by trademark /
   impersonation pressure and crypto-scam squatting of earlier names).

([TechCrunch naming history](https://techcrunch.com/2026/01/27/everything-you-need-to-know-about-viral-personal-ai-assistant-clawdbot-now-moltbot/))

**Do not confuse OpenClaw with** Anthropic's *Claude*, or with any "OpenClaude" project.
OpenClaw is an independent third-party open-source project, a *consumer of* LLM APIs
(Anthropic, OpenAI, Google, and local models), not an Anthropic product.

---

## 2. Architecture

The mental model is one local control plane plus several pluggable surfaces.

### 2.1 Gateway

The **Gateway** is the local control plane (a daemon). It:

- owns all messaging surfaces (WhatsApp via Baileys, Telegram via grammY, Slack, Discord,
  Signal, iMessage, WebChat, Google Chat, and more);
- maintains provider (model) connections;
- exposes a typed **WebSocket** API on `127.0.0.1:18789` (verify against live docs).

Control clients (CLI, web UI, macOS app) and device **Nodes** (macOS/iOS/Android) connect
to that same WS server ([Gateway architecture](https://docs.openclaw.ai/concepts/architecture)).

### 2.2 Channels

Channels are the messaging services that bring the assistant to you: **WhatsApp, Telegram,
Slack, Discord, Signal, iMessage, WebChat, Google Chat**, and more. You connect as many as
you like; the Gateway relays between them and the agent.

### 2.3 Skills

Skills are Markdown instruction files, `SKILL.md` with YAML frontmatter plus a Markdown
body, that teach the agent *how and when* to use tools. They load from **layered sources**
(workspace → project → personal → managed → bundled) with defined precedence, and are
filterable by environment/config ([Skills](https://docs.openclaw.ai/tools/skills)). Skills
are the primary unit you'll author in Week 17.

### 2.4 Plugins & ClawHub

Plugins are larger extension units built on a **plugin SDK**, distributed via **ClawHub**
(`clawhub.ai`), the community registry for skills and plugins.

### 2.5 Agent runtimes

OpenClaw separates the layers cleanly:

```
provider (auth/discovery) → model (the selected model) → agent runtime (executes a turn) → channel
```

Runtimes include the built-in embedded `openclaw` loop, harnesses like `codex`/`copilot`,
and CLI backends (`claude-cli`). It supports **sub-agents** for isolated parallel
workstreams ([Agent runtimes](https://docs.openclaw.ai/concepts/agent-runtimes)).

### 2.6 Memory

Memory is plain Markdown in the workspace, not hidden state:

- `USER.md`: stable preferences (who you are, how you like answers).
- `MEMORY.md`: durable facts/decisions the assistant should persist.
- `memory/YYYY-MM-DD.md`: daily running notes.
- `DREAMS.md`: an optional dream-diary/summary log.

The governing rule: **"the model only remembers what gets saved to disk; there is no
hidden state"** ([Memory](https://docs.openclaw.ai/concepts/memory)).

---

## 3. The context loop & compaction

Context is *everything OpenClaw sends to the model for a run*: the OpenClaw-built system
prompt, conversation history, and tool calls/results plus attachments. It is bounded by the
model's window. You inspect it with `/status`, `/context list|detail|map`, and `/usage
tokens` ([Context](https://docs.openclaw.ai/concepts/context)).

When the window fills, **compaction** summarizes older turns while keeping recent ones and
tool-call/result pairs intact. Auto-compaction is on by default; there's also a manual
`/compact` and a "safeguard" quality mode ([Compaction](https://docs.openclaw.ai/concepts/compaction)).

This is the same discipline you learned in
[`reference/knowledge-base/10-agents-multiagent.md`](../knowledge-base/10-agents-multiagent.md) §5,
OpenClaw is a working reference implementation of a context loop with compaction.

---

## 4. Permission modes & security model

OpenClaw's permission model is a clean reference for the guardrail tiering you studied in
Week 14.

### 4.1 Untrusted inbound input

Inbound messages are treated as **untrusted**. DM-capable channels pair unknown senders by
default; you approve a pairing with `openclaw pairing approve <channel> <code>`.

### 4.2 Permission modes

Host-command execution is controlled by `tools.exec.mode` (verify the exact values against
live docs), a clear tiering from least to most permissive:

| Mode | Behavior |
|---|---|
| `deny` | Block all host commands |
| `allowlist` | Only explicitly listed commands run |
| `ask` | Allowlist + prompt a human on anything not listed |
| `auto` | Allowlist + an auto-reviewer decides misses (falls back to human) |
| `full` | No prompts, trusted host only |

A separate `tools.exec.host` setting chooses *where* commands run (host vs. sandbox).

### 4.3 Sandboxing & exposure

Tools run on the host for the main session unless sandboxing is configured. Read the
sandboxing and exposure-runbook docs **before** connecting other users or exposing the
Gateway remotely ([Permission modes](https://docs.openclaw.ai/tools/permission-modes)).

> Practical rule for the lab: stay at `ask` or `auto` for any session that can touch files,
> and never set `full` on a machine you also use for real work.

---

## 5. Install & first run

Installers support macOS, Linux, Windows, and WSL2.

**Option A: install script (recommended):**

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Option B: npm (managed Node install):**

```bash
npm install -g openclaw@latest
```

Other paths include **Docker** and **Nix** ([Installation](https://docs.openclaw.ai/install)).

**First run:**

1. **Onboard**: `openclaw onboard --install-daemon`. This verifies model access, creates
   the workspace, and configures the Gateway. Pick a model provider, choose **Ollama** for
   local models (see §6).
2. **Verify the Gateway**: `openclaw gateway status`.
3. **Open the Control UI**: `openclaw dashboard`; send a message to confirm the assistant works.
4. **Connect a channel**: follow the [channels guide](https://docs.openclaw.ai/channels) for
   WhatsApp/Telegram/Discord/etc., then approve pairing requests for DM-capable channels.
5. **Extend**: add skills/plugins (ClawHub or your own `SKILL.md`), tune permission modes
   (`openclaw config set tools.exec.mode auto`), and read the
   [security guide](https://docs.openclaw.ai/gateway/security) before exposing it beyond yourself.

Full current walkthrough: [Getting started](https://docs.openclaw.ai/start/getting-started).

> The install script URL, package name, and onboarding flags are fast-moving, verify
> against live docs before scripting them.

---

## 6. Configuring a local model (Ollama)

OpenClaw talks to Ollama's **native `/api/chat`**, *not* the `/v1` OpenAI-compatible
endpoint, which breaks tool calling. It supports three modes: **Cloud + Local**, **Cloud
only**, and **Local only**. The canonical config is `baseUrl: "http://host:11434"` (no
`/v1`). Onboarding auto-discovers installed local models that support tool calling with a
≥16K context window ([Ollama provider](https://docs.openclaw.ai/providers/ollama)).

Steps:

1. **Install Ollama** and pull a tool-capable model, e.g. `ollama pull hermes4` (see
   [`hermes.md`](hermes.md) for model choice).
2. **Verify it can call tools**: a quick `ollama run hermes4` chat with a tool request is
   a decent smoke test; tool calling requires an instruction-tuned model.
3. **Point OpenClaw at it**: set the Ollama provider with `baseUrl` at `http://localhost:11434`
   (no `/v1`), and select "Local only" if you want to avoid cloud calls entirely.
4. **Confirm**: `/status` and `/usage tokens` in the assistant should show the local model
   and its context usage.

> The `baseUrl` and mode keys are fast-moving config surface, verify against
> [the Ollama provider docs](https://docs.openclaw.ai/providers/ollama) before editing `~/.openclaw`.

---

## 7. Writing a skill

A skill is a `SKILL.md` file: YAML frontmatter (name, description, and when-to-use
metadata) plus a Markdown body of instructions. Example for the lab:

```markdown
---
name: shipment-tracking
description: Answer "where is my shipment" questions using the ZoroLogistics MCP tools.
---

# Shipment tracking

Use the `track_shipment` tool whenever a user asks about a shipment's status or ETA.

Steps:
1. Extract the shipment id (format ZL-XXXXX) from the message.
2. Call `track_shipment(shipment_id=...)`.
3. Reply with the status and ETA in one short sentence.

Do NOT invent a status. If the tool errors, say so and ask the user to confirm the id.
```

Skills follow the same layered-precedence model (§2.3). Keep each skill **single-purpose**
and write the description tightly, the agent uses the description to decide *when* to
invoke it, so it is prompt engineering, exactly like tool descriptions.

---

## 8. Connecting MCP servers

OpenClaw can consume MCP servers, which is how the ZoroLab scenario (next section) works.
The pattern is the same as any MCP client: register the server (command or URL) in the
assistant's config, and its tools become available to the agent.

- **Local stdio server**: register the Week-16 server by its launch command
  (`python server.py`) with any env vars it needs.
- **Remote HTTP server**: register the URL, and mind the auth/security surface (§4).
- **Verify**: after registering, list the tools in the assistant (or the MCP Inspector) to
  confirm `track_shipment` and friends are visible before trusting an end-to-end run.

> MCP registration keys are config surface that has moved between releases, verify against
> live docs.

---

## 9. Production notes

- **Single-operator by design**: OpenClaw assumes *you* are the user. Exposing it to a
  team or the internet changes the threat model: re-read the security and exposure runbooks
  first.
- **Permission mode is your blast radius**: prefer `ask`/`auto`; reserve `full` for a
  trusted, disposable host.
- **Secrets**: store API keys and MCP credentials in environment variables or a secret
  store, never in skill bodies or `USER.md`/`MEMORY.md` (those files are part of what gets
  sent to the model).
- **Compaction & context budget**: watch `/usage tokens`; a long-running assistant degrades
  if compaction keeps evicting important state (the "context starvation" failure from
  [`10-agents-multiagent.md`](../knowledge-base/10-agents-multiagent.md)).
- **Tracing & cost**: route runs through a tracing backend (Langfuse/LangSmith) for the
  Week-17 ops layer, and track per-model spend.

### 9.1 Common gotchas

- **Tool calling breaks when pointed at Ollama's `/v1` endpoint.** Use the native
  `/api/chat` (`baseUrl` without `/v1`), the single most common first-run failure (§6).
- **"It doesn't remember anything."** Memory is only what you persist (§2.6). If a fact
  keeps vanishing, check whether it was ever written to `MEMORY.md` and whether compaction
  is evicting it.
- **A skill never fires.** The `description` frontmatter is what the agent matches against
  the request, treat it like a tool description and make it specific.
- **Paired vs. unknown senders.** DM channels pair unknown senders by default; a "silent"
  channel is usually a pending `openclaw pairing approve` (§4.1).
- **Gateway port conflicts.** The WebSocket API binds `127.0.0.1:18789` (verify against
  live docs); a second instance or a port collision will fail to start.

### 9.2 Where OpenClaw fits (positioning)

OpenClaw is not a replacement for the Week 12 to 13 coding harnesses (Claude Code, Cursor,
the DeepSeek Harness) nor for a graph framework like LangGraph. Think of it as a
**personal assistant runtime**: a long-lived, single-operator agent that lives in your
messaging channels and coordinates models, tools, and skills, the "always-on helper"
layer, distinct from a coding harness (interactive, repo-scoped) and a production agent
framework (deployed, multi-tenant, governed). It earns its place in the program because it
is the cleanest way to *operate* an assistant end-to-end, channels, context loop,
compaction, permissions, memory, and MCP, all in one small, readable system.

---

## 10. AI Engineering Lab scenario: the ZoroLab assistant

Week 17's use case: a personal **ZoroLab assistant** that answers shipment questions via
the Week-16 MCP server.

```
    You (Telegram/WebChat)
            │
            ▼
   ┌──────────────────┐      ┌─────────────────────────────┐
   │ OpenClaw Gateway │─────▶│  MCP server (Week 16)        │
   │  + Hermes model  │      │  track_shipment / list_lanes │
   └──────────────────┘      │  search_policy / request_refund │
            │                └─────────────────────────────┘
            ▼
   ZoroLogistics data (shipments, carriers, lanes) + policy corpus
```

Build it in order:

1. Install OpenClaw and onboard with a **local Hermes model** via Ollama (§6,
   [`hermes.md`](hermes.md)).
2. **Write two skills** (§7): `shipment-tracking` (uses `track_shipment`) and
   `policy-lookup` (uses `search_policy`).
3. **Register the Week-16 MCP server** (§8) and verify its tools are visible.
4. **Test the context loop**: ask a multi-turn question (track a shipment, then follow up
   "and what carrier is that?") and watch `/usage tokens` and compaction behavior.
5. **Gate the write tool**: keep `request_refund` behind an approval prompt (permission
   mode + HITL), the one irreversible action in the flow.
6. **Add tracing + cost** to finish the Week-17 ops runbook.

Success criterion from the curriculum: a working installation with 2 custom skills, the
Week-16 MCP server wired in, and a documented ops runbook.

---

## Sources

- Repository: https://github.com/openclaw/openclaw
- Docs: https://docs.openclaw.ai (Gateway architecture: /concepts/architecture · Context: /concepts/context · Compaction: /concepts/compaction · Memory: /concepts/memory · Skills: /tools/skills · Permission modes: /tools/permission-modes · Agent runtimes: /concepts/agent-runtimes · Ollama: /providers/ollama · Getting started: /start/getting-started · Security: /gateway/security · Installation: /install)
- Naming history (TechCrunch): https://techcrunch.com/2026/01/27/everything-you-need-to-know-about-viral-personal-ai-assistant-clawdbot-now-moltbot/
- Site: https://openclaw.ai

---

© 2026 Zorost Intelligence LLC · https://zorost.com
