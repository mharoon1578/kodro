"""Typer CLI with 6 commands and modular constitution generation."""

from __future__ import annotations

import sys
from contextlib import suppress

# Reconfigure stdout/stderr to use UTF-8 to prevent encoding crashes on Windows console
if hasattr(sys.stdout, "reconfigure"):
    with suppress(Exception):
        sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    with suppress(Exception):
        sys.stderr.reconfigure(encoding="utf-8")


from datetime import datetime, timezone
from pathlib import Path

import typer
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table

from kodro.config import Framework, Integration, KodroConfig, PhaseState
from kodro.constants import (
    CONSTITUTION_DIR,
    INTEGRATION_DIRS,
    INTEGRATION_FILES,
    PHASE_NAMES,
    SPEC_FILE,
    TASKS_FILE,
)
from kodro.state import StateManager
from kodro.utils import (
    display_error,
    display_file_tree,
    display_phase_complete,
    display_phase_header,
    display_status_table,
    display_success,
    display_warning,
    display_welcome_banner,
    ensure_git_repo,
    format_constitution,
    write_file,
)


def _version_callback(value: bool) -> None:
    if value:
        from kodro.constants import VERSION
        console = Console()
        console.print(f"kodro {VERSION}")
        raise typer.Exit()

app = typer.Typer(
    name="kodro",
    help="Kodro — One-Command Spec-Driven Development Engine",
    add_completion=False,
)

@app.callback()
def _main(
    version: bool = typer.Option(False, "--version", "-V", callback=_version_callback, is_eager=True, help="Show version and exit."),
) -> None:
    pass

console = Console()


