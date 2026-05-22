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
      <img src="assets/kodro_bg.png" alt="Kodro - AI Development Framework for Production LLM Applications">
    </picture>
  </a>
</p>

<p align="center">
<a href="https://pypi.org/project/kodro">
    <img src="https://img.shields.io/pypi/v/kodro.svg" alt="PyPI version">
</a>    
<a href="https://www.python.org">
    <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+">
</a>
<a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
</a>
<a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
</a>
<a href="https://github.com/mharoon1578/kodro">
    <img src="https://img.shields.io/badge/status-beta-orange.svg" alt="Status: Beta">
</a>
</p>

<h1 align="center">Kodro: Production-Ready AI Development Framework</h1>

<p align="center">
Transform natural language prompts into production software with an intelligent 6-phase pipeline. Kodro is a prompt engineering framework that delivers token-efficient, spec-driven development for AI agents—reducing costs by 84% while maintaining production quality.
</p>

<p align="center">
<strong>One command. Six phases. Production-ready code.</strong>
</p>

> [!NOTE]
> **Beta Software:** Kodro is in active development. You may encounter bugs, incomplete features, or breaking changes. Please report issues at [GitHub Issues](https://github.com/mharoon1578/kodro/issues).

> [!TIP]
> **New to Kodro?** Start with the [Getting Started Guide](docs/getting-started.md). For detailed configuration options see [Configuration](docs/configuration.md). For a deep dive into the pipeline phases see [Pipeline](docs/pipeline.md).


---

## Table of Contents
- [What is Kodro?](#what-is-kodro)
- [Why Kodro?](#why-kodro)
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [Token Efficiency Architecture](#token-efficiency-architecture)
- [Features](#features)
- [Use Cases](#use-cases)
- [Post-Delivery Changes](#post-delivery-making-changes)
- [Supported AI Agents](#supported-integrations)
- [CLI Commands](#cli-commands)
- [Comparison](#kodro-vs-alternatives)


---

## What is Kodro?

Kodro is an **AI development framework** that transforms a single natural language prompt into production software through a **6-phase Spec-Driven Development (SDD) pipeline**. Built for AI agents like Claude, Cursor, OpenCode, and GitHub Copilot, Kodro brings structure, quality control, and massive token savings to LLM-powered development.

Unlike traditional AI coding tools that require multiple prompts and manual orchestration, Kodro collapses the entire software development lifecycle into one `/kodro` command—with built-in quality gates, formal specifications, and automated testing.

**The pipeline:**

```
Your Idea → /kodro → P1 Clarify → P2 Specify → [GATEKEEPER] → P3 Plan → [GATEKEEPER]
→ P4 Implement → P5 Validate → P6 Deliver → Production-Ready Code
```

At each **gatekeeper**, the AI agent pauses for your review. **Type "Continue"** to proceed. No code is written until Phase 4—the agent first clarifies your intent, writes a formal specification, and creates a dependency-aware task plan.

---

## Why Kodro?

### **Built for Production LLM Applications**
- ✅ Formal BDD specifications (not just comments)
- ✅ Gatekeeper checkpoints prevent runaway AI
- ✅ Self-healing validation with decision trees
- ✅ Cost tracking per phase
- ✅ Rollback and resume state machine

### **84% Token Cost Reduction**
Kodro's modular constitution system loads only what's needed per phase:
- **~1,060 tokens/turn** vs. ~6,750 tokens for monolithic prompts
- Pay for what you use, not what you don't

### **Designed for AI Agents**
Native integrations with:
- OpenCode, Claude, Cursor, GitHub Copilot, Gemini, Aider

### **Spec-Driven, Not Prompt-Driven**
Generate formal specifications before code. Change requirements? Update the spec and regenerate—don't rewrite prompts.

---

## Quick Start

```bash
# Install Kodro
pip install kodro

# Initialize a project
mkdir my-weather-app && cd my-weather-app
kodro init --integration opencode --framework react-typescript

# In your AI agent (OpenCode, Claude, Cursor, etc.):
/kodro "Build a weather dashboard with 7-day forecast and location search"
```

**The agent will:**

1. **Phase 1 (Clarify):** Ask 3-5 clarifying questions about your requirements
2. **Phase 2 (Specify):** Generate formal spec.md with BDD scenarios (DQI ≥80%)
3. **Gatekeeper:** Pause—type "Continue" to review spec.md
4. **Phase 3 (Plan):** Create task registry with dependency graph
5. **Gatekeeper:** Pause—type "Continue" to review tasks.md
6. **Phase 4 (Implement):** Write all code following the plan
7. **Phase 5 (Validate):** Run tests, self-heal failures (5 attempts)
8. **Phase 6 (Deliver):** Generate run instructions + cost report

**Result:** Production-ready code with tests, documentation, and specifications—from one command.

---

## How It Works

Kodro implements **Spec-Driven Development (SDD)** for AI agents:

```
┌─────────────────────────────────────────────────────────────┐
│  Phase 1: CLARIFY                                           │
│  • Ask domain questions                                     │
│  • Identify ambiguities                                     │
│  • Capture user intent                                      │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 2: SPECIFY                                           │
│  • Generate formal specification (spec.md)                  │
│  • Write BDD scenarios (Given/When/Then)                    │
│  • Define acceptance criteria (DQI ≥80%)                    │
└─────────────────────────────────────────────────────────────┘
                           ↓
                   [GATEKEEPER: Review spec.md]
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 3: PLAN                                              │
│  • Decompose into tasks                                     │
│  • Build dependency graph                                   │
│  • Estimate complexity                                      │
└─────────────────────────────────────────────────────────────┘
                           ↓
                   [GATEKEEPER: Review tasks.md]
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 4: IMPLEMENT                                         │
│  • Execute tasks in dependency order                        │
│  • Generate code + tests                                    │
│  • Follow framework conventions                             │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 5: VALIDATE                                          │
│  • Run test suite                                           │
│  • Self-heal failures (5 attempts)                          │
│  • Verify specifications                                    │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 6: DELIVER                                           │
│  • Generate run instructions                                │
│  • Document next steps                                      │
│  • Report token costs                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Token Efficiency Architecture

Kodro uses a **modular constitution system** for massive token savings in prompt engineering:

| Component | Size | Load Strategy |
|-----------|------|---------------|
| **Kernel** | ~560 tokens | Always loaded |
| **Phase Module** | ~110-280 tokens | On-demand per phase |
| **Framework Spec** | ~120-230 tokens | Once per project |
| **Total/turn** | **~1,060 tokens** | vs ~6,750 monolithic |

**Results:** Active context consumption falls to ~1,060 tokens per turn instead of ~6,750 tokens—yielding **84% savings** in LLM API costs.

**Why this matters for production AI:**
- Lower costs for enterprise LLM applications
- Faster response times (less context to process)
- Scale to larger projects without hitting context limits

---

## Features

| Feature | Status |
|---------|--------|
| One-command pipeline (`/kodro`) | ✅ |
| 6-phase SDD with formal BDD | ✅ |
| Gatekeeper checkpoints (manual approval) | ✅ |
| Resume / Rollback state machine | ✅ |
| Self-healing validation (5 attempts) | ✅ |
| Per-phase cost tracking | ✅ |
| Post-delivery changes workflow | ✅ |
| Modular token-efficient constitution | ✅ |
| 6 AI agent integrations | ✅ |
| 7 framework constitutions | ✅ |

---

## Use Cases

### **Perfect for:**
- 🚀 **Rapid prototyping** with production-quality output
- 🏢 **Enterprise AI development** with cost control
- 📚 **Learning projects** with clear specifications
- 🔄 **Iterative development** with spec-first approach
- 🤖 **AI agent workflows** requiring structure and gates

### **Real-world applications:**
- Build full-stack web applications (React, Vue, Next.js)
- Create REST/GraphQL APIs with OpenAPI specs
- Develop CLI tools with comprehensive testing
- Generate data pipelines with validation
- Prototype ML applications with proper architecture

### **Who uses Kodro:**
- AI-assisted developers who need production quality
- Teams managing LLM costs at scale
- Indie hackers building products with AI agents
- Engineers learning prompt engineering best practices

---

## Post-Delivery: Making Changes

After your project is delivered (Phase 6), request changes without starting from scratch:

```bash
# Log a change request
kodro changes -p ~/projects/my-api "Add OAuth2 Google login"

# Then in your AI agent:
/kodro "Implement change CHANGE-20260522-001"
```

**The agent will:**
1. Read `.kodro/CHANGES.md` and current specifications
2. Propose changes in `.kodro/changes/`
3. Wait for your approval (gatekeeper)
4. Implement approved changes
5. Re-run validation suite
6. Update specifications

**No need to regenerate the entire project.** Kodro's state machine handles incremental changes intelligently.

---

## Supported Integrations

Kodro works with all major AI coding agents:

| Agent | Command | Configuration File |
|-------|---------|-------------------|
| **OpenCode** | `/kodro` | `.opencode/commands/kodro.md` |
| **Claude** | `$kodro` | `.claude/CLAUDE.md` |
| **Cursor** | Auto-read | `.cursor/rules/kodro.mdc` |
| **GitHub Copilot** | Context | `.github/prompts/kodro.prompt.md` |
| **Gemini** | Instructions | `.gemini/instructions.md` |
| **Aider** | Conventions | `.aider/CONVENTIONS.md` |

**No API keys required.** Kodro generates configuration files that work with your existing agent setup.

---

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

---

## Kodro vs Alternatives

| Feature | Kodro | LangChain | Direct API | Aider |
|---------|-------|-----------|-----------|-------|
| **One-command pipeline** | ✅ `/kodro` | ❌ Manual | ❌ Manual | ⚠️ Partial |
| **Formal specifications** | ✅ BDD | ❌ | ❌ | ❌ |
| **Gatekeeper checkpoints** | ✅ Built-in | ❌ | ❌ | ❌ |
| **Token efficiency** | ✅ 84% savings | ❌ High cost | ⚠️ Varies | ⚠️ Moderate |
| **Self-healing validation** | ✅ 5 attempts | ❌ | ❌ | ⚠️ Manual |
| **State management** | ✅ Resume/Rollback | ❌ | ❌ | ⚠️ Limited |
| **Cost tracking** | ✅ Per phase | ❌ | ⚠️ Manual | ❌ |
| **Learning curve** | Low | High | High | Medium |

**When to use Kodro:**
- You want production-quality code from AI agents
- You need cost control for enterprise LLM usage
- You value formal specifications over ad-hoc prompts
- You want automated quality gates and validation

**When to use alternatives:**
- LangChain: Building complex LLM chains and agents
- Direct API: Maximum control, custom workflows
- Aider: Quick iterative changes to existing code

---

## Architecture

```
User Idea → /kodro → Kernel (560tok) + P-Module (250tok) + FW-Spec (180tok)
    ↓
P1 Clarify → P2 Specify (DQI≥80) → [GATEKEEPER: type "Continue"]
→ P3 Plan → [GATEKEEPER: type "Continue"]
→ P4 Implement → P5 Validate → P6 Deliver → Next Steps & Run Guide
```

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Areas we need help:**
- Additional framework constitutions (Svelte, Angular, Django, etc.)
- More AI agent integrations (Windsurf, Replit, etc.)
- Performance optimizations for large projects
- Documentation improvements
- Bug reports and feature requests

---

## Development

```bash
git clone https://github.com/mharoon1578/kodro.git
cd kodro
pip install -e ".[dev]"
pytest tests/ -v
```

---


## Roadmap

- [x] PyPI package publication (v2.0.0)
- [ ] GitHub Pages documentation site
- [ ] VS Code extension
- [ ] Cost analytics dashboard
- [ ] Multi-agent collaboration support
- [ ] Cloud deployment integrations (Vercel, Railway, etc.)

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

<p align="center">
<strong>Built with ❤️ for the AI development community</strong>
</p>

<p align="center">
⭐ Star this repo if Kodro helps your projects! ⭐
</p>
