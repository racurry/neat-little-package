# Cross-Ecosystem Plan

> Goal (conceptual): every agent I use, on every computer I use, can reach the knowledge skills in this repo — with low friction. The *target directory* is irrelevant; reuse is the point. The Claude marketplace was only ever a way to share these with myself at work; official marketplace structure is not required.

## Discovery reality — who reads what

`[VERIFIED 2026-06-14]` unless noted.

| Agent                   | Reads `.agents/skills/`?                                                              | Native skill location(s)                                                                              |
| ----------------------- | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **Codex**               | **Yes**                                                                               | `.agents/skills` (cwd → repo root), `~/.agents/skills`, `/etc/codex/skills`; plugins for distribution |
| **Gemini CLI**          | **Yes** (alias takes precedence)                                                      | `~/.gemini/skills/` or `~/.agents/skills/`; `.gemini/skills/` or `.agents/skills/`                    |
| **Claude Code**         | **No**                                                                                | `.claude/skills/` (project), `~/.claude/skills/` (user), plugin skills via marketplace                |
| Cursor, Copilot, others | `[unverified]` — listed as AgentSkills clients; check each tool's docs before relying | varies                                                                                                |

**The crux:** a single `.agents/skills/` directory gets Codex + Gemini for free. Claude Code is the odd one out — it needs the skills in `.claude/skills/` (or a plugin), via symlink or copy.

Two scopes matter: **project-level** (`<repo>/.agents/skills/`, repo-scoped — Codex/Gemini see it only when working in this repo) vs **user-level** (`~/.agents/skills/`, `~/.claude/skills/` — available in every project). General-purpose skills (git workflow, readme-style) want user-level reach.

## Component classification

`[VERIFIED]` by reading each component. 18 skills + the non-skill glue.

### Portable — pure knowledge, usable by any agent

| Skill                                                                                                     | Plugin         | Notes                                           |
| --------------------------------------------------------------------------------------------------------- | -------------- | ----------------------------------------------- |
| `agent-skills`                                                                                            | box-factory    | About the universal spec itself                 |
| `commit`, `pr`, `github`, `merge-conflicts`, `code-history`                                               | dmv            | git/gh workflow + prefs; no Claude-isms         |
| `readme-style`, `uv-scripts`                                                                              | mr-sparkle     | Pure preference/convention knowledge            |
| `home-organization`, `gridfinity-openscad`, `opengrid-openscad`, `neogrid-openscad`, `underware-openscad` | spirograph     | Pure domain knowledge; **zero Claude features** |
| `home-assistant`                                                                                          | ultrahouse3000 | HA config knowledge                             |

That's **13 clearly portable.** Two more are conditional:

