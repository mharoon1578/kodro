# Changelog

All notable changes to this project will be documented in this file.


## [2.0.3] — 2026-05-29

### ✨ Added
- **`--version` / `-V` flag** — `kodro --version` now displays the version and exits (previously crashed with unrecognized option).

### 🐛 Fixed
- **`display_error` not imported** — Added `display_error` to imports in `main.py`. The `plan`, `status`, `resume`, `rollback`, and `changes` commands would crash with `NameError` on their error paths.
- **`rollback()` targets wrong phases** — Was using `state.phases[-i]` instead of `completed[-i]`, which could revert non-completed phases when mixed-status phases existed.
- **`changes` command writes malformed CHANGES.md** — `console.print()` was embedded as literal text inside the f-string instead of being executed. Also fixed missing `## CHANGE-{date}-{NNN}` header format and auto-incrementing change number.
- **`test_calculate_cost` assertion wrong by 1000x** — Asserted `12.5` instead of `0.0125`, test always failed.
- **`display_status_table` uses wrong status key** — Used `"completed"` but actual status values are `"complete"` (without 'd') and `"rolled_back"`. Completed phases now render in green.
- **Phase header ASCII art never renders** — `PHASE_ASCII` dictionary keys (`"clarify"`, `"specify"`, etc.) didn't match `PHASE_NAMES` values (`"Clarification"`, `"Specification"`, etc.). All lookups fell through to generic fallback.
- **Removed unused imports** — `display_gatekeeper`, `git_commit`, and `VERSION` were imported in `main.py` but never used.

### 🔧 Changed
- **Removed unused dependencies** — `gitpython` and `pyyaml` removed from `pyproject.toml`; neither was used anywhere in the codebase.

## [2.0.2] — 2026-05-29
### 🐛 Fixed
- **OpenCode `/kodro` command broken** — Removed broken LLM-level command parsing (STEP 0) that tried to regex-match `/kodro` prefix from the message. OpenCode already routes the command; the user arguments were being appended to the template without the `$ARGUMENTS` placeholder. Replaced with `$ARGUMENTS` so OpenCode injects the project idea directly where the LLM can find it.
- **Bootloader replacement logic removed** — `$kodro`/`/kodro` string replacement in `main.py:init` is no longer needed since the template no longer contains those patterns.

## [2.0.1] — 2026-05-22
### 🐛 Fixed
- **Windows Encoding Errors** — Enforced UTF-8 encoding (`encoding="utf-8"`) for all file reads and writes.
- **Terminal Rendering Crashes** — Reconfigured `sys.stdout` and `sys.stderr` to use UTF-8 on startup to prevent encoding errors on non-UTF-8 command prompts and PowerShell environments.
- **Test Compatibility** — Added UTF-8 encoding support to file-reading operations in unit tests.


## [2.0.0] — 2026-05-22

### ✨ Added
- **Modular token-efficient constitution** — Kernel + Phase Modules + Framework Micro-spec (84% token reduction)
- **Gatekeeper checkpoints** — Type "Continue" to proceed after reviewing artifacts
- **Post-delivery changes workflow** — `kodro changes` command + CHANGES.md tracking
- **Next Steps display** — How to run, where files are, after delivery
- One-command `/kodro` pipeline covering all 6 SDD phases
- Formal BDD Gherkin syntax with DQI scoring (0-100, gate≥80)
- Architecture Decision Records (ADR) with rejected alternatives
- Resume and rollback state machine with atomic JSON writes
- Self-healing loop with decision tree (syntax→logic→flaky→dependency→human)
- Per-phase cost tracking for 6 major LLM models
- Smart chunking for token-efficient context management
- Parallel task markers `[P]` in task lists with dependency graphs
- Git auto-commit integration
- Rich TUI with ASCII art, tables, trees, and progress bars
- Support for 6 AI agents and 7 framework constitutions

### 🐛 Fixed
- N/A — Initial release
