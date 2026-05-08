# Git & VCS: Depth + Test Prep (300 Lines)

## The Problem VCS Solves

You're coding. Ctrl+Z only works in the current session. Close your editor? Undo history is gone. You edited 5 files 2 hours ago and broke something—which file was it? You want to remember what you changed last week—impossible without notes.

**A Version Control System (VCS) is a system that records changes to files over time** so you can:
- See the full history of what changed and when
- Revert instantly to any previous version
- Understand *why* you made a change (via commit messages)
- Collaborate with teammates without overwriting each other

Without VCS, teams would manually email files to each other. Disaster.

---

## Three Generations of VCS

### Local VCS
Simple database on your machine. Records versions locally. You can revert to old versions.

**Problem**: Only you have the history. If your disk dies, everything is gone. No collaboration.

### Centralized VCS (CVCS) - Example: SVN
One central server holds all versioned files. Everyone commits to it.

```
Your Computer ← commit/checkout → Central Server (all history)
Coworker's Computer ← commit/checkout → Central Server
```

**Advantage**: Team can collaborate. All history is in one place.

**Problem**: Single point of failure. Server dies = nobody can commit. Nobody can work offline. If server data corrupts, there's no backup.

### Distributed VCS (DVCS) - Example: Git ⭐
Every developer's machine has a *complete copy* of the entire history.

```
Your Machine (full history) ← → Central Server (full history)
Coworker's Machine (full history) ← → Central Server
Coworker's Laptop (full history) ← → Server
```

**Advantage**: 
- Server dies? Any machine can restore it. 
- You can work offline. Commits are local.
- Each clone is a backup.

**This is why Git dominates.**

---

## How Git Thinks About Data: Snapshots vs Deltas

Most VCS systems store **deltas** (differences):

```
Version 1: file.js { 50 lines }
Version 2: file.js { Version 1 + 3 lines added }
Version 3: file.js { Version 2 + 5 lines removed }
```

To get Version 3's content, you reconstruct: Start with V1, apply V2's delta, apply V3's delta.

**Git is different. It stores snapshots:**

```
Snapshot 1: { user.js (100 lines), post.js (80 lines), db.js (60 lines) }
Snapshot 2: { user.js (100 lines, unchanged), post.js (85 lines, NEW), db.js (60 lines, unchanged) }
Snapshot 3: { user.js (102 lines, MODIFIED), post.js (refs S2), db.js (refs S1) }
```

Git stores full file content (or references to unchanged files). You can instantly jump to any snapshot without reconstructing history.

**Why this matters**:
- **Speed**: Jumping to old versions is instant (no reconstruction).
- **Data Integrity**: Every snapshot is locked with a **SHA-1 hash**. Change one character in one file, and the hash changes. Git detects tampering immediately.

---

## The Three States (The Core Mental Model)

Everything in Git revolves around three states. This is **critical to understanding Git**.

| State | Location | Meaning |
|-------|----------|---------|
| **Modified** | Working Directory | You changed a file; Git hasn't recorded it |
| **Staged** | Staging Area (Index) | You marked this file "include in next snapshot" |
| **Committed** | Repository (.git) | The snapshot is safely in Git's database |

**The workflow**:

```
You edit file.js
    ↓ (file is "Modified")
git add file.js
    ↓ (file is now "Staged" — will go in the snapshot)
git commit -m "Fix bug in file.js"
    ↓ (snapshot created, file is now "Committed")
Snapshot saved in .git forever
```

**Key Insight: Staging Area is intentional.** You control what goes into the next snapshot.

---

## Git Internals: The Three Areas

```
Working Directory     Staging Area (.git/index)    Repository (.git)
   (edit here)          (stage here)                (commits here)
      ↓                      ↓                            ↓
   user.js         git add user.js              Snapshot A
   post.js                                      Snapshot B
   db.js           git commit                   Snapshot C
                                                (full history)
```