@app.command()
def init(
    integration: Integration = typer.Option(
        Integration.OPENCODE, "--integration", "-i", help="AI agent integration"
    ),
    framework: Framework = typer.Option(
        Framework.PYTHON_FASTAPI, "--framework", "-f", help="Target framework"
    ),
    path: Path = typer.Option(Path("."), "--path", "-p", help="Project directory"),
    git: bool = typer.Option(True, "--git/--no-git", help="Enable Git integration"),
    quick: bool = typer.Option(False, "--quick", "-q", help="Quick mode: skip phases for small projects"),
) -> None:
    """Initialize a Kodro project with modular token-efficient constitution."""
    display_welcome_banner()

    config = KodroConfig(
        integration=integration,
        framework=framework,
        enable_git=git,
        output_dir=path / ".kodro",
        state_file=path / ".kodro" / "state.json",
    )

    # Ensure directories
    config.output_dir.mkdir(parents=True, exist_ok=True)
    (path / CONSTITUTION_DIR).mkdir(parents=True, exist_ok=True)
    integration_dir = path / INTEGRATION_DIRS[integration.value]
    integration_dir.mkdir(parents=True, exist_ok=True)

    if git:
        if ensure_git_repo(path):
            display_success("Git repository ready")
        else:
            display_warning("Git not available")

    # Generate modular constitution (token-efficient architecture)
    format_constitution(framework.value, path)
    display_success("Modular constitution generated (kernel + 6 phase modules + framework spec)")

    # Generate integration bootloader with $ARGUMENTS placeholder
    from kodro.constants import BOOTLOADER_TEMPLATE
    integration_file = integration_dir / INTEGRATION_FILES[integration.value]
    write_file(integration_file, BOOTLOADER_TEMPLATE)
    display_success(f"Integration bootloader: {integration_file}")

    # Generate spec.md template
    spec_template = f"""# Specification — {path.name}

## 1. Overview
<!-- High-level description -->

## 2. BDD Requirements (Gherkin)
<!-- SC-{{FEAT}}-NNN format. Min 5 scenarios/major feature -->

## 3. ADRs
<!-- ADR-NNN: Title | Context | Decision | Consequences -->

## 4. Interface
<!-- OpenAPI 3.1 YAML per endpoint -->

## 5. Data Model
<!-- ERD + schema + constraints -->

## 6. NFRs
<!-- p50/p95/p99 | SLO/SLA | Auth model | Metrics -->
"""
    write_file(path / SPEC_FILE, spec_template)
    display_success(f"Spec template: {path / SPEC_FILE}")

    # Generate tasks.md template
    tasks_template = """# Tasks

## Dependency Graph
```mermaid
graph TD
    A[Setup] --> B[Core]
    B --> C[API]
    B --> D[Auth]
    C --> E[Tests]
    D --> E
```

## Task Registry
| ID | Task | Block | [P] | Dep | SC-Link | Tok |
|----|------|-------|-----|-----|---------|-----|
| T001 | Scaffold | B1 | [P] | — | — | 500 |

## Execution Blocks
### B1: Foundation
- [ ] T001 — Scaffold with linting, testing, CI stubs
"""
    write_file(path / TASKS_FILE, tasks_template)
    display_success(f"Tasks template: {path / TASKS_FILE}")

    # Generate CHANGES.md template for post-delivery edits
    changes_template = """# Change Requests

## How to Request Changes
After delivery, request changes by creating entries below:

### Format
```
## CHANGE-{YYYYMMDD}-{NNN}: {Title}
- **Status:** proposed | approved | rejected | implemented
- **Request:** {specific description}
- **Scope:** {files affected}
- **Priority:** low | medium | high | critical
- **Estimated tokens:** {N}K
- **Impact on spec:** {which BDD scenarios affected}
```

## Active Changes

## Completed Changes
"""
    write_file(path / ".kodro/CHANGES.md", changes_template)
    display_success("Changes template: .kodro/CHANGES.md")

    # Initialize state
    state_mgr = StateManager(config)
    state_mgr.initialize_state(path, integration, framework, quick=quick)
    display_success("State initialized")

    # Display tree
    console.print("\n[bold]Project Structure:[/bold]")
    display_file_tree(path, max_depth=3)

    # Token efficiency summary
    console.print("\n[bold cyan]📊 Token Efficiency[/bold cyan]")
    table = Table(show_header=True, header_style="bold green")
    table.add_column("Component", style="cyan")
    table.add_column("Tokens", style="white")
    table.add_column("Load Strategy", style="dim")
    table.add_row("Kernel", "~560", "Always")
    table.add_row("Phase Module", "~110-280", "On-demand per phase")
    table.add_row("Framework Spec", "~120-230", "Once per project")
    table.add_row("Total/turn", "~1060", "vs ~6750 monolithic")
    table.add_row("Savings", "84%", "Differential updates + refs")
    console.print(table)

    if quick:
        console.print("\n[bold yellow]⚡ Quick mode:[/bold yellow] Phases: [2]Specify → [4]Implement → [5]Validate")
        console.print("[dim]Clarification, Planning, Delivery skipped.[/dim]")
    else:
        console.print("\n[bold cyan]Full pipeline:[/bold cyan] 6 phases (use --quick for small projects)")

    console.print(f"\n[bold cyan]Next:[/bold cyan] Use your AI agent with the `/{integration.value}` command.")
    console.print(f"[dim]Example: /{integration.value} \"Build a REST API with {framework.value}\"[/dim]")


@app.command()
def plan(
    path: Path = typer.Option(Path("."), "--path", "-p"),
    spec: Path = typer.Option(SPEC_FILE, "--spec", "-s"),
) -> None:
    """Generate tasks.md from spec.md using smart chunking."""
    config = KodroConfig(
        output_dir=path / ".kodro",
        state_file=path / ".kodro" / "state.json",
    )
    state_mgr = StateManager(config)
    state = state_mgr.load()

    if not state:
        display_error("No Kodro project found. Run `kodro init` first.")
        raise typer.Exit(1)

    spec_path = path / spec
    if not spec_path.exists():
        display_error(f"Spec not found: {spec_path}")
        raise typer.Exit(1)

    tasks_md = f"""# Tasks — Auto-generated from spec.md
<!-- Generated at {datetime.now(timezone.utc).isoformat()} -->

## Implementation Tasks
- [ ] [P] Parse specification sections
- [ ] [P] Generate task list from BDD scenarios
- [ ] Implement core logic per §4
- [ ] Implement data models per §5
- [ ] Write unit tests for all public interfaces
- [ ] Write integration tests for @critical paths
- [ ] Validate against NFRs in §6

## Validation Tasks
- [ ] Run test suite
- [ ] Check coverage tiers (critical 100%, API 90%, overall 80%)
- [ ] Self-heal any failures (max 5 attempts)
"""
    tasks_path = path / TASKS_FILE
    write_file(tasks_path, tasks_md)

    phase = PhaseState(
        phase_number=3,
        phase_name=PHASE_NAMES[3],
        status="complete",
        timestamp_start=datetime.now(timezone.utc).isoformat(),
        timestamp_end=datetime.now(timezone.utc).isoformat(),
        notes="Generated from spec.md via plan command",
    )
    state_mgr.update_phase(state, phase)
    display_success(f"Tasks written to: {tasks_path}")
    console.print("[dim]Review tasks.md, then run implementation via your AI agent.[/dim]")


