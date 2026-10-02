# 10: Model Serving

> Part of AI Engineering Lab · Developed by Zorost Intelligence AI Lab · [zorost.com](https://zorost.com)

Model Serving is the layer that turns a registered model or a hosted foundation model
into a **REST API** you (and any app) can call. It is serverless, auto-scaling, and
governed by Unity Catalog, and every LLM call you make on Databricks can be routed
through one control plane: the **Unity AI Gateway**.

> **Week 23 · ML & GenAI.** This file pairs with
> [`09-model-training.md`](09-model-training.md) (you train and register a model first) and
> [`13-agents.md`](13-agents.md) (agents are served as custom models).

---

## 1. The mental model: three things you can serve

An **endpoint** is identified by a unique **name** per workspace. Behind that name sits a
**config** made of two pieces, *what* to serve (served entities) and *how to route traffic
across them* (traffic config), plus a gateway for rate limits and a live `state`.

| Model type | What it is | Billing / sizing |
|---|---|---|
| **Databricks-hosted foundation models** | Foundation Model APIs (Llama, Claude, Gemini, GTE/BGE embeddings…) pre-provisioned in every workspace under the `system.ai.*` catalog | **Pay-per-token** (per-1M-token) or **provisioned throughput** (dedicated GPU, guaranteed throughput) |
| **External models** | Third-party providers (OpenAI, Anthropic, Amazon Bedrock, Google Vertex AI, Cohere…) behind one Databricks credential | Provider pricing; credentials centralized in the gateway |
| **Custom models** | Your own MLflow **PyFunc** (scikit-learn, XGBoost, PyTorch, Hugging Face), **agents are custom models** (wrapped in `ResponsesAgent`) | Auto-scaling from zero; GPU or CPU workloads |

**Foundation Model APIs are OpenAI-compatible**: you can point the OpenAI SDK at your
Databricks endpoint and get chat/completions/embeddings without rewriting client code. That
makes pay-per-token the fastest way to experiment; provisioned throughput is the production
answer when you need latency/throughput guarantees or a fine-tuned model.

> **Name note.** The "Mosaic AI" prefix has been retired in the docs, it is just
> **Model Serving** now (you will still see "Mosaic AI Model Serving" in older marketing).
> "AI Gateway" is now **Unity AI Gateway**.

The endpoint lifecycle, end to end:

```mermaid
%%{init:{"theme":"base","fontFamily":"Helvetica Neue,Helvetica,Arial,sans-serif","flowchart":{"curve":"basis","padding":14,"nodeSpacing":45,"rankSpacing":55},"themeVariables":{"fontSize":"15px","background":"#FFFFFF","primaryColor":"#EEF2F7","primaryTextColor":"#14213D","primaryBorderColor":"#14213D","secondaryColor":"#FFF1E3","secondaryTextColor":"#14213D","tertiaryColor":"#E7F4F1","tertiaryTextColor":"#14213D","lineColor":"#64748B","textColor":"#14213D","edgeLabelBackground":"#FFFFFF","clusterBkg":"#F5F8FC","clusterBorder":"#94A3B8","nodeBorder":"#14213D","mainBkg":"#EEF2F7","titleColor":"#14213D"}}}%%
flowchart LR
    REG["Register model in UC\nset @prod alias"] --> CRE[create endpoint\nscale-to-zero]
    CRE --> RDY{state.ready == READY?}
    RDY -- no --> RDY
    RDY -- yes --> QRY[query / stream\nfrom clients]
    QRY --> AB["A/B: update-config\n90/10 split"]
    AB --> VER{challenger wins\non metrics?}
    VER -- no --> AB
    VER -- yes --> SWAP["repoint @prod alias\n+ update-config 100%"]
    SWAP --> GW[put-ai-gateway\nrate limit + guardrails]
    GW --> OBS[export-metrics\nbuild-logs / logs]
    OBS --> DEL[delete endpoint\nwhen retired]
```

Every arrow is a distinct, scriptable step. "Swap the model" is never one step, it is
**alias repoint** plus **endpoint config update**, and both are separate API calls (§3).

---

## 2. Creating a serving endpoint

### 2.1 From the UI

Serving UI → **Create serving endpoint** → pick a model type:

1. **Foundation model**: choose a model (e.g. a Llama chat model or `GTE` embedding),
   pick **pay-per-token** or **provisioned throughput**, name the endpoint, done.
2. **Custom model**: select a model registered in Unity Catalog (or an MLflow run),
   choose a version, set workload size (Small/Medium/Large) and
   **scale-to-zero**, done.
3. **External model**: select the provider, paste/select the API key secret, choose a
   model name (e.g. `gpt-4o`), done.

### 2.2 From the CLI

The CLI is the automation path (and the one DABs/CI use). Discover commands first, do not
guess flags:

```bash
databricks serving-endpoints -h
databricks serving-endpoints create -h
```

Create a **custom** endpoint that scales to zero (the cheap default for a dev endpoint):

```bash
databricks serving-endpoints create zrl-eta-model \
  --json '{
    "served_entities": [{
      "entity_name": "zrl_.zorologistics.eta_model",
      "entity_version": "1",
      "min_provisioned_throughput": 0,
      "max_provisioned_throughput": 0,
      "workload_size": "Small",
      "scale_to_zero_enabled": true
    }],
    "traffic_config": {
      "routes": [{
        "served_entity_name": "zrl_eta_model-1",
        "traffic_percentage": 100
      }]
    }
  }' --profile zrl
```

`scale_to_zero_enabled: true` + `min_provisioned_throughput: 0` means the endpoint costs
nothing while idle and cold-starts on the first request, perfect for the ETA model that ops
queries a few thousand times a day.

Create is long-running; the CLI waits by default. Add `--no-wait` to return immediately and
poll readiness:

```bash
databricks serving-endpoints get zrl-eta-model --profile zrl \
  | jq '{ready: .state.ready, config_update: .state.config_update}'
```

**Both** matter: `state.ready == "READY"` means *some* config is live; during a version swap
`ready` stays `READY` while `state.config_update == "IN_PROGRESS"`. Fully ready =
`ready == READY` **and** `config_update == NOT_UPDATING`.

### 2.3 Python (MLflow Deployments client)

```python
from mlflow.deployments import get_deploy_client

deploy = get_deploy_client("databricks")

deploy.create_endpoint(
    name="zrl-eta-model",
    config={
        "served_entities": [{
            "entity_name": "zrl_.zorologistics.eta_model",
            "entity_version": "1",
            "workload_size": "Small",
            "scale_to_zero_enabled": True,
        }],
        "traffic_config": {
            "routes": [{"served_model_name": "eta_model-1", "traffic_percentage": 100}]
        },
    },
)
```

> **Gotcha:** in `traffic_config.routes[].served_model_name`, the value is
> `"<model>-<version>"` (e.g. `eta_model-1`), not the catalog path. Get it wrong and the
> route silently points nowhere. The CLI/API auto-derives the entity's name from the served
> entity; you must reference the exact `<model>-<version>` string in `traffic_config`.

> **Second gotcha (SDK only):** `tags=` is a **top-level keyword** of `create_endpoint`,
> not a field inside `config`. Same `[{key, value}]` shape as the CLI `patch --add-tags`.

### 2.4 The full lifecycle reference

One command (or SDK method) per phase, learn the shape once and script it:

| Phase | CLI | SDK (`deploy` client / `WorkspaceClient`) |
|---|---|---|
| Create | `serving-endpoints create <NAME> --json '…'` | `deploy.create_endpoint(name=…, config=…)` |
| Inspect state | `serving-endpoints get <NAME>` | `deploy.get_endpoint(name=…)` |
| List | `serving-endpoints list` | `w.serving_endpoints.list()` |
| Update config | `serving-endpoints update-config <NAME> --json '…'` | `deploy.update_endpoint(endpoint=…, config=…)` |
| Patch tags | `serving-endpoints patch <NAME> --json '…'` | `w.serving_endpoints.patch(name=…, …)` |
| Gateway | `serving-endpoints put-ai-gateway <NAME> --json '…'` | `w.serving_endpoints.put_ai_gateway(name=…, …)` |
| Schema | `serving-endpoints get-open-api <NAME>` | `w.serving_endpoints.get_open_api(name=…)` |
| Build logs | `serving-endpoints build-logs <NAME> <ENTITY>` |(read via `get` → entity name) |
| Runtime logs | `serving-endpoints logs <NAME> <ENTITY>` | n/a |
| Metrics | `serving-endpoints export-metrics <NAME>` | n/a |
| Delete | `serving-endpoints delete <NAME>` | `w.serving_endpoints.delete(name=…)` |

For `build-logs` / `logs`, the **served entity name** is not the endpoint name, read it from
`get` output at `served_entities[].name` (e.g. `zrl_eta_model-1`). Getting this wrong is the
most common "logs are empty" mistake.

---

## 3. Traffic routing & A/B via model versions

A serving endpoint can host **multiple served entities** and split traffic between them.
This is how you A/B a new model version or canary it into production with **zero downtime**:

```bash
databricks serving-endpoints update-config zrl-eta-model --json '{
  "served_entities": [
    {"entity_name": "zrl_.zorologistics.eta_model", "entity_version": "1",
     "workload_size": "Small", "scale_to_zero_enabled": true},
    {"entity_name": "zrl_.zorologistics.eta_model", "entity_version": "2",
     "workload_size": "Small", "scale_to_zero_enabled": true}
  ],
  "traffic_config": {
    "routes": [
      {"served_entity_name": "zrl_eta_model-1", "traffic_percentage": 90},
      {"served_entity_name": "zrl_eta_model-2", "traffic_percentage": 10}
    ]
  }
}' --profile zrl
```

Version 2 (the "Challenger") now gets 10% of traffic. After you confirm MAE improved in the
serving metrics, move the `@prod` alias and repoint 100% of traffic, the **alias** and the
**endpoint config** are two separate steps and you must do both:

```python
from mlflow.tracking import MlflowClient
from mlflow.deployments import get_deploy_client

registry = MlflowClient(registry_uri="databricks-uc")
deploy   = get_deploy_client("databricks")

FULL = "zrl_.zorologistics.eta_model"
registry.set_registered_model_alias(FULL, "prod", "2")     # repoint the alias
deploy.update_endpoint(endpoint="zrl-eta-model", config={
    "served_entities": [{"entity_name": FULL, "entity_version": "2",
                         "workload_size": "Small", "scale_to_zero_enabled": True}],
    "traffic_config": {"routes": [
        {"served_model_name": "eta_model-2", "traffic_percentage": 100}]},
})
```

The same convention (aliases `Champion`/`Challenger` or `@prod`) is what you used when you
registered the model in [`07-mlflow-experiments.md`](07-mlflow-experiments.md).

### 3.1 The routing fields, decoded

| Field | Meaning | ZoroLogistics use |
|---|---|---|
| `served_entities[]` | The models/versions the endpoint can serve (name + version + scaling) | v1 and v2 of `eta_model` side by side |
| `traffic_config.routes[]` | What fraction of requests each entity receives | 90/10 during canary |
| `served_entity_name` / `served_model_name` | The `<model>-<version>` string that identifies a route | `zrl_eta_model-2` |
| `traffic_percentage` | Integer % per route (must sum to 100) | 10% challenger |

### 3.2 A canary recipe (steps, not just config)

A safe canary is a *sequence*, not a single `update-config`:

1. **Register** v2 and give it the `Challenger` alias (leave `Champion` on v1).
2. **`update-config`** to 90/10. Watch serving metrics (latency, error rate, your business
   metric) for a few hours, not minutes.
3. **Promote** to 50/50, then 100/0 only after the challenger is stable.
4. **Repoint** `@prod` to v2 and keep a single-entity 100% config (simpler than a permanent
   split).
5. **Roll back** instantly by `update-config` back to v1 100%, no redeploy, no downtime.

The key discipline: **traffic routing and alias state are independent.** A "promoted" model
whose endpoint still routes 100% to v1 is the classic silent failure.

---

## 4. Scale-to-zero, provisioning, and cost shape

| Setting | Effect |
|---|---|
| `scale_to_zero_enabled: true` | Endpoint scales to **0 replicas** when idle; cold start on first request. Zero cost while idle, the right default for dev/low-traffic endpoints. |
| `min_provisioned_throughput` > 0 | Keeps capacity warm; you pay for it even when idle. |
| `max_provisioned_throughput` | Caps scale (and cost), set a sane ceiling for a public endpoint. |
| `workload_size` | Small/Medium/Large (CPU/GPU instance sizing) for custom models. |

> **Pay-per-token vs provisioned throughput:** pay-per-token is usage-only (great for
> experimentation and spiky traffic); provisioned throughput is a committed capacity that
> bills continuously but guarantees latency. For the ETA model, pay-per-token is almost
> certainly right, until you have a latency SLA, do not commit.

### 4.1 Scale-to-zero in practice

Scale-to-zero is the FinOps default, but it is a **latency trade**, not a free lunch:

- **Cold start**: a scale-to-zero endpoint has *no warm replica*, so the first request after
  idle pays a startup penalty (seconds for CPU; longer for GPU). A nightly ETL that calls the
  ETA model at 3 a.m. does not care; a chat assistant a user hits mid-conversation does.
- **Warm-keep is the middle ground**: set `min_provisioned_throughput` just above 0 to keep
  one replica warm and avoid the worst cold starts while still capping idle cost.
- **Measure before committing**: `export-metrics` gives you latency percentiles per served
  entity; use them to decide whether to keep scale-to-zero or pay for a warm floor.
- **Idle still means zero**: with scale-to-zero, an unqueried endpoint bills $0. That is why
  the capstone's `zrl-eta-model` ships with it on.

---

## 5. Unity AI Gateway (formerly AI Gateway)

The gateway is the **governance control plane** for all LLM/agent/MCP traffic, built on
Unity Catalog. It governs three dimensions:

| Dimension | What it governs |
|---|---|
| **Asset** | Models, MCP servers, functions, connections as governed UC securables |
| **Traffic** | Central routing, **rate limits**, **budgets**, usage tracking, cost observability |
| **Behavior** | **Service policies** (guardrails), `ALLOW` / `DENY` / `ASK` per request/response |

### 5.1 Rate limits

Attach a rate limit to an endpoint via `put-ai-gateway`. ZoroLogistics caps the ETA endpoint
so a runaway client cannot blow past the ops budget:

```bash
databricks serving-endpoints put-ai-gateway zrl-eta-model --json '{
  "rate_limits": [{
    "calls": 1000,
    "key": "user",
    "renewal_period": "minute"
  }]
}' --profile zrl
```

- `key` can be `user` (per-identity), `endpoint` (global), or a custom attribute.
- `renewal_period` is `minute` (or a time unit), 1,000 calls/minute/user here.
- A `RATE_LIMIT_EXCEEDED` (HTTP **429**) means the limit tripped; add backoff/retry in the
  client, or raise the limit if the traffic is legitimate.

A fuller gateway config, multiple limits plus a budget, reads:

```json
{
  "rate_limits": [
    {"calls": 1000, "key": "user", "renewal_period": "minute"},
    {"calls": 50000, "key": "endpoint", "renewal_period": "day"}
  ],
  "usage_tracking_config": {
    "enabled": true
  }
}
```

| Knob | Purpose | Typical ZoroLogistics value |
|---|---|---|
| `rate_limits[].key = user` | Per-caller ceiling | 1,000 calls/min/user |
| `rate_limits[].key = endpoint` | Global ceiling across all callers | 50,000 calls/day |
| `usage_tracking_config.enabled` | Record usage for cost observability | `true` (always) |
| `budgets` | Hard spend ceiling per time window | a monthly $ ceiling on the ops agent |

### 5.2 Credential management (external models)

External models store their provider API key **once** as a Databricks secret, and the gateway
injects it on every call, no key ever lives in application code:

```bash
# one-time, from the admin
databricks secrets create-scope zrl-ai --profile zrl
databricks secrets put-secret zrl-ai openai-key --string "$OPENAI_API_KEY" --profile zrl
```

Then create an external-model endpoint that references the secret by path:

```json
{
  "name": "zrl-gpt4o",
  "config": {
    "served_entities": [{
      "name": "gpt-4o",
      "external_model": {
        "name": "gpt-4o",
        "provider": "openai",
        "task": "llm/v1/chat",
        "openai_config": {
          "openai_api_key": "{{secrets/zrl-ai/openai-key}}"
        }
      }
    }]
  }
}
```

The secret stays in the scope; the config stores only the `{{secrets/…}}` reference. Rotating
the key is a `put-secret`, not a code change.

### 5.3 Guardrails (service policies)

**Service policies** (Beta) are SQL-UDF content checks evaluated **ON CALL** (request) and
**ON RESULT** (response). Built-in checks are LLM-as-judge and **fail-closed**:

- `block_unsafe_content`: refuse harmful content.
- `block_jailbreak`: refuse jailbreak/injection attempts.
- `block_hallucination`: flag responses unsupported by retrieved context (RAG).

A policy decides `ALLOW` / `DENY` / `ASK` per request or response. In a freight context where
a hallucinated rate is a liability, you gate the policy-RAG endpoint with
`block_hallucination` so an answer that invents a tariff is refused or flagged for review.

A content-check policy is just a SQL UDF returning a verdict, attached to the securable:

```sql
-- A guardrail that blocks prompts trying to override the assistant's instructions
CREATE OR REPLACE FUNCTION zrl_.zorologistics.no_injection(body STRING)
RETURN CASE
  WHEN lower(body) LIKE '%ignore previous instructions%'
    OR lower(body) LIKE '%act as%'
  THEN '{"decision": "DENY", "reason": "prompt injection pattern detected"}'
  ELSE '{"decision": "ALLOW"}'
END;

-- Attach it to the model/endpoint as a service policy (ON CALL).
```

The three verdicts map to action:

| Verdict | Meaning | Effect on the call |
|---|---|---|
| `ALLOW` | Passes the check | Request/response proceeds |
| `DENY` | Fails the check | Call refused (fail-closed) |
| `ASK` | Needs a human | Flagged for review, not silently blocked |

> **Fail-closed is the point.** If the judge cannot decide (timeout, error), the safe default
> is *deny*, never *allow*. For a refund-issuing agent, a guardrail that silently fails open
> is worse than no guardrail.

---

## 6. OpenAPI schema export

Every serving endpoint exposes its input/output contract as an **OpenAPI 3.1** schema. Use it
to discover a model's request shape (especially embeddings or custom schemas) before you code
against it:

```bash
databricks serving-endpoints get-open-api zrl-eta-model --profile zrl
```

The schema lists paths per served model (e.g. `/served-models/<name>/invocations`) with the
full request/response definitions, parameter types, enums, nullable fields. Feed it to a
typed client generator, or just read it to know whether the ETA model expects
`dataframe_records` vs `inputs`.

Practical uses of the exported schema:

```bash
# 1. Read the request schema for one served model (jq the paths + components)
databricks serving-endpoints get-open-api zrl-eta-model --profile zrl \
  | jq '.paths["/served-models/zrl_eta_model-1/invocations"].post.requestBody'

# 2. Generate a typed client (OpenAPI Generator example)
databricks serving-endpoints get-open-api zrl-eta-model --profile zrl > eta-openapi.json
openapi-generator-cli generate -i eta-openapi.json -g python -o eta_client
```

Because the schema is versioned with the served entity, you can diff it across versions, the
same way you diff a library's public API, before you bump traffic to a new model.

---

## 7. Calling endpoints from Python

### 7.1 databricks-sdk

```python
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# Chat / foundation-model endpoints take a messages array
resp = w.serving_endpoints.query(
    name="databricks-llama-3-1-70b-instruct",
    messages=[{"role": "user", "content": "Summarize freight on-time risk."}],
)
print(resp.choices[0].message.content)

# Custom / classical-ML endpoints take dataframe_records (one dict per row)
eta = w.serving_endpoints.query(
    name="zrl-eta-model",
    dataframe_records=[{
        "distance_km": 1800.0,
        "weight_kg": 850.0,
        "carrier_on_time_rate": 0.88,
        "weather_severity": "moderate",
    }],
)
print(eta.predictions)
```

### 7.2 OpenAI-compatible

Foundation Model API endpoints speak the OpenAI wire format. Point the OpenAI SDK at your
workspace host and call `chat.completions` as if it were OpenAI:

```python
from openai import OpenAI

client = OpenAI(
    api_key="<DATABRICKS_PAT_OR_OAUTH_TOKEN>",
    base_url="https://<workspace-host>/serving-endpoints",
)

resp = client.chat.completions.create(
    model="databricks-llama-3-1-70b-instruct",
    messages=[{"role": "user", "content": "What is the ZoroLogistics refund SLA?"}],
)
print(resp.choices[0].message.content)
```

`model` is the **endpoint name**. The same client works for embeddings
(`client.embeddings.create(model="databricks-gte-large-en", input=[...])`), which is exactly
what the Vector Search RAG lab in [`11-vector-search-rag.md`](11-vector-search-rag.md) leans on.

### 7.3 Streaming

For chat endpoints, stream tokens as they are generated. CLI:

```bash
databricks serving-endpoints query <NAME> \
  --json '{"messages":[{"role":"user","content":"Explain the DG policy"}]}' \
  --stream --profile zrl
```

OpenAI SDK, add `stream=True`:

```python
stream = client.chat.completions.create(
    model="databricks-llama-3-1-70b-instruct",
    messages=[{"role": "user", "content": "Explain the DG policy"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

The `databricks-sdk` equivalent is `w.serving_endpoints.http_request(..., stream=True)` (the
client-side `--stream` maps to a streaming HTTP response). For **off-platform** streaming
clients, a Vercel app or a standalone Node service calling your Databricks gateway with the
Vercel AI SDK, the same OpenAI-compatible wire format works; wire the endpoint name and
`base_url` and you get token streaming across the boundary.

---

## 8. ZoroLogistics: serve the ETA model

**Goal.** Turn the Week-23 point-in-time ETA model (a registered `pyfunc` that predicts
arrival-delay hours from shipment + carrier + lane features) into a governed, rate-limited
REST endpoint ops can call.

1. **Register** the trained model in Unity Catalog with a signature and alias `@prod`
   (see [`09-model-training.md`](09-model-training.md)).
2. **Create** a scale-to-zero endpoint (UI or the CLI JSON above).
3. **Put it behind the gateway** with a rate limit:

```bash
databricks serving-endpoints put-ai-gateway zrl-eta-model --json '{
  "rate_limits": [{"calls": 1000, "key": "user", "renewal_period": "minute"}]
}' --profile zrl
```

4. **Export the schema** and read the input columns:

```bash
databricks serving-endpoints get-open-api zrl-eta-model --profile zrl
```

5. **Ship the client** the ops team pastes into their scheduling tool:

```python
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

