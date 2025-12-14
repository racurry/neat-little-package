# Component Communication & Delegation

All interactions involve the `User` and the `Main Claude Agent`.

## Overview

Every component is only able to interact with certain other components. There is a clear flow of information and control.

## Component Selection

| Component...        | Go to ...                               |
| ------------------- | --------------------------------------- |
| `User`              | [User](#user)                           |
| `Main Claude Agent` | [Main Claude Agent](#main-claude-agent) |
| `Command`           | [Command](#command)                     |
| `Sub-agent`         | [Sub-agent](#sub-agent)                 |
| `Skill`             | [Skill](#skill)                         |
| `MCP server`        | [MCP Server](#mcp-server)               |
| `Memory`            | [Memory](#memory)                       |

User experience and plugin components are not part of the agentic flow, but for reference:

| Component...   | Go to ...                                    |
| -------------- | -------------------------------------------- |
| `Hooks`        | [UX Components](#user-experience-components) |
| `Status Line`  | [UX Components](#user-experience-components) |
| `Output Style` | [UX Components](#user-experience-components) |
| `Plugin`       | [Plugin Components](#plugin-components)      |
| `Marketplace`  | [Plugin Components](#plugin-components)      |

## See Also

- [Choosing the Right Component](../components/choosing-the-right-component.md)
- [Interaction Patterns](./interaction-patterns.md)

## Components

### `User`

Users CAN:

- Send a request to the `Main Claude Agent`
- Directly invoke `Command` with /command syntax

Users CANNOT:

- Directly access a `Skill`
- Directly invoke an `Sub-agent`
- Directly access an `MCP Server`
- Directly access `Memory`

### `Main Claude Agent`

The `Main Claude Agent` CAN:

- Choose to invoke a `Command`
- Choose to delegate actions to an `Sub-agent`
- Reference a `Skill` to guide itself
- Choose to use an `MCP Server`
- Reference `Memory` based on the context & ruleset defined for the memory

The `Main Claude Agent` has has nothing on its CANNOT list!

### `Command`

`Commands` are re-usable prompts that the `Main Claude Agent` uses when invoked by the `User`.

`Commands` CAN:

- Instruct the `Main Claude Agent` to perform a series of actions or follow its prompt
- Instruct the `Main Claude Agent` to collect information from the `User`
- Instruct the `Main Claude Agent` to delegate work to an `Sub-agent`
- Instruct the `Main Claude Agent` to reference a `Skill`
- Instruct the `Main Claude Agent` to use an `MCP server`
- Reference `Memory` based on the context & ruleset defined for the memory

`Commands` CANNOT:

- Invoke another `Command`

### `Sub-agent`

`Sub-agents` are entirely separate from the `Main Claude Agent`. They have their own standalone prompt, their own context, and run in isolation.

`Sub-agents` CAN:

- Instruct itself to perform a series of actions or follow its prompt separate from the `Main Claude Agent`
- Reference and use a `Skill` to guide itself
- Reference and use an `MCP server`
- Reference `Memory` based on the context & ruleset defined for the memory
- Return information back to the `Main Claude Agent` when complete

`Sub-agents` CANNOT:

- Interact directly with the `User`
- See the main conversation between the `User` and the `Main Claude Agent`
- Invoke `Commands`
- Spawn other sub-agents (only `Main Claude Agent` can delegate to sub-agents via the Task tool)

### `Memory`

`Memory` in Claude is a series of instructions, notes, and rules, loaded into the main prompt.

`Memory` CAN:

- Contain references to other components

`Memory` CANNOT:

- Take any action directly

### `MCP Server`

`MCP Servers` are external systems that provide data or perform actions.

`MCP Servers` CANNOT initiate interactions with any components at all.

### `Skill`

`Skills` are re-usable pieces of knowledge or guidance.

`Skills` have no CAN list!

`Skills` CANNOT:

- Initiate interactions at all.
- Reference any other components

### User Experience Components

`Status Lines`, `Hooks`, and `Output Styles` are user experience components and aren't part of the agentic flow.

### Plugin Components

`Plugins` and `Marketplaces` are systems for distributing and installing components, and aren't part of the agentic flow.
