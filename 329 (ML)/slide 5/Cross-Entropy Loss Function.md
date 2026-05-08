> [[MOC (NN)]] | Prev: [[One-Hot Encoding]] | Next: [[Backpropagation and the Chain Rule]]

# Cross-Entropy Loss Function

The Loss Function $L(\hat{y}, y)$ quantifies the error for a single training example. In classification, we primarily use Negative Log-Likelihood, also known as Cross-Entropy.

## Binary Cross-Entropy

For a single example $(x, y)$ where $y \in \{0, 1\}$:

$$L(\hat{y}, y) = -(y \log(\hat{y}) + (1-y) \log(1-\hat{y}))$$

### Detailed Example: Binary Cross-Entropy Calculation

Let's illustrate binary cross-entropy with an example of classifying an email as "spam" or "not spam".

**Scenario:** We have a model predicting whether an email is spam ($y=1$) or not spam ($y=0$).

**Ground Truth:**
Suppose the email *is* spam.
- $y = 1$

**Model's Prediction:**
The model outputs a single probability $\hat{y}$ (the likelihood that the email is spam). Let's say:
- $\hat{y} = 0.8$ (The model predicts an 80% chance that it's spam).

**Calculating the Loss (Case 1: Actual = Spam, Predicted = 0.8 Spam):**
We use the binary cross-entropy formula:
$$L(\hat{y}, y) = -(y \log(\hat{y}) + (1-y) \log(1-\hat{y}))$$

Substitute $y=1$ and $\hat{y}=0.8$:
$$L = -(1 \cdot \log(0.8) + (1-1) \cdot \log(1-0.8))$$
$$L = -(\log(0.8) + 0 \cdot \log(0.2))$$
$$L = -\log(0.8)$$

Using a calculator for the natural logarithm:
$$L \approx -(-0.2231)$$
$$L \approx 0.2231$$

**Interpretation for Case 1:** The loss is relatively low (0.2231) because the model predicted a high probability (0.8) for the correct class (spam).

---

**Scenario 2:** Now, consider an email that *is not* spam.

**Ground Truth:**
- $y = 0$

**Model's Prediction:**
The model still outputs a probability $\hat{y}$ for being spam. Let's say, in this case, the model wrongly predicts a high chance of spam:
- $\hat{y} = 0.7$ (The model predicts a 70% chance that it's spam, but it's not).

**Calculating the Loss (Case 2: Actual = Not Spam, Predicted = 0.7 Spam):**
Substitute $y=0$ and $\hat{y}=0.7$:
$$L = -(0 \cdot \log(0.7) + (1-0) \cdot \log(1-0.7))$$
$$L = -(0 \cdot \log(0.7) + 1 \cdot \log(0.3))$$
$$L = -\log(0.3)$$

Using a calculator for the natural logarithm:
$$L \approx -(-1.2040)$$
$$L \approx 1.2040$$

**Interpretation for Case 2:** The loss is significantly higher (1.2040) compared to Case 1 because the model was confident (0.7) but incorrect (the email was not spam). A higher loss value penalizes the model more for being confidently wrong.

## Multi-class Cross-Entropy

For $K$ classes with one-hot encoded targets $y$:

$$L(\hat{y}, y) = -\sum_{j=1}^K y_j \log(\hat{y}_j)$$

## Empirical Risk (Cost Function)

The total cost $J(W, b)$ over a dataset of $N$ samples is the average loss:

$$J(W, b) = \frac{1}{N} \sum_{i=1}^N L(\hat{y}^{(i)}, y^{(i)})$$

## Derivative of Loss

To perform [[Backpropagation and the Chain Rule]], we need the derivative of the loss with respect to the pre-activation output $z$ of the final layer. For Softmax with Cross-Entropy:

$$\frac{\partial L}{\partial z_i} = \hat{y}_i - y_i$$

This elegant result simplifies the computation of gradients significantly.

## Detailed Example: Multi-Class Cross-Entropy Calculation

Let's walk through a tangible example to see how the multi-class cross-entropy loss is calculated in practice.

**Scenario:** Suppose we have a trained image classification model that is trying to classify an image into one of three possible classes: **Cat**, **Dog**, or **Bird**.

**Ground Truth:**
The image we are testing is a **Dog**. We represent this ground truth using one-hot encoding:
- $y = [y_1, y_2, y_3]$
- where the classes are (Cat, Dog, Bird)
- So, $y = [0, 1, 0]$

**Model's Prediction:**
After passing the image through the neural network, the final layer (with a Softmax activation function) outputs a probability distribution across the three classes. Let's say the model's predicted probabilities ($\hat{y}$) are:
- $\hat{y} = [\hat{y}_1, \hat{y}_2, \hat{y}_3]$
- $\hat{y} = [0.3, 0.6, 0.1]$

This means the model is 30% confident it's a Cat, 60% confident it's a Dog, and 10% confident it's a Bird.

**Calculating the Loss:**
We use the multi-class cross-entropy formula:
$$L(\hat{y}, y) = -\sum_{j=1}^K y_j \log(\hat{y}_j)$$

Let's break down the calculation term by term:

$$L = - (y_1 \log(\hat{y}_1) + y_2 \log(\hat{y}_2) + y_3 \log(\hat{y}_3))$$

Now, substitute the values for $y$ and $\hat{y}$:

$$L = - (0 \cdot \log(0.3) + 1 \cdot \log(0.6) + 0 \cdot \log(0.1))$$

The terms for the incorrect classes (Cat and Bird) get multiplied by 0, so they disappear. This is a key feature of cross-entropy with one-hot encoding.

$$L = - (0 + \log(0.6) + 0)$$
$$L = - \log(0.6)$$

Using a calculator for the natural logarithm:
$$L \approx -(-0.5108)$$
$$L \approx 0.5108$$

**Interpretation:**
The cross-entropy loss for this single prediction is approximately **0.5108**.

- A lower loss value indicates a better prediction (i.e., the predicted probability for the correct class is closer to 1).
- If the model were perfectly confident and correct ($\hat{y} = [0, 1, 0]$), the loss would be $-\log(1) = 0$.
- If the model were very confident but incorrect (e.g., predicted `[0.9, 0.1, 0]`), the loss would be $-\log(0.1) \approx 2.30$, which is much higher.

This example demonstrates how cross-entropy loss provides a meaningful measure of how "surprised" the model is by the true answer. The higher the surprise, the higher the loss.

## Derivation of the Loss Derivative for Softmax

The result $\frac{\partial L}{\partial z_i} = \hat{y}_i - y_i$ is a cornerstone of training classification networks. It elegantly combines the derivatives of the Cross-Entropy Loss and the Softmax function. Here is a step-by-step derivation.

### 1. Components

**Multi-Class Cross-Entropy Loss (L):**
$$L = -\sum_{j=1}^K y_j \log(\hat{y}_j)$$
where $y_j$ is the ground truth (0 or 1) for class $j$, and $\hat{y}_j$ is the predicted probability for class $j$.

**Softmax Activation ($\hat{y}_j$):**
The predicted probability $\hat{y}_j$ is the output of the softmax function applied to the pre-activation (logit) values $z_k$:
$$\hat{y}_j = \frac{e^{z_j}}{\sum_{k=1}^K e^{z_k}}$$

Our goal is to find the gradient of the loss with respect to a single logit, $z_i$.

### 2. The Chain Rule

We use the chain rule to find how a change in $z_i$ affects the loss $L$. The loss $L$ is a function of all predicted probabilities $\hat{y}_j$, and each $\hat{y}_j$ is a function of all logits $z_k$. Therefore, we must sum the influences of $z_i$ on every $\hat{y}_j$:

$$\frac{\partial L}{\partial z_i} = \sum_{j=1}^K \frac{\partial L}{\partial \hat{y}_j} \frac{\partial \hat{y}_j}{\partial z_i}$$

### 3. Calculating the Partial Derivatives

#### a) Derivative of Loss with respect to $\hat{y}_j$

First, let's find the derivative of the loss function with respect to a single output probability $\hat{y}_j$.
$$\frac{\partial L}{\partial \hat{y}_j} = \frac{\partial}{\partial \hat{y}_j} \left( -\sum_{k=1}^K y_k \log(\hat{y}_k) \right)$$
Since the derivatives of $\log(\hat{y}_k)$ are zero for $k \neq j$, we only consider the term where $k=j$:
$$\frac{\partial L}{\partial \hat{y}_j} = -\frac{\partial}{\partial \hat{y}_j} (y_j \log(\hat{y}_j)) = -\frac{y_j}{\hat{y}_j}$$

#### b) Derivative of Softmax with respect to $z_i$

This is the most complex part. The derivative of the softmax function depends on whether we are differentiating with respect to the same logit ($i=j$) or a different one ($i \neq j$).

**Case 1: $i = j$** (e.g., $\frac{\partial \hat{y}_i}{\partial z_i}$)
Using the quotient rule on $\hat{y}_i = \frac{e^{z_i}}{\sum_k e^{z_k}}$:
$$ \frac{\partial \hat{y}_i}{\partial z_i} = \frac{ (e^{z_i})' (\sum_k e^{z_k}) - e^{z_i} (\sum_k e^{z_k})' }{ (\sum_k e^{z_k})^2 } $$
$$ = \frac{ e^{z_i} (\sum_k e^{z_k}) - e^{z_i} (e^{z_i}) }{ (\sum_k e^{z_k})^2 } $$
$$ = \frac{e^{z_i}}{\sum_k e^{z_k}} \cdot \frac{\sum_k e^{z_k} - e^{z_i}}{\sum_k e^{z_k}} $$
$$ = \hat{y}_i (1 - \hat{y}_i) $$

**Case 2: $i \neq j$** (e.g., $\frac{\partial \hat{y}_j}{\partial z_i}$)
Again, using the quotient rule, but now the derivative of the numerator $e^{z_j}$ with respect to $z_i$ is 0.
$$ \frac{\partial \hat{y}_j}{\partial z_i} = \frac{ (e^{z_j})' (\sum_k e^{z_k}) - e^{z_j} (\sum_k e^{z_k})' }{ (\sum_k e^{z_k})^2 } $$
$$ = \frac{ 0 - e^{z_j} (e^{z_i}) }{ (\sum_k e^{z_k})^2 } $$
$$ = - \frac{e^{z_j}}{\sum_k e^{z_k}} \cdot \frac{e^{z_i}}{\sum_k e^{z_k}} $$
$$ = -\hat{y}_j \hat{y}_i $$

### 4. Combining the Parts

Now we substitute these results back into the chain rule sum. It's helpful to split the sum into two parts: the term where $j=i$ and all the terms where $j \neq i$.

$$ \frac{\partial L}{\partial z_i} = \underbrace{ \left( \frac{\partial L}{\partial \hat{y}_i} \frac{\partial \hat{y}_i}{\partial z_i} \right) }_{j=i \text{ term}} + \underbrace{ \sum_{j \neq i} \left( \frac{\partial L}{\partial \hat{y}_j} \frac{\partial \hat{y}_j}{\partial z_i} \right) }_{j \neq i \text{ terms}} $$

Substitute the derivatives we found:

$$ \frac{\partial L}{\partial z_i} = \left( -\frac{y_i}{\hat{y}_i} \right) (\hat{y}_i(1-\hat{y}_i)) + \sum_{j \neq i} \left( -\frac{y_j}{\hat{y}_j} \right) (-\hat{y}_j \hat{y}_i) $$

Simplify the terms:

$$ \frac{\partial L}{\partial z_i} = -y_i(1-\hat{y}_i) + \sum_{j \neq i} y_j \hat{y}_i $$
$$ \frac{\partial L}{\partial z_i} = -y_i + y_i \hat{y}_i + \hat{y}_i \sum_{j \neq i} y_j $$

We can factor out $\hat{y}_i$:

$$ \frac{\partial L}{\partial z_i} = -y_i + \hat{y}_i \left( y_i + \sum_{j \neq i} y_j \right) $$

Since the $y$ vector is one-hot encoded, it contains a single 1 (at the true class index) and the rest are 0s. The sum of all elements of $y$ is therefore 1.
$$ \sum_{j=1}^K y_j = y_i + \sum_{j \neq i} y_j = 1 $$
So, the term in the parenthesis is simply 1.

$$ \frac{\partial L}{\partial z_i} = -y_i + \hat{y}_i(1) $$
$$ \frac{\partial L}{\partial z_i} = \hat{y}_i - y_i $$

This gives us the remarkably simple and efficient gradient used for backpropagation in multi-class classification networks.
