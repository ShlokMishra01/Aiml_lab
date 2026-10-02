# Skill: Claude Code

> Part of AI Engineering Lab · Developed by Zorost Intelligence AI Lab · zorost.com

## 1. What it is

**Claude Code** is Anthropic's official **CLI coding agent**. It runs in your terminal,
inside your repo, so it has real filesystem context: it reads your code, runs your shell
commands (with permission prompts), edits files, and verifies with your tests. The same
agent runs **headless** in CI, which makes it scriptable and pipeline-friendly.

Think of it as a pair programmer that lives in the shell rather than in an editor. You talk
to it in plain language; it plans, acts, and shows you diffs before you accept. It is the
reference implementation of the "rules file + subagents + hooks" pattern the other harnesses
borrow from.

- **Builder:** Anthropic
- **Model:** the Claude family (Sonnet, Opus, Haiku)
- **Docs:** https://docs.claude.com/en/docs/claude-code/overview

## 2. Install & auth

Install one of two ways:

```bash
# npm (requires Node.js)
npm install -g @anthropic-ai/claude-code

# native installer
curl -fsSL https://claude.ai/install.sh | bash
```

Then authenticate with **either** of:

1. **A Claude account**: `claude` then sign in with a Claude Pro/Max subscription
   (usage is included in the subscription up to its limits).
2. **An API key**: export `ANTHROPIC_API_KEY` for pay-as-you-go API billing.

```bash
claude            # start the interactive REPL
claude --version  # confirm it's installed
```

> **Which auth?** Pro/Max is simpler and predictable for daily use; an API key gives you
> fine-grained, per-token control and is required for unattended/CI usage.

## 3. Core workflow

The happy path is a loop you already know from this program (plan → act → verify):

```bash
cd /path/to/zorologistics   # always start inside the repo
claude
```

Then, in the REPL:

```
> Build the ETA CLI from SPEC.md. Read SPEC.md first, then implement and run the tests.
```

Claude Code will:

1. **Plan**: read relevant files and lay out the steps.
2. **Act**: run shell commands (each gated by a permission prompt you approve) and edit files.
3. **Verify**: run your tests; if red, it iterates.
4. **Review**: you read the diff and accept or reject.

Useful in-session controls:

| Command | What it does |
|---|---|
| `/help` | List slash commands |
| `/init` | Generate a starter `CLAUDE.md` |
| `/clear` | Clear the conversation context |
| `/compact` | Compact history to free context |
| `/review` | Request a code review |
| `/status` | Show session and cost status |
| `Esc` | Interrupt the current action |

Headless mode runs the same agent without the REPL, ideal for CI or scripts:

```bash
claude -p "Run the test suite and fix any failures" --output-format stream-json
```

## 4. Config & rules files: CLAUDE.md

`CLAUDE.md` is the project memory Claude Code reads at the start of every session. Put it in
the repo root (checked into git, so your whole team shares it) and keep it short and
command-like. You can also keep a **user-level** `~/.claude/CLAUDE.md` for cross-project
defaults.

### ZoroLogistics CLAUDE.md template

````markdown
# CLAUDE.md

## What this repo is
ZoroLogistics AI tooling, freight data, ETA models, and support agents from the
AI Engineering Lab program. Read README.md first.

## Commands
- Install:      pip install -e .
- Run tests:    pytest -q
- Lint:         ruff check src
- Type check:   mypy src
- CLI smoke:    zoro-eta --help

## Conventions
- Python 3.11+, type hints on public functions.
- Data in `data/`; prefer Parquet, keep committed CSVs < 10 MB.
- Every model ships with a metric + error-analysis note.

## Never touch without asking
- `data/raw/`, generated input; edit the generator instead.
- `secrets/`, `.env`, `*.key`, `*.pem`, never read these into context.
- `scripts/build_tracker.py`, generated tracker tooling.
````

## 5. Power moves

