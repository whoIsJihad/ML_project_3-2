# Better Architecture Questions: Practice Version (No Answers)

High quality practice set with balanced options.

---

## CLIENT-SERVER ARCHITECTURE (1-10)

1. A social app has users in many cities. Why keep profile data on a central server?
- A) It removes the need for backups
- B) It makes login optional for users
- C) It keeps one shared state across devices
- D) It guarantees zero latency globally

2. Why should browsers call an API instead of querying SQL directly?
- A) Browsers can only read CSV files
- B) API can enforce auth and validation rules
- C) SQL works only on localhost networks
- D) Databases reject all browser requests by design

3. A cart stored only in memory disappears after refresh. Best fix?
- A) Save cart state in backend storage
- B) Increase browser cache size manually
- C) Disable refresh with JavaScript alerts
- D) Move checkout to static HTML pages

4. Two API instances read the same database. User A updates a record. User B reads from another API instance. Expected result?
- A) User B sees older data until midnight
- B) User B sees updated data if commit succeeded
- C) User B sees random data due to replication lag
- D) User B must query both instances first

5. Which statement best separates Web Server and API Server responsibilities?
- A) Web serves static assets; API serves computed data
- B) Web handles payments; API handles CSS files
- C) Web stores sessions; API stores images only
- D) Web and API roles are always identical

6. Why can frontend validation never be your only defense?
- A) Users can modify client code and requests
- B) Browsers auto-correct invalid payloads
- C) HTML forms encrypt all input by default
- D) Local storage blocks malicious users

7. When is CDN caching most appropriate?
- A) Personalized account balances
- B) Per-user notification counts
- C) Shared static assets like images and JS
- D) Short-lived OTP verification responses

8. In a three-tier system, which tier usually enforces business rules?
- A) Browser extension layer
- B) API/application layer
- C) DNS resolver layer
- D) CDN edge cache layer

9. A session token expires while editing a draft. What should happen?
- A) Browser silently bypasses auth checks
- B) App keeps editing and syncs later without auth
- C) UI stays visible but protected actions fail
- D) Entire page binary crashes immediately

10. Why is HTTPS critical for login APIs?
- A) It lowers compute usage on all servers
- B) It hides packet size from all observers
- C) It removes need for password hashing
- D) It encrypts credentials in transit

---

## GIT & VERSION CONTROL (11-20)

11. What is the main value of version control in teams?
- A) Automatic bug fixing in production
- B) Shared history and safe collaboration
- C) Elimination of merge conflicts forever
- D) Removal of code review needs

12. Two branches changed the same lines differently. On merge, Git will:
- A) Pick newer commit without warning
- B) Delete both versions automatically
- C) Raise a conflict for manual resolution
- D) Force a rebase to remote main

13. Why use feature branches?
- A) To avoid writing commit messages
- B) To isolate work before integration
- C) To make pull requests unnecessary
- D) To replace testing pipelines entirely

14. What does git revert do to history?
- A) Erases old commits permanently
- B) Rewrites all commit hashes after target
- C) Creates a commit that undoes changes
- D) Deletes remote branch protection rules

15. Why is force-pushing risky on shared branches?
- A) It can rewrite published history
- B) It disables all repository webhooks
- C) It compresses files irreversibly
- D) It blocks clone operations globally

16. Best reason to write meaningful commit messages?
- A) They improve runtime performance
- B) They help audits and debugging later
- C) They reduce repository size significantly
- D) They remove need for issue trackers

17. Merge vs rebase: which is accurate?
- A) Rebase preserves merge graph as-is
- B) Merge rewrites commit authorship data
- C) Merge can add merge commit; rebase rewrites
- D) Both always create identical history

18. Why protect main branch with required checks?
- A) To speed up local development loops
- B) To block unverified code from merging
- C) To prevent creating any new branches
- D) To hide commit history from reviewers

19. A leaked API key was committed, then deleted in a later commit. Correct response?
- A) Do nothing; deletion is sufficient
- B) Rotate key and clean history if needed
- C) Rename repository to invalidate key
- D) Archive branch to stop all access

