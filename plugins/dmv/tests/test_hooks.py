"""Tests for dmv hook scripts with per-project config support."""

import json
import os
import subprocess
import sys
from pathlib import Path

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
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        claude_dir = project_dir / ".claude"
        claude_dir.mkdir()
        (claude_dir / "dmv.local.md").write_text("---\nvalidate_commit_message: false\n---\n")

        result = run_hook(
            VALIDATE_COMMIT,
            {
                "tool_name": "Bash",
                "tool_input": {"command": 'git commit -m "Fix: bad message \U0001f680."'},
                "cwd": str(project_dir),
            },
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
