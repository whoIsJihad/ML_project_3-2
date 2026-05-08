# Comprehensive Questions: Client-Server, VCS, CI/CD, and API

**Medium to Hard | Scenario-Based & Theory-Based**

---

## CLIENT-SERVER ARCHITECTURE (Questions 1-15)

**1. [Scenario] A social media startup is deciding whether to use a client-server model or have users run the app entirely on their local computers. Which of these is NOT a primary reason to use client-server architecture?**
- A) Centralized data: all user data stored in one place, not scattered across users' devices
- B) Security control: server validates all requests; clients can't bypass security or manipulate data
- C) Data synchronization: millions of users see consistent data across devices (your profile on mobile = desktop)
- D) Reduced server costs: client-server architecture eliminates the need for any backend infrastructure

**2. [Theory] In a client-server architecture, why can't the frontend browser directly query the database, even though it would be faster?**
- A) Browsers don't support database protocols
- B) Security: users could manipulate queries, delete all data, or see private info; the API Server validates all requests
- C) Frontend code is too slow for databases
- D) It's a performance optimization only

**3. [Scenario] A developer builds an e-commerce site with a React frontend. The shopping cart is stored in the user's browser memory. The user refreshes the page. What happens to the cart?**
- A) The cart persists because React saves it
- B) The cart is lost; frontend state is cleared on refresh. To persist, data must be stored in the backend database
- C) The browser automatically downloads it from the server
- D) A backup copy is kept in localStorage forever

**4. [Scenario] Two API Servers serve the same database. User A modifies their profile on Server 1. User B on Server 2 requests the profile. Should they see the updated data?**
- A) No; each server has its own independent data
- B) Yes; both servers connect to the same centralized database, ensuring data consistency
- C) Only if the servers synchronize manually
- D) It depends on the user's internet speed

**5. [Theory] Explain why "static content" (HTML/CSS) is served by the Web Server, while "dynamic content" (personalized data) comes from the API Server:**
- A) They're the same thing; there's no difference
- B) Web Server: unchanging files for all users; API Server: evaluates logic and returns different data per user
- C) Static content is faster, so it's served separately
- D) The Web Server can't handle logic

**6. [Scenario] You deploy a new frontend design (HTML/CSS). All users see it immediately. But you deploy a new backend feature (API endpoint). Not all users see it until they refresh. Why?**
- A) Backend features don't reload automatically
- B) Frontend code is cached in browsers; users have cached the old HTML/CSS. API calls bypass cache and hit the server each time
- C) APIs are slower than frontends
- D) Browsers don't support API calls for new features

**7. [Theory] CDNs (Content Delivery Networks) cache static files geographically near users. Is this a Web Server or API Server function?**
- A) API Server (it serves dynamic content)
- B) Web Server (static files like HTML/CSS/JS can be cached globally). API Servers can't be cached because responses differ per user/time
- C) Both equally
- D) Neither; CDNs are separate systems

**8. [Scenario] A banking app allows users to transfer money using an API endpoint. The client sends: `POST /transfer { amount: -$1000, to: attacker_account }`. Why can't the frontend prevent this alone?**
- A) Frontend validation is impossible
- B) The API Server must validate independently. Frontend code runs on the user's device and can be manipulated; the server is the source of truth
- C) Negative amounts are technically valid
- D) Banks don't use APIs

**9. [Theory] In a three-tier architecture (Client → Web Server → API Server → Database), which tier can be "scaled horizontally" (adding more servers)?**
- A) Only the Database
- B) Only the Web Server
- C) All tiers (load balancing across multiple servers). The Database might use replication/sharding
- D) None; architecture can't be scaled

**10. [Scenario] A mobile app sends an API request to fetch user data. The API response is JSON: `{ "name": "John", "email": "john@example.com" }`. The app crashes due to a logic error. Is this the fault of the API Server?**
- A) Yes; the API sent bad data
- B) No; the API Server provided valid JSON. The frontend app failed to handle the response correctly
- C) Both are equally at fault
- D) The database is responsible

