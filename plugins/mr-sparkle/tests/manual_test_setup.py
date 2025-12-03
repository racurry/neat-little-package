#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
"""
Manual test setup for lint_on_write hook.

Creates test directories with various linter configurations to manually verify
hook behavior when Claude edits files.

Usage:
    ./manual_test_setup.py
    # or
    python manual_test_setup.py

Then have Claude edit files in plugins/mr-sparkle/.tmp/manual/ and observe
the hook feedback in system reminders.

WHY MANUAL TESTING?
Automated tests verify the hook's internal logic and output format. Manual
testing verifies the ACTUAL Claude Code integration:

- Does Claude receive the system reminder with hook feedback?
- Is the feedback useful and actionable?
- Does auto-formatting work correctly and get reported?

This is real end-to-end validation that cannot be replicated with automated
tests because it requires observing Claude's behavior in a live session.
"""

import json
import shutil
from pathlib import Path

BASE = Path(__file__).parent.parent / ".tmp" / "manual"


def main():
    """Create all manual test directories."""
    if BASE.exists():
        shutil.rmtree(BASE)
    BASE.mkdir(parents=True)

    setup_js_biome()
    setup_js_eslint_prettier()
    setup_js_no_config()
    setup_ts_biome()
    setup_markdown_config()
    setup_markdown_no_config()
    setup_python_ruff()
    setup_python_ruff_toml()
    setup_python_pylint_black()
    setup_python_traditional()
    setup_python_no_config()
    setup_shell_config()
    setup_shell_no_config()
    setup_ruby_standard()
    setup_ruby_rubocop()
    setup_ruby_no_config()

    # Warning and error cases
    setup_python_unfixable_warnings()
    setup_shell_warnings()
    setup_python_syntax_error()
    setup_js_syntax_error()
    setup_ruby_warnings()

    print(f"Created manual test directories in {BASE}")
    print("\nTest by having Claude edit files and observing hook feedback.")
    print("Each directory tests a specific configuration scenario.")


# =============================================================================
# JavaScript/TypeScript Test Cases
# =============================================================================


def setup_js_biome():
    """
    js-biome/: Project with Biome configuration.

    EXPECTED WHEN CLAUDE EDITS test.js:
    - Hook detects Biome via package.json devDependency
    - Runs: `biome check --fix test.js`
    - Claude receives: "biome test.js: OK" or error details
    - Auto-fixes: inconsistent spacing, missing semicolons

    KNOWN ISSUE:
    If the parent project has a biome.json at the root, Biome reports
    "nested root configuration" error. This is expected Biome behavior.
    """
    d = BASE / "js-biome"
    d.mkdir()

    (d / "biome.json").write_text(
        json.dumps(
            {
                "$schema": "https://biomejs.dev/schemas/1.4.0/schema.json",
                "formatter": {"enabled": True, "indentStyle": "space"},
                "linter": {"enabled": True},
            },
            indent=2,
        )
        + "\n"
    )

    (d / "package.json").write_text(json.dumps({"devDependencies": {"@biomejs/biome": "^1.4.0"}}, indent=2) + "\n")

    # Intentional issues: missing spaces around =, extra spaces in call
    (d / "test.js").write_text('const x=1\nconst y =  2\nconsole.log(  "hello"  )\n')


def setup_js_eslint_prettier():
    """
    js-eslint-prettier/: Project with ESLint + Prettier (legacy config).

    EXPECTED WHEN CLAUDE EDITS test.js:
    - Hook detects ESLint via .eslintrc.json and package.json
    - Hook detects Prettier via .prettierrc and package.json
    - Runs both: `eslint --fix` and `prettier --write`
    - Claude receives: "eslint, prettier test.js: OK" or errors
    - Prettier auto-fixes: spacing, semicolons

    KNOWN ISSUE:
    ESLint v9+ requires flat config (eslint.config.js). The legacy .eslintrc.json
    causes "ESLint couldn't find an eslint.config" errors. This test case
    intentionally uses legacy config to verify error reporting works.
    """
    d = BASE / "js-eslint-prettier"
    d.mkdir()

    (d / ".eslintrc.json").write_text(
        json.dumps(
            {"env": {"browser": True, "es2021": True}, "rules": {"no-unused-vars": "warn"}},
            indent=2,
        )
        + "\n"
    )

    (d / ".prettierrc").write_text(json.dumps({"semi": True, "singleQuote": False}, indent=2) + "\n")

    (d / "package.json").write_text(json.dumps({"devDependencies": {"eslint": "^8.0.0", "prettier": "^3.0.0"}}, indent=2) + "\n")

    (d / "test.js").write_text('const x=1\nconst y =  2\nconsole.log(  "hello"  )\n')


