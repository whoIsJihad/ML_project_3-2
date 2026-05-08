### Topic: Linear Regression as a Neural Network

#### The Core Concept

Linear regression is often taught as a statistical method, but in Deep Learning, it is best understood as the "Hello World" of Neural Networks. It represents a single-layer neural network with a single output neuron and no activation function. It teaches you how inputs are weighted to produce an output.

The Architecture

Imagine a structure with two distinct parts:

1. **Input Layer ($x$):** These are your features. If you are predicting house prices, $x_1$ might be square footage, and $x_2$ might be the number of bedrooms.
    
2. **The Output Node ($\hat{y}$):** This is the prediction engine.
    

Connecting these parts are **Weights ($w$)**. Each input has a dedicated weight line connecting it to the output. The weight determines the importance of that input. A high weight on square footage means size matters a lot for the price.

##### The Mathematical Operation

The computation happens inside the output neuron. It performs a "weighted sum."

$$z = \sum (x_i \cdot w_i) + b$$

$$\hat{y} = z$$

- **Dot Product:** You multiply every input by its corresponding weight and add them up.
    
- **The Bias ($b$):** This is an extra parameter that doesn't depend on any input. It allows the model to shift the activation line up or down. Without a bias, if all inputs were zero, your prediction would strictly have to be zero. The bias fixes this restriction.
    

#### The Learning Objective

The network starts "stupid." The weights ($w$) and bias ($b$) are initialized randomly. The goal of training is to adjust these numbers so that the prediction ($\hat{y}$) matches the real target ($y$) as closely as possible.

**Next Step:** Move to **[[Loss Functions (MSE)]]** to explain how we measure "closeness"?