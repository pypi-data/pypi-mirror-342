# File: trieye/tests/test_processor.py
import logging
import time
from unittest.mock import MagicMock

import numpy as np
import pytest
from _pytest.python_api import ApproxBase  # Import for type checking approx

# Import from source
from trieye.config import MetricConfig, StatsConfig
from trieye.schemas import LogContext, RawMetricEvent
from trieye.stats_processor import StatsProcessor

logger = logging.getLogger(__name__)


@pytest.fixture
def stats_config_for_processor() -> StatsConfig:
    """Provides a StatsConfig specifically for processor tests."""
    return StatsConfig(
        processing_interval_seconds=0.01,
        metrics=[
            MetricConfig(
                name="Test/Mean",
                source="custom",
                aggregation="mean",
                log_frequency_steps=1,
            ),
            MetricConfig(
                name="Test/Sum",
                source="custom",
                aggregation="sum",
                log_frequency_steps=1,
            ),
            MetricConfig(
                name="Test/Latest",
                source="custom",
                aggregation="latest",
                log_frequency_steps=1,
            ),
            MetricConfig(
                name="Test/Count",
                source="custom",
                raw_event_name="item",
                aggregation="count",
                log_frequency_steps=1,
            ),
            # Corrected log_to for Test/Rate
            MetricConfig(
                name="Test/Rate",
                source="custom",
                aggregation="rate",
                rate_numerator_event="item",
                log_frequency_seconds=0.05,
                log_frequency_steps=0,
                log_to=["mlflow", "console"],
            ),
            MetricConfig(
                name="Test/ContextScore",
                source="custom",
                raw_event_name="episode",
                context_key="score",
                aggregation="mean",
                log_frequency_steps=1,
            ),
            MetricConfig(
                name="Test/TimeFreq",
                source="custom",
                aggregation="latest",
                log_frequency_seconds=0.05,
                log_frequency_steps=0,
            ),
            MetricConfig(
                name="Test/NeverLog",
                source="custom",
                aggregation="latest",
                log_frequency_seconds=0,
                log_frequency_steps=0,
            ),  # Should not be logged
        ],
    )


@pytest.fixture
def stats_processor(
    stats_config_for_processor: StatsConfig,
    mock_mlflow_client: MagicMock,
    mock_tb_writer: MagicMock,
) -> StatsProcessor:
    """Provides a StatsProcessor instance with mocked clients."""
    processor = StatsProcessor(
        config=stats_config_for_processor,
        run_name="test_processor_run",
        tb_writer=mock_tb_writer,
        mlflow_run_id="test_processor_mlflow_id",
    )
    # Inject mock client after initialization
    processor.mlflow_client = mock_mlflow_client
    return processor


# Helper to create RawMetricEvent for processor tests
def create_proc_test_event(
    name: str, value: float | int, step: int, context: dict | None = None
) -> RawMetricEvent:
    return RawMetricEvent(
        name=name,
        value=value,
        global_step=step,
        context=context or {},
        timestamp=time.time(),
    )


def test_processor_aggregation_and_logging(
    stats_processor: StatsProcessor,
    mock_mlflow_client: MagicMock,
    mock_tb_writer: MagicMock,
):
    """Tests aggregation and logging logic."""
    step = 10
    raw_data_input: dict[int, dict[str, list[RawMetricEvent]]] = {
        step: {
            "Test/Mean": [
                create_proc_test_event("Test/Mean", 10.0, step),
                create_proc_test_event("Test/Mean", 20.0, step),
            ],
            "Test/Sum": [
                create_proc_test_event("Test/Sum", 5.0, step),
                create_proc_test_event("Test/Sum", 6.0, step),
            ],
            "Test/Latest": [
                create_proc_test_event("Test/Latest", 1.0, step),
                create_proc_test_event("Test/Latest", 2.0, step),
            ],
            "item": [
                create_proc_test_event("item", 1, step),
                create_proc_test_event("item", 1, step),
                create_proc_test_event("item", 1, step),
            ],  # For Count and Rate
            "episode": [
                create_proc_test_event("episode", 1, step, context={"score": 80.0}),
                create_proc_test_event("episode", 1, step, context={"score": 120.0}),
            ],
            "Test/TimeFreq": [create_proc_test_event("Test/TimeFreq", 99.0, step)],
            "Test/NeverLog": [create_proc_test_event("Test/NeverLog", 111.0, step)],
        }
    }

    current_time = time.monotonic()
    log_context = LogContext(
        latest_step=step,
        last_log_time=current_time - 1.0,  # Simulate 1 second interval
        current_time=current_time,
        event_timestamps={
            "item": [
                (current_time - 0.5, step),
                (current_time - 0.2, step),
                (current_time - 0.1, step),
            ]
        },  # Mock timestamps for rate
        latest_values={},  # Not strictly needed for this test flow
    )

    # --- Execute ---
    stats_processor.process_and_log(raw_data_input, log_context)

    # --- Verification ---
    mlflow_calls = mock_mlflow_client.log_metric.call_args_list
    tb_calls = mock_tb_writer.add_scalar.call_args_list

    # Check aggregated values were logged correctly
    expected_logs = {
        "Test/Mean": 15.0,
        "Test/Sum": 11.0,
        "Test/Latest": 2.0,
        "Test/Count": 3.0,
        "Test/ContextScore": 100.0,
        "Test/TimeFreq": 99.0,
        # Rate is approx 3 items / 1 second = 3.0
        "Test/Rate": pytest.approx(3.0, abs=0.5),  # Allow some tolerance for timing
    }

    metrics_logged_mlflow = {c.kwargs["key"]: c.kwargs["value"] for c in mlflow_calls}
    metrics_logged_tb = {c.args[0]: c.args[1] for c in tb_calls}

    for name, expected_value in expected_logs.items():
        # Check MLflow logging
        if name == "Test/Rate":  # Rate logs only to mlflow and console
            assert name in metrics_logged_mlflow, f"{name} not logged to MLflow"
        else:  # Others log to both
            assert name in metrics_logged_mlflow, f"{name} not logged to MLflow"
            assert name in metrics_logged_tb, f"{name} not logged to TensorBoard"

        # Check values, handling pytest.approx correctly
        mlflow_val = metrics_logged_mlflow[name]
        tb_val = metrics_logged_tb.get(name)  # Use .get() as Rate won't be here

        if isinstance(expected_value, ApproxBase):
            assert mlflow_val == expected_value
            if tb_val is not None:  # Only check TB if it was expected
                assert tb_val == expected_value
        else:
            # Ensure comparison is between floats for isclose
            assert isinstance(mlflow_val, int | float)
            assert isinstance(expected_value, int | float)
            assert np.isclose(float(mlflow_val), float(expected_value)), (
                f"MLflow value mismatch for {name}"
            )
            if tb_val is not None:  # Only check TB if it was expected
                assert isinstance(tb_val, int | float)
                assert np.isclose(float(tb_val), float(expected_value)), (
                    f"TensorBoard value mismatch for {name}"
                )

        # Check step
        mlflow_step = next(
            c.kwargs["step"] for c in mlflow_calls if c.kwargs["key"] == name
        )
        assert mlflow_step == step
        if tb_val is not None:  # Only check TB step if logged
            tb_step = next(c.args[2] for c in tb_calls if c.args[0] == name)
            assert tb_step == step

    # Check that NeverLog metric was NOT logged
    assert "Test/NeverLog" not in metrics_logged_mlflow
    assert "Test/NeverLog" not in metrics_logged_tb

    # Check console log for Rate (if logger captured)
    # This requires capturing logs, e.g., with caplog fixture
