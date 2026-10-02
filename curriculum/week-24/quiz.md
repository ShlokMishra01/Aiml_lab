# Week 24: Quiz (10 questions, 8/10 to pass)

Answer each, then check the answer key. Each question ends with a pointer to the
Concepts section (§) or notebook cell it tests.

1. **(MCQ)** Unity Catalog's privilege model is "additive-only." What does that mean
   in practice? (see Concepts §governance)

   - A) You can `DENY` a specific principal
   - B) There is no `DENY`; a principal only gains privileges, and the default is "nothing"
   - C) Grants are automatically replicated across workspaces
   - D) Privileges only apply to tables, not views

2. **(Short answer)** In `01-governance-and-finopps.ipynb`, why must the
   `mask_value` function return `DOUBLE` (and not `STRING`)? (see Concepts §governance;
   notebook 01 cell 7)

3. **(MCQ)** Which query proves *which source tables feed* `gold_on_time_kpis`? (see
   Concepts §system tables; notebook 01 cell 17)

   - A) `SELECT * FROM system.access.audit`
   - B) `SELECT * FROM system.access.table_lineage WHERE target_table_full_name LIKE '%gold_on_time_kpis'`
   - C) `SELECT * FROM system.billing.usage`
   - D) `SHOW GRANTS ON TABLE gold_on_time_kpis`

4. **(MCQ)** In a bundle, what distinguishes the `prod` target from `dev`? (see
   Concepts §DABs)

   - A) `prod` uses a different bundle name
   - B) `mode: production` locks the workspace against accidental overwrites
   - C) `prod` cannot use variables
   - D) `prod` skips `bundle validate`

5. **(Short answer)** Why does the CI/CD reference flow use OIDC token federation
   (or OAuth M2M) instead of a personal access token? (see Concepts §DABs; How it
   breaks)

6. **(MCQ)** A **row filter** is best described as… (see Concepts §governance)

   - A) a view that joins an entitlements table
   - B) a boolean UDF attached to the table that hides rows per group
   - C) an LLM call that rewrites free text
   - D) a column-level NULL mask

7. **(MCQ)** Serverless compute charges a *premium* DBU rate yet often wins on total
   cost. Why? (see Concepts §FinOps)

   - A) It never cold-starts
   - B) It eliminates idle time and over-provisioning, which dominate the classic bill
   - C) It has no rate limit
   - D) DBU rates are flat across SKUs

8. **(Short answer)** The notebook estimates cost with `total_dbu * 0.55` and comments
   that the rate is "illustrative." What is the *correct* way to get a real dollar
   figure, and which table do you join? (see Concepts §FinOps; notebook 01 final cell)

9. **(MCQ)** What does `databricks bundle validate --strict -t dev` guarantee? (see
   Concepts §DABs)

   - A) The resources are deployed to prod
   - B) The config is sound, with warnings treated as errors
   - C) The pipeline has run successfully
   - D) The workspace is locked

10. **(MCQ)** Which is a **column mask** (not `ai_mask`)? (see Concepts §governance;
    How it breaks)

   - A) `ai_mask(text, ARRAY('person_name', 'email'))`
   - B) `ALTER TABLE t ALTER COLUMN value_usd SET MASK f`
   - C) `ai_classify(text, ARRAY('a','b'))`
   - D) `CREATE VIEW v AS SELECT '*** REDACTED ***'`

## Answer key

1. **B.** There is no `DENY`; access is granted additively and the default is
   "nothing," so over-broad grants must be actively revoked.

2. **The mask function's return type must match the masked column's type.** `value_usd`
   is `DOUBLE`, so `mask_value` must return `DOUBLE`; a `STRING` return would fail the
   `SET MASK`.

3. **B.** `system.access.table_lineage` maps source→target tables; filtering the
   target on `gold_on_time_kpis` lists its upstream sources.

4. **B.** `mode: production` locks the workspace against accidental overwrites; `dev`
   uses `mode: development` for fast iteration.

5. **To avoid storing a secret in the repo.** OIDC/M2M exchange the CI platform's
   identity for Databricks OAuth (or use a service-principal client secret managed
   outside the repo), whereas a PAT is a long-lived secret that must not sit in source
   control.

6. **B.** A row filter is a boolean UDF applied with `SET ROW FILTER` that returns
   TRUE only for rows the caller may see.

7. **B.** Classic compute bills idle VMs and over-provisioning (an all-purpose cluster
   idling 22 h/day bills ~24 h for 2 h of work); serverless bills only what runs, so
   the premium rate is often cheaper in total monthly spend.

8. **Join `system.billing.usage` to `system.billing.list_prices`** on `sku_name` (and
   cloud) and multiply `usage_quantity` by the SKU's price (`p.pricing.default`),
   instead of a fixed `0.55` constant.

9. **B.** `validate --strict` checks the bundle configuration and treats warnings as
   errors, it does not deploy or run anything.

10. **B.** `ALTER TABLE … ALTER COLUMN … SET MASK` attaches a deterministic,
    query-time governance policy; `ai_mask` (A) is an LLM content rewrite, and a view
    (D) is a dynamic view, not a column mask.
