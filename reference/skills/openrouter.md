# Skill: OpenRouter

> Part of AI Engineering Lab · Developed by Zorost Intelligence AI Lab · zorost.com

## 1. What it is

**OpenRouter** is a **unified LLM API and router**: one account, one key, one
OpenAI-compatible endpoint that reaches **hundreds of models** across many providers
(Anthropic, OpenAI, DeepSeek, Meta, Mistral, Google, and more). It also adds **automatic
failover**, so a provider error or timeout reroutes your request instead of killing the run.

It is *not* a model and *not* an editor, it's the routing layer *behind* a harness. Use it
when you want to switch models by changing a slug instead of reconfiguring a provider.

- **Site:** https://openrouter.ai
- **Docs:** https://openrouter.ai/docs/llms.txt

> **Note.** As of research time there is **no product named "9Router"**, the closest match
> is OpenRouter (the phrase is almost certainly a mishearing). Treat "9Router" = OpenRouter.

## 2. Account & keys

1. Create an account at **openrouter.ai**.
2. Generate a key at **openrouter.ai/keys**.
3. Call the API with a standard header:

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"meta-llama/llama-3.3-70b-instruct",
       "messages":[{"role":"user","content":"What is the predicted ETA for SH-4821?"}]}'
```

Keep the key in an **environment variable**, never in a prompt or committed file.

## 3. Routing one API to many models

Models are addressed by **slug** (`provider/model`):

```
anthropic/claude-sonnet-4
deepseek/deepseek-chat
meta-llama/llama-3.3-70b-instruct
```

Beyond plain slugs, OpenRouter adds:

- **Provider routing**: pick specific providers, or let OpenRouter sort by price/latency/throughput.
- **Automatic fallbacks / model fallbacks**: on error or timeout, reroute automatically.
- **Routers**: higher-level helpers: *Auto Router* (pick a model for your prompt), *Pareto
  Router* (pick a coding model by minimum coding score), *Fusion Router* (multi-model
  deliberation as a slug), *Free Models Router*.
- **Variants**: suffixes that change behavior: `:free`, `:extended`, `:thinking`,
  `:online`, `:nitro`, `:exacto`.

  | Variant | What it does |
  |---|---|
  | `:free` | Zero-cost, rate-limited access |
  | `:thinking` | Extended reasoning / thinking output |
  | `:online` | Adds web-search grounding |
  | `:nitro` | Faster, higher-tier routing |
  | `:extended` | Larger context variant |
  | `:exacto` | Deterministic / exact-output behavior |

- **BYOK**: bring your own provider keys so you pay the provider directly (skips
  OpenRouter's token markup).

**Switching models = editing one string.** That's the whole point.

## 4. Model selection UI

Browse **openrouter.ai/models** to compare models by slug, context length, pricing per token
(input/output/cache), and capabilities. The UI (and the `/api/v1/models` endpoint) is where
you confirm a slug exists before wiring it into a harness, model names change often.

## 5. `:free` models

Append `:free` to a model id for **zero-cost access**:

```
meta-llama/llama-3.2-3b-instruct:free
```

Free variants carry **stricter rate limits and availability** than paid versions (per-model
limits, commonly on the order of tens of requests per minute or a daily cap; check the
rate-limits doc). Use them to **test plumbing** (auth, config, prompts) before paying, then
swap to a paid slug for real throughput. *Don't* build a production loop on `:free`.

## 6. Cost tracking & limits

- **Pay-per-token** against a prepaid **credit** balance; top up on the dashboard. You are
  charged input, output, and (when applicable) cache-read tokens at per-model rates.
- OpenRouter adds a small markup for its routing/failover service; **BYOK** removes it if
  you already pay Anthropic/OpenAI directly.
- Track spend in the dashboard (usage, per-model and per-key cost), and set **usage limits**
  and budget alerts so a runaway agent loop can't drain the balance.
- Exact per-model prices are listed on each model's page, read them before quoting, and
  re-read them before a big batch, since they shift.

**Quick cost playbook for a harness:** use `:free` or a cheap small model to prove the
config and prompt work → run real tasks on a mid-tier paid slug → reserve the expensive
frontier models for the hard reasoning steps only → set a daily usage limit as a backstop.

## 7. Using it from your tools

- **OpenCode**: add an `openrouter` provider with `baseURL: https://openrouter.ai/api/v1`
  and set `"model": "openrouter/<slug>"` in `opencode.json` (see the OpenCode skill).
- **Claude Code / other OpenAI-compatible clients**: point the base URL at OpenRouter and
  use your key; swap models by slug.
- **Ollama-compat / local**: OpenRouter is a *hosted* endpoint, not a local one; for local
  models use Ollama/LM Studio. You can run the two side by side: `:free` hosted for one-off
  checks, Ollama for private/offline work.
- **Curl / SDKs**: anything that speaks the OpenAI chat-completions shape works.

## 8. Pitfalls

Before relying on a new slug, run a one-line sanity check (auth + slug validity):

```bash
curl -s https://openrouter.ai/api/v1/models | grep -o '"id":"[^"]*"' | grep "$SLUG"
```

If the slug isn't in the list, it's been renamed or retired, find its replacement before
wiring it into a config.

- **Pricing changes.** Per-token prices and markup shift without notice, re-check the model
  page before committing to a budget.
- **Model deprecation.** Slugs get retired or renamed; a config that worked last month may
  return 404. Pin to a *current* slug and re-verify periodically.
- **`:free` is not for production.** Rate limits and availability are much lower, treat it
  as a sandbox tier only.
- **Provider variability.** The "same" model can behave differently across providers; if
  quality drifts, pin a specific provider rather than letting OpenRouter choose.
- **Secrets.** The key is bearer-credential sensitive, keep it out of prompts, logs, and git.
- **Failover is not quality insurance.** Automatic fallback keeps the request alive, but a
  fallback model may answer worse, don't treat "no error" as "good answer."
- **Cache-read billing.** If your harness caches prompts, you may see cache-read token
  charges in addition to input/output, budget for all three line items.

## 9. Sources

- OpenRouter docs index: https://openrouter.ai/docs/llms.txt
- Quickstart: https://openrouter.ai/docs/quickstart.md
- `:free` variant: https://openrouter.ai/docs/guides/routing/model-variants/free.md
- Models: https://openrouter.ai/models

> Pricing, rate limits, and model slugs change frequently; re-check the docs before quoting.

---

© 2026 Zorost Intelligence LLC · https://zorost.com
