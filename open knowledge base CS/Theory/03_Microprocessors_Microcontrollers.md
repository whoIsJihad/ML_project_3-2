# Microprocessors & Microcontrollers

## Quick Reference
**Reading Time:** ~2 hours  
**Prerequisites:** [[02_Computer_Architecture]], [[01_Digital_Logic_Design]]  
**Next:** [[05_Memory_Systems]]

---

## 1. Microprocessor vs Microcontroller

### Microprocessor (μP)
- **General-purpose CPU** on a single chip
- Requires external memory, peripherals, I/O
- High performance, flexible
- **Examples:** Intel Core, AMD Ryzen, ARM Cortex-A
- **Use:** PCs, servers, smartphones

### Microcontroller (μC)
- **Complete computer system** on a single chip
- Includes: CPU, RAM, ROM/Flash, I/O, timers, ADC/DAC
- Low power, cost-effective, integrated
- **Examples:** ARM Cortex-M, AVR, PIC, ESP32, STM32
- **Use:** Embedded systems (IoT, automotive, appliances)

### Comparison Table

| Feature | Microprocessor | Microcontroller |
|---------|---------------|-----------------|
| **Integration** | CPU only | CPU + Memory + I/O |
| **Performance** | High | Moderate |
| **Power** | High | Low |
| **Cost** | High | Low |
| **Memory** | External (GB) | On-chip (KB-MB) |
| **Architecture** | Von Neumann or Harvard | Mostly Harvard |
| **Application** | Compute-intensive | Control-intensive |

---

## 2. Microprocessor Architecture

### x86-64 Architecture (Intel/AMD)

**Key Features:**
- CISC instruction set
- Variable-length instructions (1-15 bytes)
- 16 general-purpose 64-bit registers (RAX, RBX, ..., R15)
- 16 128/256/512-bit vector registers (XMM, YMM, ZMM)
- Segment registers (legacy compatibility)
- x86 compatibility mode

**Registers:**
- **RAX-RDX:** General purpose (accumulator, base, counter, data)
- **RSI, RDI:** Index registers (string operations)
- **RBP, RSP:** Base pointer, stack pointer
- **RIP:** Instruction pointer (program counter)
- **RFLAGS:** Status flags (zero, carry, overflow, etc.)

**Instruction Format:**
```
[Prefix] [Opcode] [ModR/M] [SIB] [Displacement] [Immediate]
```
- Highly variable and complex

**Operating Modes:**
- **Real Mode:** 16-bit (legacy DOS)
- **Protected Mode:** 32-bit with virtual memory
- **Long Mode:** 64-bit

### ARM Architecture

**Key Features:**
- RISC instruction set
- Fixed 32-bit instructions (ARM) or 16/32-bit (Thumb/Thumb-2)
- Load/store architecture
- Conditional execution on most instructions
- 16 general-purpose 32-bit registers (R0-R15)
- Barrel shifter for efficient shift operations

**Register Summary:**
- **R0-R12:** General purpose
- **R13 (SP):** Stack pointer
- **R14 (LR):** Link register (return address)
- **R15 (PC):** Program counter
- **CPSR:** Current program status register (flags)

**Profiles:**
- **Cortex-A:** Applications (high performance, OS support)
- **Cortex-R:** Real-time (predictable, low latency)
- **Cortex-M:** Microcontrollers (low power, integrated peripherals)

**Thumb Mode:**
- 16-bit instruction encoding
- Better code density
- Slightly lower performance than 32-bit ARM
- Thumb-2: Mix of 16/32-bit for best of both

### RISC-V Architecture

**Key Features:**
- Open-source ISA
- Modular extensions (I, M, A, F, D, C)
- Clean, simple design
- 32 general-purpose registers (x0-x31)
- x0 always zero

**Base ISAs:**
- RV32I: 32-bit integer
- RV64I: 64-bit integer
- RV128I: 128-bit integer (future)

**Extensions:**
- **M:** Integer multiply/divide
- **A:** Atomic operations
- **F:** Single-precision floating point
- **D:** Double-precision floating point
- **C:** Compressed (16-bit) instructions
- **V:** Vector operations

