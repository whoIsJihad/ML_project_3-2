# Theoretical Questions: Digital Communications

## Section 1: Bandwidth and Transmission Fundamentals

1. Explain why signal bandwidth must be less than or equal to channel bandwidth for successful transmission. What happens when this condition is violated?

2. A communication channel has a bandwidth of 10 kHz. Can it successfully transmit: (a) human voice, (b) FM radio quality music? Justify your answers.

3. Describe the difference between signal bandwidth and channel bandwidth. Give a real-world analogy to explain this distinction.

4. Why does increasing signal bandwidth generally require increasing channel bandwidth? What are the practical implications for communication system design?

5. What is the relationship between a signal's time duration and its required bandwidth? Explain using the time-frequency uncertainty principle.

## Section 2: Signal-to-Noise Ratio and System Performance

6. Define Signal-to-Noise Ratio (SNR). Why is it typically expressed in decibels rather than as a linear ratio?

7. Explain how SNR affects the data rate of a communication channel according to Shannon's Capacity formula.

8. If SNR is very low (close to 0 dB), what strategies can be employed to still achieve reliable communication?

9. Compare the impact of doubling the bandwidth versus doubling the SNR on channel capacity. Which has a more dramatic effect?

10. Why does increasing signal power improve noise immunity? Explain the physical reasoning.

## Section 3: Energy Signals vs Power Signals

11. Define energy signals and power signals. Why can't a signal be both simultaneously?

12. Explain why periodic signals are classified as power signals while transient pulses are energy signals.

13. Which type of signal (energy or power) is more relevant for practical communication systems? Justify your answer.

14. State the mathematical conditions that define an energy signal. What must be true about the signal's behavior as time approaches infinity?

15. Give three examples each of energy signals and power signals from real-world applications.

## Section 4: Fourier Analysis Foundations

16. Explain the conceptual transition from Fourier Series to Fourier Transform. What happens to the frequency spectrum as the period approaches infinity?

17. What is the significance of the Fourier Transform pair? How do the analysis and synthesis equations relate to each other?

18. State Dirichlet's conditions for the existence of the Fourier Transform. Why is the finite energy condition necessary?

19. Explain why we use Fourier Series for periodic signals and Fourier Transform for aperiodic signals.

20. What does it mean for a signal to be "decomposed into harmonically related sinusoids"? Why must they be harmonically related?

## Section 5: Fourier Transform Properties

21. Explain the time scaling property of the Fourier Transform. Why does compressing a signal in time expand its spectrum?

22. State and explain the convolution theorem. Why is this property considered the most important for system analysis?

23. What is the duality property? Give an example of how it can be used to derive new transform pairs.

24. Explain the time shift property. Why does delaying a signal affect only its phase spectrum and not its magnitude spectrum?

25. Describe the multiplication theorem. How is it related to the convolution theorem?

## Section 6: Special Functions

26. Define the unit impulse (delta) function. Why is it not a "real" function in the conventional sense?

27. Explain the sampling property of the delta function. How is this property used in signal sampling?

28. What is the Fourier Transform of the delta function? What does this reveal about the frequency content of an impulse?

29. Define the sinc function. Why does it appear so frequently in communication theory?

30. Explain why an ideal lowpass filter has a sinc function as its impulse response. What makes this filter "unrealizable" in practice?

## Section 7: Sampling Theory

31. State the Sampling Theorem. What is the Nyquist rate and why is it significant?

32. Explain the concept of spectral replication in sampled signals. Why does sampling create copies of the spectrum?

33. What is aliasing? Under what conditions does it occur, and why is it irreversible?

34. Describe the interpolation formula for perfect signal reconstruction. What role does the sinc function play?

35. Why is it common to sample at rates higher than the Nyquist rate in practical systems? What factors influence this decision?

36. Explain why an ideal lowpass filter is required for perfect reconstruction. What are the challenges in implementing this?

37. What is the relationship between sampling interval and sampling frequency? How does this relate to the Nyquist interval?

## Section 8: LTI Systems and Transfer Functions

38. What does it mean for a system to be Linear and Time-Invariant? Give examples of systems that violate each property.

