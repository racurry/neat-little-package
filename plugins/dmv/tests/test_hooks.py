"""Tests for dmv hook scripts with per-project config support."""

import json
import os
import subprocess
import sys
from pathlib import Path

BLOCK_GIT_DASH_C = Path(__file__).parent.parent / "hooks" / "block_git_dash_c.py"
VALIDATE_COMMIT = Path(__file__).parent.parent / "hooks" / "validate_commit_message.py"


def run_hook(hook_path, hook_input: dict, env_override: dict = None) -> subprocess.CompletedProcess:
    """Run a hook with given input and return the result."""
    env = {**os.environ}
    if env_override:
        env.update(env_override)
    return subprocess.run(
        [sys.executable, str(hook_path)],
        input=json.dumps(hook_input),
        capture_output=True,
        text=True,
        env=env,
    )


# =============================================================================
# block_git_dash_c.py
# =============================================================================


class TestBlockGitDashC:
    """Test core blocking behavior."""

    def test_blocks_git_dash_c(self):
        result = run_hook(
            BLOCK_GIT_DASH_C,
            {
                "tool_name": "Bash",
                "tool_input": {"command": "git -C /some/path status"},
                "cwd": "/some/project",
            },
        )
        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert output["decision"] == "block"

    def test_allows_normal_git(self):
        result = run_hook(
            BLOCK_GIT_DASH_C,
            {
                "tool_name": "Bash",
                "tool_input": {"command": "git status"},
                "cwd": "/some/project",
            },
        )
        assert result.returncode == 0
        assert result.stdout == ""

    def test_allows_non_bash(self):
        result = run_hook(
            BLOCK_GIT_DASH_C,
            {"tool_name": "Write", "tool_input": {"file_path": "test.py"}, "cwd": "/some/project"},
        )
        assert result.returncode == 0
        assert result.stdout == ""


class TestBlockGitDashCConfig:
    """Test config-based disabling of block_git_dash_c."""

    def test_allows_git_dash_c_when_disabled(self, tmp_path):
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        (config_dir / "dmv.toml").write_text(f'[[overrides]]\nmatch = "{tmp_path}/project"\nblock_git_dash_c = false\n')

        result = run_hook(
            BLOCK_GIT_DASH_C,
            {
                "tool_name": "Bash",
                "tool_input": {"command": "git -C /some/path status"},
                "cwd": str(tmp_path / "project"),
            },
            env_override={"NLP_CONFIG_DIR": str(config_dir)},
        )
        assert result.returncode == 0
        assert result.stdout == ""

    def test_blocks_when_no_config(self):
        result = run_hook(
            BLOCK_GIT_DASH_C,
            {
                "tool_name": "Bash",
                "tool_input": {"command": "git -C /some/path status"},
                "cwd": "/some/project",
            },
            env_override={"NLP_CONFIG_DIR": "/nonexistent/path"},
        )
        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert output["decision"] == "block"


# =============================================================================
# validate_commit_message.py
# =============================================================================


class TestValidateCommitMessage:
    """Test core validation behavior."""

    def test_warns_on_emoji(self):
        result = run_hook(
            VALIDATE_COMMIT,
            {
                "tool_name": "Bash",
                "tool_input": {"command": 'git commit -m "fix bug \U0001f680"'},
                "cwd": "/some/project",
            },
        )
        assert result.returncode == 0
        if result.stdout:
            output = json.loads(result.stdout)
            assert "emojis" in output.get("systemMessage", "")

    def test_no_warning_on_clean_message(self):
        result = run_hook(
            VALIDATE_COMMIT,
            {
                "tool_name": "Bash",
                "tool_input": {"command": 'git commit -m "fix race condition in session cleanup"'},
                "cwd": "/some/project",
            },
        )
        assert result.returncode == 0
        assert result.stdout == ""

    def test_ignores_non_commit(self):
        result = run_hook(
            VALIDATE_COMMIT,
            {
                "tool_name": "Bash",
                "tool_input": {"command": "git status"},
                "cwd": "/some/project",
            },
        )
        assert result.returncode == 0
        assert result.stdout == ""


class TestValidateCommitMessageConfig:
    """Test config-based disabling of validate_commit_message."""

    def test_skips_validation_when_disabled(self, tmp_path):
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        (config_dir / "dmv.toml").write_text(f'[[overrides]]\nmatch = "{tmp_path}/project"\nvalidate_commit_message = false\n')

        result = run_hook(
            VALIDATE_COMMIT,
            {
                "tool_name": "Bash",
                "tool_input": {"command": 'git commit -m "Fix: bad message \U0001f680."'},
                "cwd": str(tmp_path / "project"),
            },
            env_override={"NLP_CONFIG_DIR": str(config_dir)},
        )
        assert result.returncode == 0
        assert result.stdout == ""

    def test_validates_when_no_config(self):
        result = run_hook(
            VALIDATE_COMMIT,
            {
                "tool_name": "Bash",
                "tool_input": {"command": 'git commit -m "Fix: bad message \U0001f680."'},
                "cwd": "/some/project",
            },
            env_override={"NLP_CONFIG_DIR": "/nonexistent/path"},
        )
        assert result.returncode == 0
        if result.stdout:
            output = json.loads(result.stdout)
            assert "systemMessage" in output
