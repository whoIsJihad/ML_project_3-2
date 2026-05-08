### Topic: Computation Graphs

#### The Core Concept

A **Computation Graph** is a visual way to represent mathematical calculations as a flowchart. It breaks down complex nested functions into a series of simple, atomic operations (add, multiply, apply function, etc.).

**Why This Matters:** When you write `loss = ((y - model(x))**2).mean()`, the computer doesn't just magically know how to compute gradients. It needs to trace through every single operation to apply the chain rule. Computation graphs make this systematic and automatic.

**Real-World Impact:** This is how TensorFlow, PyTorch, and JAX work under the hood. When you call `.backward()` in PyTorch, it traverses the computation graph you built during the forward pass.

---

#### Why Do We Need Computation Graphs?

Neural networks are **deeply nested functions**. Consider a simple 2-layer network:

$$\hat{y} = \sigma(W_2 \cdot \text{ReLU}(W_1 \cdot x + b_1) + b_2)$$

Computing the derivative $\frac{\partial \text{Loss}}{\partial W_1}$ manually would require:
- Derivative of Loss with respect to $\hat{y}$
- Derivative of Sigmoid
- Derivative of matrix multiplication
- Derivative of ReLU
- Another matrix multiplication derivative

**Without computation graphs:** You'd have to write out the entire derivative by hand, prone to errors.

**With computation graphs:** The computer automatically applies the chain rule step-by-step by traversing the graph backward.

---

#### A Simple Example: Breaking Down the Math

Let's start with a simple equation and build its computation graph:

$$J = 3(a + b \cdot c)$$

**Goal:** Compute $J$ and find how sensitive $J$ is to changes in $a$, $b$, and $c$.

##### **Step 1: Break Into Intermediate Steps**

Instead of computing this all at once, we introduce intermediate variables:

1. $u = b \cdot c$ (multiply $b$ and $c$)
2. $v = a + u$ (add $a$ and $u$)
3. $J = 3 \cdot v$ (multiply by 3)

##### **Step 2: The Computation Graph Structure**

**Nodes:** Variables or operations
**Edges:** Flow of data

The graph flows like this:

**Inputs:** $a$, $b$, $c$  
↓  
**Operation 1:** $u = b \times c$  
↓  
**Operation 2:** $v = a + u$  
↓  
**Operation 3:** $J = 3 \times v$  
↓  
**Output:** $J$

---

#### Forward Pass: Computing the Value

Let's plug in actual numbers: $a = 5$, $b = 3$, $c = 2$

**Step-by-step calculation:**

1. $u = b \cdot c = 3 \times 2 = 6$
2. $v = a + u = 5 + 6 = 11$
3. $J = 3 \cdot v = 3 \times 11 = 33$

**Forward Pass Summary:**
- Start with inputs: $a=5$, $b=3$, $c=2$
- Flow forward through operations
- End with output: $J=33$

**This is exactly what happens when you run a neural network** — data flows forward through layers to produce a prediction.

---

#### Backward Pass: Computing Gradients

Now we want to know: *"If I change $a$ slightly, how much does $J$ change?"*

This is $\frac{\partial J}{\partial a}$ (the gradient of $J$ with respect to $a$).

**The Chain Rule in Action:**

$$\frac{\partial J}{\partial a} = \frac{\partial J}{\partial v} \times \frac{\partial v}{\partial a}$$

##### **Step 1: Gradient at the Output**

Start at the end: $J = 3v$

$$\frac{\partial J}{\partial v} = 3$$

**Meaning:** If $v$ increases by 1, $J$ increases by 3.

##### **Step 2: Gradient at the Second Operation**

Now move back to: $v = a + u$

$$\frac{\partial v}{\partial a} = 1$$

**Meaning:** If $a$ increases by 1, $v$ increases by 1 (addition has gradient 1).

##### **Step 3: Combine Using Chain Rule**

$$\frac{\partial J}{\partial a} = \frac{\partial J}{\partial v} \times \frac{\partial v}{\partial a} = 3 \times 1 = 3$$

**Interpretation:** If we increase $a$ by 1, $J$ increases by 3.

---

#### Computing All Gradients

Let's find gradients for all inputs:

**For $\frac{\partial J}{\partial b}$:**

$$\frac{\partial J}{\partial b} = \frac{\partial J}{\partial v} \times \frac{\partial v}{\partial u} \times \frac{\partial u}{\partial b}$$

- $\frac{\partial J}{\partial v} = 3$
- $\frac{\partial v}{\partial u} = 1$ (from $v = a + u$)
- $\frac{\partial u}{\partial b} = c = 2$ (from $u = b \cdot c$)

$$\frac{\partial J}{\partial b} = 3 \times 1 \times 2 = 6$$

**For $\frac{\partial J}{\partial c}$:**

$$\frac{\partial J}{\partial c} = \frac{\partial J}{\partial v} \times \frac{\partial v}{\partial u} \times \frac{\partial u}{\partial c}$$