---

## 3. Microcontroller Architectures

### AVR (Atmel/Microchip)

**Features:**
- 8-bit RISC
- Harvard architecture
- 32 general-purpose registers
- Single-cycle execution (most instructions)
- **Popular:** Arduino uses ATmega series

**Peripherals:**
- GPIO (General Purpose I/O)
- UART, SPI, I2C
- Timers/Counters
- ADC (10-bit)
- PWM
- Interrupts

**Memory:**
- Flash: 2-256 KB (program)
- SRAM: 128 bytes - 16 KB (data)
- EEPROM: 0-4 KB (non-volatile data)

### ARM Cortex-M

**Features:**
- 32-bit RISC (Thumb-2 instructions)
- Harvard architecture
- 13 general registers + SP, LR, PC
- Nested Vectored Interrupt Controller (NVIC)
- Low power modes
- Memory Protection Unit (MPU)

**Variants:**
- **Cortex-M0/M0+:** Ultra-low power, simple (IoT sensors)
- **Cortex-M3:** Balanced performance/power
- **Cortex-M4:** DSP instructions, FPU (audio, motor control)
- **Cortex-M7:** High performance, cache (industrial)
- **Cortex-M33:** TrustZone security (secure boot)

**Interrupt Handling:**
- Automatic register stacking
- Tail-chaining (no overhead between consecutive interrupts)
- Interrupt priorities (0-255)

### PIC (Microchip)

**Features:**
- 8-bit, 16-bit, 32-bit variants
- Harvard architecture
- Accumulator-based (older models)
- Wide product range

**PIC16/18 (8-bit):**
- Simple instruction set (~35-80 instructions)
- Bank-switched memory
- Popular in hobbyist/educational projects

### ESP32 (Espressif)

**Features:**
- 32-bit Xtensa LX6 dual-core (up to 240 MHz)
- Wi-Fi + Bluetooth integrated
- 520 KB SRAM, external flash
- Rich peripherals (ADC, DAC, touch sensors, etc.)
- FreeRTOS support

**Popular for:** IoT, wireless projects

---

## 4. Memory Architecture

### Harvard Architecture in Microcontrollers

**Separate buses for instruction and data:**
- Instruction bus: Fetch opcode from program memory (Flash/ROM)
- Data bus: Access variables in data memory (SRAM)

**Advantages:**
- Parallel instruction fetch and data access
- Different bus widths optimized for each
- No Von Neumann bottleneck

**Modified Harvard:**
- Separate caches, unified main memory (modern CPUs)
- Allows constants in program memory (AVR)

### Memory Map

**Typical Layout:**
```
0x00000000: Interrupt Vectors
0x00000100: Program Code (Flash/ROM)
0x20000000: SRAM (Data, Stack, Heap)
0x40000000: Peripheral Registers (Memory-mapped I/O)
0xE0000000: System Registers (ARM Cortex-M)
```

### Stack
- **Stack Pointer (SP):** Current top of stack
- **Push:** Decrement SP, write data
- **Pop:** Read data, increment SP
- **Usage:** Function calls, local variables, interrupt context

**Stack Overflow:** Critical error, overwrites data

---

## 5. Peripheral Interfacing

### Memory-Mapped I/O
- Peripherals accessed via memory addresses
- Read/write to specific addresses controls hardware
- Example: `*(volatile uint32_t*)0x40020000 = 0x01;` sets GPIO pin

**Volatile Keyword:** Prevents compiler optimization (hardware can change value)

### Registers for Peripherals

**Typical Registers:**
- **Control Register:** Configure mode, enable/disable
- **Status Register:** Current state, flags
- **Data Register:** Read/write data

**Example: USART (Serial Port)**
- **USART_CR1:** Control (enable TX/RX, parity, etc.)
- **USART_SR:** Status (TX empty, RX ready, errors)
- **USART_DR:** Data register (send/receive bytes)

---

## 6. Input/Output Peripherals

