from __future__ import annotations
import os
import re
import subprocess
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree
from rich import box
from rich.rule import Rule
from rich.text import Text
from rich.markdown import Markdown

console = Console()

# ASCII Art
KODRO_LOGO = """
    ██╗  ██╗ ██████╗ ██████╗ ██████╗  ██████╗ 
    ██║ ██╔╝██╔═══██╗██╔══██╗██╔══██╗██╔═══██╗
    █████╔╝ ██║   ██║██║  ██║██████╔╝██║   ██║
    ██╔═██╗ ██║   ██║██║  ██║██╔══██╗██║   ██║
    ██║  ██╗╚██████╔╝██████╔╝██║  ██║╚██████╔╝
    ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ 
"""

PHASE_ASCII = {
    "clarify": "❓ CLARIFY",
    "specify": "📝 SPECIFY",
    "architect": "🏛️  ARCHITECT",
    "schedule": "📋 SCHEDULE",
    "implement": "💻 IMPLEMENT",
    "verify": "✅ VERIFY",
}

def ensure_dir(path: Path) -> Path:
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)
    return path

def write_file(path: Path, content: str, safe: bool = False) -> None:
    """Write file with optional safe mode confirmation."""
    if safe and path.exists():
        console.print(f"[yellow]⚠️  File exists:[/yellow] {path}")
        if not console.input("[bold yellow]Overwrite? [y/N]:[/bold yellow] ").lower().startswith("y"):
            console.print("[dim]↳ Skipped.[/dim]")
            return
    ensure_dir(path.parent)
    temp_file = path.with_suffix(path.suffix + ".tmp")
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(content)
    temp_file.replace(path)
    console.print(f"[green]✓[/green] [dim]{path}[/dim]")

def read_file(path: Path) -> str:
    """Read file contents."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def parse_xml_files(content: str) -> list[dict]:
    """Parse <file path="...">...</file> blocks from LLM output."""
    pattern = r'<file\s+path="([^"]+)"(?:\s+is_new="(true|false)")?>(.*?)</file>'
    matches = re.findall(pattern, content, re.DOTALL)
    files = []
    for path_str, is_new_str, content_str in matches:
        files.append({
            "path": path_str.strip(),
            "content": content_str.strip(),
            "is_new": is_new_str.lower() == "true" if is_new_str else True,
        })
    return files

def parse_checkbox_tasks(content: str) -> list[dict]:
    """Parse markdown checkbox tasks."""
    pattern = r'-\s*\[(.?)\]\s*(.*?)(?:\n|$)'
    tasks = []
    for i, match in enumerate(re.finditer(pattern, content)):
        bracket_content = match.group(1).strip()
        desc = match.group(2).strip()
        completed = "x" in bracket_content
        parallel = "P" in bracket_content
        tasks.append({
            "id": f"T{i+1:03d}",
            "description": desc,
            "completed": completed,
            "parallel": parallel,
        })
    return tasks

def update_checkbox_task(content: str, task_id: str, completed: bool = True) -> str:
    """Update a specific checkbox in markdown content."""
    pattern = rf'(-\s*\[.\]\s*)({re.escape(task_id)}:.*?)(?:\n|$)'
    replacement = rf'- [{"x" if completed else " "}] \2\n'
    return re.sub(pattern, replacement, content)

def get_file_tree(root: Path, max_depth: int = 3) -> str:
    """Generate ASCII tree of project files."""
    lines = []
    for path in sorted(root.rglob("*")):
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        depth = len(path.relative_to(root).parts) - 1
        if depth <= max_depth:
            indent = "  " * depth
            icon = "📁" if path.is_dir() else "📄"
            lines.append(f"{indent}{icon} {path.name}")
    return "\n".join(lines)

def run_command(cmd: list[str], cwd: Optional[Path] = None, timeout: int = 60) -> tuple[int, str, str]:
    """Run shell command safely."""
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "⏱️  Command timed out"
    except Exception as e:
        return -1, "", str(e)

def git_commit(project_path: Path, message: str) -> bool:
    """Stage all changes and commit."""
    try:
        subprocess.run(["git", "add", "-A"], cwd=project_path, check=True)
        subprocess.run(["git", "commit", "-m", message], cwd=project_path, check=True)
        console.print(f"[green]✓[/green] [dim]Git commit:[/dim] {message[:50]}")
        return True
    except subprocess.CalledProcessError:
        return False

# ── Modular Constitution Loader (Token-efficient) ──

def load_constitution_module(project_path: Path, module_name: str) -> str:
    """Load a modular constitution file. Returns empty string if missing."""
    module_path = project_path / ".kodro" / "constitution" / f"{module_name}.md"
    if module_path.exists():
        return module_path.read_text(encoding="utf-8")
    return ""

def load_phase_module(project_path: Path, phase_number: int) -> str:
    """Load phase-specific instructions on demand."""
    from kodro.constants import PHASE_NAMES
    content = load_constitution_module(project_path, f"p{phase_number}")
    if not content:
        return f"# K:P{phase_number}-{PHASE_NAMES.get(phase_number, 'Unknown')}\n# Module not found. Proceed with kernel defaults."
    return content

def load_framework_spec(project_path: Path) -> str:
    """Load framework micro-spec."""
    return load_constitution_module(project_path, "framework")

def assemble_agent_context(project_path: Path, phase_number: int) -> str:
    """Assemble minimal context: kernel + current phase + framework."""
    kernel = load_constitution_module(project_path, "kernel")
    phase = load_phase_module(project_path, phase_number)
    framework = load_framework_spec(project_path)
    return f"{kernel}\n\n{phase}\n\n{framework}"

# ── Additional helpers ──

def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Calculate USD cost based on model rates."""
    from kodro.constants import MODEL_COSTS
    rates = MODEL_COSTS.get(model, (0.005, 0.015))
    input_cost = (input_tokens / 1000) * rates[0]
    output_cost = (output_tokens / 1000) * rates[1]
    return round(input_cost + output_cost, 6)