def setup_js_no_config():
    """
    js-no-config/: JavaScript with NO linter configuration.

    EXPECTED WHEN CLAUDE EDITS test.js:
    - No project config detected for any JS tool
    - Falls back to first group: ["biome"]
    - Runs: `biome check --fix test.js` (if biome installed)
    - Claude receives: "biome test.js: OK"
    - If biome not installed: silent skip (no feedback)

    PURPOSE:
    Verifies fallback behavior when no explicit configuration exists.
    Biome works well without config, making it a good default.
    """
    d = BASE / "js-no-config"
    d.mkdir()

    # Already well-formatted to verify OK feedback on clean files
    (d / "test.js").write_text('const x = 1;\nconst y = 2;\nconsole.log("hello");\n')


def setup_ts_biome():
    """
    ts-biome/: TypeScript file with Biome configuration.

    EXPECTED WHEN CLAUDE EDITS test.ts:
    - Hook maps .ts extension to js_ts toolset
    - Hook detects Biome via biome.json
    - Runs: `biome check --fix test.ts`
    - Claude receives: "biome test.ts: OK"

    PURPOSE:
    Verifies TypeScript files (.ts, .tsx) are handled by the js_ts toolset.
    Important because .ts is a different extension than .js but same tooling.
    """
    d = BASE / "ts-biome"
    d.mkdir()

    (d / "biome.json").write_text(
        json.dumps(
            {
                "$schema": "https://biomejs.dev/schemas/1.4.0/schema.json",
                "formatter": {"enabled": True},
                "linter": {"enabled": True},
            },
            indent=2,
        )
        + "\n"
    )

    # TypeScript with type annotation
    (d / "test.ts").write_text('const x: number = 1;\nconst y: string = "hello";\nconsole.log(x, y);\n')


# =============================================================================
# Markdown Test Cases
# =============================================================================


def setup_markdown_config():
    """
    markdown-config/: Markdown with local markdownlint configuration.

    EXPECTED WHEN CLAUDE EDITS test.md:
    - Hook detects markdownlint via .markdownlint-cli2.jsonc
    - Runs: `markdownlint-cli2 --fix test.md`
    - Claude receives: "markdownlint-cli2 test.md: OK"
    - Auto-fixes: multiple consecutive blank lines
    """
    d = BASE / "markdown-config"
    d.mkdir()

    (d / ".markdownlint-cli2.jsonc").write_text(
        json.dumps(
            {"config": {"default": True, "MD013": False}},  # Disable line length
            indent=2,
        )
        + "\n"
    )

    # Intentional issue: multiple blank lines (MD012)
    (d / "test.md").write_text("# Test\n\nSome text here\n\n\nExtra blank lines above\n")


def setup_markdown_no_config():
    """
    markdown-no-config/: Markdown with NO local configuration.

    EXPECTED WHEN CLAUDE EDITS test.md:
    - No local config detected
    - Checks for global config at ~/.markdownlint-cli2.jsonc
    - If global config EXISTS: runs with --config flag, reports OK
    - If global config MISSING: silent skip (no feedback to Claude)

    PURPOSE:
    Verifies global config fallback. Unlike other tools, markdownlint
    requires explicit config and won't run with just defaults.
    """
    d = BASE / "markdown-no-config"
    d.mkdir()

    (d / "test.md").write_text("# Test\n\nSome text here\n\n\nExtra blank lines above\n")


# =============================================================================
# Python Test Cases
# =============================================================================


def setup_python_ruff():
    """
    python-ruff/: Python project with Ruff configuration.

    EXPECTED WHEN CLAUDE EDITS test.py:
    - Hook detects Ruff via [tool.ruff] in pyproject.toml
    - Runs: `ruff check --fix` then `ruff format`
    - Claude receives: "ruff test.py: OK"
    - Auto-fixes: formatting (z=3 -> z = 3)
    """
    d = BASE / "python-ruff"
    d.mkdir()

    (d / "pyproject.toml").write_text(
        """\
[tool.ruff]
line-length = 100

[tool.ruff.format]
quote-style = "double"
"""
    )

    # Intentional issue: missing spaces around = in z=3
    (d / "test.py").write_text('x = 1\ny = 2\nz=3\nprint("hello")\n')


