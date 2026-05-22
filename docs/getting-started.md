# Getting Started

## Installation

```bash
pip install kodro
```

## 3-Step Quick Start

1. **Initialize**
   ```bash
   kodro init --integration claude --framework python-fastapi
   ```

2. **Prompt**
   Inside Claude:
   ```
   $kodro "Build a task management API"
   ```

3. **Review & Continue**
   Kodro pauses at gatekeepers. Review the generated files, then **type "Continue"** to proceed.

## Token Efficiency

Kodro's modular constitution loads only what's needed:
- **Kernel** (~560 tok): Always loaded — state machine, rules, I/O format
- **Phase Module** (~250 tok): Loaded on demand — current phase only
- **Framework Spec** (~180 tok): Loaded once — your chosen stack

Total per turn: **~1,000 tokens** instead of dumping a 7,000-token wall of text.

## Gatekeeper Checkpoints

At Phase 2 (Specification) and Phase 3 (Task Planning), the pipeline pauses:

```
╔══════════════════════════════════════════════════════════════════════╗
║  🛡️  GATEKEEPER CHECKPOINT                                          ║
╠══════════════════════════════════════════════════════════════════════╣
║  Phase: Specification                                                ║
║  Artifact: .kodro/spec.md                                            ║
╠══════════════════════════════════════════════════════════════════════╣
║  [bold green]Type 'Continue' and press Enter to proceed[/bold green]                     ║
║  [bold yellow]Type 'review' to pause and inspect[/bold yellow]                             ║
╚══════════════════════════════════════════════════════════════════════╝
```

**Type "Continue"** to proceed. Type "review" to pause and inspect files.

## Post-Delivery Changes

After delivery (Phase 6), request changes:

```bash
# Log a change request
kodro changes -p ~/projects/my-api "Add user authentication"

# In your AI agent:
/kodro "Implement change CHANGE-20260522-001"
```

## Next Steps

- Read [Configuration](configuration.md)
- Understand the [Pipeline](pipeline.md)
- Run `kodro doctor` anytime to check project health
