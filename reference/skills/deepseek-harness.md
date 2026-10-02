# Skill: DeepSeek Harness (DSH)

> Part of AI Engineering Lab · Developed by Zorost Intelligence AI Lab · zorost.com

## 1. What it is

**DeepSeek Harness (DSH)** is DeepSeek's **open-source agent harness**, an *agentic CLI +
web GUI* that turns a model into a coding agent. It is deliberately **not an editor** and
**not a model**: it supplies the loop, the tools, and the coordination layer, while you
supply the model credentials. Its central design claim is **"everything is a plugin"**,
models, tools, skills, sessions, sandboxes, storage, loops, scheduling, and even the UI are
plugin bundles composed on a plugin kernel called **Cordis**.

For this program, DSH is the harness to learn when you want to go beyond "type a prompt"
and start *composing* an agent: skills, goals, subagents, workflows, and a full trace of
everything the model did.

- **Builder:** DeepSeek AI
- **Repo:** https://github.com/deepseek-ai/deepseek-harness · npm `@deepseek-ai/dsh`, MIT
- **Status:** developer preview, "iterating rapidly," expect breaking changes.
- **Site:** https://deepseek.com/harness/en/

## 2. Install & auth

Requires **Node.js**.

```bash
# global install
npm i -g @deepseek-ai/dsh

# initialize a profile / project
dsh init

# launch the web GUI (http://localhost:3080 by default)
dsh web
```

Zero-install quickstart (no global package needed):

```bash
npx @deepseek-ai/dsh web      # web GUI at http://localhost:3080 (a.k.a. 127.0.0.1:3080)
```

From source (when you want to write plugins):

```bash
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness && pnpm install && pnpm run build
pnpm dsh web
```

Other entry modes: `dsh --profile <name>` boots a named profile, and
`dsh --profile headless "job"` runs one fresh persisted session, prints the final answer,
and exits.

**Auth.** DSH itself is free (MIT), there is no per-seat license. You bring your own model
credentials (API keys / provider config) through the web GUI or config. Cost = your model
provider.

## 3. Core workflow

1. Launch `dsh web` and open the GUI.
2. Start a session and pick a **runtime mode** (below).
3. Give it a task; it plans → runs tools → edits → verifies.
4. When it misbehaves, open the **Trajectory** view (the append-only log) to see exactly
   what it saw and did.

**Runtime modes** (chosen per session) change the toolset:

| Mode | Toolset |
|---|---|
| **Standard** | Full: file editing, shell, file/web search, skills, planning, goals, subagents, workflows |
| **Code** | Tools exposed through a code-mode SDK, orchestrate multi-step ops in one TypeScript program |
| **Minimal** | Bare two-tool agent (persistent bash + `str_replace_editor`), for benchmarking models |
| **Creator** | Runtime inspection and preset authoring |

**Mode selection in practice.** Default to **Standard** for real coding tasks. Drop to
**Minimal** when you're benchmarking a model's raw ability (or comparing models fairly,
which Week 12's harness comparison wants). Use **Code** when you want the model to
orchestrate several operations in a single TypeScript program rather than turn-by-turn.
Reach for **Creator** only when authoring presets or inspecting the runtime.

## 4. Config & env

A **profile** is an ordered stack of plugin bundles plus your own patch layer. Compose
profiles without editing the source; inspect the composed tree with `--dump-config` /
`--dump-default-config`. **Agent presets** (`code`, `minimal`, `standard`, `cordis`) bundle a
base toolset. Your patch layer lives in `cordis.patch.yml`, for example, to pin a model
provider without touching the bundled plugins:

```yaml
# cordis.patch.yml
openai:
  baseURL: https://openrouter.ai/api/v1
  apiKey: env:OPENROUTER_API_KEY
  model: deepseek/deepseek-chat
```

- Provider/API keys go in config or the web GUI, reference them via `env:VAR`, never
  hard-code the secret itself.
- DSH also ships an **MCP client**, **job management** (background jobs), **todo tracking**,
  **plan mode**, **token metering**, and **session compaction**.

## 5. Skills, goals, subagents & workflows (the power moves)

These four primitives are what make DSH more than a REPL:

- **Skills.** Reusable, task-specific instruction packs loaded on demand, the same idea as
  this program's `reference/skills/` library. Author a skill once (a domain procedure, a repo
  convention) and reuse it across sessions. Example: a `zoro-eta-release` skill that encodes
  the "bump version → run tests → tag → changelog" checklist so every release follows it.
