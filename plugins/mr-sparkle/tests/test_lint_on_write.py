"""Tests for lint_on_write.py hook (thin wrapper over lint.py)."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

HOOK_PATH = Path(__file__).parent.parent / "hooks" / "lint_on_write.py"


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def hook_script():
    """Path to the lint_on_write.py hook."""
    return HOOK_PATH


@pytest.fixture
def python_project_with_ruff(tmp_path):
    """Create a Python project with ruff config."""
    (tmp_path / "pyproject.toml").write_text("[tool.ruff]\nline-length = 88\n")
    (tmp_path / "main.py").write_text("x = 1\n")
    return tmp_path


# =============================================================================
# Tests: Thin wrapper behavior
# =============================================================================


class TestThinWrapper:
    """Test that the hook delegates to lint.py correctly."""

    def test_hook_exists(self, hook_script):
        assert hook_script.is_file()

    def test_lint_script_exists(self, hook_script):
        """The lint.py script that the hook delegates to must exist."""
        lint_script = hook_script.parent.parent / "skills" / "linting" / "scripts" / "lint.py"
        assert lint_script.is_file()

    def test_passes_stdin_to_lint_script(self, hook_script, python_project_with_ruff):
        """Hook should pass stdin through to lint.py --stdin-hook."""
        import shutil

        if not shutil.which("ruff"):
            pytest.skip("ruff not installed")

        file_path = python_project_with_ruff / "main.py"
        hook_input = json.dumps({"tool_input": {"file_path": str(file_path)}})

        result = subprocess.run(
            [sys.executable, str(hook_script)],
            input=hook_input,
            capture_output=True,
            text=True,
        )

        # Hook should always exit 0 (non-blocking)
        assert result.returncode == 0

        # Should produce hook-compatible JSON output
        if result.stdout:
            data = json.loads(result.stdout)
            assert "systemMessage" in data

    def test_exits_zero_on_invalid_json(self, hook_script):
        """Hook should exit 0 even on invalid JSON (silent skip)."""
        result = subprocess.run(
            [sys.executable, str(hook_script)],
            input="not valid json",
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

    def test_exits_zero_on_missing_file_path(self, hook_script):
        """Hook should exit 0 when no file_path in input."""
        hook_input = json.dumps({"tool_input": {}})

        result = subprocess.run(
            [sys.executable, str(hook_script)],
            input=hook_input,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

    def test_exits_zero_on_nonexistent_file(self, hook_script, tmp_path):
        """Hook should exit 0 for nonexistent files."""
        hook_input = json.dumps({"tool_input": {"file_path": str(tmp_path / "does_not_exist.py")}})

        result = subprocess.run(
            [sys.executable, str(hook_script)],
            input=hook_input,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

    def test_exits_zero_on_unknown_extension(self, hook_script, tmp_path):
        """Hook should exit 0 for unknown file types."""
        unknown_file = tmp_path / "file.unknown"
        unknown_file.write_text("content")
        hook_input = json.dumps({"tool_input": {"file_path": str(unknown_file)}})

        result = subprocess.run(
            [sys.executable, str(hook_script)],
            input=hook_input,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0


# =============================================================================
# Tests: Per-project config
# =============================================================================


class TestConfigDisabling:
    """Test that lint_on_write respects per-project config."""

    def test_skips_linting_when_disabled(self, tmp_path):
        """When lint_on_write is disabled for the cwd, hook exits with no output."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        (config_dir / "mr-sparkle.toml").write_text(f'[[overrides]]\nmatch = "{tmp_path}/project"\nlint_on_write = false\n')

        project_dir = tmp_path / "project"
        project_dir.mkdir()
        test_file = project_dir / "main.py"
        test_file.write_text("x=1\n")

        hook_input = json.dumps(
            {
                "tool_input": {"file_path": str(test_file)},
                "cwd": str(project_dir),
            }
        )

        result = subprocess.run(
            [sys.executable, str(HOOK_PATH)],
            input=hook_input,
            capture_output=True,
            text=True,
            env={**os.environ, "NLP_CONFIG_DIR": str(config_dir)},
        )

        assert result.returncode == 0
        assert result.stdout == ""

    def test_runs_normally_when_no_config(self, hook_script, python_project_with_ruff):
        """Without config file, hook runs lint.py normally (fail-open)."""
        import shutil

        if not shutil.which("ruff"):
            pytest.skip("ruff not installed")

        file_path = python_project_with_ruff / "main.py"
        hook_input = json.dumps(
            {
                "tool_input": {"file_path": str(file_path)},
                "cwd": str(python_project_with_ruff),
            }
        )

        result = subprocess.run(
            [sys.executable, str(hook_script)],
            input=hook_input,
            capture_output=True,
            text=True,
            env={**os.environ, "NLP_CONFIG_DIR": "/nonexistent/path"},
        )

        assert result.returncode == 0
        if result.stdout:
            data = json.loads(result.stdout)
            assert "systemMessage" in data