- **Working Directory**: Your actual project folder. Where you edit files.
- **Staging Area**: Temporary holding area. Tells Git which changes to include in the next snapshot.
- **Repository** (.git folder): Database of all commits. Every snapshot ever created.

---

## Staging Area and Snapshots

### Why the Staging Area Exists

The Staging Area is unique to Git. It sits between your working directory and the repository.

**The concept**: You can edit 5 files but only commit 2 of them right now. The staging area lets you choose which files go into the next snapshot.

**Why this matters**:
- **Fine-grained control**: Separate unrelated work into focused commits
- **Clean history**: Each commit = one logical change (easier to debug later)
- **Safe merging**: Reviewers see focused diffs, not "everything I changed today"
- **Safe reverts**: If you need to undo one feature, you don't undo unrelated changes

**The flow**:
```
Edit files → MODIFIED (in working directory)
              ↓
Select which to commit → STAGED (staging area)
              ↓
Take snapshot → COMMITTED (in .git repository)
```

### Snapshots vs Deltas

**Snapshots** (Git's way):
- Git stores **full state** of all files at each commit
- Jumping to any old version is instant (no reconstruction needed)
- Every commit is self-contained
- More disk space but faster access

**Deltas** (traditional way):
- Store only differences between versions
- "Version 2 = Version 1 + changes"
- Takes less space but must reconstruct history to see old versions
- Change one character, and all later versions need recalculation

**Which is better?**
- Git chose snapshots because speed and safety matter more than disk space
- Snapshots with SHA-1 hashing means tampering is instant to detect

---

---

## Branching: Why and How

### What is a Branch?

A branch is a **pointer to a commit**. Nothing more.

- `main` points to the latest commit on main
- `feature/auth` points to a different commit
- Creating a branch = creating a new pointer
- Switching branches = moving HEAD to different pointer
- Branches are cheap (just pointers, not copies)

### Why Branch?

**Without branches** (dangerous):
```
main: v1.0 → v1.1 → [START FEATURE] → v1.2 (broken) → v1.3 (still broken)
                    ↑
              All new work on main
              Everyone sees broken code
              Can't mark v1.1 as "stable"
```

**With branches** (safe):
```
main:     v1.0 → v1.1 → v1.2 → v1.3 (stays stable)
                          ↓
                      [TEST & REVIEW]
feature:                        v2.0 (merged after testing)
                    
Feature branch is isolated.
Main stays stable and usable.
Others don't see broken feature code.
```

### Branching Rules

1. **Main branch is sacred** — Only tested, working code. Never push broken code to main.
2. **Create branches for features** — One branch per feature/bugfix. Name: `feature/name` or `bugfix/name`
3. **Merge when ready** — After testing locally and code review
4. **Delete after merging** — Cleanup remote and local branches

### Multiple Branches in DAG

When multiple developers work on different features, the DAG explodes.

```
main:      A → B → C → D → M1 → E → M2 (after merging features)
                ↖                      ↗
feature-1:          F → G → H  ↗
                ↖                  
feature-2:          I → J → K ↗
```

- Three branches developed in parallel
- F, I, and C all have B as parent (branching point)
- M1 = merge of feature-1 into main
- M2 = merge of feature-2 into main
- This is how real teams work

---

## Important Concepts

**Commit (Snapshot)**: A complete record of your project at a moment in time. Has a unique SHA-1 ID, message, author, timestamp. You can instantly jump to any commit or see what was in that snapshot.

**HEAD**: Pointer to your current position in history. Usually points to the latest commit of your current branch. When you `checkout`, you move HEAD to a different commit.

**Branch**: Isolated line of development. A branch is just a pointer to a commit. When you create `feature/auth`, it's a new pointer. You can create unlimited branches without affecting each other.

**Conflict**: Two developers edited the **exact same lines** in the same file on different branches. Git can't auto-merge because both versions are valid—only humans can decide which is correct.

**Remote**: A copy of the repository on a server (GitHub, GitLab, etc.). `origin` is the default name for the server's repo. Your local repo is separate; pushing and pulling synchronize them.

**Merge Commit**: A special commit that has TWO parents. Created when merging two branches that both have new commits. Records in history that work was merged.

---

---

## Core Concepts: Push, Pull, and Merge

### Push and Pull: Two Directions of Sync

**Pull** = Download changes from server and merge into your local branch.
- Synchronizes you with teammates' work
- Server has commits your local doesn't have
- Pulling adds those commits to your history
- Do this at start of day and before critical work

**Push** = Upload your local commits to server.
- Shares your work with teammates
- Your commits leave your machine and go to GitHub/server
- Makes your work a backup (disk crash won't lose it)
- Do after testing and review

**The Rule**: Always pull before push. Otherwise you get non-fast-forward errors.

### How Merging Works Internally

A merge combines two branches' histories.

**Behind the scenes**:
1. Git finds the **common ancestor** (last commit both branches shared)
2. Git compares: ancestor → tip of branch A (your changes)
3. Git compares: ancestor → tip of branch B (their changes)
4. If changes don't overlap → automatic merge (creates merge commit)
5. If changes **overlap** (same lines) → **conflict** (manual decision needed)

**After merge**:
- New merge commit created (has 2 parents—one from each branch)
- This records in permanent history that branches were combined
- One branch is merged INTO another (usually feature → main)

### Merge Conflicts: When and Why

Conflicts happen when **two people edit the exact same lines** in the same file on different branches.

**Why Git can't auto-fix**:
```
main has:    function login(user, pass) { return authenticate(user); }
feature has: function login(user, pass) { return validate(user); }

Git sees: "Both versions modified the same lines. Which is correct?"
Answer: Only the developers know.
```

**The conflict appears as**:
```
<<<<<<< HEAD (current branch - main)
  return authenticate(user);
=======
  return validate(user);  ← Other branch (feature)
>>>>>>> feature
```

**Resolution**: Delete the markers and **choose which code to keep**, or combine both.

**Key insight**: Conflicts are NORMAL in teams. They're Git saying "I found something you must decide."

### How Conflicts are Avoided

1. **Pull frequently**: Stay updated with main, reduce divergence
2. **Short-lived branches**: Merge fast, don't work in isolation for weeks
3. **Coordinate**: Tell teammates "I'm editing auth.js" before major changes
4. **Code review**: Catch merge issues early before pushing

---

### Push Failures: Why They Happen

**Non-Fast-Forward Push**: Your local history diverged from the server.
- Someone else pushed commits while you were offline
- Your local main has commits the server doesn't have
- Server has commits your local doesn't have
- If Git allowed you to push, the server's commits would be lost
- **Must pull first** to merge server's commits, then push

**Authentication Failed**: Credentials or SSH keys are wrong.
- SSH key not set up on your machine
- Key not added to GitHub
- Token expired
- Username/password incorrect

**Permission Denied**: You don't have write access.
- Repository is private and you're not a collaborator
- Organization restricted access
- Need to ask owner for permission
- Or use fork + pull request instead

---

## Complex Merge Scenarios

### Scenario 1: Forgot to Pull Before Pushing

Your local is out of sync with server.

**What happens**:
- You made commits locally
- Teammate also pushed commits
- Both of you edited the same codebase
- Git refuses your push (non-fast-forward)
- Your local and server diverged

**To fix**: Pull the server's commits first (merges them locally), resolve any conflicts, then push.

### Scenario 2: Committed on Wrong Branch

You made commits on `main` but they should be on `feature-auth`.

**What happened**:
- Main branch should only have stable code
- Feature branch should have in-progress work
- You accidentally edited and committed on main
- Now main is broken

**To fix**: Create the feature branch and move those commits there, then undo them on main.

### Scenario 3: Massive Merge with Many Conflicts

You're merging main into your feature branch after 2 weeks of parallel work.

**Why conflicts explode**:
- 2 weeks = many commits on main
- Many commits on your feature
- Large number of overlapping edits
- Every overlapping edit = potential conflict

**How to approach**:
- Pull main into your branch
- Use IDE's merge conflict tool (visual, easier than manual)
- Resolve file by file
- Test thoroughly before pushing

### Scenario 4: Push Succeeds But Teammates Can't See Changes

You pushed, but teammates pulling get old code.

**Why this happens**:
- You pushed to the wrong branch (pushed feature to feature, not to main)
- You're on a local branch but never merged to main
- Teammates are on a different branch

**To fix**: Merge your branch into main, then push main.

---

---

## Understanding the Commit Tree (DAG)

Git's commit history is a **Directed Acyclic Graph (DAG)**—a tree showing parent-child relationships between commits.

### Linear History (Single Branch)

```
A → B → C → D
```
- Straight line of commits
- Each commit has exactly one parent
- No parallel work
- Rare in real teams

### Branching Creates Parallel Lines

```
A → B → C → D (main)
     ↖
      E → F (feature)
```
- Both C and E have B as parent
- Two separate lines of development from point B onward
- C doesn't know about E; E doesn't know about C
- They develop independently

### Merge Creates Two Parents

```
      M (merge commit)
     / ↖
A → B→ C  F
     ↖__ → (feature)
```

**Key concept**: Merge commit M has TWO parents.
- One parent: C (tip of main)
- Other parent: F (tip of feature)
- This records that work was merged at this point
- History shows both branches AND where they joined

### Why DAG Structure Matters

1. **Tracks collaboration**: Two parents = parallel work that was combined
2. **Debugging**: Can trace exact commit where bug was introduced
3. **Fast-forward vs merge**: DAG determines if linear history or merge commit
4. **Rebase**: Changes the DAG by replaying commits (cleaner but riskier)

### Fast-Forward vs Merge Commit

**Fast-forward** (linear history):
```
Before:           After:
main: A → B       main: A → B → C → D
feature: C → D    (just moved pointer, no merge commit)
```
- Feature branch was directly ahead of main
- No other commits on main after feature branched
- Git just moves main pointer forward
- No merge commit created
- History stays linear and simple

**Merge commit** (records collaboration):
```
Before:           After:
main: A → B → E   main: A → B → E → M (merge commit with 2 parents)
feature: C → D         ↖ C → D ↙
```
- Both branches had new commits
- Git creates new commit M with 2 parents
- Shows in history that merging happened
- More complex but documents parallel work

**Which happens?**
- Fast-forward: When feature is cleanly ahead (no divergence)
- Merge commit: When both branches diverged (real team collaboration)

### Rebase: Alternative to Merge

Instead of creating a merge commit, **rebase replays commits** on top of main.

```
Merge commit approach:
A → B → C → M (merge commit)
     ↖→ E → F ↗

Rebase approach:
A → B → C → E' → F' (E and F replayed on top of C)
```

**Rebase effect**:
- Removes merge commit
- History stays linear
- Looks like feature work happened AFTER main's work
- Actually happened in parallel, but history shows sequentially

**Trade-off**:
- Rebase: Cleaner, linear history (but rewrites history—risky on shared branches)
- Merge: Preserve exact history (but creates merge commits—messier DAG)

For team collaboration: **Merge is safer** (doesn't rewrite history). For personal branches: **Rebase is fine** (you're only affecting your work).

---

## Q&A Session

**Q1: Why does Git store snapshots instead of deltas?**
A: Snapshots let Git instantly jump to any version without reconstruction. Deltas are smaller but require rebuilding. Git prioritizes speed and simplicity over storage size.

**Q2: What's the difference between Modified, Staged, and Committed?**
A: Modified = you changed it in your editor. Staged = you told Git "include this in my next snapshot." Committed = snapshot is created and saved in .git forever.

**Q3: Why is there a Staging Area? Why not just commit everything I changed?**
A: Fine-grained control. You might edit 5 files but only want to commit 2 right now. Staging Area lets you choose what goes into each snapshot.

**Q4: What happens if the central server (GitHub) dies?**
A: Your local repo has the full history. Someone else's local repo also has it. You can push to a new server or continue working offline. No data loss.

**Q5: When should I create a branch?**
A: When starting a new feature, experiment, or bug fix. Always isolate work on a branch. Main should stay stable. Merge only when tested.

**Q6: What's a merge conflict and how do I avoid it?**
A: Conflict = two people edited the same line on different branches. Difficult to resolve. Avoid by: communicating with teammates, keeping branches short-lived, pulling often.

**Q7: If I commit something wrong, is it permanent?**
A: Not permanent, but difficult to undo. Use `git revert` to create a new commit that undoes it (safer). `git reset` can remove commits, but is riskier on shared repos.

**Q8: Does every commit go to the server automatically?**
A: No. Commits are local. `git push` sends them to the server. This lets you work offline and decide when to share.

**Q9: What's the difference between fetch and pull?**
A: `git fetch` downloads changes but doesn't merge them. `git pull` downloads AND merges. Pull is usually what you want.

**Q10: Can I work on a feature branch while someone else works on main?**
A: Yes. You work on your branch, they work on main. Later, you merge. No interference. That's the power of distributed branches.

**Q11: When should I pull vs push?**
A: Pull at START of work session to sync with server. Push after testing locally. Pull gets changes TO you. Push sends changes FROM you. Always pull before push.

**Q12: What happens if I push and it fails with "non-fast-forward"?**
A: Someone else pushed while you were offline. Do `git pull origin main` to download and merge their changes locally, then `git push origin main` again.

**Q13: How do merge conflicts happen?**
A: Two people edited the SAME lines in the same file on different branches. Git can't automatically choose which version is correct. You must manually resolve by editing the conflict markers.

**Q14: How do I resolve a merge conflict?**
A: (1) `git status` shows conflicted files. (2) Open file and delete conflict markers. (3) Keep the correct code (or combine both). (4) `git add .` (5) `git commit`.

**Q15: What does this mean: `<<<<<<< HEAD` to `>>>>>>>`?**
A: Conflict marker showing two versions. `HEAD` = current branch. `=======` = separator. Bottom part = branch being merged. Delete markers and keep correct code.

**Q16: How can I avoid merge conflicts?**
A: Pull frequently, keep branches short-lived, don't work in isolation for weeks, coordinate with teammates about who's editing what.

**Q17: What's the difference between a merge commit and fast-forward?**
A: Fast-forward: no merge commit, just moves pointer forward (linear history). Merge commit: creates new commit with two parents (records that work was merged). Fast-forward is cleaner; merge commit tracks collaboration.

**Q18: What does `git log --graph --oneline --all` show?**
A: Visual tree of commits showing branches, merges, and relationships. Each `*` is a commit, `|` shows parent-child connections, `/` and `\` show branching/merging.

**Q19: Why does my push fail with "Permission denied"?**
A: You don't have write access. Either the repo owner must add you, or you contribute via fork + pull request. Check ssh keys or credentials are correct.

**Q20: What should I do before pushing my feature branch to main?**
A: (1) Pull main to sync. (2) Resolve any conflicts locally. (3) Test thoroughly. (4) Merge into main locally and test again. (5) Then push.

**Q21: Can I push while working on a feature branch?**
A: Yes, push your feature branch often (`git push origin feature-name`). Main should only have stable, tested code. Merge feature to main only when ready.

**Q22: What happens in a Directed Acyclic Graph (DAG) when I merge?**
A: New commit is created with TWO parents (one from each branch). This records the merge point. Graph shows as `/` or `\` in `git log --graph`.

**Q23: Is rebase better than merge?**
A: Rebase keeps history linear (cleaner), but rewrites history (riskier on shared branches). Merge is safer but creates merge commits. For main: use merge. For personal branches: rebase is fine.

**Q24: What data do I lose if I don't push?**
A: Your commits stay locally in `.git` folder. If your disk crashes, commits are lost. That's why you push—to back up on the server.

