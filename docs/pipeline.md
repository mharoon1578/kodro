<p align="center">
  <a href="https://github.com/mharoon1578/kodro">
    <img src="../assets/kodro_bg.png" alt="Kodro - Pipeline" >
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

<h1 align="center">🏗️ Pipeline</h1>

<p align="center">
<strong>Spec-Driven Development in 6 phases — from idea to production code.</strong>
</p>

---

## 📊 6-Phase Breakdown

| Phase | Name | Output | Gatekeeper | Token Budget |
|:-----:|------|--------|:----------:|:-----------:|
| **1** | ❓ Clarification | `clarifications.md` | No (skippable¹) | 1K |
| **2** | 📝 Specification | `spec.md` (BDD + ADR + DQI) | **✅ Yes** (skippable¹) | 2K |
| **3** | 📋 Task Planning | `tasks.md` (graph + registry) | **✅ Yes** | 1.5K |
| **4** | 💻 Implementation | `src/` | No | 3K |
| **5** | ✅ Validation | `validation_report.md` | No | 2K |
| **6** | 🚀 Delivery | `delivery.md` + Next Steps | No | 1K |

```
Your Idea → [P1 Clarify] → [P2 Specify] → 🛡️ GATEKEEPER →
            [P3 Plan]    → 🛡️ GATEKEEPER →
            [P4 Implement] → [P5 Validate] → [P6 Deliver] →
            Production-Ready Code
```

No code is written until Phase 4. The agent first clarifies your intent, writes a formal specification, and creates a dependency-aware task plan.

¹ P1/P2 gatekeepers are skipped when using `--quick` mode (v2.1.0+).

---

## 🛡️ Gatekeeper Checkpoints

At **Phase 2 (Specification)** and **Phase 3 (Task Planning)**, the pipeline pauses for human review:

```
╔══════════════════════════════════════════════════════════════════════╗
║  🛡️  GATEKEEPER CHECKPOINT                                          ║
╠══════════════════════════════════════════════════════════════════════╣
║  Phase: {PhaseName}                                                  ║
║  Artifact: {file_path}                                               ║
╠══════════════════════════════════════════════════════════════════════╣
║  Review the generated files before continuing.                       ║
║                                                                      ║
║  Type 'Continue' and press Enter to proceed                          ║
║  Type 'review' to pause and inspect                                  ║
╚══════════════════════════════════════════════════════════════════════╝
```

> **You MUST type "Continue"** — pressing Enter alone will not proceed.

### ⏩ Skipping Gatekeepers with `--quick` (v2.1.0+)

Use the `--quick` flag during init to bypass P1 (Clarification) and P2 (Specification) gatekeepers:

```bash
kodro init --quick --integration claude --framework python-fastapi
```

The pipeline starts directly at **Phase 3 (Task Planning)** using default spec templates. Recommended for experienced users who know their requirements upfront.

---

## 🔬 Phase Detail

### Phase 1: Clarification
Parse your idea → extract Needs, Features, Constraints → ask 3-5 clarifying questions.

```
Input:  "Build a weather dashboard"
Output: clarifications.md with NFC analysis + 3-5 questions
Gate:   All questions have rationale + impact
```

### Phase 2: Specification
Generate a formal specification with 6 mandatory sections and self-score DQI (must be ≥80).

```
Input:  User answers from Phase 1
Output: spec.md with BDD Gherkin, ADRs, Interface, Data, NFRs
Gate:   DQI ≥ 80 (self-scored)
```

### Phase 3: Task Planning
Decompose BDD scenarios into atomic tasks with a dependency graph and parallel markers.

```
Input:  spec.md
Output: tasks.md with Mermaid graph + task registry
Gate:   100% SC coverage, no circular deps
```

### Phase 4: Implementation
Execute tasks in dependency order. Write code via XML file blocks with atomic writes.

```
Input:  tasks.md + relevant spec sections
Output: Source code files
Anti:   No hardcoded secrets, no bare exceptions, no N+1 queries
```

### Phase 5: Validation
Run tests, self-heal failures (up to 5 attempts), check coverage tiers.

```
Input:  All implementation artifacts
Output: validation_report.md
Tree:   Syntax → Logic → Refactor → Deep → Human
```

### Phase 6: Delivery
Git commit, generate cost report, write delivery manifest, display next steps.

```
Input:  Validation report
Output: delivery.md + cost report + git commit
```

---

## 💰 Token Efficiency Techniques

| Technique | Implementation | Savings |
|-----------|---------------|:-------:|
| **Modular constitution** | Kernel + on-demand phase modules | ~75% |
| **Differential updates** | Append to artifact, don't regenerate | ~30% |
| **Smart chunking** | Max 2K chars per section | ~40% |
| **Section references** | "See §SPEC.4" instead of inlining | ~15% |
| **Cached framework** | Load once, reuse across phases | ~20% |

**Combined: ~84% reduction** — from ~6,750 to ~1,060 tokens per turn.

### Cost Comparison

| Tool | Tokens / Project | Relative Cost |
|------|:---------------:|:-------------:|
| Spec-Kit (7 commands) | ~50K | 100% |
| OpenSpec (multi-prompt) | ~35K | 70% |
| **Kodro** (modular) | **~10K** | **20%** |

---

## 🔄 Post-Delivery Workflow

After Phase 6 (Delivery):

1. **Next Steps Displayed** — How to run, where files are, key docs
2. **CHANGES.md** — Log change requests
3. **`kodro changes`** — CLI command to log changes
4. **Agent implements** — Reads CHANGES.md + specs, proposes edits, gatekeeper approval

```bash
kodro changes -p . "Add OAuth2 Google login"
/kodro "Implement change CHANGE-20260522-001"
```

---

## 📚 Related Resources

| Resource | Description |
|----------|-------------|
| [Getting Started](getting-started.md) | 3-step quick start guide |
| [Configuration](configuration.md) | Framework options, integrations, customization |
| [README](../README.md) | Full project overview |