- $\frac{\partial u}{\partial c} = b = 3$ (from $u = b \cdot c$)

$$\frac{\partial J}{\partial c} = 3 \times 1 \times 3 = 9$$

---

#### Visual Flow Summary

**Forward Pass (Values):**

$a=5$, $b=3$, $c=2$  
→ $u = 6$  
→ $v = 11$  
→ $J = 33$

**Backward Pass (Gradients):**

$\frac{\partial J}{\partial J} = 1$ (start here)  
← $\frac{\partial J}{\partial v} = 3$  
← $\frac{\partial J}{\partial u} = 3$  
← $\frac{\partial J}{\partial a} = 3$, $\frac{\partial J}{\partial b} = 6$, $\frac{\partial J}{\partial c} = 9$

**Key Insight:** The backward pass multiplies gradients along the path from output to input. This is **automatic differentiation**.

---

#### How This Connects to Neural Networks

In a neural network:

**Forward Pass:**
- Input data flows through layers
- Each layer performs operations (matrix multiply, add bias, apply activation)
- Produces a prediction
- Computes loss

**Backward Pass:**
- Start at the loss
- Flow backward through each operation
- Compute gradient at each weight using chain rule
- Update weights using these gradients

**Example Operations in a Network:**
- **Matrix Multiplication:** $z = W \cdot x$
  - Forward: Compute $z$
  - Backward: Compute $\frac{\partial \text{Loss}}{\partial W}$ and $\frac{\partial \text{Loss}}{\partial x}$
  
- **ReLU Activation:** $a = \max(0, z)$
  - Forward: Apply ReLU
  - Backward: Gradient is 1 if $z > 0$, else 0

- **Loss Function:** $L = (y - \hat{y})^2$
  - Forward: Compute loss value
  - Backward: $\frac{\partial L}{\partial \hat{y}} = -2(y - \hat{y})$

---

#### Why "Graphs"? The DAG Structure

A computation graph is a **Directed Acyclic Graph (DAG)**:

- **Directed:** Information flows in one direction (inputs → outputs)
- **Acyclic:** No loops — you can't have a variable depend on itself
- **Graph:** Nodes (operations/variables) connected by edges (data flow)

**Real PyTorch Example:**

When you write:
```python
x = torch.tensor([1.0, 2.0], requires_grad=True)
y = x * 2
z = y.sum()
z.backward()
```

PyTorch builds a graph:
- Node 1: $x$ (input)
- Node 2: $y = x \times 2$ (multiply operation)
- Node 3: $z = \sum(y)$ (sum operation)

When you call `.backward()`, PyTorch traverses this graph backward and computes $\frac{\partial z}{\partial x}$.

---

#### Common Operations and Their Gradients

| Operation | Forward | Backward Gradient |
|-----------|---------|-------------------|
| Addition: $z = x + y$ | Compute sum | $\frac{\partial L}{\partial x} = \frac{\partial L}{\partial z} \times 1$ |
| Multiplication: $z = x \times y$ | Compute product | $\frac{\partial L}{\partial x} = \frac{\partial L}{\partial z} \times y$ |
| Power: $z = x^2$ | Square the value | $\frac{\partial L}{\partial x} = \frac{\partial L}{\partial z} \times 2x$ |
| ReLU: $z = \max(0, x)$ | Apply max | $\frac{\partial L}{\partial x} = \frac{\partial L}{\partial z} \times (x > 0)$ |
| Sigmoid: $z = \sigma(x)$ | Apply sigmoid | $\frac{\partial L}{\partial x} = \frac{\partial L}{\partial z} \times \sigma(x)(1-\sigma(x))$ |

Each operation knows two things:
1. How to compute its output (forward)
2. How to compute its gradient (backward)

---

#### The Big Picture: Automatic Differentiation

**Manual Differentiation (Old Way):**
- Derive formulas by hand
- Error-prone for complex functions
- Doesn't scale to large networks

**Symbolic Differentiation:**
- Computer derives formulas symbolically
- Can produce very long expressions
- Memory intensive

**Automatic Differentiation (Modern Way):**
- Break computation into elementary operations
- Each operation has a simple derivative rule
- Chain rule applied automatically during backward pass
- This is what deep learning frameworks use

**Why It's Revolutionary:**
You can write any differentiable function in code, and the framework automatically computes gradients. You don't need to derive anything by hand!

---

#### Quick Mental Model

**Computation Graph = Recipe with Intermediate Steps**

**Forward Pass:**
"Follow the recipe: Mix ingredients, bake, frost → Final cake"

**Backward Pass:**
"If the cake is too sweet, which ingredient caused it? Work backward through each step to find the culprit."

---

**Next Step:** Now that you understand how computations are organized, you're ready for **[[Backward Propagation]]** — where we use computation graphs to systematically compute gradients for every weight in a neural network.