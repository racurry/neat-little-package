"""Tests for shared plugin_config module."""

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from plugin_config import _normalize_match, _path_matches, get_plugin_config


class TestNormalizeMatch:
    """Test pattern normalization."""

    def test_tilde_expansion(self):
        result = _normalize_match("~/workspace/foo")
        assert "~" not in result
        assert result.endswith("/workspace/foo")

    def test_strips_double_star(self):
        result = _normalize_match("/some/path/**")
        assert result == "/some/path"

    def test_strips_single_star(self):
        result = _normalize_match("/some/path/*")
        assert result == "/some/path"

    def test_strips_trailing_slash(self):
        result = _normalize_match("/some/path/")
        assert result == "/some/path"

    def test_no_glob_unchanged(self):
        result = _normalize_match("/some/path")
        assert result == "/some/path"


class TestPathMatches:
    """Test directory matching against patterns."""

    def test_exact_match(self):
        assert _path_matches("/workspace/project", "/workspace/project")

    def test_subdirectory_matches(self):
        assert _path_matches("/workspace/project/src/deep", "/workspace/project")

    def test_double_star_pattern(self):
        assert _path_matches("/workspace/project/src", "/workspace/project/**")

    def test_no_match_different_directory(self):
        assert not _path_matches("/workspace/other", "/workspace/project")

    def test_no_partial_name_match(self):
        """project-v2 should NOT match a pattern for project."""
        assert not _path_matches("/workspace/project-v2", "/workspace/project")

    def test_tilde_pattern(self):
        home = str(Path.home())
        cwd = home + "/workspace/test"
        assert _path_matches(cwd, "~/workspace/test")

    def test_tilde_pattern_subdirectory(self):
        home = str(Path.home())
        cwd = home + "/workspace/test/src"
        assert _path_matches(cwd, "~/workspace/test")

    def test_trailing_slash_pattern(self):
        assert _path_matches("/workspace/project/src", "/workspace/project/")


class TestGetPluginConfig:
    """Test full config reading with overrides."""

    def test_missing_config_returns_empty_dict(self, tmp_path, monkeypatch):
        monkeypatch.setattr("plugin_config.CONFIG_DIR", tmp_path / "nonexistent")
        result = get_plugin_config("mr-sparkle", "/some/path")
        assert result == {}

    def test_reads_top_level_values(self, tmp_path, monkeypatch):
        monkeypatch.setattr("plugin_config.CONFIG_DIR", tmp_path)
        (tmp_path / "mr-sparkle.toml").write_text("lint_on_write = false\nblock_direct_markdownlint = true\n")
        result = get_plugin_config("mr-sparkle", "/some/path")
        assert result["lint_on_write"] is False
        assert result["block_direct_markdownlint"] is True

    def test_override_applies_for_matching_directory(self, tmp_path, monkeypatch):
        monkeypatch.setattr("plugin_config.CONFIG_DIR", tmp_path)
        (tmp_path / "test-plugin.toml").write_text(f'feature = true\n\n[[overrides]]\nmatch = "{tmp_path}/project"\nfeature = false\n')
        result = get_plugin_config("test-plugin", str(tmp_path / "project"))
        assert result["feature"] is False

    def test_override_applies_for_subdirectory(self, tmp_path, monkeypatch):
        monkeypatch.setattr("plugin_config.CONFIG_DIR", tmp_path)
        (tmp_path / "test-plugin.toml").write_text(f'feature = true\n\n[[overrides]]\nmatch = "{tmp_path}/project"\nfeature = false\n')
        result = get_plugin_config("test-plugin", str(tmp_path / "project" / "src"))
        assert result["feature"] is False

    def test_override_does_not_apply_for_non_matching(self, tmp_path, monkeypatch):
        monkeypatch.setattr("plugin_config.CONFIG_DIR", tmp_path)
        (tmp_path / "test-plugin.toml").write_text(f'feature = true\n\n[[overrides]]\nmatch = "{tmp_path}/other"\nfeature = false\n')
        result = get_plugin_config("test-plugin", str(tmp_path / "project"))
        assert result["feature"] is True

    def test_last_matching_override_wins(self, tmp_path, monkeypatch):
        monkeypatch.setattr("plugin_config.CONFIG_DIR", tmp_path)
        (tmp_path / "test-plugin.toml").write_text(
            "feature = true\n"
            "\n"
            "[[overrides]]\n"
            f'match = "{tmp_path}/workspace"\n'
            "feature = false\n"
            "\n"
            "[[overrides]]\n"
            f'match = "{tmp_path}/workspace/special"\n'
            "feature = true\n"
        )
        # More specific override re-enables
        result = get_plugin_config("test-plugin", str(tmp_path / "workspace" / "special"))
        assert result["feature"] is True

    def test_malformed_toml_returns_empty_dict(self, tmp_path, monkeypatch):
        monkeypatch.setattr("plugin_config.CONFIG_DIR", tmp_path)
        (tmp_path / "bad.toml").write_text("this is not valid toml [[[")
        result = get_plugin_config("bad", "/some/path")
        assert result == {}

    def test_caller_defaults_with_get(self, tmp_path, monkeypatch):
        """Callers use .get(key, True) so missing keys default to enabled."""
        monkeypatch.setattr("plugin_config.CONFIG_DIR", tmp_path / "nonexistent")
        result = get_plugin_config("mr-sparkle", "/some/path")
        assert result.get("lint_on_write", True) is True
        assert result.get("block_direct_markdownlint", True) is True

    def test_override_only_affects_specified_keys(self, tmp_path, monkeypatch):
        monkeypatch.setattr("plugin_config.CONFIG_DIR", tmp_path)
        (tmp_path / "test-plugin.toml").write_text(
            f'feature_a = true\nfeature_b = true\n\n[[overrides]]\nmatch = "{tmp_path}/project"\nfeature_a = false\n'
        )
        result = get_plugin_config("test-plugin", str(tmp_path / "project"))
        assert result["feature_a"] is False
        assert result["feature_b"] is True

    def test_different_plugins_read_different_files(self, tmp_path, monkeypatch):
        monkeypatch.setattr("plugin_config.CONFIG_DIR", tmp_path)
        (tmp_path / "alpha.toml").write_text("x = 1\n")
        (tmp_path / "beta.toml").write_text("x = 2\n")
        assert get_plugin_config("alpha", "/any")["x"] == 1
        assert get_plugin_config("beta", "/any")["x"] == 2
