# Week 03: Quiz (10 questions, 8/10 to pass)

Answer all ten, then check against the answer key. *(see Concepts §X)* points at a README subsection; *(see notebook cell Y)* points at a cell in `01-eta-regression-baseline.ipynb` or `02-on-time-classification.ipynb`.

1. **Multiple choice.** What does the time-aware split prevent, and how? *(see Concepts §2, split cell)*
   a. Overfitting, by adding more features
   b. Leakage, by splitting on `planned_departure` so train always precedes validation/test
   c. Class imbalance, by resampling the late class
   d. Underfitting, by using a smaller test set

2. **Short answer.** Why is the model trained on `delay_hours` rather than the raw arrival timestamp, when the goal is an ETA? *(see notebook "ETA regression baseline" intro)*

3. **Multiple choice.** On this dataset, which baseline has the *lowest* test MAE, and why? *(see Concepts §6, worked example 2)*
   a. The mean baseline, because the mean minimizes squared error
   b. The median baseline, because `delay_hours` is right-skewed and the median is robust to the long tail
   c. LinearRegression, because it is linear
   d. RandomForest, because trees handle outliers

4. **Short answer.** In the regression notebook, what two categories go through `OneHotEncoder` and what seven numeric columns go through `StandardScaler`? *(see notebook "feature table" cell)*

5. **Multiple choice.** Why is **accuracy banned** as the headline metric for the on-time classifier? *(see Concepts §4, classification intro)*
   a. Accuracy is never computed for binary tasks
   b. With ~20% late, "always on time" is ~80% accurate yet misses every late shipment
   c. Accuracy requires a GPU
   d. Accuracy is identical to F1 here

6. **Short answer.** The LogisticRegression at threshold 0.5 has recall ≈ 0.06. What does that recall value mean in operational terms, and how does lowering the threshold change it? *(see Concepts §6, worked example 3)*

7. **Multiple choice.** What is `predict_proba(test_df)[:, 1]` returning in the classification notebook? *(see notebook "threshold" cell)*
   a. The predicted class label (0 or 1)
   b. The probability of the *late* class, as a float per row
   c. The accuracy of the model
   d. The feature importances

8. **Short answer.** When you fit a `StandardScaler` for the Week 3 features, on which split must you call `.fit()`, and why? *(see Concepts §5)*

9. **Multiple choice.** Which row is a correct read of the confusion matrix's four cells? *(see notebook "confusion matrix" cell)*
   a. Rows are predictions, columns are actual
   b. Diagonal = correct (TN and TP), off-diagonal = errors (FP and FN)
   c. The matrix only counts on-time rows
   d. The matrix is symmetric by construction

10. **Short answer.** What three things must the Week 3 model card state, per the Friday Zorost gate? *(see "The use case")*

## Answer key

1. **b.** A random shuffle would let a future shipment train the model while a past one sits in test; splitting on `planned_departure` with cut dates keeps train strictly before val before test, so the future can't leak.

2. **`delay_hours` is the correction to the planned arrival**: `planned_arrival + predicted_delay` is the adjusted ETA. Predicting the delay directly targets the part the model can learn (lateness), rather than a timestamp dominated by the schedule.

3. **b.** `delay_hours` is right-skewed (median 0.73 h vs. mean 3.56 h, max 227.88 h), so the median baseline (MAE 3.795 h) resists the tail and beats the mean baseline (5.088 h) and all three models.

4. **`weather_severity` and `commodity`** go through `OneHotEncoder`; **`distance_km`, `weight_kg`, `value_usd`, `on_time_rate`, `fleet_size`, `month`, and `day_of_week`** go through `StandardScaler`. They are the `CAT_COLS` and `NUM_COLS` lists in `build_features`.

5. **b.** The target is imbalanced (~20% late), so a constant "on time" classifier is ~80% accurate while catching zero late shipments. The late class is the one that matters, so F1/precision/recall on it replace accuracy.

6. **Recall ≈ 0.06 means the model flags only ~6% of actually-late shipments**: it is missing almost every breach. Lowering the threshold (e.g. to 0.20) flags more rows as late, raising recall (to ~0.49) while lowering precision.

7. **b.** `predict_proba` returns a two-column array of class probabilities; `[:, 1]` takes the second column, the probability of the positive (`is_late`) class for each test row.

8. **`.fit()` on the training split only**, then `.transform()` validation and test. Fitting on all data would leak the val/test mean and variance into training and inflate the model's apparent performance.

9. **b.** With rows = actual and columns = predicted, the diagonal holds the correct calls (TN top-left, TP bottom-right) and the off-diagonal holds the errors (FP and FN). Moving the threshold shifts mass between those two off-diagonal cells.

10. **The headline metric** (MAE for ETA, F1 on the late class for on-time), **the exact split** that produced it (cut dates, not "80/20"), and **the single biggest error source** found by slicing errors (e.g. severe weather, a lane, a carrier).