20. What does distributed VCS mean in Git?
- A) Only maintainers have full history
- B) Remote stores all history; local is partial
- C) Every clone has full commit history
- D) Commits require internet to complete

---

## CI/CD (21-30)

21. Continuous Integration primarily means:
- A) Auto-deploy every successful commit
- B) Frequent merges with automated checks
- C) Manual testing at release time only
- D) Nightly cron-based integration only

22. Pipeline stage order is Build -> Unit -> Integration -> Deploy. Unit tests fail. Best behavior?
- A) Continue to integration for extra data
- B) Skip deploy but run integration anyway
- C) Stop early to save time and cost
- D) Deploy to staging and observe failures

23. Why keep a staging environment?
- A) To replace production completely
- B) To test in production-like conditions
- C) To avoid writing integration tests
- D) To reduce monitoring requirements

24. Continuous Delivery vs Continuous Deployment?
- A) Delivery requires approval before prod
- B) Deployment requires approval before prod
- C) Both require approval by definition
- D) Neither can use automated testing

25. A PR passes tests but fails under real traffic. Most likely reason?
- A) CI tools cannot run shell commands
- B) Tests missed load or race scenarios
- C) Git hooks were not installed locally
- D) Branch naming was non-standard

26. What does allow-failure on a job imply?
- A) Pipeline ignores all future failures
- B) Failing job can be non-blocking
- C) Job reruns until it passes automatically
- D) Job runs only on release branches

27. Why enforce security scanning in CI?
- A) It replaces all code review needs
- B) It catches vulnerable dependencies/secrets
- C) It increases compile speed dramatically
- D) It prevents merge conflicts always

28. A team pushes faster than pipeline capacity. Primary impact?
- A) Faster feedback for every developer
- B) Queue buildup and delayed validation
- C) Automatic scale with no extra setup
- D) Guaranteed zero flaky test rate

29. Safe frequent deployment requires:
- A) Backward-compatible migrations and rollback
- B) Disabling alerts during deploy window
- C) Manual SSH edits on live servers
- D) Single-server architecture only

30. Biggest benefit of CD over manual release?
- A) Fewer commits in repository history
- B) Higher consistency and auditability
- C) Zero need for incident response
- D) No requirement for monitoring

---

## APIs (31-40)

31. REST endpoint GET /users/42 means:
- A) Create user with id 42
- B) Delete user with id 42
- C) Read resource users with id 42
- D) Replace users collection entirely

32. API returns HTTP 200 but body includes {ok:false}. Correct interpretation?
- A) Transport succeeded; business rule failed
- B) Client must treat as network timeout
- C) Server ignored request completely
- D) HTTP status is irrelevant to clients

33. Rate limit exceeded. Best client behavior?
- A) Retry immediately in tight loop
- B) Switch to random endpoint paths
- C) Exponential backoff and retry later
- D) Open parallel sessions to bypass cap

34. Why avoid committing API tokens in code?
- A) Tokens break JSON formatting rules
- B) Secrets in history can be abused
- C) Repositories cannot store strings safely
- D) CI systems reject all environment vars

35. Why store timestamps in UTC on server side?
- A) It avoids timezone conversion everywhere
- B) It removes daylight saving changes globally
- C) It provides one canonical time reference
- D) It lets clients skip locale formatting

36. Idempotency key is most useful for:
- A) Caching static files in browser
- B) Preventing duplicate side effects on retries
- C) Encrypting payloads without TLS
- D) Generating globally unique usernames

37. Why do APIs return structured error objects?
- A) To make logs shorter than plain text
- B) To let clients handle errors predictably
- C) To force browsers to show alerts
- D) To bypass status code handling

38. Pagination is preferred because it:
- A) Reduces payload size and memory pressure
- B) Guarantees lower total query count
- C) Removes need for database indexes
- D) Prevents all timeout errors entirely

39. Why keep API versions (v1, v2) in production?
- A) To avoid writing API documentation
- B) To support old clients during migration
- C) To reduce TLS certificate overhead
- D) To make endpoint names shorter

40. CORS policy exists mainly to:
- A) Compress API responses by origin
- B) Control cross-origin browser access
- C) Replace authentication tokens fully
- D) Speed up DNS lookups globally

