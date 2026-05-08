Look, the internet is built on top of the **Internet Protocol (IP)**, which is "best-effort." That’s a polite way of saying it’s unreliable garbage. IP is perfectly happy to drop your packets in a ditch if a router gets slightly overwhelmed.

**TCP** is the babysitter that sits on top of IP to make sure your data actually arrives, and in the right order. To do that, it needs a way to say, _"I sent you something 200ms ago and you haven't acknowledged it. I'm assuming it's dead. I'll send it again."_

The problem is: **how long should TCP wait before giving up?**

### The Calculation Logic

If you wait 5 seconds for every packet on a high-speed fiber line, the internet would feel like a 1990s dial-up connection. If you wait only 10ms on a satellite link that takes 500ms, you’ll end up resending the same packet a thousand times while the original is still in flight.

We need a **Retransmission Timeout (RTO)** that adapts to the network's current mood.

### Step 1: The Raw Measurement (SampleRTT)

Every time TCP sends a packet and gets an ACK back, it notes the time. That’s your **SampleRTT**. It’s raw, twitchy, and unreliable.

### Step 2: Smoothing the Noise (EstimatedRTT)

Because one slow packet shouldn't break the system, we use an average. We take a piece of the old average (87.5%) and a tiny slice of the new sample (12.5%). This is the **EstimatedRTT**. It’s a "weighted" average that filters out temporary spikes.

### Step 3: Measuring the Chaos (DevRTT)

Now we track how much the samples are "jittering." If the network is stable, the samples stay near the average. If the network is chaotic, the samples fluctuate wildly. **DevRTT** measures this variation.

### Step 4: The Safety Margin (RTO)

Finally, we set the timer:

$$RTO = EstimatedRTT + 4 \cdot DevRTT$$

We take our average speed and add a massive safety buffer (4x the deviation). This ensures we only retransmit when we are _reasonably certain_ the packet is actually gone, not just stuck in traffic.

---

**Essentially:** We are trying to predict the future (how long the next ACK will take) using a smoothed-out version of the past, plus a buffer for safety.

Since you're a CSE student, would you like a quick Python snippet or C++ logic to see how these values update in a loop, or are we clear on the "why"?