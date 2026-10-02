# Week 20: Quiz (10 questions, 8/10 to pass)

1. **MCQ**: Which one-line rule captures the Bedrock vs SageMaker split? (see Concepts §Bedrock vs SageMaker)
   - A) Bedrock = consume models; SageMaker = own models
   - B) Bedrock = train; SageMaker = call APIs
   - C) They are the same service
   - D) Bedrock requires GPU clusters

2. **MCQ**: The Converse API is described as the cleanest of the three clouds because… (see Concepts §Converse API)
   - A) It is the only API that supports images
   - B) One provider-neutral message/tool-calling format lets you swap the `modelId` and nothing else
   - C) It is free
   - D) It auto-fine-tunes models

3. **MCQ**: An `AccessDeniedException` on Bedrock usually means… (see Concepts §How it breaks)
   - A) Your Python is out of date
   - B) You haven't enabled the model in Model access, or your IAM policy lacks the action
   - C) The region is wrong
   - D) The model ID is too long

4. **Short answer**: In notebook 01, which **two** metrics does the RAG section compute, and what does each mean? (see notebook 01 cell 9 to 11)

5. **MCQ**: Bedrock model IDs like `anthropic.claude-3-5-sonnet-20241022-v2:0` carry dated suffixes because… (see Concepts §Model catalog)
   - A) They are random
   - B) Models get superseded often, so you copy the current ID from the console rather than memorize it
   - C) They encode the price
   - D) They encode the region

6. **MCQ**: Which Guardrail filter masks names, addresses, and tracking identifiers? (see Concepts §Guardrails table)
   - A) Denied topics
   - B) Content filters
   - C) PII redaction
   - D) Custom word filters

7. **Short answer**: In notebook 02's dry-run `local_guardrail`, what two conditions cause a prompt to return `GUARDRAIL_INTERVENED`? (see notebook 02 cell 6)

8. **MCQ**: Provisioned Throughput is a bad idea for a lab week because… (see Concepts §Pricing)
   - A) It is pay-per-token only
   - B) It reserves model units per hour and bills whether you use them or not
   - C) It requires a credit card
   - D) It only works with Nova

9. **Short answer**: What does the Week 20 portfolio deliverable (the three-cloud matrix) require in *every* cell, and why does that make it a procurement decision rather than a blog post? (see Concepts §The problem / How it breaks)

10. **MCQ**: In notebook 02's dry-run, the final cell prints… (see notebook 02 cell 11)
    - A) `RECALL: 1.000 GROUNDEDNESS: 1.000`
    - B) `BLOCKED: 3 ALLOWED: 2`
    - C) `EVAL_SCORE: 1.000`
    - D) `BLOCKED: 2 ALLOWED: 3`

## Answer key

1. **A**: Bedrock is the managed foundation-model layer (consume); SageMaker AI is the build/train/deploy-your-own layer (own).
2. **B**: The Converse API's single format across Claude/Nova/Llama/Mistral means you swap `modelId` and nothing else.
3. **B**: `AccessDeniedException` means the model isn't enabled in Model access or the IAM policy lacks the action, check both before touching code.
4. **Recall**: the fraction of questions where retrieval surfaced the correct source document; **groundedness**, the fraction of answers containing the ground-truth fact (cited, not hallucinated). Both are fractions over the question set.
5. **B**: Dated suffixes get superseded often; copy the current ID from the console, never memorize it.
6. **C**: PII redaction masks names, addresses, and tracking identifiers.
7. **Either** the prompt contains an insult word (`idiot`, `garbage`, `stupid`, `useless`) **or** it contains no freight keyword (`shipment`, `refund`, `track`, `freight`, `delivery`, `policy`, `pallet`, `bill`).
8. **B**: Provisioned Throughput reserves model units per hour and meters while idle; on-demand is the right choice for a lab.
9. **Every cell must trace to a measured number** from Weeks 18 to 20 (same golden set, seed, and metric). With per-cell evidence the matrix supports a recommendation; without it, it is just opinion, hence a procurement decision, not a blog post.
10. **B**: `BLOCKED: 3 ALLOWED: 2` (three blocked prompts, insult, cake recipe, pirate joke, and two allowed freight prompts).
