### Topic 2: Data Collection

#### The Core Concept

Before you can teach a machine to learn, you need to give it something to learn from. **Data Collection** is the process of gathering examples that show the relationship between inputs and outputs. Think of it like collecting flashcards to study from—if your flashcards are incomplete or wrong, you won't learn the right answers.

**Key Principle:** Your model will only be as good as the data you feed it.

---

#### Why Data Matters (The GIGO Principle)

**Garbage In, Garbage Out (GIGO)** is the golden rule of machine learning.

- **Bad Data → Bad Model:** If you train a face recognition model using only photos taken in bright daylight, it will fail completely in dim lighting.
- **Good Data → Good Model:** High-quality, diverse, representative data leads to models that work in the real world.

**Real Example:** Amazon tried building an AI hiring tool trained on past resumes. Since most past hires were male, the model learned to discriminate against women. The data was biased, so the model became biased.

---

#### Where Does Data Come From?

##### 1. **Existing Datasets (The Easy Start)**

These are pre-packaged datasets that others have already collected and cleaned.

**Best Sources:**
- **[Kaggle](https://www.kaggle.com/datasets):** Thousands of datasets for competitions (House prices, Titanic survival, image classification).
- **[UCI Machine Learning Repository](https://archive.ics.uci.edu/):** Classic academic datasets (Iris flowers, Wine quality).
- **[Google Dataset Search](https://datasetsearch.research.google.com/):** Search engine specifically for datasets.
- **Government Portals:** Census data, weather records, COVID statistics.

**When to Use:** Great for learning and practice projects when you're starting out.

##### 2. **APIs (Live Data Streams)**

APIs (Application Programming Interfaces) let you pull real-time data from websites and services.

**Examples:**
- **Twitter API:** Fetch tweets for sentiment analysis.
- **OpenWeather API:** Get current weather data for predictions.
- **Stock Market APIs (Alpha Vantage, Yahoo Finance):** Historical stock prices.
- **News APIs:** Headlines for text classification.

**When to Use:** When you need current, dynamic data that updates frequently.

##### 3. **Web Scraping (Custom Extraction)**

If no API exists, you can write code to automatically extract data from websites.

**Tools:** Beautiful Soup (Python), Scrapy, Selenium.

**Warning:** Always check if web scraping is legal for that website (look for `robots.txt`). Some sites prohibit it.

##### 4. **Sensors & IoT Devices (Physical World)**

Data from hardware devices in the real world.

**Examples:**
- **Temperature sensors** for climate prediction.
- **Accelerometers** in phones for activity recognition (walking vs running).
- **Cameras** for image/video data.
- **Microphones** for speech recognition.

**When to Use:** Building systems that interact with the physical world (robotics, smart homes, health monitors).

##### 5. **Manual Labeling (Human Effort)**

Sometimes you need humans to label data because machines can't do it yet.

**Examples:**
- Drawing boxes around objects in images ("This is a car").
- Tagging emails as spam or not spam.
- Transcribing audio into text.

**Tools:** Amazon Mechanical Turk, LabelBox, Scale AI.

**Fun Fact:** When you solve CAPTCHAs ("Select all squares with traffic lights"), you're actually labeling training data for AI systems!

---

#### Types of Data

##### **Structured Data (Organized Tables)**

Data that fits neatly into rows and columns, like a spreadsheet.

**Format:** CSV files, Excel sheets, SQL databases.

**Example:**

| Name  | Age | Salary | Purchased |
|-------|-----|--------|-----------|
| Alice | 25  | 50000  | Yes       |
| Bob   | 30  | 60000  | No        |

**Use Case:** Predicting customer purchases, loan approvals, house prices.

##### **Unstructured Data (No Fixed Format)**

Data that doesn't fit into tables.

**Types:**
- **Images:** Photos for object detection, medical scans.
- **Text:** Tweets, reviews, emails, articles.
- **Audio:** Music files, voice recordings.
- **Video:** Surveillance footage, YouTube clips.

**Challenge:** Requires preprocessing (converting images to pixel arrays, text to numerical embeddings).

---

#### The Bias Problem (A Critical Warning)

Your model learns patterns from your data. If your data is biased, your model will be biased too.

**Common Bias Types:**

1. **Sampling Bias:** Your data doesn't represent the full population.
   - *Example:* Training a medical diagnosis model only on data from young patients—it fails for elderly patients.

2. **Historical Bias:** Your data reflects past prejudices or inequalities.
   - *Example:* Training on past hiring decisions where certain groups were unfairly excluded.

3. **Measurement Bias:** Your data collection method is flawed.
   - *Example:* Using smartphone app data to study exercise habits (excludes people without smartphones).

**How to Avoid Bias:**
- Collect data from diverse sources and demographics.
- Check if your dataset represents all groups fairly.
- Test your model on different subgroups to catch problems.

---

#### Data Quality Checklist

Before using any dataset, ask:

✅ **Is it large enough?** (More examples = better learning)  
✅ **Is it diverse?** (Covers all scenarios you'll encounter)  
✅ **Is it clean?** (No missing values, duplicates, or errors)  
✅ **Is it labeled correctly?** (For supervised learning)  
✅ **Is it recent?** (Old data might not reflect current patterns)  
✅ **Is it representative?** (Matches the real-world distribution)

---

#### Quick Start for Beginners

**If you're learning ML for the first time:**

1. Start with **Kaggle datasets**—they're cleaned and ready to use.
2. Pick a simple problem (house prices, iris flower classification).
3. Don't worry about collecting your own data yet—focus on understanding the algorithms first.
4. As you advance, try building your own dataset using APIs or web scraping.

**Next Step:** Once you have data, you need to understand how to use it. Move to **[[Linear Regression as a Neural Network]]** to see how we actually feed data into a model.