39. Explain why the impulse response completely characterizes an LTI system.

40. Compare the difficulty of analyzing LTI systems in the time domain versus the frequency domain. Why is frequency domain analysis preferred?

41. Define the transfer function H(f). What information does its magnitude and phase provide?

42. How does filtering become multiplication in the frequency domain? Explain using the convolution theorem.

43. What is the difference between a lowpass, highpass, and bandpass filter in terms of their transfer functions?

44. Explain the concept of linear phase response. Why is it desirable in communication systems?

## Section 9: Shannon Capacity and Fundamental Limits

45. State Shannon's Channel Capacity formula. What does it represent fundamentally?

46. Explain the bandwidth-SNR tradeoff. In what types of channels is bandwidth more important than power, and vice versa?

47. Why does channel capacity increase logarithmically with SNR rather than linearly? What are the practical implications?

48. What happens to channel capacity as bandwidth approaches infinity with fixed power? Why doesn't capacity become infinite?

49. Explain why Shannon Capacity is considered a fundamental limit. Can any coding scheme exceed this limit?

## Section 10: Analog-to-Digital Conversion

50. Describe the two steps of Analog-to-Digital Conversion. Why are both necessary?

51. Explain the difference between sampling and quantization. Which introduces irreversible error?

52. Why does increasing the sampling rate improve the fidelity of digitized signals?

53. How does the number of quantization levels relate to the number of bits used? What is the tradeoff?

54. Explain why quantization error cannot be reduced to zero. How does it differ from sampling according to the sampling theorem?

## Section 11: Source Coding vs Channel Coding

55. What is the goal of source coding? Give an example of a source coding technique.

56. What is the goal of channel coding? Why does it seem to contradict source coding?

57. Explain the concept of redundancy. How does it differ in source coding versus channel coding?

58. Why do communication systems typically use both source coding and channel coding in sequence?

## Section 12: Signal Properties and Transformations

59. What is a periodic signal? Give the mathematical definition and two examples.

60. Explain the operations of time shifting, time scaling, and time inversion. Give the order of operations for a composite transformation like x(2t - 3).

61. What is the difference between continuous-time and discrete-time signals? Between continuous-amplitude and discrete-amplitude signals?

62. Define an analog signal and a digital signal using the time and amplitude dimensions.

## Section 13: Unit Step Function

63. Define the unit step function u(t). What is its relationship with the unit impulse function?

64. How can the unit step function be expressed as an integral of the impulse function?

65. What is the derivative of the unit step function? How is this relationship useful?

## Section 14: Advanced Properties and Concepts

66. Explain Parseval's Theorem. What does it tell us about energy conservation in Fourier analysis?

67. What is the significance of conjugate symmetry in Fourier Transforms? When does it apply?

68. Explain the differentiation property of the Fourier Transform. Why does it act like a high-pass filter?

69. Explain the integration property of the Fourier Transform. Why does it act like a low-pass filter?

70. Describe the frequency shift (modulation) property. How is this used in communication systems to shift signals to different frequency bands?

## Section 15: Conceptual Integration Questions

71. Explain the complete chain: How does bandwidth, SNR, and Shannon Capacity all relate to determine the maximum data rate of a channel?

72. Trace the process of transmitting an analog signal digitally: from ADC (sampling and quantization) through transmission over a bandwidth-limited, noisy channel, to reconstruction at the receiver.

73. Why is Fourier analysis fundamental to communication theory? How does it unify the concepts of bandwidth, filtering, and sampling?

74. Explain how the concepts of energy signals, Fourier Transform, and sampling theorem are interconnected.

75. Describe the role of the sinc function in connecting frequency-domain filtering (ideal lowpass) with time-domain signal reconstruction.

## Section 16: Formulas and Key Equations

76. State the formula for Signal-to-Noise Ratio in both linear and decibel forms.

77. Write the Fourier Transform pair equations (analysis and synthesis).

78. State the Shannon Capacity formula and identify each term.

79. Write the formulas for signal energy and signal power.

80. State the sampling theorem inequality and define the Nyquist rate.
