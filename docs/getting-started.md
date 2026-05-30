<p align="center">
  <a href="https://github.com/mharoon1578/kodro">
    <img src="../assets/kodro_bg.png" alt="Kodro - Getting Started" >
  </a>
</p>

<p align="center">
<a href="https://www.python.org">
    <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+">
</a>
<a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
</a>
<a href="../README.md">
    <img src="https://img.shields.io/badge/-Back%20to%20README-blue?style=flat" alt="Back to README">
</a>
</p>

<h1 align="center">🚀 Getting Started with Kodro</h1>

<p align="center">
<strong>From zero to production-ready code in 3 steps.</strong>
</p>

---

## 📦 Installation

Install Kodro directly from PyPI:

```bash
pip install kodro
```

Or for development / local installation:
```bash
git clone https://github.com/mharoon1578/kodro.git
cd kodro
pip install -e ".[dev]"
```


---

## ⚡ 3-Step Quick Start

### 1️⃣ Initialize

```bash
kodro init --integration claude --framework python-fastapi
```

This scaffolds your project with a modular constitution — kernel + phase modules + framework spec — averaging just **~1,060 tokens/turn**.

| Flag | Default | Purpose |
|------|---------|---------|
| `--integration` / `-i` | `opencode` | AI agent (claude, cursor, copilot, gemini, aider) |
| `--framework` / `-f` | `python-fastapi` | Target stack (react, vue, go, rails, rust, django) |
| `--path` / `-p` | `.` | Project directory |
| `--quick` / `--no-quick` | `--no-quick` | Skip P1/P2 gatekeepers for experienced users |
| `--git` / `--no-git` | `--git` | Enable Git integration |

### 2️⃣ Prompt

Inside your AI agent:

```bash
# OpenCode
/kodro "Build a task management API"

# Claude
$kodro "Build a task management API"

# Cursor / Copilot / Gemini / Aider
# (Uses respective command — see Configuration)
```

### 3️⃣ Review & Continue

Kodro pauses at **gatekeeper checkpoints** after Specification (Phase 2) and Task Planning (Phase 3). Review the generated files, then:

```
╔══════════════════════════════════════════════════════════════════════╗
║  🛡️  GATEKEEPER CHECKPOINT                                          ║
╠══════════════════════════════════════════════════════════════════════╣
║  Phase: Specification                                                ║
║  Artifact: .kodro/spec.md                                            ║
╠══════════════════════════════════════════════════════════════════════╣
║  Type 'Continue' and press Enter to proceed                          ║
║  Type 'review' to pause and inspect                                  ║
╚══════════════════════════════════════════════════════════════════════╝
```

**Type `Continue`** to proceed. Type `review` to pause and inspect files.

---

## ⚡ Quick Mode (v2.1.0+)

Skip the Clarification (P1) and Specification (P2) gatekeepers to go straight to task planning:

```bash
kodro init --quick --integration claude --framework python-fastapi
```

In your AI agent, the pipeline starts at Phase 3 instead of Phase 1.

---

---

## 🔧 Flexible Bootloader (v2.1.0+)

Run Kodro without `kodro init`. The bootloader auto-detects your project and picks defaults:

```bash
# Auto-detect framework from project files
kodro bootstrap

# Specify framework + integration on the fly
kodro bootstrap --framework python-fastapi --integration claude

# Or just start — the bootloader asks what you need
kodro
```

The bootloader checks for existing `.kodro/` state, project type (package.json, pyproject.toml, etc.), and prompts only for missing info.

---

## 🧠 Token Efficiency

Kodro's modular constitution loads only what's needed, saving **84%** vs. monolithic prompts:

| Component | Tokens | Load Strategy |
|-----------|--------|---------------|
| **Kernel** | ~560 | Always loaded — state machine, rules, I/O format |
| **Phase Module** | ~250 | On demand — current phase only |
| **Framework Spec** | ~180 | Loaded once — your chosen stack |
| **Total / turn** | **~1,000** | vs ~7,000 monolithic |

**Bottom line:** Lower costs, faster responses, and the ability to scale to larger projects without hitting context limits.

---

## 🔄 Post-Delivery Changes

After delivery (Phase 6), request changes without starting over:

```bash
# Log a change request
kodro changes -p ~/projects/my-api "Add user authentication"

# In your AI agent:
/kodro "Implement change CHANGE-20260522-001"
```

The agent will read current specs, propose changes in `.kodro/changes/`, wait for your approval, implement, and re-validate.

---

## 📚 Next Steps

| Resource | Description |
|----------|-------------|
| [Configuration](configuration.md) | Framework options, integration setup, customization |
| [Pipeline](pipeline.md) | Deep dive into all 6 phases and gatekeepers |
| [README](../README.md) | Full project overview, features, comparisons |
| Run `kodro doctor` | Check project health anytime |
