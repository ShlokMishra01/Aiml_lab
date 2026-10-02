# Skill: OpenCode

> Part of AI Engineering Lab · Developed by Zorost Intelligence AI Lab · zorost.com

## 1. What it is

**OpenCode** is an **open-source, terminal-first AI coding agent** from **SST** (the team
behind the SST framework and OpenNext). It is deliberately **model-agnostic and
provider-agnostic**: point it at Anthropic, OpenAI, OpenRouter, Ollama, LM Studio, or any
OpenAI-compatible endpoint and it works the same way.

It ships a full **TUI** (session list, slash commands, diff review) plus desktop, web, and
IDE-extension surfaces, but the terminal is the heart of it. Because it is free and speaks
to any endpoint, it's the natural first harness for this program: test prompts against a
local model for free, then flip one config line to a hosted model.

- **Builder:** SST
- **Site / docs:** https://opencode.ai · https://opencode.ai/docs/

## 2. Install

```bash
# native installer
curl -fsSL https://opencode.ai/install | bash

# or via npm
npm i -g opencode-ai

opencode            # launch the TUI
```

Auth is separate: `opencode auth login` stores credentials for a provider, or you supply
keys per provider in config / environment variables.

## 3. Core workflow (the TUI)

Run `opencode` inside your repo and you get an interactive session:

```
> Build the ETA CLI from SPEC.md. Read SPEC.md first, then implement and run the tests.
```

The agent edits files and shows a **diff**; you review/accept; it iterates until your tests
or approval pass. Useful keys/commands:

| Input | What it does |
|---|---|
| `/help` | List commands and keybinds |
| `/new` | Start a new session |
| `/sessions` | List and switch sessions |
| `/share` | Share a session for collaboration |
| `/models` | Show available models and switch |
| `Tab` / arrows | Navigate the diff; accept/reject hunks |
| `Esc` | Interrupt the running agent |

**Sessions** are first-class: each is a persisted conversation you can return to, branch
from, or share, so a long Week 13 loop isn't lost when you close the terminal. The
client/server split means the core keeps running headless while any surface (TUI, web, IDE)
attaches, so you can leave a session running and reconnect from another terminal.

## 4. Config: `opencode.json`

Config lives in `opencode.json` at the project root, or globally at
`~/.config/opencode/opencode.json`. A `provider` map holds named providers (`baseURL`,
`apiKey`, `models`), and `model` sets the default.

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "openrouter": {
      "npm": "@ai-sdk/openrouter",
      "options": { "baseURL": "https://openrouter.ai/api/v1" }
    },
    "ollama": {
      "npm": "ollama-ai-provider",
      "options": { "baseURL": "http://localhost:11434/v1" }
    }
  },
  "model": "openrouter/anthropic/claude-sonnet-4"
}
```

- Set the model by slug: `"anthropic/claude-sonnet-4"`, `"openrouter/... "`, or a local
  `"ollama/llama3.2"`.
- API keys can come from `opencode auth login` or environment variables per provider
  (e.g. `OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY`). Reference the env var rather than
  pasting the secret into JSON.
- Because it targets any OpenAI-compatible endpoint, the same config works for OpenRouter,
  Ollama, LM Studio, and local servers.

A richer example, two providers plus a local model with an explicit baseURL:

```json
{
  "provider": {
    "anthropic": { "npm": "@ai-sdk/anthropic", "options": { "apiKey": "env:ANTHROPIC_API_KEY" } },
    "openrouter": { "npm": "@ai-sdk/openrouter", "options": { "baseURL": "https://openrouter.ai/api/v1" } },
    "lmstudio": { "npm": "openai", "options": { "baseURL": "http://localhost:1234/v1" } }
  },
  "model": "openrouter/deepseek/deepseek-chat"
}
```

## 5. Rules: AGENTS.md

OpenCode auto-loads **`AGENTS.md`** as persistent instructions: the project file
(`./AGENTS.md`) and a global `~/.config/opencode/AGENTS.md` for cross-project defaults.
This is the single highest-leverage config in the whole tool, put build commands,
conventions, and "don't touch these files" there.

````markdown
# AGENTS.md

## Commands
- Install: `pip install -e .`
- Run tests: `pytest -q`
- Lint: `ruff check src`

## Conventions
- Python 3.11+, type hints on public functions.

## Never touch
- `data/raw/`, `secrets/`, `.env`, `*.key`
````

## 6. Providers (incl. OpenRouter)

OpenCode's provider map makes multi-provider work trivial:

- **Anthropic / OpenAI**: native providers with `opencode auth login`.
- **OpenRouter**: one provider entry pointing at `https://openrouter.ai/api/v1`, then any
  model by slug (see the `openrouter` skill). This is the fastest way to try many models.
- **Ollama / LM Studio**: point `baseURL` at `http://localhost:11434/v1` (or `:1234/v1`)
  to run a model locally for free.
- **Any OpenAI-compatible server**: vLLM, SGLang, TGI, or your own endpoint.

**Power move:** test a prompt for free on a local/Ollama model, then flip `model` to a
hosted slug, zero code changes.

## 7. When OpenCode shines

- **Model-agnostic exploration**: you want to A/B the same task across Anthropic, DeepSeek,
  a local model, and OpenRouter without touching your code.
- **Terminal-native, git-centric work**: you live in the shell and want a fast TUI, not an
  editor.
- **Headless / client-server**: the core can run headless with any surface attached, so it
  slots into scripts and CI.
- **Teams**: `share` a session for collaboration; commit `AGENTS.md` + `opencode.json` so
  everyone gets the same setup.

Choose OpenCode when you want an open, flexible, terminal-first agent you can point at any
model; choose Claude Code when you want Anthropic's polished defaults; choose DSH when you
want plugin-level composition and a full trace.

## 8. Cost & safety

- **Cost.** Free, open source (MIT), you pay only your model provider. Control cost by
  model choice (local/`:free` for plumbing, hosted for real work) and by keeping
  `AGENTS.md`/context tight.
- **Safety.** OpenCode has a **permission/policy system**, configure which tools need
  approval. Run on a branch, keep secrets in env vars (never in prompts), and add a "never
  touch" list to `AGENTS.md`. Review diffs before accepting.

## 9. Common failures

| Symptom | Likely cause | Fix |
|---|---|---|
| `opencode: command not found` | Install path issue | Reinstall via the curl script, or use `npm i -g opencode-ai`. |
| "No provider configured" | Missing provider/model in `opencode.json` | Add the provider map + `model` (see §4). |
| Auth errors on first call | No credentials for that provider | `opencode auth login` or set the provider's API key env var. |
| Agent ignores repo conventions | No `AGENTS.md` | Add one at the repo root; restart the session. |
| Local model won't connect | Wrong baseURL / Ollama not running | Start Ollama; confirm `http://localhost:11434/v1` responds. |
| Model slug 404s | Provider renamed/deprecated the slug | Check `opencode.ai/models` or OpenRouter; update `model`. |
| Diff applies to wrong files | Task too vague | Narrow the task; point at specific paths. |

## 10. Sources

- OpenCode site: https://opencode.ai
- OpenCode docs: https://opencode.ai/docs/
- OpenCode config reference: https://opencode.ai/docs/config/
- OpenRouter (for the OpenRouter provider): https://openrouter.ai/docs/llms.txt

> Config keys and provider schemas evolve; re-check the docs before quoting.

---

© 2026 Zorost Intelligence LLC · https://zorost.com