### GPIO (General Purpose Input/Output)
- Digital pins configurable as input or output
- **Modes:**
  - Input: Floating, pull-up, pull-down
  - Output: Push-pull, open-drain
  - Alternate function (UART, SPI, etc.)
  - Analog (for ADC)

**Operations:**
- Set pin high: `GPIO->BSRR = (1 << pin);`
- Set pin low: `GPIO->BRR = (1 << pin);`
- Read pin: `value = (GPIO->IDR >> pin) & 1;`

### Timers/Counters
- Count clock cycles or external events
- Generate periodic interrupts
- **Modes:**
  - Basic timer (count up/down)
  - Capture (measure input pulse width)
  - Compare (generate output at specific count)
  - PWM (Pulse Width Modulation)

**PWM:**
- Duty cycle control (e.g., LED brightness, motor speed)
- Frequency typically 1-100 kHz
- Duty cycle: $\frac{t_{on}}{t_{period}} \times 100\%$

### ADC (Analog-to-Digital Converter)
- Convert analog voltage to digital value
- **Resolution:** 8-bit, 10-bit, 12-bit, 16-bit typical
- **Reference Voltage:** Defines max voltage (e.g., 3.3V, 5V)
- **Conversion:** $Digital = \frac{V_{in}}{V_{ref}} \times (2^{resolution} - 1)$

**Sampling Rate:** Conversions per second (1 kSPS - 1 MSPS typical)

**Modes:**
- Single conversion
- Continuous conversion
- Scan mode (multiple channels)

### DAC (Digital-to-Analog Converter)
- Convert digital value to analog voltage
- Less common than ADC in microcontrollers
- Used for: Audio output, waveform generation

### Communication Interfaces

#### UART (Universal Asynchronous Receiver/Transmitter)
- **Pins:** TX (transmit), RX (receive), GND
- **Parameters:** Baud rate (9600, 115200, etc.), data bits, parity, stop bits
- **Asynchronous:** No shared clock
- **Simple, point-to-point**

**Frame Format:**
```
[Start bit (0)] [Data (7-8 bits)] [Parity (optional)] [Stop bit(s) (1)]
```

#### SPI (Serial Peripheral Interface)
- **Pins:** MOSI (master out), MISO (master in), SCK (clock), SS/CS (select)
- **Synchronous:** Master provides clock
- **Full-duplex:** Simultaneous TX and RX
- **Fast:** 10+ MHz typical
- **Multi-slave:** Chip select per slave

**Modes (CPOL/CPHA):**
- Mode 0: CPOL=0, CPHA=0
- Mode 1: CPOL=0, CPHA=1
- Mode 2: CPOL=1, CPHA=0
- Mode 3: CPOL=1, CPHA=1

#### I2C (Inter-Integrated Circuit)
- **Pins:** SDA (data), SCL (clock)
- **Multi-master, multi-slave**
- **Addressing:** 7-bit or 10-bit slave addresses
- **Slower than SPI:** 100 kHz (standard), 400 kHz (fast), 3.4 MHz (high-speed)
- **Bidirectional:** One data line (half-duplex)

**Transaction:**
1. Master sends START condition
2. Master sends slave address + R/W bit
3. Addressed slave ACKs
4. Data transfer (with ACK after each byte)
5. Master sends STOP condition

**Advantages:** Only 2 wires, addressable devices

#### CAN (Controller Area Network)
- **Pins:** CANH, CANL (differential pair)
- **Multi-master:** Any node can transmit
- **Robust:** Error detection, arbitration
- **Use:** Automotive, industrial control
- **Speed:** Up to 1 Mbps

---

## 7. Interrupts

### Interrupt Concept
- Asynchronous event handling
- Pause current execution, run handler, resume
- **Triggered by:** Peripherals (UART RX, timer overflow), external pins, software

### Interrupt Vector Table
- Array of handler addresses
- Index corresponds to interrupt source
- Cortex-M: First entry is initial stack pointer

### Priority
- Multiple interrupts → Handle by priority
- **Preemption:** High priority can interrupt low priority handler
- **Nesting:** Interrupts within interrupts

