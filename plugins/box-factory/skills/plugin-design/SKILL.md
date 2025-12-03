---
name: box-factory-plugin-design
description: Interpretive guidance for designing Claude Code plugins. Helps you understand plugin architecture, marketplace distribution, and when plugins are the right pattern. Use when creating or reviewing plugins.
---

# Plugin Design Skill

This skill provides interpretive guidance and best practices for creating Claude Code plugins. It helps you understand what the docs mean and how to create excellent plugins.

## Official Documentation

**Claude Code changes rapidly and is post-training knowledge.** Fetch these docs when creating plugins to ensure current syntax:

- **<https://code.claude.com/docs/en/plugins>** - Plugin overview and quickstart
- **<https://code.claude.com/docs/en/plugins-reference>** - Complete specifications
- **<https://code.claude.com/docs/en/plugin-marketplaces>** - Distribution patterns

## Core Understanding

### Plugins Are Packaging, Not Functionality

**Key insight:** Plugins don't add new capabilities to Claude Code. They package existing extension points (commands, agents, skills, hooks, MCP servers) for distribution.

**What this means:**

- Plugins bundle components together
- The value is distribution and discoverability
- Components work the same inside or outside plugins
- You're organizing and sharing, not creating new primitives

**Decision test:** If you're asking "should this be a plugin?", you're asking the wrong question. Ask "should I package these existing components for sharing?"

### Critical Directory Structure (Official Specification)

**The #1 mistake** that causes plugins to install but not work:

```
✅ Correct:
plugin-name/
├── .claude-plugin/
│   └── plugin.json     ← Only metadata here
├── commands/            ← At plugin root
├── agents/              ← At plugin root
├── skills/              ← At plugin root
└── hooks/               ← At plugin root

❌ Wrong (won't work):
plugin-name/
└── .claude-plugin/
    ├── plugin.json
    ├── commands/        ← Won't be found!
    └── agents/          ← Won't be found!
```

**Official docs say:** "All other directories (commands/, agents/, skills/, hooks/) must be at the plugin root, not inside `.claude-plugin/`."

### Skills Directory Structure

Skills use subdirectories with a `SKILL.md` file:

```
skills/
├── skill-one/
│   ├── SKILL.md         ← Skill definition
│   └── helpers.py       ← Supporting files (optional)
└── skill-two/
    └── SKILL.md
```

## Plugin Manifest (plugin.json) - Official Specification

Located at `.claude-plugin/plugin.json`:

### Required Fields

- **name**: Unique identifier in kebab-case (e.g., "deployment-tools")

### Optional Metadata Fields We Use

| Field | Type | Purpose |
|-------|------|---------|
| version | string | Semantic versioning (e.g., "2.1.0") |
| description | string | Brief plugin purpose explanation |
| repository | string | Source code location |

### Optional Metadata Fields We NEVER Use

| Field | Type | Purpose |
|-------|------|---------|
| author | object | Author details: `{name, email, url}` |
| homepage | string | Documentation URL |
| license | string | License identifier (MIT, Apache-2.0, etc.) |
| keywords | array | Discovery tags for categorization |

### Component Path Fields (Optional)

Override default locations:

- **commands**: Additional command files/directories (string or array)
- **agents**: Agent markdown files (string or array)
- **hooks**: Hook configuration path or inline JSON
- **mcpServers**: MCP server configuration path or inline JSON

**Note:** Custom paths *supplement* default directories, they don't replace them.

**Best practice:** Always include `description` and `version` even though they're optional - improves discoverability and user trust. Do NOT include `author`, `repository`, `homepage`, `license`, or `keywords` unless explicitly specified.

## Advanced Features (Official Specification)

### Environment Variables

Use `${CLAUDE_PLUGIN_ROOT}` in paths to reference the plugin's absolute directory.

### Custom Component Paths

Specify additional locations for components:

```json
{
  "name": "my-plugin",
  "commands": ["./extra-commands", "./legacy/commands"],
  "agents": "./custom-agents"
}
```

All paths must be relative to plugin root and start with `./`

### Inline Component Configuration

Define hooks or MCP servers directly in plugin.json instead of separate files:

```json
{
  "name": "my-plugin",
  "hooks": {
    "PreToolUse:Bash": "./hooks/bash-guard.sh"
  },
  "mcpServers": {
    "custom-server": {
      "command": "node",
      "args": ["./server.js"]
    }
  }
}
```

### MCP Server Configuration (Best Practices)

**CRITICAL:** When configuring MCP servers in plugins, follow these security and maintainability patterns.

#### Always Use External Configuration Files

**✅ CORRECT - External file:**

