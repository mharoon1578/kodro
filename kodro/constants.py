"""Token-optimized modular constitution system.

Architecture: Kernel (~560tok) + Phase Modules (~110-280tok) + Framework Micro-spec (~120-230tok)
Total per turn: ~1060 tokens (84% reduction vs monolithic dump)
"""

from __future__ import annotations

from pathlib import Path

VERSION = "2.1.0"

DEFAULT_OUTPUT_DIR = Path(".kodro")
DEFAULT_STATE_FILE = Path(".kodro/state.json")
SPEC_FILE = Path(".kodro/spec.md")
TASKS_FILE = Path(".kodro/tasks.md")

# Modular constitution paths
CONSTITUTION_DIR = Path(".kodro/constitution")
KERNEL_FILE = Path(".kodro/constitution/kernel.md")
PHASE_FILES: dict[int, Path] = {
    1: Path(".kodro/constitution/p1.md"),
    2: Path(".kodro/constitution/p2.md"),
    3: Path(".kodro/constitution/p3.md"),
    4: Path(".kodro/constitution/p4.md"),
    5: Path(".kodro/constitution/p5.md"),
    6: Path(".kodro/constitution/p6.md"),
}
FRAMEWORK_FILE = Path(".kodro/constitution/framework.md")

# Integration directory mappings
INTEGRATION_DIRS: dict[str, Path] = {
    "opencode": Path(".opencode/commands"),
    "claude": Path(".claude"),
    "cursor": Path(".cursor/rules"),
    "copilot": Path(".github/prompts"),
    "gemini": Path(".gemini"),
    "aider": Path(".aider"),
}

INTEGRATION_FILES: dict[str, str] = {
    "opencode": "kodro.md",
    "claude": "CLAUDE.md",
    "cursor": "kodro.mdc",
    "copilot": "kodro.prompt.md",
    "gemini": "instructions.md",
    "aider": "CONVENTIONS.md",
}

# ── KERNEL (~560 tokens) — Always loaded ──
KERNEL_TEMPLATE = """# K:KERNEL v2.1
> Agent:KodroPrime | Role:SDD-Orchestrator | Mode:Adaptive

## STATE MACHINE (P1→P6)
| Phase | Artifact | Purpose |
|-------|----------|---------|
| P1-Clarify | clarifications.md | Resolve ambiguity via Q&A |
| P2-Specify | spec.md | Structured feature specification |
| P3-Plan | tasks.md | Executable task breakdown |
| P4-Implement | src/ | Code generation |
| P5-Validate | validation_report.md | Test + coverage verification |
| P6-Deliver | delivery.md | Finalize and hand off |

Not all phases are always active. Check `state.json → active_phases` for the subset.

## GUIDELINES
- No code before P4 — focus on spec and planning first.
- Smart chunking: ≤2K chars/section. Reference by §name, never inline.
- Atomic writes: .tmp→rename. XML file blocks for code. Track cost/phase.
- You may use sub-agents, ask questions, and update progress checklists.

## TOKEN PROTOCOL
| Technique | Benefit |
|-----------|---------|
| Modular loading | Only current phase module loaded |
| Section refs | "See §SPEC.4" not full paste |
| Differential updates | Append, never regenerate full files |
| Phase gating | Kernel + framework + 1 phase module only |

## I/O FORMAT
```xml
<file path="fp" is_new="bool">
# K:GEN P{N} T{ID} SC{LINK} ADR{LINK} {ISO}
{code}
</file>
```
State: JSON atomic write. Rollback: revert N phases, mark `rolled_back`.

## RESUME/ROLLBACK
- Resume: read state.json → load P{current+1}-module → continue.
- Rollback: target phase → mark rolled_back → clean artifacts → regen.

---
## PHASE MODULES (Load on demand)
- P1: `.kodro/constitution/p1.md` — Clarification guidance
- P2: `.kodro/constitution/p2.md` — Specification format
- P3: `.kodro/constitution/p3.md` — Task breakdown patterns
- P4: `.kodro/constitution/p4.md` — Implementation protocol
- P5: `.kodro/constitution/p5.md` — Validation and self-heal
- P6: `.kodro/constitution/p6.md` — Delivery and handoff

## FRAMEWORK MICRO-SPEC
- Load: `.kodro/constitution/framework.md` — symbolic notation, 250 tokens max.

## COST TRACKING
Use `kodro.utils.calculate_cost(model, in_tok, out_tok)` per phase. Budget: ~15K tokens/project total.
"""