def predict_eta(shipment: dict) -> float:
    """Return predicted delay in hours for one shipment feature dict."""
    resp = w.serving_endpoints.query(
        name="zrl-eta-model",
        dataframe_records=[{
            "distance_km": shipment["distance_km"],
            "weight_kg": shipment["weight_kg"],
            "carrier_on_time_rate": shipment["carrier_on_time_rate"],
            "weather_severity": shipment["weather_severity"],
        }],
    )
    return resp.predictions[0]

print(predict_eta({
    "distance_km": 1800.0,
    "weight_kg": 850.0,
    "carrier_on_time_rate": 0.88,
    "weather_severity": "moderate",
}))
```

6. **A/B a new version**: register v2, canary 90/10, then swap to 100% once MAE improves
   (the §3 recipe).

**Acceptance:** the endpoint returns a prediction under a second (warm), 429s when the rate
limit trips, and costs $0 while idle (scale-to-zero). Log the endpoint's **serving metrics**
(`export-metrics`) so the Week-24 FinOps dashboard can show its cost next to the pipeline's.

---

## 9. Troubleshooting

| Symptom | Fix |
|---|---|
| Endpoint stuck `NOT_READY` | Wait (provisioned throughput can take minutes); read `build-logs <NAME> <ENTITY>`, get the entity name from `get` → `served_entities[].name` |
| `RATE_LIMIT_EXCEEDED` (429) | Gateway limit; add backoff, or check `put-ai-gateway` config |
| Query returns 404 | Endpoint still provisioning, check `state.ready` |
| `PERMISSION_DENIED` | Grant `CAN QUERY` on the endpoint (or declare the serving-endpoint resource with `CAN_QUERY` in a Databricks App) |
| Endpoint missing from Serving UI after a CI deploy | The UI filter defaults to "Owned by me"; a deploy job runs as a service principal, switch to "All" (or use `serving-endpoints list`) |
| Client can't find the model name | Copy the live foundation-model endpoint name at runtime (`serving-endpoints list`, filter `system.ai.*`), names rotate |
| `build-logs`/`logs` return empty | You passed the endpoint name, not the served-entity name (`zrl_eta_model-1`); read it from `get` |

> **Verify against live docs.** Endpoint JSON fields, gateway rate-limit keys, and foundation
> model names change; confirm exact flags with `serving-endpoints <cmd> -h` and the docs
> index at `https://docs.databricks.com/llms.txt`.