```json
// plugin.json
{
  "name": "my-plugin",
  "mcpServers": "./.mcp.json"
}
```

```json
// .mcp.json (at plugin root)
{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
    }
  }
}
```

**❌ WRONG - Inline configuration:**

```json
{
  "name": "my-plugin",
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": ""
      }
    }
  }
}
```

**Why external files are better:**

- Separation of concerns (metadata vs configuration)
- Easier to edit MCP config independently
- Cleaner plugin.json focused on plugin metadata
- Matches user expectations from standalone MCP setups

#### Always Use Environment Variable References

**✅ CORRECT - Environment variable reference:**

```json
{
  "server-name": {
    "command": "server-binary",
    "env": {
      "API_KEY": "${API_KEY}",
      "AUTH_TOKEN": "${AUTH_TOKEN}",
      "DATABASE_URL": "${DATABASE_URL}"
    }
  }
}
```

**❌ WRONG - Hardcoded empty strings:**

```json
{
  "server-name": {
    "env": {
      "API_KEY": "",
      "AUTH_TOKEN": "",
      "DATABASE_URL": ""
    }
  }
}
```

**❌ VERY WRONG - Hardcoded actual secrets:**

```json
{
  "server-name": {
    "env": {
      "API_KEY": "sk_live_abc123..."
    }
  }
}
```

**Why environment variables are critical:**

- **Security**: Never commit secrets to git history
- **Portability**: Different users/environments have different credentials
- **Standard practice**: `${VAR_NAME}` is the established MCP pattern
- **Documentation clarity**: Shows what env vars are required

#### Document Required Environment Variables

**In your README, always include:**

```markdown
## MCP Server Setup

This plugin includes the [Server Name] MCP server.

### Prerequisites

- [Tool requirements, e.g., Node.js, Python]
- [Service account or API access]

### Configuration

1. Obtain credentials:
   - Visit [credential URL]
   - Create [token/API key] with `scope1`, `scope2` permissions

2. Set environment variables:
   ```bash
   export API_KEY="your_key_here"
   export AUTH_TOKEN="your_token_here"
   ```

1. The MCP server will start automatically when the plugin is enabled

```

**Required documentation elements:**
- Prerequisites (tools, accounts, permissions)
- How to obtain credentials with specific scopes/permissions
- Exact environment variable names to set
- Example export commands
- When the server starts (usually: when plugin enabled)

#### Common MCP Server Types

**GitHub:**
```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
    }
  }
}
```

**Filesystem:**

```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"],
    "env": {}
  }
}
```

**Database:**

```json
{
  "database": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres"],
    "env": {
      "DATABASE_URL": "${DATABASE_URL}"
    }
  }
}
```

**Custom server using plugin root:**

```json
{
  "custom": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/custom-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
    "env": {
      "CUSTOM_API_KEY": "${CUSTOM_API_KEY}"
    }
  }
}
```

#### MCP Configuration Checklist

Before publishing plugin with MCP servers:

**Security:**

- ✓ All secrets use `${ENV_VAR}` references (never hardcoded)
- ✓ No empty string placeholders for secrets
- ✓ No actual credentials in git history
- ✓ .env files in .gitignore if used for local testing

**Structure:**

- ✓ MCP configuration in external file (`.mcp.json` or custom path)
- ✓ Path in plugin.json is relative and starts with `./`
- ✓ Valid JSON syntax in MCP configuration file

**Documentation:**

- ✓ README explains how to obtain credentials
- ✓ Required scopes/permissions documented
- ✓ Environment variable names clearly listed
- ✓ Example export commands provided
- ✓ Troubleshooting section for common issues

**Testing:**

- ✓ Verified MCP server starts with plugin enabled
- ✓ Tested with actual credentials in environment
- ✓ Confirmed required tools/dependencies work

## Marketplace Distribution (Official Specification)

### Marketplace.json Structure

Located at `.claude-plugin/marketplace.json`:

**Required fields:**

- **name**: Marketplace identifier (kebab-case)
- **owner**: Maintainer information object
- **metadata.pluginRoot**: Base path for resolving plugin sources (use `".."` since marketplace.json is in `.claude-plugin/`)
- **plugins**: Array of plugin entries

**Example marketplace:**

```json
{
  "name": "marketplace-name",
  "owner": { "name": "owner-name", "url": "https://..." },
  "metadata": {
    "pluginRoot": ".."
  },
  "plugins": [...]
}
```

**Plugin entry fields:**

```json
{
  "name": "plugin-name",
  "source": "./plugins/plugin-name",
  "description": "Optional override",
  "strict": true
}
```

