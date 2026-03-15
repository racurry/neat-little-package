---
name: pr
description: Create a pull request with Problem/Solution format. Can optionally commit first. Use when opening PRs or when branch changes are ready for review.
argument-hint: [optional problem context]
---

# PR

## Process

1. **Analyze branch context:**
   - Current branch: `git branch --show-current`
   - Base branch: `git remote show origin | grep 'HEAD branch'`
   - Commits since divergence: `git log --oneline <base>..HEAD`
   - Full diff: `git diff <base>...HEAD`

2. **Determine Problem scope:**
   - All commits relate to one issue → single Problem statement
   - Commits address distinct issues → numbered list, matching Solution numbers

3. **Generate PR description** in Problem/Solution format:

   ```markdown
   ## Problem
   {problem statement - describe the issue being solved}

   ## Solution
   {plain language overview of the changes}
   ```

   For multiple problems, use numbered lists with matching numbers in both sections.

   - If `$ARGUMENTS` provided, use as context for the Problem statement
   - If not, infer Problem from commits and diff
   - Be terse — no filler words
   - Problem is human-readable English explaining the issue
   - Solution is plain language overview of changes, not implementation details
   - Can include links to logs/docs or error output if relevant
   - **Ignore any PR templates in the repo**

4. **Generate PR title:**
   - Short, descriptive, lowercase, no type prefixes, no emojis

5. **Create PR** (prefer gh CLI, fall back to GitHub MCP server):
   - Write body to `.tmp/pr-body.md`, then `gh pr create --title "title" --body-file .tmp/pr-body.md`
   - If branch not pushed: `git pub` first

6. **Return PR URL**

## What NOT to Include

- NO "Generated with Claude Code" footer
- NO attribution text or co-authorship
- NO emojis in titles or body
- NO PR template boilerplate (Summary/Test Plan/etc)
- NO checkbox test plans
