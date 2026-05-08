# Maximum Likelihood Estimation (MLE)

In Linear Regression, we minimize Mean Squared Error. In [[Logistic_Regression_Core|Logistic Regression]], we maximize the **Likelihood**.

## The Probability Model

For a single sample $(x, y)$, we assume:

- $P(y=1|x; \theta) = h_{\theta}(x)$
    
- $P(y=0|x; \theta) = 1 - h_{\theta}(x)$
    

This can be written in a single "compact" form:

$$p(y|x; \theta) = (h_{\theta}(x))^y (1 - h_{\theta}(x))^{1-y}$$

_(If_ $y=1$_, the second term becomes 1; if_ $y=0$_, the first term becomes 1. Simple algebra, don't overthink it.)_

## The Likelihood Function $L(\theta)$

For $n$ independent samples, the likelihood is the product of all individual probabilities:

$$L(\theta) = \prod_{i=1}^{n} (h_{\theta}(x^{(i)}))^{y^{(i)}} (1 - h_{\theta}(x^{(i)}))^{1-y^{(i)}}$$

## The Log-Likelihood $l(\theta)$

Product functions are a nightmare for derivatives. We take the $log$ to turn products into sums:

$$l(\theta) = \sum_{i=1}^{n} y^{(i)} \log h(x^{(i)}) + (1 - y^{(i)}) \log(1 - h(x^{(i)}))$$

To find the best $\theta$, we perform [[Optimization_and_Gradient_Ascent|Gradient Ascent]] to maximize this function.