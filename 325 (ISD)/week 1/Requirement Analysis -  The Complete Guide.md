
# Requirement Analysis: The Complete Guide

## 1. The Big Picture: SDLC

**Systems Development Life Cycle (SDLC)** is the standard process for planning, creating, and deploying information systems. Requirement Analysis is the critical **Phase 3**.

1. **Identify:** Find problems/opportunities.
    
2. **Determine:** What info do humans need?
    
3. **Analyze (We are here):** Define exactly what the system needs to do.
    
4. **Design:** Blueprint the system.
    
5. **Develop:** Code it.
    
6. **Test:** Verify it works.
    
7. **Implement:** Deploy to users.
    

## 2. What is a "Requirement"?

A requirement is simply a statement of **what a system must do** or **characteristics it must have**.

### Why do we need them? (The Roles)

Different team members use requirements for different things:

- **Customers:** It's a contract ("This is what I paid for").
    
- **Project Managers:** It's a progress bar ("We finished 3 of 10 requirements").
    
- **Designers:** It's the blueprint specs.
    
- **Programmers:** It's the coding target (Input -> Logic -> Output).
    
- **QA/Testers:** It's the answer key ("Did the system do X? If yes, Pass. If no, Fail.").
    

## 3. Stakeholders (Who cares?)

A stakeholder is anyone affected by your system. You must identify all of them, or your system will fail.

### The 3 Types of Viewpoints

1. **Interactor Viewpoints (Direct Users):**
    
    - People who actually touch the system.
        
    - _Example (ATM):_ The bank customer, the maintenance guy refilling cash.
        
2. **Indirect Viewpoints (Influencers):**
    
    - People who don't use it but care about the output or management.
        
    - _Example (ATM):_ Bank Manager (needs reports), Security Team (worried about theft).
        
3. **Domain Viewpoints (Rules):**
    
    - Not people, but constraints of the industry/environment.
        
    - _Example (ATM):_ Federal banking laws, inter-bank communication standards.
        

## 4. Types of Requirements (Crucial Exam Topic)

### A. User vs. System Requirements

- **User Requirement (The WHAT):** Written in plain English. Describes user goals.
    
    - _Ex:_ "I want to upload a profile picture."
        
- **System Requirement (The HOW):** Technical detail. Describes implementation.
    
    - _Ex:_ "The system shall accept PNG/JPG files <2MB and store them in the Blob storage."
        

### B. Functional vs. Non-Functional

This is the most important distinction in this course.

#### 1. Functional Requirements (FR)

**Behaviors.** What the system _does_. If you delete this code, a feature disappears.

- _Library System:_ Search for books, check out a book, calculate fine.
    
- _Food App:_ Show restaurant list, place order, track driver.
    

#### 2. Non-Functional Requirements (NFR)

**Attributes.** _How_ the system performs. If you ignore these, the system "works" but sucks (too slow, insecure, ugly).

- **Performance:** Speed and throughput. (_Ex: Load homepage in <2 seconds._)
    
- **Usability:** Ease of use. (_Ex: New users can sign up in <1 minute without help._)
    
- **Security:** Protection. (_Ex: Passwords must be hashed; Data encrypted AES-256._)
    
- **Availability:** Uptime. (_Ex: System is online 99.9% of the time._)
    
- **Scalability:** Growth. (_Ex: Can handle 10,000 users at once during finals week._)
    
- **Reliability:** Robustness. (_Ex: If the server crashes, data is not lost._)
    

## 5. How to Gather Requirements (Day 3 Content)

You can't just guess what users want. You must research.

### Method 1: Observation

Watching users to see reality vs. what they _say_ they do.

- **Participant Observation:** You join the team and do the work with them.
    
    - _Pros:_ Deep understanding. _Cons:_ You might lose objectivity (bias).
        
- **Non-Participant Observation:** You watch from the corner (fly on the wall).
    
    - _Pros:_ Objective. _Cons:_ **Hawthorne Effect** (People act differently/work harder when they know they are being watched).
        

### Method 2: Interviews

Talking to users.

- **Unstructured:** "Tell me about your job." (Good for exploration).
    
- **Structured:** Strict list of questions. (Good for comparing answers).
    
- **Semi-Structured:** **(Best Choice)** A guide of themes, but you can ask "Why?" and dig deeper.
    
    - _Tip:_ Avoid "Yes/No" questions. Ask "How do you...?" or "Tell me about a time..."
        

### Method 3: Focus Groups

Get 6-9 people in a room to discuss.

- _Good for:_ Brainstorming, understanding shared problems.
    
- _Bad for:_ Sensitive topics (people won't share private info in a group), Groupthink (everyone agrees with the loud guy).
    

### Method 4: Contextual Inquiry (CI)

The "Master/Apprentice" model. You watch them work _in their environment_ (Context) and ask questions as they go (Inquiry).

- **4 Principles:**
    
    1. **Context:** Go to where the work happens.
        
    2. **Partnership:** They are the master; you are the learner.
        
    3. **Interpretation:** Validate what you see immediately ("You just clicked X, was that because of Y?").
        
    4. **Focus:** Keep your research goals in mind.
        

### Method 5: Surveys

Questionnaires sent to many people.

- _Good for:_ Getting lots of data (Quantitative).
    
- _Bad for:_ "Why" questions (Qualitative).
    
- _Tip:_ Don't use double negatives ("Do you not like not having..."). Keep it simple.

#### Listen to this : [[Designing Great Software Requirement Analysis and Core Components.mp3]]