### Interrupt Latency
- Time from event to handler execution
- Components: Detection, context save, vector fetch, jump
- **Cortex-M:** Very low latency (~12 cycles) due to automatic stacking

### Best Practices
- **Keep handlers short:** Minimize time in interrupt context
- **Set flags, defer work:** Main loop processes detailed logic
- **Disable carefully:** Critical sections protect shared data
- **Volatile variables:** For communication with main code

---

## 8. Power Management

### Low Power Modes

**Active Mode:**
- CPU running, all peripherals available
- Highest power consumption

**Sleep Mode:**
- CPU stopped, peripherals running
- Wake on interrupt
- Low exit latency

**Deep Sleep / Stop Mode:**
- CPU and some peripherals stopped
- Clocks gated
- Very low power
- Slower wake-up

**Standby / Shutdown Mode:**
- Nearly everything off
- Only RTC, backup registers
- Ultra-low power (μA range)
- Slow wake-up (like reset)

### Power Saving Techniques
- **Clock gating:** Disable clocks to unused peripherals
- **Dynamic voltage/frequency scaling:** Lower voltage/speed when possible
- **Peripheral shut down:** Disable unused modules
- **Optimize code:** Less cycles = less power

**Battery Life:**
$$Life = \frac{Battery\ Capacity\ (mAh)}{Average\ Current\ (mA)}$$

---

## 9. Real-Time Operating Systems (RTOS)

### Bare-Metal vs RTOS

**Bare-Metal:**
- Main loop + interrupts
- Simple, low overhead
- Good for simple applications

**RTOS:**
- Multi-tasking kernel
- Task scheduling, synchronization, communication
- Complex applications, easier development

### RTOS Concepts

**Task/Thread:**
- Independent execution unit
- Has own stack, priority
- Managed by scheduler

**Scheduler:**
- Decides which task runs
- **Preemptive:** High priority task preempts low priority
- **Round-robin:** Equal priority tasks share time slices

**Context Switch:**
- Save current task state, load new task state
- Overhead: ~10-100 cycles

**Synchronization:**
- **Semaphore:** Signaling, resource counting
- **Mutex:** Mutual exclusion (binary semaphore with ownership)
- **Queue:** Inter-task communication (FIFO)
- **Event Flags:** Signal multiple events

**Priority Inversion:**
- Low-priority task holds resource needed by high-priority
- **Solution:** Priority inheritance (temporary boost)

**Popular RTOS:**
- FreeRTOS (open-source, widely used)
- Zephyr
- RIOT
- mbed OS
- ThreadX

---

## 10. Microprocessor Interfaces

### Bus Interfaces

**Address Bus:**
- Specifies memory/device location
- Width determines addressable space (20-bit → 1 MB)

**Data Bus:**
- Carries data
- Width: 8-bit, 16-bit, 32-bit, 64-bit

**Control Bus:**
- Read/Write signals
- Clock
- Chip select
- Interrupt request

### Memory Interface

**SRAM:**
- Fast, direct connection
- Address + control → data ready same/next cycle

**DRAM:**
- Requires refresh cycles
- Memory controller handles timing
- RAS (Row Address Strobe), CAS (Column Address Strobe)

**Flash/ROM:**
- Non-volatile program storage
- Slower writes, fast reads
- Wear leveling for flash

### Peripheral Bus Standards

**AHB (Advanced High-performance Bus):**
- High-speed, pipelined
- For fast peripherals (DMA, memory)

**APB (Advanced Peripheral Bus):**
- Simpler, lower speed
- For slower peripherals (UART, I2C)

**AXI (Advanced eXtensible Interface):**
- High performance, burst transfers
- Used in complex SoCs

---

## 11. Development Tools

### Cross-Compilation
- Compile on PC (host) for microcontroller (target)
- **Toolchain:** Compiler, linker, assembler for target architecture
- Examples: GCC ARM, Keil, IAR

### Programming/Debugging Interfaces

