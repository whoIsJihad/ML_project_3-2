
## 0. What is an Optimiser, "Really"?

Before we talk about Momentum, we must define what we are actually doing.

An **Optimiser** is an algorithm that answers one question at every step:
> "Given my current location and the local slope, **how far** and in **what direction** should I move?"

In plain Gradient Descent, the answer is always:
> "Move a fixed fraction of the current slope."

This is a **Stateless Controller**. It ignores everything that happened before.

---

## 1. The Real Problem: Local vs. Global

The "real" challenge of optimization in ML is that the **local gradient is a liar**.

1.  **It is short-sighted:** It only knows the slope at point $x$. It doesn't know if a cliff is $0.001$ units away.
2.  **It is noisy:** Especially in Stochastic GD, the gradient at one point might point the wrong way due to a single bad data point.
3.  **It lacks scale:** A gradient of $10.0$ in a wide flat valley means something different than $10.0$ in a narrow sharp crack.

**A "Real" Optimiser** is a strategy to **filter** and **scale** these local lies into a reliable path toward the minimum.

---

## 2. The Shift: From Slope to Strategy

When we move from plain GD to things like Momentum, RMSProp, or Adam, we are changing the nature of the optimizer:

- **Plain GD:** Only uses **Current Slope**.
- **Momentum:** Uses **History** (Gradients over time).
- **RMSProp/AdaGrad:** Uses **Scale** (Magnitude of gradients).
- **Adam:** Uses **Both**.

---

## 3. The "Memoryless" Problem (Momentum's Motivation)

Now we see why Momentum is the first "real" step up.

In plain GD, your update rule is:
$$ \theta_{t+1} = \theta_t - \eta \nabla \mathcal{L}(\theta_t) $$

Because it is **Markovian** (no memory), it falls for every "local lie" the gradient tells. If the gradient zig-zags, the optimizer zig-zags.

---

## 4. The Physics Intuition (Adding State)

Instead of a "weightless point," we give the optimizer **Mass**.

- **In GD:** No mass. You stop the moment the push (gradient) stops.
- **In Momentum:** You have **Velocity** ($v$). Velocity is the "State" or "Memory" of the optimizer.

---

## 5. Introducing Velocity ($v$)

We don't just update the position; we update the **velocity** first, then move the position.

**The Math:**

1.  **Update Velocity (The Memory):**
    $$ v_{t+1} = \gamma v_t + \eta \nabla \mathcal{L}(\theta_t) $$

2.  **Update Position (The Move):**
    $$ \theta_{t+1} = \theta_t - v_{t+1} $$

**What is $\gamma$ (Gamma)?**
It’s the "Memory Retention" (usually $0.9$). It defines how much you trust the **past** vs. the **present**.

---

## 6. Why this fixes the "Zig-Zag"

Consider a narrow valley.
- The **Sides** (Vertical) have gradients that flip-flop: $+10, -10, +10$. In the velocity sum, these cancel out to $\approx 0$.
- The **Floor** (Horizontal) has a tiny but consistent gradient: $0.1, 0.1, 0.1$. In the velocity sum, these build up!

**The Result:**
> Momentum **dampens** what is inconsistent and **accelerates** what is consistent.

---

## 7. Nesterov Accelerated Gradient (NAG): "Looking Ahead"

If standard momentum is "Blind Memory," Nesterov is "Intelligent Memory."

Instead of calculating the gradient where you are, you calculate it where you **expect to be** after your momentum carries you:

$$ v_{t+1} = \gamma v_t + \eta \nabla \mathcal{L}(\theta_t - \gamma v_t) $$
$$ \theta_{t+1} = \theta_t - v_{t+1} $$

It’s like a driver tapping the brakes *before* the curve because they see it coming.

---

## Pause Checkpoint

Answer this carefully:

> We said an optimizer is a "strategy to filter and scale." 
> 
> How does Momentum specifically "filter" the gradient signal in a zig-zagging valley? Describe the interaction between $\gamma v_t$ and $\nabla \mathcal{L}(\theta_t)$.