**11. [Theory] Explain the difference between "Where code runs" (execution) and "Where code is stored" (serving):**
- A) They're the same thing
- B) Frontend JS: stored on Web Server, executed in browser. Backend code: stored and executed on API Server. This separation prevents cheating
- C) Code always runs where it's stored
- D) Execution and storage are unrelated

**12. [Scenario] A website uses WebSockets for real-time chat. User A sends a message. User B should see it instantly (not polling every second). Which server must support this?**
- A) The Web Server
- B) The API Server (with WebSocket/real-time push logic). The Web Server only serves static files
- C) Neither can do real-time
- D) The database broadcasts directly

**13. [Scenario] A session token expires while a user is editing a document. Their API requests start failing (auth error). Should the page still display?**
- A) No; nothing works without the API
- B) Yes; the frontend can still display (it's already downloaded). But any action requiring the API will fail, prompting re-login
- C) The browser automatically refreshes the token
- D) Sessions never expire

**14. [Theory] Why must passwords be sent to the API Server (not the Web Server), and why use HTTPS?**
- A) Web Servers can't handle passwords
- B) API Server enforces authentication/authorization logic. HTTPS encrypts the password in transit so it's never exposed
- C) Passwords don't need protection
- D) Web Servers handle password encryption

**15. [Scenario] A company hosts 100 Web Servers but only 5 API Servers (behind a load balancer). Is this a good design? Why or why not?**
- A) No; there should be equal numbers
- B) Possibly yes; static files are easier to scale horizontally. API Servers handle logic and databases, which are bottlenecks
- C) Always yes; more servers is always better
- D) This combination is impossible

---

## VERSION CONTROL SYSTEMS & GIT (Questions 16-30)

**16. [Scenario] Your team has 10 developers. Without VCS, how are they sharing code?**
- A) Emailing .zip files (version conflicts, overwrites, lost work, no history)
- B) Merging code manually by hand-editing files (extremely error-prone)
- C) Both A and B (disaster waiting to happen)
- D) They can't collaborate at all

**17. [Theory] What does "version control" actually control? (Choose the BEST answer)**
- A) Only the current state of code
- B) Every historical change: who changed what, when, and why (through commit messages). Allows reverting bad changes
- C) The versions of libraries your project uses
- D) Just branch names

**18. [Scenario] Developer A commits: `Fix login bug - changed password validation logic`. Developer B commits: `Add password strength requirements - refactored validation`. Both modified the same file. What happens?**
- A) One developer's changes are lost (merge conflict)
- B) Git detects both modified the same file; developers must resolve the merge conflict manually to combine both changes
- C) Both commits are automatically merged
- D) Commits are rejected

**19. [Theory] A team uses a feature branch strategy: `main` branch, and each dev creates `feature/feature-name` branches. What problem does this solve?**
- A) Developers don't need to write tests anymore
- B) Features are isolated; multiple devs can work independently without blocking each other. `main` remains stable
- C) It's slower than committing directly to main
- D) It doesn't solve anything

**20. [Scenario] A developer reverts a commit: `git revert abc123`. The commit is from 5 days ago. Does the entire history disappear?**
- A) Yes; reverting deletes everything
- B) No; revert creates a NEW commit that undoes the changes of abc123. History remains intact (important for audits/debugging)
- C) Only the reverted commit disappears
- D) The file is deleted

**21. [Theory] Git is "distributed" VCS. What does this mean?**
- A) It requires a central server
- B) Every developer has a full copy of the entire repository and history locally. No single point of failure (though most teams use GitHub as the central hub)
- C) Git doesn't work without internet
- D) Distributed means slow

**22. [Scenario] A developer force-pushes (`git push --force`) to delete an accidentally-committed API key. The key is now gone and secure, right?**
- A) Wrong; even after force push, the key is in Git history and can be recovered with `git reflog` or by cloning before the push
- B) Correct; force-pushing removes commits permanently
- C) The key is deleted from the server but still on the developer's computer
- D) API keys can't be committed

