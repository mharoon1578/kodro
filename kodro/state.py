"""Atomic state management with resume and rollback capabilities."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from kodro.config import KodroConfig, PhaseState, PipelineState


class StateManager:
    """Handles atomic serialization and state transitions."""

    def __init__(self, config: KodroConfig) -> None:
        self.config = config
        self.state_path = config.state_file
        self._ensure_dir()

    def _ensure_dir(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, state: PipelineState) -> None:
        """Atomic write: temp file then rename."""
        state.last_updated = datetime.now(timezone.utc).isoformat()
        data = state.model_dump()
        data = self._serialize_paths(data)
        temp_path = Path(str(self.state_path) + ".tmp")
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        os.replace(temp_path, self.state_path)

    def load(self) -> PipelineState | None:
        """Load state if it exists and is valid."""
        if not self.state_path.exists():
            return None
        try:
            with open(self.state_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            return self._deserialize(raw)
        except (json.JSONDecodeError, KeyError, TypeError):
            return None

    def _serialize_paths(self, data: Any) -> Any:
        if isinstance(data, dict):
            return {k: str(v) if isinstance(v, Path) else self._serialize_paths(v) for k, v in data.items()}
        if isinstance(data, list):
            return [self._serialize_paths(i) for i in data]
        return data

    def _deserialize(self, raw: dict[str, Any]) -> PipelineState:
        """Reconstruct PipelineState from JSON dict."""
        if "project_path" in raw:
            raw["project_path"] = Path(raw["project_path"])
        if "spec_path" in raw and raw["spec_path"]:
            raw["spec_path"] = Path(raw["spec_path"])
        if "tasks_path" in raw and raw["tasks_path"]:
            raw["tasks_path"] = Path(raw["tasks_path"])
        if "phases" in raw:
            raw["phases"] = [PhaseState(**p) for p in raw["phases"]]
        return PipelineState(**raw)

    def initialize_state(self, project_path: Path, integration: Any, framework: Any) -> PipelineState:
        """Create fresh pipeline state."""
        now = datetime.now(timezone.utc).isoformat()
        state = PipelineState(
            project_path=project_path,
            integration=integration,
            framework=framework,
            created_at=now,
            last_updated=now,
        )
        self.save(state)
        return state

    def update_phase(self, state: PipelineState, phase: PhaseState) -> PipelineState:
        """Replace or append phase state."""
        existing = [p for p in state.phases if p.phase_number == phase.phase_number]
        if existing:
            idx = state.phases.index(existing[0])
            state.phases[idx] = phase
        else:
            state.phases.append(phase)
        state.current_phase = phase.phase_number
        self.save(state)
        return state

    def rollback(self, phases: int = 1) -> PipelineState | None:
        """Revert N phases atomically."""
        state = self.load()
        if not state:
            return None
        completed = [p for p in state.phases if p.status == "complete"]
        if not completed:
            return state
        to_rollback = min(phases, len(completed))
        for i in range(1, to_rollback + 1):
            target = state.phases[-i]
            target.status = "rolled_back"
            target.notes += f" [Rolled back at {datetime.now(timezone.utc).isoformat()}]"
        state.current_phase = max(0, state.current_phase - to_rollback)
        self.save(state)
        return state

    def reset(self) -> None:
        """Clear state file."""
        if self.state_path.exists():
            self.state_path.unlink()