def chunk_text(text: str, max_chars: int = 2000) -> list[str]:
    """Split text into smart chunks by section headers."""
    lines = text.splitlines()
    chunks = []
    current = []
    current_len = 0
    for line in lines:
        line_len = len(line) + 1
        if line.startswith("## ") and current:
            chunks.append("\n".join(current))
            current = [line]
            current_len = line_len
        elif current_len + line_len > max_chars and current:
            chunks.append("\n".join(current))
            current = [line]
            current_len = line_len
        else:
            current.append(line)
            current_len += line_len
    if current:
        chunks.append("\n".join(current))
    return chunks

def ensure_git_repo(path: Path) -> bool:
    """Initialize git repo if none exists."""
    if (path / ".git").exists():
        return True
    try:
        subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def format_constitution(framework: str, project_path: Path) -> str:
    """Generate modular constitution files for the project."""
    from kodro.constants import (
        CONSTITUTION_DIR,
        FRAMEWORK_TEMPLATES,
        KERNEL_TEMPLATE,
        PHASE_TEMPLATES,
    )
    # Write kernel
    write_file(project_path / CONSTITUTION_DIR / "kernel.md", KERNEL_TEMPLATE)
    # Write phase modules
    for num, content in PHASE_TEMPLATES.items():
        write_file(project_path / CONSTITUTION_DIR / f"p{num}.md", content)
    # Write framework spec
    fw_content = FRAMEWORK_TEMPLATES.get(framework, "# No framework-specific rules.")
    write_file(project_path / CONSTITUTION_DIR / "framework.md", fw_content)
    return "Constitution modules generated."

# Display Functions
def display_panel(title: str, content: str, style: str = "blue") -> None:
    """Display rich panel."""
    console.print(Panel(content, title=title, border_style=style))

