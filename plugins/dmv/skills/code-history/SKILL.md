---
name: code-history
description: Traces code history via git blame and log to explain why code exists in its current form. Use when asked about code history, reasoning behind changes, or "when/why did this change".
---

# Git Historian

Investigate code history and synthesize narrative explanations of why code is the way it is.

## Process

1. **Parse the query** — determine what to research (file, function, line, concept, pattern)

2. **Research using git archaeology:**
   - Always use `--follow` to track through renames
   - Use `git blame` for line-level attribution
   - Use `git log -S` (pickaxe) and `git log -G` for concept/pattern searches
   - Follow commit references to find related PRs: `gh pr list --search "<hash>" --state all`
   - Check PR discussions for reasoning and alternatives considered — Claude tends to skip this step

3. **Synthesize a narrative, not a list:**
   - Focus on WHY, not just WHAT and WHEN
   - Connect technical changes to the problems they solved
   - Distinguish facts from inferences — "Based on the commit message, it appears..."
   - Note gaps honestly — state what's missing, don't paper over it

4. **Return in this structure:**

   ```
   # Summary
   [Direct 2-3 sentence answer to the question]

   # Historical Evolution
   [Chronological narrative with dates and commit hashes]

   # Reasoning
   [Why decisions were made — problems, constraints, alternatives considered]

   # Supporting Evidence
   [Relevant commits quoted, PR discussions, code snippets showing evolution]

   # Assessment
   [Is this still the right approach? Technical debt? Context changed?]

   # Gaps in Historical Record
   [What's unclear or missing — only if applicable]
   ```

## Constraints

- NEVER dump raw git output without interpretation — synthesize into narrative
- NEVER present speculation as fact
- NEVER ignore file renames — always use `--follow`
- ALWAYS start with a direct summary answer
- ALWAYS investigate referenced PRs/issues when found in commit messages
- ALWAYS distinguish between what you know and what you're inferring
