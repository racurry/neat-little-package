# shellcheck Reference

Common shellcheck error codes with examples and fixes.

## Overview

shellcheck is a static analysis tool for shell scripts. It catches common mistakes, portability issues, and style problems.

**Official wiki:** <https://www.shellcheck.net/wiki/>

## Error Code Categories

- **SC1xxx** - Syntax errors (parsing failures)
- **SC2xxx** - Semantic errors (logic, common mistakes)
- **SC3xxx** - Portability warnings (bash-isms in POSIX)

## Most Common Error Codes

### SC2086: Quote Variables to Prevent Word Splitting

**What it means:** Unquoted variable expansion can split on whitespace or glob filenames.

**Problem:**

```bash
file="my document.txt"
cat $file  # Expands to: cat my document.txt (two arguments)
```

**Fix:**

```bash
file="my document.txt"
cat "$file"  # Expands to: cat "my document.txt" (one argument)
```

**When to ignore:** Intentional word splitting (rare):

```bash
# shellcheck disable=SC2086
options="-v -x"
mycommand $options  # Want word splitting here
```

**Better alternative:**

```bash
options=(-v -x)
mycommand "${options[@]}"
```

### SC2034: Variable Appears Unused

**What it means:** Variable assigned but never read in this script.

**Problem:**

```bash
#!/bin/bash
username="admin"  # SC2034: unused
password="secret"
echo "$password"
```

**Fixes:**

1. Remove unused variable
2. Use the variable
3. Export if meant for subprocesses
4. Disable if used by sourcing script

```bash
# Exported for child processes
# shellcheck disable=SC2034
export CONFIG_PATH="/etc/app"
```

### SC2154: Variable Referenced But Not Assigned

**What it means:** Using variable that was never set in this script.

**Problem:**

```bash
#!/bin/bash
echo "Home: $USER_HOME"  # SC2154: USER_HOME not assigned
```

**Fixes:**

1. Assign the variable before use
2. Use existing variable: `$HOME` instead
3. Disable if from environment or sourced file

```bash
# Provided by parent script via source
# shellcheck disable=SC2154
echo "Data dir: $APP_DATA_DIR"
```

### SC2068: Quote Array Expansions

**What it means:** Use `"$@"` not `$@` to prevent word splitting of arguments.

**Problem:**

```bash
#!/bin/bash
function wrapper() {
  command $@  # SC2068: Quote to prevent splitting
}

wrapper "arg with spaces"  # Will split incorrectly
```

**Fix:**

```bash
function wrapper() {
  command "$@"  # Preserves argument boundaries
}

wrapper "arg with spaces"  # Passed as single argument
```

### SC2046: Quote Command Substitution

**What it means:** Unquoted `$(...)` can word-split and glob.

**Problem:**

```bash
# If find returns "a b.txt", rm sees two arguments
rm $(find . -name "*.tmp")  # SC2046
```

**Fix:**

```bash
# Better: quote it
rm "$(find . -name "*.tmp")"

# Best: use while loop for multiple files
find . -name "*.tmp" -print0 | while IFS= read -r -d '' file; do
  rm "$file"
done
```

### SC1091: File Not Found (Source/Dot)

**What it means:** shellcheck can't find or follow sourced file.

**Problem:**

```bash
source /etc/myapp/config.sh  # SC1091: Not following
```

**Fixes:**

1. Make file available to shellcheck
2. Tell shellcheck where it is
3. Disable if file is external/runtime-only

```bash
# Tell shellcheck where to find it
# shellcheck source=/etc/myapp/config.sh
source /etc/myapp/config.sh

# Or disable if truly external
# shellcheck source=/dev/null
source "${RUNTIME_CONFIG}"
```

### SC2164: Use `cd ... || exit` in Case cd Fails

**What it means:** cd can fail; handle the error.

**Problem:**

```bash
cd /important/directory  # SC2164
rm -rf ./*  # Dangerous if cd failed!
```

**Fix:**

```bash
cd /important/directory || exit 1
rm -rf ./*  # Safe: only runs if cd succeeded

# Or:
cd /important/directory || { echo "Failed to cd"; exit 1; }
```

### SC2155: Declare and Assign Separately

**What it means:** `local var=$(cmd)` masks command's exit code.

**Problem:**

```bash
function test() {
  local result=$(failing_command)  # SC2155
  # $? is exit code of 'local', not failing_command
}
```

**Fix:**

```bash
function test() {
  local result
  result=$(failing_command)
  # Now $? is exit code of failing_command
}
```

### SC2166: Prefer `[ p ] && [ q ]` over `[ p -a q ]`