- **Goals.** Persisted, same-session completion objectives that drive *automatic
  continuation rounds*. Use a goal for a long, multi-round objective instead of one giant
  prompt, e.g. *"ship the ETA CLI: implement, test green, write the comparison note"*, and
  let DSH carry it across rounds, pausing only when it needs you.
- **Subagents & forks.** Delegate to background children that either start fresh or inherit
  the conversation (`subagent_fork`); children stay continuable, so you can hand them more
  work later. Use for independent, bounded tasks, keeps your main context small. Example:
  fork three researchers to compare pricing, then read their summaries in the main session.
- **Workflows.** Scripted fan-out across many subagents (phases, structured results), for
  audits over many files, migrations, or multi-angle research. Define phases, fan a
  checklist out to parallel agents, and collect structured results back.
- **Ralph loops.** Fresh-agent iterative execution: each round starts a new child with no
  inherited context, using the shared workspace as durable memory. (Use only when you
  explicitly want fresh-agent iteration.)

**The Traceability habit.** Everything the model sees, system prompts, reasoning, tool
calls, subagent scheduling, is recorded in an append-only session log. The **Trajectory**
view lets you inspect by source, and resume/fork/search/replay operate on the same event
stream. When a run goes wrong, read the trace before you re-prompt. A quick triage pass:

1. **System prompt & context**: did the right files/rules actually load? (Usually the bug.)
2. **First tool call**: did it act on the right thing, or misread the task?
3. **The divergence point**: where did the plan go off the rails; was a tool result misread?
4. **Verifier calls**: did it actually run the tests, or declare victory without checking?

Fix the *context* or *verifier*, not just the wording of the prompt, that's the difference
between steering and begging.

## 6. Cost & safety

- **Cost.** Free, open source (MIT). You pay only your model provider, so every cost
  lever is a model-choice lever: use a small model for mechanical edits, OpenRouter
  `:free` variants to test plumbing, and cap runs with max-turn limits + token metering.
- **Safety.** DSH is a preview with full shell access, treat it like any agent:
  run it on a branch, keep secrets in env vars (never in prompts), and use the permission
  layer to bound what it can touch. Pin expectations loosely: it is moving-target software
  with compatibility-breaking changes expected.

## 7. DSH vs. Claude Code

| | DeepSeek Harness | Claude Code |
|---|---|---|
| **License** | Open source (MIT) | Proprietary (free to use, Anthropic-hosted) |
| **Surface** | Web GUI + CLI + headless | Terminal CLI + headless |
| **Model** | Any (BYO key, provider-agnostic) | Claude family |
| **Extensibility** | Plugin-everything (Cordis), skills/goals/workflows, full trace | CLAUDE.md, subagents, hooks, MCP |
| **Best for** | Composing/inspecting agents; model benchmarking; open-source control | Fast, polished daily coding; deep Anthropic integration |

**Rule of thumb.** Want a polished, opinionated daily driver tightly coupled to Claude →
**Claude Code**. Want an open, inspectable, composable harness you can extend and point at
*any* model (including DeepSeek's) → **DSH**. They're complementary: in Week 12 you can run
the same ETA CLI spec through both and compare the trace and output.

## 8. Common failures

| Symptom | Likely cause | Fix |
|---|---|---|
| `dsh: command not found` | Node/npm not installed, or bin not on PATH | Install Node.js; re-run `npm i -g @deepseek-ai/dsh`. |
| Web GUI won't open | Port 3080 busy | Use the configured port or free the port. |
| No model responds | Missing provider config/key | Add your API key in the web GUI or config. |
| Behavior changed between versions | Preview breaks compatibility | Pin a version; read the release notes. |
| Run looks wrong and you can't tell why | You're guessing, not reading the trace | Open the **Trajectory** view. |
| Subagent/workflow result missing | It's still running or was killed | Check job status; collect output before concluding. |
| Secret appears in the trace | You pasted it into a prompt | Rotate it; reference keys via `env:VAR` only. |

## 9. Sources

- DeepSeek Harness site: https://deepseek.com/harness/en/
- GitHub: https://github.com/deepseek-ai/deepseek-harness

> Feature names and entry commands shift quickly in this preview; re-check the repo before
> quoting.

---

© 2026 Zorost Intelligence LLC · https://zorost.com
