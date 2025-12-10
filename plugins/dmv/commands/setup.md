---
description: Set up the DMV plugin (install gh CLI and configure GitHub MCP server)
allowed-tools: Bash, Read
---

Set up everything needed for the DMV plugin to work properly.

**Step 1: GitHub CLI Installation**

Check if gh CLI is installed:

- Run `which gh` to check if gh is available
- If not found, install via Homebrew: `brew install gh`
- If Homebrew is not available, provide platform-specific installation instructions
- Verify installation: `gh --version`

**Step 2: GitHub CLI Authentication**

Check and configure gh authentication:

- Run `gh auth status` to check current authentication state
- If unauthenticated, stop and report to the user that they need to run `gh auth login` and set up gh.

**Step 3: GitHub MCP Server Configuration**

Verify the GitHub MCP server setup:

- Check if GITHUB_PERSONAL_ACCESS_TOKEN environment variable is set: `echo $GITHUB_PERSONAL_ACCESS_TOKEN`
- If not set, provide instructions for creating a GitHub personal access token:
  - Visit <https://github.com/settings/tokens>
  - Create a new token with `repo` scope for full repository access
  - Set the environment variable in the user's shell profile (e.g., ~/.zshrc or ~/.bashrc)
- Verify the MCP configuration file exists in the plugin directory (.mcp.json)
- Explain that the MCP server will be available after Claude Code restarts

**Step 4: Verification Summary**

Provide a summary of:

- gh CLI installation status and version
- gh CLI authentication status
- GITHUB_PERSONAL_ACCESS_TOKEN environment variable status
- MCP server configuration file status
- Any remaining manual steps the user needs to complete

**Note:** The gh auth login command requires interactive terminal input and cannot be automated. Guide the user to run it manually if needed.
