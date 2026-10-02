# Week 18: Exercises & Checklist

## Graded exercises

1. **Easy**: Run `notebooks/01-foundry-serverless-endpoints.ipynb` to completion. It
   deploys/calls a serverless endpoint, runs the Week 6 bill-of-lading extraction prompt,
   and prints per-field accuracy plus an estimated cost. Record the printed cost in the
   Week 18 tracker sheet.

2. **Standard**: Run the same extraction prompt against a *second* deployment (for
   example a Phi-4 serverless endpoint vs a GPT deployment in Azure OpenAI). Add a markdown
   cell with a two-row table comparing per-field accuracy and estimated cost, and state in
   one line which model you would pick for high-volume BoL extraction and why.

3. **Stretch**: Put the support-agent endpoint behind the **AI Gateway** (Azure API
   Management). Configure a token-rate-limit policy and a content-safety policy, then fire a
   burst of calls and capture evidence that the rate limit actually throttles. Re-run the
   evaluation batch behind the gateway and confirm the score did not regress.

4. **Portfolio**: Commit a `foundry-deployment-guide.md` to your fork (setup steps,
   endpoint call, agent definition, eval trace, cost estimate, gateway config). This is the
   **Microsoft column** of the three-cloud comparison matrix you complete in Week 20, keep
   the "how do I do X here" notes so the matrix writes itself.

## Hints

1. **Easy**: The printed cost is the final `TOTAL_ESTIMATED_COST_USD`; dry-run still walks
   the whole pipeline, but the *real* number requires credentials, don't record a dry-run
   `0.000` as if it were a measurement.
2. **Standard**: Reuse `call_openai_sdk` with a different `deployment=` argument; keep the
   same 4 documents and seed so the two rows are a fair comparison, not two different tests.
3. **Stretch**: The rate limit only shows itself under a *burst*: fire many requests in a
   tight loop and count the 429/429-equivalent responses as your throttling evidence.
4. **Portfolio**: Structure the guide as a "how do I do X here" list (endpoint, agent, eval,
   gateway, cost), the Week 20 matrix column writes itself from those headings.

## Checklist (mirrors manifest.json + Excel tracker)

- [ ] Mon: Set up the Azure subscription and AI Foundry hub/project (free tier).
- [ ] Tue: Deploy a serverless model endpoint; call it from the Python SDK and OpenAI SDK.
- [ ] Wed: Create the support agent in Foundry with tools; test in the playground.
- [ ] Thu: Run an online evaluation batch; read the trace; fix the worst failure.
- [ ] Fri: Use case: put the agent behind the AI Gateway (rate limit + content safety); publish cost.
- [ ] Sat: Take the Week 18 quiz (quiz.md), pass with 8/10; record the score in Notes.
- [ ] Milestone: Update the Excel tracker; commit the Foundry deployment guide.
