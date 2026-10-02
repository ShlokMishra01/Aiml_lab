# Week 03: Exercises & Checklist

## Graded exercises

1. **Easy**: Run `notebooks/01-eta-regression-baseline.ipynb` to completion. It
   prints a final comparison of MAE/RMSE for the mean/median baseline and three
   regressors. Record the best test MAE in the Week 3 tracker sheet.

2. **Standard**: Add a fourth regressor (for example
   `HistGradientBoostingRegressor`) using the *same* time-aware split and features.
   Report its MAE/RMSE in the same comparison table and state, in one line, whether it
   beats the baseline and by how much (the delta).

3. **Stretch**: Replace the single validation split with `TimeSeriesSplit` from
   scikit-learn and cross-validate your best model, reporting mean ± standard deviation
   of MAE across the folds. Add a markdown cell explaining why a time-ordered
   cross-validation estimate is fairer than one random split.

4. **Portfolio**: Advance the **ETA prediction (ML → DL) with model cards** milestone
   (see [`curriculum/projects/README.md`](../projects/README.md)): commit the Week 3 model card
   and an `experiments.json` log recording every run's model, split dates, seed, and
   metrics, the raw material the Week 4 neural model must beat.

## Hints

1. **Easy**: Record the baseline *and* each model's MAE/RMSE from the printed
   comparison table; the "best" row is the one with the lowest test MAE, and it may
   not be a model at all.
2. **Standard**: Add `HistGradientBoostingRegressor` to the same `models` dict and
   keep the identical `Pipeline([("prep", prep), ("model", ...)])` wrapper so the only
   thing that changes is the estimator.
3. **Stretch**: `TimeSeriesSplit` produces *ordered* train/test index pairs; iterate
   them with your pipeline and average the fold MAEs, and note that you still never
   shuffle inside a fold.
4. **Portfolio**: In `experiments.json`, store the split as the two cut dates
   (`CUT1`, `CUT2`) rather than a percentage, so the log is reproducible, a "80/20"
   string is not enough for a stranger to rebuild your split.

## Checklist (mirrors manifest.json + Excel tracker)

- [ ] Mon: Study supervised learning and the eval mindset: pick the metric before the model.
- [ ] Tue: Run the ETA regression baseline; log MAE/RMSE for 3 models in a comparison table.
- [ ] Wed: Implement a time-aware split and cross-validation; compare models fairly.
- [ ] Thu: On-time classification: precision/recall/F1, threshold tradeoff, confusion matrix.
- [ ] Fri: Use case: write the Week 3 model card (metric, split, top error source) and commit it.
- [ ] Sat: Take the Week 3 quiz (quiz.md), pass with 8/10; record the score in Notes.
- [ ] Milestone: Update the Excel tracker; log all experiments to a JSON experiment log.
