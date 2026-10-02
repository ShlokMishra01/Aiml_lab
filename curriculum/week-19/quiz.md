# Week 19: Quiz (10 questions, 8/10 to pass)

1. **MCQ**: Google AI Studio and Vertex AI expose largely the same Gemini models. What is the single most important difference for *sensitive data*? (see Concepts §AI Studio vs Vertex)
   - A) Vertex models are faster
   - B) AI Studio's free tier may use your data to improve Google's products by default
   - C) Vertex has no quotas
   - D) AI Studio requires a cloud project

2. **MCQ**: In the `google-genai` SDK, what flips the same client from AI Studio to Vertex? (see notebook 02 cell 8)
   - A) Changing the model name
   - B) Setting `vertexai=True` plus `project`/`location`
   - C) Using a different import
   - D) Setting `response_mime_type`

3. **MCQ**: Which Gemini rung is the *cheapest* for high-volume, simple extraction? (see Concepts §Gemini ladder)
   - A) `gemini-2.5-pro`
   - B) `gemini-2.5-flash`
   - C) `gemini-2.5-flash-lite`
   - D) A "Thinking" variant

4. **Short answer**: In notebook 01, why does the pipeline render each BoL **text** to a **PNG** with Pillow before calling Gemini, instead of just pasting the text into the prompt? (see notebook 01 cell 3)

5. **MCQ**: A `429` error mid-batch on Vertex is almost always… (see Concepts §How it breaks)
   - A) A syntax bug
   - B) A quota ceiling, raise per-region/per-model quotas or spread calls out
   - C) A wrong API key
   - D) A model that doesn't exist

6. **MCQ**: Which of Google's three agent layers is the **code-first, open-source** framework you rebuild the support agent with? (see Concepts §Agent stack)
   - A) Agent Builder
   - B) Agent Engine
   - C) ADK
   - D) Colab Enterprise

7. **Short answer**: Name at least **five** of the ten BoL fields the OCR prompt returns as JSON. (see notebook 01 cell 6)

8. **MCQ**: `ML.GENERATE_TEXT` in BigQuery ML lets you… (see Concepts §BigQuery ML)
   - A) Train a transformer from scratch in SQL
   - B) Call Gemini for generation/classification from *inside* BigQuery without leaving SQL
   - C) Replace Vertex IAM
   - D) Render images

9. **Short answer**: Using the notebook's placeholder prices ($0.000315/image, $0.30/1M input, $2.50/1M output), compute the cost of **one** BoL document that is one image, 150 input tokens, and 120 output tokens. Show the arithmetic. (see notebook 01 cell 11)

10. **MCQ**: "A pipeline without a per-field number is just a screenshot of a JSON blob" means… (see Concepts §How it breaks)
    - A) JSON output is never correct
    - B) You must measure accuracy field-by-field against ground truth, not just eyeball a pretty blob
    - C) Screenshots are the deliverable
    - D) Only total accuracy matters, per-field is optional

## Answer key

1. **B**: AI Studio's free tier may use data to improve Google's products by default; Vertex is where governed data goes. The segregation habit is the deliverable.
2. **B**: `genai.Client(vertexai=True, project=..., location=...)` switches auth and billing to Vertex with ADC.
3. **C**: `flash-lite` is the cheapest rung for high-volume/simple tasks; pick the cheapest model that clears your accuracy bar.
4. **To make Gemini exercise *vision*, not read text from the prompt**, rendering to an image keeps the pipeline end-to-end (image → JSON) and tests the OCR capability that is Google's edge.
5. **B**: `429` is a quota problem, not a code bug; check and raise per-region/per-model quotas before the batch.
6. **C**: ADK is the code-first open-source framework; Agent Builder is low-code, Agent Engine is the managed runtime.
7. Any five of: `shipper`, `consignee`, `port_of_loading`, `port_of_discharge`, `commodity`, `quantity`, `gross_weight_kg`, `declared_value_usd`, `freight_terms`, `date_of_issue`.
8. **B**: `ML.GENERATE_TEXT` calls a remote Gemini model from inside BigQuery SQL, "AI without leaving the warehouse."
9. Image $0.000315 + input 150 × $0.30/1M = $0.000045 + output 120 × $2.50/1M = $0.00030 → **total ≈ $0.00066**.
10. **B**: A correct-looking JSON blob can still have the wrong consignee; per-field accuracy against ground truth is the only honest metric.
