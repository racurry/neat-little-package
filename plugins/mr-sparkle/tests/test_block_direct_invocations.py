"""Tests for block_direct_invocations.sh hook."""

import json
import os
import subprocess
from pathlib import Path


HOOK_PATH = Path(__file__).parent.parent / "hooks" / "block_direct_invocations.sh"


def run_hook(hook_input: dict, env_override: dict = None) -> subprocess.CompletedProcess:
    """Run the hook with given input and return the result."""
    env = {**os.environ}
    if env_override:
        env.update(env_override)
    return subprocess.run(
        ["bash", str(HOOK_PATH)],
        input=json.dumps(hook_input),
        capture_output=True,
        text=True,
        env=env,
    )


class TestAllowNonBashTools:
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
        result = run_hook({"tool_name": "Bash", "tool_input": {"command": "grep markdownlint-cli2 package.json"}})
        assert result.returncode == 0


class TestBlockDirectMarkdownlint:
    def test_blocks_simple_invocation(self):
        result = run_hook({"tool_name": "Bash", "tool_input": {"command": "markdownlint-cli2 README.md"}})
        assert result.returncode == 2
        assert "markdownlint-cli2" in result.stderr

    def test_blocks_with_fix_flag(self):
        result = run_hook({"tool_name": "Bash", "tool_input": {"command": "markdownlint-cli2 --fix docs/"}})
        assert result.returncode == 2

    def test_blocks_glob_pattern(self):
        result = run_hook({"tool_name": "Bash", "tool_input": {"command": "markdownlint-cli2 **/*.md"}})
        assert result.returncode == 2

    def test_error_message_suggests_lint(self):
        result = run_hook({"tool_name": "Bash", "tool_input": {"command": "markdownlint-cli2 README.md"}})
        assert "/mr-sparkle:lint" in result.stderr


class TestAllowMarkdownlintWithConfig:
    def test_allows_with_config_flag(self):
        result = run_hook({"tool_name": "Bash", "tool_input": {"command": "markdownlint-cli2 --config .markdownlint.json README.md"}})
        assert result.returncode == 0

    def test_allows_config_at_end(self):
        result = run_hook({"tool_name": "Bash", "tool_input": {"command": "markdownlint-cli2 README.md --config ~/.markdownlint.jsonc"}})
        assert result.returncode == 0

    def test_allows_with_fix_and_config(self):
        result = run_hook({"tool_name": "Bash", "tool_input": {"command": "markdownlint-cli2 --fix --config config.json docs/"}})
        assert result.returncode == 0


class TestEdgeCases:
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
        result = subprocess.run(
            ["bash", str(HOOK_PATH)],
            input="not valid json",
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

    def test_markdownlint_not_at_start(self):
        result = run_hook({"tool_name": "Bash", "tool_input": {"command": "echo markdownlint-cli2 test"}})
        assert result.returncode == 0

    def test_just_markdownlint_no_space(self):
        result = run_hook({"tool_name": "Bash", "tool_input": {"command": "markdownlint-cli2"}})
        assert result.returncode == 0


class TestConfigDisabling:
    def test_allows_when_block_direct_disabled(self, tmp_path):
        """When block_direct: [] in config, direct invocations are allowed."""
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        claude_dir = project_dir / ".claude"
        claude_dir.mkdir()
        (claude_dir / "mr-sparkle.config.yml").write_text("block_direct: []\n")

        result = run_hook(
            {
                "tool_name": "Bash",
                "tool_input": {"command": "markdownlint-cli2 README.md"},
                "cwd": str(project_dir),
            },
        )
        assert result.returncode == 0

    def test_blocks_when_no_config(self):
        result = run_hook(
            {
                "tool_name": "Bash",
                "tool_input": {"command": "markdownlint-cli2 README.md"},
                "cwd": "/nonexistent/project",
            },
        )
        assert result.returncode == 2
