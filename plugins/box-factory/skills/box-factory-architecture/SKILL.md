---
name: box-factory-architecture
description: Guidance for using Claude Code component architecture and choosing between agents, skills, commands, and hooks. Helps decide which component type fits a use case, understand delegation and isolation, debug cross-component issues, and design cohesive plugin architectures. Use when choosing component types, designing plugins with multiple components, debugging delegation failures, asking about component interaction patterns, or creating Box Factory-compliant components.
---

# Box Factory Architecture

This meta-skill teaches the Claude Code ecosystem architecture - how components interact, when to use each type, and how to design cohesive multi-component solutions. **This applies to both Main Claude (choosing what to create) and sub-agents (understanding their role).**

## Instructions

1. Select a workflow based on your needs from [Workflow Selection](#workflow-selection)

**Claude Code changes rapidly and is post-training knowledge.** Fetch the [official documentation](#claude-code-official-documentation) when designing components to ensure current specifications.

## Workflow Selection

| If you need...                                                      | Go to ...                                                                               |
| ------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| To understand key architectural concepts                            | [Core Architectural Concepts](#core-architectural-concepts)                             |
| To understand design patterns for multi-component workflows         | [Design Patterns in Claude Code Components](#design-patterns-in-claude-code-components) |
| To understand which individual component to use in a given scenario | [Which Component Should I Choose](#which-component-should-i-choose)                     |
| To understand how components can delegate and communicate           | [Component Communication & Delegation](#component-communication-and-delegation)         |
| To see example component ecosystems                                 | [Example Component Ecosystems](#example-component-ecosystems)                           |
| Recent documentation on all components                              | [Claude Code Official Documentation](#claude-code-official-documentation)               |

## Core Architectural Concepts

Key concepts:

- **Isolation model**: Only the `Main Claude Agent` has user access. All other agents operate in isolated contexts.
- **Return based model** : Agents return complete results, not partial or interactive outputs.
- **Progressive disclosure philosophy:** Knowledge should load progressively when relevant to save tokens.

For detailed explanations of architectural patterns, anti-patterns, and design philosophies, see [Core Architectural Concepts](./core-architecture.md).

## Design Patterns in Claude Code Components

Most common patterns used in multi-component workflows:

| Pattern                                     | Workflow                                  |
| ------------------------------------------- | ----------------------------------------- |
| Simple series of steps or tool call         | `User` -> `Command`                       |
| Complex agent flow triggered by command     | `User` -> `Command` -> `Agent`            |
| Complex agent flow backed by knowledge base | `User` -> `Command` -> `Agent` -> `Skill` |

For detailed references and examples of these patterns, see [Component Interaction Patterns](./component-interaction/component-interaction-patterns.md)

## Component Communication and Delegation

For full details on component delegation and communication abilities, see [Component Communication & Delegation](./component-interaction/component-comms-delegation.md).

## Which Component Should I Choose

Users can customize Claude Code using components broken into roughly three categories.

### Components used by Claude

| Component Type | Purpose                                           | When to Use                                       |
| -------------- | ------------------------------------------------- | ------------------------------------------------- |
| `Sub-agent`    | Isolated AI instances that do work                | Complex logic, autonomous delegation              |
| `Skill`        | Knowledge loaded when needed or relevant          | Substantial interpretive guidance across contexts |
| `Command`      | User-triggered prompts with argument substitution | Simple repeatable actions, explicit user control  |
| `Memory`       | Persistent context and rules                      | Project knowledge, behavior shaping               |
| `MCP server`   | Backend service for tool access                   | Custom tool integrations, specialized transports  |

### Components for the UX of the User

| Component Type | Purpose                                     | When to Use                                 |
| -------------- | ------------------------------------------- | ------------------------------------------- |
| `Hook`         | Deterministic execution at lifecycle events | Guaranteed enforcement, simple rules        |
| `Status Line`  | User interface element showing session info | Custom session metadata display             |
| `Output Style` | Formatting and style for agent responses    | Custom response formats, structured outputs |

### Distribution Wrappers for Components

| Component Type | Purpose                                      | When to Use                            |
| -------------- | -------------------------------------------- | -------------------------------------- |
| `Plugin`       | Packaging and distribution of components     | Bundling multiple components for reuse |
| `Marketplace`  | Platform for browsing and publishing plugins | Discovering and sharing plugins        |

[For detailed breakdown of when to create each component type, see Choosing the Right Component](./choosing-the-right-component.md).

## Claude Code Official Documentation

**Claude Code changes rapidly and is post-training knowledge.** Fetch these docs when designing components to ensure current specifications:

- <https://docs.anthropic.com/en/docs/claude-code/sub-agents> - Agent architecture and isolation model
- <https://docs.anthropic.com/en/docs/claude-code/slash-commands> - Command structure and triggering
- <https://docs.anthropic.com/en/docs/claude-code/hooks> - Hook lifecycle and execution
- <https://docs.anthropic.com/en/docs/claude-code/plugins> - Plugin packaging and distribution
- <https://docs.anthropic.com/en/docs/claude-code/mcp> - MCP server configuration and transports
- <https://docs.anthropic.com/en/docs/claude-code/memory> - CLAUDE.md, rules, and project memory
- <https://docs.anthropic.com/en/docs/claude-code/skills> - Skill definition and loading

## Example Component Ecosystems

A very simple ecosystem:

```markdown
CLAUDE.md    # Basic project memory.  Indicates to use code-reviewer agent when reviewing code.
commands/review-code.md    # Command that triggers code review by delegating to code-reviewer agent.
agents/code-reviewer.md    # Code review agent, looks up guidelines from skill.
skills/code-review-guidelines.md    # Skill with guidance on code review best practices.
```

[See Example Component Ecosystems](./example-component-ecosystems.md) for reference implementations of example systems.
