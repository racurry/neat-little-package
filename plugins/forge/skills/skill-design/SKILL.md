---
name: skill-design
description: Meta-skill that teaches how to design Claude Code skills following the Forge philosophy. Helps you understand when to create skills, how to structure them for low maintenance, and how to add value beyond documentation. Use when creating or reviewing skills.
---

# Skill Design Skill

This meta-skill teaches you how to design excellent Claude Code skills. **Skills are unique among Claude Code components** - they provide progressive knowledge disclosure and interpretive guidance that loads when relevant.

## Required Reading Before Creating Skills

**Official documentation:** Skills are part of the agent system but don't have dedicated documentation. Their purpose and structure are inferred from:

- **<https://code.claude.com/docs/en/sub-agents.md>** - Skills mentioned as knowledge loaded when relevant
- Existing skills in the wild - Examine high-quality skills for patterns

## Core Understanding

### Skills Are Progressive Knowledge Disclosure

**Key insight:** Skills solve the "you can't put everything in the system prompt" problem.

**What this means:**

- **Without skills:** Important knowledge buried in long prompts or forgotten
- **With skills:** Knowledge loads automatically when topics become relevant
- **Value proposition:** Right information at the right time, without token bloat

**Decision test:** Does this information need to be available across multiple contexts, but not always?

### Skills vs System Prompts vs CLAUDE.md

**Skills are for:**

- Substantial procedural expertise (20+ lines of guidance)
- Domain-specific knowledge needed sporadically
- Interpretive frameworks that enhance understanding
- Best practices that apply across multiple scenarios

**System prompts are for:**

- Always-relevant instructions
- Core behavior and personality
- Universal constraints

**CLAUDE.md is for:**

- Project-specific context
- Repository structure
- Team conventions
- Always-loaded information

### Knowledge Delta Filter (Critical Understanding)

**THE MOST IMPORTANT PRINCIPLE:** Skills should only document what Claude DOESN'T already know.

**Why this matters:** Claude's training includes extensive knowledge of common development tools, standard workflows, well-established frameworks, and general best practices. Skills that duplicate this base knowledge waste tokens and create maintenance burden without adding value.

**Skills document the DELTA** - the difference between Claude's base knowledge and what Claude needs to know for your specific context.

**INCLUDE in skills (the delta):**

✅ **User-specific preferences and conventions**
- "This user wants commit messages terse, single-line, no emojis, no attribution"
- "This team uses specific naming conventions not found in standard docs"
- "This project requires custom workflow steps"
- Example: User's preference for no "Generated with Claude Code" messages

✅ **Edge cases and gotchas Claude would miss**
- "Pre-commit hooks that modify files require retry with --amend"
- "This API has undocumented rate limiting behavior"
- "File system paths need special escaping in this environment"
- Example: Specific retry logic for linter hooks that auto-fix

✅ **Decision frameworks for ambiguous situations**
- "When to use gh CLI vs GitHub MCP server in this project"
- "Tool selection hierarchy when multiple options exist"
- "Which pattern to prefer when standards conflict"
- Example: Prefer gh CLI when available, fall back to MCP

✅ **Things Claude gets wrong without guidance**
- "Claude invents unsupported frontmatter in slash commands"
- "Claude uses deprecated syntax for Tool X without this guidance"
- "Claude doesn't know about this project-specific integration pattern"
- Example: Claude making up `skills: git-workflow` frontmatter that doesn't exist

✅ **New or rapidly-changing technology (post-training)**
- Claude Code itself (released after training cutoff)
- New framework versions with breaking changes
- Emerging tools not well-represented in training data
- Example: Claude Code plugin system specifics

✅ **Integration patterns between tools (project-specific)**
- "How this project connects Tool A with Tool B"
- "Custom workflow orchestration"
- "Project-specific toolchain configuration"
- Example: Using both gh CLI and GitHub MCP server in same plugin

**EXCLUDE from skills (Claude already knows):**

