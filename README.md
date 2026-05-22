<!-- 

```
    ██╗  ██╗ ██████╗ ██████╗ ██████╗  ██████╗ 
    ██║ ██╔╝██╔═══██╗██╔══██╗██╔══██╗██╔═══██╗
    █████╔╝ ██║   ██║██║  ██║██████╔╝██║   ██║
    ██╔═██╗ ██║   ██║██║  ██║██╔══██╗██║   ██║
    ██║  ██╗╚██████╔╝██████╔╝██║  ██║╚██████╔╝
    ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ 
```

**One-Command Spec-Driven Development Engine** -->

<p align="center">
  <a href="https://github.com/mharoon1578/kodro">
    <picture>
      <source srcset="assets/kodro_bg.png">
      <img src="assets/kodro_bg.png" alt="Kodro logo">
    </picture>
  </a>
</p>

<p align="center">
<a href="https://www.python.org">
    <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python">
</a>
<a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
</a>
<a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
</a>
<a href="https://github.com/mharoon1578/kodro">
    <img src="https://img.shields.io/badge/status-beta-orange.svg" alt="Status">
</a>
<a href="#">
    <img src="https://img.shields.io/badge/Love%20You-red" alt="Message">
</a>

</p>




> [!NOTE]
> **Beta Software:** Kodro v2.0.0 is in active development. You may encounter bugs, incomplete 
>features, or breaking changes. Please report issues at [GitHub Issues](https://github.com/mharoon1578/kodro/issues).

---

## What Kodro Does

Kodro transforms a single natural language prompt into production software through a **6-phase Spec-Driven Development (SDD) pipeline**. Unlike other tools that require 7+ separate commands, Kodro collapses everything into one `/kodro` command.

**The pipeline:**

```
Your Idea → /kodro → P1 Clarify → P2 Specify → [GATEKEEPER] → P3 Plan → [GATEKEEPER]
→ P4 Implement → P5 Validate → P6 Deliver → Next Steps
```

At each **gatekeeper**, the AI agent pauses so you can review generated files. **Type "Continue"** to proceed. No code is written until Phase 4 — the agent first clarifies your intent, writes a formal specification, and plans tasks.

---

## Quick Start

```bash
# Install Kodro
pip install kodro

# Initialize a project
mkdir my-project && cd my-project
kodro init --integration opencode --framework react-typescript

# In your AI agent (OpenCode, Claude, Cursor, etc.):
/kodro "Build a weather dashboard with React"
```
The agent will:

1. Ask 3-5 clarifying questions (Phase 1)
2. Generate a formal spec with BDD scenarios (Phase 2)
3. Pause — type "Continue" to review spec.md
4. Create a task registry with dependency graph (Phase 3)
5. Pause — type "Continue" to review tasks.md
6. Implement all tasks (Phase 4)
7. Run tests and self-heal failures (Phase 5)
8. Deliver with run instructions and cost report (Phase 6)


## Token Efficiency Architecture

Kodro uses a **modular constitution system** for 84% token savings:

| Component | Size | Load Strategy |
|-----------|------|---------------|
| **Kernel** | ~560 tokens | Always loaded |
| **Phase Module** | ~110-280 tokens | On-demand per phase |
| **Framework Spec** | ~120-230 tokens | Once per project |
| **Total/turn** | **~1,060 tokens** | vs ~6,750 monolithic |

**Results:** Active context consumption falls to ~1,060 tokens per turn instead of ~6,750 tokens—yielding 84% savings in token costs.

## Features

| Feature | Status |
|---------|--------|
| One-command pipeline | ✅ |
| 6-phase SDD with formal BDD | ✅ |
| Gatekeeper checkpoints (type "Continue") | ✅ |
| Resume / Rollback state machine | ✅ |
| Self-healing (5 attempts) with decision tree | ✅ |
| Per-phase cost tracking | ✅ |
| Post-delivery changes workflow | ✅ |
| Modular token-efficient constitution | ✅ |
| 6 AI agent integrations | ✅ |
| 7 framework constitutions | ✅ |

## Post-Delivery: Making Changes

After your project is delivered (Phase 6), request changes:

```bash
# Log a change request
kodro changes -p ~/projects/my-api "Add OAuth2 Google login"

# Then in your AI agent:
/kodro "Implement change CHANGE-20260522-001"
```

The agent will:
1. Read `.kodro/CHANGES.md` and current specs
2. Propose changes in `.kodro/changes/`
3. Wait for your approval (gatekeeper)
4. Implement approved changes
5. Re-run validation

## Architecture

```
User Idea → /kodro → Kernel (560tok) + P-Module (250tok) + FW-Spec (180tok)
    ↓
P1 Clarify → P2 Specify (DQI≥80) → [GATEKEEPER: type "Continue"]
→ P3 Plan → [GATEKEEPER: type "Continue"]
→ P4 Implement → P5 Validate → P6 Deliver → Next Steps & Run Guide
```

## Supported Integrations

| Agent | Command | File |
|-------|---------|------|
| OpenCode | `/kodro` | `.opencode/commands/kodro.md` |
| Claude | `$kodro` | `.claude/CLAUDE.md` |
| Cursor | Auto-read | `.cursor/rules/kodro.mdc` |
| Copilot | Context | `.github/prompts/kodro.prompt.md` |
| Gemini | Instructions | `.gemini/instructions.md` |
| Aider | Conventions | `.aider/CONVENTIONS.md` |

## CLI Commands

| Command | Purpose |
|---------|---------|
| `kodro init` | Initialize project with modular constitution |
| `kodro plan` | Generate tasks from spec |
| `kodro status` | Show pipeline progress |
| `kodro resume` | Continue from last phase |
| `kodro rollback` | Revert N phases |
| `kodro doctor` | Check project health |
| `kodro changes` | Request post-delivery changes |
| `kodro agent` | Get agent command syntax |

## Development

```bash
git clone https://github.com/mharoon1578/kodro.git
cd kodro
pip install -e ".[dev]"
pytest tests/ -v
```

## License

MIT
