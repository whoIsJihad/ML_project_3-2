# Containerization & Docker: Fundamentals

## The Problem: "It Works on My Machine"

A developer builds code on Ubuntu 22.04 with Python 3.10 and Flask 2.1. The app works perfectly locally.
When deployed to production (Ubuntu 20.04 with Python 3.8, Flask 1.9), it breaks.

**Why?** The stack has three layers:

```
Layer 3 (Top):     Application Code
Layer 2 (Middle):  Libraries/Dependencies (versions matter: Python 3.10 vs 3.8, Flask 2.1 vs 1.9)
Layer 1 (Bottom):  Operating System (Ubuntu 22.04 vs 20.04)
```

The developer's machine has all three layers. The server has a different combination. **Dependency Hell**: Versions don't match.

**Solution**: Ship the entire stack, not just the code.

---

## Docker Images: The Snapshot

A **Docker Image** is a read-only snapshot containing everything needed to run the application:

- Application code
- Runtime (Python 3.10, Node.js 18, Java 17, etc.)
- Libraries/dependencies with exact versions (requirements.txt, package.json, etc.)
- Base OS configuration (Ubuntu, Alpine, etc.)
- Environment variables, startup commands

Think of it as a "frozen recipe" or "blueprint." The image never changes once created.

**Key property**: An image built on Developer Machine X will run identically on Production Server Y.

---

## Docker Containers: The Instance

A **Docker Container** is a running instance of a Docker Image.

| Concept | Analogy | Reality |
|---------|---------|---------|
| Image | Recipe (frozen, read-only) | Blueprint for running an app |
| Container | Actual cooked meal | Running app instance |

**One image can spawn multiple containers**: If you need three instances of your web app load-balanced behind a proxy, you create three containers from the same image.

---

## Container Architecture

```
Hardware (CPU, RAM, Disk)
        ↓
Host Operating System (Ubuntu 22.04)
        ↓
Container Engine (Docker Daemon)
        ↓
Container 1 (App X) | Container 2 (App Y) | Container 3 (App Z)
```

Each container is isolated: Container 1 runs Python 3.10, Container 2 runs Python 3.11, both on the same OS.

**Contrast with Virtual Machines**:
```
VMs: Hardware → Hypervisor → Guest OS A (Ubuntu) → App X
                           → Guest OS B (Ubuntu) → App Y   // Extra OS per app (heavy)

Containers: Hardware → Host OS (Ubuntu) → Docker → Container X → App X
                                                  → Container Y → App Y   // Shared OS (light)
```

Containers share the Host OS kernel, making them faster and more efficient.

---

## Isolation Without Overhead

Containers don't need separate operating systems. Docker's **namespaces** isolate:

- **Process namespace**: Container 1's processes don't see Container 2's processes.
- **Network namespace**: Each container has its own IP and ports.
- **Filesystem namespace**: Each container has its own `/` filesystem.
- **Memory/CPU limits**: Each container can be capped to use max X GB RAM, Y CPU cores.

**Result**: Multiple containers on one Host OS, each thinking it's alone.

---

## The Build & Run Workflow

```
1. Write Dockerfile (recipe):
   FROM python:3.10
   COPY app.py /app/
   RUN pip install flask==2.1
   CMD ["python", "app.py"]

2. Build Image: docker build -t myapp:1.0 .
   → Creates a snapshot (layers of changes)

3. Run Container: docker run myapp:1.0
   → Spins up isolated instance from image
```

**Dockerfile** defines how to build the image (the recipe).
**Image** is the packaged snapshot (immutable).
**Container** is the running instance (temporary, can be restarted).

---

## Key Insight

If a developer needs three separate instances of the web app running, they need **three containers**, not three images. All three containers run from the same image.

Similarly, if the app needs to be updated, build a new image (e.g., `myapp:2.0`), then run containers from the new image. Old containers from `myapp:1.0` can coexist.
