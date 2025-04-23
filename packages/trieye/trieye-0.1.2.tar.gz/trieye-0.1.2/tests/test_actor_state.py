# File: tests/test_actor_state.py
import time
from collections import deque

import pytest

from trieye.actor_state import ActorState
from trieye.schemas import LogContext, RawMetricEvent


@pytest.fixture
def actor_state() -> ActorState:
    """Provides a fresh ActorState instance for each test."""
    return ActorState()


def test_state_initialization(actor_state: ActorState):
    """Test the initial state of ActorState."""
    assert actor_state._raw_data_buffer == {}
    assert actor_state._latest_values == {}
    assert actor_state._event_timestamps == {}
    assert actor_state.get_last_processed_step() == -1
    assert actor_state.get_last_processed_time() <= time.monotonic()
    assert actor_state._last_log_time_per_metric == {}


def test_state_add_valid_event(actor_state: ActorState):
    """Test adding a single valid event."""
    event = RawMetricEvent(name="test_event", value=10.0, global_step=1)
    start_time = time.monotonic()
    actor_state.add_event(event)
    end_time = time.monotonic()

    assert 1 in actor_state._raw_data_buffer
    assert "test_event" in actor_state._raw_data_buffer[1]
    assert len(actor_state._raw_data_buffer[1]["test_event"]) == 1
    assert actor_state._raw_data_buffer[1]["test_event"][0] == event

    assert "test_event" in actor_state._latest_values
    assert actor_state._latest_values["test_event"] == (1, 10.0)

    assert "test_event" in actor_state._event_timestamps
    assert isinstance(actor_state._event_timestamps["test_event"], deque)
    assert len(actor_state._event_timestamps["test_event"]) == 1
    ts, step = actor_state._event_timestamps["test_event"][0]
    assert start_time <= ts <= end_time
    assert step == 1


def test_state_add_invalid_event(actor_state: ActorState, caplog):
    """Test adding an event with a non-finite value."""
    event = RawMetricEvent(name="invalid_event", value=float("inf"), global_step=1)
    actor_state.add_event(event)

    assert 1 not in actor_state._raw_data_buffer
    assert "invalid_event" not in actor_state._latest_values
    assert "invalid_event" not in actor_state._event_timestamps
    assert "Attempted to add invalid (non-finite value) event" in caplog.text


def test_state_add_non_event_object(actor_state: ActorState, caplog):
    """Test adding an object that is not a RawMetricEvent."""
    actor_state.add_event({"not": "an event"})  # type: ignore[arg-type]
    assert not actor_state._raw_data_buffer
    assert "Attempted to add non-RawMetricEvent object" in caplog.text


def test_state_get_data_to_process(actor_state: ActorState):
    """Test retrieving data for processing."""
    event1 = RawMetricEvent(name="e1", value=1, global_step=1)
    event2 = RawMetricEvent(name="e1", value=2, global_step=2)
    event3 = RawMetricEvent(name="e2", value=3, global_step=2)
    event4 = RawMetricEvent(name="e1", value=4, global_step=3)
    actor_state.add_event(event1)
    actor_state.add_event(event2)
    actor_state.add_event(event3)
    actor_state.add_event(event4)

    # Process up to step 2
    data, max_step = actor_state.get_data_to_process(current_global_step=2)

    assert max_step == 2
    assert 1 in data
    assert 2 in data
    assert 3 not in data  # Step 3 should not be included
    assert data[1]["e1"] == [event1]
    assert data[2]["e1"] == [event2]
    assert data[2]["e2"] == [event3]

    # Check original buffer still contains step 3
    assert 3 in actor_state._raw_data_buffer

    # Process up to step 3 (should include step 3 now)
    data_all, max_step_all = actor_state.get_data_to_process(current_global_step=3)
    assert max_step_all == 3
    assert 3 in data_all
    assert data_all[3]["e1"] == [event4]

    # Process step 0 (no data)
    data_none, max_step_none = actor_state.get_data_to_process(current_global_step=0)
    assert data_none == {}
    assert max_step_none == -1  # Initial value


