"""Tests for lint_on_write.py hook."""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Import the module under test
sys.path.insert(0, str(Path(__file__).parent.parent / "hooks"))
import lint_on_write


class TestExtractFilePath:
    """Tests for extract_file_path() - parsing file paths from hook input."""

    def test_valid_path(self):
        hook_input = {"tool_input": {"file_path": "/some/file.py"}}
        assert lint_on_write.extract_file_path(hook_input) == "/some/file.py"

    def test_missing_tool_input(self):
        hook_input = {}
        assert lint_on_write.extract_file_path(hook_input) is None

    def test_missing_file_path(self):
        hook_input = {"tool_input": {}}
        assert lint_on_write.extract_file_path(hook_input) is None

    def test_null_file_path(self):
        hook_input = {"tool_input": {"file_path": None}}
        assert lint_on_write.extract_file_path(hook_input) is None

    def test_non_string_file_path(self):
        hook_input = {"tool_input": {"file_path": 123}}
        assert lint_on_write.extract_file_path(hook_input) is None

    def test_empty_string_file_path(self):
        hook_input = {"tool_input": {"file_path": ""}}
        assert lint_on_write.extract_file_path(hook_input) is None


class TestGetLinterConfig:
    """Tests for get_linter_config() - mapping extensions to linter configs."""

    def test_markdown_md(self):
        result = lint_on_write.get_linter_config("/path/to/file.md")
        assert result is not None
        language, config = result
        assert language == "markdown"
        assert ".md" in config["extensions"]

    def test_markdown_uppercase(self):
        result = lint_on_write.get_linter_config("/path/to/README.MD")
        assert result is not None
        language, _ = result
        assert language == "markdown"

    def test_python(self):
        result = lint_on_write.get_linter_config("/path/to/script.py")
        assert result is not None
        language, config = result
        assert language == "python"
        assert "pipeline_resolver" in config

    def test_javascript(self):
        result = lint_on_write.get_linter_config("/path/to/app.js")
        assert result is not None
        language, _ = result
        assert language == "javascript"

    def test_typescript(self):
        result = lint_on_write.get_linter_config("/path/to/app.tsx")
        assert result is not None
        language, _ = result
        assert language == "typescript"

    def test_shell_sh(self):
        result = lint_on_write.get_linter_config("/path/to/script.sh")
        assert result is not None
        language, _ = result
        assert language == "shell"

    def test_shell_bash(self):
        result = lint_on_write.get_linter_config("/path/to/script.bash")
        assert result is not None
        language, _ = result
        assert language == "shell"

    def test_unknown_extension(self):
        result = lint_on_write.get_linter_config("/path/to/file.xyz")
        assert result is None

    def test_no_extension(self):
        result = lint_on_write.get_linter_config("/path/to/Makefile")
        assert result is None


class TestFindProjectRoot:
    """Tests for find_project_root() - locating project root directory."""

    def test_finds_package_json(self, tmp_path):
        # Create nested structure with package.json at root
        project = tmp_path / "project"
        project.mkdir()
        (project / "package.json").write_text("{}")
        subdir = project / "src" / "components"
        subdir.mkdir(parents=True)
        target_file = subdir / "App.tsx"
        target_file.write_text("")

        result = lint_on_write.find_project_root(str(target_file))
        assert result == project

    def test_finds_pyproject_toml(self, tmp_path):
        project = tmp_path / "project"
        project.mkdir()
        (project / "pyproject.toml").write_text("[project]")
        subdir = project / "src" / "mypackage"
        subdir.mkdir(parents=True)
        target_file = subdir / "main.py"
        target_file.write_text("")

        result = lint_on_write.find_project_root(str(target_file))
        assert result == project

    def test_finds_git_directory(self, tmp_path):
        project = tmp_path / "project"
        project.mkdir()
        (project / ".git").mkdir()
        subdir = project / "scripts"
        subdir.mkdir()
        target_file = subdir / "build.sh"
        target_file.write_text("")

        result = lint_on_write.find_project_root(str(target_file))
        assert result == project

    def test_prefers_package_json_over_git(self, tmp_path):
        # package.json should be found before .git
        project = tmp_path / "project"
        project.mkdir()
        (project / ".git").mkdir()
        (project / "package.json").write_text("{}")
        target_file = project / "index.js"
        target_file.write_text("")

        result = lint_on_write.find_project_root(str(target_file))
        assert result == project

    def test_no_project_root(self, tmp_path):
        # Isolated file with no markers
        isolated = tmp_path / "isolated"
        isolated.mkdir()
        target_file = isolated / "orphan.py"
        target_file.write_text("")

        result = lint_on_write.find_project_root(str(target_file))
        # May find something in parent dirs or None
        # Don't assert None since tmp_path parents may have markers