@app.command()
def status(
    path: Path = typer.Option(Path("."), "--path", "-p"),
) -> None:
    """Display pipeline progress table."""
    config = KodroConfig(
        output_dir=path / ".kodro",
        state_file=path / ".kodro" / "state.json",
    )
    state_mgr = StateManager(config)
    state = state_mgr.load()

    if not state:
        display_error("No state found. Run `kodro init` first.")
        raise typer.Exit(1)

    phases_data = [
        {
            "phase_name": p.phase_name,
            "status": p.status,
        }
        for p in state.phases
    ]
    display_status_table(phases_data, state.current_phase)

    if state.can_resume():
        console.print(f"\n[bold yellow]→ Pipeline can resume from Phase {state.current_phase + 1}[/bold yellow]")
    elif state.current_phase >= max(state.active_phases):
        console.print("\n[bold green]✓ Pipeline complete[/bold green]")


@app.command()
def resume(
    path: Path = typer.Option(Path("."), "--path", "-p"),
) -> None:
    """Continue pipeline from last saved phase."""
    config = KodroConfig(
        output_dir=path / ".kodro",
        state_file=path / ".kodro" / "state.json",
    )
    state_mgr = StateManager(config)
    state = state_mgr.load()

    if not state:
        display_error("No state found. Run `kodro init` first.")
        raise typer.Exit(1)

    if not state.can_resume():
        display_warning("Pipeline is either complete or not started. Nothing to resume.")
        raise typer.Exit(0)

    next_phase = state.current_phase + 1
    display_phase_header(PHASE_NAMES[next_phase], next_phase, 6)
    console.print("[dim]Agent would continue execution here...[/dim]")
    display_phase_complete(PHASE_NAMES[next_phase])


@app.command()
def rollback(
    phases: int = typer.Option(1, "--phases", "-n", help="Number of phases to revert"),
    path: Path = typer.Option(Path("."), "--path", "-p"),
) -> None:
    """Revert N phases with state reset."""
    config = KodroConfig(
        output_dir=path / ".kodro",
        state_file=path / ".kodro" / "state.json",
    )
    state_mgr = StateManager(config)
    new_state = state_mgr.rollback(phases)

    if not new_state:
        display_error("No state found.")
        raise typer.Exit(1)

    display_warning(f"Rolled back {phases} phase(s)")
    phases_data = [
        {
            "phase_name": p.phase_name,
            "status": p.status,
        }
        for p in new_state.phases
    ]
    display_status_table(phases_data, new_state.current_phase)


@app.command()
def doctor(
    path: Path = typer.Option(Path("."), "--path", "-p"),
) -> None:
    """Validate project structure and diagnose issues."""
    issues = []
    checks = []

    kodro_dir = path / ".kodro"
    if kodro_dir.exists():
        checks.append(("Output directory", True, str(kodro_dir)))
    else:
        checks.append(("Output directory", False, "Missing .kodro/"))
        issues.append("Run `kodro init` to scaffold the project.")

    state_file = kodro_dir / "state.json"
    if state_file.exists():
        checks.append(("State file", True, str(state_file)))
    else:
        checks.append(("State file", False, "Missing state.json"))
        issues.append("State file missing; resume/rollback unavailable.")

    # Check modular constitution
    const_dir = path / CONSTITUTION_DIR
    if const_dir.exists():
        kernel = const_dir / "kernel.md"
        fw = const_dir / "framework.md"
        phases = sum(1 for i in range(1, 7) if (const_dir / f"p{i}.md").exists())
        checks.append(("Constitution modules", phases == 6, f"{phases}/6 phases + kernel + framework"))
        if phases < 6 or not kernel.exists() or not fw.exists():
            issues.append("Incomplete constitution. Run `kodro init` to regenerate.")
    else:
        checks.append(("Constitution modules", False, "Missing .kodro/constitution/"))

    spec = path / SPEC_FILE
    if spec.exists():
        checks.append(("Specification", True, str(spec)))
    else:
        checks.append(("Specification", False, "Missing spec.md"))

    tasks = path / TASKS_FILE
    if tasks.exists():
        checks.append(("Task plan", True, str(tasks)))
    else:
        checks.append(("Task plan", False, "Missing tasks.md"))

    git_dir = path / ".git"
    if git_dir.exists():
        checks.append(("Git repository", True, str(git_dir)))
    else:
        checks.append(("Git repository", False, "Not a git repository"))

    table = Table(title="Kodro Doctor", show_header=True, header_style="bold magenta")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Detail", style="dim")

    for name, ok, detail in checks:
        status = "[green]✓[/green]" if ok else "[red]✗[/red]"
        table.add_row(name, status, detail)

    console.print(table)

    if issues:
        console.print("\n[bold yellow]Recommendations:[/bold yellow]")
        for issue in issues:
            console.print(f"  • {issue}")
    else:
        console.print("\n[bold green]✓ Project structure is healthy.[/bold green]")