def test_state_clear_processed_data(actor_state: ActorState):
    """Test clearing processed data from the buffer."""
    actor_state.add_event(RawMetricEvent(name="e1", value=1, global_step=1))
    actor_state.add_event(RawMetricEvent(name="e1", value=2, global_step=2))
    actor_state.add_event(RawMetricEvent(name="e1", value=3, global_step=3))

    assert 1 in actor_state._raw_data_buffer
    assert 2 in actor_state._raw_data_buffer
    assert 3 in actor_state._raw_data_buffer

    actor_state.clear_processed_data([1, 2])

    assert 1 not in actor_state._raw_data_buffer
    assert 2 not in actor_state._raw_data_buffer
    assert 3 in actor_state._raw_data_buffer  # Step 3 should remain


def test_state_get_log_context(actor_state: ActorState):
    """Test creating the LogContext."""
    actor_state.add_event(RawMetricEvent(name="e1", value=1, global_step=1))
    actor_state.add_event(RawMetricEvent(name="e1", value=2, global_step=2))
    actor_state._last_processed_time = (
        time.monotonic() - 5.0
    )  # Simulate last run 5s ago

    current_time = time.monotonic()
    context = actor_state.get_log_context(latest_step=2, current_time=current_time)

    assert isinstance(context, LogContext)
    assert context.latest_step == 2
    assert context.last_log_time == actor_state._last_processed_time
    assert context.current_time == current_time
    assert "e1" in context.event_timestamps
    assert len(context.event_timestamps["e1"]) == 2
    assert isinstance(context.event_timestamps["e1"], list)  # Should be a copy
    assert "e1" in context.latest_values
    assert context.latest_values["e1"] == (2, 2.0)


def test_state_update_last_processed(actor_state: ActorState):
    """Test updating last processed step and time."""
    assert actor_state.get_last_processed_step() == -1
    actor_state.update_last_processed_step(10)
    assert actor_state.get_last_processed_step() == 10
    # Should not decrease
    actor_state.update_last_processed_step(5)
    assert actor_state.get_last_processed_step() == 10

    t1 = time.monotonic()
    actor_state.update_last_processed_time(t1)
    assert actor_state.get_last_processed_time() == t1
    time.sleep(0.01)
    t2 = time.monotonic()
    actor_state.update_last_processed_time(t2)
    assert actor_state.get_last_processed_time() == t2


def test_state_get_persistable_state(actor_state: ActorState):
    """Test getting the state dictionary for persistence."""
    actor_state._last_processed_step = 100
    actor_state._last_processed_time = 12345.678
    actor_state._last_log_time_per_metric = {"metric1": 12340.0}

    persist_state = actor_state.get_persistable_state()

    assert isinstance(persist_state, dict)
    assert persist_state["last_processed_step"] == 100
    assert persist_state["last_processed_time"] == 12345.678
    assert persist_state["_last_log_time_per_metric"] == {"metric1": 12340.0}
    # Ensure it's a copy
    persist_state["_last_log_time_per_metric"]["metric2"] = 999.0
    assert "metric2" not in actor_state._last_log_time_per_metric


def test_state_restore_from_state(actor_state: ActorState):
    """Test restoring state from a dictionary."""
    # Add some data first to ensure buffers are cleared
    actor_state.add_event(RawMetricEvent(name="e1", value=1, global_step=1))

    restore_state = {
        "last_processed_step": 99,
        "last_processed_time": 54321.999,
        "_last_log_time_per_metric": {"metric_a": 54300.0},
    }
    actor_state.restore_from_state(restore_state)

    assert actor_state.get_last_processed_step() == 99
    assert actor_state.get_last_processed_time() == 54321.999
    assert actor_state._last_log_time_per_metric == {"metric_a": 54300.0}

    # Check buffers were cleared
    assert not actor_state._raw_data_buffer
    assert not actor_state._latest_values
    assert not actor_state._event_timestamps

    # Test restoring with missing keys (should use defaults)
    actor_state.restore_from_state({"last_processed_step": 5})
    assert actor_state.get_last_processed_step() == 5
    assert (
        actor_state.get_last_processed_time() <= time.monotonic()
    )  # Defaulted to current time
    assert actor_state._last_log_time_per_metric == {}
