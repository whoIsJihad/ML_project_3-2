
## 0. The Problem: AdaGrad's "Infinite Memory"

As we discovered in AdaGrad, tracking the sum of squared gradients ($G_t$) leads to a fatal flaw: the effective learning rate eventually shrinks to zero. 

**The Limitation:**
AdaGrad treats gradients from the very first iteration with the same weight as gradients from the current iteration. In non-convex optimization (like Deep Learning), the "terrain" changes as you move. A massive gradient you saw 10,000 steps ago shouldn't necessarily force you to take tiny steps *now* if you are in a completely different part of the landscape.

---

## 1. The Intuition: The "Leaky Bucket" (Moving Average)

**RMSProp (Root Mean Square Propagation)** fixes AdaGrad by changing how we accumulate the squared gradients. 

Instead of an infinite sum, we use an **Exponentially Weighted Moving Average (EWMA)**.
> "I care about the scale of the gradients, but I mostly care about the **recent** scale. I will slowly forget the distant past."

This prevents the denominator from growing indefinitely, allowing the optimizer to stay "alive" and adaptive forever.

---

## 2. The Formalism: The Moving Average of Squares

We track $E[g^2]_t$, which is the "expected" squared gradient at time $t$.

**The Math:**

1.  **The Leaky Accumulator:**
    $$ v_t = \beta v_{t-1} + (1 - \beta) (\nabla \mathcal{L}(\theta_t))^2 $$
    *Here, $v_t$ (often called $S_t$ or $E[g^2]_t$) is the moving average.*

2.  **The Update Rule:**
    $$ \theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{v_t + \epsilon}} \cdot \nabla \mathcal{L}(\theta_t) $$

**What is $\beta$ (The Decay Rate)?**
-   Usually set to **0.9**.
-   It determines the effective memory window. A value of 0.9 means roughly $\approx \frac{1}{1-0.9} = 10$ steps have significant weight; older steps decay exponentially and contribute negligibly.
-   If $\beta = 1$, you get $v_t = v_{t-1}$ (accumulator freezes; no current gradient contributes). Mathematically similar to AdaGrad's "infinite memory," but $v_t$ never updates.
-   If $\beta = 0$, you get $v_t = g_t^2$ (only current gradient; no memory).

---

## 3. Why this works: Constant Adaptivity

Because $v_t$ is an average, it doesn't just grow—it can also **shrink**.

-   **Entering a Steep Gorge:** Gradients become large $\rightarrow$ $v_t$ increases $\rightarrow$ step size decreases (protection against explosion).
-   **Entering a Flat Plateau:** Gradients become tiny $\rightarrow$ $v_t$ decreases $\rightarrow$ step size **increases** (acceleration to escape the plateau).

**The Result:**
> RMSProp is like a car that automatically shifts gears based on the current incline, but doesn't get stuck in "low gear" just because it climbed a mountain three hours ago.

---

## 4. Practical Application: The RNN Connection

RMSProp was popularized by Geoff Hinton in his Coursera class. It was particularly famous for being the go-to optimizer for **Recurrent Neural Networks (RNNs)** for years. 

**Why?**
RNNs often suffer from "Exploding Gradients" due to their deep temporal structure. RMSProp’s ability to quickly dampen the learning rate when gradients spike (and then recover when they settle) made it much more stable than standard SGD or Momentum for sequences.

---

## 5. Comparison: AdaGrad vs. RMSProp

| Feature | AdaGrad | RMSProp |
| :--- | :--- | :--- |
| **Accumulation Strategy** | Simple Sum ($g^2_1 + g^2_2 + \dots$) | Moving Average ($\beta v_{t-1} + (1-\beta)g^2_t$) |
| **Memory** | Infinite (Eternal) | Recent (Leaky) |
| **Learning Rate Fate** | Guaranteed to vanish to zero. | Stays adaptive and responsive. |
| **Best For...** | Sparse data (where features are rare). | Deep Networks, RNNs, and Non-convex surfaces. |

---

## Pause Checkpoint

Answer this:

> Suppose you are at a **Saddle Point**. The gradient is zero in most directions, but there is one direction that slopes downwards very gently.
> 
> How would RMSProp help you escape this saddle point faster than plain Gradient Descent? Think about what happens to the denominator ($\sqrt{v_t}$) in that "gentle" direction over time.
