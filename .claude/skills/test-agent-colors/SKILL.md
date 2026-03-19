---
name: test-agent-colors
description: Test all agent colors by invoking each color test agent
---

Test all supported agent colors. This is a two-phase skill because agents are discovered at session startup.

## Colors to test

red, green, blue, yellow, magenta, cyan, white, black, gray, grey, purple, orange, redBright, greenBright, blueBright, yellowBright, magentaBright, cyanBright, whiteBright, blackBright

## Phase 1: Generate agents (if they don't exist)

Check if `.claude/agents/color-red.md` exists. If it does NOT:

1. Run `./scripts/generate-color-agents.sh` from this skill's directory
2. Tell the user: "Color test agents generated. Restart the session and run `/test-agent-colors` again to execute the test."
3. Stop here — do not proceed to Phase 2.

## Phase 2: Run tests and clean up (if agents exist)

If `.claude/agents/color-red.md` exists, the agents are loaded and ready.

1. Invoke agents IN ORDER, four at a time:

   - color-red, color-green, color-blue, color-yellow
   - color-magenta, color-cyan, color-white, color-black
   - color-gray, color-grey, color-purple, color-orange
   - color-redBright, color-greenBright, color-blueBright, color-yellowBright
   - color-magentaBright, color-cyanBright, color-whiteBright, color-blackBright

2. After all agents complete, provide a summary table:

   - Color name
   - Whether it loaded (success/fail)
   - Any notes about visibility or appearance

3. Run `./scripts/cleanup-color-agents.sh` from this skill's directory to remove the generated agents.

4. Tell the user the color agents have been cleaned up.
