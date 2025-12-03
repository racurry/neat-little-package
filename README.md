# Everything Is Wrapped Up In a Neat Little Package

![Sorry if it sounded sarcastic](assets/really-i-mean-that.png)

A collection of Claude Code plugins.

## Set up

```bash
 # Add the marketplace
/plugin marketplace add racurry/neat-little-package

# Browse the plugins
/plugin 

# Install em
/plugin install hello-world@neat-little-package

# Use the thing
/hello
```

## Plugins

- [box-factory](plugins/box-factory/README.md): A toolkit for creating and managing Claude Code components (plugins, commands, skills, hooks)
- [dmv](plugins/dmv/README.md): Manage your git and github workflows and preferences
- [mr-sparkle](plugins/mr-sparkle/README.md): Nice clean code.  Linting & autoformatting.

## Automated Documentation Maintenance

A GitHub Actions workflow runs bi-weekly using the [Claude GitHub App](https://code.claude.com/docs/en/github-actions) to keep Box Factory skills current with Claude Code documentation changes.

**What it does:** Fetches official docs, compares against skills, and creates PRs with surgical updates when decision frameworks or best practices need revision. Respects Box Factory's philosophy: no syntax duplication, knowledge delta filter applied.

**Setup:** Add `ANTHROPIC_API_KEY` to repository secrets

**Run manually:** `gh workflow run check-documentation.yml` (add `-f dry_run=true` to preview changes)

## Refs

- [Official Plugin Documentation](https://code.claude.com/docs/en/plugins)
