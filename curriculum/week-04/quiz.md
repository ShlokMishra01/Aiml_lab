# Week 04: Quiz (10 questions, 8/10 to pass)

Answer all ten, then check against the answer key. *(see Concepts §X)* points at a README subsection; *(see notebook cell Y)* points at a cell in `01-pytorch-tensors-and-autograd.ipynb` or `02-mlp-eta-train-and-eval.ipynb`.

1. **Multiple choice.** In the autograd cell, `y = x ** 2` with `x = torch.tensor(3.0, requires_grad=True)` and `y.backward()`. What is `x.grad`, and why? *(see Concepts §2, autograd cell)*
   a. 3.0, because it copies `x`
   b. 6.0, because `df/dx = 2x` and `2 × 3 = 6`
   c. 9.0, because `3² = 9`
   d. 0.0, because `x` is a leaf

2. **Short answer.** Write the five lines of the training loop in order, and say what each line is for. *(see Concepts §4)*

3. **Multiple choice.** Why must you call `model.eval()` (and `torch.no_grad()`) before evaluating on validation/test? *(see Concepts §7, "How it breaks")*
   a. To move the model to the GPU
   b. To turn **off dropout** and skip gradient tracking, so test predictions are deterministic and cheap
   c. To reset the optimizer's state
   d. To re-seed the DataLoader

4. **Short answer.** What is the difference between the **loss** the model optimizes and the **metric** the model card reports, in this week's ETA task? *(see Concepts §4)*

5. **Multiple choice.** The ETA MLP has 23 input features. Where do those 23 come from? *(see notebook "feature table" cell, Concepts §5)*
   a. 23 raw shipment columns
   b. 7 numeric + 4 one-hot weather + 12 one-hot commodity = 23
   c. 20 carriers + 3 dates
   d. 23 random embeddings

6. **Short answer.** On this dataset the neural MLP's test MAE is ≈ 4.99 h and the gradient-boosting baseline's is ≈ 4.87 h. What is the delta, and why is reporting it (rather than hiding it) the point of the week? *(see Concepts §7, worked example 3)*

7. **Multiple choice.** Which symptom in the learning curves indicates **overfitting**? *(see Concepts §5)*
   a. Both train and val high and flat
   b. Train low, val high, and the gap widening with epochs
   c. Both curves decreasing together to the same value
   d. Val lower than train

8. **Short answer.** In `DataLoader(train_ds, batch_size=256, shuffle=True)`, why is `shuffle=True` correct for training but wrong for validation/test? *(see notebook "DataLoader" cell, Concepts §5)*

9. **Multiple choice.** What does the `weight_decay` argument on `AdamW` do? *(see Concepts §6)*
   a. Randomly zeroes a fraction of activations during training
   b. Adds a squared-weight penalty to the loss, nudging weights toward zero
   c. Decays the learning rate each epoch
   d. Shrinks the batch size over time

10. **Short answer.** Name the two regularizers used in `EtaMLP`, and state the symptom each one is meant to reduce. *(see Concepts §6, model cell)*

## Answer key

1. **b.** For `f(x) = x²` the derivative is `2x`; at `x = 3` that is `6.0`. Autograd walks the computation graph in reverse and fills `x.grad` with the chain-rule gradient, which the notebook asserts equals 6.0.

2. **`opt.zero_grad()` (clear last step's gradients) → `loss = loss_fn(model(xb), yb)` (forward + measure error) → `loss.backward()` (autograd fills `.grad`) → `opt.step()` (optimizer updates weights)**, looped over `for xb, yb in loader`. Forward, loss, backward, step is the whole engine.

3. **b.** `model.eval()` disables training-only behavior (dropout), and `torch.no_grad()` disables gradient bookkeeping, so predictions use the full network deterministically and don't waste memory. Forgetting it leaves dropout on and corrupts the test metric.

4. **The loss is MSE**: smooth and differentiable, which the optimizer minimizes. **The reported metric is MAE in hours**, interpretable to an operator ("off by X hours") even though it isn't what's differentiated. They differ by design: optimize what's smooth, report what matters.

5. **b.** The `ColumnTransformer` standardizes 7 numeric columns and one-hot encodes `weather_severity` (4 categories) and `commodity` (12 categories), yielding 7 + 4 + 12 = 23 features.

6. **Delta ≈ +0.116 h**: the MLP is about 7 minutes *worse* on average, a virtual tie. Reporting the loss honestly is the discipline: a model is judged against its baseline with the delta stated, not by its own training loss, and the point of Week 4 is the evals + error-analysis habit, not a cherry-picked win.

7. **b.** Overfitting shows as train loss low while validation loss is high and the gap widens, the model is memorizing the training sample. Both-high-and-flat is underfitting; converging together is healthy.

8. **Shuffling training batches** decorrelates successive gradient steps and helps generalization, but validation/test order must be preserved so per-epoch loss is comparable and (in time-series data) the chronological order is not broken. Only the training loader gets `shuffle=True`.

9. **b.** `weight_decay` adds a penalty proportional to squared weights to the loss, pulling weights toward zero for a smoother, less noise-fitting function. It is decoupled from Adam's adaptive step in `AdamW`.

10. **Dropout** (randomly zeroing activations during training only) and **weight decay** (the squared-weight penalty). Both reduce **overfitting**, the symptom of training loss far below validation loss with a widening gap.