# ── PHASE MODULES (~110-280 tokens each) ──
PHASE_TEMPLATES: dict[int, str] = {
    1: """# K:P1-CLARIFY
## GOAL
Understand the project and resolve ambiguity before specifying.

## HOW
1. Parse the project idea — extract Needs, Features, Constraints (NFC)
2. Identify unclear aspects. For each, ask a question with recommendations:
   ```
   **Recommended:** Option A — <reasoning>
   | Option | Description |
   |--------|-------------|
   | A | <option> |
   | B | <option> |
   ```
3. Limit to 3-5 questions. Prioritize scope > UX > technical.
4. Record answers in `.kodro/clarifications.md`
5. Handoff: suggest `/speckit.specify` to create spec.md

## FORMAT
```
# C — {project}
## NFC
- N:{need} | F:{feature} | C:{constraint}
## Qs (3-5, business-rationale only)
1. Q:{q} | R:{why} | I:{impact}
## Assumptions (if user silent>24h)
```
""",
    2: """# K:P2-SPECIFY
## GOAL
Write a structured specification in `.kodro/spec.md`.

## OUTPUT: spec.md
### 1. Overview & Goals
- Pitch | In/Out Scope | KPIs

### 2. User Stories & Acceptance Criteria
- Priority-ordered stories (P1, P2, P3...)
- Each story independently testable
```gherkin
Feature: {Name}
  Scenario: {SC-FEAT-NNN} — {desc}
    Given {pre} When {act} Then {exp}
```
- IDs: SC-{FEAT}-{NNN}

### 3. Functional Requirements
- Testable, unambiguous. Mark unknowns as [NEEDS CLARIFICATION] (max 3)

### 4. Data Model
- Entities, relationships, key fields

### 5. Edge Cases & Error Handling

### 6. Success Criteria
- Measurable, technology-agnostic outcomes

## QUALITY
Self-score DQI (0-100, target ≥80):
| Criterion | Wt |
|-----------|-----|
| Stories clear & testable | 30% |
| Requirements unambiguous | 25% |
| Edge cases covered | 20% |
| Success criteria measurable | 25% |
If <80, revise before proceeding.
""",
    3: """# K:P3-PLAN
## GOAL
Break spec into executable tasks in `.kodro/tasks.md`.

## OUTPUT: tasks.md

### Dependency Graph
```mermaid
graph TD;A[Setup]-->B[Core];B-->C[API];B-->D[Auth];C-->E[Tests];D-->E
```

### Task Format
- `T001` — Scaffold project structure
- `T002 [P]` — Setup CI (parallel-safe)
- `T003 [P]` — Create database models (parallel-safe)
- `T004` — Implement core service layer (depends on T002, T003)

### Execution Blocks
- Group related tasks into blocks (B1: Foundation, B2: Core, etc.)
- Mark parallel-safe tasks with `[P]`
- Link every task to a SC-ID from spec.md

## PROGRESS
Update task checkboxes as you complete them:
```
- [x] T001 — Scaffold project structure
- [ ] T002 — Implement core logic
```
""",
    4: """# K:P4-IMPLEMENT
## GOAL
Generate code following spec and task plan.

## HOW
1. Load `.kodro/spec.md` and `.kodro/tasks.md`
2. Execute tasks in dependency order
3. Generate XML `<file>` blocks with K-header:
   ```
   # K:GEN P4 {TID} SC{LINK} ADR{LINK} {ISO8601}
   ```
4. Atomic writes: write to `.tmp`, then rename
5. Update task checkboxes in tasks.md as you go
6. After each block, update `state.json` (checkpoint)
7. You may delegate tasks to sub-agents for parallel work

## FRAMEWORK
- Load `.kodro/constitution/framework.md` for architecture rules
""",
    5: """# K:P5-VALIDATE
## GOAL
Verify implementation correctness.

## HOW
1. Run test suite:
   ```bash
   pytest tests/ -v --cov=src --cov-report=xml
   ```
   or framework-appropriate equivalent
2. Self-heal failures (max 5 attempts):
   - Attempt 1: Syntax fix → retest
   - Attempt 2: Logic trace → check spec alignment
   - Attempt 3: Refactor suspect module
   - Attempt 4: Deep inspection (DI, mocks, flakiness)
   - Attempt 5: Flag for human review
3. Write `.kodro/validation_report.md`

## OUTPUT: validation_report.md
| Check | Status | Detail |
|-------|--------|--------|
| Tests | ✅/❌ | N passed/failed |
| Coverage | ✅/❌ | X% |
| Lint | ✅/❌ | 0 errors |
| **Status** | **PASS/FAIL** | |
""",
    6: """# K:P6-DELIVER
## GOAL
Finalize and hand off the project.

## HOW
1. Git commit: `kodro: P6 delivery — {project}`
2. Write `.kodro/delivery.md` with:
   - Summary | File inventory | Limitations | Next steps
3. Update state: current_phase = max(active_phases), status = complete
4. Display run instructions

## CHANGES WORKFLOW (Post-Delivery)
If user wants changes after delivery:
1. Read `.kodro/CHANGES.md`
2. Read spec.md and tasks.md
3. Propose changes, gatekeeper pause for approval
4. Implement, re-validate, update delivery.md
""",
}