**What it means:** `-a` and `-o` are deprecated, use separate brackets.

**Problem:**

```bash
if [ -f file -a -r file ]; then  # SC2166
  echo "exists and readable"
fi
```

**Fix:**

```bash
if [ -f file ] && [ -r file ]; then
  echo "exists and readable"
fi

# Or use [[  ]] (bash-specific)
if [[ -f file && -r file ]]; then
  echo "exists and readable"
fi
```

### SC2181: Check Exit Code Directly

**What it means:** Don't compare `$?`, test command directly.

**Problem:**

```bash
command
if [ $? -eq 0 ]; then  # SC2181
  echo "success"
fi
```

**Fix:**

```bash
if command; then
  echo "success"
fi

# If you need output AND status:
output=$(command)
if [ $? -eq 0 ]; then  # OK here - no alternative
  echo "$output"
fi
```

### SC2162: read Without -r Mangles Backslashes

**What it means:** Use `read -r` to preserve backslashes.

**Problem:**

```bash
while read line; do  # SC2162
  echo "$line"
done < file.txt
```

**Fix:**

```bash
while IFS= read -r line; do
  echo "$line"
done < file.txt
```

## Portability Warnings (SC3xxx)

These warn about bash-isms when targeting POSIX sh.

### SC3010: `[[ ]]` Is Not POSIX

**Problem:**

```bash
#!/bin/sh
if [[ $var == "test" ]]; then  # SC3010: [[ ]] is bash-specific
  echo "match"
fi
```

**Fix for POSIX:**

```bash
#!/bin/sh
if [ "$var" = "test" ]; then
  echo "match"
fi
```

**Or use bash:**

```bash
#!/bin/bash
if [[ $var == "test" ]]; then
  echo "match"
fi
```

### SC3043: `local` Is Not POSIX

**Problem:**

```bash
#!/bin/sh
function test() {
  local var="value"  # SC3043: local is not POSIX
}
```

**Fix:** Either use bash or avoid local:

```bash
#!/bin/bash
# Now local is OK
```

## Disabling Warnings

### Inline Disable (Single Line)

```bash
# shellcheck disable=SC2086
command $variable
```

### Disable Multiple Codes

```bash
# shellcheck disable=SC2086,SC2046
command $(find . -name "$pattern")
```

### Disable for Function/Block

```bash
# shellcheck disable=SC2086
function legacy_wrapper() {
  # SC2086 disabled for entire function
  command $unquoted_var
  other_command $another_var
}
```

### Disable in Configuration

```bash
# .shellcheckrc
disable=SC1091,SC2034
```

**Use sparingly:** Disabling should be rare and documented.

## Configuration File

**.shellcheckrc in project root:**

```bash
# Disable specific warnings globally
disable=SC1091

# Set default shell
shell=bash

# Enable optional checks
enable=all
```

**Available options:**

- `disable=SC1234,SC5678` - Disable specific codes
- `enable=all` - Enable optional checks
- `shell=bash|sh|dash|ksh` - Default shell to assume
- `source-path=SCRIPTDIR` - Where to find sourced files

## Best Practices

**Fixing priority:**

1. **SC1xxx** (syntax errors) - Fix immediately
2. **SC2xxx** (semantic issues) - Fix most; disable carefully
3. **SC3xxx** (portability) - Fix if targeting POSIX; ignore if bash-only

**Quoting rules:**

- Always quote: `"$variable"`, `"$@"`, `"$(command)"`
- Exception: Arrays use `"${array[@]}"`
- Exception: Intentional word splitting (rare, document it)

**Array usage:**

```bash
# Instead of string with spaces
files="file1.txt file2.txt"
command $files  # Will trigger SC2086

# Use array
files=(file1.txt file2.txt)
command "${files[@]}"  # No warning, correct
```

**Testing:**

```bash
# Check syntax
bash -n script.sh

# Run shellcheck
shellcheck script.sh

# Test with set -u (error on unset variables)
bash -u script.sh
```

## Integration

**Editor integration:**

- VSCode: ShellCheck extension
- Vim: ALE, Syntastic
- Emacs: flycheck-shellcheck

**CI/CD:**

```bash
# Fail build on shellcheck errors
shellcheck **/*.sh
```

**Pre-commit hook:**

```bash
# .git/hooks/pre-commit
shellcheck $(git diff --cached --name-only --diff-filter=ACM | grep '\.sh$')
```

## Further Reading

- Wiki with all codes: <https://www.shellcheck.net/wiki/>
- GitHub issues: <https://github.com/koalaman/shellcheck/issues>
- Online tool: <https://www.shellcheck.net/>
