# Week 18: Quiz (10 questions, 8/10 to pass)

1. **MCQ**: In the Foundry hierarchy, which resources does the **hub** own? (see Concepts §Model catalog / hub-project)
   - A) Deployments, evals, and traces
   - B) Azure OpenAI instances, AI Search indexes, storage, key vaults, and the network boundary
   - C) Only the agent definitions
   - D) Nothing; the project owns everything

2. **MCQ**: When you call the OpenAI SDK against Azure, the `model=` argument is your… (see notebook 01 cell 3)
   - A) Raw model ID, e.g. `gpt-4.1`
   - B) Deployment name you chose at deploy time
   - C) Region name
   - D) API version string

3. **MCQ**: Which deployment option bills whether you use it or not? (see Concepts §Deployment table)
   - A) Serverless endpoint (MaaS)
   - B) Provisioned throughput (PTU)
   - C) Pay-per-token on-demand
   - D) None of them

4. **Short answer**: In notebook 01, which **two** BoL fields does `field_matches` compare as integers (numeric comparison, not string equality)? (see notebook 01 cell 12)

5. **MCQ**: Which AI Gateway control is the right tool to cap *monthly spend* so a runaway agent cannot blow the budget? (see Concepts §AI Gateway)
   - A) Token-rate limit
   - B) Semantic cache
   - C) Token-usage quota / cost cap
   - D) Model routing

6. **MCQ**: In notebook 02's dry-run, which golden question fails *before* the fix, and why? (see notebook 02 cell 10)
   - A) Q1 (refund), because the prompt is wrong
   - B) Q4 (customs), because `KEYWORD_DOCS` has no `customs` → `POL-004` mapping
   - C) Q2 (address), because `$85` is misspelled
   - D) Q3 (dangerous goods), because `UN number` is missing from the doc

7. **Short answer**: Name at least **five** of the ten fields the Week 6 `EXTRACT_PROMPT` asks the model to return as JSON. (see notebook 01 cell 4)

8. **MCQ**: What is the recommended production authentication for Foundry code (instead of keys)? (see Concepts §How it breaks)
   - A) Hardcoded API key
   - B) Entra ID via `DefaultAzureCredential` / managed identity
   - C) A shared team password
   - D) No authentication at all

9. **Short answer**: Using the notebook's placeholder prices ($0.15/1M input, $0.60/1M output), compute the cost of one BoL extraction that uses 150 input and 120 output tokens. Show the arithmetic. (see notebook 01 cell 15)

10. **MCQ**: "A trace without a fix is a bug report" means… (see Concepts §Evaluation & tracing)
    - A) You should delete failed traces
    - B) Reading the trace is enough even if the score is unchanged
    - C) The eval loop is only complete when you read the trace, fix the worst failure, and show a before/after score
    - D) Traces are only for LLM-as-judge runs

## Answer key

1. **B**: The hub owns shared enterprise resources; projects hold the team's deployments, evals, and traces. That split is the whole governance point.
2. **B**: In Azure, `model=` is your *deployment name*, not the raw model ID, the classic Week 18 gotcha.
3. **B**: PTU reserves capacity and bills regardless of usage; serverless is pay-per-token.
4. **`quantity` and `gross_weight_kg`**: both are compared with `int(float(pred)) == int(float(truth))`.
5. **C**: A token-usage quota / cost cap bounds cumulative spend; a rate limit only throttles the burst rate.
6. **B**: `KEYWORD_DOCS` deliberately omits `customs`/`storage`, so Q4 (customs hold fee) has no matching doc and fails until the fix adds `customs → POL-004`.
7. Any five of: `shipper`, `consignee`, `port_of_loading`, `port_of_discharge`, `commodity`, `quantity`, `gross_weight_kg`, `declared_value_usd`, `freight_terms`, `date_of_issue`.
8. **B**: Production guidance is managed identity / service principal via `DefaultAzureCredential`; keys are the legacy quick-start path.
9. Input 150 × $0.15/1M = $0.0000225; output 120 × $0.60/1M = $0.0000720; **total ≈ $0.0000945** (under a tenth of a cent).
10. **C**: The loop closes only when the trace leads to a fix with a before/after number; a score without diagnosis, or a diagnosis without a fix, is incomplete.