def display_code(path: str, content: str, language: str = "python") -> None:
    """Display syntax-highlighted code."""
    syntax = Syntax(content, language, theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title=f"📄 {path}", border_style="green"))

def display_success(message: str) -> None:
    console.print(f"[bold green]✓ {message}[/bold green]")

def display_warning(message: str) -> None:
    console.print(f"[bold yellow]⚠️  {message}[/bold yellow]")

def display_error(message: str) -> None:
    console.print(f"[bold red]✗ {message}[/bold red]")

def display_info(message: str) -> None:
    console.print(f"[bold blue]ℹ️  {message}[/bold blue]")

def display_phase_header(phase_name: str, phase_number: int, total_phases: int) -> None:
    """Display phase header with ASCII art."""
    ascii_art = PHASE_ASCII.get(phase_name.lower(), f"📍 {phase_name.upper()}")
    progress = f"[{phase_number}/{total_phases}]"
    console.print()
    console.print(Rule(f"[bold cyan]{ascii_art} {progress}[/bold cyan]", style="cyan"))
    console.print()

def display_phase_complete(phase_name: str) -> None:
    """Display phase completion."""
    console.print(f"[bold green]✅ {phase_name.upper()} COMPLETE[/bold green]")
    console.print()

def display_welcome_banner() -> None:
    """Display welcome banner."""
    from kodro.constants import VERSION
    console.print("[bold cyan]" + KODRO_LOGO + "[/bold cyan]")
    console.print(f"[bold green]🔨 Kodro v{VERSION} — One-command Spec-Driven Development[/bold green]")
    console.print("[dim]Type `kodro --help` for commands[/dim]")
    console.print()

def display_file_tree(root: Path, max_depth: int = 3) -> None:
    """Display rich tree of project structure."""
    tree = Tree("📦 Project Structure")
    def add_to_tree(tree_node, current_path: Path, current_depth: int):
        if current_depth > max_depth:
            return
        try:
            items = sorted(current_path.iterdir())
        except PermissionError:
            return
        for item in items:
            if item.name.startswith(".") or item.name == "__pycache__":
                continue
            if item.is_dir():
                branch = tree_node.add(f"📁 [bold cyan]{item.name}[/bold cyan]")
                add_to_tree(branch, item, current_depth + 1)
            else:
                tree_node.add(f"📄 [dim]{item.name}[/dim]")
    add_to_tree(tree, root, 0)
    console.print(tree)

def display_status_table(phases: list[dict], current_phase: int) -> None:
    """Display status table."""
    table = Table(title="[bold cyan]📊 Pipeline Status[/bold cyan]", box=box.ROUNDED, border_style="cyan")
    table.add_column("Phase", style="white", width=15)
    table.add_column("Status", style="white", width=12)
    status_colors = {"pending": "dim", "running": "yellow", "completed": "green", "failed": "red", "paused": "blue"}
    for i, phase in enumerate(phases):
        status = phase.get("status", "pending")
        color = status_colors.get(status, "white")
        marker = ">>>" if i == current_phase else "   "
        table.add_row(f"{marker} {phase.get('phase_name', 'Unknown')}", f"[{color}]{status}[/{color}]")
    console.print(table)

def display_todo_summary(tasks: list[dict]) -> None:
    """Display todo list summary."""
    table = Table(title="[bold cyan]📋 Task Breakdown[/bold cyan]", box=box.ROUNDED, border_style="cyan")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Task", style="white", width=40)
    table.add_column("Status", style="white", width=12)
    table.add_column("Type", style="white", width=10)
    for task in tasks:
        status = "[green]✓ Done[/green]" if task["completed"] else "[yellow]○ Pending[/yellow]"
        task_type = "[blue]⟡ Parallel[/blue]" if task["parallel"] else "[dim]Sequential[/dim]"
        desc = task["description"]
        if len(desc) > 40:
            desc = desc[:38] + ".."
        table.add_row(task["id"], desc, status, task_type)
    console.print(table)

