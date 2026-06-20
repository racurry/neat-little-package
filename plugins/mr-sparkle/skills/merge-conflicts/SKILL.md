---
name: merge-conflicts
description: Resolves git merge conflicts by analyzing intent from both sides. Use when merge conflicts are detected or when git operations fail with conflict errors.
---

# Merge Conflicts

## Process

1. **Detect conflicted files:** `git status` — look for "both modified" / "both added"

2. **For each conflicted file:**

   **Read and understand intent:**
   - Read the FULL file, not just conflict sections
   - Use `git log -p --follow -- path/to/file` to see recent history
   - Use `git blame path/to/file` to understand why each side made changes
   - Determine: what problem does HEAD solve? What problem does incoming solve? Are they compatible?

   **Classify and resolve:**

   **Compatible changes** (different additions, merged imports) → auto-resolve, keep both
   - Confidence: High
   - Example: different methods added to same class, `import { A, B }` vs `import { A, C }` → `import { A, B, C }`

   **Overlapping changes** (same logic modified differently) → combine if possible, explain reasoning
   - Confidence: Medium — explain reasoning, may flag for review
   - Example: two different optimizations of same function

   **Incompatible changes** (mutually exclusive) → do NOT auto-resolve
   - Confidence: Low — explain both options, recommend one, flag for manual review
   - Example: one side disabled a feature for security, other side enhanced it

3. **Apply resolution:**
   - Write resolved file without conflict markers
   - Verify resolved code is syntactically valid
   - Stage resolved file: `git add path/to/file`

4. **Report per file:**
   ```
   File: path/to/file
   Strategy: Compatible / Overlapping / Incompatible
   Reasoning:
     - HEAD: <what it was trying to do>
     - Incoming: <what it was trying to do>
     - Resolution: <how both intents were preserved>
   Confidence: High / Medium / Low
   Status: Auto-resolved / Needs review
   ```

5. **Provide next steps:**
   - Files staged and ready
   - Files needing manual review
   - How to complete: `git commit` or `git merge --continue`
   - How to abort: `git merge --abort` or `git rebase --abort`

## Constraints

- ALWAYS read full file and git history before resolving — never resolve based on conflict markers alone
- ALWAYS explain reasoning with "HEAD wanted X, incoming wanted Y" language
- ALWAYS state confidence level honestly per file
- Be conservative — prefer flagging for review over incorrect auto-resolution
- Never guess at business logic
- Never complete the merge/rebase automatically — only stage resolved files
- Never lose functionality from either side without explaining the tradeoff
