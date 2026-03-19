---
name: update-box-factory
description: Review and update box-factory's skills and agents against current official docs. Fetches live specs, applies the knowledge delta filter, and proposes targeted edits. Use when it's time to check if box-factory is still current.
user-invocable: true
---

# Update Box Factory

Periodic review of box-factory's content against current official documentation. The goal is keeping box-factory lean and current — not comprehensive.

## Review Process

### Step 1: Fetch Current Docs

Fetch ALL of these in parallel — they are the source of truth:

- <https://agentskills.io/specification> — Universal AgentSkills spec
- <https://code.claude.com/docs/en/skills> — Claude Code skills docs
- <https://code.claude.com/docs/en/sub-agents> — Sub-agents docs
- <https://code.claude.com/docs/en/hooks> — Hooks docs
- <https://code.claude.com/docs/en/plugins> — Plugins docs
- <https://code.claude.com/docs/en/plugin-marketplaces> — Marketplaces docs
- <https://code.claude.com/docs/en/mcp> — MCP docs

### Step 2: Read Box Factory

Read all content under `plugins/box-factory/` — skills, agents, and assets. Discover files dynamically; don't assume a fixed list.

### Step 3: Diff Against the Delta Filter

For each piece of guidance in box-factory, ask:

1. **Is it still accurate?** Compare against fetched docs. Flag anything that contradicts current specs.
2. **Is it still needed?** If Claude would now get this right without the guidance (e.g., post-training knowledge caught up), flag for removal.
3. **Is anything missing?** Look for new conventions, patterns, or gotchas in the docs that box-factory should encode.

### Step 4: Apply the Addition Filter

This is the hard part. For every potential addition, apply these tests IN ORDER:

**Test 1 — Is it durable and divergent?**

A piece of guidance earns its place when it's (a) unlikely to change and (b) different from what Claude would do by default. Both conditions must hold.

- `.agents/skills/` as the cross-client discovery path → Foundational to the spec, diverges from Claude's default `.claude/skills/`. **Add it.**
- `maxTurns` frontmatter field for agents → A spec detail Claude can fetch when needed. **Skip it.**
- "Community prefers kebab-case skill names" → Claude would probably do this anyway, and the consequences of not doing it are trivial. **Skip it.**

**Test 2 — Would Claude get it wrong or do it non-standardly?**

"Wrong" includes producing something that works but doesn't match ecosystem conventions. A skill that functions but uses a non-standard structure creates silent friction.

- Empirically tested gotchas (like nested delegation not working) → Yes. Add it.
- Patterns where Claude's default diverges from ecosystem norms → Yes. Add it.
- Standard features that work as documented → No. Skip it.

**Test 3 — Is it a user preference or a spec fact?**

- User preferences (minimal plugin.json, no license field, 7-color list) → Keep these. They encode choices.
- Spec facts (what fields exist, what types are valid) → Don't add. The spec is the source of truth for its own facts.

### Step 5: Propose Changes

Present findings as a structured report:

```
## Stale (should update or remove)
- [file:line] [what's wrong] → [proposed fix]

## Missing (should add)
- [description] → [where it belongs and why it passes the delta filter]

## Confirmed Current
- [brief list of sections verified against current docs]
```

Wait for the user to approve each change before making edits. Do not batch-apply.

## Anti-Patterns to Avoid

- **Don't enumerate spec fields.** Box-factory's job is to encode gotchas, preferences, and conventions — not to be a mirror of the spec. If someone needs the field list, they fetch the spec.
- **Don't add guidance Claude already follows.** Test by asking: "Would Claude actually get this wrong?" If the answer is "probably not," skip it.
- **Don't remove empirical findings just because docs don't mention them.** The 7-color list and no-nested-delegation rule are empirically tested. Docs being silent on something doesn't make the guidance wrong.
- **Don't remove gotchas you're confident about.** Some box-factory guidance exists precisely because Claude is confident it knows better and is categorically wrong. If a section says "Claude consistently believes X but Y is true" or "empirically tested and confirmed," that guidance was added *because* of Claude's confidence, not despite it. Never remove it based on your own assessment that it should work — that assessment is the problem the guidance exists to correct.
- **Don't over-document new features.** A new feature existing is not reason enough to document it. Step 1 fetches the live spec every time this skill runs — new features are already visible. Box-factory only needs to capture what Claude would misuse, misunderstand, or miss despite having the spec in context.

## Scope

Review everything under `plugins/box-factory/` — all skills, agents, and assets. Do NOT review other plugins in the marketplace.
