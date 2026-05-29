"""Tests for Pydantic configuration models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from kodro.config import Framework, Integration, KodroConfig, PhaseState, PipelineState


def test_default_config() -> None:
    config = KodroConfig()
    assert config.integration == Integration.OPENCODE
    assert config.framework == Framework.PYTHON_FASTAPI
    assert config.temperature == 0.7


def test_framework_enum() -> None:
    assert Framework.REACT_TYPESCRIPT.value == "react-typescript"
    assert len(Framework) == 7


def test_integration_enum() -> None:
    assert Integration.CLAUDE.value == "claude"
    assert len(Integration) == 6


def test_temperature_boundary() -> None:
    with pytest.raises(ValidationError):
        KodroConfig(temperature=2.1)
    with pytest.raises(ValidationError):
        KodroConfig(temperature=-0.1)
    config = KodroConfig(temperature=1.5)
    assert config.temperature == 1.5


def test_pipeline_state_resume() -> None:
    from pathlib import Path
    state = PipelineState(
        project_path=Path("."),
        integration=Integration.OPENCODE,
        framework=Framework.GO_GIN,
        current_phase=3,
    )
    assert state.can_resume() is True
    state.current_phase = 6
    assert state.can_resume() is False


def test_phase_state_model() -> None:
    phase = PhaseState(phase_number=2, phase_name="Specification", status="complete")
    assert phase.phase_number == 2
    assert phase.cost_usd == 0.0
