# Skill: Cursor

> Part of AI Engineering Lab · Developed by Zorost Intelligence AI Lab · zorost.com

## 1. What it is

**Cursor** is an **AI-native code editor** built by Anysphere, a fork of VS Code with an
agent bolted into the editor chrome rather than layered on as an extension. Its headline is
the **Agent**: a panel where you hand it a task and it plans, edits multiple files, runs
commands, and shows you a diff to review.

Because it is a VS Code fork, your muscle memory and most extensions carry over. The value
is that the agent lives *inside* your editor, so you move fluidly between typing, accepting
completions, and delegating whole features, without leaving the window.

- **Builder:** Anysphere
- **Site:** https://cursor.com

## 2. Install

1. Download the app from **cursor.com**.
2. Sign in with a Cursor account (created on first launch; team management lives in the web
   dashboard).
3. Optional: import your VS Code settings and extensions during onboarding.

There is also a **CLI** and an **SDK** for scripting Cursor's agent outside the editor, the
CLI lets you fire a headless agent task from a terminal or CI (`cursor-agent`-style entry
points vary by version), and the SDK exposes the same for programmatic use. For this program
the desktop app is the surface that matters; reach for the CLI/SDK only when you need to
automate Cursor in a pipeline, where a CLI harness (Claude Code/OpenCode) is usually the
cleaner tool anyway.

## 3. Tab vs. Agent (and Chat)

Cursor has three surfaces, and knowing which to use is most of the skill:

| Surface | What it does | Use it for |
|---|---|---|
| **Tab** | Inline, multi-line autocomplete as you type | Micro-edits, boilerplate, completing a line you already started |
| **Chat** (`⌘L`) | Q&A about selected code in a side panel | Explaining code, one-off "why does this fail?" questions |
| **Agent** (`⌘I`, formerly Composer) | Autonomous multi-file planning + editing | Cross-file refactors, "implement this spec," feature work |

The **Agent** is the one this program cares about in Week 12. Open it, paste a short task
(or point it at `SPEC.md`), and let it plan and edit across files. Review the diff, then
run your tests. The old name "Composer" still appears in older docs, same thing.

**Core loop:** open repo → `⌘K` for a targeted edit or `⌘I` for an agent task → accept Tab
suggestions inline → review the agent's full diff → run tests → iterate.

**Week 12 in Cursor (concrete).** With `SPEC.md` committed and Rules in place:

1. Open the repo; `⌘I` to open the Agent.
2. Type: `Read SPEC.md and implement the ETA CLI. Run pytest after; keep the diff minimal.`
3. Let it plan and edit; watch the per-file diff.
4. Run `pytest -q` yourself; if red, send the failing output back to the Agent.
5. Accept, commit on a branch, and open a PR for a human review.

Shortcuts to memorize: `⌘I` (Agent), `⌘L` (Chat), `⌘K` (inline edit), `Tab` (accept
completion), `Esc` (dismiss a suggestion).

## 4. Config & rules files: Rules

Cursor reads **Rules** for persistent project instructions: `.cursor/rules/*.mdc` (the
modern format) and the legacy `.cursorrules` (a single file). Rules are the Cursor
equivalent of `CLAUDE.md`/`AGENTS.md`. Commit them to the repo so every teammate's agent
follows the same conventions.

### Project rules template (`.cursor/rules/zorologistics.mdc`)

```markdown
---
description: ZoroLogistics repo conventions for the Cursor agent
---

# ZoroLogistics conventions

## Commands
- Install: `pip install -e .`
- Run tests: `pytest -q`
- Lint: `ruff check src`
- Type check: `mypy src`

## Conventions
- Python 3.11+, type hints on public functions.
- Data lives in `data/`; prefer Parquet, keep committed CSVs under 10 MB.
- Every model ships with a metric + an error-analysis note.

## Never touch without asking
- `data/raw/`, generated input; edit the generator instead.
- `secrets/`, `.env`, `*.key`, `*.pem`, never read these into context.
```

## 5. Power moves

- **Model selection.** Cursor routes each request through the **Cursor Router**. Its
  "Auto" modes pick a model per request by trading cost, quality, and reliability:

  | Auto mode | Behavior |
  |---|---|
  | **Cost** | Cheapest model that fits; fixed low per-token rates |
  | **Balance** | Middle ground for everyday tasks |
  | **Intelligence** | Strongest available model for hard reasoning |

  You can also pin a specific model per task. *Bringing your own API key* is supported for
  some models, but most users run on Cursor's included pools; check the settings pane for
  what your plan includes. Set the mode in Settings → Models.
