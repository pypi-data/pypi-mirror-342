# File: tests/test_stats_processor.py
import logging
import time
from typing import Any
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
        processing_interval_seconds=0.01,  # Low interval for testing time frequency
        metrics=[
            MetricConfig(
                name="Test/Mean",
                source="custom",
                aggregation="mean",
                log_frequency_steps=1,
                log_to=["mlflow", "tensorboard", "console"],
            ),
            MetricConfig(
                name="Test/Sum",
                source="custom",
                aggregation="sum",
                log_frequency_steps=1,
                log_to=["mlflow", "tensorboard", "console"],
            ),
            MetricConfig(
                name="Test/Latest",
                source="custom",
                aggregation="latest",
                log_frequency_steps=1,
                log_to=["mlflow", "tensorboard", "console"],
            ),
            MetricConfig(
                name="Test/Count",
                source="custom",
                raw_event_name="item",
                aggregation="count",
                log_frequency_steps=1,
                log_to=["mlflow", "tensorboard", "console"],
            ),
            MetricConfig(
                name="Test/Min",
                source="custom",
                aggregation="min",
                log_frequency_steps=1,
                log_to=["mlflow", "tensorboard", "console"],
            ),
            MetricConfig(
                name="Test/Max",
                source="custom",
                aggregation="max",
                log_frequency_steps=1,
                log_to=["mlflow", "tensorboard", "console"],
            ),
            MetricConfig(
                name="Test/Std",
                source="custom",
                aggregation="std",
                log_frequency_steps=1,
                log_to=["mlflow", "tensorboard", "console"],
            ),
            MetricConfig(
                name="Test/Rate",
                source="custom",
                aggregation="rate",
                rate_numerator_event="item",  # Use 'item' value sum for rate
                log_frequency_seconds=0.05,  # Time based
                log_frequency_steps=0,
                log_to=["mlflow", "console"],  # Test specific targets
            ),
            MetricConfig(
                name="Test/ContextScore",
                source="custom",
                raw_event_name="episode",
                context_key="score",
                aggregation="mean",
                log_frequency_steps=1,
                log_to=["mlflow", "tensorboard", "console"],
            ),
            MetricConfig(
                name="Test/TimeFreq",
                source="custom",
                aggregation="latest",
                log_frequency_seconds=0.05,  # Time based
                log_frequency_steps=0,
                log_to=["mlflow", "tensorboard", "console"],
            ),
            MetricConfig(
                name="Test/NeverLog",
                source="custom",
                aggregation="latest",
                log_frequency_seconds=0,  # Disabled
                log_frequency_steps=0,  # Disabled
            ),
            MetricConfig(
                name="Test/OnlyConsole",
                source="custom",
                aggregation="latest",
                log_frequency_steps=1,
                log_to=["console"],  # Test specific target
            ),
        ],
    )


@pytest.fixture
def stats_processor(
    stats_config_for_processor: StatsConfig,
    mock_mlflow_client: MagicMock,
    mock_tb_writer: MagicMock,
) -> StatsProcessor:
    """Provides a StatsProcessor instance with mocked clients injected via constructor."""
    processor = StatsProcessor(
        config=stats_config_for_processor,
        run_name="test_processor_run",
        tb_writer=mock_tb_writer,
        mlflow_run_id="test_processor_mlflow_id",
        _mlflow_client=mock_mlflow_client,  # Inject mock client here
    )
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


def test_processor_aggregation_methods(stats_processor: StatsProcessor):
    """Test various aggregation methods directly."""
    values = [10.0, 20.0, 15.0, 10.0]
    assert stats_processor._aggregate_values(values, "mean") == pytest.approx(13.75)
    assert stats_processor._aggregate_values(values, "sum") == pytest.approx(55.0)
    assert stats_processor._aggregate_values(values, "latest") == pytest.approx(10.0)
    assert stats_processor._aggregate_values(values, "min") == pytest.approx(10.0)
    assert stats_processor._aggregate_values(values, "max") == pytest.approx(20.0)
    assert stats_processor._aggregate_values(values, "count") == 4
    assert stats_processor._aggregate_values(values, "std") == pytest.approx(
        np.std(values)
    )

    # Edge cases
    assert stats_processor._aggregate_values([], "mean") is None
    assert (
        stats_processor._aggregate_values([float("inf"), float("nan")], "mean") is None
    )
    assert stats_processor._aggregate_values([5.0], "mean") == pytest.approx(5.0)
    assert stats_processor._aggregate_values([5.0], "std") == pytest.approx(
        0.0
    )  # Std of single value
    assert stats_processor._aggregate_values([5.0, 5.0], "std") == pytest.approx(
        0.0
    )  # Std of identical values


