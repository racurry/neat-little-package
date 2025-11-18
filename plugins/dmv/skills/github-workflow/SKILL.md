---
name: github-workflow
description: Tool selection hierarchy for GitHub interactions (gh CLI vs MCP server) and user's PR requirements. Use when interacting with GitHub or creating pull requests.
---

# GitHub Workflow Skill

This skill documents tool selection patterns and user preferences for GitHub interactions. For standard GitHub workflows, Claude relies on base training.

## Tool Selection Hierarchy (Decision Framework)

**Two GitHub integration tools are available:**

1. **gh CLI** - GitHub's official command-line tool (user-installed)
2. **GitHub MCP Server** - Model Context Protocol integration (configured via `.mcp.json`)

**Decision hierarchy:**

```
Task requires GitHub interaction
├─ Is gh installed and available?
│  ├─ Yes → Check if gh supports this operation
│  │  ├─ Yes → USE gh CLI (preferred)
│  │  └─ No → USE GitHub MCP Server
│  └─ No → USE GitHub MCP Server
```

**Prefer gh CLI for:**

- Creating/managing pull requests
- Creating/managing issues
- Release management
- Reviewing PRs and addressing feedback
- Checking CI/build status and failures
- Reading PR comments and review feedback
- Any well-supported interactive workflow

**Use MCP Server for:**

- When gh is not installed
- Complex search queries across repos
- Bulk data retrieval
- Operations gh doesn't support
- Lower-level API access needs

## Installation Check Pattern (Required Before Using gh)

**Always check gh availability before using:**

```bash
which gh  # Returns path if installed, empty if not
```

**If gh not found:**

- Use `/dmv:install-gh` command (installs via Homebrew on macOS)
- Or fall back to GitHub MCP Server
- Or guide user to install manually

**Verify authentication:**

```bash
gh auth status  # Check if authenticated
```

**If not authenticated:**

```bash
gh auth login  # Interactive authentication flow
```

## Pull Request Requirements (User Preference)

**This user wants PRs WITHOUT attribution:**

**Good PR body structure:**

```bash
gh pr create --title "fix: specific description" --body "$(cat <<'EOF'
## Summary
- Bullet points of what changed and why

## Test Plan
- [ ] Specific testing step 1
- [ ] Specific testing step 2
- [ ] Manual testing completed

Fixes #123
EOF
)"
```

**User does NOT want:**

- NO "Generated with [Claude Code](https://claude.com/claude-code)" footer
- NO attribution text
- NO emojis in PR titles

**Include in PRs:**

- Clear summary of changes
- Why the change is needed
- Test plan with checkboxes
- Related issues (Fixes #XXX)
- Screenshots for UI changes (if applicable)

## GitHub MCP Server Setup

**Requires environment variable:** `GITHUB_PERSONAL_ACCESS_TOKEN`

**Check if configured:**

```bash
echo $GITHUB_PERSONAL_ACCESS_TOKEN  # Should show token
```

**If not set, guide user:**

1. Create token at <https://github.com/settings/tokens>
2. Grant scopes: `repo`, `read:org`, `read:user`
3. Set environment variable:

   ```bash
   export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_..."
   ```

## When gh vs MCP is Unclear

**Examples of edge cases:**

- **Task:** Create a PR → Prefer gh CLI (better UX, standard operation)
- **Task:** Search issues across 10 repos → Use MCP Server (bulk query)
- **Task:** Get PR comments → Either works, prefer gh if available
- **Task:** Complex GraphQL query → Use MCP Server (lower-level access)

**General rule:** If gh supports it well and is installed, use gh. Otherwise use MCP.

## Documentation References

When you need specific syntax:

- **gh CLI:** <https://cli.github.com/manual/> - Official gh command reference
- **GitHub API:** <https://docs.github.com/en/rest> - For MCP server capabilities
- **MCP Server:** Check `.mcp.json` configuration for available tools
