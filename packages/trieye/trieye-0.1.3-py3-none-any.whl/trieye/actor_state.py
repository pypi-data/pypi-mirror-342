# File: trieye/trieye/actor_state.py
import logging
import time
from collections import defaultdict, deque
from collections.abc import Iterable
from typing import Any

from .schemas import LogContext, RawMetricEvent

logger = logging.getLogger(__name__)


class ActorState:
    """Manages the internal state buffers and counters for the TrieyeActor."""

    def __init__(self) -> None:
        # --- State for Stats ---
        # Buffer: step -> event_name -> list of events at that step
        self._raw_data_buffer: dict[int, dict[str, list[RawMetricEvent]]] = defaultdict(
            lambda: defaultdict(list)
        )
        # Latest value seen for each event name: event_name -> (step, value)
        self._latest_values: dict[str, tuple[int, float]] = {}
        # Timestamp history for rate calculation: event_name -> deque[(timestamp, step)]
        self._event_timestamps: dict[str, deque[tuple[float, int]]] = defaultdict(
            lambda: deque(maxlen=200)  # Keep last 200 timestamps per event
        )
        self._last_processed_step: int = -1
        self._last_processed_time: float = time.monotonic()
        # Track last log time per metric for time-based frequency: metric_name -> timestamp
        self._last_log_time_per_metric: dict[str, float] = {}

    def add_event(self, event: RawMetricEvent) -> None:
        """Adds a single validated event to the internal buffers."""
        # Basic validation (caller should ensure validity)
        if not isinstance(event, RawMetricEvent):
            logger.warning(f"Attempted to add non-RawMetricEvent object: {type(event)}")
            return
        if not event.is_valid():
            logger.warning(
                f"Attempted to add invalid (non-finite value) event: {event}"
            )
            return

        step = event.global_step
        name = event.name
        value = float(event.value)  # Ensure value is float for consistency
        timestamp = time.monotonic()

        self._raw_data_buffer[step][name].append(event)
        self._latest_values[name] = (step, value)
        self._event_timestamps[name].append((timestamp, step))

    def get_data_to_process(
        self, current_global_step: int
    ) -> tuple[dict[int, dict[str, list[RawMetricEvent]]], int]:
        """
        Returns a copy of the raw data buffer for steps up to current_global_step
        and the maximum step included in the returned data.
        """
        data_copy: dict[int, dict[str, list[RawMetricEvent]]] = {}
        max_step_in_batch: int = self._last_processed_step
        # Find steps in buffer that are <= current_global_step
        steps_to_process = sorted(
            [step for step in self._raw_data_buffer if step <= current_global_step]
        )

        if not steps_to_process:
            return {}, max_step_in_batch

        for step in steps_to_process:
            # Deep copy might be safer if RawMetricEvent becomes mutable, but list copy is usually sufficient
            data_copy[step] = {
                key: list(event_list)  # Create a copy of the list of events
                for key, event_list in self._raw_data_buffer[step].items()
            }
            max_step_in_batch = max(max_step_in_batch, step)

        return data_copy, max_step_in_batch

    def clear_processed_data(self, processed_steps: Iterable[int]) -> None:
        """Removes processed steps from the internal buffer."""
        for step in processed_steps:
            if step in self._raw_data_buffer:
                del self._raw_data_buffer[step]

    def get_log_context(self, latest_step: int, current_time: float) -> LogContext:
        """Creates the LogContext for the current processing cycle."""
        # Return copies to prevent modification by the processor
        timestamp_data = {name: list(dq) for name, dq in self._event_timestamps.items()}
        latest_values_copy = self._latest_values.copy()
        return LogContext(
            latest_step=latest_step,
            last_log_time=self._last_processed_time,
            current_time=current_time,
            event_timestamps=timestamp_data,
            latest_values=latest_values_copy,
        )

    def update_last_processed_step(self, step: int) -> None:
        """Updates the last processed step, ensuring it only increases."""
        self._last_processed_step = max(self._last_processed_step, step)

    def update_last_processed_time(self, timestamp: float) -> None:
        """Updates the timestamp of the last processing cycle."""
        self._last_processed_time = timestamp

    def get_last_processed_time(self) -> float:
        """Gets the timestamp of the last processing cycle."""
        return self._last_processed_time

    def get_last_processed_step(self) -> int:
        """Gets the last processed global step."""
        return self._last_processed_step

    def get_persistable_state(self) -> dict[str, Any]:
        """Returns the minimal state needed for persistence."""
        # Return copies to prevent modification if the dict is held elsewhere
        return {
            "last_processed_step": self._last_processed_step,
            "last_processed_time": self._last_processed_time,
            # Include the per-metric log times for accurate time-based logging after restore
            "_last_log_time_per_metric": self._last_log_time_per_metric.copy(),
        }

    def restore_from_state(self, state: dict[str, Any]) -> None:
        """Restores internal state from a dictionary."""
        self._last_processed_step = state.get("last_processed_step", -1)
        # Use current time as fallback if not in state
        self._last_processed_time = state.get("last_processed_time", time.monotonic())
        # Restore per-metric log times
        self._last_log_time_per_metric = state.get("_last_log_time_per_metric", {})

        # Clear buffers on restore, as they are transient
        self._raw_data_buffer.clear()
        self._latest_values.clear()
        self._event_timestamps.clear()
        logger.info(
            f"ActorState restored. Last processed step: {self._last_processed_step}"
        )
