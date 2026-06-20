---
name: chezmoi
description: Idioms and gotchas for managing dotfiles with chezmoi — source-state naming/attributes, when to use templates vs modify_ scripts vs run_ scripts, package installation, externals, secrets, and machine differences. Use when adding, editing, or structuring chezmoi-managed dotfiles, or writing chezmoi templates/scripts.
---

# Chezmoi

Corrections for working with chezmoi. Claude knows chezmoi exists but consistently guesses wrong on naming attributes, when to template vs script, and how packages are installed. This is the knowledge delta — verify anything not here against the official docs (each section links the canonical page).

## The One Rule: Never Edit the Target

Source state (the repo, `chezmoi source-path`) is the authority. The destination (`~`) is generated. **Editing `~/.zshrc` directly is wrong** — `chezmoi apply` regenerates it from source and your edit is gone.

- Start managing a file: `chezmoi add ~/.zshrc` (captures it into source with the right attributes — don't hand-create `dot_zshrc`).
- Change a managed file: `chezmoi edit ~/.zshrc` (opens the *source*; add `--apply` to apply on save).
- Pull a manual edit back into source: `chezmoi re-add ~/.zshrc` (preserves templates/encryption; `add --force` overwrites unconditionally).
- Preview / deploy: `chezmoi diff` then `chezmoi apply`.
- Commit: `chezmoi git -- commit -am "…"` or work in `chezmoi cd`. **Committing doesn't apply, and applying doesn't commit** — they're separate.
- `chezmoi update` = `git pull` in the source dir **then** `apply`. `chezmoi apply` alone never pulls.

Concepts: <https://www.chezmoi.io/reference/concepts/> · Daily ops: <https://www.chezmoi.io/user-guide/daily-operations/>

## Source Naming: Attributes Are Prefixes, in a Fixed Order

Attributes are filename prefixes ending in `_`. **Order is mandatory.** For regular files:

```
encrypted_  private_  readonly_  empty_  executable_  dot_
```

`dot_` is **always last** (closest to the name). So `private_dot_ssh`, `executable_dot_bashrc`, `encrypted_private_dot_netrc` — never `dot_private_…`. Directories use a different set/order: `remove_ external_ exact_ private_ readonly_ dot_`. The `.tmpl` suffix goes at the very end; `.literal` stops attribute parsing (use it when a real filename contains `_` that looks like an attribute).

| Prefix                   | Effect on the *target*                                                                                      |
| ------------------------ | ----------------------------------------------------------------------------------------------------------- |
| `dot_`                   | leading `.` (`dot_zshrc` → `.zshrc`) — naming only, not content                                             |
| `private_` / `readonly_` | strips group/world perms / removes write bit                                                                |
| `empty_`                 | keep a zero-length file (git would otherwise drop it)                                                       |
| `executable_`            | sets the execute bit                                                                                        |
| `encrypted_`             | file is stored encrypted in the repo (age/gpg)                                                              |
| `exact_` (dirs)          | **destructive**: deletes any file in that dir not in source — only for dirs you fully own, never `.config/` |
| `create_`                | create if absent, then leave alone (vs a normal file, which is re-enforced every apply)                     |
| `remove_`                | deletes the target on apply                                                                                 |
| `symlink_`               | target is a symlink; empty content deletes it                                                               |

Authoritative table (don't guess the order — check it): <https://www.chezmoi.io/reference/source-state-attributes/> · Target types: <https://www.chezmoi.io/reference/target-types/>

## Templates: When and How

A file is a template if it ends in `.tmpl` (or lives in `.chezmoitemplates/`). Go `text/template` + chezmoi/sprig functions.

- **Use a template** when the *whole file* varies by machine/OS/secret. **Don't** template a file you only partially own (app-managed config) — use a `modify_` script instead.
- **`modify_` files** are scripts that receive the current file on stdin and emit the new contents on stdout (a `.tmpl` suffix renders the script before it runs, like any other script). Simpler alternative: put a `chezmoi:modify-template` marker line in the file — chezmoi strips those lines and treats the rest as a template with the current contents in `.chezmoi.stdin`, whose output becomes the new file (no separate script needed).
- **Data precedence** (later wins): built-in `.chezmoi.*` < `.chezmoidata.<fmt>` files < `[data]` in the config. `.chezmoidata` files are **not** themselves templates (read before the engine runs). See everything with `chezmoi data`.
- **Test without applying**: `chezmoi execute-template '{{ .chezmoi.os }}'` or pipe a file in. Add `--init` to test config/init-only functions like `promptStringOnce`.
- **Secrets** come from password-manager functions (`onepasswordRead`, `bitwardenFields`, …) evaluated at apply time — see Secrets below.
- **`.chezmoitemplates/` gotcha**: `{{ template "name" }}` passes *no* data; the partial can't see `.chezmoi.*`. Pass context explicitly: `{{ template "name" . }}`.
- Strict mode is on (`missingkey=error`) — a typo'd variable errors rather than rendering empty. Emit literal braces with `{{ "{{" }}`.

Templating guide: <https://www.chezmoi.io/user-guide/templating/> · Functions: <https://www.chezmoi.io/reference/templates/functions/> · Partial-file management: <https://www.chezmoi.io/user-guide/manage-different-types-of-file/>

## Scripts: For Actions, Not File Contents

Scripts are source files prefixed `run_`. They **run on every `chezmoi apply`** unless you scope them. Use them to *do things* (install packages, system setup) — **never to generate config files** (that's what target files/templates are for).

- `run_once_` — runs once per unique *content hash*; editing the script re-runs it.
- `run_onchange_` — re-runs whenever the *content* changes.
- Both hash **after** template rendering, so a `.tmpl` script re-runs when its rendered output changes.
- Order: scripts interleave with files in ASCII order; `before_`/`after_` break out of it. Combine as `run_once_before_`, `run_onchange_after_`, etc.
- Put scripts with no corresponding target in `.chezmoiscripts/`.
- Write them idempotent regardless — they may run during diffs or after state resets.

Scripts guide: <https://www.chezmoi.io/user-guide/use-scripts-to-perform-actions/>

## Packages vs Externals: Two Different Mechanisms

These get conflated. chezmoi has **no built-in package manager**.

- **Install system packages** (brew/apt/dnf): a templated `run_onchange_` script that ranges over a package list in `.chezmoidata/packages.yaml`. Because the list is inlined into the rendered script, adding a package changes the script body and `run_onchange_` re-fires — **no manual hash needed**.

  ```yaml
  # .chezmoidata/packages.yaml
  packages: { darwin: { brews: [git, ripgrep, fzf] } }
  ```

  ```bash
  # run_onchange_install-packages.sh.tmpl
  {{ if eq .chezmoi.os "darwin" -}}
  #!/bin/bash
  brew install {{ .packages.darwin.brews | join " " }}
  {{ end -}}
  ```

  The manual `# {{ include "file" | sha256sum }}` comment trick is only for when a script reads an external file **at runtime** rather than inlining it.

- **Vendor external files/archives/repos** (oh-my-zsh, vim plugins, a binary): declare them in `.chezmoiexternal.toml`. Types: `file`, `archive`, `archive-file`, `git-repo`. Set `refreshPeriod` (default never re-downloads); `chezmoi apply -R` forces a refresh. URLs can be templated for per-OS/arch downloads.

Install packages: <https://www.chezmoi.io/user-guide/advanced/install-packages-declaratively/> · Externals: <https://www.chezmoi.io/reference/special-files/chezmoiexternal-format/>

## Secrets

Never commit plaintext. Two complementary approaches:

- **Password-manager functions** (idiomatic, zero secrets in repo): templates call `onepasswordRead`, `bitwardenFields`, etc., fetching at apply time. The repo holds only the reference.
- **Encryption at rest**: `encrypted_` prefix (age or gpg) stores ciphertext in the repo; `chezmoi edit` transparently decrypts/re-encrypts. Don't hand-decrypt source files.

Be careful enabling `autoCommit`/`autoPush` — a stray plaintext secret becomes permanent public history.

Password managers: <https://www.chezmoi.io/user-guide/password-managers/> · Encryption: <https://www.chezmoi.io/user-guide/encryption/>

## Machine Differences

One repo, one branch — chezmoi enforces a single source of truth by design (no multi-repo/branch dotfiles). Vary by machine with templates, not branches:

- Built-ins: `.chezmoi.os`, `.chezmoi.arch`, `.chezmoi.hostname`, `.chezmoi.config`.
- **`.chezmoiignore` is itself a template** — use conditionals to include/exclude files per machine.
- Per-machine values belong in `.chezmoidata/` or are prompted once at init (`promptStringOnce`) into the generated config.
- Scope is the home directory; chezmoi is not for `/etc` (use Ansible/etc. for that).

Machine differences: <https://www.chezmoi.io/user-guide/manage-machine-to-machine-differences/>

## Debugging

- `chezmoi doctor` — health/config check first.
- `chezmoi diff` / `chezmoi apply --dry-run --verbose` — see what would change.
- `chezmoi cat ~/.zshrc` — show the rendered target.
- `chezmoi execute-template …` — test template logic in isolation.
- `chezmoi managed` / `unmanaged` / `status` / `verify` — audit what's tracked and whether it matches.
- Force a script to re-run: `chezmoi state delete-bucket --bucket=scriptState`.

FAQ: <https://www.chezmoi.io/user-guide/frequently-asked-questions/> · execute-template: <https://www.chezmoi.io/reference/commands/execute-template/>

Bootstrapping a new machine (`chezmoi init --apply`): <https://www.chezmoi.io/user-guide/setup/>
