# DMV

![Some Days, We Don't Let The Line Move At All](assets/dmv.png)

Opinionated git and GitHub workflows with automated commit handling and intelligent tool selection. DMV provides terse commit messages, pre-commit hook retry logic, and seamless integration between gh CLI and GitHub MCP server.

## Overview

DMV (Department of Motor Vehicles) streamlines git and GitHub workflows by automating common operations and enforcing consistent patterns. It handles the tedious parts of version control while maintaining strict quality standards.

**Core capabilities:**

- Automated commit workflows with smart message generation
- Pre-commit hook retry logic for auto-formatting tools
- Partial commits based on natural language descriptions
- Intelligent tool selection (gh CLI → GitHub MCP server)
- Terse, attribution-free commit messages
- Easy setup and configuration

## Features

### Commands

#### `/dmv:commit [commit_message]`

Commit all changes with smart message generation or provided message.

**What it does:**

- Analyzes all staged and unstaged changes
- Generates terse, specific commit message if not provided
- Stages all files automatically
- Handles pre-commit hook failures with single-retry pattern
- No emojis or attribution added to commits

**Usage:**

```
/dmv:commit
```

Analyzes all changes and generates an appropriate commit message following the user's format preferences.

```
/dmv:commit refactor authentication flow
```

Commits all changes with the provided message.

**Commit message format:**

- Terse, single-line (max ~200 characters)
- Present tense, imperative mood
- Lowercase start (unless proper noun)
- No period at end
- No emojis or decorative elements
- No attribution or co-authorship lines
- Specific about WHAT changed and WHY

**Examples:**

```
prevent race condition in user session cleanup
rate limiting middleware for API endpoints
improve error handling in payment flow
extract validation logic for reuse
```

#### `/dmv:commit-partial <what_to_commit>`

Commit a subset of changes based on a natural language description.

**What it does:**

- Identifies files matching the provided description
- Stages only relevant files automatically
- Generates appropriate commit message for the subset
- Follows same commit format as full commits

**Usage:**

```
/dmv:commit-partial documentation changes
```

Commits only markdown files and documentation updates.

```
/dmv:commit-partial all files related to authentication
```

Commits files related to authentication (auth modules, tests, etc.).

**Description examples:**

- "only test files"
- "changes to the API layer"
- "frontend components"
- "configuration files"

#### `/dmv:setup`

Set up the DMV plugin (install gh CLI and configure GitHub MCP server).

**What it does:**

- Checks for gh CLI installation
- Installs gh via Homebrew if needed (macOS)
- Verifies gh authentication status
- Validates GitHub MCP server configuration
- Provides step-by-step setup guidance

**Usage:**

```
/dmv:setup
```

Runs complete setup verification and guides you through any missing steps.

### Agents

#### `dmv:git-committer`

Executes git commit workflows including full commits and partial commits.

**Automatically invoked when:**

- User requests committing changes
- Creating commits with or without messages
- Commit operations are needed

**What it does:**

- Loads git-workflow skill for user preferences
- Analyzes repository state (git status, git diff)
- Handles full or partial file selection
- Generates terse commit messages when not provided
- Executes commits with proper formatting
- Handles pre-commit hook failures with single-retry pattern
- Verifies commit success

**Tools:** Bash, Read, Skill

**Model:** Sonnet

### Skills

#### `dmv:git-workflow`

User-specific git workflow preferences and edge case handling.

**What it provides:**

- Commit message format requirements (terse, no emojis, no attribution)
- Pre-commit hook retry logic for auto-formatting failures
- Quality checklist for commits
- Common pitfalls to avoid

**When to use:**

- Creating commits
- Handling pre-commit hook failures
- Understanding user's commit format preferences

**Key patterns:**

**Commit format:**

```
<brief specific description>
```

Not:

```
❌ add: new feature ✨
❌ fix: correct bug

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

**Pre-commit hook retry:**

When hooks auto-modify files during commit:

1. Commit fails (hook reformatted code)
2. Stage modified files: `git add .`
3. Retry ONCE: `git commit --amend --no-edit`
4. If second attempt fails, investigate hook configuration

#### `dmv:github-workflow`

Tool selection hierarchy for GitHub interactions and PR requirements.

**What it provides:**

- Decision hierarchy: gh CLI (preferred) → GitHub MCP server (fallback)
- Installation and authentication patterns
- Pull request requirements (no attribution)
- When to use each tool

**When to use:**

- Interacting with GitHub
- Creating pull requests
- Deciding between gh CLI and MCP server

**Tool selection pattern:**

```
Task requires GitHub interaction
├─ Is gh installed and available?
│  ├─ Yes → Check if gh supports this operation
│  │  ├─ Yes → USE gh CLI (preferred)
│  │  └─ No → USE GitHub MCP Server
│  └─ No → USE GitHub MCP Server
```

## Design Philosophy

### Terse Over Verbose

Commit messages are single-line, specific, and focused. No boilerplate, no attribution, no decoration.

**Why:** Fast to read, easy to scan, meaningful at a glance.

### Automation Over Manual

Pre-commit hook failures are handled automatically with single-retry pattern.

**Why:** Auto-formatting is common, retrying once is safe and saves time.

### Intelligent Tool Selection

Prefer gh CLI when available, fall back to GitHub MCP server when needed.

**Why:** Use the best tool for each task while maintaining compatibility.

### User-Specific Preferences

Skills document user's specific requirements, not general git knowledge.

**Why:** Claude already knows standard git - skills focus on the delta.

## Installation

### Prerequisites

- Git installed and configured
- Node.js (for GitHub MCP server)
- Homebrew (for installing gh CLI on macOS)

### From the Marketplace

1. Add the marketplace (if not already added):

   ```
   /plugin marketplace add /path/to/neat-little-package
   ```

2. Install the plugin:

   ```
   /plugin install dmv@neat-little-package
   ```

3. Run setup to configure:

   ```
   /dmv:setup
   ```

### GitHub MCP Server Setup

The plugin includes the official GitHub MCP server for advanced GitHub operations.

**Required:**

1. Create a GitHub Personal Access Token:
   - Visit <https://github.com/settings/tokens>
   - Generate a new token (classic) with `repo`, `read:org`, and `read:user` scopes

2. Set the token in your environment:

   ```bash
   export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_..."
   ```

   Add this to your shell profile (~/.zshrc or ~/.bashrc) to persist.

3. The MCP server will automatically start when the plugin is enabled

## Quick Start Guide

### Making Your First Commit

1. Make some changes to your repository
2. Run `/dmv:commit` to analyze and commit all changes
3. The git-committer agent will:
   - Analyze your changes via git status and git diff
   - Generate a terse, specific commit message
   - Stage all files
   - Create the commit
   - Handle any pre-commit hook failures automatically

### Committing Partial Changes

1. Make changes across multiple areas of your codebase
2. Run `/dmv:commit-partial documentation changes` to commit only docs
3. The agent will:
   - Identify files matching "documentation" (*.md, docs/ directory)
   - Stage only those files
   - Generate an appropriate commit message
   - Create the commit

### Setting Up GitHub Integration

1. Run `/dmv:setup` to verify your configuration
2. Follow any instructions for missing components:
   - Install gh CLI if needed
   - Authenticate with `gh auth login`
   - Set GITHUB_PERSONAL_ACCESS_TOKEN environment variable
3. Start using GitHub operations with intelligent tool selection

## Workflow Examples

### Daily Development Flow

```
# Make changes to multiple files
vim src/auth.ts src/api.ts tests/auth.test.ts

# Commit everything with generated message
/dmv:commit

# Continue working on documentation
vim README.md docs/api.md

# Commit just the docs
/dmv:commit-partial documentation updates
```

### Pre-Commit Hook Handling

```
# Attempt commit
/dmv:commit

# Hook auto-formats files, commit fails
# Agent automatically:
# 1. Stages the auto-formatted files
# 2. Retries commit once with --amend --no-edit
# 3. Succeeds without user intervention
```

### Custom Commit Messages

```
# When you know exactly what to say
/dmv:commit prevent race condition in session cleanup

# When you want the agent to analyze and suggest
/dmv:commit
```

## Component Design Patterns

### Skills: Knowledge Delta Filter

DMV skills only document what Claude doesn't already know:

- ✅ User-specific commit format preferences
- ✅ Pre-commit hook retry edge case
- ✅ Tool selection hierarchy
- ❌ Standard git commands (Claude knows these)
- ❌ General GitHub workflows (Claude knows these)

**Result:** Focused skills (~80-150 lines) that add real value.

### Agent: Autonomous Commit Handling

The git-committer agent operates autonomously:

- No user interaction during execution
- Analyzes changes intelligently
- Makes decisions based on context
- Handles failures with retry logic
- Returns complete results

**Pattern:** Load skills → Analyze → Execute → Handle failures → Verify → Return

### Commands: Thin Wrapper Delegation

DMV commands delegate to the specialized git-committer agent:

```
/dmv:commit → git-committer agent → git-workflow skill
```

**Why:** Commands stay simple, agents handle complexity, skills provide guidance.

## File Structure

```
plugins/dmv/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── .mcp.json               # GitHub MCP server config
├── agents/
│   └── git-committer.md    # Commit workflow agent
├── commands/
│   ├── commit.md           # Full commit command
│   ├── commit-partial.md   # Partial commit command
│   └── setup.md            # Setup command
├── skills/
│   ├── git-workflow/
│   │   └── SKILL.md        # User-specific git preferences
│   └── github-workflow/
│       └── SKILL.md        # GitHub tool selection
├── assets/
│   └── dmv.png            # Plugin logo
├── README.md              # User documentation
└── CLAUDE.md             # Development guidelines
```

## Troubleshooting

### Commit command not working

- Verify you're in a git repository: `git status`
- Check that files have changes: `git diff`
- Ensure plugin is installed: `/plugin list`
- Reinstall if needed: `/plugin uninstall dmv@neat-little-package && /plugin install dmv@neat-little-package`

### Pre-commit hook keeps failing

- Check if hook is modifying files or validating
- If modifying: Agent should retry automatically (check agent is loaded)
- If validating: Fix the validation errors, don't retry
- View hook output for specific error messages

### GitHub MCP server not working

- Verify GITHUB_PERSONAL_ACCESS_TOKEN is set: `echo $GITHUB_PERSONAL_ACCESS_TOKEN`
- Check token has correct scopes: `repo`, `read:org`, `read:user`
- Ensure Node.js is installed: `node --version`
- Restart Claude Code after setting environment variable

### gh CLI not found

- Run `/dmv:setup` to install gh CLI
- Or install manually: `brew install gh`
- Authenticate: `gh auth login`
- Verify installation: `gh --version`

### Commit messages don't match preferences

- Check that git-workflow skill is being loaded
- Verify agent is using the skill (should see skill loading in execution)
- Review skill content for format requirements
- Reinstall plugin if skill changes aren't taking effect

### Partial commits selecting wrong files

- Provide more specific descriptions
- Use file extensions: "only .ts files"
- Use paths: "changes in src/components/"
- Review git status output to see available files
- Agent will explain which files matched and why

## Resources

### Official Documentation

- **Claude Code Plugins**: <https://code.claude.com/docs/en/plugins>
- **Git Documentation**: <https://git-scm.com/docs>
- **GitHub CLI**: <https://cli.github.com/manual/>
- **GitHub API**: <https://docs.github.com/en/rest>
- **Pre-commit Framework**: <https://pre-commit.com/>

### Included Skills

- `dmv:git-workflow` - User-specific git preferences and edge cases
- `dmv:github-workflow` - GitHub tool selection hierarchy

### Related Tools

- **gh CLI** - GitHub's official command-line tool (preferred)
- **GitHub MCP Server** - Model Context Protocol integration (fallback)
- **Pre-commit** - Git hook framework for automated checks

## Examples

See the component files in this plugin for implementation examples:

- **Agent**: `agents/git-committer.md` - Autonomous commit handling
- **Commands**: `commands/commit.md`, `commands/commit-partial.md` - Thin wrapper delegation
- **Skills**: `skills/git-workflow/SKILL.md` - Knowledge delta filter applied
- **Skills**: `skills/github-workflow/SKILL.md` - Tool selection decision framework

## Version History

### 1.0.0

- Initial release
- Full commit workflow with smart message generation
- Partial commit workflow with natural language selection
- Pre-commit hook retry logic
- GitHub MCP server integration
- gh CLI installation and setup
- User-specific git and GitHub workflow skills
