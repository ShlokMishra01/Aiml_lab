# 03: Coding-Agent Harnesses, LLM Routers & Local Model Stacks

> AI Engineering Lab research note · synthesized from official docs and primary sources · Aug 2026
> Audience: engineers standing up agentic coding workflows and local inference. Everything below is written in our own words; no third-party training text is reproduced. Sources are listed at the end.

This note covers four layers of the stack a working AI engineer touches every day: (A) the harnesses and IDEs that turn an LLM into a *coding agent*, (B) the local inference runtimes that let you run those models yourself, (C) quantization (how to make models fit), and (D) fine-tuning (when to change the weights instead of the prompt).

---

## A) Harnesses & AI Coding Tools

A harness is the software between the model and the environment: it gives an LLM tools (shell, file editing, search), a loop (plan → act → verify → repeat), persistence (sessions, logs), and coordination primitives (subagents, skills, workflows). The model supplies reasoning; the harness supplies agency.

### A.1 DeepSeek Harness (DSH)

- **What it is.** An open-source **agent harness** (not an editor and not a model) from DeepSeek AI. Its central design claim is **"everything is a plugin."** Models, tools, skills, sessions, sandboxes, storage, loops, scheduling, and even the UI are plugin bundles composed by configuration on top of a plugin kernel called **Cordis**.
- **Who builds it.** DeepSeek AI. Repository: `github.com/deepseek-ai/deepseek-harness` (npm package `@deepseek-ai/dsh`, MIT license).
- **Status.** Developer preview, explicitly "iterating rapidly" with compatibility-breaking changes expected.
- **Key features.**
  - **Runtime modes** (picked per session): *Standard* (full toolset, file editing, shell, file/web search, skills, planning, goals, subagents, workflows), *Code* (tools exposed through a code-mode SDK so the model can orchestrate multi-step operations in one TypeScript program), *Minimal* (a two-tool agent with persistent bash + `str_replace_editor`, useful for benchmarking models in a bare environment), and *Creator* (runtime inspection and preset authoring).
  - **Skills**: reusable, task-specific instruction packs (e.g., a "skill" for a domain workflow) loaded on demand.
  - **Goals**: persisted, same-session completion objectives that drive automatic continuation rounds.
  - **Subagents & forks**: delegate work to background children that either start fresh or inherit the conversation; children stay continuable.
  - **Ralph loops**: fresh-agent iterative execution where each round starts a new child with no inherited context and uses the shared workspace as durable memory.
  - **Workflows**: scripted fan-out across many subagents (phases, structured results).
  - **Traceability**: everything the model sees is recorded in an append-only session log (system prompts, reasoning, tool calls, subagent scheduling). A *Trajectory* view lets you inspect by source; resume, fork, search, and replay operate on the same event stream.
  - **MCP client**, job management (background jobs), todo tracking, plan mode, token metering, and session compaction.
