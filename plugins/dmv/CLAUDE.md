# DMV Development Guidelines

## Philosophy

**User-Specific Preferences First**

- Skills document ONLY user's specific requirements (knowledge delta filter applied)
- Defer to Claude's base training for standard git/GitHub knowledge
- Focus on edge cases, preferences, and patterns Claude gets wrong
- No comprehensive documentation of well-known tools

**Automation Over Manual Intervention**

- Pre-commit hook failures handled automatically with single-retry pattern
- Smart message generation when user doesn't provide one
- Intelligent tool selection (gh CLI → GitHub MCP server)
- Minimize user interruption during workflows

**Terse Over Verbose**

- Commit messages: single-line, specific, no attribution
- No emojis or decorative elements
- Present tense, imperative mood
- Focused on WHAT and WHY, not HOW

**Evidence-Based Patterns**

- Pre-commit retry pattern based on real failure scenarios
- Commit format based on user's established preferences
- Tool selection hierarchy based on capability and availability
- All patterns grounded in actual workflows, not speculation

## Component Patterns

### Skills

**Knowledge Delta Filter (Critical):**

DMV skills apply strict knowledge delta filtering:

✅ **Include:**

- User's specific commit message format (terse, no emojis, no attribution)
- Pre-commit hook retry edge case (auto-formatting failures)
- Tool selection hierarchy (gh CLI → GitHub MCP server)
- User's PR format requirements (no attribution)

❌ **Exclude:**

- Standard git commands (Claude knows: status, diff, commit, add, log, etc.)
- General GitHub workflows (Claude knows: PRs, issues, branches, etc.)
- Basic authentication patterns (Claude knows: gh auth login, tokens, etc.)
- Common git best practices (Claude knows these from training)

**Result:** Focused skills (~80-150 lines) documenting only user-specific preferences and edge cases.

**Structure Pattern:**

```markdown
---
name: skill-name
description: User-specific [area] preferences and edge case handling
---

# Skill Name

This skill documents [specific patterns] specific to this user. Claude already knows standard [tool] from training - this skill only documents the user-specific details.

## User-Specific [Topic] Requirements

**This user has specific [preferences] that differ from standard practices.**

[Document the delta]

## [Edge Case Name] (Critical)

**Problem this user encounters:** [Specific issue]

[Document the solution]

## Quality Checklist

[User-specific validation items]
```

**Quality Checklist:**

- ✓ Applies knowledge delta filter strictly (only user-specific content)
- ✓ Distinguishes user preferences from standard practices
- ✓ Includes decision frameworks for ambiguous situations
- ✓ Documents edge cases and common pitfalls
- ✓ Provides quality checklist
- ✓ Defers to official docs for syntax/specifications
- ✓ Focused scope (~80-150 lines typical)

### Agents

**git-committer Pattern:**

The git-committer agent handles all commit operations autonomously:

**Structure:**

1. **Load git-workflow skill (REQUIRED)** - Get user preferences first
1. **Analyze repository state** - Run git status, git diff, git diff --staged
1. **Determine commit scope** - Full (all files) or partial (selected files)
1. **Generate commit message** - If not provided, analyze changes and create terse message
1. **Execute commit** - Proper quoting, no attribution
1. **Handle pre-commit hook failures** - Single-retry pattern for auto-formatting
1. **Verify commit success** - Check git status and git log

**Pre-commit hook retry logic (Critical):**

```bash
# 1. Initial commit attempt fails (hook modified files)
git commit -m "message"  # FAILS

# 2. Stage auto-modified files
git add .

# 3. Retry ONCE with --amend --no-edit
git commit --amend --no-edit  # SUCCEEDS
```

**CRITICAL rules:**

- ✓ Only retry ONCE (avoid infinite loops)
- ✓ Only retry for modifications, not validation errors
- ✓ Use --amend --no-edit to keep same message
- ✓ If retry fails, investigate hook configuration

**Commit message generation pattern:**

```markdown
1. Analyze git diff --staged output
2. Identify nature of changes (fix, add, update, refactor, etc.)
3. Read affected files if needed for context
4. Generate terse message: "<brief specific description>"
5. Validate: lowercase start, no period, no emoji, no attribution
6. Execute commit with proper formatting
```

**Quality Checklist:**

- ✓ Loads git-workflow skill before proceeding
- ✓ Analyzes repository state thoroughly
- ✓ Generates terse, specific commit messages
- ✓ No emojis or attribution in commits
- ✓ Handles pre-commit hook failures with single-retry
- ✓ Verifies commit success before returning
- ✓ No user interaction language
- ✓ Autonomous operation in isolated context

