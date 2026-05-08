
## **Lockstep = Synchronized Movement**

**Lockstep** literally means moving in perfect sync, like soldiers marching in step together.

In programming:

```c
for (int i = 0; i < SIZE; i++) {
    array1[i]++;    // Step 1: Access array1
    array2[i]++;    // Step 2: Access array2
}
```

Both arrays are accessed **together** on each loop iteration — they're **in lockstep**. When `i=0`, you access both `array1[0]` and `array2[0]`. When `i=1`, you access both `array1[1]` and `array2[1]`.

**Contrast with non-lockstep:**

```c
// Process array1 first, then array2 separately
for (int i = 0; i < SIZE; i++) {
    array1[i]++;
}
for (int i = 0; i < SIZE; i++) {
    array2[i]++;
}
```

Here they're **not** in lockstep — you finish one array completely before touching the other.

---

## **Why Lockstep Causes Thrashing**

When you access two arrays in lockstep AND they map to the same cache sets:

- You load `array1[i]` into Set X
- Immediately load `array2[i]` — also into Set X
- This **evicts** `array1[i]` you just loaded
- Next iteration, you need `array1[i]` again → cache miss
- Loop repeats → constant thrashing

If you process them separately (non-lockstep), the cache has time to age out old data from one array before you switch to the other.

That's the essence of it!