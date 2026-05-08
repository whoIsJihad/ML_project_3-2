Study Guide: Amplitude Modulation (CSE 311)

Part 1: Page-by-Page Headline Map

Pages 1-3: Introduction & Recap

Importance of Fourier Transform properties.

Course Outline: DSB-SC, SSB, QAM, VSB, FDM, and PLL.

Pages 4-8: The Case for Modulation

Baseband Communication: Sending $m(t)$ directly.

The Problems: Interference (multiplexing issues) and Antenna Size (the $c/f$ relationship).

The Solution: Modulation (shifting frequency to a higher band).

Pages 9-20: DSB-SC (Double Sideband Suppressed Carrier)

Mathematical Foundation: Product of message $m(t)$ and carrier $c(t) = \cos(2\pi f_c t)$.

Frequency Domain: Shifting $M(f)$ to $\pm f_c$.

Bandwidth: Why DSB-SC requires $2B$ bandwidth.

Demodulation (Coherent): The requirement of phase/frequency synchronicity.

Pages 21-30: Modulators & Practical Implementation

Multiplier Modulators: Using variable gain.

Non-linear Modulators: Square-law modulators and the filtering process.

Switching Modulators: Modeling modulation as a periodic switching function.

Pages 31-40: Coherent Detection & Phase Errors

Frequency and Phase errors in local oscillators.

The "Vanishing Signal" problem when phase error reaches $90^\circ$.

Pages 41-55: Conventional AM (Large Carrier)

Adding a carrier component: $s(t) = [A + m(t)] \cos(2\pi f_c t)$.

The Condition: $A + m(t) > 0$ for Envelope Detection.

Modulation Index ($\mu$): Under-modulation vs. Over-modulation.

Efficiency: The trade-off between power wasted in the carrier and ease of detection.

Pages 56-65: SSB & QAM

SSB (Single Sideband): Using Hilbert Transforms to save 50% bandwidth.

QAM (Quadrature AM): Sending two signals on the same frequency using sine and cosine (Phase Orthogonality).

Pages 66-75: VSB & Multiplexing

VSB (Vestigial Sideband): The compromise for TV signals.

FDM (Frequency Division Multiplexing): How multiple users share the spectrum.

Pages 76-End: The Phase Locked Loop (PLL)

Tracking the carrier phase automatically.

Components: Phase Detector, Low Pass Filter, and VCO (Voltage Controlled Oscillator).

Part 2: The Master Prompt for Claude

Copy and paste the text below into Claude to generate your deep-dive study materials.

Prompt:
"I am studying for a critical exam on Amplitude Modulation (CSE 311). I have a set of headlines and I need you to act as a world-class Communications Engineer.

Your goal is to create a series of .md files that explain the following topics from First Principles. For every topic, do not just give me the formula; explain the 'Why' behind the physics.

The Topics to Cover:

The Antenna Problem: Prove mathematically why we need modulation based on antenna height vs. wavelength.

DSB-SC vs. Conventional AM: Explain the 'Power vs. Complexity' trade-off. Why do we waste power on a carrier in AM? Explain the Envelope Detector vs. Synchronous Detector.

The Mathematics of Orthogonality: Deep dive into QAM. Show why $\sin$ and $\cos$ don't interfere with each other mathematically.

Bandwidth Efficiency: Compare DSB-SC, SSB, and VSB. Explain the Hilbert Transform's role in SSB.

The PLL (Phase Locked Loop): Explain the feedback loop. How does a VCO 'lock' onto a signal?

Strict Instructions for the Output:

Use First Principles: Start with basic trig identities and build up to the modulation equations.

Visual Descriptions: Describe what the spectrum looks like at every stage (Baseband -> Modulated -> Filtered).

Handholding: Identify the 'Common Pitfalls' where students lose marks (e.g., forgetting the $1/2$ factor in Fourier shifts or phase sync errors).

Format: Provide the output as clear, structured Markdown sections ready for saving."