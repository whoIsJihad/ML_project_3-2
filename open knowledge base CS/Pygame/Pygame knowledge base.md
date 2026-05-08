### `from pygame.locals import *`

**What it does:**

- `pygame.locals` is a module inside Pygame.
    
- It contains **constants** used in Pygame.
    

Examples of constants inside it:

- `QUIT`
    
- `KEYDOWN`
    
- `K_UP`
    
- `K_DOWN`
    
- `K_LEFT`
    
- `K_RIGHT`
    
- `MOUSEBUTTONDOWN`
    

**Why people import it:**

Without it:

```python
import pygame

if event.type == pygame.QUIT:
    running = False
```

With it:

```python
from pygame.locals import *

if event.type == QUIT:
    running = False
```

So it lets you write **shorter names** instead of `pygame.CONSTANT`.

**Important syntax meaning**

`from X import *`  
→ import **everything public** from module `X` into the current namespace.

So after this line, all constants from `pygame.locals` can be used directly.

Example:

```python
if event.type == KEYDOWN:
    print("key pressed")
```
### Sprite
**Sprite**

In Pygame, a **sprite** is an object that represents something **visible in the game**.

Usually:

- a player
    
- enemy
    
- bullet
    
- coin
    
- wall
    
- square
    
- character
    

Basically **anything drawn and updated on the screen**.

**Typical structure**

A sprite usually contains:

1. **image** → what it looks like
    
2. **rect** → its position and size
    
3. **update()** → how it moves or changes
    

Example:

```python
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((50,50))  # appearance
        self.image.fill((255,0,0))            # red square

        self.rect = self.image.get_rect()     # position + size
        self.rect.x = 100
        self.rect.y = 200
```

**Why sprites exist**

Pygame provides a **sprite system** to manage many objects easily:

- draw them
    
- update them
    
- detect collisions
    

Usually used with **sprite groups**:

```python
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

all_sprites.update()
all_sprites.draw(screen)
```

So:

**Sprite = object + image + position + behavior.**


### How to write sprite code?
Code:

```python
class Sq(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((0, 200, 255))
```

### 1. `class Sq(pygame.sprite.Sprite):`

Creates a **new class** called `Sq`.

It **inherits** from `pygame.sprite.Sprite` in Pygame.

Meaning:

- `Sq` becomes a **type of sprite**
    
- it can use sprite system features like groups, collisions, updates.
    

Equivalent idea:

```
Sq IS-A Sprite
```

---

### 2. `def __init__(self):`

Constructor.

Runs when you create the object:

```python
s = Sq()
```

`self` = the object being created.

---

### 3. `super().__init__()`

Runs the **constructor of the parent class** (`Sprite`).

So the base sprite system initializes its internal stuff.

Without this, some sprite features may not work.

Equivalent long form:

```python
pygame.sprite.Sprite.__init__(self)
```

---

### 4. `self.surf = pygame.Surface((25, 25))`

Creates a **surface** (an image buffer).

A `Surface` is basically a **rectangle of pixels**.

Size:

```
25 × 25 pixels
```

Stored in the object as `surf`.

So each `Sq` object has its **own image**.

---

### 5. `self.surf.fill((0, 200, 255))`

Fills that surface with a color.

Color format:

```
(R, G, B)
```

Here:

```
(0, 200, 255) → cyan/light blue
```

So the sprite becomes a **25×25 blue square**.

---

### What the object now contains

If you create:

```python
s = Sq()
```

Memory roughly holds:

```
s
 ├─ surf → Surface(25x25 pixels)
 └─ sprite internal fields (from Sprite class)
```

---

### Same thing **without inheritance**

You could write:

```python
class Sq:
    def __init__(self):
        self.surf = pygame.Surface((25,25))
        self.surf.fill((0,200,255))
```

But then it **will NOT work with sprite groups**, collisions, etc.

Because it's no longer a real `Sprite`.

---

### How to write this **without LLM**

You learn these **3 primitives of Pygame**:

1. `Surface`
    

```
pygame.Surface((w,h))
```

2. Color fill
    

```
surface.fill((r,g,b))
```

3. Sprite inheritance
    

```
class X(pygame.sprite.Sprite)
```

Once you know these **building blocks**, you can write it yourself.

Example you could invent manually:

```python
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((40,40))
        self.surf.fill((255,0,0))
```

Same pattern.


### Python constructor

In Python, the **constructor method name is always `__init__`**, but the **parameters can be anything**.

General form:

```python
class A:
    def __init__(self, ...parameters...):
        ...
```

### Minimal constructor

```python
class A:
    def __init__(self):
        print("object created")
```

Usage:

```python
a = A()
```

---

### Constructor with parameters

```python
class A:
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

Usage:

```python
a = A(5, 10)
```

Here:

```
self = the object being created
x = 5
y = 10
```

---

### Why `self` exists

Python passes the object automatically.

So:

```python
a = A(5,10)
```

is internally like:

```
A.__init__(a, 5, 10)
```

So `self` refers to `a`.

---

### Important rule

Inside **class methods**, the first parameter must represent the object.

By convention we call it:

```
self
```

But technically you could write:

```python
class A:
    def __init__(me):
        print("works")
```

This still works, but **nobody does it**.

---

### Summary

Constructor pattern:

```
def __init__(self, ...)
```

But **arguments vary depending on what the object needs**.

### Python vs C++
Yes. Python classes look different from C++.

### C++ style

Example:

```cpp
class A {
public:
    int a;
    string s;

    A(int x, string y) {
        a = x;
        s = y;
    }
};
```

Fields (`a`, `s`) are **declared in the class body**.

Memory layout is mostly **fixed at compile time**.

---

### Python style

Python does **not declare fields ahead of time**.

Fields are created **when you assign to `self`**.

Example:

```python
class A:
    def __init__(self, x, y):
        self.a = x
        self.s = y
