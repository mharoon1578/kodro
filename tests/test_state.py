"""Tests for atomic state management."""

from __future__ import annotations

from pathlib import Path

import pytest

from kodro.config import Framework, Integration, KodroConfig, PhaseState
from kodro.state import StateManager


@pytest.fixture
def tmp_config(tmp_path: Path) -> KodroConfig:
    return KodroConfig(
        output_dir=tmp_path / ".kodro",
        state_file=tmp_path / ".kodro" / "state.json",
    )


def test_state_initialization(tmp_config: KodroConfig) -> None:
    mgr = StateManager(tmp_config)
    state = mgr.initialize_state(
        Path("/tmp/project"), Integration.CURSOR, Framework.REACT_TYPESCRIPT
    )
    assert state.integration == Integration.CURSOR
    assert state.framework == Framework.REACT_TYPESCRIPT
    assert state.current_phase == 0


def test_load_save_roundtrip(tmp_config: KodroConfig) -> None:
    mgr = StateManager(tmp_config)
    original = mgr.initialize_state(Path("/tmp/proj"), Integration.AIDER, Framework.GO_GIN)
    phase = PhaseState(phase_number=1, phase_name="Clarification", status="complete")
    mgr.update_phase(original, phase)

    loaded = mgr.load()
    assert loaded is not None
    assert loaded.current_phase == 1
    assert loaded.phases[0].status == "complete"


def test_resume_detection(tmp_config: KodroConfig) -> None:
    mgr = StateManager(tmp_config)
    state = mgr.initialize_state(Path("/tmp/proj"), Integration.OPENCODE, Framework.PYTHON_FASTAPI)
    assert not state.can_resume()
    state.current_phase = 2
    assert state.can_resume()