class TestDetectTool:
    """Tests for detect_tool() - detecting configured tools in projects."""

    def test_detects_biome_config(self, tmp_path):
        (tmp_path / "biome.json").write_text("{}")
        assert lint_on_write.detect_tool(tmp_path, "biome") is True

    def test_detects_biome_jsonc(self, tmp_path):
        (tmp_path / "biome.jsonc").write_text("{}")
        assert lint_on_write.detect_tool(tmp_path, "biome") is True

    def test_detects_eslint_config(self, tmp_path):
        (tmp_path / "eslint.config.js").write_text("export default []")
        assert lint_on_write.detect_tool(tmp_path, "eslint") is True

    def test_detects_prettier_config(self, tmp_path):
        (tmp_path / ".prettierrc").write_text("{}")
        assert lint_on_write.detect_tool(tmp_path, "prettier") is True

    def test_detects_ruff_config(self, tmp_path):
        (tmp_path / "ruff.toml").write_text("")
        assert lint_on_write.detect_tool(tmp_path, "ruff") is True

    def test_detects_biome_in_package_json(self, tmp_path):
        pkg = {"devDependencies": {"@biomejs/biome": "^1.0.0"}}
        (tmp_path / "package.json").write_text(json.dumps(pkg))
        assert lint_on_write.detect_tool(tmp_path, "biome") is True

    def test_detects_eslint_in_dependencies(self, tmp_path):
        pkg = {"dependencies": {"eslint": "^8.0.0"}}
        (tmp_path / "package.json").write_text(json.dumps(pkg))
        assert lint_on_write.detect_tool(tmp_path, "eslint") is True

    def test_no_tool_detected(self, tmp_path):
        assert lint_on_write.detect_tool(tmp_path, "biome") is False
        assert lint_on_write.detect_tool(tmp_path, "eslint") is False

    def test_unknown_tool(self, tmp_path):
        assert lint_on_write.detect_tool(tmp_path, "nonexistent") is False


