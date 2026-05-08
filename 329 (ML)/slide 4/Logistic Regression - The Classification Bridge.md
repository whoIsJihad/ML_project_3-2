## What problem does it solve?

Linear regression predicts a continuous number (e.g. house price). Logistic regression predicts **which class** something belongs to — specifically, it outputs the **probability** of belonging to class 1.

Example: given a student's hours studied, predict probability they pass (1) or fail (0).

---

## Input / Output

**Input:** a feature vector — just a row of numbers.

```
x = [hours_studied, sleep_hours, prev_score]
    = [5.0,          7.0,         72.0]
```

**Output:** a single number between 0 and 1 — a probability.

```
ŷ = 0.83   →  83% chance of passing
```

You then threshold it: if ŷ ≥ 0.5 → predict class 1, else class 0.

---

## How does it compute that probability?

Two steps:

**Step 1 — linear combination** (same as linear regression):

```
z = w₁x₁ + w₂x₂ + w₃x₃ + b
```

This gives some raw number, could be anything: -10, 0, 4.7, etc.

**Step 2 — squash it into [0, 1]** using the sigmoid function:

```
ŷ = σ(z) = 1 / (1 + e^(-z))
```

Sigmoid maps any real number to (0, 1). That's your probability.

- z = 0 → ŷ = 0.5
- z = 5 → ŷ ≈ 0.99
- z = -5 → ŷ ≈ 0.01

---

## How do we train it?

Training = finding the weights **w** and bias **b** that make good predictions.

**Step 1 — pick a loss function.** We use **binary cross-entropy** (not MSE, because MSE behaves badly here):

```
Loss = -[y·log(ŷ) + (1-y)·log(1-ŷ)]
```

Intuition: if the true label is 1 and you predicted 0.99 → tiny loss. If you predicted 0.01 → huge loss.

**Step 2 — gradient descent.** Compute how much each weight contributed to the loss, then nudge each weight in the direction that reduces it:

```
w = w - lr · (∂Loss/∂w)
```

Repeat over all training examples, many times (epochs).

---

## Concrete mini-example

|Hours studied|Pass?|
|---|---|
|1|0|
|2|0|
|5|1|
|8|1|

Model starts with random weights. Computes ŷ for each row. Computes loss. Adjusts weights to make ŷ closer to y. After enough iterations, the weight on "hours studied" becomes large and positive — because more hours → higher z → higher probability of passing.

---

One thing to make sure you've got before moving on: **why can't we just use linear regression for classification?** Do you know?