- `mr-sparkle:lint` — the knowledge + `lint.py` are portable, but the skill is wired to `CLAUDE_SKILL_DIR` and the lint-on-write hook. Portable **with adaptation**.
- `box-factory:claude-components` — portable *text*, but only *useful* inside Claude (it's about building Claude components). Ship it where convenient; it adds no value to other agents.

### Claude-specific — and *why*

| Component                                                               | Why it's Claude-only                                                                                                |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `dmv:dmv-config`, `ultrahouse3000:check`                                | Skill bodies use Claude skill-exec frontmatter (`!` command runner, `disable-model-invocation`, `CLAUDE_SKILL_DIR`) |
| `box-factory:audit-components` (agent)                                  | Uses the **Agent** tool (Claude-only) and audits Claude components                                                  |
| mr-sparkle's 5 hooks + `lint_on_write`; dmv's `validate_commit_message` | **Claude Code hooks** — no cross-agent equivalent                                                                   |
| ultrahouse3000 HA **MCP** (`.mcp.json`)                                 | The MCP *server* is a universal protocol (reusable), but the `.mcp.json` plugin wiring is Claude-specific           |
| `marketplace.json`, each `plugin.json`                                  | Claude plugin/marketplace packaging                                                                                 |

**Takeaway:** the knowledge lives in portable skills; the *automation* (hooks, the agent, MCP wiring, manifests) is the genuinely Claude-bound part. They can be cleanly separated.

## The problem, stated plainly

The portable skills currently live inside `plugins/<plugin>/skills/` and reach **Claude** via the marketplace. They do **not** reach Codex or Gemini, because those scan `.agents/skills/` and nothing here is exposed there. We want the portable set reachable by all three (and future agents) on every machine, without hand-copying.

## Distribution options (brainstorm)

### A. Symlink farm from plugin source → client dirs (recommended start)

Keep the plugin layout as the source of truth. A small idempotent `install.sh` symlinks each **portable** skill into the locations clients actually read:

- `~/.agents/skills/<skill>` → Codex + Gemini, all projects
- `~/.claude/skills/<skill>` → Claude, all projects (bypasses needing them in the marketplace)
- optionally `<repo>/.agents/skills/<skill>` → repo-scoped, for agents working in this repo

Run once per machine after `git pull`; re-run when skills are added/removed (symlinks track content automatically).

- **Pros:** non-disruptive (marketplace untouched), single source of truth, Codex/Gemini get the convention they already read, friction = one command per machine.
- **Cons:** symlinks must be regenerated on add/remove; symlinks are unix-friendly (fine on darwin/linux; would break on Windows).

### B. Commit the symlinks (no install step)

Instead of a per-machine script, commit `<repo>/.agents/skills/<skill>` symlinks (repo-relative) so `git pull` delivers working links. Codex/Gemini read them in-repo. Claude still needs `~/.claude/skills` links (script or manual).

- **Pros:** zero per-machine setup for the in-repo case.
- **Cons:** only covers *project-scoped* discovery (this repo), not cross-project user-level; doesn't solve Claude; committed symlinks are brittle across OSes.

### C. Restructure: `.agents/skills/` becomes the canonical home

Move the portable skills out of the plugins to a top-level `.agents/skills/` (or `skills/`). Claude plugins shrink to just their Claude-specific parts (hooks/agents/MCP). Claude reaches the knowledge skills via symlink into `.claude/skills/` or by keeping thin plugin references.

- **Pros:** most honest structure — knowledge is first-class and ecosystem-neutral; matches the "less Claude-specific" goal.
- **Cons:** biggest change; redefines what the dmv/spirograph/etc. "plugins" are; more upfront work.

### D. Dual-publish as a Codex plugin

Codex has its own plugin system + `$skill-installer`. Package the portable (or bundled) skills as a Codex plugin too.

- **Pros:** first-class Codex distribution/versioning.
- **Cons:** a second packaging to maintain; overkill for personal reuse.

### E. Investigate community installers

- `skills.sh` — `[unverified]` whether this is a real installer ecosystem; check before relying.
- `skills-ref` — the spec's reference library (`skills-ref validate`); validation, not distribution, but worth wiring into CI.

## Recommendation

Start with **A** (symlink farm + `install.sh`), targeting `~/.agents/skills/` and `~/.claude/skills/`. It directly serves the goal (all agents, all machines, one command), keeps the working Claude marketplace intact, and is reversible. Keep the **plugin/marketplace wrapper for the genuinely Claude-specific bundles** (hooks, the auditor agent, the HA MCP) — that's the right channel for those.

Then, if the repo's identity should fully shift away from "Claude marketplace," graduate to **C** (canonical `.agents/skills/`), with the Claude plugins reduced to automation-only.

## Open / to verify before building

- `[verify]` exact skill paths for Cursor, Copilot, and any other agent you use.
- `[verify]` `skills.sh` — real tool or not?
- `[decide]` symlink vs copy (symlink = live updates; copy = OS-portable but can go stale).
- `[decide]` which conditional skills to include: adapt `mr-sparkle:lint` for portability? ship `claude-components` anywhere?
- `[verify]` committed-symlink behavior across your specific machines (all darwin/linux?).
