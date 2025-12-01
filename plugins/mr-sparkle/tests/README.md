# mr-sparkle Tests

## Running Tests

```bash
# From the repository root
uv run --with pytest pytest ./plugins/mr-sparkle/tests/

# With verbose output
uv run --with pytest pytest -v ./plugins/mr-sparkle/tests/

# Run a specific test file
uv run --with pytest pytest ./plugins/mr-sparkle/tests/test_lint_on_write.py

# Run a specific test function
uv run --with pytest pytest ./plugins/mr-sparkle/tests/test_lint_on_write.py::test_extract_file_path
```

## Test Organization

Tests follow the standard Python convention: **one test file per source file**.

```
hooks/
  lint_on_write.py
tests/
  test_lint_on_write.py   # all tests for lint_on_write.py
```

Within each test file, group related tests by the function they exercise:

```python
# test_lint_on_write.py

class TestExtractFilePath:
    def test_valid_path(self): ...
    def test_missing_path(self): ...

class TestGetLinterConfig:
    def test_markdown_extension(self): ...
    def test_unknown_extension(self): ...
```

This is more idiomatic than one-file-per-function because:

- Keeps related tests together for easier navigation
- Reduces file proliferation (20+ tiny files gets unwieldy)
- Matches how pytest discovery works (`test_*.py`)
- Classes provide natural grouping without extra directories