**23. [Theory] Explain the difference between `git merge` and `git rebase`:**
- A) They do the same thing
- B) Merge: combines two branches, creates a merge commit, preserves history. Rebase: replays commits on top of another branch, creates a linear history (cleaner but alters history)
- C) Rebase is always better
- D) Merge is for code, rebase is for data

**24. [Scenario] Team A uses `main`, `develop`, and `feature/*` branches. Team B uses only `main`. A bug is discovered in production. Which team can hotfix faster?**
- A) Team B; fewer branches mean less complexity
- B) Team A can create a `hotfix/*` branch off `main`, fix it, and deploy. Team B must interrupt all ongoing work on `main`
- C) Both equally fast
- D) Neither can hotfix

**25. [Theory] What is a "commit" in Git? (Choose the most complete answer)**
- A) Saving a file to disk
- B) A snapshot of all changes (additions/deletions/modifications) with a unique ID, author, timestamp, and message. Forms the chain of history
- C) Uploading code to the server
- D) Deleting old code

**26. [Scenario] A developer's code is reviewed and approved on the PR, but before merging, another developer pushed a conflicting change to `main`. What happens when the reviewer clicks "Merge"?**
- A) It merges automatically
- B) GitHub detects the conflict and blocks the merge until the developer resolves it (rebases/merges to the latest main)
- C) Both changes are somehow combined magically
- D) Merging deletes the earlier change

**27. [Theory] Why should commit messages be descriptive? (e.g., "Fix login validation bug" vs. "fix")**
- A) It's just a convention, doesn't really matter
- B) Descriptive messages help future developers understand WHY changes were made, enable quick audits, and help with bisecting bugs
- C) Short messages are faster to type
- D) Bitbucket requires it

**28. [Scenario] A developer works on a feature for 3 weeks, making 100 commits. Before merging to `main`, they do `git rebase -i` to squash all 100 commits into 1. Benefits? Drawbacks?**
- A) No benefit; wastes time
- B) Benefit: `main` history is cleaner. Drawback: you lose the granularity of small commits (harder to bisect/review if something breaks)
- C) Squashing is always best
- D) Cannot squash commits

**29. [Scenario] Your team requires that `main` branch is protected: PRs require review + all CI checks pass. A developer bypasses this (force-pushes bad code). What's the impact?**
- A) None; force-push is safe
- B) Major: breaks the pipeline, could deploy bad code to production, breaks team trust, violates CI/CD principles
- C) Only affects that developer
- D) The force-push is automatically rejected

**30. [Theory] Compare Git (VCS) with CI/CD. How do they relate?**
- A) They're unrelated
- B) Git tracks code history and changes. CI/CD watches Git changes and automates testing/deployment. Together they enforce code quality
- C) CI/CD doesn't use Git
- D) Git is slower when using CI/CD

---

## CONTINUOUS INTEGRATION / CONTINUOUS DEPLOYMENT (Questions 31-45)

**31. [Scenario] A team without CI/CD: developers push code manually, QA tests later. A critical bug reaches production. How long before it's noticed?**
- A) Immediately (developers are perfect)
- B) Hours or days (QA testing is slow, customers are affected, debugging takes time)
- C) The bug never happens
- D) Within 5 minutes

**32. [Theory] What does "Continuous Integration" guarantee?**
- A) Code is deployed immediately
- B) Code is merged frequently AND tested automatically on every merge. If tests fail, the merge is blocked
- C) Integration with databases only
- D) Continuous updates to dependencies

**33. [Scenario] Developer A's PR passes linting, unit tests, and integration tests. Developer B reviews and approves. The PR is merged to `main`. Seconds later, customers report a bug. How is this possible?**
- A) Should be impossible
- B) Possible: E2E tests weren't run, or a race condition in production under load wasn't caught. CI checks aren't exhaustive
- C) Tests are useless
- D) Customers are always wrong

