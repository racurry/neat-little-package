"""Tests for lint_on_write.py hook."""

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Import the module under test
sys.path.insert(0, str(Path(__file__).parent.parent / "hooks"))
import lint_on_write as low


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary project directory."""
    return tmp_path


@pytest.fixture
def python_project_with_ruff(tmp_path):
    """Create a Python project with ruff config."""
    (tmp_path / "pyproject.toml").write_text("[tool.ruff]\nline-length = 88\n")
    (tmp_path / "main.py").write_text("x = 1\n")
    return tmp_path


@pytest.fixture
def python_project_with_black(tmp_path):
    """Create a Python project with black config."""
    (tmp_path / "pyproject.toml").write_text("[tool.black]\nline-length = 88\n")
    (tmp_path / "main.py").write_text("x = 1\n")
    return tmp_path


@pytest.fixture
def python_project_with_isort_and_black(tmp_path):
    """Create a Python project with isort and black config."""
    (tmp_path / "pyproject.toml").write_text('[tool.isort]\nprofile = "black"\n\n[tool.black]\nline-length = 88\n')
    (tmp_path / "main.py").write_text("x = 1\n")
    return tmp_path


@pytest.fixture
def js_project_with_biome(tmp_path):
    """Create a JS project with biome config."""
    (tmp_path / "package.json").write_text('{"devDependencies": {"@biomejs/biome": "^1.0.0"}}')
    (tmp_path / "biome.json").write_text("{}")
    (tmp_path / "index.js").write_text("const x = 1;\n")
    return tmp_path


@pytest.fixture
def js_project_with_eslint(tmp_path):
    """Create a JS project with eslint config."""
    (tmp_path / "package.json").write_text('{"devDependencies": {"eslint": "^8.0.0"}}')
    (tmp_path / "eslint.config.js").write_text("module.exports = {};\n")
    (tmp_path / "index.js").write_text("const x = 1;\n")
    return tmp_path


@pytest.fixture
def js_project_with_prettier(tmp_path):
    """Create a JS project with prettier config."""
    (tmp_path / "package.json").write_text('{"devDependencies": {"prettier": "^3.0.0"}}')
    (tmp_path / ".prettierrc").write_text("{}")
    (tmp_path / "index.js").write_text("const x = 1;\n")
    return tmp_path


@pytest.fixture
def shell_project(tmp_path):
    """Create a project with shell scripts."""
    (tmp_path / ".git").mkdir()
    (tmp_path / "script.sh").write_text('#!/bin/bash\necho "hello"\n')
    return tmp_path


@pytest.fixture
def markdown_project(tmp_path):
    """Create a project with markdown files."""
    (tmp_path / ".git").mkdir()
    (tmp_path / "README.md").write_text("# Title\n\nContent here.\n")
    return tmp_path


# =============================================================================
# Tests: find_project_root
# =============================================================================


class TestFindProjectRoot:
    def test_finds_pyproject_toml(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("")
        subdir = tmp_path / "src"
        subdir.mkdir()
        file_path = subdir / "main.py"
        file_path.write_text("")

        result = low.find_project_root(str(file_path))
        assert result == tmp_path

    def test_finds_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("{}")
        subdir = tmp_path / "src"
        subdir.mkdir()
        file_path = subdir / "index.js"
        file_path.write_text("")

        result = low.find_project_root(str(file_path))
        assert result == tmp_path

    def test_finds_git_directory(self, tmp_path):
        (tmp_path / ".git").mkdir()
        subdir = tmp_path / "src"
        subdir.mkdir()
        file_path = subdir / "script.sh"
        file_path.write_text("")

        result = low.find_project_root(str(file_path))
        assert result == tmp_path

    def test_prefers_package_json_over_git(self, tmp_path):
        """package.json found first when walking up."""
        (tmp_path / ".git").mkdir()
        subdir = tmp_path / "packages" / "frontend"
        subdir.mkdir(parents=True)
        (subdir / "package.json").write_text("{}")
        file_path = subdir / "index.js"
        file_path.write_text("")

        result = low.find_project_root(str(file_path))
        assert result == subdir

    def test_returns_none_when_no_markers(self, tmp_path):
        file_path = tmp_path / "orphan.py"
        file_path.write_text("")

        # May find something in parent directories, or None
        # This depends on the actual filesystem - just verify it doesn't crash
        low.find_project_root(str(file_path))


# =============================================================================
# Tests: check_pyproject_key
# =============================================================================


class TestCheckPyprojectKey:
    def test_finds_existing_key(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[tool.ruff]\nline-length = 88\n")
        assert low.check_pyproject_key(tmp_path, "tool.ruff") is True

    def test_finds_nested_key(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[tool.black]\nline-length = 88\n")
        assert low.check_pyproject_key(tmp_path, "tool.black") is True

    def test_returns_false_for_missing_key(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[tool.black]\nline-length = 88\n")
        assert low.check_pyproject_key(tmp_path, "tool.ruff") is False

    def test_returns_false_when_no_pyproject(self, tmp_path):
        assert low.check_pyproject_key(tmp_path, "tool.ruff") is False

    def test_handles_invalid_toml(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("invalid [ toml")
        assert low.check_pyproject_key(tmp_path, "tool.ruff") is False


# =============================================================================
# Tests: has_project_config
# =============================================================================


class TestHasProjectConfig:
    def test_detects_ruff_in_pyproject(self, python_project_with_ruff):
        assert low.has_project_config("ruff", python_project_with_ruff) is True

    def test_detects_ruff_toml_file(self, tmp_path):
        (tmp_path / "ruff.toml").write_text("")
        assert low.has_project_config("ruff", tmp_path) is True

    def test_detects_dot_ruff_toml(self, tmp_path):
        (tmp_path / ".ruff.toml").write_text("")
        assert low.has_project_config("ruff", tmp_path) is True

    def test_detects_black_in_pyproject(self, python_project_with_black):
        assert low.has_project_config("black", python_project_with_black) is True

    def test_detects_biome_in_package_json(self, js_project_with_biome):
        assert low.has_project_config("biome", js_project_with_biome) is True

    def test_detects_biome_json_file(self, tmp_path):
        (tmp_path / "package.json").write_text("{}")
        (tmp_path / "biome.json").write_text("{}")
        assert low.has_project_config("biome", tmp_path) is True

    def test_detects_eslint_config(self, js_project_with_eslint):
        assert low.has_project_config("eslint", js_project_with_eslint) is True

    def test_detects_prettier_config(self, js_project_with_prettier):
        assert low.has_project_config("prettier", js_project_with_prettier) is True

    def test_returns_false_when_no_config(self, tmp_path):
        (tmp_path / "package.json").write_text("{}")
        assert low.has_project_config("ruff", tmp_path) is False
        assert low.has_project_config("biome", tmp_path) is False

    def test_returns_false_when_no_project_root(self):
        assert low.has_project_config("ruff", None) is False

    def test_detects_isort_in_setup_cfg(self, tmp_path):
        (tmp_path / "setup.cfg").write_text("[isort]\nprofile = black\n")
        assert low.has_project_config("isort", tmp_path) is True

    def test_detects_pylint_in_pylintrc(self, tmp_path):
        (tmp_path / ".pylintrc").write_text("[MESSAGES CONTROL]\ndisable = C0114\n")
        assert low.has_project_config("pylint", tmp_path) is True

    def test_detects_pylint_in_setup_cfg(self, tmp_path):
        (tmp_path / "setup.cfg").write_text("[pylint]\nmax-line-length = 100\n")
        assert low.has_project_config("pylint", tmp_path) is True

    def test_detects_pylint_in_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[tool.pylint]\nmax-line-length = 100\n")
        assert low.has_project_config("pylint", tmp_path) is True


# =============================================================================
# Tests: has_ini_section
# =============================================================================


class TestHasIniSection:
    def test_finds_section_in_setup_cfg(self, tmp_path):
        (tmp_path / "setup.cfg").write_text("[isort]\nprofile = black\n")
        tool_def = {"ini_sections": [{"file": "setup.cfg", "section": "isort"}]}
        assert low.has_ini_section(tool_def, tmp_path) is True

    def test_returns_false_when_section_missing(self, tmp_path):
        (tmp_path / "setup.cfg").write_text("[metadata]\nname = myproject\n")
        tool_def = {"ini_sections": [{"file": "setup.cfg", "section": "isort"}]}
        assert low.has_ini_section(tool_def, tmp_path) is False

    def test_returns_false_when_file_missing(self, tmp_path):
        tool_def = {"ini_sections": [{"file": "setup.cfg", "section": "isort"}]}
        assert low.has_ini_section(tool_def, tmp_path) is False

    def test_returns_false_when_no_ini_sections_defined(self, tmp_path):
        tool_def = {}
        assert low.has_ini_section(tool_def, tmp_path) is False

    def test_handles_invalid_ini_file(self, tmp_path):
        (tmp_path / "setup.cfg").write_text("not valid ini {{{{")
        tool_def = {"ini_sections": [{"file": "setup.cfg", "section": "isort"}]}
        assert low.has_ini_section(tool_def, tmp_path) is False


# =============================================================================
# Tests: select_tools
# =============================================================================


class TestSelectTools:
    def test_python_with_ruff_config(self, python_project_with_ruff):
        tools = low.select_tools("python", python_project_with_ruff)
        assert tools == ["ruff"]

    def test_python_with_black_config(self, python_project_with_black):
        tools = low.select_tools("python", python_project_with_black)
        assert tools == ["black"]

    def test_python_with_isort_and_black(self, python_project_with_isort_and_black):
        tools = low.select_tools("python", python_project_with_isort_and_black)
        assert tools == ["isort", "black"]

    def test_python_with_pylint(self, tmp_path):
        """pylint configured -> uses traditional toolchain."""
        (tmp_path / ".pylintrc").write_text("[MESSAGES CONTROL]\ndisable = C0114\n")
        tools = low.select_tools("python", tmp_path)
        assert tools == ["pylint"]

    def test_python_with_pylint_and_black(self, tmp_path):
        """pylint + black configured -> both run."""
        (tmp_path / ".pylintrc").write_text("[MESSAGES CONTROL]\n")
        (tmp_path / "pyproject.toml").write_text("[tool.black]\nline-length = 88\n")
        tools = low.select_tools("python", tmp_path)
        assert tools == ["pylint", "black"]

    def test_python_with_full_traditional_toolchain(self, tmp_path):
        """pylint + isort + black all configured."""
        (tmp_path / "setup.cfg").write_text("[pylint]\n\n[isort]\nprofile = black\n")
        (tmp_path / "pyproject.toml").write_text("[tool.black]\nline-length = 88\n")
        tools = low.select_tools("python", tmp_path)
        assert tools == ["pylint", "isort", "black"]

    def test_python_fallback_to_ruff(self, tmp_path):
        """No config -> fallback to first tool in first group (ruff)."""
        tools = low.select_tools("python", tmp_path)
        assert tools == ["ruff"]

    def test_js_with_biome(self, js_project_with_biome):
        tools = low.select_tools("js_ts", js_project_with_biome)
        assert tools == ["biome"]

    def test_js_with_eslint_only(self, js_project_with_eslint):
        """eslint config but no prettier -> only eslint."""
        tools = low.select_tools("js_ts", js_project_with_eslint)
        assert tools == ["eslint"]

    def test_js_with_eslint_and_prettier(self, tmp_path):
        """Both eslint and prettier configured."""
        (tmp_path / "package.json").write_text('{"devDependencies": {"eslint": "^8", "prettier": "^3"}}')
        (tmp_path / ".eslintrc.json").write_text("{}")
        (tmp_path / ".prettierrc").write_text("{}")

        tools = low.select_tools("js_ts", tmp_path)
        assert tools == ["eslint", "prettier"]

    def test_js_fallback_to_biome(self, tmp_path):
        """No config -> fallback to biome."""
        tools = low.select_tools("js_ts", tmp_path)
        assert tools == ["biome"]

    def test_shell_fallback(self, tmp_path):
        """Shell tools fallback to entire first group (shfmt + shellcheck)."""
        tools = low.select_tools("shell", tmp_path)
        assert tools == ["shfmt", "shellcheck"]

    def test_markdown_fallback(self, tmp_path):
        """Markdown fallback to markdownlint."""
        tools = low.select_tools("markdown", tmp_path)
        assert tools == ["markdownlint"]


# =============================================================================
# Tests: run_tool
# =============================================================================


class TestRunTool:
    def test_returns_none_when_binary_not_found(self, tmp_path):
        file_path = tmp_path / "test.py"
        file_path.write_text("")

        with patch("shutil.which", return_value=None):
            result = low.run_tool(str(file_path), "ruff", tmp_path)
        assert result is None

    def test_returns_result_on_success(self, tmp_path):
        file_path = tmp_path / "test.py"
        file_path.write_text("x = 1\n")

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""

        with patch("shutil.which", return_value="/usr/bin/ruff"):
            with patch("subprocess.run", return_value=mock_result):
                result = low.run_tool(str(file_path), "ruff", tmp_path)

        assert result is not None
        assert result.name == "ruff"
        assert result.status == low.Status.OK

    def test_returns_warning_on_lint_errors(self, tmp_path):
        file_path = tmp_path / "test.py"
        file_path.write_text("x = 1\n")

        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = "Found 1 error"
        mock_result.stderr = ""

        with patch("shutil.which", return_value="/usr/bin/ruff"):
            with patch("subprocess.run", return_value=mock_result):
                result = low.run_tool(str(file_path), "ruff", tmp_path)

        assert result is not None
        assert result.status == low.Status.WARNING
        assert "Found 1 error" in result.output

    def test_returns_error_on_timeout(self, tmp_path):
        file_path = tmp_path / "test.py"
        file_path.write_text("x = 1\n")

        with patch("shutil.which", return_value="/usr/bin/ruff"):
            with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("ruff", 60)):
                result = low.run_tool(str(file_path), "ruff", tmp_path)

        assert result is not None
        assert result.status == low.Status.ERROR
        assert "timed out" in result.output

    def test_skips_markdownlint_without_global_config(self, tmp_path):
        """When no project config, markdownlint needs global_config_location to exist."""
        file_path = tmp_path / "README.md"
        file_path.write_text("# Test\n")

        # No project config exists, so has_project_config returns False
        # Mock user_config path to not exist
        with patch("shutil.which", return_value="/usr/bin/markdownlint-cli2"):
            with patch.object(Path, "expanduser", return_value=Path("/fake/.markdownlint-cli2.jsonc")):
                with patch.object(Path, "is_file", return_value=False):
                    result = low.run_tool(str(file_path), "markdownlint", tmp_path)

        assert result is None


# =============================================================================
# Tests: format_results
# =============================================================================


class TestFormatResults:
    def test_empty_results(self):
        summary, context = low.format_results("/path/to/file.py", [])
        assert summary == ""
        assert context is None

    def test_all_skipped(self):
        results = [low.ToolResult("ruff", low.Status.SKIPPED)]
        summary, context = low.format_results("/path/to/file.py", results)
        assert summary == ""

    def test_success_formatting(self):
        results = [low.ToolResult("ruff", low.Status.OK)]
        summary, context = low.format_results("/path/to/file.py", results)
        assert "ruff" in summary
        assert "file.py" in summary
        assert "OK" in summary
        # OK status now surfaces context to Claude so it knows linting ran
        assert context == "ruff file.py: OK"

    def test_warning_formatting(self):
        results = [low.ToolResult("ruff", low.Status.WARNING, "line 1: error")]
        summary, context = low.format_results("/path/to/file.py", results)
        assert "Lint errors" in summary
        assert context == "line 1: error"

    def test_error_formatting(self):
        results = [low.ToolResult("ruff", low.Status.ERROR, "execution failed")]
        summary, context = low.format_results("/path/to/file.py", results)
        assert "execution failed" in summary

    def test_multiple_tools_formatting(self):
        results = [
            low.ToolResult("isort", low.Status.OK),
            low.ToolResult("black", low.Status.OK),
        ]
        summary, context = low.format_results("/path/to/file.py", results)
        assert "isort" in summary
        assert "black" in summary


# =============================================================================
# Tests: extract_file_path
# =============================================================================


class TestExtractFilePath:
    def test_extracts_file_path(self):
        hook_input = {"tool_input": {"file_path": "/path/to/file.py"}}
        assert low.extract_file_path(hook_input) == "/path/to/file.py"

    def test_returns_none_for_missing_tool_input(self):
        assert low.extract_file_path({}) is None

    def test_returns_none_for_missing_file_path(self):
        assert low.extract_file_path({"tool_input": {}}) is None

    def test_returns_none_for_non_string_file_path(self):
        assert low.extract_file_path({"tool_input": {"file_path": 123}}) is None

    def test_returns_none_for_empty_string(self):
        assert low.extract_file_path({"tool_input": {"file_path": ""}}) is None

    def test_returns_none_for_null_file_path(self):
        assert low.extract_file_path({"tool_input": {"file_path": None}}) is None


# =============================================================================
# Tests: Extension mapping
# =============================================================================


class TestExtensionMapping:
    @pytest.mark.parametrize(
        "ext,expected",
        [
            (".py", "python"),
            (".md", "markdown"),
            (".markdown", "markdown"),
            (".js", "js_ts"),
            (".jsx", "js_ts"),
            (".ts", "js_ts"),
            (".tsx", "js_ts"),
            (".mjs", "js_ts"),
            (".cjs", "js_ts"),
            (".mts", "js_ts"),
            (".cts", "js_ts"),
            (".sh", "shell"),
            (".bash", "shell"),
            (".zsh", "shell"),
        ],
    )
    def test_extension_maps_to_toolset(self, ext, expected):
        assert low.EXTENSION_TO_TOOLSET.get(ext) == expected

    def test_unknown_extension_returns_none(self):
        assert low.EXTENSION_TO_TOOLSET.get(".unknown") is None


# =============================================================================
# Tests: Toolset structure validation
# =============================================================================


class TestToolsetStructure:
    def test_all_toolsets_have_groups(self):
        for name, groups in low.TOOLSETS.items():
            assert isinstance(groups, list), f"{name} should be a list"
            assert len(groups) > 0, f"{name} should have at least one group"
            for group in groups:
                assert isinstance(group, list), f"{name} groups should be lists"
                assert len(group) > 0, f"{name} groups should not be empty"

    def test_all_tools_in_toolsets_are_defined(self):
        for toolset_name, groups in low.TOOLSETS.items():
            for group in groups:
                for tool_name in group:
                    assert tool_name in low.TOOLS, f"{tool_name} in {toolset_name} not defined in TOOLS"

    def test_all_tools_have_required_fields(self):
        for name, tool in low.TOOLS.items():
            assert "binary" in tool, f"{name} missing 'binary'"
            assert "commands" in tool, f"{name} missing 'commands'"
            assert isinstance(tool["commands"], list), f"{name} commands should be list"


# =============================================================================
# Tests: output_response
# =============================================================================


class TestOutputResponse:
    def test_system_message_only(self, capsys):
        low.output_response(system_message="Test message")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["systemMessage"] == "Test message"

    def test_with_additional_context(self, capsys):
        low.output_response(system_message="Warning", additional_context="Details here")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "hookSpecificOutput" in data
        assert data["hookSpecificOutput"]["additionalContext"] == "Details here"

    def test_empty_response_outputs_nothing(self, capsys):
        low.output_response()
        captured = capsys.readouterr()
        assert captured.out == ""


# =============================================================================
# Integration Tests
# =============================================================================


class TestIntegration:
    """End-to-end tests for the main flow."""

    def test_python_file_with_ruff_project(self, python_project_with_ruff):
        """Python file in project with ruff config uses ruff."""
        file_path = python_project_with_ruff / "main.py"
        project_root = low.find_project_root(str(file_path))

        assert project_root == python_project_with_ruff
        assert low.has_project_config("ruff", project_root) is True

        tools = low.select_tools("python", project_root)
        assert tools == ["ruff"]

    def test_js_file_with_biome_project(self, js_project_with_biome):
        """JS file in project with biome config uses biome."""
        file_path = js_project_with_biome / "index.js"
        project_root = low.find_project_root(str(file_path))

        assert project_root == js_project_with_biome
        assert low.has_project_config("biome", project_root) is True

        tools = low.select_tools("js_ts", project_root)
        assert tools == ["biome"]

    def test_biome_takes_priority_over_eslint(self, tmp_path):
        """When both biome and eslint are configured, biome wins (first group)."""
        (tmp_path / "package.json").write_text('{"devDependencies": {"@biomejs/biome": "^1", "eslint": "^8"}}')
        (tmp_path / "biome.json").write_text("{}")
        (tmp_path / ".eslintrc.json").write_text("{}")

        tools = low.select_tools("js_ts", tmp_path)
        # biome group comes first, so biome wins
        assert tools == ["biome"]
