# Gitting

Streamline git and GitHub workflows with integrated CLI tools and MCP server support.

## Installation

1. Install the plugin by adding it to your Claude Code marketplace configuration
2. Configure the GitHub MCP server (see MCP Server Setup below)
3. Optionally install GitHub CLI using `/gitting:install-gh`

## MCP Server Setup

The plugin includes the official GitHub MCP server for advanced GitHub operations.

### Prerequisites

- Node.js installed (for running npx)
- GitHub Personal Access Token with appropriate permissions

### Configuration

1. Create a GitHub Personal Access Token:
   - Visit https://github.com/settings/tokens
   - Generate a new token (classic) with `repo`, `read:org`, and `read:user` scopes

2. Set the token in your environment:
   ```bash
   export GITHUB_PERSONAL_ACCESS_TOKEN="your_token_here"
   ```

3. The MCP server will automatically start when the plugin is enabled

## Components

### Skills

- **git-workflow** - Git usage patterns, best practices, and commit strategies
- **github-workflow** - GitHub interaction patterns, preferring gh CLI with MCP fallback

### Slash Commands

- **/gitting:commit [commit_message]** - Commit all changes with smart message generation
  - Stages all changes
  - Generates terse commit message if not provided
  - Handles pre-commit hook failures automatically
  - No emojis or attribution added

- **/gitting:install-gh** - Install GitHub CLI via Homebrew

## Usage Examples

### Quick Commit

```
/gitting:commit
```

Analyzes staged and unstaged changes, generates a brief commit message, and commits everything.

### Commit with Custom Message

```
/gitting:commit refactor user authentication flow
```

Commits all changes with the provided message.

### Install GitHub CLI

```
/gitting:install-gh
```

Installs the gh CLI tool if not already present.

## Requirements

- Git installed
- Node.js (for GitHub MCP server)
- GitHub Personal Access Token (for MCP server)
- Homebrew (for installing gh CLI)

## GitHub Interaction Pattern

This plugin follows a smart GitHub interaction strategy:

1. **Prefer gh CLI**: Use the gh tool when available and it supports the use case
2. **Fall back to MCP**: Use the GitHub MCP server when gh is unavailable or doesn't support the operation

This ensures maximum compatibility and leverages the best tool for each task.