**34. [Theory] A pipeline has these stages: [Build] → [Unit Tests] → [Integration Tests] → [Deploy]. If Unit Tests fail, should Integration Tests run?**
- A) Yes; independent checks
- B) No; if unit tests fail, the build is broken. No point running integration tests (save time/resources)
- C) Depends on the day
- D) Stages run in parallel always

**35. [Scenario] Your bank's app uses Continuous DEPLOYMENT. A developer introduces a bug that causes transfers to fail. The code passed all tests but breaks in production under real load. What's the impact?**
- A) Customers don't mind buggy banks
- B) Severe; all transfers fail immediately, customers are angry, trust erodes. This is why banks use Continuous DELIVERY (manual approval before production)
- C) The bug is automatically fixed
- D) Deployment doesn't affect production

**36. [Theory] Explain the difference between Continuous Delivery and Continuous Deployment:**
- A) Same thing, different names
- B) Delivery: code passes tests and waits for human approval before production. Deployment: code automatically goes to production after tests pass
- C) Delivery is manual, Deployment is manual (opposite of the names)
- D) Both are fully automated

**37. [Scenario] A code coverage metric shows: "Only 40% of the codebase is tested." What does this mean, and is it a problem?**
- A) 40% of the code runs successfully
- B) 60% of code paths are untested; risky changes could break untested code without detection. Lower coverage = higher risk
- C) The remaining 60% is tested elsewhere
- D) Coverage doesn't matter

**38. [Scenario] A pipeline is rate-limited: it can run 500 times/day. Your team pushes 1000 times/day. What happens?**
- A) All pushes are tested
- B) 500 pushes are tested, the rest are queued or rejected. Developers can't validate code immediately (breaks "fast feedback")
- C) The rate limit increases automatically
- D) Code is pushed regardless of tests

**39. [Theory] Why do API Servers sometimes have a "staging environment" separate from production?**
- A) To have a backup
- B) To test code in a production-like environment (same database structure, similar traffic) before deploying to real customers
- C) It's just a naming convention
- D) Staging and production are the same

**40. [Scenario] A CI pipeline detects a vulnerability in a third-party npm package and blocks the deployment. The package is used in 100 places. What should developers do?**
- A) Ignore the vulnerability
- B) Update the package (if available) or remove the dependency. The pipeline prevented a potential security breach in production
- C) Manually overwrite the security check
- D) Vulnerabilities can't be detected

**41. [Theory] A company has 10 servers in its CI system. Servers 1-5 build code, Servers 6-10 run tests. Is this a good distribution?**
- A) No; build is fast, tests are slow. You should have more test servers
- B) Possibly; it balances resources. But ideal distribution depends on your bottleneck (monitoring will show)
- C) Both are equally fast always
- D) Number of servers doesn't matter

**42. [Scenario] A developer's code fails the "security scanning" stage of the pipeline. The scan detected a hardcoded API key. They delete the commit. Is the key now safe?**
- A) Yes; it's deleted
- B) No; even after deletion, the key was in Git history and could be recovered. It must be rotated (disabled) ASAP. This is why scanning is important
- C) Keys can't be found in history
- D) Scanning prevents this entirely

**43. [Theory] Explain what happens when a pipeline stage is marked "allow-failure":**
- A) The stage shouldn't be there
- B) If that stage fails, the pipeline continues (not blocked). Useful for non-critical checks like linting or optional tests
- C) The entire pipeline fails
- D) It's a random stage

**44. [Scenario] Your API Server is deployed hourly via CD. Which of the following MUST be true?**
- A) UI changes must also deploy hourly
- B) Each deployment must be safe to rollback. Database migrations must be backwards-compatible, feature flags should hide incomplete features
- C) Users see downtime hourly
- D) CD is impossible

**45. [Theory] Compare manual deployment vs. CD. What's the value of CD?**
- A) Manual deployment is faster
- B) CD: automated, consistent, frequent, auditable. Manual: slow, error-prone, scary (developers fear deployments)
- C) Both are equally risky
- D) Manual allows more testing

