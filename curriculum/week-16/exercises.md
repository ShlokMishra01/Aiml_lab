# Week 16: Exercises & Checklist

## Graded exercises

1. **Easy**: Run `notebooks/01-mcp-server-lab.ipynb` end-to-end (no API key needed).
   Copy the tool-schema JSON for `track_shipment` (as returned by `list_tools()`) into the
   Week 16 sheet of the Excel tracker.

2. **Standard**: Add a fourth tool to the MCP server, `get_bol(bol_id)`, backed by
   `zoro.data.bol_samples()`. Re-run the client connection and call the new tool through
   the protocol; confirm its result matches a direct call to `data.bol_samples()`.

3. **Stretch**: In `notebooks/02-multiagent-triage-team.ipynb`, add a fourth specialist
   (billing) and its routing rule, re-run the A/B on the same 10 tickets, and rewrite the
   architecture justification using the new accuracy/latency/cost numbers.

4. **Portfolio**: Commit the MCP server, the triage team, and the A/B report
   (`notebooks/02` output). The report, one table plus one paragraph of justification,
   is a hiring-manager-readable artifact (tracked in
   [`curriculum/projects/README.md`](../projects/README.md)).

## Hints

1. **Easy**: Run notebook 01 top to bottom; the `ROUND_TRIP_TOOLS` number should be `3` when
   the `mcp` SDK is present. Copy the `track_shipment` schema exactly as cell [10] prints it.
2. **Standard**: Add `get_bol(bol_id)` to the server *and* to `MANUAL_SCHEMAS`; `bol_id`
   looks like `ZRL-10000`. Reconnect the client (a new `stdio_client` session) so `list_tools()`
   picks up the fourth tool, then assert its result equals a direct `data.bol_samples()` call.
3. **Stretch**: Add the `billing` specialist by extending `supervisor_classify`, `CAT_TO_ROUTE`,
   and the `add_conditional_edges` map *together*; re-run the same 10 tickets and rewrite the
   justification using the new `ACCURACY_DELTA`.
4. **Portfolio**: The A/B report is the artifact, so ship the table *and* the justification
   paragraph; a reviewer should see the numbers and your decision in the same breath.

## Checklist (mirrors manifest.json + Excel tracker)

- [ ] Mon: Study orchestration patterns and MCP (knowledge-base/10 + knowledge-base/11).
- [ ] Tue: Build an MCP server exposing ZoroLogistics tools; test with an MCP inspector.
- [ ] Wed: Build the multi-agent triage team (supervisor + 3 specialists).
- [ ] Thu: A/B test: multi-agent vs single agent on the same 10 tasks; measure quality and cost.
- [ ] Fri: Use case: publish the A/B report; justify your architecture decision.
- [ ] Sat: Take the Week 16 quiz (quiz.md), pass with 8/10; record the score in Notes.
- [ ] Milestone: Update the Excel tracker; commit the team and the MCP server.