```

When this runs:

```python
obj = A(5, "hello")
```

Python dynamically creates:

```
obj
 ├─ a = 5
 └─ s = "hello"
```

---

### Key difference

C++:

```
fields defined first
then assigned in constructor
```

Python:

```
fields created by assignment
inside __init__
```

So this line:

```python
self.a = x
```

means both:

```
create field a
assign value x
```

---

### Another difference

In C++:

```cpp
A a1;
A a2;
```

Both objects have the **same fixed structure**.

In Python you could do:

```python
a1 = A(1,"x")
a2 = A(2,"y")

a2.extra = 99
```

Now:

```
a1 → a, s
a2 → a, s, extra
```

Objects can have **different fields**.

---

### Mental model

Think of Python objects like **hash maps / dictionaries attached to objects**.

```
self.name = value
```

adds a key-value pair.

---

### pygame.init()

Function in Pygame.

### What it does

Initializes **all Pygame modules** that need setup.

Examples of modules:

- display
    
- sound
    
- keyboard input
    
- mouse input
    
- timers
    
- joystick
    

Without initialization, many parts of Pygame **won't work**.

---

### Typical program start

```python
import pygame

pygame.init()
```

Then you can do things like:

```python
screen = pygame.display.set_mode((800,600))
```

---

### What happens internally (conceptually)

`pygame.init()` calls things like:

```
display.init()
mixer.init()
font.init()
joystick.init()
```

Each subsystem prepares the OS resources it needs.

---

### Return value

```python
(success_count, fail_count)
```

Example:

```
(6, 0)
```

Meaning:

```
6 modules initialized
0 failed
```

Most people ignore the return value.
### `pygame.display.set_mode((800, 600))`

Function from the **display module** of Pygame.

### What it does

Creates the **game window** and the **main drawing surface**.

```
(800, 600)
 width height
```

So the window size becomes:

```
800 pixels wide
600 pixels tall
```

---

### Return value

It returns a **Surface object**.

Usually stored like:

```python
screen = pygame.display.set_mode((800,600))
```

Now `screen` is the **canvas you draw on**.

---

### Example drawing

```python
screen.fill((0,0,0))
```

fills the window black.

---

### Mental model

```
screen = display.set_mode(...)
```

creates:

```
Game Window
┌─────────────────────────┐
│                         │
│        screen           │
│      (Surface)          │
│                         │
└─────────────────────────┘
```

You draw everything onto `screen`.

Then you show it using:

```python
pygame.display.update()
```

or

```python
pygame.display.flip()
```


### **Events in** Pygame

Events = **things the user or system does**.

Examples:

```text
key press
mouse click
window close
mouse move
```

Pygame stores these in an **event queue**.

Your program **reads the queue every frame**.

---

### Getting events

```python
for event in pygame.event.get():
```

`pygame.event.get()`  
→ returns a **list of events currently in the queue**.

Example loop:

```python
for event in pygame.event.get():
    print(event)
```

---

### Typical event handling

```python
for event in pygame.event.get():
    if event.type == QUIT:
        running = False
```

`QUIT` happens when the user clicks the **window close button**.

---

### Keyboard example

```python
for event in pygame.event.get():
    if event.type == KEYDOWN:
        print("key pressed")
```

`KEYDOWN` = a key was pressed.

Specific key:

```python
if event.key == K_SPACE:
    print("space pressed")
```

---

### Mouse example

```python
if event.type == MOUSEBUTTONDOWN:
    print("mouse clicked")
```

---

### Event object structure

An event contains fields.

Example keyboard event:

```text
event.type = KEYDOWN
event.key  = K_LEFT
```

Example mouse event:

```text
event.type = MOUSEBUTTONDOWN
event.pos  = (x,y)
event.button = 1
```

---

### Why events must be processed

If you don't read events:

```text
window freezes
OS thinks program is unresponsive
```

So every game loop must include:

```python
for event in pygame.event.get():
```

---

### Typical game loop skeleton

```python
running = True

while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
```


---

### `Surface.blit(source, dest)`

**Purpose:**  
Copy the pixels from one surface (`source`) onto another surface (`destination`) at a specified position.

**Syntax:**

```python
destination_surface.blit(source_surface, position)
```

**Parameters:**

- `source_surface` → the `Surface` to draw.
    
- `position` → tuple `(x, y)` specifying the **top-left corner** on the destination where the source will appear.
    

**Returns:**

- A `Rect` representing the area of the destination that was updated.
    

**Notes:**

- Does **not display** immediately; call `pygame.display.update()` or `pygame.display.flip()` to show changes.
    
- Used for drawing images, sprites, or shapes stored in surfaces.
    

**Example:**

```python
win = pygame.display.set_mode((800,600))
player = pygame.Surface((25,25))
player.fill((0,200,255))

win.blit(player, (40,40))
pygame.display.update()
```

**Visual effect:**  
Draws a 25×25 blue square at coordinates `(40,40)` on the window.

---

### Speed in Pygame

**Problem:** Game loop runs too fast if unchecked.

**Use Clock to control FPS:**

```python
clock = pygame.time.Clock()
clock.tick(60)  # 60 frames per second
```

**Movement speed:**

```python
speed = 5  # pixels per frame
x += speed
```

**Full loop example:**

```python
clock = pygame.time.Clock()
speed = 5
x = 100
run = True
while run:
    for e in pygame.event.get():
        if e.type == QUIT:
            run = False

    x += speed
    win.fill((0,0,0))
    win.blit(player_surf, (x,100))
    pygame.display.flip()
    clock.tick(60)
```

- **Loop runs 60 times per second**.
    
- **Object moves speed × FPS pixels per second**.