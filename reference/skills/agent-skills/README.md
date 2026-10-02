# Zorost Agent Skills: Catalog

> **Reusable, harness-agnostic agent skills for AI engineering work, authored by
> [Zorost Intelligence](https://zorost.com) and shipped with AI Engineering Lab.**
>
> A *skill* is procedural memory you can hand to an AI coding agent: one `SKILL.md`
> file that turns a senior engineer's workflow into steps the agent follows every
> time. This catalog is Zorost's own set, written from the practice behind the
> 24-week program, tested against the ZoroLogistics case study, and designed to be
> read by humans as easily as by agents.

---

## What a skill is (and is not)

| | Skill (this catalog) | Prompt | Tool / MCP server |
|---|---|---|---|
| Form | A `SKILL.md` file of instructions | One message | Running software |
| Loaded | On demand, when the task matches | Once | Always available |
| Teaches the agent | **How** to do a class of task | What to do once | What it can call |
| Fails safely | Steps + verification gates | n/a | Type errors |

A skill is **not** software. It installs nothing, calls nothing by itself, and never
replaces a test, an eval, or a human gate. It *sequences* those things so the agent
cannot skip them when you are not watching.

## The Zorost skill standard (how every skill here is written)

Every skill in this catalog follows the same anatomy, in the same order:

```
SKILL.md
├── frontmatter     name · description · version · author · license · tags
│ The description is the picker hint, agents choose skills by it.
├── 1 · Purpose      One sentence. What the skill makes true.
├── 2 · When to use  Trigger conditions. When NOT to use it is listed too.
├── 3 · Inputs       What the agent must collect before step 1.
├── 4 · Procedure    Numbered steps. One action per step. Verbs first.
├── 5 · Anti-rationalization  The excuses agents give, and the answers.
├── 6 · Red flags    Observable signs the work is going wrong.
├── 7 · Verify       Evidence that must exist before the skill exits.
└── 8 · ZoroLogistics example   The skill applied to the program's case study.
```

The writing rules are adapted from **ASD-STE100 Simplified Technical English**, the
controlled language aviation uses so a tired mechanic cannot misread a step. Zorost
applies the same discipline to agent instructions (see
[OneRead](https://github.com/zorost/oneread), our STE type-checker):

1. **One action per sentence.** If a sentence has two verbs, it is two steps.
2. **Imperative verb first.** "Run the eval.", never "You should run the eval."
3. **Warnings before the step they protect**, never after.
4. **Numbers over adjectives.** "Stop after 3 failed attempts", never "retry a bit".
5. **No vague verbs.** Replace *handle, manage, deal with* with the actual action.
6. **Name the evidence.** Every skill ends with what must *exist*, a file, a score,
   a passing test, not with "make sure it works".
7. **The agent must be able to fail honestly.** Every procedure has an explicit
   STOP condition and says what to report when it fires.

## Installing the skills

Skills are plain Markdown. Any harness that reads instruction files can use them.

```bash
# Skills CLI (installs into Claude Code, Cursor, Codex, Copilot, OpenCode, and more)
npx skills add zorost/ai-engineering-lab --path reference/skills/agent-skills

# Or browse first
npx skills add zorost/ai-engineering-lab --path reference/skills/agent-skills --list
```

Manual install, copy the skill folders you want into your harness's skills directory:

| Harness | Where skills live |
|---|---|
| Claude Code | `~/.claude/skills/` or `<repo>/.claude/skills/` |
| Cursor | `.cursor/skills/` (rules for short policies only) |
| OpenCode | referenced from `AGENTS.md` / `opencode.json` |
| Hermes-class agents | `~/.hermes/skills/<category>/` |
| Any other agent | paste the `SKILL.md` body into the system/rules file |

Pick skills by **description match**, the same way the agent does: read the one-line
description in the catalog below, open only the skill that matches your task.

## The catalog

### Define: decide what "done" means before building

| Skill | One-line description | Program week |
|---|---|---|
| [spec-first-ai-feature](spec-first-ai-feature/SKILL.md) | Write the one-page spec, user, golden set, metric, gate, before any AI code. | W13 |
| [eval-first-development](eval-first-development/SKILL.md) | Build the golden set and the scorer before touching the prompt or model. | W6, W11 |

### Build: construct the AI component

| Skill | One-line description | Program week |
|---|---|---|
| [prompt-suite-versioning](prompt-suite-versioning/SKILL.md) | Treat a prompt as a versioned artifact with a score; change one variable at a time. | W6 |
| [context-budget-audit](context-budget-audit/SKILL.md) | Audit the seven claimants on the context window and set a working ceiling. | W6 |
| [rag-pipeline-checkup](rag-pipeline-checkup/SKILL.md) | Verify a RAG pipeline end-to-end: chunks, embeddings, retrieval, rerank, citations. | W7 |
| [local-model-fit](local-model-fit/SKILL.md) | Compute the VRAM budget and pick a model + quantization before downloading anything. | W8 to 9 |
| [fine-tune-readiness](fine-tune-readiness/SKILL.md) | Decide whether fine-tuning is justified, and gate the dataset before training. | W10 |
| [agent-loop-safety](agent-loop-safety/SKILL.md) | Wrap an agent loop with step limits, cost caps, human gates, and a trace. | W14 |
| [mcp-server-craft](mcp-server-craft/SKILL.md) | Design MCP tools that are narrow, typed, idempotent, and documented. | W16 |

### Verify: prove it works

| Skill | One-line description | Program week |
|---|---|---|
| [error-analysis-50](error-analysis-50/SKILL.md) | Read 50 real failures, cluster them, fix the largest class, extend the golden set. | W11 |
| [ai-output-review](ai-output-review/SKILL.md) | Review AI-generated code or text: spec diff, verifier run, secret scan, smell list. | W12 to 13 |

### Ship & operate: run it in production

| Skill | One-line description | Program week |
|---|---|---|
| [agent-ops-handoff](agent-ops-handoff/SKILL.md) | Move an agent from laptop to operated: tracing, cost dashboard, alerts, rollback. | W17 |
| [cloud-deploy-gate](cloud-deploy-gate/SKILL.md) | The pre-deploy gate for Foundry / Vertex / Bedrock: evals, budget, guardrails, owner. | W18 to 20 |

### Meta

| Skill | One-line description | Program week |
|---|---|---|
| [using-zorost-skills](using-zorost-skills/SKILL.md) | How to pick, run, and amend skills from this catalog. Start here. | all |

## How these skills relate to the ecosystem

The `SKILL.md` format is an emerging open convention (see
[agentskills.io](https://agentskills.io)) used across Claude Code, Cursor, OpenCode,
Hermes-class agents, and community packs. Good public collections to study after
this one:

- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills), the
  software-lifecycle pack (spec → plan → build → verify → review → ship) that
  popularized anti-rationalization tables.
- [emilkowalski/skills](https://github.com/emilkowalski/skills), domain-expertise
  skills (design, animation) showing how taste gets encoded.
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
  a community index of skill packs.
- [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs)
  research-workflow skills.
- [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills), vault and
  note-management skills.
- [Romanescu11/hermes-skill-factory](https://github.com/Romanescu11/hermes-skill-factory)
  generating Hermes-format skills from specifications.
- [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
  a UI/UX review skill.

**What makes this catalog different:** these skills are *AI-engineering* skills, not
general software skills, they encode the program's core doctrines (evals first, one
variable at a time, the seven-claimant budget, single agent first, evidence at exit)
as steps an agent cannot silently skip. They are also the same skills the 24-week
curriculum teaches a human, so by Week 12 you can read your agent's playbook because
you wrote it.

## Authoring a new skill (the checklist)

Earn the right first: use the workflow by hand on a real task, collect the steps you
*actually* took and the failure you *actually* hit, then:

- [ ] One skill, one class of task. Two tasks = two skills.
- [ ] Frontmatter `description` is a concrete picker hint with trigger words,
      the agent will choose the skill on that sentence alone.
- [ ] Procedure steps follow the clarity rules above (imperative, one action,
      warnings first, numbers over adjectives).
- [ ] Anti-rationalization table has at least three rows you have heard or caught
      yourself thinking.
- [ ] Verify section names evidence that must exist, not vibes.
- [ ] ZoroLogistics example included, so the skill stays teachable.
- [ ] Add the row to this catalog and cross-link the related program week.
- [ ] Run `python scripts/check_links.py` from the repo root.

---
© 2026 Zorost Intelligence LLC · [zorost.com](https://zorost.com)
