# Enterprise Cloud AI Platforms: Azure, Google, and AWS

> **Status:** Research draft · **Owner:** AI Engineering Lab (Zorost Intelligence)
> **Scope:** A learner-oriented deep dive into the three major enterprise cloud AI platforms, Microsoft Azure AI Foundry, Google (AI Studio + Vertex AI), and AWS (Bedrock + SageMaker AI).
> **⚠️ Verify against live docs:** This field changes weekly. Model names, service names, SDK versions, and prices in this document were checked against vendor documentation at the time of writing, but every vendor is shipping aggressively. Before you publish or build on any specific name, price, or limit, re-check the live "model catalog / pricing / release notes" pages linked in the [Sources](#sources) section. The "naming churn" callouts below are deliberate: Microsoft and Google in particular have renamed their AI portals more than once.

---

## A) Microsoft Azure AI Foundry

### 1. Platform overview & mental model

**Azure AI Foundry** (recently rebranded in places as **"Microsoft Foundry"**; formerly "Azure AI Studio," and before that pieces of "Azure Machine Learning Studio") is Microsoft's unified, enterprise-grade platform for building, evaluating, deploying, and governing generative-AI applications on Azure. Think of it as the "control plane" that glues together many previously separate Azure AI services, Azure OpenAI, Azure AI Search, Azure AI Content Safety, Azure Machine Learning, Speech, Vision, Document Intelligence, behind one portal and one set of SDKs.

The mental model is a **hub-and-project (workspace) hierarchy**:

- **Hub (or "AI resource"):** the shared enterprise container. It owns the shared connection resources, the Azure OpenAI Service instances, Azure AI Search indexes, storage accounts, key vaults, and (crucially) the network boundary (VNet/private endpoints). Governance, identity, and security are configured once at the hub and inherited by projects.
- **Project:** a workspace where a team does actual work. A project contains deployments, fine-tuning jobs, prompt-flow flows, evaluation runs, traces, and agent definitions. Multiple projects can share one hub, and a hub can span multiple projects.

This separation is the platform's core idea for the enterprise: **central IT controls the hub (connectivity, models, data, keys); data scientists and developers get freedom inside projects without re-plumbing infrastructure.** [Azure AI Foundry architecture (Microsoft Learn)](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/architecture)

### 2. Portal/console structure

The AI Foundry portal (`ai.azure.com`, now surfaced from the Azure portal) is organized around a left-hand navigation that maps roughly to the lifecycle:

- **Model catalog**: browse, compare, and deploy foundation models (Microsoft/OpenAI, Meta, Mistral, Cohere, DeepSeek, and others).
- **Models + endpoints / Deployments**: see your deployed models and their endpoints and keys.
- **Playgrounds**: interactive chat/completion/realtime "try it" surfaces, with model parameters and prompt iteration.
- **Agents**: build, configure, and deploy agents (Microsoft Agent Framework).
- **Prompt flow**: visual/authoring DAG for orchestrating LLM + tools + retrieval into a callable flow.
- **Evaluation**: run built-in and custom evaluators against a flow/app or a dataset.
- **Tracing**: view end-to-end traces of agent/flow runs.
- **Fine-tuning**: create SFT/DPO fine-tuning jobs.
- **AI services / Content Safety**: configure safety policies and detection.
- **Management center**: hub/project settings, RBAC, networking, billing.

Everything visible in the portal is also reachable **code-first** through the SDKs and CLI (below), so the portal is best understood as a "UI over the same APIs you call in code."

### 3. Model catalog & available models

The **model catalog** aggregates two broad classes of models:

1. **Azure OpenAI models** (first-party, accessed through Azure OpenAI Service), OpenAI's GPT family (e.g. **GPT-4.1**, GPT-4.1-mini, GPT-4o, and the **o-series reasoning models** such as o1/o3/o4-mini), plus DALL·E, Whisper, and embeddings (text-embedding-3). Microsoft also contributes its own open models, most notably **Phi-4** (a small, efficient open-weight model family).
2. **Third-party / open models**: Meta **Llama**, **Mistral**, **Cohere**, **DeepSeek**, and others, deployed via **serverless API endpoints** ("Models as a Service," MaaS) where the model runs in a Microsoft-managed, metered endpoint without you owning infrastructure.

Current flagship names to know (verify currency): **GPT-4.1 / GPT-5-era models** and the **o-series reasoning models** on the OpenAI side, and **Phi-4** on the Microsoft-open side. The exact list and regional availability change constantly, the live matrices are the source of truth. [Azure OpenAI models (Microsoft Learn)](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models)

**Relationship to Azure OpenAI Service:** Azure OpenAI Service is the specific Azure resource that *hosts* OpenAI models. AI Foundry is the *platform* around it. In practice you create an Azure OpenAI resource (or several) attached to a hub, deploy a model into it, and then call that deployment either through the Azure OpenAI SDK/endpoint or through Foundry's unified tooling. For OpenAI models specifically, Foundry and Azure OpenAI are effectively the same thing seen through two lenses.

### 4. Core AI services

Beyond model hosting, the Foundry ecosystem's core adjacent services include:

- **Azure AI Search**: managed vector + hybrid + semantic search, the standard retrieval backend for RAG.
- **Azure AI Content Safety**: prompt shields, jailbreak detection, groundedness checks, and protected-material detection; used to filter both inputs and outputs.
- **Azure AI Document Intelligence**: OCR + document layout/field extraction for RAG ingestion.
- **Azure AI Speech / Vision / Language**: speech-to-text, text-to-speech, translation, OCR, etc.
- **Azure Machine Learning**: the underlying ML platform for training, registries, and compute (much of Foundry is built on it).

### 5. How to authenticate

- **Human/portal:** Entra ID (Azure AD) login, governed by Azure RBAC roles on the hub/project.
- **Code (recommended):** **Entra ID managed identity / service principal** via `DefaultAzureCredential` (from `azure-identity`), rather than keys. The hub/project itself can be reached with a **project connection string** (a URI that encodes subscription/resource-group/project) plus an Entra credential.
- **Keys (legacy/quick-start):** Azure OpenAI resources still expose API keys for quick experiments, but Microsoft's guidance for production is managed identity + role-based access. Key-based access to Foundry projects is being deprecated in favor of Entra.

### 6. Main SDKs & code patterns

Three entry points cover almost everything:

1. **`openai` SDK with Azure endpoints**: the most common "quick start" path for chat completion on Azure OpenAI models. You instantiate `AzureOpenAI` with the Azure endpoint and API version.
2. **`azure-ai-projects` SDK**: the Foundry-native SDK (`AIProjectClient`). It gives you typed access to agents, evaluations, tracing, and the "project" abstraction itself.
3. **`azure-identity` + `azure-ai-inference`**: the newer, model-agnostic **Azure AI Inference SDK** for calling any serverless-endpoint model with a uniform surface.

**Minimal chat completion (OpenAI SDK against an Azure OpenAI deployment):**

```python
import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],   # https://<resource>.openai.azure.com
    api_key=os.environ["AZURE_OPENAI_API_KEY"],           # or use azure-identity + managed identity
    api_version="2024-10-21",
)

resp = client.chat.completions.create(
    model="gpt-4.1",                                      # your *deployment name*, not the raw model id
    messages=[{"role": "user", "content": "Explain a hub vs a project in AI Foundry."}],
)
print(resp.choices[0].message.content)
```

**Project client (Foundry-native, `azure-ai-projects`):**

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

client = AIProjectClient.from_connection_string(
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
    credential=DefaultAzureCredential(),
)
```

**Model-agnostic call (Azure AI Inference SDK):**

```python
from azure.ai.inference import ChatCompletionsClient
from azure.identity import DefaultAzureCredential

client = ChatCompletionsClient(
    endpoint=os.environ["SERVERLESS_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
resp = client.complete(
    model="Phi-4",                                        # any catalog model
    messages=[{"role": "user", "content": "Hello"}],
)
print(resp.choices[0].message.content)
```

### 7. Deployment options

- **Serverless API endpoints (Models-as-a-Service):** pay-per-token, Microsoft-managed; ideal for catalog/open models and getting started.
- **Provisioned throughput (PTUs):** reserved, guaranteed capacity with predictable cost, for OpenAI models at production scale.
- **Managed compute (real-time / batch):** deploy models to your own Azure Machine Learning compute for full control or for custom/fine-tuned models.
- **Azure OpenAI provisioned vs. standard (pay-as-you-go)**: the standard trade-off between guaranteed capacity and metered usage.

### 8. Agent-building services

- **Microsoft Agent Framework** (and the **Azure AI Agent Service** under it) is Foundry's first-class agent runtime. An agent = model + instructions + tools + (optional) vector-store/grounding. Tools include function calling, code interpreter, file search, and connectors to services like Azure AI Search or third-party APIs.
- Agents can be built in the **portal (Agents page)**, through the **`azure-ai-projects` SDK** (an `AIAgent`), or with the **Agent Framework SDKs** (Python/C#/JS), which also support multi-agent orchestration (handoffs) and open-source interoperability.
- **Deployment:** an agent can be exposed as a hosted endpoint, wired into a Foundry project, or run locally via "Foundry Local."
- **MCP support:** Foundry supports the **Model Context Protocol**, you can connect an agent to **MCP server endpoints** (both cloud and local servers) as tools, and Azure API Management can also expose/convert APIs and MCP tools (see AI Gateway below). [Connect agents to MCP server endpoints (Microsoft Learn)](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/model-context-protocol)

### 9. Evaluation & tracing

- **Evaluation:** built-in quality/safety evaluators (groundedness, relevance, coherence, fluency, and custom evaluators), plus the ability to run **LLM-as-a-judge** and metric-based evaluations over a dataset, either in the portal or via the `azure-ai-evaluation` SDK. You can evaluate a prompt-flow flow, an agent, or any callable app.
- **Tracing:** Foundry records end-to-end traces (inputs, tool calls, intermediate steps, outputs) for agents and flows. Traces are viewable in the portal and exportable; the SDK (`azure.ai.projects` / `azure.ai.evaluation`) can enable tracing for your app with minimal code.
- **Prompt flow:** a visual + code authoring tool for building an LLM application as a **DAG of nodes** (prompt → LLM → tool → retrieval → output). It's the vehicle for structured, testable prompt engineering and is tightly coupled to evaluation ("develop a flow, evaluate it, deploy it").

### 10. Fine-tuning

- Supervised fine-tuning (**SFT**) and **DPO** (preference) are supported for eligible models (e.g. GPT-4o, Phi, and several open models).
- Jobs are created in the portal or via SDK (`azure-ai-ml` / Foundry), with a training + validation dataset, then the resulting model is **deployed as its own endpoint** (including as a serverless API).
- **Fine-tuned models are your own**: Microsoft doesn't use your data to train its base models, and fine-tunes are private to your subscription.

### 11. Monitoring / governance (AI Gateway)

- **AI Gateway** is Foundry's governance layer, implemented via **Azure API Management (APIM)** with **GenAI policies**. It sits in front of your model endpoints and provides: **token-rate limiting**, **token-usage quotas/cost caps**, **semantic caching**, **content-safety filtering**, **load balancing across backends**, and **model routing**. APIM also lets you **convert APIs/OpenAPI to MCP** and govern MCP tool calls (rate limiting, safety).
- Broader governance: **Azure RBAC** on hubs/projects, **private networking/VNet**, **Azure Policy**, **cost management**, and **monitoring via Azure Monitor / Application Insights** (logs, metrics, traces for deployed apps).

### 12. CLI

- **AI Foundry CLI / Foundry Local:** a command-line experience (`ai`/`foundry` tooling, plus the **Azure Developer CLI (`azd`) Foundry extensions**) for creating projects, deploying agents, running evaluation, and doing local agent development with `azd ai agent`-style commands. It complements `az` (the general Azure CLI). [Install the Azure Developer CLI Foundry extensions (Microsoft Learn)](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/install-cli-foundry-extensions)

### 13. Pricing model (rough)

- **Pay-as-you-go (serverless/standard):** per-token (input/output priced separately, often with output more expensive) and/or per-image, per-minute for speech. Varies by model.
- **Provisioned throughput (PTU):** reserve capacity (e.g., per "PTU" hour) for guaranteed throughput at a discount vs. pay-as-you-go.
- **Fine-tuning:** training cost (per token-hour/compute) + per-hour hosting of the fine-tuned model.
- **Azure OpenAI vs. OpenAI parity:** Azure generally prices at parity with OpenAI's own API for equivalent models, but bills through Azure with enterprise agreements, reservations, and consolidated Azure cost management. Always check the live **Azure OpenAI pricing page**.

---

## B) Google (AI Studio + Vertex AI)

### 1. Platform overview & mental model

Google splits its generative-AI surface into **two entry points over largely the same Gemini models**:

- **Google AI Studio** (`aistudio.google.com`), the **developer/experiment sandbox**. Free tier, no cloud project required (just a Google account and an **API key**), optimized for prompt testing, prototyping, and quick Gemini API calls. Great for learning; not designed for enterprise production control.
- **Vertex AI** (in Google Cloud Console), the **enterprise platform**. Same Gemini models plus hundreds of others, but with cloud project billing, IAM, VPC Service Controls, quotas, and MLOps. This is where you productionize.

**Mental model:** AI Studio = "open the hood and tinker with Gemini for free." Vertex AI = "run AI as governed enterprise infrastructure on GCP." The two converge through a documented **migration path**, you can start in AI Studio and later point the same code at Vertex with different credentials. [Migrate from Google AI Studio to Vertex AI (Google Cloud docs)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/migrate/migrate-google-ai)

### 2. Portal/console structure

- **Google AI Studio:** a single-page workspace, prompt builder, model selector, **"Get code"** button (generates a runnable snippet in Python/JS/etc.), prompt gallery, and tuning. Minimal structure, zero cloud ceremony.
- **Vertex AI (console):** left-nav with **Vertex AI Studio** (prompt/chat playground, tuning), **Model Garden** (catalog), **Agent Builder / Agent Engine**, **Evaluation**, **Pipelines**, **Training**, **Deployment / Model Registry**, **Feature Store**, **Metadata**, and **Colab Enterprise**. It is the full MLOps console.

### 3. Model catalog & available models

**Gemini** is the flagship family, with a clear size/cost ladder (naming is tier + generation):

- **Gemini 2.5 Pro**: the flagship "thinking"/frontier model (large context, best reasoning).
- **Gemini 2.5 Flash**: the cost/performance workhorse; low latency, lower price.
- **Gemini 2.5 Flash-Lite**: the cheapest, for high-volume/simple tasks.
- **Gemini 2.5 Pro / Flash "Thinking" variants**: models that expose internal reasoning with controlled budget.
- (Historically: Gemini 1.5 Pro/Flash, Nano for on-device, and **Gemma** as the open-weight sibling, Google's open model family analogous to Llama.)

Beyond Gemini, **Model Garden** surfaces a broad catalog of **first-party (Gemini, Imagen for images, Veo for video, Chirp for speech), open (Llama, Mistral, Gemma), and partner models**, including many deployable to Vertex endpoints. [Model Garden supported models (Google Cloud docs)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-garden/available-models)

### 4. Core AI services

- **Vertex AI Studio**: prompt/chat playground, plus tuning.
- **Model Garden**: the catalog/discovery layer.
- **Agent Builder / Agent Engine**: agentic RAG and agent deployment (below).
- **Vertex AI Evaluation, Pipelines, Prediction (endpoints), Training**: the MLOps backbone.
- **BigQuery ML**: train/invoke ML **inside BigQuery with SQL**, including **`ML.GENERATE_TEXT`**-style remote calls to Gemini for in-warehouse generation/embedding. This is a distinctive "AI without leaving the data warehouse" capability.
- **Colab Enterprise**: managed, governed Colab notebooks for data scientists (the enterprise version of the free Google Colab).

### 5. How to authenticate

- **AI Studio:** a simple **Gemini API key** (created in AI Studio), the easiest possible auth for learning.
- **Vertex AI:** **Google Cloud application default credentials (ADC)**, `gcloud auth application-default login` for local dev, or a **service account** key/workload identity in production. Vertex calls go through GCP IAM and project quotas.
- **Unified `google-genai` SDK** can target either: pass `api_key` for AI Studio, or `vertexai=True` + project/location for Vertex.

### 6. Main SDKs & code patterns

The **`google-genai`** SDK (Python: `google-genai`; also TS/Go/Java) is the current recommended unified client, it replaced the older `google-generativeai` ("Gemini API") and `vertexai`-garden paths.

**Minimal chat completion (Gemini API via AI Studio key):**

```python
from google import genai

client = genai.Client(api_key="YOUR_API_KEY")          # AI Studio key
resp = client.models.generate_content(
    model="gemini-2.5-flash",                          # or gemini-2.5-pro, gemini-2.5-flash-lite
    contents="Explain the difference between AI Studio and Vertex AI.",
)
print(resp.text)
```

**Same call on Vertex AI (enterprise):**

```python
from google import genai

client = genai.Client(
    vertexai=True,                                     # switches to Vertex auth + project
    project="your-gcp-project",
    location="us-central1",
)
resp = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain Vertex AI Model Garden.",
)
print(resp.text)
```

### 7. Deployment options

- **AI Studio:** no deployment, it's a playground that returns API responses.
- **Vertex AI:** deploy models to **Prediction/Model endpoints** (serverless or dedicated), use **Batch prediction**, or call Gemini directly through the API with project quotas. **Model Garden** supports one-click "deploy to endpoint" for open models.

### 8. Agent-building services

- **Agent Builder**: the no-code/low-code agent + grounded RAG builder (search-your-own-data grounded on Vertex AI Search / Google Search). You pick a model, connect data sources/tools, define instructions, and get a testable agent with governance.
- **Agent Engine**: the managed **runtime** that hosts/deploys agents (including ADK-built agents) as scalable endpoints with sessions, memory, and orchestration.
- **ADK (Agent Development Kit)**: Google's **code-first, open-source** agent framework (Python; lightweight, LangGraph-style orchestration, multi-agent, tool calling). ADK agents can be deployed to Agent Engine.
- **MCP support:** the ADK and Agent Engine/Agent Builder support the **Model Context Protocol** for attaching tools, and Vertex offers "advanced tool governance" for agent tool/MCP access control.

### 9. Evaluation & fine-tuning

- **Vertex AI Evaluation**: model-based/LLM-as-judge evaluation with a library of metric templates, plus **Gen AI evaluation service** for comparing prompts/models and running offline/batch evaluation on datasets.
- **Fine-tuning:** **supervised fine-tuning (SFT)** of Gemini (e.g., Gemini 2.5 Flash) with your own dataset, plus continued pre-training and RLHF for select models. Managed tuning jobs produce a private, deployable model. [Tune Gemini models by using supervised fine-tuning (Google Cloud docs)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini-use-supervised-tuning)

### 10. Monitoring / governance

- **Vertex AI:** IAM roles, **VPC Service Controls**, CMEK, audit logs, quotas, and **Model Monitoring** for drift/alerts on endpoints. Enterprise controls are the main differentiator vs. AI Studio.
- **AI Studio:** essentially none of these, data may be used to improve Google's products (by default), no enterprise isolation. This is the single most important thing to teach learners: **do not send sensitive data through the free AI Studio tier.**

### 11. Pricing (rough)

- **AI Studio free tier:** a daily request quota on Gemini API (historically on the order of tens-to-hundreds of requests/day depending on model and tier, e.g. free tier vs. paid "Tier 1" at ~1,000 RPD for Flash). Exact limits change; check the live Gemini API quota page.
- **Paid Gemini API (AI Studio):** per-token (input/output) and per-image, with **context caching** discounts; a "pay-as-you-go" tier removes the free-tier caps.
- **Vertex AI:** per-token/per-image/per-second for Gemini (priced at parity-ish with the Gemini API but billed through Google Cloud), plus endpoint hosting, tuning, and pipeline costs. **BigQuery ML** and other services bill separately. Always confirm against the live **Gemini/Vertex pricing pages**, prices per million tokens drop frequently.

---

## C) AWS (Bedrock + SageMaker AI)

### 1. Platform overview & mental model

AWS's generative-AI story is best understood as **two complementary layers**:

- **Amazon Bedrock**: the **managed foundation-model layer**. "Call models as an API without running any infrastructure." It unifies many third-party and first-party models behind one **Converse API**, and layers on RAG, agents, guardrails, and evals.
- **SageMaker AI**: the **build/train/deploy-your-own-model layer**. "Bring your own data and models, train on managed clusters, deploy to endpoints." This is AWS's classical ML platform now refocused on generative AI (LLM fine-tuning, HyperPod, JumpStart).

**Mental model:** Bedrock = consume models + managed GenAI features (RAG/agents/guardrails). SageMaker = build, fine-tune, and serve models you own. A production RAG app commonly uses **Bedrock (model + Knowledge Bases) + SageMaker (if fine-tuning)**. Around them sit **Amazon Q** (end-user/workplace AI assistants) and **PartyRock** (a free, no-code playground for experimenting with Bedrock models).

### 2. Portal/console structure

- **Bedrock console:** left-nav with **Model catalog**, **Playgrounds** (Chat/Text/Image), **Knowledge Bases**, **Agents**, **Guardrails**, **Prompt management**, **Model evaluation**, **AgentCore**, **Marketplace**, and **Cross-region inference** settings.
- **SageMaker AI console:** **SageMaker Studio** (the unified IDE/workspace), **JumpStart** (one-click model catalog + fine-tune + deploy), **Training jobs**, **HyperPod** (resilient large-scale GPU clusters), **Inference/endpoints**, **Model Customization** (fine-tuning), plus Pipelines, Feature Store, and Model Registry.

### 3. Model catalog & available models

Bedrock's catalog spans **first-party and third-party** foundation models, all callable through the same Converse/InvokeModel surface:

- **Amazon Nova**: AWS's own first-party family: **Nova Pro, Nova Lite, Nova Micro** (text), **Nova Canvas** (image) and **Nova Reel** (video). Cheapest, deep AWS integration.
- **Anthropic Claude**: **Claude 3.7 Sonnet / Claude 4** families; the flagship frontier models on Bedrock for reasoning/coding (and the anchor of many Bedrock agents).
- **Meta Llama**: Llama 3.x / 4 open-weight models.
- **Mistral**: Mistral/Mixtral open models.
- **Amazon Titan**: AWS's older first-party text/embedding models (embeddings still useful for RAG).
- Plus **Cohere, Stability AI, DeepSeek**, and others via **Bedrock Marketplace**.

**Converse API** is the key abstraction: a single, provider-neutral request/response format (system/messages/tool-calling) that lets you swap models without rewriting code. [Supported models & features for Converse API (AWS docs)](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-supported-models-features.html)

### 4. Core AI services

- **Knowledge Bases (RAG)**: fully managed ingestion + retrieval: point it at S3/other sources, it chunks, embeds (Titan/Cohere), stores vectors (OpenSearch Serverless/Aurora/Pinecone/etc.), and exposes `retrieve`/`retrieve_and_generate`.
- **Agents**: managed agent orchestration: model + instructions + action groups/tools + knowledge bases, with multi-agent collaboration and code interpreter.
- **AgentCore**: the newer **managed agent runtime infrastructure**: hosts agents (including LangGraph/Strands-style open frameworks) with memory, sessions, and tool/gateway controls, aimed at running agentic systems at scale.
- **Guardrails**: configurable safety filters (denied topics, content filters, PII redaction, custom word filters) applied to model I/O.
- **Prompt management**: versioned, cataloged prompts with the ability to invoke by ARN.
- **Model evaluation**: automatic (benchmark) and human-in-the-loop (LLM-as-judge) evaluation jobs.
- **Bedrock Marketplace**: browse/deploy third-party and specialized models.

### 5. How to authenticate

- **AWS IAM** everywhere. Bedrock/SageMaker calls are authorized by **IAM roles/policies** (e.g. `bedrock:InvokeModel`, `bedrock:Converse`, `sagemaker:*`). No API keys, you sign requests with credentials from environment, EC2 instance role, or SSO (`aws sso login`). Model access is **explicitly enabled per model** in the Bedrock console before you can invoke it.

### 6. Main SDKs & code patterns

**`boto3`** is the AWS SDK for Python; Bedrock runtime calls go through the `bedrock-runtime` client. The **Converse API** is the recommended modern pattern (replacing raw `invoke_model` with provider-specific JSON bodies).

**Minimal chat completion (boto3, Converse API):**

```python
import boto3

client = boto3.client("bedrock-runtime", region_name="us-east-1")

resp = client.converse(
    modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",   # or a Nova/Llama/Mistral model id
    messages=[
        {"role": "user", "content": [{"text": "Explain Bedrock vs SageMaker."}]}
    ],
)
print(resp["output"]["message"]["content"][0]["text"])
```

(Also worth knowing: `invoke_model` for legacy/streaming use cases, the higher-level **`boto3` Agents/Knowledge Bases** clients, and **`@aws-sdk/client-bedrock-runtime`** in TypeScript.)

### 7. Deployment options

- **Bedrock:** serverless by default, no endpoints to manage. **On-demand** (pay-per-token) vs. **Provisioned Throughput** (reserve capacity, buy model units for guaranteed throughput at a discount). **Cross-region inference** routes traffic across regions in a pre-defined set for higher throughput and resilience.
- **SageMaker:** **real-time endpoints**, **batch transform**, **serverless inference**, and **async inference**, with **multi-model endpoints** and **autoscaling**. **HyperPod** provides resilient, high-performance GPU clusters for large training/fine-tuning jobs (checkpointing, auto-repair).

### 8. Agent-building services

- **Bedrock Agents**: build agents that call knowledge bases and tools (Lambda/action groups), with multi-agent collaboration.
- **AgentCore**: deploy/manage **code-first agents** (LangGraph, Strands, etc.) with managed runtime, memory, sessions, and an API gateway for tools (with optional OAuth/Cedar-policy tool access control). This is AWS's answer to "run my agent framework in production."
- **Amazon Q**: pre-built assistant products: **Amazon Q Developer** (coding assistant in IDE/CLI, plus agentic features) and **Amazon Q Business** (workplace assistant grounded in your enterprise data via connectors). These are "assistants you buy" rather than "agents you build."
- **PartyRock**: a free, shareable, no-code playground (drag-and-drop widgets) that runs on Bedrock models, the best zero-friction "taste of Bedrock" for learners.

### 9. Evaluation & fine-tuning

- **Bedrock Model Evaluation**: automatic evaluation (built-in benchmarks + custom metrics) and human evaluation workflows (LLM-as-judge with your own rubric).
- **Fine-tuning:** **SageMaker Model Customization** fine-tunes both first-party (Nova) and open (Llama/Mistral) models with SFT/DPO/reinforcement approaches; **Bedrock** also supports custom model import and some fine-tuning flows. The fine-tuned model is then deployed to a SageMaker endpoint (or, for Nova, back through Bedrock).

### 10. Monitoring / governance

- **Bedrock Guardrails** for content safety; **CloudWatch** for logs/metrics/alarms; **CloudTrail** for API audit; **IAM + SCPs** for access; **model invocation logging** to S3/CloudWatch.
- **SageMaker** adds **Model Monitor** (drift/quality), SageMaker Clarify (bias/explainability), and full training-job observability.
- Enterprise governance anchors: IAM, KMS, VPC endpoints, AWS Organizations/SCPs, and the AWS Well-Architected + Responsible AI frameworks.

### 11. Pricing (rough)

- **Bedrock on-demand:** per-token (input/output) or per-image, model-specific. Nova is typically cheapest; Claude frontier models most expensive.
- **Provisioned Throughput:** reserve "model units" per hour (commitment-based, significant discount vs. on-demand) for guaranteed throughput.
- **Cross-region inference:** billed at the same on-demand token rates but lets you pool capacity across regions (no extra per-call cost beyond tokens).
- **Knowledge Bases / Agents / Guardrails / AgentCore:** mostly pay-per-use (tokens + storage + vector DB + per-session/per-node runtime for AgentCore).
- **SageMaker:** pay for **compute-hour** of training/inference instances (on-demand or spot), plus storage. **JumpStart** models deploy to endpoints billed like normal SageMaker inference.
- Always confirm on the live **Bedrock pricing page**, token prices change and model ids get superseded frequently.

---

## Comparison Table

| Dimension | **Azure AI Foundry** | **Google (AI Studio + Vertex AI)** | **AWS (Bedrock + SageMaker)** |
|---|---|---|---|
| **Model access** | Azure OpenAI (GPT/o-series, Phi) + Llama/Mistral/Cohere/DeepSeek via serverless endpoints | Gemini 2.5 (Pro/Flash/Lite) + open/partner models in Model Garden | Claude, Nova, Llama, Mistral, Titan, Cohere + Marketplace |
| **Unified API abstraction** | OpenAI SDK + Azure AI Inference SDK (serverless) | `google-genai` SDK (one client for AI Studio & Vertex) | **Converse API** (provider-neutral), the cleanest of the three |
| **Agent building** | Microsoft Agent Framework + Azure AI Agent Service; portal + SDK | Agent Builder (low-code) + Agent Engine (runtime) + ADK (code-first) | Bedrock Agents + **AgentCore** (managed runtime for LangGraph/Strands) |
| **RAG** | Azure AI Search (vector/hybrid/semantic) + agent file-search/grounding | Vertex AI Search / Agent Builder grounding; BigQuery ML in-warehouse | **Bedrock Knowledge Bases** (managed ingest+retrieve) |
| **Evals** | Foundry Evaluation + tracing (built-in + LLM-as-judge) | Vertex AI Evaluation / Gen AI Eval service | Bedrock Model Evaluation (auto + human/LLM-as-judge) |
| **Fine-tuning** | SFT/DPO on GPT/Phi/open models, private deploy | SFT of Gemini (plus RLHF/CPT on select models) | SageMaker Model Customization (SFT/DPO) on Nova/Llama/Mistral |
| **Serving** | Serverless endpoints, PTU, managed compute | Vertex Prediction endpoints (serverless/dedicated), batch | Bedrock serverless + Provisioned Throughput + cross-region inference; SageMaker endpoints |
| **Governance** | RBAC, VNet/private endpoints, APIM AI Gateway (GenAI policies), Content Safety | IAM, VPC-SC, CMEK, quotas, model monitoring (Vertex only) | IAM/SCPs, Guardrails, CloudTrail, VPC endpoints, model-invocation logging |
| **Pricing** | Per-token + PTU + fine-tune/hosting | Per-token; free AI Studio tier; Vertex pay-as-you-go | Per-token on-demand + Provisioned Throughput; SageMaker per compute-hour |
| **Learning curve** | Medium, hub/project concept + Entra ID adds ceremony | **Lowest to start (AI Studio), medium to productionize (Vertex)** | Medium-high, IAM + two overlapping platforms (Bedrock vs SageMaker) |

---

## Which Platform for Which Learner

- **Total beginner, wants instant gratification and the cheapest possible start → Google AI Studio.** A browser, a Google account, and a free API key get you a working Gemini chat call in minutes with zero infrastructure. The free tier is the best "hello world" in the industry. Just learn the rule early: it's not for sensitive data.

- **Learner who wants a clean, single mental model for "call any model with one API" → AWS Bedrock (Converse API).** The Converse API's provider-neutral messages format is the most pedagogically clean way to learn how model invocation, tool calling, and streaming work across Claude/Nova/Llama, one code shape, swap the `modelId`. Bedrock's managed Knowledge Bases + Agents + Guardrails also teach the full RAG → agent → safety arc without running servers.

- **Learner on the Microsoft/enterprise-IT path (Azure shops, .NET/Entra ecosystems) → Azure AI Foundry.** If you're heading toward Azure/Entra ID-heavy enterprises, Foundry teaches the hub/project governance model, managed identity auth, and the AI Gateway pattern that real Azure deployments use. The OpenAI SDK familiarity transfers directly from OpenAI's own API.

- **Learner who wants to actually *train* models, not just call them → SageMaker AI (or Vertex AI).** Bedrock/AI Studio call models; if your goal is fine-tuning, dataset pipelines, HyperPod-scale training, or deploying your own endpoints, SageMaker's JumpStart → Training → Customization → Endpoint path is the most complete "build-it-yourself" curriculum. Vertex AI offers a similarly deep (and in some ways more unified) MLOps alternative if you prefer GCP.

- **Data/analytics professional → Google (BigQuery ML + Colab Enterprise) or AWS (SageMaker + Bedrock).** Google's in-warehouse `ML.GENERATE_TEXT` and Colab Enterprise are uniquely friendly to SQL/notebook-first practitioners; AWS wins if your data already lives in S3/Redshift and you want Bedrock RAG on top.

**Practical recommendation for AI Engineering Lab's teaching order:** start everyone in **AI Studio** (free, 10-minute win) → teach the model-invocation concept again in **Bedrock Converse** (cleanest API) → then contrast **Foundry's hub/project governance** (enterprise reality) → end with a **SageMaker/Vertex fine-tuning** unit for the "own your model" lesson.

---

## ⚠️ What Each Vendor Says Is Changing Fast (verify against live docs)

- **Microsoft:** the portal/product itself has been renamed repeatedly (Azure AI Studio → Azure AI Foundry → **Microsoft Foundry**), and the OpenAI model lineup (GPT-4.x → GPT-5-era, o-series reasoning) turns over every few months. The **`azure-ai-projects` / Agent Framework / AI Inference** SDKs and the **APIM GenAI-policy** surface are actively evolving. Check: [Azure AI Foundry docs](https://learn.microsoft.com/en-us/azure/ai-foundry/) and the [Azure OpenAI model list](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models).

- **Google:** Gemini versions and tier names (2.0 → 2.5 → …) churn quickly, and the **`google-genai` SDK is a moving target** (the older `google-generativeai` and `vertexai` clients are being consolidated into it). Free-tier quotas and token prices are revised often. Check: [Gemini API docs](https://ai.google.dev/gemini-api/docs) and [Vertex AI generative AI docs](https://cloud.google.com/vertex-ai/generative-ai/docs/).

- **AWS:** Bedrock **model ids include dated suffixes** (e.g. `...-20241022-v2:0`) and are frequently superseded; the Claude/Nova/Llama families add new versions constantly. **AgentCore** is brand-new and under heavy iteration. Check: [Amazon Bedrock docs](https://docs.aws.amazon.com/bedrock/) and [SageMaker AI docs](https://docs.aws.amazon.com/sagemaker/).

**Rule of thumb for this knowledge base:** treat every *specific* model name, model id, SDK import, and price in this document as "correct at time of writing, subject to change." For any decision that matters, click through to the live pages above.

---

## Sources

**Microsoft / Azure**
- Azure AI Foundry architecture: https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/architecture
- Azure OpenAI Service models: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models
- Microsoft Agent Framework overview: https://learn.microsoft.com/en-us/agent-framework/overview/
- Azure AI Projects client library (JS): https://learn.microsoft.com/en-us/javascript/api/overview/azure/ai-projects-readme
- Connect agents to MCP server endpoints: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/model-context-protocol
- Install the Azure Developer CLI Foundry extensions: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/install-cli-foundry-extensions
- Deploy models as serverless APIs: https://learn.microsoft.com/en-us/azure/ai-studio/how-to/deploy-models-serverless
- Azure AI Foundry deployment options: https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/deployments-overview
- Prompt flow (Azure Machine Learning): https://learn.microsoft.com/en-us/azure/machine-learning/prompt-flow/community-ecosystem
- Azure API Management GenAI gateway policies (microsoft/azure-skills): https://github.com/microsoft/azure-skills/blob/main/.github/plugins/azure-skills/skills/azure-aigateway/SKILL.md
- Azure OpenAI chat completion (OpenAI SDK): https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/chatgpt

**Google**
- Migrate from Google AI Studio to Vertex AI: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/migrate/migrate-google-ai
- Model Garden supported models: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-garden/available-models
- Tune Gemini models with supervised fine-tuning: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini-use-supervised-tuning
- Migrate to the Google GenAI SDK: https://ai.google.dev/gemini-api/docs/migrate
- Vertex AI Agent Builder (product page): https://cloud.google.com/products/agent-builder
- Gemini 2.5 model family expansion (Google blog): https://blog.google/products-and-platforms/products/gemini/gemini-2-5-model-family-expands/
- Gemini API free tier / quotas (community + forum discussion): https://discuss.ai.google.dev/t/gemini-api-free-tier-daily-quota-25-rpd-blocking-paid-usage-tier-1-1000-rpd/79899

**AWS**
- Amazon Bedrock Converse API supported models: https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-supported-models-features.html
- Amazon Bedrock overview: https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html
- Amazon Bedrock model availability & compatibility: https://docs.aws.amazon.com/bedrock/latest/userguide/models.html
- Bedrock cross-region inference / inference profiles: https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html
- Bedrock capacity & cost optimization (on-demand vs PTU): https://docs.aws.amazon.com/bedrock/latest/userguide/capacity-limits-cost-optimization.html
- Bedrock Runtime code examples (boto3): https://docs.aws.amazon.com/code-library/latest/ug/python_3_bedrock-runtime_code_examples.html
- SageMaker AI (deploy from JumpStart / HyperPod): https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-model-deployment-deploy.html
- Amazon Bedrock AgentCore (AWS news): https://www.aboutamazon.com/news/aws/aws-amazon-bedrock-agent-core-ai-agents

> *Note: this is a synthesized knowledge-base draft written in AI Engineering Lab's own words; no third-party training content was copied. Where a fact is a moving target (model names, ids, prices, quotas), it is flagged inline and should be re-verified against the live vendor links above.*