**JTAG (Joint Test Action Group):**
- Standard debugging interface
- Boundary scan, memory access, breakpoints
- 4-5 pins: TDI, TDO, TCK, TMS, (TRST)

**SWD (Serial Wire Debug):**
- ARM's 2-pin alternative to JTAG
- SWDIO (data), SWCLK (clock)
- Simpler, fewer pins

**Bootloader:**
- Pre-loaded program to update firmware
- Can program over UART, USB, etc. without debugger

### Simulation & Emulation
- **Simulator:** Software model (fast, not cycle-accurate)
- **Emulator:** Hardware-based (cycle-accurate, expensive)
- **Virtual Prototype:** Fast functional model for software development

---

## 12. Performance Considerations

### Clock Speed
- Higher frequency → more instructions per second
- Limited by: Power, heat, critical path delay

### Instruction Throughput
- **Pipeline depth:** Affects throughput and latency
- **Superscalar:** Multiple instructions per cycle (rare in microcontrollers)

### Memory Bottleneck
- Flash slower than SRAM
- **Solutions:** Cache, copy code to RAM, wait states

### Peripheral Overhead
- **Polling:** Wastes CPU cycles
- **Interrupts:** Efficient but latency
- **DMA:** Offload data transfers (best for large transfers)

### Code Optimization
- **Compiler flags:** -O2, -O3, -Os (size)
- **Inline functions:** Reduce call overhead
- **Array access:** Contiguous memory, cache-friendly
- **Fixed-point:** Faster than floating-point (if no FPU)

---

## 13. Common Microcontroller Applications

### Embedded Systems
- **Automotive:** Engine control, ABS, airbags
- **Industrial:** PLCs, motor drives, sensors
- **Consumer:** Washing machines, microwaves, remote controls
- **Medical:** Pacemakers, glucose monitors
- **IoT:** Smart home devices, wearables, environmental sensors

### Typical System Architecture
```
[Sensors] → [ADC] → [Microcontroller] → [DAC/GPIO] → [Actuators]
                          ↓
                    [Communication]
                          ↓
                    [Gateway/Cloud]
```

---

## Key Concepts Summary

| Concept | Core Principle |
|---------|----------------|
| **Microprocessor** | CPU only, requires external components |
| **Microcontroller** | Complete system on chip (CPU + memory + I/O) |
| **Harvard Architecture** | Separate instruction and data memory/buses |
| **Memory-Mapped I/O** | Peripherals accessed via memory addresses |
| **Interrupts** | Asynchronous event handling |
| **Power Modes** | Trade performance for power savings |
| **RTOS** | Multi-tasking for complex applications |
| **Communication Protocols** | UART, SPI, I2C, CAN for external interfacing |

---

## Common Pitfalls

1. **Forgetting volatile for hardware registers** → Compiler optimizes away reads
2. **Stack overflow** → Overwriting variables, crashes
3. **Interrupt re-entrancy** → Shared data corruption
4. **Incorrect clock/baud rate** → Communication failures
5. **Uninitialized peripherals** → Unpredictable behavior
6. **Blocking in interrupt handlers** → Missed interrupts, system freeze
7. **Not considering power consumption** → Short battery life

---

## Cross-Links
- [[02_Computer_Architecture]] - General processor concepts
- [[01_Digital_Logic_Design]] - Hardware building blocks
- [[05_Memory_Systems]] - Memory hierarchy details
- [[Session_04_Databases_Concurrency]] - Synchronization concepts apply to RTOS
- [[Session_05_Networks_Distributed_Systems]] - Communication protocols

---

## Quick Reference

**GPIO Write:** `*GPIO_REG = value;`  
**ADC Resolution:** $Levels = 2^{bits}$  
**UART Frame:** `[Start][Data][Parity][Stop]`  
**PWM Duty Cycle:** $DC = \frac{t_{on}}{t_{period}} \times 100\%$  
**I2C Transaction:** `START → ADDR+R/W → ACK → DATA → ACK → STOP`  
**Power:** $P = V \times I$  
**Interrupt Latency:** Detection + Save Context + Vector Fetch + Jump
