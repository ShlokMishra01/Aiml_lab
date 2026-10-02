# Week 04: Exercises & Checklist

## Graded exercises

1. **Easy**: Run `notebooks/01-pytorch-tensors-and-autograd.ipynb` to completion.
   Confirm the autograd gradient matches your hand-computed value and record the toy
   MLP's final training loss in the Week 4 tracker sheet.

2. **Standard**: In `notebooks/02-mlp-eta-train-and-eval.ipynb`, deliberately break
   exactly one thing (for example, set the learning rate 100× too high, or skip feature
   normalization) and run it. In a markdown cell, diagnose the failure from the learning
   curves (e.g. exploding loss, or training loss far below validation loss) and name the
   fix.

3. **Stretch**: Tune three hyperparameters: hidden width, dropout rate, and weight
   decay, using the **validation** split only, and record the best combination's
   validation MAE. Only then evaluate on the test set exactly once, and report that
   number alongside the baseline.

4. **Portfolio**: Complete the **ETA prediction (ML → DL) with model cards** milestone
   (see [`curriculum/projects/README.md`](../projects/README.md)): commit model card v2 with
   (a) the neural test MAE, (b) the Week 3 baseline MAE it is compared against, and (c)
   the error-analysis note naming the biggest error cluster by carrier/lane plus a
   hypothesis.

## Hints

1. **Easy**: Compare your hand-computed `2x` value against `x.grad.item()` right after
   `y.backward()`; the toy-MLP final loss is the number printed by the notebook's last
   cell, and "near zero" means the net learned the linear signal.
2. **Standard**: Change exactly one knob (e.g. `lr=0.1`, or skip the scaler) and re-run;
   then read the *shape* of the train/val curves, an exploding value or a diverging gap
   to name the failure before you fix it.
3. **Stretch**: Loop over a small grid of `(width, dropout, weight_decay)`, train each
   on the **training** split, and score on **validation** only; the best combo is the one
   with the lowest validation MAE, and only then do you run the test set once.
4. **Portfolio**: In the error-analysis note, pair the *number* (the worst carrier/lane's
   mean absolute error) with the *hypothesis* (e.g. extreme delays or seasonality
   dominate that slice), the gate is the number plus the "why," not the number alone.

## Checklist (mirrors manifest.json + Excel tracker)

- [ ] Mon: Study tensors, autograd, and the computation-graph mental model.
- [ ] Tue: Run the MLP notebook; verify loss curves; deliberately break one thing and diagnose it.
- [ ] Wed: Add dropout/weight decay; tune 3 hyperparameters using the validation split.
- [ ] Thu: Compare neural vs baseline on the test set; segment errors by carrier and lane.
- [ ] Fri: Use case: write the error-analysis note (biggest error cluster + hypothesis).
- [ ] Sat: Take the Week 4 quiz (quiz.md), pass with 8/10; record the score in Notes.
- [ ] Milestone: Update the Excel tracker; commit model card v2.
