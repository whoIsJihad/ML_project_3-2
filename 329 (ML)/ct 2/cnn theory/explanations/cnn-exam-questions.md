# CNN Exam Practice Questions

## Question 1: LeNet vs AlexNet
What are the 3 main differences between LeNet (1998) and AlexNet (2012)? Why did the field wait 14 years before proving deep networks work at scale?

---

## Question 2: ReLU Advantage
Explain why ReLU is better than sigmoid for deep networks. Give a numerical gradient example showing why sigmoid causes vanishing gradients.

---

## Question 3: VGG Design Choice
VGG uses stacked 3×3 filters instead of one 5×5 filter. Compare:
- Two 3×3 filters stacked
- One 5×5 filter
In terms of receptive field, parameters, non-linearity, and computation.

---

## Question 4: Filter Size Progression
AlexNet uses mixed filter sizes (11×11, 5×5, 3×3). Why does AlexNet use 11×11 in the first layer instead of 3×3? What information does a large first filter capture?

---

## Question 5: Inception Module
Draw or describe a complete Inception module. What are the 4 branches, and why use 1×1 convolutions before the 3×3 and 5×5 branches?

---

## Question 6: 1×1 Convolution Speedup
GoogLeNet saves 8.8× computation using bottleneck architecture:
- 56×56×256 → 3×3 conv direct: 1.85B operations
- 56×56×256 → 1×1 (256→64) → 3×3 → 1×1 (64→256): 0.22B operations

Show the calculation for each step and explain why this 8.8× speedup doesn't significantly hurt accuracy.

---

## Question 7: Auxiliary Classifiers
GoogLeNet has 3 classification outputs (2 auxiliary + 1 main). Answer:
- Where are they placed in the network?
- Why are there exactly 3 (not 2 or 4)?
- What happens to auxiliary classifiers during testing?
- How do they help during training?

---

## Question 8: Vanishing Gradients
A 50-layer network without residual connections fails to train. Show numerically why gradients vanish:
- Gradient at layer 50: dL/dw₅₀ = 0.1
- Gradient at layer 40: dL/dw₄₀ ≈ ?
- Gradient at layer 1: dL/dw₁ ≈ ?

Assume each layer multiplies gradient by 0.9.

---

## Question 9: ResNet Skip Connections
Explain why skip connections solve the vanishing gradient problem. Draw the gradient flow diagram showing:
- Path 1: Through F(x) layers
- Path 2: Direct skip connection
How does total gradient = (Path 1 gradient) + (Path 2 gradient)?

---

## Question 10: ResNet Residual Learning
A residual block computes y = F(x, W) + x instead of y = H(x, W).
- What is F(x)?
- Why is learning F(x) easier than learning H(x)?
- Give a numerical example where identity mapping is optimal (no change needed).

---

## Question 11: Parameter Efficiency Comparison
Compare parameters across architectures:
- AlexNet: 60M params, 63.3% accuracy
- VGG-16: 138M params, 71.3% accuracy
- GoogLeNet: 6.9M params, 74.8% accuracy
- ResNet-50: 25.5M params, 76.0% accuracy

Which is most parameter-efficient? Why?

---

## Question 12: BatchNorm in ResNet
ResNet uses BatchNorm extensively. How does BatchNorm help ResNet training? Explain the connection between:
- Higher learning rates enabled
- Gradient stability
- Ability to train deep networks

---

## Question 13: Dropout and Regularization
AlexNet uses dropout with p=0.5. Explain:
- What happens during training vs testing
- Why p=0.5 is typical for fully-connected layers
- How dropout acts like ensemble learning

---

## Question 14: Architecture Evolution
Arrange these networks in chronological order and explain how each solved problems from the previous:
- ResNet
- LeNet
- AlexNet
- GoogLeNet
- VGG

---

## Question 15: Design Choice Reasoning
For each architecture, identify ONE key design choice and explain why it was important:
1. LeNet: Average pooling
2. AlexNet: ReLU + GPU
3. VGG: All 3×3 filters
4. GoogLeNet: Inception modules
5. ResNet: Skip connections

---

## Question 16: Modern Architecture Selection
You're building a computer vision system. Choose between:
- AlexNet (simple, proven)
- VGG-16 (accurate, slow)
- ResNet-50 (accurate, moderate)
- GoogLeNet (efficient, accurate)

Justify your choice for:
a) Maximum accuracy with unlimited compute
b) Deployment on edge device (limited memory)
c) Fast training for research
d) Transfer learning backbone

---

## Question 17: Gradient Flow Analysis
Without ResNet skip connections, explain why adding more layers beyond 50 actually makes accuracy WORSE. With ResNet skip connections, why does adding more layers (up to 152) keep improving accuracy?

---

## Question 18: Inception vs Sequential
GoogLeNet uses parallel branches (Inception) while VGG uses sequential layers.
- What information does parallel processing capture that sequential misses?
- Why didn't VGG use parallel branches too?
- When is sequential better than parallel?

---

## Question 19: Bottleneck Analysis
In GoogLeNet's bottleneck (256→64 before 3×3):
- What information is lost during dimension reduction (256→64)?
- Why doesn't this hurt accuracy?
- What's the trade-off between speedup and accuracy?

---

## Question 20: Training Dynamics
Compare training of:
- VGG-16: Can train successfully with 10 layers, but gets worse beyond 20
- ResNet-50: Gets better as you add layers all the way to 152

Explain the fundamental difference in training dynamics caused by skip connections.

