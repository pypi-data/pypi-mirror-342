# File: trieye/trieye/schemas.py
from typing import Any

import numpy as np
from pydantic import BaseModel, ConfigDict, Field

# --- Core Data Schemas ---

arbitrary_types_config = ConfigDict(arbitrary_types_allowed=True)


class CheckpointData(BaseModel):
    """Pydantic model defining the structure of saved checkpoint data."""

    model_config = arbitrary_types_config

    run_name: str
    global_step: int = Field(..., ge=0)
    episodes_played: int = Field(..., ge=0)
    total_simulations_run: int = Field(..., ge=0)
    # Generic dictionaries for state dicts
    model_state_dict: dict[str, Any] = Field(default_factory=dict)
    optimizer_state_dict: dict[str, Any] = Field(default_factory=dict)
    # State specific to the TrieyeActor itself
    actor_state: dict[str, Any] = Field(default_factory=dict)
    # Optional user-provided data (e.g., application-specific configs)
    user_data: dict[str, Any] = Field(default_factory=dict)
    # Store relevant configs directly in checkpoint for easier inspection/resumption
    model_config_dict: dict[str, Any] = Field(default_factory=dict)
    env_config_dict: dict[str, Any] = Field(default_factory=dict)


class BufferData(BaseModel):
    """
    Pydantic model defining the structure of saved buffer data.
    Stores a list of arbitrary experience objects. The user application
    is responsible for interpreting the content.
    """

    model_config = arbitrary_types_config
    buffer_list: list[Any]


class LoadedTrainingState(BaseModel):
    """Pydantic model representing the fully loaded state."""

    model_config = arbitrary_types_config
    checkpoint_data: CheckpointData | None = None
    buffer_data: BufferData | None = None


# --- Statistics Schemas ---


class RawMetricEvent(BaseModel):
    """Structure for raw metric data points sent to the collector."""

    name: str = Field(
        ...,
        description="Identifier for the raw event (e.g., 'loss/policy', 'episode_end')",
    )
    value: float | int = Field(..., description="The numerical value of the event.")
    global_step: int = Field(
        ..., description="The training step associated with this event."
    )
    timestamp: float | None = Field(
        default=None, description="Optional timestamp of the event occurrence."
    )
    context: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional additional context (e.g., worker_id, score, length).",
    )

    def is_valid(self) -> bool:
        """Checks if the value is finite."""
        # Cast numpy bool_ to standard bool
        return bool(np.isfinite(self.value))


class LogContext(BaseModel):
    """Context information passed to the StatsProcessor during logging."""

    latest_step: int
    last_log_time: float  # Timestamp of the last time processor ran
    current_time: float  # Timestamp of the current processor run
    event_timestamps: dict[
        str, list[tuple[float, int]]
    ]  # event_name -> list of (timestamp, global_step)
    latest_values: dict[str, tuple[int, float]]  # event_name -> (global_step, value)


# Rebuild models
CheckpointData.model_rebuild(force=True)
BufferData.model_rebuild(force=True)
LoadedTrainingState.model_rebuild(force=True)
RawMetricEvent.model_rebuild(force=True)
LogContext.model_rebuild(force=True)
