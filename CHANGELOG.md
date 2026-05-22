# Changelog

All notable changes to this project will be documented in this file.

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