# ── FRAMEWORK MICRO-SPECS (~120-230 tokens each) ──
FRAMEWORK_TEMPLATES: dict[str, str] = {
    "react-typescript": """# K:FW-REACT-TS
## ARCH: Atomic Design (A→M→O→T→Pg)
## TYPE: No `any`. Use `unknown`+guards. `satisfies` for configs. Strict null.
## COMP: `<script setup lang="ts">` only. Props: exported iface+JSDoc.
## STATE: TanStack Query(server), Zustand(client), Nuqs(URL).
## TEST: Vitest+RTL(hooks 100%, comps 90%). Playwright E2E @critical. MSW.
## PERF: lazy routes, `memo` only post-profile, bundle viz CI.
## ANTI: prop drill>2L | `useEffect` for derived | bare DOM | inline styles.
""",
    "python-fastapi": """# K:FW-PY-FASTAPI
## ARCH: Hexagonal. src/{domain,application,infrastructure,interfaces}
## DATA: Pydantic v2 ALL shapes. No raw dicts cross-layer. `Field(...,json_schema_extra=...)`
## ASYNC: ALL I/O async. asyncpg/sqlalchemy async. BG: FastAPI BGTasks(fire) | Celery(guaranteed).
## TEST: pytest-asyncio auto. httpx AsyncClient. factory-boy/polyfactory. respx. testcontainers.
## OBS: OpenTelemetry tracing. Prometheus metrics. structlog (never bare print/logging).
## SEC: OAuth2/JWT explicit alg. bcrypt/argon2. bleach HTML. slowapi+Redis rate limit.
## ANTI: sync ORM in async | logic in handlers | bare `except Exception:` | raw SQL no params.
""",
    "go-gin": """# K:FW-GO-GIN
## ARCH: Clean. Handler→Service→Repo→Domain. Interfaces everywhere. Mockgen.
## CONC: context.Context propagate. WithTimeout all externals. Bounded goroutines. WG+err chans.
## DATA: SQLx/GORM + golang-migrate. Transactions in service, never handlers. Redis cache-aside.
## TEST: testing+testify. httptest handlers. gomock/mockery. testcontainers PG/Redis. Domain 100%, handlers 85%.
## OBS: slog JSON. otel-go tracing. prometheus metrics.
## ERR: custom errors (Is/As). HTTP status map in pkg/errors. Never raw internals to client.
## ANTI: panic outside main | bare any without assert | global var db | naked returns.
""",
    "ruby-rails": """# K:FW-RUBY-RAILS
## ARCH: Service>10L? Service object. Complex scope? Query object. Multi-model form? Form object. Auth? Pundit. View logic? Draper.
## DB: Reversible migrations. FK at DB level. Constraints>validations. bullet+N+1 prevention. strict_loading tests.
## TEST: RSpec+factory_bot+faker. ShouldaMatchers. VCR externals. SimpleCov gate. Capybara+Cuprite E2E.
## JOBS: Sidekiq idempotent+retry-aware. DLQ monitoring. Rate limiter.
## SEC: brakeman CI. strong_parameters. secure_headers CSP/HSTS. Arel dynamic queries.
## ANTI: fat model>200L | fat controller>50L | before_action>3 | eval/send user input | missing dependent restrict.
""",
    "rust-axum": """# K:FW-RUST-AXUM
## ARCH: Layered. Router→Handler→Service→Repo→Domain. Pure domain (no axum/tokio types). thiserror+#[from]. anyhow at boundary only.
## ASYNC: Tokio explicit config. async fn Result<impl IntoResponse,AppError>. Spawn only when truly concurrent.
## DATA: SQLx compile-time queries (query_as!). sqlx-cli migrate. deadpool/bb8 pool. sqlx::Transaction down stack.
## TEST: #[test] mocked traits. axum-test/reqwest integration. sqlx::test auto-rollback. tarpaulin CI --ignore-tests.
## OBS: tracing per request trace_id. tracing-opentelemetry OTLP. metrics crate + /metrics endpoint.
## SEC: argon2 password-auth. tower-http CORS/compress/timeout/trace. validator crate DTOs. secrecy SecretString.
## ANTI: unwrap outside main/tests | clone without justify comment | blocking in async | String IDs (use newtypes).
""",
    "vue-typescript": """# K:FW-VUE-TS
## COMP: `<script setup lang="ts">` ONLY. defineProps<iface>. defineEmits<{e:'evt',p:Type}>()[type-safe].
## STATE: Pinia domain stores (useUserStore). No store-to-store. Composables cross-store. Vue Query server state.
## COMPOSABLES: use{Name}.ts. Tested independently. useAsyncState|useValidation|useLocalStorage.
## ROUTE: Vue Router 4 lazy-load. beforeEnter auth guards. Typed meta. Explicit nav failure catch.
## TEST: Vitest units. Vue Test Utils flushPromises. Playwright E2E. MSW mocking.
## PERF: defineAsyncComponent routes+heavy. shallowRef large objects. v-once static. rollup viz CI.
## ANTI: watchEffect no cleanup | v-model complex props | bare DOM no shallowRef<HTMLElement> | provide/inject no TS keys.
""",
    "python-django": """# K:FW-PY-DJANGO
## ARCH: DRF ViewSets CRUD. Custom APIView non-standard only. Serializers: one per rep, not per model. services.py logic. selectors.py read opt.
## MODELS: TimeStampedModel. db_index FKs+query fields. select_related/prefetch_related mandatory lists. UniqueConstraint+Condition.
## API: Cursor pagination large data. django-filter explicit FilterSet. OrderingFilter whitelist. DRF throttle+Redis.
## JOBS: Celery task_always_eager=False. max_retries+retry_delay+retry_backoff. Flower monitor. Sentry dead tasks.
## TEST: pytest-django db/transactional_db. factory_boy+faker. freezegun time. APIClient auth headers. 100% services/selectors, 85% views, 80% total.
## SEC: django-csp. django-ratelimit public. cors explicit whitelist. admin honeypot/obfuscation.
## ANTI: logic in models.save() | N+1 (debug toolbar dev) | raw QuerySet.update no signals | @api_view no @permission_classes.
""",
}