- **Subagents.** Define specialist agents under `.claude/agents/` (a researcher, a tester,
  a reviewer). The main agent delegates bounded work to them and gets a summary back,
  keeping its own context small. Use them for independent, well-scoped tasks. A subagent is
  just a Markdown file with a system prompt and allowed tools:

  ```markdown
  # .claude/agents/reviewer.md
  ---
  name: reviewer
  description: Reviews diffs for correctness and style
  tools: Read, Grep, Glob
  ---
  You are a code reviewer. Check the diff for bugs, security issues, and
  conformance to the repo's CLAUDE.md conventions. Report findings, don't edit.
  ```

- **Hooks.** Automate policy instead of prompting for it. A `PreToolUse` hook can block a
  dangerous command; a `PostToolUse` hook can auto-run a linter after every edit. Hooks turn
  "please remember to check X" into something the harness enforces. Example, block anything
  touching `data/raw/` and refuse secrets:

  ```json
  // .claude/settings.json
  { "hooks": { "PreToolUse": [
    { "matcher": "Bash|Edit|Write",
      "hooks": [ { "type": "command",
        "command": "if echo \"$CLAUDE_PROMPT\" | grep -Eq 'data/raw/|\\.env|API_KEY'; then echo 'BLOCKED by policy'; exit 2; fi" } ] }
  ] } }
  ```

- **MCP integration.** Attach external tools/servers with `claude mcp add`. This is how
  Claude Code reaches data sources, APIs, or your own MCP server (Week 16):

  ```bash
  claude mcp add zorologistics -- npx -y @zorologistics/mcp-server
  ```

- **Headless + allow-lists.** `claude -p` with `--allowedTools "Read,Bash(git:*)"` bounds
  exactly what a non-interactive run can touch, essential for CI safety. A CI smoke test:

  ```bash
  claude -p "Run pytest and fix any failures." \
    --output-format stream-json \
    --allowedTools "Read,Grep,Glob,Edit,Bash(pytest:*)"
  ```

- **Review diffs, don't skim.** Claude Code is fast *because* it does many small steps.
  Read the full diff before accepting; the human owns the commit.

## 6. Cost & safety

**Cost.** Included with Claude subscriptions, **Pro ~$20/mo**, **Max ~$100 and ~$200/mo**
for higher usage, **Team** seats per user (~$25 to 60 depending on tier), Enterprise custom,
or billed per-token through the API. *Verify current numbers at Anthropic's pricing page;
tiers shift.* The cheapest lever is the same everywhere: narrow the task, trim context, and
pick a smaller model for mechanical edits.

**Safety.**

- **Permission system**: by default it prompts before shell commands and file writes;
  tighten it with allow-lists/deny-lists for the tools you never want it to run.
- **Blast radius**: run on a branch, never against production data; never paste secrets
  into the prompt (keep them in the environment, add a "never read secrets into context"
  line to CLAUDE.md).
- **Review before merge**: agent-authored code is still your code to ship or reject.

## 7. Common failures

| Symptom | Likely cause | Fix |
|---|---|---|
| `claude: command not found` | npm global bin not on PATH | Reinstall with the native installer, or add npm's bin dir to PATH. |
| "Authentication required" every run | Expired OAuth / missing key | Run `claude` and re-login, or set `ANTHROPIC_API_KEY`. |
| Hits the rate/usage limit mid-task | Subscription tier exhausted | Switch tier, use an API key, or `/compact` + narrow the task. |
| Loops without converging | Task too vague, no verifier | Give it a spec + a test command; break the task into steps. |
| Edits a file it shouldn't | Missing guardrail | Add the path to CLAUDE.md "Never touch" and a `PreToolUse` hook. |
| Context fills up / slows down | Too much pasted in | `/compact`, point at specific files, use subagents for bulk reading. |

## 8. Sources

- Claude Code overview: https://docs.claude.com/en/docs/claude-code/overview
- Anthropic pricing: https://www.anthropic.com/pricing
- Subagents: https://docs.claude.com/en/docs/claude-code/sub-agents
- Hooks: https://docs.claude.com/en/docs/claude-code/hooks
- MCP: https://docs.claude.com/en/docs/claude-code/mcp
- Headless mode: https://docs.claude.com/en/docs/claude-code/headless

> Pricing and feature names change frequently; re-check the vendor docs before quoting.

---

© 2026 Zorost Intelligence LLC · https://zorost.com
