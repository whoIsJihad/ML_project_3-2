# Learning Algorithms and Optimizers in PyTorch

This is the root reference for all optimization-related concepts in deep learning. Each algorithm and supporting concept has its own note, with explicit dependencies and cross-references.

## Core Concepts (Prerequisites)

Before studying any optimizer, ensure you understand:

- [[Gradient_Descent_Fundamentals]]
- [[Learning_Rate_and_Step_Size]]
- [[Convergence_Criteria]]

## First-Order Optimization Methods

These algorithms use only first-order gradient information (∇f).

### Fundamental Algorithm

- [[Stochastic_Gradient_Descent_SGD]]

### SGD Variants and Extensions

- [[SGD_Variants]] — Overview and comparison of momentum-based extensions
  - [[SGD_with_Momentum]]
  - [[Nesterov_Momentum]]

### Adaptive Methods

Optimizers that maintain parameter-specific learning rates:

- [[Adagrad]]
- [[RMSprop]]
- [[Adam]]
- [[AdamW]]
- [[AMSGrad]]

## Second-Order Methods

These algorithms incorporate second-order information (Hessian):

- [[Newton's Method in Deep Learning]]
- [[L-BFGS and Quasi-Newton Methods]]

## Learning Rate Schedules

Dynamic adjustment of learning rate during training:

- [[Constant Learning Rate]]
- [[Step Decay]]
- [[Exponential Decay]]
- [[Cosine Annealing]]
- [[Warm Restarts]]

## Implementation and Practical Considerations

- [[Optimizer State and Buffers in PyTorch]]
- [[Gradient Accumulation and zero_grad()]]
- [[Weight Decay vs L2 Regularization]]
- [[Optimizer Hyperparameter Selection]]
- [[Convergence Diagnostics]]

## Theoretical Foundations

- [[Convex vs Non-Convex Optimization]]
- [[Local and Global Minima]]
- [[Saddle Points and Escape Dynamics]]
- [[Gradient Flow and Backpropagation]]
- [[Loss Landscape Geometry]]

## Comparative Analysis

- [[SGD vs Adam: When to Use Which]]
- [[Optimization Dynamics Comparison]]
- [[Generalization and Optimizer Choice]]

---

Start with the prerequisites, then proceed to specific algorithms based on your needs.
