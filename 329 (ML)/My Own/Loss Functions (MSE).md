### Topic: Loss Functions (The Scorecard)

#### The Core Concept

A neural network, at the start, is just a random line. It has no idea if it is doing a good job or a terrible job. To fix this, we need a mathematical "scorecard" that tells the model exactly how wrong it is. This scorecard is called the Loss Function (or Cost Function).

In Linear Regression, the standard standard loss function is **Mean Squared Error (MSE)**.

#### The Geometry of Error (Residuals)

Imagine your data points scattered on a graph ($y$) and your regression line passing through them ($\hat{y}$).

- For any specific data point, the model predicts a value on the line.
    
- The actual data point might be slightly above or below that line.
    
- The vertical distance between the actual point and the line is called the **Residual** or **Error**.
    

##### The Formula: Mean Squared Error (MSE)

To get a single score for the entire dataset, we combine all these individual errors into one number.

$$J(w, b) = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2$$

**Breakdown of the Math**

1. **Difference $(y - \hat{y})$:** Calculate the error for a single point. If the house costs $200k and the model predicted $150k, the error is $50k.
    
2. **Squaring $(\dots)^2$:** We square this difference.
    
    - **Reason 1 (Positivity):** If the prediction is too high (+50) or too low (-50), the error is still "bad." Squaring makes all errors positive ($2500$) so they don't cancel each other out.
        
    - **Reason 2 (Punishment):** Squaring penalizes outliers heavily. An error of 10 becomes 100. An error of 2 becomes 4. The model is forced to pay more attention to the massive mistakes than the tiny ones.
        
3. **Sum $\sum$:** Add up the squared errors for every single data point in your dataset.
    
4. **Mean $\frac{1}{N}$:** Divide by the number of data points to get the average. This ensures your error score doesn't just get bigger simply because you have more data.
    

##### The Goal

The value of the Loss Function $J(w,b)$ represents the "Cost."

- High Cost = Bad Model (Line fits poorly).
    
- Low Cost = Good Model (Line fits well).
    

**Optimization Objective:** We want to find the specific values of $w$ and $b$ that result in the **lowest possible MSE**.

**Next Step:** We have the architecture and the scorecard. Now, how do we actually improve the score? Move to **[[Gradient Descent]]**?