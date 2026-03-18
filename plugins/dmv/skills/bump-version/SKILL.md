---
name: bump-version
description: Bump the version and release. Use when the user says /bump-version, "bump version", "cut a release", or "release".
argument-hint: [optional: major|minor|patch]
---

# Bump Version

Analyze recent changes and bump the project version.

## Step 1: Find the current version

Check for version manifests in priority order. Use the **first** match:

1. `package.json` → `.version`
2. `pyproject.toml` → `[project] version`
3. `Cargo.toml` → `[package] version`
4. `.claude-plugin/plugin.json` → `.version`
5. No manifest → latest git tag matching `v*.*.*` (fall back to `v0.0.0`)

## Step 2: Review changes since that version

- If the repo uses version tags, review commits since the last tag: `git log <tag>..HEAD --oneline`
- If no tags, review recent commits: `git log --oneline -20`

## Step 3: Determine bump type

Unless `$ARGUMENTS` specifies `major`, `minor`, or `patch`:

- **major**: breaking changes — removed commands, changed CLI flags/behavior, renamed packages, changed install paths, removed public API
- **minor**: new features — new commands, new flags, new capabilities, new files that add functionality
- **patch**: bug fixes, documentation, refactoring, test changes, dependency updates

## Step 4: Confirm with user

Tell the user:

- Current version
- What changed (brief summary)
- Proposed bump type and new version

**Wait for confirmation before proceeding.**

## Step 5: Apply the bump

1. **Edit the manifest** with the new version using the Edit tool. If no manifest exists, skip this step.
2. **Commit** the manifest change: `bump version to v<new>`
3. **Tag** — only if the repo already uses version tags (i.e., `git tag` has `v*.*.*` entries). Do not introduce tags to a repo that doesn't use them.
4. **Push** with `git pub --tags` (or `git pub` if no tag was created).