def setup_python_ruff_toml():
    """
    python-ruff-toml/: Python with standalone ruff.toml config file.

    EXPECTED WHEN CLAUDE EDITS test.py:
    - Hook detects Ruff via ruff.toml (config_indicators path)
    - Runs: `ruff check --fix` then `ruff format`
    - Claude receives: "ruff test.py: OK"

    PURPOSE:
    Verifies detection of standalone ruff.toml config file, as opposed to
    [tool.ruff] in pyproject.toml. Tests the config_indicators detection path.
    """
    d = BASE / "python-ruff-toml"
    d.mkdir()

    (d / "ruff.toml").write_text(
        """\
line-length = 100

[format]
quote-style = "double"
"""
    )

    # Intentional issue: missing spaces
    (d / "test.py").write_text('x = 1\ny = 2\nz=3\nprint("hello")\n')


def setup_python_pylint_black():
    """
    python-pylint-black/: Python with Pylint + Black configuration.

    EXPECTED WHEN CLAUDE EDITS test.py:
    - Hook detects Pylint via .pylintrc
    - Hook detects Black via [tool.black] in pyproject.toml
    - Runs both (if installed): `pylint` then `black`
    - Claude receives: "pylint, black test.py: OK" or lint warnings
    - Black auto-fixes formatting
    - Pylint reports unused imports as warnings (not auto-fixed)

    NOTE:
    Pylint must be installed (`pip install pylint`). If missing, only Black runs.
    """
    d = BASE / "python-pylint-black"
    d.mkdir()

    (d / ".pylintrc").write_text(
        """\
[MESSAGES CONTROL]
disable=C0114,C0115,C0116
"""
    )

    (d / "pyproject.toml").write_text(
        """\
[tool.black]
line-length = 100
"""
    )

    # Intentional issue: unused imports (sys, os)
    (d / "test.py").write_text('import sys\nimport os\n\nx = 1\ny = 2\nprint("hello")\n')


def setup_python_traditional():
    """
    python-traditional/: Python with isort + Black via setup.cfg.

    EXPECTED WHEN CLAUDE EDITS test.py:
    - Hook detects isort via [isort] section in setup.cfg
    - Hook detects Black via [tool.black] in pyproject.toml
    - Runs both: `isort` then `black`
    - Claude receives: "isort, black test.py: OK"
    - Auto-fixes: import order (os before sys), formatting (z=3 -> z = 3)

    PURPOSE:
    Verifies detection of tool config in setup.cfg INI sections,
    representing older Python project conventions.
    """
    d = BASE / "python-traditional"
    d.mkdir()

    (d / "setup.cfg").write_text(
        """\
[isort]
profile = black
line_length = 100
"""
    )

    (d / "pyproject.toml").write_text(
        """\
[tool.black]
line-length = 100
"""
    )

    # Intentional issues: imports not alphabetized, missing spaces in z=3
    (d / "test.py").write_text('import sys\nimport os\n\nx = 1\ny = 2\nz=3\nprint("hello")\n')


def setup_python_no_config():
    """
    python-no-config/: Python with NO linter configuration.

    EXPECTED WHEN CLAUDE EDITS test.py:
    - No project config detected for any Python tool
    - Falls back to first group: ["ruff"]
    - Runs: `ruff check --fix` and `ruff format`
    - Claude receives: "ruff test.py: OK"
    - If ruff not installed: silent skip

    PURPOSE:
    Verifies fallback to ruff for unconfigured Python projects.
    Ruff works excellently without config, making it ideal as default.
    """
    d = BASE / "python-no-config"
    d.mkdir()

    # Clean file to verify OK feedback
    (d / "test.py").write_text('x = 1\ny = 2\nprint("hello")\n')


# =============================================================================
# Shell Test Cases
# =============================================================================


def setup_shell_config():
    """
    shell-config/: Shell script with shfmt configuration.

    EXPECTED WHEN CLAUDE EDITS test.sh:
    - Hook detects shfmt via .editorconfig
    - shellcheck has no config (.shellcheckrc missing)
    - Runs ONLY shfmt: `shfmt -w test.sh`
    - Claude receives: "shfmt test.sh: OK"
    - Auto-fixes: indentation per .editorconfig settings

    KEY BEHAVIOR:
    Only tools WITH config in their group run. shellcheck is in the same
    group as shfmt but won't run because it lacks .shellcheckrc.
    """
    d = BASE / "shell-config"
    d.mkdir()
    (d / ".git").mkdir()  # Project root marker

    (d / ".editorconfig").write_text(
        """\
root = true

[*.sh]
indent_style = space
indent_size = 2
"""
    )

    # 2-space indentation matching .editorconfig
    (d / "test.sh").write_text('#!/bin/bash\nif [ "$1" = "test" ]; then\n  echo "hello"\n  echo "world"\nfi\n')


