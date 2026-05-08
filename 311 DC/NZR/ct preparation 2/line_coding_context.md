
## 1. Prerequisites

You don't need much, but refresh these to avoid getting stuck:

* 
**Digital Logic Basics:** Understanding high vs. low voltage levels (, , and ).


* 
**Basic Signals:** What frequency and bandwidth mean (intuitively).


* 
**Clock Synchronization:** Why two systems need to agree on when a "bit" starts and ends.



---

## 2. Topic List (The "What")

I've grouped these by the logical flow of the slides:

### **A. Core Fundamentals**

* 
**Line Coding vs. Decoding:** Converting digital data (bits) to digital signals (voltage pulses).


* 
**Data Elements vs. Signal Elements:** Distinguishing the "carried" bit from the "carrier" pulse.


* 
**The  Factor:** The ratio of data elements to signal elements (Crucial for calculations).


* 
**Data Rate (Bit Rate) vs. Signal Rate (Baud Rate):** Relationship between  and .



### **B. Evaluation Metrics (The "Criteria")**

* 
**Baseline Wandering:** Why long strings of 0s or 1s make the receiver "lose track" of the average voltage.


* 
**DC Components:** Why low-frequency signals are bad for certain channels.


* 
**Self-Synchronization:** Signals that include timing info so the receiver's clock stays in sync.



### **C. Line Coding Schemes (The "How")**

* 
**Unipolar (NRZ):** Basic, but has DC and sync issues.


* **Polar (NRZ-L, NRZ-I, RZ):** Using  and ; NRZ-I handles 1s better; RZ returns to zero mid-bit.


* 
**Biphase (Manchester & Differential Manchester):** The gold standard for self-sync (used in Ethernet).


* **Bipolar (AMI & Pseudoternary):** Three voltage levels; AMI alternates 1s.


* 
**Multilevel (2B1Q, 8B6T, 4D-PAM5):** Coding groups of bits to increase efficiency ().


* 
**Multitransition (MLT-3):** Complex transition rules for specific bandwidth needs.



### **D. Advanced Robustness**

* 
**Block Coding ():** Adding extra bits (redundancy) for better sync and error detection (e.g., 4B/5B, 8B/10B).


* 
**Scrambling (B8ZS, HDB3):** "Fixing" AMI by replacing long strings of 0s with special "violation" patterns without increasing bandwidth.



---

## 3. How to Study This (The "Strategy")

Since you get stuck in "tutorial watching without retention," try this:

1. **Don't Watch, Draw:** Take a bit sequence like `10110001`. For every scheme (Manchester, AMI, etc.), try to draw the signal yourself on paper. Compare your drawing to the slides. If it matches, you've "built" it.


2. **Focus on the "Trade-offs":** For the exam and real-world understanding, focus on *why* one is better than the other. Make a table: Does it have DC? Does it self-sync? What is the bandwidth?.


3. **The Scrambling Logic:** For B8ZS and HDB3, don't just look at the patterns. Memorize the *rule* (e.g., "if even, use B00V") and apply it to a new bitstream. This is high-probability exam material for BUET.



