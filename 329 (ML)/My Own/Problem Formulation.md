### Topic 1: Problem Formulation

#### The Core Concept

**Problem Formulation** is the art of translating a messy, real-world problem into a mathematical function that a machine can learn. You need to decide: *What are my inputs? What should the output be? And how do I measure success?*

Mathematically, we're looking for a function:

$$f(X) \approx Y$$

Where $X$ is your input data, $Y$ is what you want to predict, and $f$ is the function the machine will learn.

---

#### The Paradigm Shift: How ML is Different

**Traditional Programming:**
```
Rules + Data → Answers
```
You write explicit instructions (if-else statements, formulas) to transform data into answers.

**Example:** Calculating tax on a purchase.
- Rule: `tax = price × 0.15`
- You explicitly tell the computer the formula.

**Machine Learning:**
```
Data + Answers → Rules
```
You give the machine examples of inputs and their correct outputs. The machine figures out the rules on its own.

**Example:** Email spam detection.
- Instead of writing rules like "if email contains 'FREE MONEY' → spam", you show the machine 10,000 emails labeled spam/not spam.
- The machine discovers patterns you might never think of (e.g., sender's domain, time sent, unusual character combinations).

**Why This Matters:** For complex problems (recognizing faces, translating languages, driving cars), the rules are too complicated to write manually. ML discovers them automatically from data.

---

#### The Three Core Questions (The Pillars)

Every ML problem must answer these:

##### 1. **What Are My Inputs ($X$)?** — The Features

These are the measurements or characteristics you have access to.

**Real Examples:**

| Problem | Features (Inputs) |
|---------|-------------------|
| **Predicting House Prices** | Square footage, number of bedrooms, location zip code, age of house, nearby schools |
| **Diagnosing Pneumonia from X-rays** | Pixel values of the chest X-ray image (millions of numbers) |
| **Recommending Movies (Netflix)** | User's past ratings, time of day, device type, genres watched |
| **Predicting Customer Churn** | Account age, support tickets filed, usage frequency, last login date |

**Key Point:** Choosing good features is critical. If you're predicting house prices but forget to include location, your model will be terrible.

##### 2. **What Am I Predicting ($Y$)?** — The Target

This is what you want the model to output.

**Real Examples:**

| Problem | Target (Output) |
|---------|-----------------|
| **House Prices** | Dollar amount ($450,000) |
| **Pneumonia Detection** | Binary: Pneumonia present (Yes/No) |
| **Movie Recommendation** | Rating the user would give (1-5 stars) |
| **Self-Driving Car** | Steering angle (-30° to +30°) |

##### 3. **How Do I Measure Success?** — The Objective

You need a numerical way to tell if your model is doing well or poorly.

**Example:** For house price prediction, you might measure the average dollar difference between your predictions and actual prices. If you're off by $10,000 on average, that's better than being off by $100,000.

Mathematically: Minimize the error between $\hat{y}$ (prediction) and $y$ (actual).

---

#### The Two Main Problem Types

##### **Regression: Predicting Numbers**

The output is a continuous value (can be any number on a scale).

**Real-World Examples:**

1. **Stock Price Prediction**
   - Input: Historical prices, trading volume, news sentiment
   - Output: Tomorrow's closing price ($342.15)

2. **Weather Forecasting**
   - Input: Temperature, humidity, pressure, wind speed
   - Output: Temperature 24 hours from now (72.3°F)

3. **Ad Click Revenue**
   - Input: User demographics, ad placement, time of day
   - Output: Expected revenue from showing this ad ($0.43)

4. **Estimating Delivery Time**
   - Input: Distance, traffic, weather, restaurant prep time
   - Output: Delivery time (37 minutes)

**Key Trait:** The output exists on a spectrum. There's no "gap" between values—$100,000 and $100,001 are both valid house prices.

##### **Classification: Predicting Categories**

The output is a discrete label from a fixed set of options.

**Real-World Examples:**

1. **Medical Diagnosis (Binary)**
   - Input: Patient symptoms, blood test results, age, medical history
   - Output: Disease present? (Yes/No)

2. **Spam Detection (Binary)**
   - Input: Email text, sender address, subject line, attachments
   - Output: Spam or Not Spam

3. **Image Recognition (Multi-class)**
   - Input: Pixels of a photo
   - Output: One category (Cat / Dog / Bird / Car / ...)

4. **Sentiment Analysis (Multi-class)**
   - Input: Movie review text
   - Output: Positive / Neutral / Negative

5. **Handwritten Digit Recognition (Multi-class)**
   - Input: Image of handwritten number
   - Output: Which digit? (0, 1, 2, ..., 9)

**Key Trait:** The output is one of a fixed set of options. You can't output "halfway between cat and dog"—it's one or the other.

---

#### How to Formulate Your Own Problem (Step-by-Step)

Let's say you want to build an ML system. Here's how to think through it:

**Example Problem:** *"I want to predict if a student will pass or fail a course."*

**Step 1: Define the Input ($X$)**
- What data do you have access to?
- Attendance rate, homework scores, midterm grade, hours studied per week, previous GPA.

**Step 2: Define the Output ($Y$)**
- What exactly are you predicting?
- Binary classification: Pass (1) or Fail (0).

**Step 3: Choose the Problem Type**
- Is the output continuous or discrete?
- Discrete → This is a **Classification** problem.

**Step 4: Decide Success Metric**
- How will you measure if the model is good?
- Accuracy: What percentage of predictions are correct?

---

#### Common Mistakes Beginners Make

❌ **Choosing features the model can't access in real life**
- *Example:* Predicting if someone will default on a loan, but using "future credit score" as a feature. You won't have that information when making the prediction!

❌ **Target leakage** (using future information as input)
- *Example:* Predicting if a patient will survive surgery, but including "days in ICU after surgery" as a feature. That happens *after* the event you're predicting!

❌ **Unclear target definition**
- *Example:* "Predict if a customer is satisfied." What does satisfied mean? 4+ stars? Would recommend? Be specific.

❌ **Wrong problem type**
- *Example:* Treating age groups (child/teen/adult/senior) as regression. This should be classification because the categories are distinct.

---

#### Quick Reference: Is It Regression or Classification?

Ask yourself: **"Can the output take any value on a continuous scale, or is it picking from distinct categories?"**

**Continuous scale → Regression**
- Temperature, price, distance, time, weight, probability

**Distinct categories → Classification**
- Yes/No, spam/ham, cat/dog, cancer type, credit rating

**Edge Case:** Sometimes you can frame the same problem both ways.
- *Example:* "Will it rain tomorrow?"
  - **Classification:** Yes or No
  - **Regression:** Probability of rain (0% to 100%)

---

**Next Step:** Once you've formulated your problem, you need data to train on. Move to **[[Data Collection]]** to learn how to gather the examples your model will learn from.

