# Mr. Sparkle Plugin Conventions

## Running Tests

We use `uv` to run tests - do NOT use `python -m pytest` directly:

Eg:

```bash
uv run --with pytest pytest ./plugins/mr-sparkle/tests/
uv run --with pytest pytest ./plugins/mr-sparkle/tests/test_lint.py
```

Group tests by function using classes:

```python
class TestFunctionName:
    def test_case_one(self): ...
    def test_case_two(self): ...
```

## Script Conventions

All Python scripts use UV inline metadata (PEP 723):

```python
#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
```