---

## APIs & INTEGRATION (Questions 46-60)

**46. [Scenario] A mobile app makes an API request to fetch user profile. The request says: `GET /user/123`. The developer adds query params: `GET /user/123?include=payments&filter=recent`. What's the purpose?**
- A) Confusing the API
- B) Customizing the response: request payload, permissions, filtering. Good APIs are flexible
- C) These params do nothing
- D) Only GET requests support params

**47. [Theory] An API uses REST. What does this mean?**
- A) The API is lazy
- B) Resources are identified by URLs (e.g., `/users/123` = user with ID 123). HTTP methods indicate actions (GET=read, POST=create, PUT=update, DELETE=remove)
- C) REST is a data format
- D) REST is the only API style

**48. [Scenario] A third-party API (like Stripe for payments) limits your app to 1000 requests/second. Your app makes 5000 requests/second during peak load. What happens?**
- A) All requests go through
- B) Requests beyond 1000/sec are rate-limited: queued, delayed, or rejected (429 error). Your API must handle backoff/retry logic
- C) Stripe upgrades your limit automatically
- D) Rate-limiting is impossible

**49. [Theory] API versioning: old API returns v1, new API returns v2. Why have versions instead of replacing old with new?**
- A) To confuse developers
- B) Old versions might be used by mobile apps in the wild (can't force immediate updates). Supporting versions prevents breaking production apps
- C) Versions serve no purpose
- D) All APIs are version 1

**50. [Scenario] An API returns JSON with a timestamp: `{ "created_at": "2025-03-30T10:00:00Z" }`. The client's timezone is PST (UTC-7). Should the client convert this?**
- A) No; always work in UTC internally. Convert to local timezone only for display
- B) Yes; the API provides UTC, so convert for accuracy (servers always give UTC)
- C) Times are relative to the user
- D) Timezone conversion is impossible

**51. [Theory] An API endpoint is "idempotent" if calling it twice gives the same result as calling it once. Which HTTP method should be idempotent?**
- A) POST is always idempotent
- B) GET, PUT, DELETE should be idempotent. POST typically isn't (creates a new resource each time)
- C) None are idempotent
- D) Idempotence is a myth

**52. [Scenario] An API requires authentication: pass a token in the `Authorization` header. Should you commit the token in code?**
- A) Yes; it's convenient
- B) No; tokens should be in environment variables (not version-controlled). Accidental commits leak credentials
- C) Tokens don't exist in production
- D) Version control is safe for tokens

**53. [Theory] What is API rate-limiting?**
- A) Limiting customer reviews
- B) Restricting requests per user/IP per time period (e.g., 100 requests/minute). Prevents abuse and ensures fair resource usage
- C) Limiting the number of APIs
- D) Rate limits don't exist

**54. [Scenario] An API returns status code 200 (success) but the `response.ok` field is false. How should the client interpret this?**
- A) The request succeeded
- B) The HTTP status is 200, but the business logic failed (e.g., bad input). Client must check BOTH HTTP status AND response.ok
- C) Status 200 always means success
- D) Response fields don't matter

**55. [Theory] Why should APIs return consistent error responses?**
- A) Errors are irrelevant
- B) Clients expect a predictable error format (e.g., `{ "error": "...", "code": "..." }`). Inconsistency breaks client error handling
- C) Errors should be random
- D) All APIs error differently

**56. [Scenario] An API client retries a failed request (due to timeout). If the original request already succeeded on the server, retrying will create a duplicate. How do you prevent this?**
- A) Never retry
- B) Use idempotent requests with unique IDs. Server tracks IDs; duplicate requests are ignored
- C) Duplicates are acceptable
- D) Timeouts don't happen

**57. [Theory] CORS (Cross-Origin Resource Sharing): a frontend on `example.com` calls an API on `api.example.com`. Should this be allowed?**
- A) Never; different domains shouldn't communicate
- B) Only if the API explicitly allows it via CORS headers. This prevents scripts on malicious domains from accessing your API
- C) Always allowed
- D) CORS is a myth

