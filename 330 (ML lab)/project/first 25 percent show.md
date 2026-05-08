### **Part 6: Evaluation (The Reality Check)**

After the model has finished its training epochs, we need to know if it actually learned to generalize or if it just got lucky.

#### **1. Switching to `eval()` Mode**

The code calls `model.eval()`. This is crucial.

- Remember the **Data Augmentation** (flipping/rotating) we talked about? In evaluation mode, those are turned off.
    
- We also turn off things like **Dropout** (if used) to ensure the model's predictions are deterministic and stable.
    

#### **2. `torch.no_grad()`**

While evaluating, we wrap the code in `with torch.no_grad():`.

- Since we aren't training, we don't need to calculate gradients (the "mistake" math).
    
- This saves a massive amount of memory and makes the computation much faster.
    

#### **3. Accuracy Calculation**

The model outputs "logits" (raw scores). We use `torch.max` to pick the index of the highest score—this is the model's final prediction (e.g., "I'm 85% sure this is `c3`: texting"). We then compare this to the actual label.

---

### **Part 7: Introduction to Adversarial Attacks (FGSM)**

This is where the notebook gets interesting. Most of your academic projects likely stopped at accuracy, but this one introduces **Security**.

#### **1. What is an Adversarial Attack?**

It’s a way to "trick" the AI. By adding a tiny amount of specifically calculated noise to an image—noise so small a human wouldn't even notice—you can make a world-class AI think a driver is safely driving when they are actually texting.

#### **2. The FGSM Method**

The notebook uses the **Fast Gradient Sign Method (FGSM)**.

- Instead of using gradients to _minimize_ the loss (training), FGSM uses those same gradients to _maximize_ the loss.
    
- It calculates: "Which way can I change this pixel to make the model most confused?"
    

---
Part 7 uncovers a critical concept: **Adversarial Attacks**, specifically the **Fast Gradient Sign Method (FGSM)**.

While training focuses on making the model smarter, Part 7 focuses on how to "trick" it using its own math. Here is a deep dive into how this works in your notebook.

---

### 1. The Concept: "Inverting" the Training Process

In standard training, we use **Gradients** to find out how to _change the weights_ of the model to **minimize the loss** (make the model more accurate).

In an Adversarial Attack, we do the exact opposite:

1. We **freeze the weights** (the AI's brain doesn't change).
    
2. We calculate the gradients to find out how to _change the image pixels_ to **maximize the loss**.
    

Essentially, we are asking the math: _"What is the smallest possible change I can make to these pixels to make the AI most confident in the wrong answer?"_

### 2. Deep Dive into the `fgsm_attack` Function

Let's look at the logic inside your code cell 29:

- **`images.requires_grad = True`**: Usually, we only track gradients for weights. Here, we tell PyTorch to track the gradients of the **pixels**.
    
- **`loss.backward()`**: This calculates the "direction" of the error.
    
- **`grad_sign = images.grad.sign()`**: We don't care about the _amount_ of the error, only its _direction_ (positive or negative). If the gradient is positive, increasing that pixel's brightness will increase the loss.
    
- **The Math ($x_{adv} = x + \epsilon \cdot sign(\nabla_x J(\theta, x, y))$):**
    
    Python
    
    ```
    perturbation = epsilon * grad_sign / std
    adv_images = images + perturbation
    ```
    
    We take the original image and add a tiny amount of "noise" ($\epsilon$) in the direction that causes the most confusion.
    

### 3. Why is this dangerous?

The "noise" added is mathematically calculated to be devastating to a Neural Network but invisible to a human.

- **To a Human:** The image still looks like a driver texting.
    
- **To the AI:** The tiny pixel shifts are perfectly aligned to move the image across a "decision boundary" in the AI's internal high-dimensional space, causing it to misclassify the image with high confidence (e.g., thinking the driver is "Driving Safely").
    

### 4. Part 7 in the Context of Your Notebook

Your notebook runs a loop (cell 30) that tests the model against these "corrupted" images.

- It calculates **Robust Accuracy**: How well does the model perform when a "villain" is actively trying to trick it?
    
- As you saw in your output, even a tiny $\epsilon$ (like 0.001) can cause the accuracy to drop from **76% to nearly 0%**.
    

---

### **Part 8: Epsilon—The "Invisible" Threshold**

Part 8 explores the variable $\epsilon$ (Epsilon).

- **Small $\epsilon$:** The attack is subtle. The driver looks normal, but the AI is tricked. This is a **Security Risk** (e.g., a "cloaked" image that bypasses safety filters).
    
- **Large $\epsilon$:** The image starts to look "grainy" or "static-y" to the human eye. The AI is still tricked, but now a human would realize something is wrong with the photo.
    

---

**Summary of Part 7 & 8:** We've learned that AI models are "brittle." They are incredibly accurate on data they expect, but they can be completely blinded by mathematically precise noise that a human cannot even see.

**Next, in Part 9, we will look at "Unnormalization" — how we convert those mathematical tensors back into viewable pictures to see the "static" for ourselves.**

**As a CSE student at BUET, can you think of any real-world scenarios where an adversarial attack like this could be used maliciously? (e.g., self-driving cars, facial recognition?)**