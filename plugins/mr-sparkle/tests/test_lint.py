"""Tests for skills/linting/scripts/lint.py universal linting CLI."""

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Import the module under test
sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "linting" / "scripts"))
import lint


# =============================================================================
# Fixtures
# =============================================================================


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
def js_project_with_biome(tmp_path):
    """Create a JS project with biome config."""
    (tmp_path / "package.json").write_text('{"devDependencies": {"@biomejs/biome": "^1.0.0"}}')
    (tmp_path / "biome.json").write_text("{}")
    (tmp_path / "index.js").write_text("const x = 1;\n")
    return tmp_path


@pytest.fixture
def markdown_project(tmp_path):
    """Create a project with markdown files."""
    (tmp_path / ".git").mkdir()
    (tmp_path / "README.md").write_text("# Title\n\nContent here.\n")
    return tmp_path


@pytest.fixture
def shell_project(tmp_path):
    """Create a project with shell scripts."""
    (tmp_path / ".git").mkdir()
    (tmp_path / "script.sh").write_text('#!/bin/bash\necho "hello"\n')
    return tmp_path


@pytest.fixture
def ruby_project_with_standard(tmp_path):
    """Create a Ruby project with standard config."""
    (tmp_path / "Gemfile").write_text('source "https://rubygems.org"\ngem "standard"\n')
    (tmp_path / "main.rb").write_text("x = 1\n")
    return tmp_path


@pytest.fixture
def ruby_project_with_rubocop(tmp_path):
    """Create a Ruby project with rubocop config."""
    (tmp_path / "Gemfile").write_text('source "https://rubygems.org"\ngem "rubocop"\n')
    (tmp_path / ".rubocop.yml").write_text("AllCops:\n  TargetRubyVersion: 3.0\n")
    (tmp_path / "main.rb").write_text("x = 1\n")
    return tmp_path


@pytest.fixture
def yaml_project_with_prettier(tmp_path):
    """Create a project with prettier config for YAML."""
    (tmp_path / ".prettierrc").write_text('{"tabWidth": 2}\n')
    (tmp_path / "config.yaml").write_text("name: test\n")
    return tmp_path


@pytest.fixture
def json_project_with_prettier(tmp_path):
    """Create a project with prettier config for JSON."""
    (tmp_path / ".prettierrc.json").write_text('{"tabWidth": 2}\n')
    (tmp_path / "data.json").write_text('{"key": "value"}\n')
    return tmp_path


# =============================================================================
# Tests: Core config detection (same as lint_on_write)
# =============================================================================


