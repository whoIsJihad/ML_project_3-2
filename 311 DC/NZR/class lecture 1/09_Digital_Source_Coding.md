# 9. Digital Source Coding (Compression)

**Source coding**, in the context of digital communications, is more commonly known as **data compression**. Its primary goal is to reduce the number of bits required to represent information from a source, making it more efficient to store and transmit.

The fundamental idea is to **remove redundancy**. Most raw data contains repetitive or predictable patterns. Source coding finds these patterns and represents them more efficiently.

There are two main categories of source coding:

### 1. Lossless Compression

Lossless compression algorithms reduce the file size without losing a single bit of the original information. When the data is decompressed, it is a perfect, bit-for-bit reconstruction of the original.

*   **How it Works:** These methods identify statistical redundancy. For example, in a text file, the letter 'e' and the word 'the' appear very frequently. An algorithm could replace 'the ' with a single, shorter code.
*   **Use Cases:** Essential for data where perfect accuracy is non-negotiable.
    *   Text files (e.g., `.txt`, `.docx`)
    *   Computer program executables (e.g., `.exe`, `.jar`)
    *   General-purpose file archives (e.g., `.zip`, `.rar`)
*   **Examples:**
    *   **Huffman Coding:** Assigns short binary codes to frequently occurring symbols and longer codes to less frequent ones.
    *   **Lempel-Ziv (LZ) family (LZ77, LZ78, LZW):** Forms the basis of popular formats like `.zip`, `.gz`, and `.png`. These algorithms work by finding repeated sequences of data and replacing them with a reference to their previous occurrence.

### 2. Lossy Compression

Lossy compression achieves much higher compression ratios by permanently discarding some of the "less important" information from the original data. The decompressed data is not identical to the original but is close enough for its intended purpose.

*   **How it Works:** These algorithms are based on models of human perception. They remove details that our eyes or ears are unlikely to notice. For example, in an image, they might discard very subtle color variations, and in audio, they might remove frequencies that are masked by louder sounds.
*   **Use Cases:** Ideal for analog media like images, audio, and video, where perfect fidelity is not required and a smaller file size is highly desirable.
*   **Examples:**
    *   **JPEG (Joint Photographic Experts Group):** For still images. It transforms the image into frequency components and aggressively quantizes the high-frequency components that represent fine details our eyes are less sensitive to.
    *   **MP3 (MPEG-1 Audio Layer III):** For audio. It uses psychoacoustic models to remove sounds that are inaudible to the human ear.
    *   **MPEG (Moving Picture Experts Group) family (MPEG-2, MPEG-4, H.264, H.265):** For video. These algorithms compress individual frames (like JPEG) and also exploit temporal redundancy between frames (e.g., a static background that doesn't change for several seconds).