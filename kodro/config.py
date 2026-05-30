"""Pydantic v2 configuration models for Kodro."""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator


class Framework(str, Enum):
    """Supported framework constitutions."""

    REACT_TYPESCRIPT = "react-typescript"
    PYTHON_FASTAPI = "python-fastapi"
    GO_GIN = "go-gin"
    RUBY_RAILS = "ruby-rails"
    RUST_AXUM = "rust-axum"
    VUE_TYPESCRIPT = "vue-typescript"
    PYTHON_DJANGO = "python-django"


class Integration(str, Enum):
    """Supported AI agent integrations."""

    OPENCODE = "opencode"
    CLAUDE = "claude"
    CURSOR = "cursor"
    COPILOT = "copilot"
    GEMINI = "gemini"
    AIDER = "aider"


class PhaseState(BaseModel):
    """Tracking for an individual pipeline phase."""

    phase_number: int = Field(..., ge=1, le=6)
    phase_name: str
    status: str = "pending"
    cost_usd: float = 0.0
    tokens_used: int = 0
    timestamp_start: str | None = None
    timestamp_end: str | None = None
    notes: str = ""


class PipelineState(BaseModel):
    """Serializable state for resume and rollback operations."""

    project_path: Path
    current_phase: int = 0
    phases: list[PhaseState] = Field(default_factory=list)
    integration: Integration
    framework: Framework
    spec_path: Path | None = None
    tasks_path: Path | None = None
    git_commit_hash: str | None = None
    created_at: str = ""
    last_updated: str = ""
    active_phases: list[int] = Field(default_factory=lambda: [1, 2, 3, 4, 5, 6])

    def can_resume(self) -> bool:
        """Determine if the pipeline can be resumed from current state."""
        return self.current_phase > 0 and self.current_phase < max(self.active_phases)

    def is_quick(self) -> bool:
        """Check if running in quick mode (subset of phases)."""
        return len(self.active_phases) < 6

    def get_completed_phases(self) -> list[PhaseState]:
        """Return phases marked as complete."""
        return [p for p in self.phases if p.status == "complete"]


class KodroConfig(BaseModel):
    """Main user-facing configuration."""

    project_name: str = "kodro-project"
    integration: Integration = Integration.OPENCODE
    framework: Framework = Framework.PYTHON_FASTAPI
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    max_tokens: int = 4000
    enable_git: bool = True
    enable_cost_tracking: bool = True
    gatekeeper_pause: bool = True
    self_heal_attempts: int = 5
    chunk_size: int = 2000
    output_dir: Path = Path(".kodro")
    state_file: Path = Path(".kodro/state.json")
    active_phases: list[int] = Field(default_factory=lambda: [1, 2, 3, 4, 5, 6])

    @field_validator("temperature")
    @classmethod
    def validate_temperature(cls, v: float) -> float:
        if not 0.0 <= v <= 2.0:
            raise ValueError("Temperature must be between 0.0 and 2.0")
        return v

    def model_dump_json_safe(self) -> dict[str, Any]:
        """Serialize with Path objects converted to strings."""
        data = self.model_dump()
        data["output_dir"] = str(data["output_dir"])
        data["state_file"] = str(data["state_file"])
        return data