❌ **Basic commands for well-known tools**
- Don't document: git status, git commit, git push, git diff
- Don't document: npm install, pip install, docker run
- Don't document: Standard CLI flags and options Claude knows
- Claude learned this in training and doesn't need reminders

❌ **Standard workflows Claude knows**
- Don't document: Basic git branching workflow
- Don't document: Standard PR review process
- Don't document: Common testing patterns
- These are well-established practices in Claude's training

❌ **General best practices (not project-specific)**
- Don't document: "Write clear commit messages"
- Don't document: "Test your code before committing"
- Don't document: "Use semantic versioning"
- Claude already knows these principles

❌ **Well-established patterns for common tools**
- Don't document: REST API design basics
- Don't document: Standard design patterns (MVC, etc.)
- Don't document: Common security practices Claude knows
- Training data covers these extensively

**Decision Test: Should This Be In A Skill?**

Before including content in a skill, ask:

1. **Would Claude get this wrong without the skill?**
   - Yes → Include it (fills a knowledge gap)
   - No → Exclude it (redundant with training)

2. **Is this specific to this user/project/context?**
   - Yes → Include it (contextual delta)
   - No → Probably exclude it (general knowledge)

3. **Is this well-documented in Claude's training data?**
   - No (new/custom/edge case) → Include it
   - Yes (standard practice) → Exclude it

4. **Would this information change Claude's behavior?**
   - Yes (corrects mistakes or fills gaps) → Include it
   - No (Claude already behaves this way) → Exclude it

**Example: git-workflow skill**

❌ **Bad (includes base knowledge):**
```
480 lines including:
- How to use git status, git diff, git commit
- Basic branching operations
- Standard commit message formats
- Common git commands
```
95% redundant, 5% valuable

✅ **Good (only includes delta):**
```
~80 lines including:
- User's specific commit format preferences
- Edge case: pre-commit hook retry logic
- User requirement: no attribution text
```
100% valuable, focused on what Claude doesn't know

## The Forge Philosophy for Skills

### 1. Low-Maintenance by Design

**Defer to official documentation via WebFetch:**

```markdown
## Required Reading Before Creating Agents

Fetch these docs with WebFetch every time:

- **https://code.claude.com/docs/en/sub-agents.md** - Core specification
```

**Why:** Documentation changes; skills that defer stay valid.

**Don't hardcode:**

- ❌ "Available models: sonnet, opus, haiku"
- ❌ "Tools include: Read, Write, Edit, Bash, Glob, Grep"
- ❌ Specific syntax that may change

**Do reference:**

- ✅ "See model-config documentation for current options"
- ✅ "Refer to tools documentation for current capabilities"
- ✅ "Fetch official specification for syntax details"

### 2. Two-Layer Approach

**Layer 1: Official Specification**

- What the docs explicitly say
- Required fields and syntax
- Official examples
- Mark with headings: `## X (Official Specification)`

**Layer 2: Best Practices**

- What the docs don't emphasize
- Common gotchas and anti-patterns
- Interpretive guidance
- Mark with headings: `## X (Best Practices)`

**Example:**

```markdown
## Frontmatter Fields (Official Specification)

The `description` field is optional and defaults to first line.

## Description Field Design (Best Practices)

Always include `description` even though it's optional - improves discoverability and Claude's ability to use the SlashCommand tool.
```

### 3. Evidence-Based Recommendations

**All claims must be:**

✅ Grounded in official documentation, **OR**
✅ Clearly marked as opinionated best practices, **OR**
✅ Based on documented common pitfalls

**Avoid:**
❌ Presenting opinions as official requirements
❌ Making unsupported claims about "best practices"
❌ Prescribing patterns not in documentation without labeling them

## Skill Structure (Best Practices)

### Frontmatter

```yaml
---
name: skill-name
description: What this skill teaches and when to use it
---
```

**Name:** kebab-case identifier
**Description:** Clear triggering conditions for when the skill loads

### Content Organization

