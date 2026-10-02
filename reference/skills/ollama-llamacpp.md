# Skill: Ollama & llama.cpp: Running Models Locally

> Part of AI Engineering Lab · Developed by Zorost Intelligence AI Lab · https://zorost.com
> Skill for: **Week 8** (Open Models & Local Inference) · also used in Weeks 9, 10, 17

| | |
|---|---|
| What it is | The two workhorses of local inference: **Ollama** (the friendly model manager + API) and **llama.cpp** (the engine underneath, GGUF quantized models) |
| Best for | Running open models offline, on a laptop or a homelab box, with zero cloud bills |
| Requirements | macOS / Linux / Windows; no GPU required (CPU works, GPU is faster) |
| Cost | Free (open source) |

---

## What it is

**Ollama** wraps llama.cpp in a daemon that manages models, exposes an
OpenAI-compatible REST API on `http://localhost:11434`, and makes "download a
model" a one-liner. **llama.cpp** is the raw C/C++ inference engine, more
control, more flags, more patience. LM Studio (GUI) and Apple MLX (Apple
Silicon-native) sit alongside; see the knowledge base for comparisons
([knowledge-base/08](../knowledge-base/08-local-inference-gpu.md)).

> **Verify against live docs.** Model tags (`qwen2.5:3b`, `llama3.2:3b`, etc.) rotate as
> publishers ship new releases, and the quantization ladder's exact names shift. Treat every
> specific tag and quant name here as "correct at time of writing", `ollama search <term>`
> and the Hugging Face model card are the source of truth for what exists *today*.

## Install & first run

### Ollama

```bash
# macOS / Linux / Windows, install from https://ollama.com/download
ollama pull qwen2.5:3b        # ~2 GB download, runs on CPU
ollama run qwen2.5:3b         # interactive chat, /bye to quit
ollama list                   # what you have locally
```

