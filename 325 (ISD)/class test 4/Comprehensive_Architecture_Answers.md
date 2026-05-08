# Answer Key: Comprehensive Architecture Questions

---

## CLIENT-SERVER ARCHITECTURE (Answers 1-15)

| Q | Answer | Explanation |
|---|--------|-------------|
| 2 | B | Direct database access = users could craft queries to delete/modify data, see other users' private info. API validates all requests and enforces authorization |
| 3 | B | Frontend state (browser memory) is cleared on page refresh. Data must be persisted in the backend database, not just client-side |
| 4 | B | Both API Servers connect to the same centralized database = users see consistent data regardless of which server answered their request |
| 5 | B | Web Server: delivers unchanging files (HTML/CSS) to all users identically. API Server: evaluates business logic and returns different data per user (dynamic) |
| 6 | B | Frontend code is cached in browsers; refresh gets the cached version. API calls bypass cache and hit the server fresh each time |
| 7 | B | CDNs cache static files (HTML/CSS/JS). API responses vary per user/time and can't be cached globally. Web Server function |
| 8 | B | API Server is the source of truth and must validate independently. Frontend code runs on user's device and can be manipulated (client-side validation is easily bypassed) |
| 9 | C | All layers can be scaled horizontally (multiple Web Servers behind load balancer, multiple API Servers, Database replication/sharding) |
| 10 | B | API Server provided valid JSON. The app's logic failed to handle the response. API is not responsible for how clients consume its data |
| 11 | B | Frontend JS is stored on Web Server but executes in the browser. Backend code is stored AND executed on API Server. This separation prevents users from cheating |
| 12 | B | WebSockets require persistent, two-way communication. Web Server typically serves static files only. API Server handles real-time logic |
| 13 | B | Frontend is already downloaded; can display. But API requests fail (auth error), so actions requiring the API will fail, prompting re-login |
| 14 | B | API Server validates credentials and enforces authentication/authorization rules. HTTPS encrypts the password so it's never exposed in transit |
| 15 | B | Static files are easier to scale horizontally (just serve the same files). API Servers handle logic/databases (the actual bottleneck), so fewer API Servers makes sense |

---

## VERSION CONTROL SYSTEMS & GIT (Answers 16-30)

| Q | Answer | Explanation |
|---|--------|-------------|
| 16 | C | Emailing .zip files = version conflicts, overwrites, lost work. Manual merging = extremely error-prone. Both are disasters |
| 17 | B | Version control tracks every historical change: who changed what, when, and why (commit messages). Enables reverting bad changes and auditing |
| 18 | B | Git detects the merge conflict; developers must manually resolve it (choose both, one, or a custom merge) to combine changes |
| 19 | B | Feature branches isolate work; multiple devs can work independently without blocking each other. `main` remains stable for production deployments |
| 20 | B | `git revert` creates a NEW commit that undoes the changes. History remains intact (critical for audits, debugging, and recovering from mistakes) |
| 21 | B | Distributed = every developer has a full copy of the repository locally. No single point of failure (though teams often use GitHub as the central hub) |
| 22 | A | Force-push doesn't permanently delete. Git history can be recovered with `git reflog` or by cloning before the push. Key should be rotated ASAP |
| 23 | B | Merge: combines branches, creates merge commit, preserves all history (visual record of merges). Rebase: replays commits linearly (cleaner but alters history) |
| 24 | B | Team A can create a `hotfix/*` branch off `main`, fix it, deploy fast. Team B must interrupt all work on `main` (context switching, delays) |
| 25 | B | Commit = snapshot of all changes with unique ID, author, timestamp, message. Forms the immutable chain of history |
| 26 | B | GitHub detects the conflict and blocks the merge until the developer rebases/merges to the latest main and resolves conflicts |
| 27 | B | Descriptive messages enable future developers to understand WHY changes were made, quick audits, and `git bisect` for finding breaking commits |
| 28 | B | Benefit: cleaner main history. Drawback: lose granularity of small commits (harder to bisect if break happens in the 1 squashed commit) |
| 29 | B | Force-push breaks the pipeline, could deploy bad code, erodes CI/CD trust, violates team process. Major incident |
| 30 | B | Git tracks code history and changes. CI/CD watches Git changes, automates testing/deployment. Together they enforce code quality |

