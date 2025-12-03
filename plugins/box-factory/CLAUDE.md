# Box Factory Development Guidelines

## Philosophy

**Low-Maintenance First**

- Skills MUST defer to official docs via WebFetch (never hardcode model names, tool lists, syntax)
- Agents MUST fetch current specifications before creating components
- Apply knowledge delta filter (only document what Claude doesn't know)
- Documentation changes; principles don't

**Two-Layer Approach**

- Layer 1: Official specs (what docs explicitly say)
- Layer 2: Best practices (interpretive guidance, gotchas, anti-patterns)
- Always distinguish which layer you're in

**Evidence-Based**

- Claims must be grounded in official docs OR clearly marked as opinions
- Never present best practices as official requirements

**Delegation Pattern**

- Commands are thin wrappers
- Agents do complex work in isolation
- Skills provide interpretive guidance
- Hooks enforce deterministic rules
- All Box Factory commands delegate to specialized agents

## Component Patterns

### Skills

**Structure:**

- Doc references: Point to official docs for things Claude might not know (not basics)
- Progressive disclosure: Core concepts → Advanced features
- Mark sections: "(Official Specification)" vs "(Best Practices)"
- Include: Decision frameworks, common pitfalls, quality checklists
- Filename: `SKILL.md` (uppercase) in `skills/[name]/` subdirectory

**Knowledge Delta Filter (Critical):**

- ✅ Include: User-specific preferences, edge cases, decision frameworks, things Claude gets wrong, new tech
- ❌ Exclude: Basic commands Claude knows, standard workflows, general best practices
- Result: Focused skills (~50-150 lines) that add real value

**Example Application:**

```markdown
❌ Bad: 480 lines documenting all git commands
✅ Good: 80 lines documenting user's specific commit format + pre-commit hook retry logic
```

**Quality Checklist:**

- ✓ Applies knowledge delta filter (only documents what Claude doesn't know)
- ✓ Points to docs for things Claude might not know (not common tools/workflows)
- ✓ Uses two-layer approach with clear section headings
- ✓ Defers to official docs (no hardcoded version-specific details)
- ✓ Includes decision frameworks and common pitfalls
- ✓ Provides quality checklist
- ✓ Focused scope (~50-150 lines typical)

### Agents

**Structure:**

- No user interaction language ("ask the user" = forbidden)
- Tools match autonomous responsibilities
- Strong delegation in description ("ALWAYS use when...", "MUST BE USED when...")
- Reference design skills for guidance
- Model: haiku (simple), sonnet (balanced), opus (complex reasoning)

**Tool Selection (Critical):**

- **Skill tool:** Include if agent loads ANY skills (99% of agents do)
- **Task tool:** Include if agent delegates to other agents
- **Read/Write/Edit:** Match to read-only vs creation responsibilities
- **Bash:** Only if running commands
- **WebFetch/WebSearch:** If fetching docs or searching

**Loading Design Skills:**

```markdown
# Agent Process

1. **Load design skills (REQUIRED)** - Use Skill tool to load both skills BEFORE proceeding

   ```

   Use Skill tool: skill="box-factory:box-factory-architecture"
   Use Skill tool: skill="box-factory:agent-design"

   ```

   **Do NOT use Read tool** - The Skill tool ensures proper loading and context integration.
```

**Quality Checklist:**

- ✓ Follows relevant design skill patterns
- ✓ Defers to official docs (no hardcoded specifics)
- ✓ Distinguishes specs from best practices
- ✓ Includes examples with before/after
- ✓ No user interaction language in agents
- ✓ Tools match responsibilities
- ✓ Clear, specific descriptions for autonomous delegation
- ✓ Includes Skill tool if loading any skills
- ✓ Includes Task tool if delegating to other agents

### Commands

**Structure:**

- Delegation pattern: Keep command simple, delegate to specialized agent
- Always include `description` field (improves discoverability)
- Use `argument-hint` for expected arguments
- Let agents handle complexity, validation, and decision-making

**Example Pattern:**

```markdown
---
description: Create a new agent with specified name and purpose
argument-hint: agent-name purpose
---

Delegate to the agent-writer agent to create a new Claude Code agent.

The agent-writer will:
- Load agent-design and box-factory-architecture skills
- Fetch official documentation
- Create agent with proper structure
- Validate tool selection and delegation description
- Ensure no user interaction language
```

**Quality Checklist:**

- ✓ Includes description field in frontmatter
- ✓ Delegates to specialized agent for complex work
- ✓ Uses argument-hint if accepting arguments
- ✓ Single, focused responsibility
- ✓ No complex logic in command prompt

### Hooks

**Structure:**

- Fast execution (< 60s or set custom timeout)
- Quote all variables: `"$VAR"` not `$VAR`
- Exit 2 = blocking (use sparingly, security/safety only)
- Validate inputs (path traversal, sensitive files)

**Language Selection:**

- **Bash:** Simple operations (< 20 lines, text processing, command chaining)
- **Python+UV:** Complex logic (JSON parsing, API calls, validation, multi-step processing)

**Security:**

- Quote all variables
- Validate stdin JSON inputs
- Block path traversal (`..` in paths)
- Skip sensitive files (.env, credentials)
- Use absolute paths with environment variables

**Quality Checklist:**

- ✓ Fast execution (< 60s or custom timeout configured)
- ✓ All variables quoted properly
- ✓ Exit codes appropriate (0, 2, other)
- ✓ Security validated (no path traversal, sanitized inputs)
- ✓ Proper error messages to stderr

## Decision Framework

**When creating Box Factory components, ask:**

1. **Skill vs Agent?**
   - Skill = Knowledge that loads when relevant, interpretive guidance
   - Agent = Does actual work autonomously (writes files, runs tests)

2. **Command pattern?**
   - ALL Box Factory commands delegate to specialized agents
   - Command = thin wrapper, agent = complex logic

3. **Read-only vs Write?**
   - Validation/review agents = Read, Grep, Glob, WebFetch only
   - Creation agents = Add Write, Edit as needed

4. **What design skill applies?**
   - Creating agents → use agent-design
   - Creating commands → use slash-command-design
   - Creating skills → use skill-design
   - Creating hooks → use hooks-design
   - Creating plugins → use plugin-design

5. **Apply knowledge delta filter?**
   - For skills: Only document what Claude doesn't already know
   - Would Claude get this wrong without the skill?
   - Is this specific to this user/project/context?

## Architecture

```
User → Command → Specialized Agent → Design Skill
         ↓            ↓                   ↓
     (thin wrap)  (complex logic)    (guidance)
```

**Example:** `/box-factory:add-agent` → agent-writer → agent-design skill

All Box Factory components are self-documenting examples of the patterns they teach.

## Quality Standards

**Before completing any Box Factory component:**

- ✓ Follows relevant design skill patterns
- ✓ Defers to official docs (no hardcoded specifics)
- ✓ Applies knowledge delta filter (skills only)
- ✓ Distinguishes specs from best practices
- ✓ Includes examples with before/after
- ✓ No user interaction language in agents
- ✓ Tools match responsibilities
- ✓ Skill tool included if agent loads skills
- ✓ Task tool included if agent delegates
- ✓ Clear, specific descriptions for autonomous delegation

## Anti-Patterns (Forbidden)

**In Skills:**

- ❌ Duplicating official documentation
- ❌ Hardcoding version-specific details (models, tools, syntax)
- ❌ Presenting opinions as official requirements
- ❌ Documenting basic commands Claude already knows
- ❌ Comprehensive documentation instead of knowledge delta

**In Agents:**

- ❌ User interaction language ("ask the user", "confirm with user")
- ❌ Tool mismatches (reviewer with Write, generator with Read-only)
- ❌ Vague descriptions that don't trigger delegation
- ❌ Agent loads skills but Skill tool not in tools list
- ❌ Agent delegates but Task tool not in tools list

**In Commands:**

- ❌ Reimplementing agent logic in command prompt
- ❌ Complex argument parsing (let agents handle)
- ❌ Missing description field
- ❌ Knowledge storage instead of action

**In Hooks:**

- ❌ Unquoted shell variables
- ❌ User interaction assumptions
- ❌ Slow operations without timeouts
- ❌ Path traversal vulnerabilities

## Validation Workflow

### Creating Components

1. Load relevant design skills
2. Fetch official documentation
3. Create component following patterns
4. Self-validate against quality checklist
5. Return complete result

### Validating Components

1. Load box-factory-architecture skill
2. Load component-specific design skill
3. Fetch official documentation
4. Check structure, syntax, specifications
5. Detect anti-patterns
6. Generate detailed report with file:line references

### Reviewing Components

1. Identify component type
2. Load box-factory-architecture + component-specific skill
3. Fetch official documentation
4. Analyze against design patterns
5. Provide prioritized feedback (critical, important, minor)
6. Suggest specific improvements with examples

## Component Creation Best Practices

### Writer Agents Must

1. Load both box-factory-architecture AND component-specific design skill
2. Use Skill tool (never Read tool) for loading skills
3. Fetch official documentation before creating
4. Self-validate against quality checklist
5. Delegate component creation to specialized agents (never create directly)

### Quality Agents Must

1. Load box-factory-architecture AND relevant design skills
2. Fetch current official documentation
3. Provide specific file:line references
4. Distinguish between errors (blocking) and warnings (quality)
5. Include actionable fix recommendations

## Knowledge Delta Examples

### Bad (480-line git-workflow skill)

```markdown
# Git Workflow Skill

## Common Git Operations

**Checking Repository Status:**
```bash
git status  # Shows staged, unstaged, and untracked files
```

**See detailed diff:**

```bash
git diff  # Unstaged changes
git diff --staged  # Staged changes
```

[... 450+ lines documenting standard git commands ...]

```

**Why it fails:** Claude already knows all standard git commands. 95% redundant content.

### Good (80-line git-workflow skill):

```markdown
# Git Workflow Skill

This skill documents workflow preferences specific to this user. For standard git knowledge, Claude relies on base training.

## Commit Message Requirements (User Preference)

**This user requires:**
- Terse, single-line format (max ~200 characters)
- No emojis or decorative elements
- No attribution text (no "Co-Authored-By:", no "Generated with Claude Code")

## Pre-Commit Hook Edge Case (Critical)

**Problem:** Pre-commit hooks modify files during commit, causing failure.

**Workflow:**
1. Attempt: `git commit -m "message"`
2. Hook modifies files (auto-format)
3. Commit FAILS (working directory changed)
4. Stage modifications: `git add .`
5. Retry ONCE: `git commit --amend --no-edit`
```

**Why it works:** 100% valuable delta knowledge. Focused on what Claude doesn't know.

## MCP Server Configuration

### Structure (Best Practices)

- ✓ Use external `.mcp.json` files (not inline in plugin.json)
- ✓ All secrets use `${ENV_VAR}` references (never hardcoded)
- ✓ README documents required environment variables
- ✓ Clear instructions for obtaining credentials
- ✓ Example export commands provided

### Anti-Patterns (Forbidden)

- ❌ Inline MCP configuration in plugin.json
- ❌ Hardcoded secrets or API keys
- ❌ Empty string placeholders instead of ${ENV_VAR}
- ❌ Undocumented environment variables

## Testing Strategy

### Component Testing

**Agents:** Load directly via Task tool or let delegation trigger

**Commands:** Execute via `/command-name` and verify behavior

**Skills:** Load via Skill tool and test in various contexts

**Hooks:** Trigger event and check CTRL-R logs

### Integration Testing

Test complete workflows:

1. User types command
2. Command delegates to agent
3. Agent loads relevant skills
4. Agent creates/validates component
5. Verify result matches expectations

### Validation Testing

Run `/box-factory:validate-plugin` on:

- Box Factory itself (self-validation)
- New plugins created by Box Factory
- Modified components

## Documentation Standards

### Plugin README.md (General Guidance)

**Minimal by default.** Only document what users need to know:

1. Brief description (1-2 sentences)
2. Components list (commands, agents, skills, hooks)
3. Installation (if non-obvious)
4. Basic usage examples

**Add sections only when needed:**

- Troubleshooting: Only if there are known issues
- Configuration: Only if plugin has settings
- Dependencies: Only if external tools required

**Anti-patterns (forbidden in plugin READMEs):**

- ❌ "Future Roadmap" or "Planned Features" (don't document what doesn't exist)
- ❌ "Extensibility" sections (unless user asked for extensible design)
- ❌ Detailed error handling documentation (Claude knows error handling)
- ❌ Verbose explanations of obvious behavior
- ❌ Sections copied from Box Factory's README (it's a meta-plugin, not a template)

### Box Factory's Own README (Special Case)

Box Factory is a meta-plugin that creates other plugins. Its README is intentionally comprehensive because it documents plugin creation patterns. **Do not use it as a template for simple plugins.**

### CLAUDE.md

**Structure:**

1. Philosophy and principles
2. Component patterns
3. Decision frameworks
4. Anti-patterns

**Tone:**

- Developer-facing guidelines
- Prescriptive patterns
- Clear do/don't distinctions

## Box Factory Self-Consistency

**Critical principle:** Box Factory uses its own patterns to create itself.

**What this means:**

- Every skill follows skill-design patterns
- Every agent follows agent-design patterns
- Every command follows slash-command-design patterns
- Every component exemplifies what it teaches

**Benefits:**

- Self-documenting ecosystem
- Living examples of best practices
- Dogfooding ensures patterns work
- Trust through demonstration

## Development Workflow

### Adding New Components

1. Determine component type (agent, command, skill, hook)
2. Use relevant `/box-factory:add-*` command or create manually
3. Follow design skill patterns
4. Self-validate against quality checklist
5. Test component in isolation
6. Test integration with other components
7. Run `/box-factory:validate-plugin`
8. Fix any validation issues
9. Update documentation with `/box-factory:update-docs`

### Modifying Existing Components

1. Read component and relevant design skill
2. Make changes following patterns
3. Validate against quality checklist
4. Test changes thoroughly
5. Run `/box-factory:review-component` for feedback
6. Fix any issues
7. Update documentation if needed

### Version Management

**Semantic Versioning:**

- **Major (X.0.0):** Breaking changes, incompatible API changes
- **Minor (x.Y.0):** New features, backward-compatible additions
- **Patch (x.y.Z):** Bug fixes, backward-compatible improvements

**Before Release:**

1. Validate all components
2. Review all components
3. Update documentation
4. Test end-to-end workflows
5. Update version in plugin.json
