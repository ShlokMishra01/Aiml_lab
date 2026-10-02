# Week 24: Exercises & Checklist

## Graded exercises

1. **Easy**: Run `notebooks/01-governance-and-finopps.ipynb` to completion. It prints, at the end, the total DBUs, the estimated cost, and the audit-event count. Record all three in the Week 24 tracker sheet.

2. **Standard**: Add a second column mask (e.g. on `delay_hours`) and a second row filter to the governance notebook. Write one sentence each on *who* they protect and *what breaks* (a wrong number, a leak) if the control is removed.

3. **Stretch**: Write the lineage query that traces `gold_on_time_kpis` all the way back to its bronze source tables, then confirm the **column-level** lineage for `on_time_rate` via `system.access.column_lineage`.

4. **Portfolio**: Complete the **ZoroLogistics Lakehouse Intelligence capstone**: follow [`reference/platforms/databricks/capstone/`](../../reference/platforms/databricks/capstone/) to bundle the Weeks 21 to 23 assets into a **Declarative Automation Bundle** with targets, governance, and a FinOps dashboard, then publish the deployment guide in your portfolio.

## Hints

1. **Easy**: Run the notebook to the final cell; the three numbers to record are
   `total DBUs (billing)`, `estimated cost USD`, and `audit events`. A `0.0` DBU total
   on a fresh trial is expected, the billing table fills over time.
2. **Standard**: A second column mask on `delay_hours` follows the same
   `CREATE FUNCTION … RETURN IF(is_account_group_member(…), value, NULL)` +
   `ALTER COLUMN … SET MASK` shape; match the return type to `DOUBLE`. A second row
   filter is another `SET ROW FILTER` keyed to a different column.
3. **Stretch**: Walk `system.access.table_lineage` backwards from
   `gold_on_time_kpis` to its bronze sources (it may take more than one hop), then
   filter `system.access.column_lineage` on `target_column_name = 'on_time_rate'`.
4. **Portfolio**: The capstone `databricks.yml` already declares `pipelines.medallion`
   + `jobs.etl_job`; add `dashboards`, `registered_models`, and your FinOps dataset as
   resources, then follow [`reference/platforms/databricks/capstone/README-run.md`](../../reference/platforms/databricks/capstone/README-run.md)
   for the run order.

## Checklist (mirrors manifest.json + Excel tracker)

- [ ] Mon: Bundle the Weeks 22 to 23 assets into a DAB; validate and deploy with the CLI.
- [ ] Tue: Add CI/CD: GitHub Actions validates and deploys the bundle.
- [ ] Wed: Governance: row filters + column masks + lineage review; write an audit query.
- [ ] Thu: FinOps: billing system-table dashboard; find one cost win; document it.
- [ ] Fri: Use case: capstone demo end-to-end + graduation checklist; publish your portfolio.
- [ ] Sat: Take the Week 24 quiz (quiz.md), pass with 8/10; record the score in Notes.
- [ ] Milestone: Update the Excel tracker: Week 24 done, program complete. 🎓