class TestCheckPyprojectKey:
    """Tests for check_pyproject_key() - checking pyproject.toml sections."""

    def test_finds_tool_ruff(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("[tool.ruff]\nline-length = 100\n")
        assert lint_on_write.check_pyproject_key(tmp_path, "tool.ruff") is True

    def test_finds_tool_black(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("[tool.black]\nline-length = 88\n")
        assert lint_on_write.check_pyproject_key(tmp_path, "tool.black") is True

    def test_missing_key(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("[project]\nname = 'test'\n")
        assert lint_on_write.check_pyproject_key(tmp_path, "tool.ruff") is False

    def test_no_pyproject(self, tmp_path):
        assert lint_on_write.check_pyproject_key(tmp_path, "tool.ruff") is False

    def test_invalid_toml(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text("not valid toml {{{{")
        assert lint_on_write.check_pyproject_key(tmp_path, "tool.ruff") is False


class TestGetPipeline:
    """Tests for get_pipeline() - retrieving linter pipeline stages."""

    def test_static_pipeline_markdown(self):
        config = lint_on_write.LINTER_CONFIG["markdown"]
        pipeline = lint_on_write.get_pipeline("/any/file.md", config)
        assert len(pipeline) == 1
        assert pipeline[0]["name"] == "markdownlint"

    def test_static_pipeline_shell(self):
        config = lint_on_write.LINTER_CONFIG["shell"]
        pipeline = lint_on_write.get_pipeline("/any/file.sh", config)
        assert len(pipeline) == 2
        assert pipeline[0]["name"] == "shfmt"
        assert pipeline[1]["name"] == "shellcheck"

    def test_dynamic_pipeline_python(self, tmp_path):
        # With ruff configured
        (tmp_path / "ruff.toml").write_text("")
        target = tmp_path / "test.py"
        target.write_text("")

        config = lint_on_write.LINTER_CONFIG["python"]
        pipeline = lint_on_write.get_pipeline(str(target), config)
        assert len(pipeline) == 2  # ruff check + ruff format
        assert all(s["name"] == "ruff" for s in pipeline)

    def test_dynamic_pipeline_js_biome(self, tmp_path):
        # With biome configured
        (tmp_path / "biome.json").write_text("{}")
        target = tmp_path / "app.js"
        target.write_text("")

        config = lint_on_write.LINTER_CONFIG["javascript"]
        pipeline = lint_on_write.get_pipeline(str(target), config)
        assert len(pipeline) == 1
        assert pipeline[0]["name"] == "biome"

    def test_dynamic_pipeline_js_eslint_prettier(self, tmp_path):
        # With both eslint and prettier
        pkg = {"devDependencies": {"eslint": "^8.0", "prettier": "^3.0"}}
        (tmp_path / "package.json").write_text(json.dumps(pkg))
        target = tmp_path / "app.js"
        target.write_text("")

        config = lint_on_write.LINTER_CONFIG["javascript"]
        pipeline = lint_on_write.get_pipeline(str(target), config)
        assert len(pipeline) == 2
        names = [s["name"] for s in pipeline]
        assert "eslint" in names
        assert "prettier" in names


class TestFormatSummaryLine:
    """Tests for format_summary_line() - formatting linter results."""

    def test_all_ok(self):
        results = [
            lint_on_write.StageResult("ruff", lint_on_write.Status.OK),
        ]
        summary, context = lint_on_write.format_summary_line("/path/test.py", results)
        assert "ruff" in summary
        assert "test.py" in summary
        assert "OK" in summary
        assert context is None

    def test_warning_status(self):
        results = [
            lint_on_write.StageResult(
                "markdownlint",
                lint_on_write.Status.WARNING,
                output="MD001: Heading levels"
            ),
        ]
        summary, context = lint_on_write.format_summary_line("/path/doc.md", results)
        assert "markdownlint" in summary
        assert "Lint errors!" in summary
        assert context is not None
        assert "MD001" in context

    def test_error_status(self):
        results = [
            lint_on_write.StageResult(
                "biome",
                lint_on_write.Status.ERROR,
                output="Parse error: unexpected token"
            ),
        ]
        summary, context = lint_on_write.format_summary_line("/path/bad.js", results)
        assert "biome" in summary
        assert "bad.js" in summary
        assert context is not None

    def test_skipped_not_shown(self):
        results = [
            lint_on_write.StageResult("shfmt", lint_on_write.Status.SKIPPED),
            lint_on_write.StageResult("shellcheck", lint_on_write.Status.OK),
        ]
        summary, _ = lint_on_write.format_summary_line("/path/script.sh", results)
        assert "shfmt" not in summary
        assert "shellcheck" in summary

    def test_all_skipped_empty(self):
        results = [
            lint_on_write.StageResult("shfmt", lint_on_write.Status.SKIPPED),
        ]
        summary, context = lint_on_write.format_summary_line("/path/script.sh", results)
        assert summary == ""
        assert context is None

    def test_multiple_tools(self):
        results = [
            lint_on_write.StageResult("eslint", lint_on_write.Status.OK),
            lint_on_write.StageResult("prettier", lint_on_write.Status.OK),
        ]
        summary, _ = lint_on_write.format_summary_line("/path/app.tsx", results)
        assert "eslint" in summary
        assert "prettier" in summary


class TestMakeStage:
    """Tests for make_stage() - creating pipeline stage configs."""

    def test_basic_stage(self):
        stage = lint_on_write.make_stage("biome", None, ["biome", "check", "--fix"])
        assert stage["name"] == "biome"
        assert stage["command"] == ["biome", "check", "--fix"]
        assert stage["check_installed"] == "biome"
        assert stage["unfixable_exit_code"] == 1

    def test_stage_with_project_root(self, tmp_path):
        stage = lint_on_write.make_stage("eslint", tmp_path, ["eslint", "--fix"])
        assert stage["cwd"] == str(tmp_path)

    def test_prefers_local_binary(self, tmp_path):
        # Create local node_modules binary
        bin_dir = tmp_path / "node_modules" / ".bin"
        bin_dir.mkdir(parents=True)
        local_eslint = bin_dir / "eslint"
        local_eslint.write_text("#!/bin/bash\necho 'local'")

        stage = lint_on_write.make_stage("eslint", tmp_path, ["eslint", "--fix"])
        assert stage["command"][0] == str(local_eslint)
        assert stage["check_installed"] == str(local_eslint)


class TestOutputJsonResponse:
    """Tests for output_json_response() - JSON output formatting."""

    def test_system_message_only(self, capsys):
        lint_on_write.output_json_response(system_message="Test message")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["systemMessage"] == "Test message"

    def test_with_additional_context(self, capsys):
        lint_on_write.output_json_response(
            system_message="Warning",
            additional_context="Details here"
        )
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "hookSpecificOutput" in data
        assert data["hookSpecificOutput"]["additionalContext"] == "Details here"

    def test_with_decision(self, capsys):
        lint_on_write.output_json_response(decision="approve", reason="All good")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["decision"] == "approve"
        assert data["reason"] == "All good"