class TestFindProjectRoot:
    def test_finds_pyproject_toml(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("")
        subdir = tmp_path / "src"
        subdir.mkdir()
        file_path = subdir / "main.py"
        file_path.write_text("")

        result = lint.find_project_root(str(file_path))
        assert result == tmp_path

    def test_finds_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("{}")
        subdir = tmp_path / "src"
        subdir.mkdir()
        file_path = subdir / "index.js"
        file_path.write_text("")

        result = lint.find_project_root(str(file_path))
        assert result == tmp_path

    def test_finds_git_directory(self, tmp_path):
        (tmp_path / ".git").mkdir()
        subdir = tmp_path / "src"
        subdir.mkdir()
        file_path = subdir / "script.sh"
        file_path.write_text("")

        result = lint.find_project_root(str(file_path))
        assert result == tmp_path

    def test_finds_gemfile(self, tmp_path):
        (tmp_path / "Gemfile").write_text('source "https://rubygems.org"')
        subdir = tmp_path / "lib"
        subdir.mkdir()
        file_path = subdir / "main.rb"
        file_path.write_text("")

        result = lint.find_project_root(str(file_path))
        assert result == tmp_path


class TestSelectTools:
    def test_python_with_ruff_config(self, python_project_with_ruff):
        tools = lint.select_tools("python", python_project_with_ruff)
        assert tools == ["ruff"]

    def test_python_with_black_config(self, python_project_with_black):
        tools = lint.select_tools("python", python_project_with_black)
        assert tools == ["black"]

    def test_python_fallback_to_ruff(self, tmp_path):
        tools = lint.select_tools("python", tmp_path)
        assert tools == ["ruff"]

    def test_js_with_biome(self, js_project_with_biome):
        tools = lint.select_tools("js_ts", js_project_with_biome)
        assert tools == ["biome"]

    def test_js_fallback_to_biome(self, tmp_path):
        tools = lint.select_tools("js_ts", tmp_path)
        assert tools == ["biome"]

    def test_ruby_with_standard_config(self, ruby_project_with_standard):
        tools = lint.select_tools("ruby", ruby_project_with_standard)
        assert tools == ["standard"]

    def test_ruby_with_rubocop_config(self, ruby_project_with_rubocop):
        tools = lint.select_tools("ruby", ruby_project_with_rubocop)
        assert tools == ["rubocop"]

    def test_ruby_fallback_to_standard(self, tmp_path):
        tools = lint.select_tools("ruby", tmp_path)
        assert tools == ["standard"]

    def test_yaml_with_prettier(self, yaml_project_with_prettier):
        tools = lint.select_tools("yaml", yaml_project_with_prettier)
        assert tools == ["prettier"]

    def test_yaml_fallback_to_prettier(self, tmp_path):
        tools = lint.select_tools("yaml", tmp_path)
        assert tools == ["prettier"]

    def test_json_with_prettier(self, json_project_with_prettier):
        tools = lint.select_tools("json", json_project_with_prettier)
        assert tools == ["prettier"]

    def test_json_fallback_to_prettier(self, tmp_path):
        tools = lint.select_tools("json", tmp_path)
        assert tools == ["prettier"]


# =============================================================================
# Tests: Tool definitions
# =============================================================================


class TestToolDefinitions:
    def test_all_tools_have_commands(self):
        for name, tool in lint.TOOLS.items():
            assert "commands" in tool, f"{name} missing 'commands'"
            assert isinstance(tool["commands"], list), f"{name} commands should be list"

    def test_all_tools_have_binary(self):
        for name, tool in lint.TOOLS.items():
            assert "binary" in tool, f"{name} missing 'binary'"


# =============================================================================
# Tests: run_tool
# =============================================================================


class TestRunTool:
    def test_runs_commands_with_fix_flags(self, tmp_path):
        file_path = tmp_path / "test.py"
        file_path.write_text("x = 1\n")

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""

        with patch("shutil.which", return_value="/usr/bin/ruff"):
            with patch("subprocess.run", return_value=mock_result) as mock_run:
                lint.run_tool(str(file_path), "ruff", tmp_path)

        # Should run both ruff commands (check --fix and format)
        calls = mock_run.call_args_list
        assert len(calls) == 2
        first_cmd = calls[0][0][0]
        assert "--fix" in first_cmd

    def test_returns_none_when_binary_not_found(self, tmp_path):
        file_path = tmp_path / "test.py"
        file_path.write_text("x = 1\n")

        with patch("shutil.which", return_value=None):
            result = lint.run_tool(str(file_path), "ruff", tmp_path)

        assert result is None


# =============================================================================
# Tests: Output formatting
# =============================================================================


class TestFormatTextOutput:
    def test_empty_results_returns_empty(self):
        output, code = lint.format_text_output("/path/to/file.py", [])
        assert output == ""
        assert code == 0

    def test_success_includes_tool_and_file(self):
        results = [lint.ToolResult("ruff", lint.Status.OK)]
        output, code = lint.format_text_output("/path/to/file.py", results)
        assert "ruff" in output
        assert "file.py" in output
        assert "OK" in output
        assert code == 0

    def test_warning_returns_code_1(self):
        results = [lint.ToolResult("ruff", lint.Status.WARNING, "line 1: error")]
        output, code = lint.format_text_output("/path/to/file.py", results)
        assert "Lint errors" in output
        assert code == 1

    def test_error_returns_code_2(self):
        results = [lint.ToolResult("ruff", lint.Status.ERROR, "execution failed")]
        output, code = lint.format_text_output("/path/to/file.py", results)
        assert code == 2


class TestFormatJsonOutput:
    def test_includes_file_and_toolset(self):
        results = [lint.ToolResult("ruff", lint.Status.OK)]
        output, code = lint.format_json_output("/path/to/file.py", "python", results)
        data = json.loads(output)
        assert data["file"] == "/path/to/file.py"
        assert data["toolset"] == "python"
        assert data["tools_run"] == ["ruff"]
        assert data["status"] == "ok"
        assert code == 0

    def test_warning_status_in_json(self):
        results = [lint.ToolResult("ruff", lint.Status.WARNING, "error details")]
        output, code = lint.format_json_output("/path/to/file.py", "python", results)
        data = json.loads(output)
        assert data["status"] == "warning"
        assert data["results"][0]["output"] == "error details"
        assert code == 1

    def test_includes_all_tool_results(self):
        results = [
            lint.ToolResult("isort", lint.Status.OK),
            lint.ToolResult("black", lint.Status.OK),
        ]
        output, code = lint.format_json_output("/path/to/file.py", "python", results)
        data = json.loads(output)
        assert data["tools_run"] == ["isort", "black"]
        assert len(data["results"]) == 2


class TestFormatHookOutput:
    def test_returns_hook_compatible_json(self):
        results = [lint.ToolResult("ruff", lint.Status.OK)]
        output, code = lint.format_hook_output("/path/to/file.py", results)
        data = json.loads(output)
        assert "systemMessage" in data
        assert "ruff" in data["systemMessage"]
        assert code == 0

    def test_warning_excludes_hook_specific_output_by_default(self):
        results = [lint.ToolResult("ruff", lint.Status.WARNING, "error details")]
        output, code = lint.format_hook_output("/path/to/file.py", results)
        data = json.loads(output)
        assert "hookSpecificOutput" not in data
        assert code == 1

    def test_verbose_includes_hook_specific_output(self):
        results = [lint.ToolResult("ruff", lint.Status.WARNING, "error details")]
        output, code = lint.format_hook_output("/path/to/file.py", results, verbose=True)
        data = json.loads(output)
        assert "hookSpecificOutput" in data
        assert data["hookSpecificOutput"]["hookEventName"] == "PostToolUse"
        assert "error details" in data["hookSpecificOutput"]["additionalContext"]


# =============================================================================
# Tests: lint_file main function
# =============================================================================


class TestLintFile:
    def test_returns_empty_for_nonexistent_file(self, tmp_path):
        output, code = lint.lint_file(str(tmp_path / "nonexistent.py"))
        assert output == ""
        assert code == 0

    def test_returns_empty_for_unknown_extension(self, tmp_path):
        file_path = tmp_path / "file.unknown"
        file_path.write_text("content")
        output, code = lint.lint_file(str(file_path))
        assert output == ""
        assert code == 0

    def test_lints_python_file(self, python_project_with_ruff):
        file_path = python_project_with_ruff / "main.py"

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""

        with patch("shutil.which", return_value="/usr/bin/ruff"):
            with patch("subprocess.run", return_value=mock_result):
                output, code = lint.lint_file(str(file_path), output_format="text")

        assert "ruff" in output
        assert "OK" in output
        assert code == 0

    def test_json_format_output(self, python_project_with_ruff):
        file_path = python_project_with_ruff / "main.py"

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""

        with patch("shutil.which", return_value="/usr/bin/ruff"):
            with patch("subprocess.run", return_value=mock_result):
                output, code = lint.lint_file(str(file_path), output_format="json")

        data = json.loads(output)
        assert data["toolset"] == "python"
        assert "ruff" in data["tools_run"]

    def test_hook_format_output(self, python_project_with_ruff):
        file_path = python_project_with_ruff / "main.py"

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""

        with patch("shutil.which", return_value="/usr/bin/ruff"):
            with patch("subprocess.run", return_value=mock_result):
                output, code = lint.lint_file(str(file_path), output_format="hook")

        data = json.loads(output)
        assert "systemMessage" in data


# =============================================================================
# Tests: get_skill_default_config
# =============================================================================


class TestGetSkillDefaultConfig:
    def test_returns_none_for_unsupported_tools(self):
        assert lint.get_skill_default_config("ruff") is None
        assert lint.get_skill_default_config("biome") is None
        assert lint.get_skill_default_config("eslint") is None

    def test_returns_path_for_markdownlint_if_exists(self):
        # This tests the actual file structure - may need adjustment
        result = lint.get_skill_default_config("markdownlint")
        if result is not None:
            assert "markdown-quality" in str(result)
            assert result.name == "default-config.jsonc"

    def test_returns_path_for_prettier_if_exists(self):
        # This tests the actual file structure
        result = lint.get_skill_default_config("prettier")
        if result is not None:
            assert "prettier-quality" in str(result)
            assert result.name == "default-config.json5"


# =============================================================================
# Tests: Extension mapping
# =============================================================================


class TestExtensionMapping:
    @pytest.mark.parametrize(
        "ext,expected",
        [
            (".py", "python"),
            (".md", "markdown"),
            (".js", "js_ts"),
            (".ts", "js_ts"),
            (".tsx", "js_ts"),
            (".sh", "shell"),
            (".bash", "shell"),
            (".rb", "ruby"),
            (".rake", "ruby"),
            (".gemspec", "ruby"),
            (".yaml", "yaml"),
            (".yml", "yaml"),
            (".json", "json"),
            (".json5", "json"),
            (".jsonc", "json"),
        ],
    )
    def test_extension_maps_to_toolset(self, ext, expected):
        assert lint.EXTENSION_TO_TOOLSET.get(ext) == expected

    def test_unknown_extension_returns_none(self):
        assert lint.EXTENSION_TO_TOOLSET.get(".unknown") is None


# =============================================================================
# Tests: Gemfile gem detection
# =============================================================================


class TestHasGemfileGem:
    def test_detects_gem_with_double_quotes(self, tmp_path):
        (tmp_path / "Gemfile").write_text('gem "rubocop"')
        tool_def = {"gemfile_gems": ["rubocop"]}
        assert lint.has_gemfile_gem(tool_def, tmp_path) is True

    def test_detects_gem_with_single_quotes(self, tmp_path):
        (tmp_path / "Gemfile").write_text("gem 'standard'")
        tool_def = {"gemfile_gems": ["standard"]}
        assert lint.has_gemfile_gem(tool_def, tmp_path) is True

    def test_detects_gem_with_version(self, tmp_path):
        (tmp_path / "Gemfile").write_text('gem "rubocop", "~> 1.0"')
        tool_def = {"gemfile_gems": ["rubocop"]}
        assert lint.has_gemfile_gem(tool_def, tmp_path) is True

    def test_returns_false_when_gem_not_present(self, tmp_path):
        (tmp_path / "Gemfile").write_text('gem "rails"')
        tool_def = {"gemfile_gems": ["rubocop"]}
        assert lint.has_gemfile_gem(tool_def, tmp_path) is False

    def test_returns_false_without_gemfile(self, tmp_path):
        tool_def = {"gemfile_gems": ["rubocop"]}
        assert lint.has_gemfile_gem(tool_def, tmp_path) is False

    def test_returns_false_when_no_gemfile_gems_key(self, tmp_path):
        (tmp_path / "Gemfile").write_text('gem "rubocop"')
        tool_def = {}
        assert lint.has_gemfile_gem(tool_def, tmp_path) is False

    def test_checks_multiple_gem_names(self, tmp_path):
        (tmp_path / "Gemfile").write_text('gem "standardrb"')
        tool_def = {"gemfile_gems": ["standard", "standardrb"]}
        assert lint.has_gemfile_gem(tool_def, tmp_path) is True


# =============================================================================
# Tests: CLI argument parsing
# =============================================================================


class TestCliParsing:
    def test_help_does_not_crash(self):
        """Verify --help works without errors."""
        script_path = Path(__file__).parent.parent / "skills" / "linting" / "scripts" / "lint.py"
        result = subprocess.run(
            [sys.executable, str(script_path), "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Universal polyglot linting CLI" in result.stdout

    def test_requires_file_without_stdin_hook(self):
        """Verify error when no file provided (and not --stdin-hook)."""
        script_path = Path(__file__).parent.parent / "skills" / "linting" / "scripts" / "lint.py"
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0
        assert "required" in result.stderr.lower() or "error" in result.stderr.lower()


# =============================================================================
# Integration Tests
# =============================================================================


class TestIntegration:
    """End-to-end tests running the actual script."""

    def test_lint_python_file_with_ruff_installed(self, python_project_with_ruff):
        """Test linting a Python file (if ruff is installed)."""
        import shutil

        if not shutil.which("ruff"):
            pytest.skip("ruff not installed")

        file_path = python_project_with_ruff / "main.py"
        script_path = Path(__file__).parent.parent / "skills" / "linting" / "scripts" / "lint.py"

        result = subprocess.run(
            [sys.executable, str(script_path), str(file_path), "--format", "json"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["toolset"] == "python"
        assert "ruff" in data["tools_run"]

    def test_lint_markdown_file_with_markdownlint_installed(self, markdown_project):
        """Test linting a markdown file (if markdownlint-cli2 is installed)."""
        import shutil

        if not shutil.which("markdownlint-cli2"):
            pytest.skip("markdownlint-cli2 not installed")

        file_path = markdown_project / "README.md"
        script_path = Path(__file__).parent.parent / "skills" / "linting" / "scripts" / "lint.py"

        result = subprocess.run(
            [sys.executable, str(script_path), str(file_path), "--format", "json"],
            capture_output=True,
            text=True,
        )

        # Should succeed (markdownlint will use global or skill default config)
        data = json.loads(result.stdout)
        assert data["toolset"] == "markdown"

    def test_stdin_hook_mode(self, python_project_with_ruff):
        """Test --stdin-hook mode for hook integration."""
        import shutil

        if not shutil.which("ruff"):
            pytest.skip("ruff not installed")

        file_path = python_project_with_ruff / "main.py"
        script_path = Path(__file__).parent.parent / "skills" / "linting" / "scripts" / "lint.py"

        hook_input = json.dumps({"tool_input": {"file_path": str(file_path)}})

        result = subprocess.run(
            [sys.executable, str(script_path), "--stdin-hook"],
            input=hook_input,
            capture_output=True,
            text=True,
        )

        # Hook mode always exits 0 (non-blocking)
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "systemMessage" in data

    def test_lint_yaml_file_with_prettier_installed(self, yaml_project_with_prettier):
        """Test linting a YAML file (if prettier is installed)."""
        import shutil

        if not shutil.which("prettier"):
            pytest.skip("prettier not installed")

        file_path = yaml_project_with_prettier / "config.yaml"
        script_path = Path(__file__).parent.parent / "skills" / "linting" / "scripts" / "lint.py"

        result = subprocess.run(
            [sys.executable, str(script_path), str(file_path), "--format", "json"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["toolset"] == "yaml"
        assert "prettier" in data["tools_run"]

    def test_lint_json_file_with_prettier_installed(self, json_project_with_prettier):
        """Test linting a JSON file (if prettier is installed)."""
        import shutil

        if not shutil.which("prettier"):
            pytest.skip("prettier not installed")

        file_path = json_project_with_prettier / "data.json"
        script_path = Path(__file__).parent.parent / "skills" / "linting" / "scripts" / "lint.py"

        result = subprocess.run(
            [sys.executable, str(script_path), str(file_path), "--format", "json"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["toolset"] == "json"
        assert "prettier" in data["tools_run"]

    def test_lint_yaml_formats_file(self, tmp_path):
        """Test that prettier actually formats YAML files."""
        import shutil

        if not shutil.which("prettier"):
            pytest.skip("prettier not installed")

        # Create a project with prettier config
        (tmp_path / ".prettierrc").write_text("{}")
        file_path = tmp_path / "test.yaml"
        # Badly formatted YAML
        file_path.write_text("name:    unformatted  \nitems: [ x, y,  z ]\n")

        script_path = Path(__file__).parent.parent / "skills" / "linting" / "scripts" / "lint.py"

        result = subprocess.run(
            [sys.executable, str(script_path), str(file_path)],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        # Check file was formatted
        content = file_path.read_text()
        assert "name: unformatted" in content  # Trailing spaces removed
        assert "[x, y, z]" in content  # Array spacing normalized