def test_processor_rate_calculation(stats_processor: StatsProcessor):
    """Test rate calculation logic."""
    rate_metric_config = stats_processor._metric_configs["Test/Rate"]
    step = 10
    current_time = time.monotonic()
    last_log_time = current_time - 2.0  # 2 seconds interval

    # Case 1: Events occurred
    raw_data_input: dict[int, dict[str, list[RawMetricEvent]]] = {
        step: {
            "item": [  # Numerator event
                create_proc_test_event("item", 2, step),  # Value = 2
                create_proc_test_event("item", 3, step),  # Value = 3
            ]
        }
    }
    context = LogContext(
        latest_step=step,
        last_log_time=last_log_time,
        current_time=current_time,
        event_timestamps={},
        latest_values={},  # Not needed for this calc
    )
    rate = stats_processor._calculate_rate(rate_metric_config, context, raw_data_input)
    # Expected rate = (2 + 3) / 2.0 = 2.5
    assert rate == pytest.approx(2.5)

    # Case 2: No events occurred
    raw_data_no_events: dict[int, dict[str, list[RawMetricEvent]]] = {
        step: {"other_event": []}
    }
    rate_none = stats_processor._calculate_rate(
        rate_metric_config, context, raw_data_no_events
    )
    assert rate_none == pytest.approx(0.0)  # Should return 0 rate

    # Case 3: Zero time delta
    context_zero_delta = LogContext(
        latest_step=step,
        last_log_time=current_time,
        current_time=current_time,
        event_timestamps={},
        latest_values={},
    )
    rate_zero_delta = stats_processor._calculate_rate(
        rate_metric_config, context_zero_delta, raw_data_input
    )
    assert rate_zero_delta is None


def test_processor_should_log(stats_processor: StatsProcessor):
    """Test the logic for deciding whether to log based on frequency."""
    metric_step = stats_processor._metric_configs["Test/Mean"]  # Freq step=1
    metric_time = stats_processor._metric_configs["Test/TimeFreq"]  # Freq sec=0.05
    metric_never = stats_processor._metric_configs["Test/NeverLog"]  # Freq 0

    current_time = time.monotonic()
    context = LogContext(
        latest_step=10,
        last_log_time=current_time - 1.0,
        current_time=current_time,
        event_timestamps={},
        latest_values={},
    )

    # Step frequency check
    assert (
        stats_processor._should_log(metric_step, 10, context) is True
    )  # Step 10 % 1 == 0
    # Corrected expectation: Step 9 % 1 != 0 is false, but step freq is 1, so should log every step
    assert stats_processor._should_log(metric_step, 9, context) is True
    metric_step.log_frequency_steps = 5
    assert (
        stats_processor._should_log(metric_step, 10, context) is True
    )  # Step 10 % 5 == 0
    assert (
        stats_processor._should_log(metric_step, 9, context) is False
    )  # Step 9 % 5 != 0
    metric_step.log_frequency_steps = 1  # Reset for other tests

    # Time frequency check
    stats_processor._last_log_time[metric_time.name] = (
        current_time - 0.01
    )  # Logged recently
    assert stats_processor._should_log(metric_time, 10, context) is False  # 0.01 < 0.05
    stats_processor._last_log_time[metric_time.name] = (
        current_time - 0.10
    )  # Logged long ago
    assert stats_processor._should_log(metric_time, 10, context) is True  # 0.10 >= 0.05

    # Never log check
    assert stats_processor._should_log(metric_never, 10, context) is False


