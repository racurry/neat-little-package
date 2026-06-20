---
name: commit
description: Commit changes with smart messages. Supports full and partial commits. Use whenever committing changes or handling pre-commit hook failures.
argument-hint: [message, instructions, or description of what to commit]
---

# Commit

## Process

1. **Interpret arguments** — `$ARGUMENTS` could be any of:
   - A commit message: "refactor authentication flow"
   - Instructions about what to commit: "just the test files"
   - Empty: commit everything, generate a message

   Use judgment based on context. Don't ask unless unclear — infer if possible.

2. **Analyze repository state:**
   - `git status` — see all changes
   - `git diff` and `git diff --staged` — see what's changed

3. **Stage files:**
   - Default: stage everything (`git add .`)
   - If the user specified what to commit (e.g., "just the auth stuff"): stage only matching files

4. **Generate or use commit message** following these requirements:
   - Terse, single-line format (max ~200 characters)
   - NO type prefixes (no `fix:`, `feat:`, `refactor:`, etc.)
   - NO emojis or decorative elements
   - NO attribution text (no "Generated with Claude Code", no "Co-Authored-By:")
   - Present tense, imperative mood
   - Be specific about WHAT changed

   **Good:** `prevent race condition in session cleanup`, `rate limiting middleware`

   **Bad:** `fix: correct bug`, `updates`, `add new feature ✨`, `fix bug.`

5. **Commit:**
   ```bash
   git commit -m "message"
   ```

6. **Handle pre-commit hook failures:**

   Pre-commit hooks (formatters/linters) sometimes auto-modify files during commit, causing it to fail because git won't commit when the working directory changes mid-process.

   - If hook **modified files** (auto-formatting): `git add .` then `git commit --amend --no-edit`
   - If hook **validation errors** (linting failures): report errors, do NOT retry
   - NEVER retry more than once — if the retry fails, investigate hook configuration
   - Before amending: verify authorship with `git log -1 --format='%an <%ae>'` — never amend someone else's commit

7. **Verify:** `git status` and `git log -1 --oneline`