**58. [Scenario] Your API response is large (100MB). Should you compress it?**
- A) No; size doesn't matter
- B) Yes; use gzip compression (server compresses, client decompresses). Saves bandwidth, faster transmission
- C) Compression makes it slower
- D) 100MB is small

**59. [Theory] An API uses pagination: `GET /items?page=1&limit=10` returns 10 items. What's the benefit over returning ALL items at once?**
- A) No benefit; return everything
- B) Pagination reduces memory usage, faster responses, and better UX (user sees results quickly). All-at-once is infeasible for millions of items
- C) Pagination is slower
- D) APIs don't support pagination

**60. [Scenario] An API documentation says: "This endpoint returns 10,000 results." A developer assumes the API returns all data in a single request. In production, the request times out and crashes. What's the issue?**
- A) The API is broken
- B) The documentation is misleading; 10,000 results should be paginated. The developer didn't test with realistic load
- C) Timeouts are impossible
- D) Developers don't need to read documentation

---

## CONTAINERIZATION & DOCKER (Questions 61-75)

**61. [Scenario] A developer builds a Python app on Ubuntu 22.04 with Python 3.10 and Flask 2.1. When deployed to production (Ubuntu 20.04 with Python 3.8, Flask 1.9), it breaks. Why?**
- A) Production servers are fundamentally different and can't run the same code
- B) The dependency stack doesn't match: OS, runtime, and libraries differ. "It works on my machine" but not in production
- C) The code is broken
- D) This scenario is impossible

**62. [Theory] Explain the three-layer stack in software deployment:**
- A) Frontend, Backend, Database
- B) Application Code → Libraries/Dependencies (with versions) → Operating System. Each layer's version matters
- C) Build, Test, Deploy
- D) Client, Server, Cloud

**63. [Scenario] A Docker Image is created with Python 3.10, Flask 2.1, and the app code. This image is deployed to 5 different servers with different OSes. What happens?**
- A) The app breaks on different OSes
- B) The app runs identically on all 5 servers. The image "freezes" all dependencies and OS config (read-only snapshot)
- C) Only one server works at a time
- D) Docker Images can only work on one OS

**64. [Theory] What's the primary difference between a Docker Image and a Docker Container?**
- A) They're the same thing
- B) Image: read-only snapshot (blueprint). Container: running instance of an image. One image can spawn multiple containers
- C) Image is for testing, Container is for production
- D) Containers are older than Images

**65. [Scenario] You need to run three separate instances of your web app on the same server, all processing requests independently. Do you need three different Images or three different Containers?**
- A) Three different Images (one per instance)
- B) Three different Containers from the same Image (containers are instances; image is the template)
- C) You can't run multiple instances
- D) One Image and one Container (they scale automatically)

**66. [Theory] Compare Containers with Virtual Machines. Why are containers more efficient?**
- A) Containers are faster because they use better hardware
- B) VMs require a full Guest OS per app (heavy). Containers share the Host OS kernel via namespaces (light). Containers = faster, smaller, cheaper
- C) Containers and VMs are equally efficient
- D) VMs are always better

**67. [Scenario] You have a Dockerfile that specifies Python 3.10 and Flask 2.1. You build the image. A month later, you build it again from the same Dockerfile. Will the new image have different versions of Python/Flask?**
- A) Yes; versions update automatically
- B) No; layers are cached. Same Dockerfile = same image (unless you force a rebuild). Pin versions in Dockerfile to ensure reproducibility
- C) Images can't be rebuilt
- D) Version updates happen randomly

**68. [Theory] What do Docker namespaces accomplish?**
- A) They organize code files
- B) Isolate processes, network, filesystem, memory between containers. Container 1 with Python 3.10 and Container 2 with Python 3.11 don't interfere
- C) They're just names for containers
- D) Namespaces are for databases