---

## CONTINUOUS INTEGRATION / CONTINUOUS DEPLOYMENT (Answers 31-45)

| Q | Answer | Explanation |
|---|--------|-------------|
| 31 | B | Without CI: QA tests hours/days later. Bug has already impacted customers. Manual testing is slow and inconsistent |
| 32 | B | CI guarantees: code is merged frequently + tested automatically. If tests fail, merge is blocked. Prevents bad code from reaching main |
| 33 | B | E2E tests not run, race conditions under production load not caught, caching issues. CI checks are comprehensive but not exhaustive |
| 34 | B | Failed Unit Tests = broken code. No point running Integration Tests (save time/resources). Pipeline should fail fast |
| 35 | B | Continuous DEPLOYMENT = all changes auto-deploy. A bug breaks all transfers immediately. Banks use Continuous DELIVERY (manual approval layer) |
| 36 | B | Delivery: waits for human approval. Deployment: automatically goes to production. Different risk profiles |
| 37 | B | 40% coverage = 60% of code is untested. Risky; untested code changes can break without detection |
| 38 | B | 500 requests tested, 500 queued/rejected. Developers can't validate code immediately (breaks fast feedback principle) |
| 39 | B | Staging mirrors production structure but separate. Allows testing in production-like environment before impacting real customers |
| 40 | B | Pipeline prevented a security breach in production. Developers must update the package or remove the dependency |
| 41 | A | Build is fast, tests are slow. More test servers = faster feedback. Distribution depends on your bottleneck (use monitoring) |
| 42 | B | Key was in Git history and recoverable. Must be rotated/disabled immediately. Security scanning prevents this by detecting hardcoded secrets |
| 43 | B | "allow-failure" allows non-critical checks to fail without blocking deployment. Useful for linting, optional tests |
| 44 | B | Each deployment must be safely rollbackable. Database migrations must be backwards-compatible. Feature flags hide incomplete features |
| 45 | B | CD: automated, consistent, frequent, auditable. Manual: slow, error-prone, scary (developers fear deployments cause bugs) |

---

## APIs & INTEGRATION (Answers 46-60)