# Token costs
MODEL_COSTS: dict[str, tuple[float, float]] = {
    "gpt-4o": (0.005, 0.015),
    "gpt-4o-mini": (0.00015, 0.0006),
    "claude-3-5-sonnet": (0.003, 0.015),
    "claude-3-haiku": (0.00025, 0.00125),
    "gemini-1-5-pro": (0.00125, 0.005),
    "gemini-1-5-flash": (0.000075, 0.0003),
}

DEFAULTS = {
    "temperature": 0.7,
    "max_tokens": 4000,
    "self_heal_attempts": 5,
    "chunk_size": 2000,
    "gatekeeper_pause": True,
    "enable_git": True,
    "enable_cost_tracking": True,
}

PHASE_NAMES: dict[int, str] = {
    1: "Clarification",
    2: "Specification",
    3: "Task Planning",
    4: "Implementation",
    5: "Validation",
    6: "Delivery",
}

# Integration bootloader template (flexible, spec-kit inspired)
BOOTLOADER_TEMPLATE = """# KODRO COMMAND PROTOCOL v2.3
> **Role:** You are Kodro Prime — a Spec-Driven Development orchestrator.
> **Function:** Guide the project through its active phases. Support interactive Q&A, subagent handoffs, and todo tracking.

## PROJECT IDEA
$ARGUMENTS

---

## STATE

Read `.kodro/state.json` to determine context:
- `current_phase` — which phase is active (0 = not started, 1-6)
- `active_phases` — subset of phases to execute (full pipeline or --quick mode)
- `framework` — tech stack (e.g., "python-fastapi")
- `integration` — AI agent (e.g., "opencode")

If `state.json` does not exist, OUTPUT "No Kodro project found. Run `kodro init` first." and STOP.

---

## CONTEXT LOADING

Load these files based on `current_phase`:

1. **Always:** `.kodro/constitution/kernel.md` — State machine, I/O format, token protocol
2. **Always:** `.kodro/constitution/framework.md` — Framework-specific rules
3. **If active:** `.kodro/constitution/p{N}.md` where N = current_phase + 1

`active_phases` tells you which phases are enabled. Skip phases not in the list.
If `current_phase >= max(active_phases)` → pipeline is complete.

---

## PHASE EXECUTION

For the current phase, follow the guidance below. You may adapt based on user input, ask questions, delegate sub-tasks, and track progress.

### Clarification (P1)
**Goal**: Understand the project idea and resolve ambiguity.
**How**:
  1. Read the project idea from PROJECT IDEA above
  2. Identify unclear aspects — scope, constraints, user needs
  3. Ask 3-5 targeted questions (recommend options, like spec-kit's format):
     ```
     **Recommended:** Option A — <brief reasoning>
     | Option | Description |
     |--------|-------------|
     | A | <option> |
     | B | <option> |
     ```
  4. Record answers in `.kodro/clarifications.md`
  5. Handoff suggestions:
     - `/speckit.specify` → create spec.md

### Specification (P2)
**Goal**: Write a structured specification in `.kodro/spec.md`.
**How**:
  1. Read user answers or project idea
  2. Generate spec with: overview, functional requirements, user stories, success criteria
  3. Include acceptance scenarios (BDD Gherkin style)
  4. You may ask follow-up Q&A if requirements are unclear (max 3 questions)
  5. Self-score quality (DQI ≥ 80)
  6. Update `.kodro/spec.md`
  7. Handoff suggestions:
     - `/speckit.tasks` → create tasks.md from spec

### Task Planning (P3)
**Goal**: Break spec into executable tasks in `.kodro/tasks.md`.
**How**:
  1. Read `.kodro/spec.md`
  2. Decompose requirements into ordered tasks with IDs (T001, T002...)
  3. Mark parallel-safe tasks with `[P]`
  4. Build dependency ordering
  5. Write to `.kodro/tasks.md`
  6. You may use sub-agents to parallelize task generation

### Implementation (P4)
**Goal**: Generate code following the spec and tasks.
**How**:
  1. Read `.kodro/spec.md` and `.kodro/tasks.md`
  2. Execute tasks in order, respecting dependencies
  3. Use XML `<file>` blocks with K-headers: `# K:GEN P4 {TID} SC{LINK} {ISO}`
  4. Track progress by updating task checkboxes in tasks.md
  5. You may delegate tasks to sub-agents for parallel work
  6. After each logical block, update state.json

### Validation (P5)
**Goal**: Verify implementation works correctly.
**How**:
  1. Run tests (e.g., `pytest`, `npm test`)
  2. Self-heal failures (max 5 attempts)
  3. Check coverage and linting
  4. Write `.kodro/validation_report.md`
  5. If critical failures remain, flag for user review

### Delivery (P6)
**Goal**: Finalize and document delivery.
**How**:
  1. Git commit with descriptive message
  2. Generate cost report
  3. Write `.kodro/delivery.md` manifest
  4. Display run instructions

---

## STATE UPDATE

After completing each phase:
```json
UPDATE .kodro/state.json:
  current_phase += 1
  phases.append({phase_number, status: "complete", timestamp_end: ISO8601})
```

If the phase has a gatekeeper:
```
[GATEKEEPER] "Review {artifact_path}. Press Enter to continue."
WAIT for user signal before proceeding.
```

---

## SUBAGENT HANDOFFS

You may delegate work to sub-agents. Suggested handoffs between phases:

| Current | Handoff To | Purpose |
|---------|-----------|---------|
| P1 Clarify | `/speckit.specify` | Create spec from clarified requirements |
| P2 Specify | `/speckit.tasks` | Generate task breakdown from spec |
| P3 Tasks | `/speckit.implement` | Execute implementation tasks |
| P4 Implement | validation agent | Run tests and verify |
| P5 Validate | delivery agent | Finalize and commit |

To hand off: `EXECUTE_COMMAND: speckit.<command> {args}`

---

## PROGRESS TRACKING

You should maintain a running todo/checklist during execution:
```
## Progress
- [x] Phase 1: Clarification questions answered
- [ ] Phase 2: spec.md written
- [ ] Phase 3: tasks.md generated
- [ ] Phase 4: Code implemented
- [ ] Phase 5: Validation passed
- [ ] Phase 6: Delivered
```

Update checkboxes as you complete work. This helps maintain context across turns.

---

## INTERACTIVE Q&A PATTERN

When you need to ask the user something, use this format:
```
## Question: {topic}
**Context**: {what we know so far}
**Recommended**: Option {X} — {brief reasoning}
| Option | Description |
|--------|-------------|
| A | {first choice} |
| B | {second choice} |
| C | {third choice} |
You can reply with a letter, "recommended" to accept, or your own answer.
```

Limit to 3-5 questions per phase. Prioritize scope > UX > technical details.

---

## CHANGES WORKFLOW (Post-Delivery)

If user requests changes after the pipeline is complete:
1. Read `.kodro/CHANGES.md`
2. Read current spec.md and tasks.md
3. Propose changes in a `.kodro/changes/` directory
4. Gatekeeper pause for approval
5. Implement approved changes
6. Re-run validation
7. Update delivery.md with change log

---

## GUIDELINES (not rigid rules)

- **No code before P4**: Focus on specification and planning first.
- **Read state.json** at the start of every turn.
- **Load only current phase context** — no need to load future phase modules.
- **Gatekeeper**: Pause after each phase for user review.
- **You ARE an assistant** — ask questions, adapt, use sub-agents, and update todos freely.
"""
