# Week 19: Exercises & Checklist

## Graded exercises

1. **Easy**: Run `notebooks/01-gemini-multimodal-ocr.ipynb` to completion. It renders
   bill-of-lading images locally, extracts fields to structured JSON with Gemini vision, and
   prints per-field accuracy plus a cost-per-document estimate. Record both numbers in the
   Week 19 tracker sheet.

2. **Standard**: Re-run the extraction loop on a *different* Gemini model rung (for example
   `gemini-2.5-flash-lite` vs `gemini-2.5-flash`). Add a markdown cell with a two-row table
   of accuracy vs cost per document, and write one line on whether the cheaper model clears
   your accuracy bar.

3. **Stretch**: Load the extracted JSON into **BigQuery** and run a single
   `ML.GENERATE_TEXT` call that classifies each row (for example `freight_terms` consistency
   or a commodity risk label). Document the table schema and the exact SQL; note where the
   free-tier boundary is for this data.

4. **Portfolio**: Commit a `vertex-deployment-guide.md` (AI Studio vs Vertex, OCR accuracy
   table, ADK agent, eval score, cost per document). This is the **Google column** of the
   three-cloud comparison matrix completed in Week 20.

## Hints

1. **Easy**: Record `OVERALL_FIELD_ACCURACY` and `COST_PER_DOCUMENT_USD`; image rendering
   and accuracy run locally without a key, but the *real* numbers need `GOOGLE_API_KEY`.
2. **Standard**: Change the `MODEL` constant in the `gemini_extract` cell and re-run on the
   same 4 images; compare accuracy vs cost-per-document in the two-row table.
3. **Stretch**: `ML.GENERATE_TEXT` needs a remote model registered first (`CREATE MODEL …
   REMOTE WITH CONNECTION`); load the extracted JSON, then run one classification query and
   note the schema.
4. **Portfolio**: Lead with the AI Studio-vs-Vertex decision, then the accuracy table, the
   ADK eval score, and cost per document, those four headings are the Google column.

## Checklist (mirrors manifest.json + Excel tracker)

- [ ] Mon: Set up Google Cloud and AI Studio; get an API key; check quotas.
- [ ] Tue: Gemini multimodal lab: BoL images → structured JSON; measure accuracy.
- [ ] Wed: Recreate the support agent with ADK/Agent Engine; compare with the Foundry version.
- [ ] Thu: Run a Vertex evaluation on a golden set; log results to BigQuery.
- [ ] Fri: Use case: end-to-end pipeline (images → clean table); publish cost per document.
- [ ] Sat: Take the Week 19 quiz (quiz.md), pass with 8/10; record the score in Notes.
- [ ] Milestone: Update the Excel tracker; commit the Vertex guide.