def display_gatekeeper(phase_name: str, artifact_path: str) -> bool:
    """Display gatekeeper pause with explicit Continue command."""
    console.print()
    console.print("╔" + "═" * 68 + "╗")
    console.print("║" + " " * 15 + "🛡️  GATEKEEPER CHECKPOINT" + " " * 22 + "║")
    console.print("╠" + "═" * 68 + "╣")
    console.print(f"║  Phase: {phase_name:<55}║")
    console.print(f"║  Artifact: {artifact_path:<53}║")
    console.print("╠" + "═" * 68 + "╣")
    console.print("║  Review the generated files before continuing.                     ║")
    console.print("║                                                                    ║")
    console.print("║  [bold green]Type 'Continue' and press Enter to proceed[/bold green]                     ║")
    console.print("║  [bold yellow]Type 'review' to pause and inspect[/bold yellow]                             ║")
    console.print("╚" + "═" * 68 + "╝")
    console.print()
    response = console.input("[bold green]Your choice: [/bold green] ")
    return response.strip().lower() == "continue"

def display_self_heal_attempt(attempt: int, max_attempts: int, error: str) -> None:
    """Display self-healing attempt."""
    console.print()
    console.print(f"[bold yellow]🔄 Healing Attempt {attempt}/{max_attempts}[/bold yellow]")
    err_text = f"[red]{error[:200]}[/red]..." if len(error) > 200 else f"[red]{error}[/red]"
    console.print(Panel(err_text, title="[bold red]Test Failure[/bold red]", border_style="red"))

def display_test_result(passed: bool, exit_code: int, coverage: Optional[float] = None) -> None:
    """Display test result."""
    icon = "✅" if passed else "❌"
    style = "green" if passed else "red"
    status = "PASSED" if passed else "FAILED"
    table = Table(show_header=False, box=box.ROUNDED, border_style=style)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")
    table.add_row(f"{icon} Status", status)
    table.add_row("🔢 Exit Code", str(exit_code))
    if coverage is not None:
        cov_pct = coverage * 100
        cov_color = "green" if cov_pct >= 80 else "yellow" if cov_pct >= 60 else "red"
        table.add_row("📊 Coverage", f"[{cov_color}]{cov_pct:.1f}%[/{cov_color}]")
    console.print(Panel(table, title=f"[bold {style}]Test Results[/bold {style}]", border_style=style))


