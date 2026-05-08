# Perceptron vs. Logistic Regression: The Duel of Decisions

While you were busy trying to understand if $1 \times 1$ matrices are scalars, you might have missed that the Perceptron is basically [[Logistic_Regression_Core|Logistic Regression]]'s more aggressive, less nuanced cousin.

## 1. The Core Philosophical Difference

- **Logistic Regression**: A cautious optimist. It gives you a probability (e.g., "I'm 72% sure this student passed"). It uses the [[Sigmoid_and_Hypothesis|Sigmoid Function]] to keep things smooth and differentiable.
    
- **Perceptron**: A stubborn binary thinker. It doesn't care about confidence. It’s either a 1 or a 0. It uses a **Step Function** as its activation.
    

## 2. The Activation Function Trap

In the Perceptron, the hypothesis is defined as $h_{\theta}(x) = g(\theta^T x)$, where:

$$g(z) = \begin{cases} 1 & \text{if } z \ge 0 \\ 0 & \text{if } z < 0 \end{cases}$$

There is no "gray area" or curve. It's a hard cliff.

## 3. The Bizarre Mathematical Coincidence

Despite their different origins—Logistic Regression comes from [[Likelihood_and_MLE|Maximum Likelihood Estimation]], while the Perceptron is a purely heuristic algorithm—they share the **exact same update rule**:

$$\theta_j := \theta_j + \alpha(y^{(i)} - h_{\theta}(x^{(i)})) x_j^{(i)}$$

### How they behave differently during training:

- **In Logistic Regression**: $h_{\theta}(x)$ is a fraction (like 0.6). Even if the model gets the classification right (predicts 0.6 for a $y=1$ label), the error is $1 - 0.6 = 0.4$. The model **keeps learning** and refining the weights to get closer to 1.
    
- **In the Perceptron**: $h_{\theta}(x)$ is either 0 or 1.
    
    - If the prediction is right, the error is exactly $0$. The model **stops learning** for that point immediately.
        
    - If it's wrong, the error is $1$ or $-1$, causing a massive jump in weights.
        

## 4. Summary Table

|Feature|Logistic Regression|Perceptron|
|---|---|---|
|**Output Type**|Continuous probability ( (0, 1) )|Discrete class ( {0,1} )|
|**Activation**|Sigmoid (soft)|Step function (hard)|
|**Loss Basis**|Log-likelihood (cross-entropy)|Mistake-driven heuristic|
|**Nuance**|High (captures confidence)|Zero (only cares about the decision boundary)|