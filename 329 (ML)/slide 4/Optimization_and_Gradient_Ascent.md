# Optimization: Gradient Ascent

Since we want to **maximize** the [[Likelihood_and_MLE|Log-Likelihood]], we use **Gradient Ascent** instead of Gradient Descent.

## The Update Rule

The math works out (after using the sigmoid derivative) to a rule that looks suspiciously like Linear Regression:

### 1. Stochastic Gradient Ascent

Update $\theta$ for each individual sample:

$$\theta_j := \theta_j + \alpha(y^{(i)} - h_{\theta}(x^{(i)})) x_j^{(i)}$$

### 2. Batch Gradient Ascent

Update $\theta$ after looking at the whole dataset:

$$\theta_j := \theta_j + \alpha \sum_{i=1}^{m} (y^{(i)} - h_{\theta}(x^{(i)})) x_j^{(i)}$$

## Symbols Breakdown

- $\alpha$: Learning Rate (Hyper-parameter).
    
- $(y^{(i)} - h_{\theta}(x^{(i)}))$: The Error (Actual - Predicted).
    
- $x_j^{(i)}$: The feature value that scales the update.
    

**Note**: Even though the formula looks the same as Linear Regression, $h_{\theta}(x)$ here is a non-linear [[Sigmoid_and_Hypothesis|Sigmoid Function]], not a straight line.