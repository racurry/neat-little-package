"""Tests for block_direct_markdownlint.py hook."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOK_PATH = Path(__file__).parent.parent / "hooks" / "block_direct_markdownlint.py"


def run_hook(hook_input: dict) -> subprocess.CompletedProcess:
    """Run the hook with given input and return the result."""
    return subprocess.run(
        [sys.executable, str(HOOK_PATH)],
        input=json.dumps(hook_input),
        capture_output=True,
        text=True,
    )


class TestAllowNonBashTools:
    """Hook should allow non-Bash tool invocations."""

    def test_allows_write_tool(self):
        result = run_hook({"tool_name": "Write", "tool_input": {"file_path": "test.md"}})
        assert result.returncode == 0

    def test_allows_edit_tool(self):
        result = run_hook({"tool_name": "Edit", "tool_input": {"file_path": "test.md"}})
        assert result.returncode == 0

    def test_allows_read_tool(self):
        result = run_hook({"tool_name": "Read", "tool_input": {"file_path": "test.md"}})
        assert result.returncode == 0


class TestAllowOtherBashCommands:
    """Hook should allow Bash commands that aren't markdownlint."""

    def test_allows_ls(self):
        result = run_hook({"tool_name": "Bash", "tool_input": {"command": "ls -la"}})
        assert result.returncode == 0

    def test_allows_git(self):
        result = run_hook({"tool_name": "Bash", "tool_input": {"command": "git status"}})
        assert result.returncode == 0

    def test_allows_npm(self):
        result = run_hook({"tool_name": "Bash", "tool_input": {"command": "npm install"}})
        assert result.returncode == 0

    def test_allows_grep_with_markdownlint_in_output(self):
        # Should allow grep even if searching for markdownlint
        result = run_hook({
            "tool_name": "Bash",
            "tool_input": {"command": "grep markdownlint-cli2 package.json"}
        })
        assert result.returncode == 0


class TestBlockDirectMarkdownlint:
    """Hook should block direct markdownlint-cli2 without --config."""

    def test_blocks_simple_invocation(self):
        result = run_hook({
            "tool_name": "Bash",
            "tool_input": {"command": "markdownlint-cli2 README.md"}
        })
        assert result.returncode == 2
        assert "markdownlint-cli2 requires a --config" in result.stderr

    def test_blocks_with_fix_flag(self):
        result = run_hook({
            "tool_name": "Bash",
            "tool_input": {"command": "markdownlint-cli2 --fix docs/"}
        })
        assert result.returncode == 2

    def test_blocks_glob_pattern(self):
        result = run_hook({
            "tool_name": "Bash",
            "tool_input": {"command": "markdownlint-cli2 **/*.md"}
        })
        assert result.returncode == 2

    def test_error_message_suggests_slash_command(self):
        result = run_hook({
            "tool_name": "Bash",
            "tool_input": {"command": "markdownlint-cli2 README.md"}
        })
        assert "/mr-sparkle:lint-md" in result.stderr


class TestAllowMarkdownlintWithConfig:
    """Hook should allow markdownlint-cli2 when --config is specified."""

    def test_allows_with_config_flag(self):
        result = run_hook({
            "tool_name": "Bash",
            "tool_input": {"command": "markdownlint-cli2 --config .markdownlint.json README.md"}
        })
        assert result.returncode == 0

    def test_allows_config_at_end(self):
        result = run_hook({
            "tool_name": "Bash",
            "tool_input": {"command": "markdownlint-cli2 README.md --config ~/.markdownlint.jsonc"}
        })
        assert result.returncode == 0

    def test_allows_with_fix_and_config(self):
        result = run_hook({
            "tool_name": "Bash",
            "tool_input": {"command": "markdownlint-cli2 --fix --config config.json docs/"}
        })
        assert result.returncode == 0


class TestEdgeCases:
    """Edge cases and malformed input handling."""

    def test_empty_command(self):
        result = run_hook({"tool_name": "Bash", "tool_input": {"command": ""}})
        assert result.returncode == 0

    def test_missing_command(self):
        result = run_hook({"tool_name": "Bash", "tool_input": {}})
        assert result.returncode == 0

    def test_missing_tool_input(self):
        result = run_hook({"tool_name": "Bash"})
        assert result.returncode == 0

    def test_invalid_json_input(self):
        # Run with invalid JSON
        result = subprocess.run(
            [sys.executable, str(HOOK_PATH)],
            input="not valid json",
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0  # Graceful handling

    def test_markdownlint_not_at_start(self):
        # Should allow if markdownlint-cli2 isn't at the start
        result = run_hook({
            "tool_name": "Bash",
            "tool_input": {"command": "echo markdownlint-cli2 test"}
        })
        assert result.returncode == 0

    def test_just_markdownlint_no_space(self):
        # "markdownlint-cli2" without trailing space shouldn't match
        result = run_hook({
            "tool_name": "Bash",
            "tool_input": {"command": "markdownlint-cli2"}
        })
        assert result.returncode == 0  # No space after, doesn't match pattern