- **Install / run.** Requires Node.js. Quick start launches the Web UI:
  ```sh
  npx @deepseek-ai/dsh web     # Web UI at http://127.0.0.1:3080 by default
  ```
  From source:
  ```sh
  git clone https://github.com/deepseek-ai/deepseek-harness.git
  cd deepseek-harness && pnpm install && pnpm run build
  pnpm dsh web
  ```
  Other entry modes: `dsh --profile <name>` (boot a named profile), `dsh --profile headless "job"` (run one fresh persisted session, print the final answer, exit), and `dsh plugin --profile <name> <pnpm args>` (manage a profile's plugins).
- **Configuration.** A *profile* is an ordered stack of plugin bundles plus the user's own patch layer (`cordis.patch.yml`). Compose profiles without editing the source; `--dump-config` / `--dump-default-config` inspect the composed tree. "Agent presets" (e.g., `code`, `minimal`, `standard`, `cordis`) bundle a base toolset.
- **Authentication.** DSH itself is MIT/free; you supply your own model credentials (API keys / provider config) through the Web UI or config. There is no per-seat license.
- **Pricing.** Free, open source (MIT). Cost = your model provider.
- **Practical tips.**
  1. Start with `npx @deepseek-ai/dsh web`, zero install surface; go to source only when you want to write plugins.
  2. Use **skills** for repeatable domain procedures and **goals** for long-running, multi-round objectives rather than one giant prompt.
  3. Read the **Trajectory** view when a run goes wrong, the append-only log is the fastest way to see *why* the model did something.
  4. Treat it as moving-target software: pin expectations loosely because it is a preview that breaks compatibility.

### A.2 OpenCode (SST)

- **What it is.** An open-source, terminal-first **AI coding agent** with an interactive TUI, plus desktop, web, and IDE-extension surfaces. It is deliberately model-agnostic and provider-agnostic.
- **Who builds it.** SST (the team behind the SST framework / OpenNext). Site: `opencode.ai`.
- **Key features.** Full TUI (session list, slash commands, diff review), an **AGENTS.md** convention for project memory/instructions, per-project `opencode.json` config, LSP integration, MCP server support, a permission/policy system, themes/keybinds, "share" for collaboration, and a client/server split so the core runs headless and any surface attaches.
- **Install / run.**
  ```sh
  curl -fsSL https://opencode.ai/install | bash
  # or: npm i -g opencode-ai
  opencode
  ```
- **Model / provider configuration.** Defined in `opencode.json` (project root) or `~/.config/opencode/opencode.json`. A `provider` map holds named providers (`baseURL`, `apiKey`, `models`), and `model` sets the default (e.g., `"anthropic/claude-sonnet-4"`, `"openrouter/... "`, or a local `"ollama/llama3.2"`). `AGENTS.md` (project) and `~/.config/opencode/AGENTS.md` (global) are auto-loaded as persistent instructions.
- **Authentication.** `opencode auth login` stores credentials; API keys can also come from environment variables per provider. Since it targets any OpenAI-compatible endpoint, it works with OpenRouter, Ollama, LM Studio, and local servers.
- **Typical workflow.** `opencode` → describe the change → agent edits files and shows a diff → review/accept → it iterates until tests or your approval pass.
- **Pricing.** Free and open source (MIT); you pay only your model provider.
- **Practical tips.**
  1. Put a project `AGENTS.md` in the repo (build commands, conventions, "don't touch these files"), it is the single highest-leverage configuration.
  2. Keep a `~/.config/opencode/AGENTS.md` for cross-project defaults (style, testing policy).
  3. Point a `provider` at Ollama/LM Studio to test prompts for free before paying a hosted model.

### A.3 Cursor (Anysphere)

- **What it is.** An AI-native code editor, a VS Code fork, built around an agent that edits many files at once.
- **Who builds it.** Anysphere.
- **Key features.** **Tab** (inline multi-line completion), **Chat**, and **Agent** (formerly Composer) for autonomous multi-file edits; **Rules** (`.cursor/rules`, legacy `.cursorrules`) for project instructions; **MCP** support; a CLI and SDK; and **Cursor Router** with "Auto" modes, *Cost / Balance / Intelligence*, that route each request to a model balancing cost, quality, and reliability.
- **Install / authenticate.** Download the app from `cursor.com`, sign in with a Cursor account; manage teams from the dashboard. Extensions (VS Code ecosystem) mostly carry over.
- **Typical workflow.** Open a repo → `⌘K` for targeted edits, `Tab` to accept completions → open the Agent panel with a task and let it plan and edit across files → review diffs → loop on tests.
- **Pricing (as of Aug 2026, per Cursor's pricing doc).** Hobby (free, limited), **Pro $20/mo**, **Pro+ $60/mo**, **Ultra $200/mo**; **Teams Standard $40/user/mo**, **Teams Premium $120/user/mo**; Enterprise (pooled usage, SCIM, audit logs) via sales. Auto (Cost mode) has fixed rates, $1.25/1M input, $6.00/1M output, $0.25/1M cache read, while Balance/Intelligence bill at the routed model's rate. Plans also include a monthly "Other Models" usage pool.
- **Practical tips.**
  1. Commit **Rules** to the repo so every teammate's agent follows the same conventions.
  2. Prefer **Agent** mode over single edits for cross-file refactors; keep the task narrow and review the full diff.
  3. Watch the usage pool, third-party/model routing consumes it fastest; switch the Auto mode (Cost vs Intelligence) to match the task.

### A.4 Claude Code (Anthropic)

- **What it is.** Anthropic's official **CLI coding agent** that runs in your terminal and can operate headless in CI.
- **Who builds it.** Anthropic.
- **Key features.** **CLAUDE.md** memory files (repo + user level), **subagents** defined under `.claude/agents/`, **hooks** (`PreToolUse`, `PostToolUse`, `Notification`, `Stop`, etc.) for policy and automation, **MCP** integration (`claude mcp add`), a permission/sandbox system, and **headless mode** (`claude -p "…"`) with `--output-format stream-json` for scripting and pipelines. It runs directly in the repo, giving it real filesystem context.
- **Install / authenticate.**
  ```sh
  npm install -g @anthropic-ai/claude-code   # then run `claude`
  # or the native installer: curl -fsSL https://claude.ai/install.sh | bash
  ```
  Authenticate either with a Claude account (Pro/Max subscription) or with `ANTHROPIC_API_KEY` for pay-as-you-go API billing.
- **Typical workflow.** `claude` in a repo → describe the task → it plans, runs shell commands (with permission prompts), edits files → you review diffs → it verifies with tests → `claude -p` for non-interactive runs.
- **Pricing.** Included with Claude subscriptions (Pro ~$20/mo; Max tiers ~$100 and ~$200/mo for higher usage), Team seats per user (~$25 to 60 depending on tier), Enterprise custom, or billed per-token through the API. (Verify current numbers at Anthropic's pricing page; tiers shift.)
- **Practical tips.**
  1. Maintain a repo `CLAUDE.md` (test commands, build steps, architecture notes), it is read every session and compounds.
  2. Use **hooks** to auto-run linters/tests after edits or to block dangerous commands rather than prompting for each one.
  3. Use headless mode + `--output-format stream-json` to embed the agent in scripts and CI; combine with `--allowedTools` to bound what it can touch.

### A.5 Other notable tools (one paragraph each)

- **Windsurf.** An AI-first editor (originating from the Codeium team) whose flagship is **Cascade**, an agent that maintains deep repo-wide context and previews changes; it pairs fast Supercomplete-style completion with agentic multi-file edits, Rules, and Previews. Freemium; paid tiers unlock more agent "flow action" credits. Good fit for developers who want agentic editing with an IDE feel lighter than a full fork.
- **GitHub Copilot (agent mode).** GitHub/Microsoft's assistant, now with **agent mode** in VS Code that iterates autonomously on multi-file tasks, plus Copilot Chat, inline completion, a CLI, and Copilot coding agent for issues/PRs. Tightly integrated with GitHub (PRs, Actions). Free tier + Pro (~$10/mo), Business/Enterprise tiers. Default choice when you live inside GitHub/VS Code.
- **Aider.** An open-source **CLI pair-programmer** (`pip install aider-chat`) that works directly on a git repo, proposes edits, and auto-commits; supports a huge model list (hosted or local via Ollama/LM Studio) and an architect/editor split. Free (you pay the API). Best for git-native, terminal-only, model-flexible workflows.
- **Warp.** A modern Rust terminal with built-in AI ("Warp AI") and an **Agentic Mode** that reads your terminal context and executes multi-step commands; the terminal itself is open source, AI features are subscription. Best when you want agent help *inside* the shell rather than a separate coding agent.
- **Amazon Q Developer.** AWS's AI coding assistant (IDE extension + CLI) with an agent mode; free tier and a Pro tier (~$19/mo, and included with some AWS offerings). It shines in AWS-heavy environments (IaC, CDK, AWS API knowledge), less so as a general cross-provider agent.

### A.6 OpenRouter (unified LLM API): and the "9Router" question

- **What it is.** A **unified API and router** over hundreds of models from many providers. You use one key and one OpenAI-compatible endpoint (`https://openrouter.ai/api/v1/chat/completions`); OpenRouter routes your request to a provider and adds automatic failover.
- **Who builds it.** OpenRouter (`openrouter.ai`), an independent service.
- **How routing works.** Models are addressed by slug (`provider/model`, e.g. `anthropic/claude-sonnet-4`, `deepseek/deepseek-chat`, `meta-llama/llama-3.3-70b-instruct`). Beyond plain slugs, OpenRouter adds:
  - **Provider routing**: choose providers, or let OpenRouter sort by price/latency/throughput.
  - **Automatic fallbacks / model fallbacks**: if a provider errors or times out, the request reroutes.
  - **Routers**: higher-level helpers like the *Auto Router* (pick a good model for your prompt), *Pareto Router* (pick a coding model by minimum coding score), *Fusion Router* (multi-model deliberation as a slug), and the *Free Models Router*.
  - **Variants** as suffixes, `:free` (rate-limited free access), `:extended`, `:thinking`, `:online`, `:nitro`, `:exacto`.
  - **BYOK**: bring your own provider API keys so you pay the provider directly.
- **`:free` models.** Append `:free` to a model id (e.g. `meta-llama/llama-3.2-3b-instruct:free`) for zero-cost access. Free variants carry **stricter rate limits and availability** than paid versions (limits are per-model; check the FAQ/rate-limits doc, commonly on the order of tens of requests per minute or a daily cap).
- **Credits & pricing.** Pay-as-you-go per token: top up a **credit** balance, or use BYOK for discounted/provider-direct billing. OpenRouter adds a small markup for its routing/fallback service; exact per-model prices are listed per model on `openrouter.ai/models`.
- **Authentication.** Create an API key at `openrouter.ai/keys`; send `Authorization: Bearer <KEY>`.
- **Practical tips.**
  1. For local/harness experiments, drop an `:free` model into OpenCode/DSH config to test plumbing at zero cost, then swap to a paid slug.
  2. Enable **fallbacks** so a provider outage doesn't kill an agent loop.
  3. Use **BYOK** if you already pay for Anthropic/OpenAI keys, it removes OpenRouter's token markup.

- **Is "9Router" real?** We found **no legitimate LLM-routing product named "9Router."** Searching npm surfaces only several `9router*`-suffixed packages flagged as suspicious (typosquat-style, no credible project behind them), not a real tool to adopt. The phrase is almost certainly a **mishearing of "OpenRouter"**, which we cover in full above. Treat "9Router" = OpenRouter unless a specific, citable product is named.

### A.7 Comparison: coding-agent harnesses & tools

| Tool | Maker | Surface | Model choice | Config/memory | Auth | Pricing |
|---|---|---|---|---|---|---|
| DeepSeek Harness (DSH) | DeepSeek | Web GUI + CLI + headless | Any (BYO key) | Profiles, `cordis.patch.yml`, presets | BYO provider key | Free (MIT) |
| OpenCode | SST | TUI + desktop/web/IDE | Any OpenAI-compat + native | `opencode.json`, `AGENTS.md` | `opencode auth` / env | Free (MIT) |
| Cursor | Anysphere | IDE (VS Code fork) | Curated + Cursor Router | `.cursor/rules` | Cursor account | Free → $20 to $200/mo; Teams $40 to 120 |
| Claude Code | Anthropic | Terminal CLI | Claude family | `CLAUDE.md`, `.claude/` | Claude account or API key | Subscription or API |
| Windsurf | Windsurf team | IDE | Curated | Rules | Account | Freemium credits |
| GitHub Copilot | GitHub/Microsoft | VS Code / CLI / web | Curated (OpenAI-based) | `copilot-instructions.md` | GitHub account | Free → Pro ~$10/mo |
| Aider | Open source | Terminal CLI | Any (huge list) | `.aider.conf.yml`, repo conventions | BYO key | Free (pay API) |
| Warp | Warp | Terminal + AI | Curated + BYO | n/a | Account | Freemium |
| Amazon Q Developer | AWS | IDE + CLI | Curated (AWS) | n/a | AWS Builder ID/IAM | Free + Pro ~$19/mo |
| OpenRouter | OpenRouter | API (no UI) | 100s via slugs/variants | n/a | API key, BYOK | Per-token credits |

---

## B) Local Inference Stacks

Running models locally gives you privacy, zero marginal token cost, and full control, at the cost of VRAM and throughput. The ecosystem splits into **runtime engines** (Ollama, llama.cpp, MLX) and **serving engines** (vLLM, SGLang, TGI).

### B.1 Ollama

- **What / who.** A friendly wrapper around llama.cpp that packages models as portable artifacts and exposes a simple CLI, REST API, and OpenAI-compatible endpoint. Built by the Ollama team (`ollama.com`).
- **Install.**
  ```sh
  curl -fsSL https://ollama.com/install.sh | sh     # macOS/Linux; Windows has an installer
  ollama pull llama3.2            # or a sized/quantized tag: llama3.2:7b, llama3.2:7b-q4_K_M
  ollama run llama3.2             # interactive chat
  ollama list                     # installed models
  ```
- **Modelfiles.** A `Modelfile` is a declarative recipe: `FROM <base>` (a model or GGUF), `SYSTEM` prompt, `PARAMETER` (temperature, `num_ctx`, `top_p`, `stop`, etc.), `TEMPLATE` (chat template), and `ADAPTER` (LoRA). Build with `ollama create mymodel -f Modelfile`.
- **REST API.** Served at `http://localhost:11434` (`/api/generate`, `/api/chat`, `/api/pull`, `/api/tags`, …). Set `OLLAMA_HOST` to bind elsewhere and `OLLAMA_MODELS` to relocate storage.
- **OpenAI compatibility.** `http://localhost:11434/v1` speaks the OpenAI `/chat/completions` protocol, so any OpenAI SDK can point at it.
- **Tips.** ① Pin quantized tags (`:7b-q4_K_M`) for predictable VRAM. ② Use `OLLAMA_NUM_PARALLEL`/`num_ctx` to trade concurrency and context against memory. ③ Treat it as the *simplest* path to local models; move to llama.cpp/vLLM when you need CLI-level flags or high throughput.

### B.2 llama.cpp

- **What / who.** The original C/C++ inference engine (now under the `ggml-org` org) that runs **GGUF**-format models on CPU and GPU with no Python dependency. It is the substrate under Ollama and many others.
- **GGUF.** A self-contained, single-file model format bundling weights + metadata (tokenizer, chat template, quantization info). Convert from Hugging Face with `convert_hf_to_gguf.py`, quantize with `llama-quantize`.
- **Key binaries.**
  - `llama-cli`: one-shot completion/interactive.
  - `llama-server`: OpenAI-compatible HTTP server (what you'd put behind an agent harness).
  - `llama-quantize`: convert a model to a smaller k-quant.
  - `llama-perplexity`, `llama-bench`, evaluation and benchmarking.
- **Common options.** `-ngl N` (layers offloaded to GPU, set high/all for full GPU), `-c`/`--ctx-size` (context), `-n` (max tokens to generate), `-t` (threads), `--temp`, `-fa`/`--flash-attn`, and `--jinja` for chat templates.
- **Backends.** CUDA (NVIDIA), Metal (Apple), ROCm/HIP (AMD), Vulkan, and SYCL, selected at build time (cmake flags such as `-DGGML_CUDA=ON`, `-DGGML_METAL=ON`).
- **Tips.** ① Build with your GPU backend enabled or you silently fall back to CPU. ② Use `llama-bench` to compare quant/backend choices on *your* hardware before committing. ③ GGUF quants are the standard "drop-in" artifact for local stacks, learn the `Q4_K_M` vs `Q8_0` tradeoff (see §C).

### B.3 LM Studio

- **What / who.** A desktop **GUI** for discovering, downloading, and running local models, with a built-in chat UI and a local OpenAI-compatible server. Made by the LM Studio team (`lmstudio.ai`).
- **Key features.** Browse/search Hugging Face and one-click download of GGUF models; choose a runtime (MLX on Apple Silicon, CUDA, or Vulkan); run an in-app chat; expose `http://localhost:1234/v1` (OpenAI-compatible) for external tools.
- **Fit.** Best for *interactive* local experimentation and for quickly serving a model to a coding agent (OpenCode/DSH/Aider) without touching a CLI.
- **Tips.** ① On Apple Silicon prefer the MLX runtime for speed. ② Watch the "loaded into memory" indicator, the GUI makes VRAM pressure visible. ③ Use it as the discovery layer, then graduate to llama.cpp/vLLM for scripted serving.

### B.4 Apple MLX

- **What / who.** Apple's machine-learning framework for **Apple Silicon**, exposing a NumPy-like API with **unified memory** (model, KV cache, and app share one memory pool, no host↔device copies). Repo: `ml-explore/mlx`.
- **`mlx-lm` toolkit.** `mlx_lm.generate`, `mlx_lm.convert` (import Hugging Face models), `mlx_lm.server` (OpenAI-compatible server), `mlx_lm.lora` (LoRA/QLoRA fine-tuning), and `mlx_lm.fuse`.
- **Fit.** The fastest local path on M-series Macs; memory bandwidth of unified RAM often beats a comparable GPU for large quants.
- **Tips.** ① Prefer 8-bit/4-bit (`-q --q-bits 4`) to fit big models in unified memory. ② Use `mlx_lm.server` to feed an OpenAI-compatible client. ③ MLX is research/single-node oriented; for multi-GPU serving use vLLM/SGLang.

### B.5 GPU setup: NVIDIA CUDA vs AMD ROCm vs Apple MPS

- **NVIDIA (CUDA).** The default path. You need: a **driver**, the **CUDA toolkit**, and **cuDNN** (for training frameworks); for PyTorch, install a CUDA-matched wheel:
  ```sh
  pip install torch --index-url https://download.pytorch.org/whl/cu124   # pick the CUDA build matching your driver
  ```
  Verify hardware with `nvidia-smi` (shows GPU, driver, CUDA version, VRAM) and the software stack with:
  ```python
  import torch
  torch.cuda.is_available()      # True when the build finds the driver
  torch.cuda.get_device_name(0)  # e.g. "NVIDIA RTX 4090"
  ```
  Rule of thumb: driver version ≥ CUDA toolkit version (the driver is backward-compatible).
- **AMD (ROCm).** AMD's CUDA-equivalent stack for Instinct/Radeon GPUs; PyTorch ships ROCm wheels (`pip install torch --index-url https://download.pytorch.org/whl/rocm6.x`). Check with `rocm-smi` and `torch.cuda.is_available()` (ROCm presents as the CUDA device abstraction via HIP). Historically less smooth than CUDA on consumer cards, verify your exact GPU is supported before buying.
- **Apple Silicon (Metal/MPS).** No driver install; PyTorch uses the Metal Performance Shaders backend:
  ```python
  torch.backends.mps.is_available()   # True on M-series
  device = torch.device("mps")
  ```
  MPS is great for inference and modest fine-tuning; some ops fall back to CPU. MLX (§B.4) is often faster on Apple hardware.
- **CUDA vs ROCm vs MPS summary.** CUDA = broadest support + best tooling; ROCm = AMD's answer, strongest on datacenter Instinct; MPS/MLX = zero-setup on Macs, unified memory is the differentiator.

### B.6 VRAM planning (rule-of-thumb table)

Rough memory per model size (weights only; add ~10 to 20% for activations/KV cache and always leave headroom for the OS and other processes). Rule: **FP16 ≈ 2 bytes/param · INT8 ≈ 1 byte/param · INT4 ≈ 0.5 bytes/param** → at 4-bit you need roughly **1 GB per billion parameters**.

| Model size | FP16 | 8-bit (INT8) | 4-bit (INT4/GGUF Q4) | Typical GPU to fit |
|---|---|---|---|---|
| 7B | ~14 GB | ~7 GB | ~4 GB | 8 GB card (4-bit) or 16 GB (FP16) |
| 8B | ~16 GB | ~8 GB | ~4.5 GB | 8 GB (4-bit) / 16 GB (FP16) |
| 13B | ~26 GB | ~13 GB | ~7 GB | 12 to 16 GB (4-bit) / 24 GB (FP16) |
| 34B | ~68 GB | ~34 GB | ~17 GB | 24 GB (4-bit) |
| 70B | ~140 GB | ~70 GB | ~35 GB | 2×24 GB (4-bit) or 48 to 80 GB |
| 405B+ | ~810 GB | ~405 GB | ~200 GB | Multi-GPU datacenter only |

Notes: 8-bit here ≈ GGUF `Q8_0` / bitsandbytes 8-bit; 4-bit ≈ GGUF `Q4_K_M` / bitsandbytes NF4. Apple unified memory follows the same table (a 128 GB M-series Mac runs a 70B at 4-bit comfortably).

### B.7 Serving engines (vLLM, SGLang, TGI)

- **vLLM.** The throughput workhorse. **PagedAttention** manages the KV cache in fixed-size pages (near-zero fragmentation), and **continuous batching** admits new requests token-by-token instead of waiting for whole batches. Ships an OpenAI-compatible server (`vllm serve <model>`). Best default for high-QPS production serving of many concurrent requests.
- **SGLang.** Optimized for **radix/prefix caching** (RadixAttention shares cached prefixes across requests, huge wins for shared system prompts and agent loops), plus fast structured/constrained decoding. `python -m sglang.launch_server`. Best when many requests share a long common prefix or you need fast structured outputs.
- **TGI (Text Generation Inference).** Hugging Face's production server (Rust + Python). Polished defaults, strong quantization support (bitsandbytes/GPTQ/AWQ/FP8), tensor parallelism, and easy Docker deployment (`ghcr.io/huggingface/text-generation-inference`). Best when you want HF-native, ops-friendly serving with conservative, well-tested features.
- **When to use which.** Default **vLLM** for general high-throughput serving; **SGLang** for prefix-heavy workloads and structured decoding; **TGI** for HF-ecosystem shops wanting a batteries-included, containerized server.
- **Throughput/latency knobs (all engines).** `gpu_memory_utilization` (VRAM share, ~0.9), `max_num_batched_tokens` / `max_num_seqs` (batch size, bigger = higher throughput, higher latency), `tensor_parallel_size` (split across GPUs), `max_model_len` (cap context to save KV memory), and `quantization` (awq/gptq/fp8). Raise batch for throughput; lower it (or add speculative decoding) for latency.

### B.8 Comparison: serving engines

| Engine | Key mechanism | Strengths | OpenAI-compat server | Best fit |
|---|---|---|---|---|
| vLLM | PagedAttention + continuous batching | Highest throughput, huge ecosystem | Yes (`vllm serve`) | General production serving |
| SGLang | RadixAttention (prefix cache) + structured decoding | Fast shared-prefix & JSON/tool decoding | Yes | Agent loops, repeated system prompts |
| TGI | Rust/Python, polished defaults | Ops-friendly, broad quant support, Docker | Yes | HF-native, containerized deploys |

---

## C) Quantization

Quantization lowers numerical precision to shrink memory and speed inference at a small accuracy cost.

### C.1 Precision formats

| Format | Bits/param | Notes |
|---|---|---|
| FP16 | 16 | Standard half precision; ~2× less memory than FP32 with negligible quality loss for inference. |
| BF16 | 16 | Same range as FP32, fewer mantissa bits; **more stable for training** (no overflow), now the training default. |
| FP8 | 8 | E4M3/E5M2 formats; used for inference and some training on Hopper+ (Transformer Engine). |
| INT8 | 8 | ~2× smaller than FP16; needs scale factors (per-tensor/channel). |
| INT4 | 4 | ~4× smaller than FP16; the aggressive but widely-acceptable chat/inference default. |

### C.2 GGUF k-quants

GGUF "k-quants" are llama.cpp's practical quant tiers (lower number = smaller/faster but lossier): `Q2_K` (aggressive), `Q3_K_*`, **`Q4_K_M`** (the community sweet spot, good quality/VRAM ratio), `Q5_K_M`, `Q6_K`, and `Q8_0` (near-FP16 quality). Recommendation: start with `Q4_K_M`; step up to `Q5_K_M`/`Q6_K` when quality matters and VRAM allows; avoid `Q2_K` unless memory is desperate.

### C.3 Weight-quantization methods

- **bitsandbytes.** Runtime quantization library: 8-bit (LLM.int8()) and 4-bit **NF4** (normal-float-4, a data-aware format); the backbone of **QLoRA**. Easy drop-in via `load_in_4bit=True`.
- **AWQ (Activation-aware Weight Quantization).** Protects the small fraction of weights that matter most (measured by activation magnitude) and scales the rest. Often better quality than GPTQ at 4-bit with no calibration data needed.
- **GPTQ.** Layer-wise quantization using second-order (Hessian) information from a calibration dataset. High quality but needs calibration data and is slower to produce.

### C.4 Accuracy & when quantization is (not) acceptable

- **Perplexity ladder (general trend).** FP16/BF16 ≈ FP32 for inference; 8-bit ≈ negligible loss; 4-bit k-quants ≈ small, usually imperceptible loss for chat/summarization/RAG; 2 to 3-bit = noticeable degradation.
- **Acceptable** for: conversation, summarization, classification, RAG, coding assistance at the harness level, where a tiny word-choice drift doesn't break correctness.
- **Be cautious / avoid heavy quantization** for: precise arithmetic or math, long-horizon reasoning, low-resource languages, and exact code generation where a single token error breaks compilation. Always **eval on your task** (perplexity ≠ task accuracy) before shipping a quant.

---

## D) Fine-Tuning Stacks

### D.1 Parameter-efficient methods (PEFT)

- **LoRA (Low-Rank Adaptation).** Freezes the base weights and trains low-rank matrices (`ΔW = BA`, rank `r`) injected into attention/MLP layers. Trains ~0.1 to 1% of parameters; adapters are small, swappable, and mergeable.
- **QLoRA.** LoRA on top of a **4-bit (NF4) base model** (bitsandbytes), with double quantization and paged optimizers, fine-tune a 70B on a single 24 GB GPU.
- **DoRA (Weight-Decomposed LoRA).** Splits each weight into magnitude + direction and adapts direction with LoRA; often matches full fine-tuning better than plain LoRA at the same rank.

### D.2 Training objectives

- **SFT (Supervised Fine-Tuning).** Imitation learning on (instruction → answer) pairs. Teaches style, format, and task behavior; the standard first step.
- **DPO (Direct Preference Optimization).** Trains directly on (chosen, rejected) preference pairs without a reward model, simpler and more stable than RLHF/PPO. Good for alignment and preference shaping.
- **RLVR (RL with Verifiable Rewards).** Reinforcement learning where the reward is a *checkable* signal (unit tests pass, math answer correct, code compiles) rather than a learned reward model. The current frontier method for reasoning/coding gains.

### D.3 Frameworks

- **Hugging Face TRL + PEFT.** The default Python stack: `SFTTrainer`, `DPOTrainer`, `GRPOTrainer` (RLVR), and PEFT's `LoraConfig`/`get_peft_model`. Works across Transformers models and accelerator backends.
- **Unsloth.** A drop-in speed/memory layer for fine-tuning (2 to 5× faster, ~50 to 70% less VRAM) with native TRL integration; popular for LoRA/QLoRA on Llama/Mistral/Qwen families. `pip install unsloth`.
- **Axolotl.** A YAML-config-driven fine-tuning orchestrator over TRL/PEFT, declare model, dataset, LoRA/QLoRA/DoRA config, and it wires the run; ideal for reproducible, shareable training recipes.
- **Distillation.** Train a small **student** model to mimic a larger **teacher** (logit or hidden-state matching). Different goal from LoRA: you shrink the *model*, not just the adapter. Useful for deploying a compact specialist after a large teacher proves a task.

### D.4 Dataset formats

- **Chat-template format.** A `messages` array (role/content) matching the model's chat template, the most portable today:
  ```json
  {"messages": [{"role": "system", "content": "..."},
                {"role": "user", "content": "..."},
                {"role": "assistant", "content": "..."}]}
  ```
- **ShareGPT format.** A `conversations` array with `from`/`value` (system/human/gpt), commonly used with Axolotl. Convert between the two before mixing tooling.
- **Instruction/Alpaca format.** Flat `instruction`/`input`/`output` triples (legacy but still common in older datasets).
- **Preference format (DPO).** `prompt` + `chosen` + `rejected`. **RLVR** adds a `reward`/verifier column (or a reward function/unit-test harness).

### D.5 When to fine-tune vs prompt/RAG (Ng's selection order)

Andrew Ng's practical default for application work, try each cheaper lever before training weights:

1. **Managed model API + a prototype.**
2. **Context and prompting, with an eval** (few-shot examples, system prompt, structured output).
3. **RAG** if the answer must come from *your* data/knowledge.
4. **Agentic workflow** if the job is multi-step with tools.
5. **Fine-tune (or train) only when the eval shows the base model + context cannot get there.**

In short: fine-tuning is the *last* lever, justified by a measured gap, not the first instinct. Revisit it only when prompting + RAG + tooling fail your eval on a specific, high-volume task (e.g., a strict output format, a niche domain style, or hard-to-prompt reasoning).

---

## Sources

**Harnesses & tools**
- DeepSeek Harness, official site: https://deepseek.com/harness/en/ · GitHub: https://github.com/deepseek-ai/deepseek-harness
- OpenCode, docs: https://opencode.ai/docs/ · site: https://opencode.ai
- Cursor pricing & plans: https://cursor.com/help/account-and-billing/pricing.md · site: https://cursor.com
- Claude Code, docs: https://docs.claude.com/en/docs/claude-code/overview
- Windsurf: https://windsurf.com · GitHub Copilot: https://github.com/features/copilot · Aider: https://aider.chat · Warp: https://www.warp.dev · Amazon Q Developer: https://aws.amazon.com/q/developer/
- OpenRouter, docs index: https://openrouter.ai/docs/llms.txt · quickstart: https://openrouter.ai/docs/quickstart.md · `:free` variant: https://openrouter.ai/docs/guides/routing/model-variants/free.md · models: https://openrouter.ai/models

**Local inference & serving**
- Ollama: https://ollama.com · https://github.com/ollama/ollama
- llama.cpp: https://github.com/ggml-org/llama.cpp
- LM Studio: https://lmstudio.ai
- Apple MLX: https://github.com/ml-explore/mlx
- vLLM: https://docs.vllm.ai · SGLang: https://github.com/sgl-project/sglang · TGI: https://github.com/huggingface/text-generation-inference
- PyTorch installs (CUDA/ROCm): https://pytorch.org/get-started/locally/

**Quantization & fine-tuning**
- bitsandbytes: https://github.com/TimDettmers/bitsandbytes · AWQ: https://github.com/mit-han-lab/llm-awq · GPTQ: https://github.com/IST-DASLab/gptq
- Hugging Face PEFT: https://huggingface.co/docs/peft · TRL: https://huggingface.co/docs/trl
- Unsloth: https://github.com/unslothai/unsloth · Axolotl: https://github.com/axolotl-ai-cloud/axolotl
- Andrew Ng selection order (prompt → RAG → agentic → fine-tune last): https://www.deeplearning.ai (Ng's "The Batch" letters and GenAI application guidance; see also the *AI Engineering Skills Map*, The Batch, 2026-08-14)

> Note on recency: pricing and feature tiers (Cursor, Claude Code, Windsurf, Copilot) change frequently and were captured Aug 2026 from the linked official pages; re-check the vendor's pricing page before quoting in public material.