| Q | Answer | Explanation |
|---|--------|-------------|
| 46 | B | Query params customize the response: request only specific fields, apply filters, set limits. Good APIs are flexible |
| 47 | B | REST: resources identified by URLs (e.g., `/users/123`). HTTP methods indicate actions (GET=read, POST=create, PUT=update, DELETE=remove) |
| 48 | B | Requests beyond 1000/sec receive 429 (Too Many Requests). Client must implement exponential backoff/retry logic |
| 49 | B | Old versions used by mobile apps (can't force immediate updates). Supporting multiple versions prevents breaking production apps |
| 50 | A | Always work in UTC internally. Convert to local timezone only for display (prevents timezone bugs) |
| 51 | B | GET, PUT, DELETE should be idempotent (calling 10 times = calling 1 time). POST typically isn't (creates new resource each time) |
| 52 | B | Tokens should be in environment variables, not version-controlled. Accidental commits leak credentials (and Git history is public) |
| 53 | B | Rate-limiting: restrict requests per user/IP per time period (e.g., 100/minute). Prevents abuse, ensures fair resource usage |
| 54 | B | HTTP 200 = request succeeded syntactically. But `response.ok: false` = request succeeded, but business logic failed. Check BOTH |
| 55 | B | Consistent error format (e.g., `{ "error": "...", "code": "..." }`) lets clients handle errors reliably. Inconsistency breaks logic |
| 56 | B | Idempotent requests with unique IDs. Server tracks IDs; duplicate requests are silently ignored. Prevents duplicate-payment bugs |
| 57 | B | CORS allows API to specify which domains can access it. Prevents malicious domains from stealing data or performing actions |
| 58 | B | gzip compression: server compresses, client decompresses. Saves bandwidth, faster transmission |
| 59 | B | Pagination reduces memory, speeds responses, improves UX (user sees results quickly). All-at-once is infeasible for millions of items |
| 60 | B | Documentation misleading; 10,000 items should be paginated. Developer didn't test with realistic load. Timeout crashes the app |

---

## CONTAINERIZATION & DOCKER (Answers 61-75)

| Q | Answer | Explanation |
|---|--------|-------------|
| 61 | B | OS versions, runtime versions, and library versions all differ. Docker solves this by packaging all three layers into an immutable image |
| 62 | B | Code → Libraries/Dependencies (with specific versions) → Operating System. Each layer's version combination matters |
| 63 | B | Image is a read-only snapshot. All 5 servers run identical code/OS/dependencies. No "it works on my machine" problem |
| 64 | B | Image = blueprint/recipe (immutable snapshot). Container = running instance of an image. Same image creates multiple containers |
| 65 | B | Three containers from the same image. Image is the template; containers are instances. If you need 100 instances, one image, 100 containers |
| 66 | B | VMs require full Guest OS per app (heavy). Containers share Host OS kernel via namespaces (light). Containers = faster startup, smaller footprint, cheaper |
| 67 | B | Docker layers are cached. Same Dockerfile = same image. But if base image is pulled fresh, versions may update. Pin versions in Dockerfile to ensure reproducibility |
| 68 | B | Namespaces isolate: processes (PID), filesystem (mount), network (IP/ports), memory/CPU. Containers think they're alone but share Host OS kernel |
| 69 | B | Each container has isolated port namespace. Both can use 8080 internally. Map to Host ports 8080 and 8081 externally (no conflict) |
| 70 | B | Dockerfile = recipe for building an image. Specifies: base OS, dependencies to install, code to copy, startup command |
| 71 | B | Containers are instances. v1.0 and v2.0 containers coexist (useful for gradual rollouts, canary deployments, A/B testing) |
| 72 | B | Rebuild image with patched Python, deploy new containers. Old containers continue running without patch (risky). Immutable infrastructure = safety |
| 73 | B | Layers enable caching and reusability. Small code change? Reuse unchanged layers. Many images share same base OS layers (saves space, build time) |
| 74 | B | Image is read-only; containers share it. Only container-specific changes use extra space (copy-on-write). 10 containers ≈ 2 GB + overhead (not 20 GB) |
| 75 | B | Container is identical; Host environment differs (network config, mounted volumes, resource limits, secrets). Not a container problem; check host setup |

---

## BONUS: INTEGRATED SCENARIOS (Answers 76-80)

| Q | Answer | Explanation |
|---|--------|-------------|
| 76 | B | `git bisect`: binary search through commits (find breaking change in log2(1000) ≈ 10 git commands). CI tests each commit automatically |
| 77 | B | Bottleneck could be anywhere: network latency, Web Server response, API processing, DB query. Must profile each layer with tools (Network tab, APM) |
| 78 | B | Force-push bypasses protection, breaks CI trust. Bad code reaches production, system breaks. Major incident requiring audit |
| 79 | B | Loosely coupled: frontend knows only the API interface (not DB structure). Easy to swap any layer independently without breaking others |
| 80 | B | Even 2 devs benefit: automation prevents bad code reaching customers, saves time, foundational as team grows to 200 developers |

---

## Summary Statistics

- **Total Questions**: 80
- **Scenario-Based**: ~42 questions
- **Theory-Based**: ~33 questions
- **Full-Stack Integrated**: 5 questions
- **Topics**: Client-Server (15), VCS/Git (15), CI/CD (15), APIs (15), Containerization (15), Integrated (5)
- **Difficulty**: Medium-to-Hard (requires application of concepts, not just memorization)