def test_processor_full_process_and_log(
    stats_processor: StatsProcessor,
    mock_mlflow_client: MagicMock,
    mock_tb_writer: MagicMock,
    caplog,  # Capture log output
):
    """Tests the full processing and logging flow."""
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
            "Test/Min": [
                create_proc_test_event("Test/Min", 12.0, step),
                create_proc_test_event("Test/Min", 8.0, step),
            ],
            "Test/Max": [
                create_proc_test_event("Test/Max", 12.0, step),
                create_proc_test_event("Test/Max", 8.0, step),
            ],
            "Test/Std": [
                create_proc_test_event("Test/Std", 1.0, step),
                create_proc_test_event("Test/Std", 3.0, step),
            ],
            "item": [  # For Count and Rate
                create_proc_test_event("item", 1, step),  # Value = 1
                create_proc_test_event("item", 1, step),  # Value = 1
                create_proc_test_event("item", 1, step),  # Value = 1
            ],
            "episode": [  # For ContextScore
                create_proc_test_event("episode", 1, step, context={"score": 80.0}),
                create_proc_test_event("episode", 1, step, context={"score": 120.0}),
            ],
            "Test/TimeFreq": [create_proc_test_event("Test/TimeFreq", 99.0, step)],
            "Test/NeverLog": [create_proc_test_event("Test/NeverLog", 111.0, step)],
            "Test/OnlyConsole": [
                create_proc_test_event("Test/OnlyConsole", 77.0, step)
            ],
        }
    }

    current_time = time.monotonic()
    # Simulate 1 second interval for rate calc, and assume this is the first log for time-based
    log_context = LogContext(
        latest_step=step,
        last_log_time=current_time - 1.0,
        current_time=current_time,
        event_timestamps={},
        latest_values={},  # Simplified for this test
    )

    # --- Execute ---
    with caplog.at_level(logging.INFO):  # Capture INFO level logs for console check
        stats_processor.process_and_log(raw_data_input, log_context)

    # --- Verification ---
    mlflow_calls = mock_mlflow_client.log_metric.call_args_list
    tb_calls = mock_tb_writer.add_scalar.call_args_list

    # Check aggregated values were logged correctly
    expected_logs: dict[str, Any] = {  # Use Any for value type due to ApproxBase
        "Test/Mean": 15.0,
        "Test/Sum": 11.0,
        "Test/Latest": 2.0,
        "Test/Count": 3.0,  # 3 'item' events
        "Test/Min": 8.0,
        "Test/Max": 12.0,
        "Test/Std": pytest.approx(1.0),  # std([1,3]) = 1
        "Test/ContextScore": 100.0,
        "Test/TimeFreq": 99.0,  # Logged because time interval > freq
        "Test/Rate": pytest.approx(
            3.0 / 1.0
        ),  # Rate = sum(item values) / time_delta = (1+1+1)/1.0 = 3.0
        "Test/OnlyConsole": 77.0,
    }

    # More robust check for MLflow calls
    metrics_logged_mlflow_calls = {
        call.kwargs["key"]: call.kwargs["value"] for call in mlflow_calls
    }
    metrics_logged_tb = {c.args[0]: c.args[1] for c in tb_calls}
    console_logs = [
        rec.message
        for rec in caplog.records
        if rec.levelname == "INFO" and "STATS" in rec.message
    ]

    for name, expected_value in expected_logs.items():
        metric_config = stats_processor._metric_configs[name]

        # Check MLflow logging
        if "mlflow" in metric_config.log_to:
            assert name in metrics_logged_mlflow_calls, f"{name} not logged to MLflow"
            mlflow_val = metrics_logged_mlflow_calls[name]
            # Safely convert expected_value if it's ApproxBase before float conversion
            expected_float = (
                expected_value.expected
                if isinstance(expected_value, ApproxBase)
                else expected_value
            )
            if isinstance(expected_value, ApproxBase):
                assert mlflow_val == expected_value
            else:
                assert np.isclose(float(mlflow_val), float(expected_float)), (
                    f"MLflow value mismatch for {name}"
                )
            mlflow_step = next(
                c.kwargs["step"] for c in mlflow_calls if c.kwargs["key"] == name
            )
            # Rate logs against context.latest_step, others log against step where data occurred
            assert mlflow_step == (
                log_context.latest_step if name == "Test/Rate" else step
            )
        else:
            assert name not in metrics_logged_mlflow_calls, (
                f"{name} incorrectly logged to MLflow"
            )

        # Check TensorBoard logging
        if "tensorboard" in metric_config.log_to:
            assert name in metrics_logged_tb, f"{name} not logged to TensorBoard"
            tb_val = metrics_logged_tb[name]
            expected_float = (
                expected_value.expected
                if isinstance(expected_value, ApproxBase)
                else expected_value
            )
            if isinstance(expected_value, ApproxBase):
                assert tb_val == expected_value
            else:
                assert np.isclose(float(tb_val), float(expected_float)), (
                    f"TensorBoard value mismatch for {name}"
                )
            tb_step = next(c.args[2] for c in tb_calls if c.args[0] == name)
            # Rate logs against context.latest_step, others log against step where data occurred
            assert tb_step == (log_context.latest_step if name == "Test/Rate" else step)
        else:
            assert name not in metrics_logged_tb, (
                f"{name} incorrectly logged to TensorBoard"
            )

        # Check Console logging
        if "console" in metric_config.log_to:
            expected_float = (
                expected_value.expected
                if isinstance(expected_value, ApproxBase)
                else expected_value
            )
            # Use the correct step for console logging check
            console_step = log_context.latest_step if name == "Test/Rate" else step
            expected_log_msg_part = (
                f"STATS [{console_step}]: {name} = {float(expected_float):.4f}"
            )
            assert any(expected_log_msg_part in msg for msg in console_logs), (
                f"Expected console log for {name} not found: '{expected_log_msg_part}' in {console_logs}"
            )
        else:
            expected_log_msg_part = f"{name} ="
            assert not any(expected_log_msg_part in msg for msg in console_logs), (
                f"{name} incorrectly logged to console"
            )

    # Check that NeverLog metric was NOT logged anywhere
    assert "Test/NeverLog" not in metrics_logged_mlflow_calls
    assert "Test/NeverLog" not in metrics_logged_tb
    assert not any("Test/NeverLog" in msg for msg in console_logs)

    # Check TB flush was called
    mock_tb_writer.flush.assert_called_once()
