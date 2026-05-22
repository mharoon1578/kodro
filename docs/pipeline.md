# Pipeline

## 6-Phase Breakdown

| Phase | Name | Output | Gatekeeper | Token Budget |
|-------|------|--------|------------|--------------|
| 1 | Clarification | clarifications.md | No | 1K |
| 2 | Specification | spec.md (BDD+ADR+DQI) | **Yes** | 2K |
| 3 | Task Planning | tasks.md (graph+registry) | **Yes** | 1.5K |
| 4 | Implementation | src/ | No | 3K |
| 5 | Validation | validation_report.md | No | 2K |
| 6 | Delivery | delivery.md + Next Steps | No | 1K |

## Gatekeeper Checkpoints

At Phase 2 and Phase 3, the pipeline pauses for human review:

```
╔══════════════════════════════════════════════════════════════════════╗
║  🛡️  GATEKEEPER CHECKPOINT                                          ║
╠══════════════════════════════════════════════════════════════════════╣
║  Phase: {PhaseName}                                                  ║
║  Artifact: {file_path}                                               ║
╠══════════════════════════════════════════════════════════════════════╣
║  Review the generated files before continuing.                         ║
║                                                                      ║
║  [bold green]Type 'Continue' and press Enter to proceed[/bold green]                     ║
║  [bold yellow]Type 'review' to pause and inspect[/bold yellow]                             ║
╚══════════════════════════════════════════════════════════════════════╝
```

**You MUST type "Continue"** — pressing Enter alone will not proceed.

## Token Efficiency Techniques

| Technique | Implementation | Savings |
|-----------|---------------|---------|
| **Modular constitution** | Kernel + on-demand phase modules | ~75% |
| **Differential updates** | Append to artifact, don't regenerate | ~30% |
| **Smart chunking** | Max 2K chars per section | ~40% |
| **Section references** | "See §SPEC.4" instead of inlining | ~15% |
| **Cached framework** | Load once, reuse across phases | ~20% |

## Cost Comparison

| Tool | Tokens / Project | Relative Cost |
|------|-----------------|---------------|
| Spec-Kit (7 commands) | ~50K | 100% |
| OpenSpec (multi-prompt) | ~35K | 70% |
| **Kodro** (modular) | **~10K** | **20%** |

## Post-Delivery Workflow

After Phase 6 (Delivery):

1. **Next Steps Displayed** — How to run, where files are, key docs
2. **CHANGES.md** — Log change requests
3. **kodro changes** — CLI command to log changes
4. **Agent implements** — Reads CHANGES.md + specs, proposes edits, gatekeeper approval