**pr-opener Pattern:**

The pr-opener agent handles all PR creation autonomously:

**Structure:**

1. **Load github-workflow skill (REQUIRED)** - Get user PR format preferences
1. **Analyze branch context** - Get commits since base, full diff
1. **Determine Problem scope** - Single problem or multiple (numbered list)
1. **Generate Problem statement** - User impact, symptoms, context
1. **Generate Solution statement** - Plain language overview of changes
1. **Create PR** - Use gh CLI (preferred) or MCP server
1. **Verify PR created** - Return PR URL

**Problem/Solution format (Critical):**

```markdown
## Problem
{problem statement - describe the issue being solved}

## Solution
{plain language overview of the changes}
```

**Multiple problems pattern:**

```markdown
## Problem
1. First problem description
2. Second problem description

## Solution
1. Solution to first problem
2. Solution to second problem
```

**Quality Checklist:**

- ✓ Loads github-workflow skill before proceeding
- ✓ Analyzes all commits on branch (not just latest)
- ✓ Infers Problem from commit context and diff
- ✓ Generates terse, concise descriptions
- ✓ No attribution, no emojis, no PR template boilerplate
- ✓ Matches problem count to solution count
- ✓ Verifies PR created before returning
- ✓ Autonomous operation in isolated context

### Commands

**Delegation Pattern:**

All DMV commands follow the thin wrapper delegation pattern:

```markdown
---
description: <Action-oriented description>
argument-hint: [optional arguments]
---

Use the git-committer agent to execute <specific workflow>.

If $ARGUMENTS is provided, <how to use arguments>.

If $ARGUMENTS is NOT provided, <what agent will do>.
```

**Examples:**

`/dmv:commit` → git-committer (full commit)
`/dmv:commit-partial` → git-committer (partial commit with file selection)
`/dmv:pr` → pr-opener (create PR with Problem/Solution format)
`/dmv:setup` → setup workflow (no agent needed, simple verification)

**Quality Checklist:**

- ✓ Includes description field in frontmatter
- ✓ Delegates to git-committer for commit operations
- ✓ Uses argument-hint when accepting arguments
- ✓ Single, focused responsibility
- ✓ No complex logic in command prompt

## Decision Framework

### When to Use Each Component

**Skill vs Agent:**

- **Skill** = User-specific preferences (git format, tool selection)
- **Agent** = Autonomous work (create commits, analyze changes)

**Full Commit vs Partial Commit:**

- **Full** = All changes in repository (git add .)
- **Partial** = Subset based on description (natural language file selection)

**gh CLI vs GitHub MCP Server:**

```
Task requires GitHub interaction
├─ Is gh installed and available?
│  ├─ Yes → Check if gh supports this operation
│  │  ├─ Yes → USE gh CLI (preferred)
│  │  └─ No → USE GitHub MCP Server
│  └─ No → USE GitHub MCP Server
```

**When to Retry Pre-commit Hooks:**

```
Commit failed
├─ Hook MODIFIED files (auto-formatting)?
│  ├─ Yes → Retry ONCE with staged modifications
│  └─ No (validation errors) → Report errors, do NOT retry
```

## Architecture

**Commit workflow:**

```
User → /dmv:commit → git-committer agent → git-workflow skill
         ↓              ↓                      ↓
     (thin wrap)    (complex logic)       (user prefs)
```

**PR workflow:**

```
User → /dmv:pr → pr-opener agent → github-workflow skill
         ↓           ↓                    ↓
     (thin wrap)  (complex logic)    (PR format prefs)
```

**Commit flow:**

1. User invokes command: `/dmv:commit`
1. Command delegates to agent: `git-committer`
1. Agent loads skill: `git-workflow`
1. Agent executes workflow autonomously
1. Agent handles failures (pre-commit retry)
1. Agent returns result

**PR flow:**

1. User invokes command: `/dmv:pr`
1. Command delegates to agent: `pr-opener`
1. Agent loads skill: `github-workflow`
1. Agent analyzes branch commits and diff
1. Agent generates Problem/Solution description
1. Agent creates PR via gh CLI or MCP
1. Agent returns PR URL

## Quality Standards

### Commit Messages

**Required format:**

- Terse, single-line (max ~200 characters)
- Pattern: `<brief specific description>`
- Lowercase start (unless proper noun)
- Present tense, imperative mood
- No period at end
- No emojis or decorative elements
- No attribution text (no "Generated with Claude Code", no "Co-Authored-By:")

