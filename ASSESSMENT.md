# neat-little-package — Assessment

> Strategic read of the marketplace as tools have evolved. Working doc — hunt and peck across sessions.
> Date: 2026-06-14. box-factory section re-verified empirically; the rest re-classified by confidence. Cross-ecosystem plan lives in [docs/cross-ecosystem.md](docs/cross-ecosystem.md).

## Confidence legend

Every load-bearing claim is tagged. Don't act on `[ASSUMPTION]` / `[DOC-ONLY]` / `[ESTIMATE]` without verifying first — see the `update-box-factory` skill.

- **[VERIFIED]** — empirical test or primary source (file read, git log, quoted doc)
- **[DOC-ONLY]** — docs say so; not tested in this runtime
- **[ESTIMATE]** — a rough number, not measured
- **[ASSUMPTION]** — my read/reasoning, unverified
- **[SUBAGENT]** — derived from a subagent's report, not spot-checked (treat as hypothesis)

## TL;DR

Your friction list is half real, half already-resolved.

- **MCP bloat + skill bloat** are mostly *perception* for this marketplace. `[VERIFIED]` `enabledPlugins` already splits dev from hobby; progressive disclosure keeps skill bodies out of context until triggered. `[VERIFIED]` the deferred-tool dumps are a Claude-desktop-app artifact (all connectors shown), not this marketplace.
- **box-factory mostly holds up.** `[VERIFIED]` My first-pass "drifted into wrong" was overstated. Commands-are-legacy, `.agents/skills/`, and nested-delegation are all correct — box-factory was right, I was wrong. The color list (the one real drift) is now fixed: `pink` added, 8 total.
- **The real open question is portability.** `[VERIFIED]` spirograph has zero Claude-specific features (no hooks/agents/mcp) so it's structurally portable knowledge trapped in a Claude wrapper. See [docs/cross-ecosystem.md](docs/cross-ecosystem.md).

## Two reframes

### 1. This marketplace is a light context citizen

`[VERIFIED]` `~/.claude/settings.json` `enabledPlugins`: **`box-factory`, `dmv`, `mr-sparkle` are globally enabled. `spirograph` and `ultrahouse3000` are not.** So in a normal coding session the hobby plugins (and the only embedded MCP) cost nothing.

Standing context in a normal coding project (3 dev plugins on) — **numbers are `[ESTIMATE]`, not measured:**

| Source                                                     | Always-on cost                                                 |
| ---------------------------------------------------------- | -------------------------------------------------------------- |
| 11 skill descriptions (box-factory 2, dmv 6, mr-sparkle 3) | ~550–1,100 tok (≈50–100/skill per AgentSkills implementer doc) |
| mr-sparkle `bash_guidance` SessionStart injection          | ~80–130 tok                                                    |
| Embedded MCP tool definitions                              | **0** `[VERIFIED]`                                             |
| **Total**                                                  | **~650–1,250 tok `[ESTIMATE]`**                                |

The conclusion ("light citizen") is robust to the imprecision. `[VERIFIED]` the session-start deferred-tool flood is the Claude desktop app showing all connectors — not neat-little-package.

### 2. box-factory mostly holds up (earlier "drifted into wrong" was overstated)

Re-verified 2026-06-14 against current docs + empirical runtime tests. The first pass — a doc-scrape via subagent — got two backwards.

| box-factory claim                                                                     | Verified status                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Sub-agents **cannot** spawn sub-agents… stripped even if declared in frontmatter"    | **[VERIFIED] CORRECT (this runtime).** Subagent with `Agent` explicitly in `tools` still had **no Agent/Task tool** → `COULD_NOT_SPAWN`. Doc claims explicit `Agent` enables nesting; runtime disproves it. Keep box-factory's wording. |
| Agent colors                                                                          | **[VERIFIED] fixed.** Now 8: `red, green, blue, yellow, cyan, purple, orange, pink`. `pink` added to claude-components + audit-components.                                                                                              |
| `commands/` is legacy → migrate to skills                                             | **[VERIFIED] correct — I was wrong.** CC docs: custom commands "merged into skills."                                                                                                                                                    |
| `.agents/skills/` cross-client discovery path                                         | **[VERIFIED] correct — I was wrong.** Adopted cross-client convention. **But Claude Code does NOT auto-discover it** (per user); Codex + Gemini do. box-factory wording fixed to say "adopted convention" + the Claude-Code caveat.     |
| `tools` not `allowed_tools`; hook tri-state `permissionDecision`; minimal plugin.json | **[DOC-ONLY]** still true ✓                                                                                                                                                                                                             |

Both architecture items from the prior draft ("push platform facts to fetch-then-judge", "restructure the auditor's tables") are **deleted** — they were weak. box-factory's hardcoded rules are deliberate (they live where docs are wrong or Claude misbehaves, e.g. nested delegation); the fix for drift is periodic re-verification (the `update-box-factory` skill), not de-hardcoding.

## Frictions — verdicts