```markdown
# Skill Name

[Opening paragraph explaining purpose and value]

## Required Reading Before [Task]

Fetch these docs with WebFetch every time:
- [Official doc URLs with descriptions]

## Core Understanding

[Fundamental concepts, architecture, philosophy]

## [Topic] (Official Specification)

[What the official docs explicitly state]

## [Topic] (Best Practices)

[Interpretive guidance, gotchas, patterns]

## Decision Framework

[When to use X vs Y, with clear criteria]

## Common Pitfalls

[Anti-patterns with why they fail and better approaches]

## Quality Checklist

[Validation items before finalizing]

## Documentation References

[Authoritative sources to fetch]
```

### Content Quality Standards

**Be specific and actionable:**

- ✅ "Run pytest -v and parse output for failures"
- ❌ "Run tests and check for problems"

**Distinguish official from opinionated:**

- ✅ "Official docs say 'description is optional.' Best practice: always include it."
- ❌ "description is required" (when it's not)

**Use examples effectively:**

- Show before/after
- Explain what makes the "after" better
- Mark issues with ❌ and improvements with ✅

**Progressive disclosure:**

- Start with core concepts
- Build to advanced features
- Don't overwhelm with details upfront

## When to Create Skills

### Skill vs Agent vs Command

**Use a Skill when:**

- Multiple contexts need the same knowledge
- Substantial procedural expertise (not just 2-3 bullet points)
- Progressive disclosure would save tokens
- Teaching "how to think about" something
- You want automatic loading when topics arise

**Examples:**

- `agent-design` - Teaches how to design agents
- `api-documentation-standards` - Formatting rules across projects
- `security-practices` - Principles that apply broadly

**Use an Agent when:**

- Need isolated context for complex work
- Want autonomous delegation
- Doing actual work (writing files, running tests)
- Task-oriented, not knowledge-oriented

**Examples:**

- `test-runner` - Executes tests and analyzes failures
- `code-reviewer` - Performs analysis and provides feedback

**Use a Command when:**

- User wants explicit trigger
- Simple, deterministic operation
- One-off action

**Examples:**

- `/deploy` - User-triggered deployment
- `/create-component` - File generation

### Scope Guidelines (Best Practices)

**Good skill scope:**

- Focused on single domain (API design, testing, security)
- Self-contained knowledge
- Clear boundaries
- Composable with other skills

**Bad skill scope:**

- "Everything about development" (too broad)
- Overlaps heavily with another skill
- Just 3-4 bullet points (put in CLAUDE.md instead)
- Project-specific details (put in CLAUDE.md instead)

## Common Pitfalls

### Pitfall #1: Duplicating Official Documentation

**Problem:** Skill becomes outdated copy of docs

```markdown
## Available Models

The following models are available:
- claude-sonnet-4-5-20250929
- claude-opus-4-20250514
- claude-3-5-haiku-20241022
```

**Why it fails:** Model names change, skill becomes outdated

**Better:**

```markdown
## Model Selection

Fetch current model options from:
https://code.claude.com/docs/en/model-config.md

**Best practice:** Use haiku for simple tasks, sonnet for balanced work, opus for complex reasoning.
```

### Pitfall #2: Hardcoding Version-Specific Details

**Problem:** Skill includes specifics that change

```markdown
## Tool Permissions

Grant these tools to your agent:
- Read (for reading files)
- Write (for writing files)
- Edit (for editing files)
```

**Why it fails:** Tool list may expand, descriptions may change

**Better:**

```markdown
## Tool Selection Philosophy

**Match tools to autonomous responsibilities:**

- If agent analyzes only → Read, Grep, Glob
- If agent writes code → Add Write, Edit
- If agent runs commands → Add Bash

Fetch current tool list from:
https://code.claude.com/docs/en/settings#tools-available-to-claude
```

### Pitfall #3: Presenting Opinions as Official Requirements

**Problem:** Blurs the line between specs and best practices

```markdown
## Agent Description Field

The description field MUST use strong directive language like "ALWAYS use when" to ensure proper delegation.
```

**Why it fails:** Official docs don't require this; it's a best practice opinion

**Better:**

```markdown
## Description Field Design (Best Practices)

Official requirement: "Natural language explanation of when to invoke"

**Best practice:** Use specific triggering conditions and directive language to improve autonomous delegation. While not required, this pattern increases the likelihood of proper agent invocation.
```

### Pitfall #4: Kitchen Sink Skills

**Problem:** One skill tries to cover everything

```markdown
# Full-Stack Development Skill

This skill covers:
- Frontend frameworks (React, Vue, Angular)
- Backend APIs (Node, Python, Go, Rust)
- Databases (SQL, NoSQL)
- DevOps (Docker, K8s, CI/CD)
- Security best practices
- Testing strategies
...
```

**Why it fails:** Too broad, overwhelming, hard to maintain, loads unnecessarily

**Better:** Split into focused skills:

- `frontend-architecture`
- `api-design`
- `testing-strategy`

### Pitfall #5: No Clear Triggering Conditions

**Problem:** Description doesn't indicate when skill should load

```markdown
---
name: api-standards
description: API documentation standards
---
```

**Why it fails:** Unclear when this skill is relevant

**Better:**

```markdown
---
name: api-standards
description: Guidelines for designing and documenting REST APIs following team standards. Use when creating endpoints, reviewing API code, or writing API documentation.
---
```

### Pitfall #6: Documenting Claude's Base Knowledge

**Problem:** Skill includes comprehensive documentation of tools and workflows Claude already knows from training, creating token waste and maintenance burden without adding value.

**Bad example (hypothetical 480-line git-workflow skill):**

```markdown
---
name: git-workflow
description: Comprehensive git usage guide
---

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
git diff HEAD  # All changes
```

**Commit Workflow:**

```bash
# 1. Review changes
git status
git diff

# 2. Stage changes
git add .

# 3. Commit with message
git commit -m "fix: correct validation logic"
```

**Branch Operations:**

```bash
git checkout -b feature-name  # Create and switch
git switch main  # Switch to main
git branch  # List branches
```

[... 400 more lines documenting standard git commands, branching workflows, merge strategies, rebase operations, standard commit message formats, general best practices ...]
```

**Why it fails:**

- Claude already knows all standard git commands from training
- 95% of content is redundant with base knowledge
- Wastes tokens loading information Claude doesn't need
- Creates maintenance burden (skill needs updates when nothing actually changed)
- Obscures the 5% that's actually valuable (user-specific preferences)
- No behavioral change - Claude would do the same without this skill

**Better (focused 80-line version documenting only the delta):**

```markdown
---
name: git-workflow
description: User-specific git workflow preferences and edge case handling. Use when creating commits or handling pre-commit hook failures.
---

# Git Workflow Skill

This skill documents workflow preferences and edge cases specific to this user. For standard git knowledge, Claude relies on base training.

## Commit Message Requirements (User Preference)

**This user requires:**

- Terse, single-line format (max ~200 characters)
- No emojis or decorative elements
- **No attribution text** (no "Co-Authored-By:", no "Generated with Claude Code")

**Format pattern:** `<type>: <brief specific description>`

**Examples:**
```
fix: prevent race condition in session cleanup
add: rate limiting middleware
```

**Avoid:**
```
❌ ✨ add: new feature (emoji)
❌ fix: thing

🤖 Generated with Claude Code
(attribution this user doesn't want)
```

## Pre-Commit Hook Edge Case (Critical)

**Problem:** Pre-commit hooks modify files during commit, causing failure.

**Workflow:**

1. Attempt: `git commit -m "message"`
2. Hook modifies files (auto-format)
3. Commit FAILS (working directory changed)
4. Stage modifications: `git add .`
5. Retry ONCE: `git commit --amend --no-edit`

**Critical:** Only retry ONCE to avoid infinite loops.

## Quality Checklist

- ✓ Message is terse, single-line, no emojis, no attribution
- ✓ No secrets in staged files
- ✓ Prepared for potential hook retry
```

**Key improvements:**

- ✅ Went from 480 lines → 80 lines (83% reduction)
- ✅ Removed all standard git knowledge Claude already has
- ✅ Kept only user-specific preferences (commit format, no attribution)
- ✅ Kept only edge cases Claude would miss (pre-commit hook retry logic)
- ✅ 100% of content is valuable delta knowledge
- ✅ Skill actually changes Claude's behavior (would get these things wrong without it)

**The delta principle:** Skills should only contain knowledge that bridges the gap between what Claude knows and what Claude needs to know for this specific context.

## Skill Quality Checklist

Before finalizing a skill:

**Structure (based on successful patterns):**

- ✓ Proper frontmatter with name and description
- ✓ Clear description indicating when skill loads
- ✓ Filename is `SKILL.md` (uppercase, not `skill.md`)
- ✓ Located in `skills/[skill-name]/SKILL.md` subdirectory
- ✓ Single H1 heading matching skill name
- ✓ Organized with clear H2/H3 hierarchy

**Content quality:**

- ✓ Includes "Required Reading" section with official doc URLs
- ✓ Distinguishes official specs from best practices
- ✓ Avoids hardcoding version-specific details
- ✓ Uses examples effectively (before/after, ❌/✅)
- ✓ Provides decision frameworks
- ✓ Includes common pitfalls section
- ✓ Has validation checklist
- ✓ Cites authoritative sources

**Philosophy alignment:**

- ✓ Defers to official docs via WebFetch instructions
- ✓ Two-layer approach (specs + guidance)
- ✓ Evidence-based recommendations
- ✓ Focused scope, not kitchen sink
- ✓ Interpretive, not duplicative
- ✓ Progressive disclosure structure

## Example: High-Quality Skill Design

**Before (hypothetical low-quality skill):**

```markdown
---
name: testing
description: Testing stuff
---

# Testing

Use pytest for Python testing.
Use jest for JavaScript testing.

Make sure to write good tests.
```

**Issues:**

- ❌ Vague description ("testing stuff")
- ❌ No structure or organization
- ❌ No official documentation references
- ❌ Hardcodes specific tools without context
- ❌ "Write good tests" is not actionable
- ❌ No decision framework or examples
- ❌ Too brief to warrant a skill (put in CLAUDE.md)

**After (applying skill-design principles):**

```markdown
---
name: testing-strategy
description: Interpretive guidance for test-driven development, test design, and testing workflows. Use when writing tests, reviewing test coverage, or designing testing strategies.
---

# Testing Strategy Skill

This skill provides guidance for effective testing across languages and frameworks.

## Required Reading

Fetch language/framework-specific testing docs:

- **Python/pytest**: https://docs.pytest.org/
- **JavaScript/Jest**: https://jestjs.io/docs/getting-started
- **Go**: https://go.dev/doc/tutorial/add-a-test

## Core Testing Philosophy (Best Practices)

**The Testing Pyramid:**

- Many unit tests (fast, isolated, specific)
- Fewer integration tests (moderate speed, component interaction)
- Few end-to-end tests (slow, full system, critical paths)

**Why:** Balance coverage, speed, and maintenance burden.

## Test Design Principles (Best Practices)

**Arrange-Act-Assert pattern:**

```python
def test_user_registration():
    # Arrange: Set up test data
    user_data = {"email": "test@example.com", "password": "secure123"}

    # Act: Perform the action
    result = register_user(user_data)

    # Assert: Verify outcomes
    assert result.success is True
    assert result.user.email == "test@example.com"
```

**Benefits:**

- Clear test structure
- Easy to understand intent
- Maintainable

## When to Mock (Best Practices)

**Mock when:**

- External services (APIs, databases)
- Time-dependent operations
- File system operations
- Random/non-deterministic behavior

**Don't mock when:**

- Testing integration between your components
- Pure functions with no dependencies
- Simple data transformations

## Common Pitfalls

### Pitfall #1: Testing Implementation Details

**Problem:** Tests break when refactoring even though behavior unchanged

```python
# Bad: Tests internal structure
def test_user_service():
    service = UserService()
    assert service._internal_cache is not None  # Implementation detail
```

**Better:** Test behavior, not structure

```python
# Good: Tests observable behavior
def test_user_service_caches_results():
    service = UserService()
    user1 = service.get_user(123)
    user2 = service.get_user(123)
    assert user1 is user2  # Behavior: caching works
```

## Quality Checklist

- ✓ Test names clearly describe what's being tested
- ✓ One assertion concept per test
- ✓ Tests are independent (can run in any order)
- ✓ Mocks used appropriately (external dependencies only)
- ✓ Test data is representative
- ✓ Edge cases covered
- ✓ Fast execution (< 1s for unit tests)

## Documentation References

- Fetch framework-specific docs for syntax
- Testing philosophies: <https://martinfowler.com/articles/practical-test-pyramid.html>

```

**Improvements:**

- ✅ Specific, actionable description
- ✅ Clear structure with progressive disclosure
- ✅ Defers to official docs for syntax
- ✅ Provides interpretive guidance (when to mock, testing pyramid)
- ✅ Concrete examples with explanations
- ✅ Common pitfalls with before/after
- ✅ Validation checklist
- ✅ Substantial enough to warrant a skill

## Creating Skills for Different Purposes

### Interpretive Guidance Skills (Like Forge's Design Skills)

**Purpose:** Help Claude understand how to apply official documentation

**Structure:**
- Fetch official docs first
- Explain what docs mean in practice
- Provide decision frameworks
- Include common gotchas
- Show anti-patterns

**Example:** `agent-design`, `slash-command-design`, `plugin-design`

### Domain Knowledge Skills

**Purpose:** Provide reusable expertise across projects

**Structure:**
- Define principles and philosophy
- Provide decision frameworks
- Include practical examples
- Show common patterns
- Reference external authoritative sources

**Example:** `api-standards`, `security-practices`, `testing-strategy`

### Procedural Skills

**Purpose:** Guide multi-step workflows

**Structure:**
- Clear step-by-step process
- Decision points and branching
- Success criteria
- Common failure modes
- Recovery strategies

**Example:** `deployment-workflow`, `incident-response`, `code-review-checklist`

## File Structure

Skills live in subdirectories within `skills/`:

```

plugin-name/
├── skills/
│   ├── skill-one/
│   │   ├── SKILL.md          # Required: Skill content
│   │   └── helper.py         # Optional: Supporting files
│   └── skill-two/
│       └── SKILL.md

```

**Critical:** Filename must be `SKILL.md` (uppercase), not `skill.md`, `Skill.md`, or `skill.MD`

## Testing Skills

**How to verify a skill works:**

1. Use the Skill tool to invoke it
2. Check if it loads in appropriate contexts
3. Verify the guidance is helpful and accurate
4. Test that official doc references are current
5. Ensure examples run as shown

**Signs of a good skill:**

- Claude provides better answers in the skill's domain
- Reduces need to repeat context
- Catches common mistakes proactively
- Loads automatically when relevant

## Documentation References

Skills are part of the agent system but lightweight:

**Official documentation:**

- https://code.claude.com/docs/en/sub-agents.md - Mentions skills briefly

**Examples of excellent skills:**

- Examine Forge's design skills (agent-design, slash-command-design, plugin-design, hooks-design) for patterns
- Look for skills in well-maintained plugin marketplaces

**Philosophy resources:**

- Progressive disclosure principles
- Token-efficient context management
- Knowledge organization patterns

**Remember:** This meta-skill itself follows the principles it teaches - it defers to official docs, distinguishes specs from best practices, and provides interpretive guidance rather than duplication.
