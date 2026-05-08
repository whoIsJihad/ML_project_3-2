# Logistic Regression Simulation: Pass/Fail Prediction

## The Setup

We want to predict if a student passes ($y=1$) based on Hours Studied ($x_1$).

### The Key Difference from Linear Regression

In Linear Regression, you'd predict $y = 3.5$ hours or $y = 100$ marks. Here, your actual data ($y$) is just a bunch of 0s and 1s. Your prediction ($h_\theta(x)$) is a probability.

### Initial State

- **Bias (**$\theta_0$**):** -3
    
- **Hours Weight (**$\theta_1$**):** 1
    
- **The Threshold:** The model currently thinks that $z = -3 + 1(x_1) = 0$ is the 50/50 mark. Solving for $x_1$ gives 3 hours.
    

## Data Point: The "Confused" Case

- **Input (**$x_1$**):** 3 Hours
    
- **Actual Label (**$y$**):** Fail ($0$) — _The student studied 3 hours but failed anyway._
    
- **Linear Score (**$z$**):** $\theta^T x = -3(1) + 1(3) = 0$
    
- **Prediction (**$h_\theta(x)$**):** $\sigma(0) = 0.5$ (The model is perfectly unsure).
    

## Deep Dive: The Likelihood Function

Before we update, we need to understand **Maximum Likelihood Estimation (MLE)**. This is the "Score" of how good our current weights $\theta$ are.

### 1. Probability of a Single Sample

For any single student, the probability that the model is "right" is:

- If the student passed ($y=1$), the probability is $h_\theta(x)$.
    
- If the student failed ($y=0$), the probability is $1 - h_\theta(x)$.
    

We use a "math trick" to write this as one equation:

$$P(y|x; \theta) = (h_\theta(x))^y (1 - h_\theta(x))^{1-y}$$

**Why this works:**

- If $y=1$: $(h_\theta)^1 \cdot (1-h_\theta)^0 = h_\theta$
    
- If $y=0$: $(h_\theta)^0 \cdot (1-h_\theta)^1 = 1 - h_\theta$ _It's just an if-else statement dressed up in fancy math._
    

### 2. The Total Likelihood $L(\theta)$

We want to know the probability that the model is right for the **entire dataset**. Assuming students are independent, we multiply their individual probabilities:

$$L(\theta) = \prod_{i=1}^{n} P(y^{(i)}|x^{(i)}; \theta)$$

**The Goal:** We want to find $\theta$ that makes this total probability as close to $1.0$ as possible. That's why we use **Gradient Ascent**—we are climbing to the peak of "likelihood."

## The Learning Step (Stochastic Gradient Ascent)

We use the update rule: $\theta_j := \theta_j + \alpha(y - h_\theta(x))x_j$. Let's use a learning rate $\alpha = 0.1$.

1. **Calculate the Error:** $(y - h_\theta(x)) = (0 - 0.5) = -0.5$. _Notice: The error is negative because our prediction (0.5) was "higher" than the actual result (0)._
    
2. **Update** $\theta_1$ **(Hours Weight):**
    
    $$\theta_1 = 1 + 0.1(-0.5)(3) = 1 - 0.15 = 0.85$$
3. **Update** $\theta_0$ **(Bias/Intercept):**
    
    $$\theta_0 = -3 + 0.1(-0.5)(1) = -3.05$$

## Result of Update: What happened to the "Line"?

The new decision boundary is where $-3.05 + 0.85(x_1) = 0$. Solving for $x_1$: $x_1 = 3.05 / 0.85 \approx 3.58$ hours.

**The Logic:** Because the student failed at 3 hours, the model shifted its "passing threshold" higher (from 3 hours to 3.58 hours). It is now "stricter."

## Are we "Basically running Linear Regression"?

- **Mathematically:** Yes. The update rule $\theta := \theta + \alpha(\text{error})x$ is identical to the one derived for Linear Regression.
    
- **Conceptually:** No.
    
    - In Linear Regression, the "error" is the distance to a point.
        
    - In Logistic Regression, the "error" is the difference between a label ($0$ or $1$) and a probability.
        
    - The hypothesis $h_\theta(x)$ is passed through a non-linear [[Sigmoid_and_Hypothesis|Sigmoid Function]], which means the "line" we are fitting is actually a probability curve.
        

## Summary Table for your Vault

|Symbol|Meaning in this Simulation|Typical Value|
|---|---|---|
|$y^{(i)}$|Actual result of student $i$|$0$ (Fail) or $1$ (Pass)|
|$h_\theta(x^{(i)})$|Model's confidence score|$0.12$ (likely fail) to $0.95$ (likely pass)|
|$\theta^T x$|The "Linear Score"|Any real number ($-\infty$ to $+\infty$)|
|$\sigma(z)$|The "Squashing" function|Maps score to $[0, 1]$|