**Path resolution:** Plugin source paths are resolved relative to `pluginRoot`. Since marketplace.json lives in `.claude-plugin/`, the `".."` tells Claude Code to go up one level to the repository root before resolving `./plugins/...` paths.

### Source Types

**Local path (development):**

```json
"source": "./plugins/my-plugin"
```

**GitHub repository:**

```json
"source": {
  "source": "github",
  "repo": "owner/repo"
}
```

**Git URL:**

```json
"source": {
  "source": "url",
  "url": "https://gitlab.com/user/plugin.git"
}
```

### The `strict` Field

- **`strict: true`** (default): Plugin must have its own `plugin.json`
- **`strict: false`**: Marketplace entry serves as complete manifest

**Use `strict: false` when:** Packaging third-party content without modifying it.

## Decision Framework

### When to Create a Plugin

**Create plugin when:**

- You have multiple related components (commands + agents + hooks)
- You want to share with team/community
- You need versioning and distribution
- You want one-command installation (`/plugin install`)

**Don't create plugin when:**

- Single command/agent (just share the file)
- Personal workflow (no distribution need)
- Rapid iteration (plugins add packaging overhead)
- Testing concepts (develop components first, package later)

### Plugin Scope Philosophy (Best Practices)

**Good plugin scope:**

- Focused purpose (testing suite, security scanner, docs generator)
- Related components work together
- Clear value proposition
- Composable with other plugins

**Bad plugin scope:**

- "Everything for development" (too broad)
- Unrelated utilities thrown together
- Duplicates core functionality
- Conflicts with other plugins

## Development Workflow (Best Practices)

The docs show the mechanics. Here's the philosophy:

1. **Build components first** - Create and test commands/agents individually
2. **Test without packaging** - Use `.claude/` directories for iteration
3. **Package when ready** - Add plugin.json and organize structure
4. **Validate locally** - Use `claude plugin validate .` command
5. **Create test marketplace** - Local marketplace with absolute paths
6. **Install and test** - `/plugin marketplace add ./path/to/marketplace`
7. **Iterate** - Fix issues, restart Claude Code, test again
8. **Document** - Write focused README (components, installation, basic usage)
9. **Publish** - Push to GitHub, share marketplace

**Key insight:** Don't start with plugin structure. Build components, then package them.

## Testing Plugin Scripts (Best Practices)

**Key constraint:** Claude Code plugins distribute via git clone - you can't exclude files like npm's `.npmignore` or Python's `pyproject.toml` exclusions.

### Recommended Approach

**Keep tests in the repo** but minimize their footprint:

```text
my-plugin/
├── .claude-plugin/plugin.json
├── hooks/
│   └── my-hook.py
├── tests/                    # Development tests
│   └── test_my_hook.py       # Lightweight, focused
└── README.md                 # Document that tests/ is for dev
```

**Guidelines:**

- Use a single `tests/` directory at plugin root
- Keep test files small (avoid heavy fixtures or data files)
- Prefer inline test data over separate fixture files
- Document in README that `tests/` is for development only

### Why Include Tests?

The disk space impact is negligible for most plugins:

- Plugin scripts are typically small (a few KB)
- Test files are similarly small
- Users benefit from knowing the plugin is tested
- Tests serve as documentation of expected behavior

### Testing Executable Scripts (Hooks)

For Python hook scripts using UV:

```bash
# Run tests directly
python -m pytest tests/

# Or test the hook script itself
echo '{"tool_name": "Write", "tool_input": {"file_path": "test.py"}}' | ./hooks/my-hook.py
```

For bash hooks:

```bash
# Test with sample input
echo '{"tool_name": "Bash"}' | ./hooks/my-hook.sh
echo $?  # Check exit code
```

**Best practice:** Test hooks with realistic stdin JSON matching what Claude Code provides.

## Testing Commands (Official Specification)

**Validate plugin structure:**

```bash
claude plugin validate .
```

Checks JSON syntax and directory structure.

**Add local marketplace for testing:**

```bash
/plugin marketplace add ./absolute/path/to/marketplace
```

**Install from local marketplace:**

```bash
/plugin install plugin-name@marketplace-name
```

**Verify installation:**

Check `/help` for newly installed commands and agents.

## Common Pitfalls (Best Practices)

### Pitfall #1: Components in Wrong Directory

**Problem:** Putting commands/agents inside `.claude-plugin/`

**Why it fails:** Claude Code only looks at plugin root for components

**Solution:** Keep `.claude-plugin/` for metadata only, put all components at root

### Pitfall #2: Premature Pluginification

**Problem:** Creating plugin for single command or concept

**Why it fails:**

- Overhead of marketplace setup
- Harder to iterate quickly
- Users just want the file
- More complex to maintain