1. **Embedded MCPs enabled by default** → *Nearly solved.* `[VERIFIED]` dmv dropped its GitHub MCP (`71051f2`); only ultrahouse's HA MCP remains, and it's not globally enabled. Fix: unbundle even that one (prerequisite, not bundled) per box-factory's own "Plugin MCP Duplication Trap."
2. **Skills that may not apply** → *Largely a non-issue here.* `[DOC-ONLY]` progressive disclosure keeps bodies out until triggered. The "eager ~2,100-line load" I previously flagged for spirograph's [home-organization](plugins/spirograph/skills/home-organization/SKILL.md) was wrong: the body says read references "**as needed**" (lazy); only the "Required Reading" *heading* is in mild tension. Low priority.
3. **Claude-marketplace-specific structure** → *Real, and the active workstream.* `[VERIFIED]` ~15 of 18 skills are pure-knowledge/spec-portable; the Claude-bound ones are `dmv-config`, `ultrahouse:check` (bash-exec skills), and `mr-sparkle:lint` (leans on `CLAUDE_SKILL_DIR` + hooks). Non-skill Claude-only glue: mr-sparkle's 5 hooks, dmv's commit-validate hook, the `audit-components` agent, the HA MCP, the manifests. Full classification + distribution plan: [docs/cross-ecosystem.md](docs/cross-ecosystem.md).
4. **box-factory drift** → *Resolved.* `[VERIFIED]` mostly current; only fix was the color list (done). Keep the preference layer. Periodic re-check via `update-box-factory`.
5. **(Not on your list) mr-sparkle permission-prophylactic hooks** → *Tested & narrowed.* `[VERIFIED 2026-06-14, desktop + TUI]` of the 7 patterns the hook blocked, only `$()` and backtick substitution still trigger a permission prompt (the "cannot be statically analyzed" kind — allowlist-proof, "Allow once" only). The other 5 (`---` strings, `git -C`, fully-qualified paths, `{"json"}`, redirects) run clean — even in real compound/redirect forms. Narrowed `block_unneeded_permission_triggers.sh` + `bash_guidance.sh` to the two keepers; dropped the rest. (`git -C` was also dead code — `\b` doesn't work in bash ERE.) Re-test anytime via the `test-permission-hooks` skill.

## Action menu

### Done this session

- [x] box-factory: `pink` added → 8 colors (claude-components + audit-components).
- [x] box-factory: `.agents/skills/` wording fixed to "adopted convention" + Claude-Code-doesn't-discover caveat.
- [x] Consolidated the verification methodology into `update-box-factory`; deleted the separate `audit-and-verify` skill.
- [x] Deleted `test-agent-colors` (colors settled).
- [x] Folded the nested-delegation test procedure into `update-box-factory` (replaces the standalone-skill idea).
- [x] Nested-delegation verified (box-factory right); root-`CLAUDE.md` TODO typo fixed; `commands/` flag kept.
- [x] Moved `TODO.md` → [docs/TODO.md](docs/TODO.md).
- [x] Tested (desktop + TUI) & narrowed mr-sparkle's permission-trigger hooks to `$()` + backticks; dropped the 5 patterns that no longer prompt. Added the `test-permission-hooks` skill to re-verify on demand.

### Remaining

- [ ] Run `update-box-factory` end-to-end to sweep for any other small drifts.
- [ ] Unbundle ultrahouse3000's HA MCP from [.mcp.json](plugins/ultrahouse3000/.mcp.json) → documented prerequisite. Keep the `check` skill as setup helper.
- [ ] Execute the cross-ecosystem plan ([docs/cross-ecosystem.md](docs/cross-ecosystem.md)) — make portable skills reachable by all agents.- [ ] spirograph [home-organization](plugins/spirograph/skills/home-organization/SKILL.md): minor "Required Reading" heading vs "as needed" body wording tension (low priority).
- [ ] mr-sparkle ecosystem-detection skill + `config init` ([docs/TODO.md:5](docs/TODO.md)).
- [ ] Clean stale references in settings: deleted/renamed skills, dead `mcp__plugin_dmv_github__*` permission, old `/Users/aaron/workspace/infra/` path.

## Still unverified (next audit pass)

- Token estimates in Reframe 1 — measure actual catalog tokens.
- spirograph content characterization (50/25/25, etc.) — `[SUBAGENT]`, one un-spot-checked report. Structural portability is verified; the content opinions are not.
## Evidence log

**2026-06-14**

- **Nested subagents (default):** `general-purpose` subagent → no `Agent`/`Task` tool → `COULD_NOT_SPAWN`.
- **Nested subagents (explicit `tools: Agent`):** `nested-tester` agent → still no Agent tool → `COULD_NOT_SPAWN`. Confirms "stripped even if declared in frontmatter." Doc claims otherwise; runtime wins. Artifacts removed.
- **Colors:** sub-agents doc `color` accepts `red, green, blue, yellow, purple, orange, pink, cyan` (8). `pink` added to box-factory.
- **Permission-trigger hooks:** of 7 blocked patterns, only `$()` + backticks still prompt (allowlist-proof "cannot be statically analyzed"); `---` / `git -C` / abs-paths / `{"json"}` / redirects run clean, desktop + TUI. Hook narrowed to the two keepers.
- **Commands:** CC skills doc — commands "merged into skills."
- **`.agents/skills/` discovery:** `[VERIFIED]` Codex scans `.agents/skills` (cwd→repo root, `$HOME/.agents/skills`, `/etc/codex/skills`) + has a plugin system; Gemini CLI reads `~/.gemini/skills/` or `~/.agents/skills/` alias (alias wins). **Claude Code does NOT auto-discover `.agents/skills/`** (per user) — needs symlink/copy.
- **enabledPlugins:** read from `~/.claude/settings.json` — box-factory/dmv/mr-sparkle true; spirograph/ultrahouse3000 absent.
