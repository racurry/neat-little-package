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

    def test_blocks_nested_subshell(self):
        """A loop with $() hits the substitution check first."""
        assert_blocked('for dir in plugins/*/; do echo "$(basename $dir)"; done', "substitution")


class TestBracedExpansion:
    """${...} reports as "Contains expansion" and only offers Allow-once. See hook header
    (verified 2026-06-20, apples-to-apples: `cat ${HOME}/x` prompts, `cat $HOME/x` does not)."""

    def test_blocks_dollar_brace(self):
        assert_blocked('cat "${HOME}/.config/foo"', "expansion")

    def test_blocks_brace_operator(self):
        assert_blocked('echo "${VAR:-default}"', "expansion")

    def test_allows_bare_var(self):
        """Bare $var runs clean — only braces trigger the expansion prompt."""
        assert_allowed('cat "$HOME/.config/foo"')


class TestLoops:
    """for/while/until loops always prompt (reported as simple_expansion). See hook header."""

    def test_blocks_for_loop(self):
        assert_blocked('for f in a b; do echo "$f"; done', "loop")

    def test_blocks_for_glob(self):
        assert_blocked('for d in plugins/*/; do echo "$d"; done', "loop")

    def test_blocks_while_loop(self):
        assert_blocked('while read -r l; do echo "$l"; done < file', "loop")

    def test_blocks_loop_after_and(self):
        assert_blocked('cd /tmp && for f in a; do echo "$f"; done', "loop")

    def test_blocks_loop_no_space_before_do(self):
        assert_blocked('for f in a;do echo "$f";done', "loop")

    def test_allows_bare_var_outside_loop(self):
        """Bare $var in a single command runs clean — only the loop construct prompts."""
        assert_allowed('echo "home is $HOME"')

    def test_allows_for_word_in_string(self):
        """`for` and `; do` inside a quoted arg, not at statement position — not a loop."""
        assert_allowed('git commit -m "refactor for loop; do it later"')


class TestPassthrough:
    def test_allows_safe_command(self):
        assert_allowed("git status")

    def test_allows_pipes(self):
        assert_allowed("git log --oneline | head -5")

    def test_allows_pipe(self):
        assert_allowed("cmd1 | cmd2")

    def test_allows_flags(self):
        """Actual --flags should not be blocked."""
        assert_allowed("git diff --staged --stat")

    def test_allows_grep_with_angle_bracket_in_quotes(self):
        assert_allowed("grep '>' file.txt")

    def test_allows_redirection(self):
        """Output redirection no longer triggers a prompt — not blocked."""
        assert_allowed("echo hello > output.txt")

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