**Better:** Share the markdown file directly, create plugin later if collection grows

### Pitfall #3: Kitchen Sink Plugin

**Problem:** "All my utilities" plugin with unrelated components

**Why it fails:**

- Unclear purpose
- Users only want subset
- Hard to maintain and version
- Discovery problems

**Better:** Focused plugins (testing tools, git helpers, docs generators)

### Pitfall #4: Missing Documentation

**Problem:** Plugin without README or usage examples

**Why it fails:**

- Users don't know what's included
- No installation instructions

**Solution:** Focused README with:

- Brief description
- Component list
- Installation (if external tools needed)
- Basic usage example

**Anti-pattern:** Don't over-document. No roadmaps, planned features, or verbose error handling sections.

### Pitfall #5: Ignoring Semantic Versioning

**Problem:** Breaking changes in minor/patch versions

**Why it fails:** Users expect:

- `1.0.0 → 1.0.1` - Bug fixes only, safe to auto-update
- `1.0.0 → 1.1.0` - New features, backward compatible
- `1.0.0 → 2.0.0` - Breaking changes, needs migration

**Solution:** Follow semver strictly, document breaking changes

## Marketplace Organization (Best Practices)

### Embedded vs External Plugins

**Embedded (monorepo approach):**

```
marketplace/
├── .claude-plugin/marketplace.json
└── plugins/
    ├── plugin-one/
    └── plugin-two/
```

**Pros:**

- Single source of truth
- Atomic updates
- Easier testing

**Cons:**

- Monorepo management overhead
- Slower independent development

**External (distributed approach):**

```json
{
  "plugins": [
    {
      "name": "plugin-one",
      "source": {
        "source": "github",
        "repo": "org/plugin-one"
      }
    }
  ]
}
```

**Pros:**

- Independent versioning
- Faster iteration
- Individual repos easier to manage

**Cons:**

- Dependency coordination
- Potential version conflicts

### Team Distribution Strategy

**Official mechanism:** Configure `.claude/settings.json` at repository level:

```json
{
  "extraKnownMarketplaces": ["owner/marketplace-repo"],
  "enabledPlugins": ["plugin-name@marketplace-name"]
}
```

**Best practices to consider:**

- Test plugins thoroughly before team rollout
- Document required environment variables
- Have rollback plan if plugin breaks
- Establish approval process for new plugins
- Communicate plugin updates to team

## Plugin Quality Checklist

Before publishing:

**Structure (from official docs):**

- ✓ Valid `plugin.json` at `.claude-plugin/plugin.json`
- ✓ Components at plugin root (not in `.claude-plugin/`)
- ✓ Proper directory names (commands, agents, skills, hooks)
- ✓ `claude plugin validate .` passes
- ✓ Relative paths start with `./`

**Metadata (best practices):**

- ✓ Descriptive name (kebab-case)
- ✓ Clear description (what problem it solves)
- ✓ Semantic versioning
- ✓ Author info (for support)
- ✓ Repository link (for issues/PRs)
- ✓ Keywords for discovery

**Documentation (best practices):**

- ✓ Focused README (not comprehensive)
- ✓ Component list with brief descriptions
- ✓ Installation only if external tools required
- ✓ Basic usage example
- ✗ No roadmaps or planned features
- ✗ No verbose error handling docs

**Design (best practices):**

- ✓ Focused scope (clear purpose)
- ✓ No duplication of core functionality
- ✓ Components complement each other
- ✓ Tested locally before publishing

## Example: High-Quality Plugin Manifest

**Basic (what docs show):**

```json
{
  "name": "my-plugin",
  "description": "A plugin",
  "version": "1.0.0"
}
```

**Issues:**

- ❌ Vague description

**Excellent (applying best practices):**

```json
{
  "name": "python-testing-suite",
  "version": "1.0.0",
  "description": "Comprehensive Python testing tools with pytest integration, coverage reporting, and failure analysis",
  "repository": "https://github.com/username/python-testing-suite",
}
```

**Improvements:**

- ✅ Specific description (what it does, how it helps)
- ✅ (optional, but okay)Repository for issues and PRs

## Documentation References

Authoritative sources for plugin specifications:

**Plugin creation:**

- <https://code.claude.com/docs/en/plugins> - Overview and quickstart

**Complete specifications:**

- <https://code.claude.com/docs/en/plugins-reference> - All schemas and patterns

**Distribution:**

- <https://code.claude.com/docs/en/plugin-marketplaces> - Marketplace setup

**Component specifications:**

- Reference agent-design, slash-command-design skills for component details

**Remember:** Official docs provide structure and features. This skill provides best practices and patterns for creating excellent plugins.