**69. [Scenario] Container A runs on port 8080 inside its isolated network namespace. Container B also runs on port 8080. Do they conflict?**
- A) Yes; both are on port 8080
- B) No; each container has its own isolated port namespace. Externally, map them to host ports 8080 and 8081
- C) Only the first container works
- D) Containers can't use the same port

**70. [Theory] What is the Dockerfile?**
- A) The running container
- B) A recipe/instructions for building an image (specifies base OS, dependencies, code to copy, startup command)
- C) A log of container changes
- D) A backup of the application

**71. [Scenario] A developer updates the app code, rebuilds the image to v2.0, and runs a container from v2.0. The old container from v1.0 is still running. Can they coexist?**
- A) No; old containers must be deleted
- B) Yes; they're separate instances from different images. v1.0 containers continue running, v2.0 containers run in parallel (useful for gradual rollouts)
- C) Both containers must use the same image
- D) Only the newest image can run

**72. [Scenario] A company deploys a Python app in a container. Months later, a critical vulnerability is discovered in Python 3.10. Should they patch the running container or rebuild the image?**
- A) Patch the running container (quick fix)
- B) Rebuild the image with patched Python 3.10, then deploy new containers. Leaving old containers running is risky; immutable infrastructure is safer
- C) The vulnerability doesn't affect containers
- D) Containers can't be updated

**73. [Theory] Docker Images consist of multiple layers. Why layers instead of one monolithic file?**
- A) It's just a design choice
- B) Layers enable caching and reusability. If you rebuild an image with a small code change, unchanged layers are reused (faster). Many images share base OS layers
- C) Layers are just for organization
- D) All layers are independent

**74. [Scenario] A Docker image is 2 GB. You run 10 containers from it on the same server. Do you use 20 GB of disk?**
- A) Yes; 10 containers × 2 GB = 20 GB
- B) No; the image is read-only; all containers share it. Only changes within running containers use extra space (copy-on-write). Total ≈ 2 GB + small overhead
- C) Docker uses infinite disk
- D) Disk usage is random

**75. [Scenario] A developer uses containers locally for testing. The app runs perfectly. In production (same container image), it fails. What's the likely cause?**
- A) Containers don't work in production
- B) Environment differences: the container is identical, but the HOST environment might differ (network, mounted volumes, resource limits, secrets/API keys). Not a container issue; check host config
- C) Containers are unreliable
- D) Impossible scenario

---

## BONUS: INTEGRATED SCENARIOS (Questions 76-80)

**76. [Full Stack] A company releases a feature via CD (every push = production). A critical bug is discovered after 1000 deployments. How do you quickly know the exact commit that introduced the bug?**
- A) Review all 1000 commits manually
- B) Use Git bisect: binary search through commits to find the breaking change. CI tests each commit automatically
- C) Bugs can't be tracked
- D) Revert all 1000 commits

**77. [Full Stack] Your frontend makes an API call. The response is slow (3 seconds). Where could the bottleneck be?**
- A) Only the frontend
- B) Network latency, Web Server response time, API Server processing, Database query time, or a combination. Must profile each layer
- C) Only the API
- D) Bottlenecks can't be found

**78. [Full Stack] A team uses Git + CI/CD + protected main branch. A developer's PR fails a test, but they force-push to bypass the protection. What's the consequence?**
- A) None; force-push is allowed
- B) Critical: bad code reaches production, system breaks, CI trust is broken. Team process is compromised, must be audited
- C) The force-push is magic
- D) No consequences

**79. [Full Stack] Your app has: React (frontend), Node.js (API), PostgreSQL (database). Are these components "loosely coupled"? Why?**
- A) No; they're extremely dependent on each other
- B) Loosely coupled: frontend communicates ONLY via API (standard interface). Database is hidden. Easy to swap any layer (frontend, backend, DB) independently
- C) Coupling is irrelevant
- D) They should be tightly coupled

