<p align="center">
  <a href="https://github.com/mharoon1578/kodro">
    <img src="../assets/kodro_bg.png" alt="Kodro - Configuration" >
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
<a href="getting-started.md">
    <img src="https://img.shields.io/badge/-Getting%20Started-green?style=flat" alt="Getting Started">
</a>
</p>

<h1 align="center">⚙️ Configuration</h1>

<p align="center">
<strong>Everything you need to customize Kodro for your project and workflow.</strong>
</p>

---

## 📁 Project Structure

After `kodro init`, your project contains:

```
.kodro/
├── state.json           # Pipeline state machine
├── spec.md              # Specification (BDD + ADR + NFR)
├── tasks.md             # Task registry with dependency graph
├── clarifications.md    # User answers from Phase 1
├── CHANGES.md           # Post-delivery change requests
├── delivery.md          # Delivery manifest (generated at P6)
└── constitution/        # Agent instruction modules
    ├── kernel.md        # State machine, rules, I/O format (~560 tok)
    ├── p1.md            # P1: Clarification (~110 tok)
    ├── p2.md            # P2: Specification + DQI scoring (~280 tok)
    ├── p3.md            # P3: Task Planning (~150 tok)
    ├── p4.md            # P4: Implementation (~140 tok)
    ├── p5.md            # P5: Validation (~190 tok)
    ├── p6.md            # P6: Delivery + Next Steps (~150 tok)
    └── framework.md     # Framework micro-spec (~120-230 tok)
```

> **Token efficiency:** The agent loads **only** `kernel.md` + current `p{N}.md` + `framework.md` per turn. No monolithic dump — just ~1,060 tokens at a time.

---

## 🧩 Framework Options

| Framework | Enum Value | Best For |
|-----------|-----------|----------|
| React + TypeScript | `react-typescript` | SPAs, dashboards, interactive UIs |
| Python + FastAPI | `python-fastapi` | REST APIs, microservices |
| Go + Gin | `go-gin` | High-concurrency backends |
| Ruby on Rails | `ruby-rails` | Full-stack web apps, MVPs |
| Rust + Axum | `rust-axum` | Performance-critical services |
| Vue + TypeScript | `vue-typescript` | Lightweight frontends |
| Python + Django | `python-django` | Content sites, admin panels |

Usage:

```bash
kodro init --framework python-fastapi
```

---

## 🤖 Integration Options

| Agent | Enum Value | Command | File Created |
|-------|-----------|---------|-------------|
| **OpenCode** | `opencode` | `/kodro` | `.opencode/commands/kodro.md` |
| **Claude** | `claude` | `$kodro` | `.claude/CLAUDE.md` |
| **Cursor** | `cursor` | Auto-read | `.cursor/rules/kodro.mdc` |
| **Copilot** | `copilot` | Context | `.github/prompts/kodro.prompt.md` |
| **Gemini** | `gemini` | Instructions | `.gemini/instructions.md` |
| **Aider** | `aider` | Conventions | `.aider/CONVENTIONS.md` |

Usage:

```bash
kodro init --integration claude
```

> No API keys required. Kodro generates configuration files that work with your existing agent setup.

---

## ✏️ Constitution Customization

Each constitution module is a plain markdown file in `.kodro/constitution/`. Edit any file to override rules for your project:

| Module | Purpose | Token Budget |
|--------|---------|-------------|
| `kernel.md` | State machine, absolute rules, token protocol | ~560 |
| `p1.md` – `p6.md` | Phase-specific instructions | ~110-280 each |
| `framework.md` | Architecture, data patterns, anti-patterns | ~120-230 |

**Example: Customizing the FastAPI framework spec**

Edit `.kodro/constitution/framework.md`:

```markdown
# K:FW-PY-FASTAPI
## ARCH: Hexagonal. src/{domain,application,infrastructure,interfaces}
## DATA: Pydantic v2 ALL shapes. No raw dicts cross-layer.
## ASYNC: ALL I/O async. asyncpg/sqlalchemy async.
## TEST: pytest-asyncio auto. httpx AsyncClient. factory-boy.
```

---

## 🔄 Post-Delivery Configuration

After delivery, modify `.kodro/CHANGES.md` to request edits:

```markdown
## CHANGE-20260522-001: Add OAuth2
- **Status:** proposed
- **Request:** Add Google OAuth2 login
- **Scope:** src/auth/
- **Priority:** high
```

Then log it:

```bash
kodro changes -p . "Add OAuth2"
```

---

## 📚 Related Resources

| Resource | Description |
|----------|-------------|
| [Getting Started](getting-started.md) | 3-step quick start guide |
| [Pipeline](pipeline.md) | Deep dive into all 6 phases |
| [README](../README.md) | Full project overview |