def setup_shell_no_config():
    """
    shell-no-config/: Shell script with NO configuration.

    EXPECTED WHEN CLAUDE EDITS test.sh:
    - No config detected for shfmt or shellcheck
    - Falls back to ENTIRE first group: ["shfmt", "shellcheck"]
    - Runs BOTH: `shfmt -w` and `shellcheck`
    - Claude receives: "shfmt, shellcheck test.sh: OK"
    - shfmt auto-fixes formatting
    - shellcheck reports any issues (no auto-fix)

    KEY BEHAVIOR:
    Unlike configured scenarios where only configured tools run, the no-config
    fallback runs ALL tools in the first group. This ensures shell scripts
    get both formatting (shfmt) and linting (shellcheck) by default.
    """
    d = BASE / "shell-no-config"
    d.mkdir()

    # 4-space indentation (shfmt will use its default)
    (d / "test.sh").write_text('#!/bin/bash\nif [ "$1" = "test" ]; then\n    echo "hello"\n    echo "world"\nfi\n')


# =============================================================================
# Ruby Test Cases
# =============================================================================


def setup_ruby_standard():
    """
    ruby-standard/: Ruby project with Standard (standardrb) configuration.

    EXPECTED WHEN CLAUDE EDITS test.rb:
    - Hook detects Standard via gem "standard" in Gemfile
    - Runs: `standardrb --fix test.rb`
    - Claude receives: "standardrb test.rb: OK"
    - Auto-fixes: spacing around operators, trailing whitespace

    PURPOSE:
    Verifies StandardRB (zero-config, opinionated) detection and auto-fix.
    Standard is the modern "just works" Ruby linter, like ruff for Python.
    """
    d = BASE / "ruby-standard"
    d.mkdir()

    (d / "Gemfile").write_text('source "https://rubygems.org"\ngem "standard"\n')

    # Intentional issues: missing spaces around =, extra spaces
    (d / "test.rb").write_text('x=1\ny =  2\nputs  "hello"\n')


def setup_ruby_rubocop():
    """
    ruby-rubocop/: Ruby project with RuboCop configuration.

    EXPECTED WHEN CLAUDE EDITS test.rb:
    - Hook detects RuboCop via .rubocop.yml config file
    - Runs: `rubocop -a test.rb` (safe auto-correct only)
    - Claude receives: "rubocop test.rb: OK"
    - Auto-fixes: spacing, style issues

    PURPOSE:
    Verifies RuboCop (configurable, traditional) detection and auto-fix.
    Uses -a flag for safe corrections only, not -A (unsafe).
    """
    d = BASE / "ruby-rubocop"
    d.mkdir()

    (d / "Gemfile").write_text('source "https://rubygems.org"\ngem "rubocop"\n')

    (d / ".rubocop.yml").write_text(
        """\
AllCops:
  TargetRubyVersion: 3.0
  NewCops: enable

Style/FrozenStringLiteralComment:
  Enabled: false
"""
    )

    # Intentional issues: missing spaces
    (d / "test.rb").write_text('x=1\ny=2\nputs "hello"\n')


def setup_ruby_no_config():
    """
    ruby-no-config/: Ruby with NO linter configuration.

    EXPECTED WHEN CLAUDE EDITS test.rb:
    - No project config detected for any Ruby tool
    - Falls back to first group: ["standard"]
    - Runs: `standardrb --fix test.rb`
    - Claude receives: "standardrb test.rb: OK"

    PURPOSE:
    Verifies fallback to StandardRB for unconfigured Ruby projects.
    Standard works without config, making it ideal as default.
    """
    d = BASE / "ruby-no-config"
    d.mkdir()

    # Clean file to verify OK feedback
    (d / "test.rb").write_text('x = 1\ny = 2\nputs "hello"\n')


# =============================================================================
# Warning Cases (unfixable lint issues)
# =============================================================================