**Good examples:**

```
prevent race condition in user session cleanup
rate limiting middleware for API endpoints
improve error handling in payment flow
extract validation logic for reuse
```

**Bad examples:**

```
❌ add: new feature ✨  (emoji)
❌ Fix: thing  (capitalized type)
❌ fix bug.  (has period)
❌ updates  (too vague)
❌ fix: correct bug

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
(attribution - user doesn't want)
```

### Pre-Commit Hook Handling

**Pattern:**

```bash
# 1. Attempt commit
git commit -m "message"

# 2. If fails due to hook modifications:
git add .
git commit --amend --no-edit

# 3. If retry fails, investigate hook configuration
```

**Rules:**

- ✓ Only retry ONCE (avoid infinite loops)
- ✓ Only retry for modifications (not validation errors)
- ✓ Stage all modified files before retry
- ✓ Use --amend --no-edit to preserve message
- ✓ If retry fails, report issue and stop

**When NOT to retry:**

- ❌ Hook validation errors (linting, tests failing)
- ❌ Already retried once (would create loop)
- ❌ Commit succeeded (no failure to retry)

### GitHub Interactions

**Tool selection hierarchy:**

1. **Check gh availability:** `which gh`
1. **Prefer gh CLI when:**
   - Creating/managing PRs
   - Creating/managing issues
   - Release management
   - Well-supported operations
1. **Use MCP Server when:**
   - gh not installed
   - Complex search queries
   - Bulk data retrieval
   - Operations gh doesn't support

**PR Description Format:**

```markdown
## Problem
{problem statement - describe the issue being solved}

## Solution
{plain language overview of the changes}
```

**For multiple problems, use numbered lists:**

```markdown
## Problem
1. First problem description
2. Second problem description

## Solution
1. Solution to first problem
2. Solution to second problem
```

**PR Requirements:**

- Terse, concise language - no filler words
- No "Generated with Claude Code" footer
- No attribution text or co-authorship
- No emojis in titles or body
- No PR template boilerplate (Summary/Test Plan/etc)
- No checkbox test plans
- Can include links to logs/docs if relevant
- Can include error output when fixing bugs

## Anti-Patterns (Forbidden)

### In Skills

- ❌ Documenting standard git commands Claude already knows
- ❌ Comprehensive git/GitHub documentation (use knowledge delta filter)
- ❌ Duplicating official documentation
- ❌ Presenting user preferences as universal requirements

### In Agents

- ❌ User interaction language ("ask the user", "confirm with user")
- ❌ Skipping git-workflow skill loading
- ❌ Adding emojis or attribution to commits
- ❌ Retrying pre-commit hooks more than once
- ❌ Retrying validation failures (only retry modifications)

### In Commit Messages

- ❌ Emojis or decorative elements
- ❌ Attribution text or co-authorship
- ❌ Multi-line messages with boilerplate
- ❌ Vague descriptions ("fix bug", "update code")
- ❌ Capitalized type prefixes
- ❌ Periods at end

### In Pre-Commit Handling

- ❌ Infinite retry loops
- ❌ Retrying validation errors
- ❌ Bypassing hooks with --no-verify
- ❌ Not staging modifications before retry

### In PR Descriptions

- ❌ Using PR template boilerplate (Summary/Test Plan/etc)
- ❌ Adding checkbox test plans
- ❌ Attribution or "Generated with Claude Code"
- ❌ Emojis in title or body
- ❌ Mismatched problem/solution counts
- ❌ Verbose, filler language
- ❌ Only analyzing latest commit (must analyze all commits on branch)

## Validation Workflow

### Before Committing

1. ✓ Run git status and git diff to analyze changes
1. ✓ Generate or validate commit message format
1. ✓ Check for secrets in staged files (.env, credentials.json)
1. ✓ Stage appropriate files (all or subset)
1. ✓ Execute commit with proper quoting
1. ✓ Handle pre-commit hook failures if needed
1. ✓ Verify commit success

### Commit Message Quality

1. ✓ Terse, single-line format
1. ✓ Specific about what changed (not vague)
1. ✓ Lowercase start (unless proper noun)
1. ✓ No period at end
1. ✓ No emojis or decorative elements
1. ✓ No attribution text
1. ✓ Present tense, imperative mood

### Pre-Commit Hook Retry

1. ✓ Distinguish modifications from validation errors
1. ✓ Only retry for modifications
1. ✓ Stage all modified files before retry
1. ✓ Retry ONCE only (avoid loops)
1. ✓ Report failure if retry doesn't succeed