---

## DOCKER & CONTAINERS (41-50)

41. Docker image vs container: correct statement?
- A) Image runs; container is template
- B) Image is template; container runs
- C) Both are temporary runtime states
- D) Both are immutable file archives

42. Why do containers start faster than VMs?
- A) They skip all networking setup
- B) They share host kernel instead of full guest OS
- C) They avoid filesystem operations entirely
- D) They compile application code at runtime

43. Same image on different hosts behaves differently. Likely cause?
- A) Host config/env differences
- B) Image hash changed by itself
- C) Container ignores host networking
- D) Docker daemon rewrites app code

44. Why pin dependency versions in Dockerfile?
- A) To maximize random upgrades
- B) To improve reproducibility across builds
- C) To reduce image layer count to one
- D) To disable package manager checks

45. Multiple containers from one image use disk how?
- A) Full image duplicated per container
- B) Shared base layers plus writable diffs
- C) No disk usage after first run
- D) Random usage depending on hostname

46. What problem do namespaces solve?
- A) Isolate process/network/filesystem views
- B) Encrypt container files at rest
- C) Replace load balancers in clusters
- D) Guarantee zero-kernel vulnerabilities

47. Two containers both expose internal port 8080. Conflict?
- A) Always conflict on the host
- B) No conflict unless same host port mapped
- C) Conflict only on Linux kernels
- D) Conflict only with bridge network mode

48. Best practice for security patch in base image?
- A) Patch running container manually forever
- B) Rebuild image and redeploy containers
- C) Wait until next major release cycle
- D) Disable vulnerability scanning rules

49. Dockerfile is primarily:
- A) Runtime debugger for container memory
- B) Build recipe for creating image layers
- C) Network policy for service mesh
- D) Database migration manifest format

50. Layer caching helps because:
- A) Unchanged layers are reused in rebuilds
- B) It removes need for any CI pipeline
- C) It forces immutable runtime memory
- D) It guarantees smaller images always

---

## INTEGRATED SCENARIOS (51-60)

51. You need to locate the commit that introduced a regression quickly. Best tool?
- A) git cherry-pick
- B) git stash
- C) git bisect
- D) git clean

52. API latency rose from 200ms to 3s. First step?
- A) Add random retries in frontend
- B) Profile each layer to locate bottleneck
- C) Disable logs across all services
- D) Increase CDN TTL for dynamic endpoints

53. CI is green but production fails on rollout. Most useful safeguard?
- A) Blue-green/canary with rollback path
- B) Direct deploy to all nodes at once
- C) Remove health checks to reduce delay
- D) Freeze database writes for a day

54. Frontend should be loosely coupled to backend by:
- A) Sharing direct DB credentials with UI
- B) Using stable API contracts/interfaces
- C) Embedding SQL in browser code
- D) Tying releases to same build artifact

55. Secret leaked in Git and used in production. Immediate priority?
- A) Rename variable containing the secret
- B) Rotate/revoke secret and audit access
- C) Rebase branch to hide commit only
- D) Disable CI to prevent more logs

56. For hourly deployments, database change strategy should be:
- A) Backward incompatible and immediate
- B) Expand-contract with safe migration steps
- C) Manual edits during peak traffic only
- D) Schema rewrite with no rollback plan

57. Stateless API services improve scalability because:
- A) Any instance can serve any request
- B) They eliminate need for authentication
- C) They avoid all database contention
- D) They remove load balancer necessity

58. CDN should not cache authenticated API profile responses because:
- A) JSON cannot be cached at edge nodes
- B) Content is user-specific and sensitive
- C) Auth headers block all CDN traffic
- D) CDNs only support image MIME types

59. Team bypasses branch protection once. Main risk?
- A) Faster release cadence temporarily
- B) Broken governance and higher incident risk
- C) Smaller pull request sizes on average
- D) Better autonomy for junior developers

60. Reliable architecture practice across Git, CI/CD, API, Docker is:
- A) Optimize only for delivery speed
- B) Prefer reproducibility, validation, rollback
- C) Keep all environments intentionally different
- D) Avoid automation to reduce complexity

---