- **MCP.** Add MCP servers in Cursor settings to give the agent external tools (your Week 16
  ZoroLogistics server, for example). Add a server with a name, command, and args, e.g.
  `zorologistics` running `npx -y @zorologistics/mcp-server`, then enable it for the
  workspace. The agent's tools then include the server's capabilities (track shipment,
  convert units, query the ETA model).
- **Keep tasks narrow, review the full diff.** Agent mode is strong *because* it edits many
  files; that is also the risk. One focused task at a time, then read everything it touched.
- **Watch the usage pool.** Third-party and routed models consume your monthly pool fastest;
  switch the Auto mode (Cost vs Intelligence) to match the task, Cost for mechanical work,
  Intelligence for hard reasoning.

## 6. Cost & safety

**Pricing tiers (as of Aug 2026: re-verify):**

| Plan | Price | Notes |
|---|---|---|
| Hobby | Free | Limited usage |
| Pro | $20/mo | Individual, standard usage |
| Pro+ | $60/mo | Higher usage |
| Ultra | $200/mo | Highest usage |
| Teams Standard | $40/user/mo | Team billing |
| Teams Premium | $120/user/mo | Higher team limits |
| Enterprise | via sales | Pooled usage, SCIM, audit logs |

Cursor Router's **Auto (Cost)** mode bills at fixed rates (~$1.25/1M input, ~$6.00/1M
output, ~$0.25/1M cache read), while Balance/Intelligence bill at the routed model's rate;
plans also include a monthly "Other Models" pool. *Re-check before quoting.*

**Safety.** Review every diff before accepting; commit Rules with a "never touch" list; keep
secrets out of prompts and context; for production data use a branch and narrow scope.

## 7. Team workflows

- **Commit Rules to the repo**: the single highest-leverage team practice: identical
  conventions for every engineer's agent.
- **Central billing + admin**: teams get pooled usage, member management, and (Enterprise)
  SCIM and audit logs, so usage and policy are governed in one place.
- **Shared MCP servers**: define team MCP connections once; agents inherit them.
- **Code review still belongs to humans**: the agent proposes; a teammate still reviews the
  PR. Treat the agent as a fast first draft, not an approver.

## 8. Cursor vs. a CLI harness

| | Cursor (IDE) | CLI harness (Claude Code / OpenCode) |
|---|---|---|
| **Where you work** | Inside the editor | In the terminal |
| **Best for** | Feature work with heavy manual editing; visual diff review | Scriptable, git-native, CI/headless, model-agnostic pipelines |
| **Model choice** | Cursor Router (curated + Auto modes) | Any OpenAI-compatible provider (OpenRouter, Ollama, BYO key) |
| **Team/org features** | Strong (pooled billing, SCIM, audit) | Depends on harness |
| **Automation** | CLI/SDK exists but editor-first | First-class `-p`/headless |

**Rule of thumb.** You already live in an editor and want completion + an agent with
minimal friction → **Cursor**. You want a scriptable, terminal-native agent you can point at
any model and run in CI → a **CLI harness**. For Week 12, run the ETA CLI build through both
and compare, that comparison *is* the deliverable.

## 9. Common failures

| Symptom | Likely cause | Fix |
|---|---|---|
| Agent ignores project conventions | No Rules file committed | Add `.cursor/rules/*.mdc` and restart the agent session. |
| Usage pool drains fast | Routing in Intelligence mode for easy tasks | Switch Auto to **Cost**, or pin a cheaper model. |
| Tab suggests wrong API | Old model context | Refresh the model/context; check the model selected in settings. |
| MCP server doesn't appear | Not enabled for the workspace | Add/enable it in Cursor Settings → MCP. |
| Diff review overwhelming | Task too broad | One narrow task at a time; review per-file. |
| Agent edits a file it shouldn't | Missing guardrail in Rules | Add the path to Rules' "Never touch" list; re-run. |
| Version churn / unexpected changes | Model auto-switched mid-task | Pin a model for the task; watch the Auto mode setting. |

## 10. Sources

- Cursor site: https://cursor.com
- Cursor pricing: https://cursor.com/help/account-and-billing/pricing.md
- Cursor Rules: https://docs.cursor.com/context/rules
- Cursor MCP: https://docs.cursor.com/context/model-context-protocol

> Pricing and feature tiers change frequently and were captured Aug 2026; re-check the
> vendor pages before quoting.

---

© 2026 Zorost Intelligence LLC · https://zorost.com