## Testing Strategy

### Component Testing

**Commands:**

```
/dmv:commit
/dmv:commit custom message
/dmv:commit-partial documentation changes
/dmv:pr
/dmv:pr fixing the auth timeout bug
/dmv:setup
```

Verify proper delegation and argument handling.

**Agents:**

Test git-committer in various scenarios:

- Empty repository (no changes)
- Staged changes only
- Unstaged changes only
- Mixed staged and unstaged
- Pre-commit hook success
- Pre-commit hook modification (retry)
- Pre-commit hook validation failure (no retry)

Test pr-opener in various scenarios:

- Single commit on branch (single problem)
- Multiple commits on branch (determine if single or multiple problems)
- Branch with context provided (use provided problem description)
- Branch without context (infer problem from commits/diff)
- gh CLI available (use gh)
- gh CLI not available (fall back to MCP)

**Skills:**

Load via Skill tool and verify guidance:

- git-workflow: Commit format, pre-commit retry
- github-workflow: Tool selection, PR format

### Integration Testing

**Full workflow:**

1. Make changes to repository
1. Run `/dmv:commit`
1. Verify: git-committer loads git-workflow
1. Verify: Analyzes changes correctly
1. Verify: Generates terse commit message
1. Verify: Commits successfully
1. Verify: Returns commit hash and summary

**Pre-commit hook retry:**

1. Configure pre-commit hook that modifies files
1. Run `/dmv:commit`
1. Verify: Initial commit fails
1. Verify: Agent stages modifications
1. Verify: Agent retries with --amend --no-edit
1. Verify: Retry succeeds
1. Verify: Commit created with original message

**Partial commit:**

1. Make changes to multiple file types
1. Run `/dmv:commit-partial test files`
1. Verify: Only test files staged
1. Verify: Commit message reflects subset
1. Verify: Other files remain unstaged

**PR creation (single problem):**

1. Create branch with one logical change
1. Run `/dmv:pr`
1. Verify: pr-opener loads github-workflow
1. Verify: Analyzes all commits on branch
1. Verify: Generates single Problem statement
1. Verify: Generates matching Solution statement
1. Verify: Creates PR with Problem/Solution format
1. Verify: Returns PR URL

**PR creation (multiple problems):**

1. Create branch with commits addressing multiple issues
1. Run `/dmv:pr`
1. Verify: Identifies distinct problems from commits
1. Verify: Uses numbered lists for Problem section
1. Verify: Uses matching numbered lists for Solution section
1. Verify: Problem count matches Solution count

**PR creation (with context):**

1. Create branch with bug fix
1. Run `/dmv:pr users getting 500 errors on login`
1. Verify: Uses provided context for Problem statement
1. Verify: Generates Solution from changes
1. Verify: Problem reflects provided context, not just inferred

## Documentation Standards

### README.md

User-facing documentation covering:

- Overview and core capabilities
- Features (commands, agents, skills)
- Design philosophy
- Installation instructions
- Quick start guide
- Workflow examples
- Troubleshooting
- Resources

### CLAUDE.md

Developer-facing guidelines covering:

- Philosophy (user-specific, automation, terse, evidence-based)
- Component patterns (skills, agents, commands)
- Decision framework
- Architecture
- Quality standards
- Anti-patterns
- Validation workflow
- Testing strategy

## Environment Setup

### Required Environment Variables

**GITHUB_PERSONAL_ACCESS_TOKEN:**

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_..."
```

Required for GitHub MCP server. Add to shell profile (~/.zshrc or ~/.bashrc).

**Token scopes needed:**

- `repo` - Full repository access
- `read:org` - Read organization data
- `read:user` - Read user profile data

### Optional Dependencies

**gh CLI (preferred for GitHub operations):**

```bash
brew install gh
gh auth login
gh --version
```

**Node.js (required for GitHub MCP server):**

```bash
node --version  # Should be v16+
```

## Version Management

**Semantic Versioning:**

- **Major (X.0.0):** Breaking changes to commit format, command signatures
- **Minor (x.Y.0):** New features, additional commands, new skills
- **Patch (x.y.Z):** Bug fixes, improved error handling, documentation

**Before Release:**

1. Test all commit workflows (full, partial, with hooks)
1. Validate commit message format compliance
1. Test GitHub integration (gh CLI and MCP server)
1. Update documentation (README, CLAUDE.md)
1. Update version in plugin.json
1. Test installation and setup workflow
