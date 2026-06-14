---
name: update-box-factory
description: Verification discipline for auditing this repo's components against CURRENT Claude / Claude Code reality and the user's preferences, plus the routine for keeping box-factory current. Find spec/guidance deltas, verify them empirically (don't trust the docs OR your own assumptions), push back on the user, record evidence. Use when auditing the repo, "make sure this is right", checking for drift, or updating box-factory.
user-invocable: true
---

# Update & Verify Box Factory

This repo captures two things: what Claude gets wrong, and the user's personal preferences. Both drift — Claude ships new models and Claude Code ships capabilities constantly. This skill keeps the repo true to reality, with box-factory as the primary (most drift-prone) target.

**The failure mode this exists to prevent:** confidently asserting a finding — from your training, your memory, or a subagent's "I checked the docs" summary — that turns out to be wrong. It has already happened here (a doc-scrape got nested-delegation, `commands/`, and `.agents/skills/` backwards in one pass). Assume it will happen again. You are the thing most likely to be confidently incorrect.

## Core discipline: distrust your own findings

- Treat everything you produce — and everything a subagent reports — as a **hypothesis**, not a finding, until verified.
- Find the delta, then try to **disprove it**. "X changed" deserves the same scrutiny as "X is fine."
- The **user is a verification source**, not just the audience — they have lived experience the docs lack. When they push back, re-verify. Don't fold just because they pushed, and don't dig in past contrary evidence.

## Verification hierarchy (higher wins)

1. **Empirical runtime test** — what actually happens in *this* runtime
2. **Verbatim official doc** — the *right* page, quoted, not your memory of it
3. **General knowledge / training / memory** — weakest; a hypothesis at best

When a higher tier contradicts a lower one, the higher wins — **including the runtime contradicting the docs.** Worked example: the sub-agents doc says a subagent with `Agent` in `tools` can spawn nested subagents; the runtime strips it anyway and it cannot. Runtime wins; box-factory is *right* to assert this against the docs. A blanket "always defer to the docs" rule would itself introduce bugs.

## Two kinds of "right" — handle them differently

- **Platform facts** (colors, tool/field names, hook formats, capabilities, what's legacy): drift with releases. **Re-verify every audit.** Never assume your training is current.
- **User preferences** (terse READMEs, no attribution, minimal plugin.json, CLI-over-MCP, knowledge-delta, narrow/opinionated scope): stable. **Treat as ground truth.** Do not "correct" them toward generic best practice — the opinionated narrowness is the point. Change only when the *user* changes them.

box-factory's hardcoded rules are deliberate: they live where the docs are wrong or Claude routinely misbehaves. **Don't de-hardcode them in the name of "fetch the spec."** The fix for drift is re-verification (this skill), not removal.

## Empirical verification methods

- **Fetch the right doc, quote it.** The `/specification` page is often not the whole story — check client-implementation, per-client, and reference pages too. Quote verbatim.
- **Spawn an ephemeral test.** For runtime behavior, write a throwaway test agent/skill, run it, delete it.
- **Two-phase restart-to-load.** New agents/skills are discovered at session start. Phase 1: write the test + ask the user to restart. Phase 2: invoke it, report, clean up the artifacts.
- **Defeat fabrication.** A subagent can *claim* a success it didn't achieve. Plant a secret token in a file it can only reach via the path under test, and forbid shortcuts. A negative result (capability absent) is more trustworthy than a claimed positive.
- **Test the exact conditions of the claim.** Don't generalize from the easy case.
- **Subagent caveat.** Subagents are great for fanning out reads, but a subagent told to "check the docs" returns a doc-scrape that can be confidently wrong — especially on **negatives** ("not in the spec"). Verify its claims.

### Procedure: nested-delegation test

The recurring battleground (docs claim it works; runtime strips it). To re-verify after a Claude update:

1. Write `.claude/agents/nested-tester.md` with `tools: Agent, Read, Bash` instructing it to spawn a nested subagent that reads a secret-token file.
2. Ask the user to restart, then invoke it.
3. Expected today: `COULD_NOT_SPAWN` (no Agent tool, even though declared). If it ever returns the token, nested delegation now works and box-factory's claim needs softening.
4. Delete the test agent + token file.

### Procedure: color test

To re-verify which agent colors render: write one test agent per candidate color, restart, observe which load. Current verified set is 8: `red, green, blue, yellow, purple, orange, pink, cyan`.

## Confidence labels (when reporting findings)

Tag every delta: **VERIFIED** (empirical/quoted) / **DOC-ONLY** (untested) / **ASSUMPTION** (unverified) / **PENDING** (test set up, awaiting restart). Never assert DOC-ONLY or ASSUMPTION as fact. Record findings and dated evidence in `ASSESSMENT.md`; save a memory when you hit a recurring confidently-wrong trap.

## Box-factory review routine

### Step 1: Fetch current docs

Fetch ALL of these in parallel — source of truth:

- <https://agentskills.io/specification> — Universal AgentSkills spec
- <https://code.claude.com/docs/en/skills> — Claude Code skills docs
- <https://code.claude.com/docs/en/sub-agents> — Sub-agents docs
- <https://code.claude.com/docs/en/hooks> — Hooks docs
- <https://code.claude.com/docs/en/plugins> — Plugins docs
- <https://code.claude.com/docs/en/plugin-marketplaces> — Marketplaces docs
- <https://code.claude.com/docs/en/mcp> — MCP docs

### Step 2: Read box-factory

Read all content under `plugins/box-factory/` — skills, agents, assets. Discover files dynamically.

### Step 3: Diff against the delta filter

For each piece of guidance: (1) **Still accurate?** vs fetched docs — but remember a doc-vs-box-factory conflict may mean the *doc* is wrong (verify empirically before "correcting" box-factory). (2) **Still needed?** If Claude now gets it right without the guidance, flag for removal — but verify that claim, don't assume it. (3) **Anything missing?**

### Step 4: Apply the addition filter

For every potential addition, in order:

1. **Durable and divergent?** Earns its place only if (a) unlikely to change AND (b) different from Claude's default. (`.agents/skills/` cross-client convention → add. A fetchable spec field → skip.)
2. **Would Claude get it wrong or do it non-standardly?** Empirically-tested gotchas (nested delegation) and ecosystem-norm divergences → add. Standard features that work as documented → skip.
3. **User preference or spec fact?** Preferences (minimal plugin.json, no license, the color list) → keep. Spec facts (what fields exist) → don't mirror the spec.

### Step 5: Propose changes

Structured report — **Stale** (file:line → fix), **Missing** (→ where + why it passes the filter), **Confirmed current**. Wait for approval per change; do not batch-apply.

## Anti-patterns to avoid

- **Don't enumerate spec fields.** box-factory encodes gotchas, preferences, conventions — not a mirror of the spec.
- **Don't add guidance Claude already follows.** Ask "would Claude actually get this wrong?" If probably not, skip.
- **Don't remove empirical findings just because docs don't mention them — or contradict them.** The color list and no-nested-delegation rule are empirically grounded. The docs *contradicting* a finding doesn't make the finding wrong; re-test before changing.
- **Don't remove gotchas you're confident about.** Some guidance exists precisely because Claude is confident it knows better and is categorically wrong ("Claude consistently believes X but Y is true" / "empirically tested and confirmed"). Never remove it based on your own assessment that it should work — that assessment is the problem the guidance corrects.
- **Don't over-document new features.** Step 1 fetches the live spec every run; new features are already visible. Only capture what Claude would misuse, misunderstand, or miss despite having the spec.

## Scope

box-factory is the primary, deepest target (Steps 1–5). The verification discipline above applies to **any** component in the repo when the user asks to audit or "make sure this is right."