def setup_python_unfixable_warnings():
    """
    python-unfixable-warnings/: Python with lint issues that CANNOT be auto-fixed.

    EXPECTED WHEN CLAUDE EDITS test.py:
    - Hook detects Ruff via [tool.ruff] in pyproject.toml
    - Runs: `ruff check --fix` then `ruff format`
    - Ruff finds F841 (unused variable) - NOT auto-fixable
    - Claude receives WARNING status: "ruff test.py: Lint errors!"
    - Additional context shows the actual lint error details

    PURPOSE:
    Verifies that unfixable warnings are surfaced to Claude with details,
    allowing Claude to manually address the issue or inform the user.
    """
    d = BASE / "python-unfixable-warnings"
    d.mkdir()

    (d / "pyproject.toml").write_text(
        """\
[tool.ruff]
line-length = 100
"""
    )

    # F841: Local variable 'unused_var' is assigned but never used
    # This warning cannot be auto-fixed - requires manual intervention
    (d / "test.py").write_text(
        """\
def example():
    unused_var = "this variable is never used"
    used_var = "this one is used"
    print(used_var)


example()
"""
    )


def setup_shell_warnings():
    """
    shell-warnings/: Shell script with shellcheck warnings that cannot be auto-fixed.

    EXPECTED WHEN CLAUDE EDITS test.sh:
    - No config, falls back to ["shfmt", "shellcheck"]
    - shfmt formats successfully
    - shellcheck finds SC2086 (unquoted variable) - NOT auto-fixable
    - Claude receives WARNING status: "shfmt, shellcheck test.sh: Lint errors!"
    - Additional context shows shellcheck warning details

    PURPOSE:
    Verifies shellcheck warnings are surfaced. shellcheck has no --fix flag,
    so ALL its findings are informational warnings for manual fixing.
    """
    d = BASE / "shell-warnings"
    d.mkdir()

    # SC2086: Double quote to prevent globbing and word splitting
    # shellcheck warns but cannot auto-fix
    (d / "test.sh").write_text(
        """\
#!/bin/bash
filename=$1
# SC2086: $filename should be quoted
cat $filename
"""
    )


def setup_ruby_warnings():
    """
    ruby-warnings/: Ruby file with lint issues that cannot be auto-fixed.

    EXPECTED WHEN CLAUDE EDITS test.rb:
    - Falls back to standardrb (no config)
    - StandardRB finds issues that cannot be auto-fixed
    - Claude receives WARNING status with lint details

    PURPOSE:
    Verifies Ruby lint warnings are surfaced to Claude.
    """
    d = BASE / "ruby-warnings"
    d.mkdir()

    # Lint issues: unused variable, method too long pattern
    (d / "test.rb").write_text(
        """\
def example
  unused_var = "this variable is never used"
  used_var = "this one is used"
  puts used_var
end

example
"""
    )


# =============================================================================
# Error Cases (linter-reported errors)
# =============================================================================
#
# NOTE: These test linter-reported errors (syntax errors), which produce
# WARNING status (yellow ⚠). The ERROR status (red ✗) only occurs when the
# tool itself fails to execute (timeout, crash, permission error). That path
# is defensive code for edge cases and cannot be easily triggered manually.


def setup_python_syntax_error():
    """
    python-syntax-error/: Python file with invalid syntax.

    EXPECTED WHEN CLAUDE EDITS test.py:
    - Hook runs ruff (fallback)
    - Ruff encounters syntax error, returns non-zero
    - Claude receives ERROR status with syntax error details
    - Hook reports: "ruff test.py: <syntax error message>"

    PURPOSE:
    Verifies that tool errors (not just lint warnings) are properly
    reported to Claude with actionable error messages.
    """
    d = BASE / "python-syntax-error"
    d.mkdir()

    # Invalid Python syntax - missing colon after if
    (d / "test.py").write_text(
        """\
def broken():
    if True
        print("missing colon above")
"""
    )


def setup_js_syntax_error():
    """
    js-syntax-error/: JavaScript file with invalid syntax.

    EXPECTED WHEN CLAUDE EDITS test.js:
    - Hook runs biome (fallback)
    - Biome encounters syntax error, returns non-zero
    - Claude receives ERROR status with syntax error details
    - Hook reports: "biome test.js: <syntax error message>"

    PURPOSE:
    Verifies JS/TS syntax errors are caught and reported to Claude.
    """
    d = BASE / "js-syntax-error"
    d.mkdir()

    # Invalid JS syntax - unclosed brace
    (d / "test.js").write_text(
        """\
function broken() {
    if (true) {
        console.log("missing closing brace")
    // missing }
}
"""
    )


if __name__ == "__main__":
    main()