---

## 10. Try it

Three exercises, each with a check you can run. Use `zrl_.zorologistics.eta_model` (or any
registered model you have) and the `zrl` profile.

**Task 1: Create and inspect a scale-to-zero endpoint.**
Create `zrl-eta-model` from the CLI JSON in §2.2 (add `--no-wait`), then poll it.
*Acceptance check:* `databricks serving-endpoints get zrl-eta-model` shows
`state.ready == "READY"` and `scale_to_zero_enabled == true`; the `get-open-api` output lists
a `/served-models/.../invocations` path whose request body names your input columns.

**Task 2: Canary a challenger without downtime.**
Register a second version, `update-config` to 90/10, then roll back to 100/0 on v1.
*Acceptance check:* during the split, `get` shows two `served_entities` whose
`traffic_percentage`s sum to 100; after rollback, v1 is back at 100 and `state.config_update`
settles to `NOT_UPDATING` (wait for it, not just `READY`).

**Task 3: Trip the gateway rate limit.**
Set a rate limit of 3 calls/minute/user, then fire 5 queries from one client.
*Acceptance check:* the first 3 succeed and the next return HTTP **429** with
`RATE_LIMIT_EXCEEDED`; removing the limit (or waiting a minute) restores success.

---

## 11. Common mistakes