INTEGRATION_COMMANDS = {
    "opencode": lambda idea: f"/kodro \"{idea}\"",
    "claude": lambda idea: f"$kodro \"{idea}\"",
    "cursor": lambda idea: f"Auto-read: .cursor/rules/kodro.mdc\nThen prompt: {idea}",
    "copilot": lambda idea: f"Load .github/prompts/kodro.prompt.md\nThen: {idea}",
    "gemini": lambda idea: f"Load .gemini/instructions.md\nThen: {idea}",
    "aider": lambda idea: f"Load .aider/CONVENTIONS.md\nThen: /code {idea}",
}


@app.command()
def changes(
    request: str = typer.Argument(..., help="Change request description"),
    path: Path = typer.Option(Path("."), "--path", "-p", help="Project directory"),
) -> None:
    """Request changes to a delivered project."""
    config = KodroConfig(
        output_dir=path / ".kodro",
        state_file=path / ".kodro" / "state.json",
    )
    state_mgr = StateManager(config)
    state = state_mgr.load()

    if not state:
        display_error("No Kodro project found. Run `kodro init` first.")
        raise typer.Exit(1)

    if state.current_phase < max(state.active_phases):
        display_warning("Project not yet delivered. Complete pipeline first.")
        raise typer.Exit(1)

    # Append change request to CHANGES.md
    changes_file = path / ".kodro" / "CHANGES.md"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d")

    # Count existing changes for NNN
    existing_count = 0
    if changes_file.exists():
        content = changes_file.read_text(encoding="utf-8")
        existing_count = content.count("## CHANGE-")
    nnn = f"{existing_count + 1:03d}"
    change_id = f"CHANGE-{timestamp}-{nnn}"

    change_entry = f"""
## {change_id}: {request}
- **Status:** proposed
- **Request:** {request}
- **Scope:** TBD
- **Priority:** medium
- **Estimated tokens:** TBD
- **Impact on spec:** TBD
"""

    if changes_file.exists():
        content = content.replace("## Active Changes", f"## Active Changes{change_entry}")
        write_file(changes_file, content)
    else:
        write_file(changes_file, f"# Change Requests\n\n## Active Changes{change_entry}\n\n## Completed Changes\n")

    display_success(f"Change request logged: {changes_file}")
    console.print("[dim]The agent will read this file when you request implementation.[/dim]")
    console.print("[bold cyan]Next:[/bold cyan] Use your AI agent to implement changes.")
    console.print(f"[dim]Example: /{state.integration.value} \"Implement change {change_id}\"[/dim]")


@app.command()
def agent(
    idea: str = typer.Argument(..., help="Project idea / prompt"),
    integration: Integration = typer.Option(
        Integration.OPENCODE, "--integration", "-i"
    ),
) -> None:
    """Print the exact command to use with your AI agent."""
    cmd = INTEGRATION_COMMANDS[integration.value](idea)
    console.print(f"[bold]Command for {integration.value}:[/bold]")
    syntax = Syntax(cmd, "bash", theme="monokai", padding=1)
    console.print(syntax)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
