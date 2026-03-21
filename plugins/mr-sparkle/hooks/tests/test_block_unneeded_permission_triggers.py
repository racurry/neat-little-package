"""Tests for block_unneeded_permission_triggers hook."""

import json
import subprocess

HOOK = "plugins/mr-sparkle/hooks/block_unneeded_permission_triggers.sh"


def run_hook(command: str) -> tuple[int, str, str]:
    """Run the hook with a simulated Bash tool input, return (exit_code, stdout, stderr)."""
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
    result = subprocess.run(
        ["bash", HOOK],
        input=payload,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def assert_blocked(command: str, reason_fragment: str = ""):
    """Assert a command is blocked (exit 2, reason on stderr)."""
    code, _, stderr = run_hook(command)
    assert code == 2, f"Expected exit 2 (block), got {code}"
    if reason_fragment:
        assert reason_fragment in stderr, f"Expected '{reason_fragment}' in: {stderr}"


def assert_allowed(command: str):
    """Assert a command is allowed (exit 0, no output)."""
    code, stdout, stderr = run_hook(command)
    assert code == 0, f"Expected exit 0, got {code}. stderr: {stderr}"
    assert stdout == "", f"Expected no stdout, got: {stdout}"


class TestCommandSubstitution:
    def test_blocks_dollar_paren(self):
        assert_blocked("gh run view 123 --job $(gh run view 123 --json jobs)", "substitution")

    def test_blocks_backticks(self):
        assert_blocked("echo `whoami`", "backtick")

    def test_allows_dollar_brace(self):
        """${VAR} is not command substitution — should be allowed."""
        assert_allowed('echo "${HOME}/foo"')

    def test_blocks_nested_subshell(self):
        assert_blocked('for dir in plugins/*/; do echo "$(basename $dir)"; done', "substitution")


class TestDashStrings:
    def test_blocks_echo_triple_dash(self):
        assert_blocked('echo "---UNSTAGED---"', "---")

    def test_blocks_echo_single_quote_dashes(self):
        assert_blocked("echo '---STAGED---'", "---")

    def test_allows_echo_normal_string(self):
        assert_allowed('echo "hello world"')

    def test_allows_flags(self):
        """Actual --flags should not be blocked."""
        assert_allowed("git diff --staged --stat")


class TestOutputRedirection:
    def test_blocks_stderr_to_stdout(self):
        assert_blocked("some_cmd 2>&1", "redirection")

    def test_blocks_stderr_to_devnull(self):
        assert_blocked("some_cmd 2>/dev/null", "redirection")

    def test_blocks_stdout_redirect(self):
        assert_blocked("echo hello > output.txt", "redirection")

    def test_allows_grep_with_angle_bracket_in_quotes(self):
        """grep '>' pattern should not be blocked."""
        assert_allowed("grep '>' file.txt")

    def test_allows_pipe(self):
        assert_allowed("cmd1 | cmd2")


class TestPassthrough:
    def test_allows_safe_command(self):
        assert_allowed("git status")

    def test_allows_pipes(self):
        assert_allowed("git log --oneline | head -5")

    def test_ignores_non_bash(self):
        payload = json.dumps({"tool_name": "Read", "tool_input": {"path": "foo.txt"}})
        result = subprocess.run(
            ["bash", HOOK],
            input=payload,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == ""