def display_next_steps(project_path: Path, framework: str) -> None:
    """Display how to run the project after delivery."""
    console.print()
    console.print("[bold cyan]╔" + "═" * 68 + "╗[/bold cyan]")
    console.print("[bold cyan]║" + " " * 20 + "🚀 PROJECT DELIVERED" + " " * 25 + "║[/bold cyan]")
    console.print("[bold cyan]╠" + "═" * 68 + "╣[/bold cyan]")

    # Framework-specific run instructions
    run_cmds = {
        "react-typescript": [
            ("Install", "npm install"),
            ("Run dev", "npm run dev"),
            ("Build", "npm run build"),
            ("Test", "npm test"),
        ],
        "python-fastapi": [
            ("Install", "pip install -r requirements.txt"),
            ("Run", "uvicorn main:app --reload"),
            ("Test", "pytest tests/ -v"),
        ],
        "go-gin": [
            ("Install", "go mod download"),
            ("Run", "go run main.go"),
            ("Test", "go test ./..."),
        ],
        "ruby-rails": [
            ("Install", "bundle install"),
            ("Setup DB", "rails db:setup"),
            ("Run", "rails server"),
            ("Test", "rspec"),
        ],
        "rust-axum": [
            ("Build", "cargo build --release"),
            ("Run", "cargo run"),
            ("Test", "cargo test"),
        ],
        "vue-typescript": [
            ("Install", "npm install"),
            ("Run dev", "npm run dev"),
            ("Build", "npm run build"),
        ],
        "python-django": [
            ("Install", "pip install -r requirements.txt"),
            ("Migrate", "python manage.py migrate"),
            ("Run", "python manage.py runserver"),
            ("Test", "pytest"),
        ],
    }

    cmds = run_cmds.get(framework, [("Run", "See README.md for instructions")])

    console.print("[bold cyan]║  [bold white]How to run:[/bold white]" + " " * 54 + "║[/bold cyan]")
    for label, cmd in cmds:
        console.print(f"[bold cyan]║    [/bold cyan][green]{label:<10}[/green] [dim]$[/dim] {cmd:<50}[bold cyan]║[/bold cyan]")

    console.print("[bold cyan]╠" + "═" * 68 + "╣[/bold cyan]")
    console.print("[bold cyan]║  [bold white]Project location:[/bold white]" + " " * 47 + "║[/bold cyan]")
    console.print(f"[bold cyan]║    [/bold cyan][blue]{str(project_path)}[/blue]" + " " * (55 - len(str(project_path))) + "[bold cyan]║[/bold cyan]")
    console.print("[bold cyan]║  [bold white]Key files:[/bold white]" + " " * 54 + "║[/bold cyan]")
    console.print("[bold cyan]║    [/bold cyan][dim]README.md[/dim]     — Project overview" + " " * 25 + "[bold cyan]║[/bold cyan]")
    console.print("[bold cyan]║    [/bold cyan][dim]delivery.md[/dim]  — Delivery manifest" + " " * 24 + "[bold cyan]║[/bold cyan]")
    console.print("[bold cyan]║    [/bold cyan][dim]spec.md[/dim]     — Specification" + " " * 28 + "[bold cyan]║[/bold cyan]")
    console.print("[bold cyan]║    [/bold cyan][dim]src/[/dim]         — Source code" + " " * 31 + "[bold cyan]║[/bold cyan]")
    console.print("[bold cyan]╠" + "═" * 68 + "╣[/bold cyan]")
    console.print("[bold cyan]║  [bold yellow]Want changes?[/bold yellow] See .kodro/CHANGES.md for how to request edits" + " " * 8 + "║[/bold cyan]")
    console.print("[bold cyan]╚" + "═" * 68 + "╝[/bold cyan]")
    console.print()


def display_changes_guide() -> None:
    """Display the changes workflow guide."""
    guide = """
# Making Changes After Delivery

## Option 1: Quick Fix (Single File)
```bash
# Edit the file directly, then run validation
kodro doctor -p /path/to/project
```

## Option 2: Request Agent Changes
```bash
# Create a changes request
kodro changes -p /path/to/project "Add user authentication to login page"
```

The agent will:
1. Read current spec.md and tasks.md
2. Propose changes in .kodro/changes/
3. Wait for your approval (gatekeeper)
4. Implement approved changes
5. Re-run validation

## Option 3: Full Regeneration
```bash
# Rollback to any phase and regenerate
kodro rollback -p /path/to/project --phases 2
kodro resume -p /path/to/project
```

## Change Proposal Format
When requesting changes, be specific:
- ❌ "Make it better"
- ✅ "Add OAuth2 Google login to the /auth/google endpoint"
- ✅ "Change database from SQLite to PostgreSQL with connection pooling"
- ✅ "Add real-time WebSocket notifications for task updates"

## Files the Agent Reads for Changes
| File | Purpose |
|------|---------|
| .kodro/spec.md | Current specification |
| .kodro/tasks.md | Current task registry |
| .kodro/delivery.md | What was originally built |
| .kodro/CHANGES.md | Your change requests |

## Cost Tracking
Changes consume tokens based on scope:
- Minor (1 file): ~500 tokens
- Moderate (new feature): ~2K tokens
- Major (architecture change): ~5K tokens
"""
    console.print(Markdown(guide))