Useful model tags: `qwen2.5:3b`, `llama3.2:3b`, `phi4-mini`, `gemma3:4b`,
`deepseek-r1:7b`: small first, measure, then size up. (Model names change
often; `ollama search <term>` shows what's current.)

### llama.cpp

```bash
git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
cmake -B build && cmake --build build --config Release -j
./build/bin/llama-cli -m ~/.ollama/models/blobs/<gguf-file> -p "Hello" -n 50
```

## Core workflow

1. **Pick by VRAM**: rule of thumb: ~2 GB RAM per 1B parameters at Q4.
   A 16 GB MacBook comfortably runs 7 to 8B at Q4; 32 GB runs 13 to 14B.
2. **Pull**: `ollama pull <model>` (GGUF files land in `~/.ollama`).
3. **Prompt via API**: everything speaks OpenAI format:

```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
resp = client.chat.completions.create(
    model="qwen2.5:3b",
    messages=[{"role": "user", "content": "Triage this ticket: ..."}],
    temperature=0.0,
)
print(resp.choices[0].message.content)
```

4. **Measure**: tokens/sec is your benchmark:

```bash
ollama run qwen2.5:3b --verbose   # prints eval rate after each reply
```

## Quantization selection guide (per hardware)

The single most important local-inference decision is **which quant to run**. Quantization
shrinks the model's weights so it fits in RAM/VRAM; smaller quants are faster and smaller
but lossier. Pick by *your hardware's memory budget* first, then by *quality tolerance*.

| Hardware (RAM/VRAM) | Comfortable model size at Q4_K_M | Recommended quant | Why |
|---|---|---|---|
| 8 GB unified (base M1/M2 Mac, 8 GB PC) | 3B | **Q4_K_M** (or Q5_K_M if it fits) | 3B is the largest that leaves OS headroom; Q4 is the default quality/size balance |
| 16 GB unified (M-series Mac, 16 GB PC) | 7 to 8B | **Q4_K_M** default; **Q5_K_M** if you can spare the RAM | 7 to 8B at Q4 is the local "sweet spot" for real tasks |
| 24 GB (M-series Max, 24 GB GPU) | 13 to 14B | **Q4_K_M**, or **Q5_K_M** for the 13B | Fits comfortably; bump quality since you have headroom |
| 32 GB / 16 GB dedicated GPU | 13 to 14B | **Q5_K_M** or **Q6_K** | Headroom lets you trade speed for fidelity |
| 64 GB+ / 24 GB+ GPU | 30 to 34B | **Q4_K_M** (34B is large even quantized) | The practical ceiling for most homelabs |

**The quant ladder, from best quality to smallest:**

| Quant | Size vs F16 | When to use |
|---|---|---|
| Q8_0 | ~half | "Lossless-feeling", when RAM is plentiful |
| Q6_K | smaller | High-quality, still fits mid-tier hardware |
| **Q5_K_M** | smaller still | The quality sweet spot, often the best quality-per-GB |
| **Q4_K_M** | ~quarter | The default, best speed/size/quality balance |
| Q3_K_M | small | Tight RAM, willing to accept some loss |
| Q2_K | smallest | Emergencies only, noticeable degradation |

**The rule that survives every model release:** *the biggest model that fits your memory at
Q4_K_M, then quality-up to Q5_K_M only if it still fits.* Do not chase a bigger model at a
lower quant, a 3B at Q4 usually beats a 7B at Q2. And always verify with **your own eval**,
not the published benchmark: run your Week 8 triage prompt at two quants and compare the
answers before you trust a quant for real work.

## Config & power moves

- **Custom system prompt + JSON output**:
  ```python
  resp = client.chat.completions.create(
      model="qwen2.5:3b", temperature=0,
      response_format={"type": "json_object"},
      messages=[
          {"role": "system", "content": "You are a freight support triage agent. Output JSON: {\"category\": ..., \"priority\": ...}"},
          {"role": "user", "content": ticket_text},
      ])
  ```
- **Modelfile**: package your system prompt as a reusable model:
  ```dockerfile
  FROM qwen2.5:3b
  SYSTEM "You are ZoroLogistics triage. Answer with category + priority."
  PARAMETER temperature 0.1
  ```
  `ollama create zoro-triage -f Modelfile && ollama run zoro-triage`
- **llama.cpp flags that matter**: `-ngl 99` (offload layers to GPU),
  `-c 8192` (context), `-t 8` (threads), `--mlock` (keep in RAM).
- **GGUF quantization ladder**: Q8 ≈ lossless-feeling, Q5_K_M the sweet spot,
  Q4_K_M the default, Q2 for emergencies. Perplexity + your own eval decide.
- **Apple Silicon**: Ollama already uses Metal; for MLX-native speed try
  `mlx_lm.generate` for the models that ship MLX weights.

## Offline triage, end to end (recipe)

This is the Week 8 deliverable, complete and in order: **take a support ticket, classify it,
and never touch the network.** It exercises the whole skill in one pass.

```python
# triage.py, classify a ZoroLogistics ticket fully offline
import json
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

SYSTEM = (
    "You are the ZoroLogistics triage agent. Classify each ticket into exactly one "
    "category: tracking, refund, damage, or other. Assign a priority: low, medium, high. "
    "Reply with JSON only: {\"category\": ..., \"priority\": ..., \"reason\": ...}."
)

def triage(ticket: str) -> dict:
    resp = client.chat.completions.create(
        model="zoro-triage",           # the Modelfile model from the previous section
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": ticket},
        ],
    )
    return json.loads(resp.choices[0].message.content)

if __name__ == "__main__":
    print(triage("My shipment ZRL-1042 has been stuck in Dallas for three days."))
    # → {"category": "tracking", "priority": "medium", "reason": "..."}
```

**The recipe's four checks** (do all of them, in this order):

1. **Daemon up**: `ollama serve` if `connection refused` on 11434.
2. **Model present**: `ollama list` shows `zoro-triage` (build it from the Modelfile first).
3. **Offline**: unplug (or `--offline`), then run; it must not hit the network.
4. **Deterministic**: `temperature=0` and `response_format=json_object` so the same ticket
   gives the same shape; sanity-check that `json.loads` never throws on the output.

**Why offline matters here:** a support ticket may contain real customer PII. Local
inference keeps it on the machine, the exact property that makes Ollama/llama.cpp the right
tool for regulated freight workloads, and the reason this recipe (not a cloud call) is the
Week 8 deliverable.

## Batch-processing pattern

Triage is never one ticket, it is a queue. The batch pattern is: **feed a list, process
sequentially, collect results, and write a log you can diff.** Do not parallelize until the
sequential version is correct; a local model saturates one core anyway.

```python
# batch_triage.py, process a list of tickets, write JSONL results
import json, time
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "zoro-triage"

def classify(ticket: str) -> dict:
    resp = client.chat.completions.create(
        model=MODEL, temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Classify as JSON: category + priority + reason."},
            {"role": "user", "content": ticket},
        ],
    )
    return json.loads(resp.choices[0].message.content)

def run_batch(tickets: list[str], out_path="batch_results.jsonl"):
    with open(out_path, "w") as f:
        for i, ticket in enumerate(tickets):
            t0 = time.time()
            result = classify(ticket)
            result["ticket"] = ticket
            result["latency_s"] = round(time.time() - t0, 2)
            f.write(json.dumps(result) + "\n")
            print(f"[{i+1}/{len(tickets)}] {result.get('category')} ({result['latency_s']}s)")

run_batch([
    "Where is ZRL-1042?",
    "I want a full refund for damaged freight.",
    "The driver left the pallet in the rain.",
])
```

**The batch rules:**

- **Write as you go**: one line per result to a JSONL file, so a crash at ticket 40 doesn't
  lose tickets 1 to 39.
- **Log latency per item**: it is your throughput metric, and it shows when a model is
  bigger than the job needs.
- **Re-run is the diff**: the JSONL output is diffable; change the prompt/quant and `diff`
  the two runs to see *exactly* what the change did to your classifications.
- **Cap the queue**: if you have 10,000 tickets, run 50 first, eyeball the categories, then
  scale. The cheap correction happens on 50, not 10,000.

## Benchmark log template

A benchmark without a log is a feeling. Keep this template in a file (e.g.
`benchmarks.md`) and append one block per run. Over Weeks 8 to 9 the log becomes your personal
"which quant for which job" lookup table.

```markdown
### Run #001 to 2026-08-14 · zoro-triage (qwen2.5:3b @ Q4_K_M)
| Field | Value |
|---|---|
| Hardware | MacBook, 16 GB unified, Metal |
| Model / quant | qwen2.5:3b @ Q4_K_M |
| Task | 50-ticket triage batch (Week 8 golden set) |
| Accuracy | 44/50 correct (0.88) |
| Speed | 41 tok/s (eval), 3.1 s avg/ticket |
| Peak memory | 5.2 GB |
| Cost | $0 (offline) |
| Notes | Damaged-freight vs refund confusion on 4 tickets, see diff. |
```

**The fields that matter, and why:**

| Field | Why it matters |
|---|---|
| Hardware / model / quant | The row is meaningless without the exact combo it measured |
| Task + golden set | You can only compare runs measured on the *same* task |
| Accuracy | The quality number, the reason you're benchmarking at all |
| Speed (tok/s) + latency | The throughput number; a model can be accurate and unusably slow |
| Peak memory | Whether it *actually* fit, and with how much headroom |
| Cost | Offline = $0, but log it anyway so the Week 20 comparison has a baseline |
| Notes | The error analysis, "what did it get wrong" is worth more than the score |

**The habit:** append, never overwrite. Ten rows of this log is the Week 9 quantization
lesson *already done*, you will have measured the quality/size/speed tradeoff yourself
instead of reading someone else's table.

## Cost & safety

- Free to run; the cost is RAM/disk and time.
- Models from `ollama.com/library` are vetted builds; GGUF files from random
  Hugging Face repos are not, prefer the original publisher's repo.
- Offline = private: shipment data never leaves the machine. This is why
  local inference matters for regulated workloads.

## Common failures

| Symptom | Fix |
|---|---|
| `Error: model requires more system memory` | Pick a smaller quant or model |
| Slow tokens/sec on Mac | Check Activity Monitor, another app ate the unified memory |
| GPU not used | `ollama ps` shows CPU/GPU split; in llama.cpp raise `-ngl` |
| `connection refused` on 11434 | The daemon isn't running: `ollama serve` |
| Model name 404 in API calls | Use the exact tag from `ollama list` |
| JSON output not parseable | Add `response_format={"type": "json_object"}` and `temperature=0`, and pin the JSON shape in the system prompt |

## Sources

- [Ollama docs](https://docs.ollama.com/) · [llama.cpp](https://github.com/ggml-org/llama.cpp)
- [MLX](https://github.com/ml-explore/mlx) · [LM Studio](https://lmstudio.ai/)
- knowledge-base: [08-local-inference-gpu.md](../knowledge-base/08-local-inference-gpu.md)
- AI Engineering Lab Week 8 notebooks: [`curriculum/week-08/`](../../curriculum/week-08/)

---

© 2026 Zorost Intelligence LLC · https://zorost.com