1. **Watching only `state.ready` during a swap.** `ready` stays `READY` while a new config is
   still rolling out. *Fix:* poll `ready == READY` **and** `config_update == NOT_UPDATING`
   before you consider the swap live.
2. **Alias repoint without `update_endpoint`** (or vice-versa). The `@prod` alias and the
   endpoint's `served_entities` are independent; updating one leaves the other stale. *Fix:*
   do both, in the same script, and assert the route's `served_model_name` matches the new
   version.
3. **Wrong route string.** `served_model_name` must be `"<model>-<version>"` (e.g.
   `eta_model-2`), not the catalog path or the entity display name. *Fix:* read the exact
   string from `get` → `served_entities[].name` and reuse it.
4. **Hardcoding a foundation-model name.** Names rotate as new models ship. *Fix:* resolve
   `databricks-…` endpoint names at runtime via `serving-endpoints list` (filter
   `system.ai.*`), don't bake them into code.
5. **Leaving scale-to-zero off on a dev endpoint.** You pay for idle replicas you never use.
   *Fix:* `scale_to_zero_enabled: true` + `min_provisioned_throughput: 0` as the default;
   raise the floor only when a latency SLA demands warm replicas.
6. **Storing provider keys in app code.** The gateway centralizes external-model credentials.
   *Fix:* one secret scope, one `{{secrets/…}}` reference in the external-model config, key
   rotation becomes a `put-secret`, not a redeploy.

---

## Sources

- Model Serving: https://docs.databricks.com/machine-learning/model-serving/
- Foundation Model APIs: https://docs.databricks.com/machine-learning/foundation-model-apis
- External models: https://docs.databricks.com/machine-learning/foundation-models/external-models/
- Deploy agents to serving endpoints: https://docs.databricks.com/agents/custom-agents/model-serving/deploy-agent
- Unity AI Gateway: https://docs.databricks.com/ai-gateway/
- AI governance: https://docs.databricks.com/ai-gateway/ai-governance/
- Service policies (guardrails): https://docs.databricks.com/data-governance/unity-catalog/service-policies/

> *Original AI Engineering Lab writing; endpoint fields, gateway policies, and model names change
> frequently, verify against the live links above.*

---

© 2026 Zorost Intelligence LLC · [zorost.com](https://zorost.com)