**80. [Scenario] A startup has 2 developers and 100 users. Should they invest in CI/CD?**
- A) No; too small
- B) Yes; CI/CD scales from 2 developers to 200. Automation saves time even at small scale, prevents bad code from reaching customers, is foundational as the team grows
- C) CI/CD is only for big companies
- D) Manual testing is fine forever

---

## ADDITIONAL QUESTIONS (Questions 81-90)

**81. [Theory] In a client-server architecture, why is the API Server considered the "source of truth" for data?**
- A) It's just a naming convention
- B) The API Server validates all requests and enforces business rules. Frontend data can be stale/manipulated, but the server's database is the authoritative source
- C) Clients are more reliable than servers
- D) The source of truth is always the client

**82. [Scenario] A developer creates a Git branch `feature/payment-system`, makes 50 commits, then opens a PR. The PR shows 50 commits. Is this good practice?**
- A) Yes; more commits = more detailed history
- B) Debatable; many small commits clutter history. Before merging, consider squashing related commits into fewer, logical units (but keep history detailed for review)
- C) Always squash to 1 commit
- D) Commit count doesn't matter

**83. [Theory] Explain why database transactions are critical in a multi-server backend architecture:**
- A) They improve performance
- B) Transactions ensure atomicity: either ALL changes succeed or NONE do. Without them, partial updates can corrupt data when servers/network fail mid-operation
- C) Transactions are optional
- D) Only single-server systems need transactions

**84. [Scenario] Your containerized app works perfectly locally but fails in the Kubernetes cluster (production). You're using the exact same Docker image. What's the most likely cause?**
- A) Containers don't work in Kubernetes
- B) Environment variables, secrets (API keys), resource limits (CPU/memory), or networking config differ between local and cluster. The container image is identical; host environment is different
- C) Kubernetes is broken
- D) The Docker image changed

**85. [Theory] In API design, what does a "409 Conflict" status code indicate?**
- A) The server crashed
- B) The request conflicts with current state (e.g., updating a deleted resource, or version mismatch). Client must refresh and retry
- C) The API is under maintenance
- D) 409 doesn't exist

**86. [Scenario] A team implements Git hooks that block commits with hardcoded secrets (passwords, API keys). A developer disables the hook and commits a secret anyway. What should happen?**
- A) Nothing; hooks are just suggestions
- B) The CI pipeline should catch it during security scanning and block the merge. If it reaches production, the secret is compromised and must be rotated immediately
- C) Developers are trusted; no need to scan
- D) Secrets can't be detected automatically

**87. [Theory] Load balancers at the application layer (L7) can make routing decisions based on request content. When would this be better than network-layer (L4) load balancing?**
- A) L4 is always better
- B) L7 is useful when routing depends on URL path, headers, or domain (e.g., `/api/users` → API service, `/images/*` → CDN). L4 can't inspect content, only IP/port
- C) L7 and L4 are identical
- D) Routing doesn't depend on content

**88. [Scenario] A team enforces that all API endpoints must support pagination. An endpoint returns 100,000 items by default. Is forcing pagination here beneficial?**
- A) No; 100,000 items at once is fine
- B) Yes; prevents memory exhaustion, timeout errors, and poor UX. Pagination forces thinking about scale, even if most users request tiny pages
- C) Pagination is only for large datasets
- D) Users should handle large responses

**89. [Theory] In Docker, what is a "dangling image"?**
- A) An image that's moving slowly
- B) An image with no tags or containers referencing it (orphaned). Safe to delete; it wastes disk space.
- C) An image that's broken
- D) All images dangle by design

**90. [Full Stack] A distributed system has: Web Servers (stateless), API Servers (stateless), and Database (central). A network partition temporarily splits the data center. Web Servers can't reach API Servers. What should happen?**
- A) Web Servers automatically fix the network
- B) Web Servers should return an error (5xx - service unavailable). Alternatively, serve cached static pages. Important: don't return stale/incorrect data
- C) Web Servers ignore the error and respond normally
- D) Partitions can't happen
