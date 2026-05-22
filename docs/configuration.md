# Configuration

## Config File

Kodro stores configuration in `.kodro/` and state in `.kodro/state.json`.

## Modular Constitution

After `kodro init`, your project has:

```
.kodro/
├── state.json       # Pipeline state machine
├── spec.md          # Specification (BDD + ADR + NFR)
├── tasks.md         # Task registry with dependency graph
├── clarifications.md # User answers from Phase 1
├── CHANGES.md       # Post-delivery change requests
├── delivery.md      # Delivery manifest (generated at P6)
└── constitution/    # Agent instruction modules
    ├── kernel.md       # State machine, rules, I/O format (~560 tok)
    ├── p1.md           # P1: Clarification (~110 tok)
    ├── p2.md           # P2: Specification + DQI scoring (~280 tok)
    ├── p3.md           # P3: Task Planning (~150 tok)
    ├── p4.md           # P4: Implementation (~140 tok)
    ├── p5.md           # P5: Validation (~190 tok)
    ├── p6.md           # P6: Delivery + Next Steps (~150 tok)
    └── framework.md    # Framework micro-spec (~120-230 tok)
```

The agent loads **only** `kernel.md` + current `p{N}.md` + `framework.md` per turn.

## Framework Options

| Framework | Enum Value |
|-----------|-----------|
| React + TypeScript | `react-typescript` |
| Python + FastAPI | `python-fastapi` |
| Go + Gin | `go-gin` |
| Ruby on Rails | `ruby-rails` |
| Rust + Axum | `rust-axum` |
| Vue + TypeScript | `vue-typescript` |
| Python + Django | `python-django` |

## Integration Options

| Agent | Enum Value | Command |
|-------|-----------|---------|
| OpenCode | `opencode` | `/kodro` |
| Claude | `claude` | `$kodro` |
| Cursor | `cursor` | Auto-read |
| Copilot | `copilot` | Context |
| Gemini | `gemini` | Instructions |
| Aider | `aider` | Conventions |

## Constitution Customization

Edit files in `.kodro/constitution/` to override rules for your project.

## Post-Delivery Configuration

After delivery, modify `.kodro/CHANGES.md` to request edits:

```markdown
## CHANGE-20260522-001: Add OAuth2
- **Status:** proposed
- **Request:** Add Google OAuth2 login
- **Scope:** src/auth/
- **Priority:** high
```

Then run `kodro changes -p . "Add OAuth2"` to log it.
