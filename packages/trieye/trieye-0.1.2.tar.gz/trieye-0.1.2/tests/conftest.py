# File: tests/conftest.py
import logging
import time
from pathlib import Path
from unittest.mock import MagicMock

import pytest
import ray

# --- Added Imports ---
from mlflow.tracking import MlflowClient
from torch.utils.tensorboard import SummaryWriter

# --- End Added Imports ---
# Import from source
from trieye.config import (
    MetricConfig,
    PersistenceConfig,
    StatsConfig,
    TrieyeConfig,
)
from trieye.schemas import BufferData, CheckpointData, RawMetricEvent

# Configure logging for tests
logging.basicConfig(level=logging.INFO)  # Reduce default log level for tests
logging.getLogger("trieye").setLevel(logging.DEBUG)  # Enable debug for trieye module


@pytest.fixture(scope="session")
def ray_init_shutdown_session():
    """Initialize Ray once per test session (non-local mode)."""
    # Ensure Ray is shut down before starting (clean slate)
    if ray.is_initialized():
        ray.shutdown()
    # Use minimal resources for testing
    ray.init(
        logging_level=logging.WARNING,
        num_cpus=2,  # Allow at least 2 CPUs for actor + driver
        log_to_driver=False,
        local_mode=False,  # Explicitly non-local
        configure_logging=True,  # Let Ray manage its logging setup
        include_dashboard=False,  # Disable dashboard for tests
    )
    yield
    if ray.is_initialized():
        ray.shutdown()


@pytest.fixture(scope="function")
def ray_local_mode_init():
    """Initialize Ray in local mode for a single test function."""
    if ray.is_initialized():
        ray.shutdown()
    # Local mode runs everything in the main process
    ray.init(
        logging_level=logging.WARNING,
        local_mode=True,
        num_cpus=1,
        log_to_driver=True,  # Log directly for easier debugging in local mode
        configure_logging=True,
        include_dashboard=False,
    )
    yield
    if ray.is_initialized():
        ray.shutdown()


@pytest.fixture
def temp_data_dir(tmp_path: Path) -> Path:
    """Creates a temporary root data directory for a single test."""
    data_dir = tmp_path / ".test_trieye_data"
    data_dir.mkdir()
    return data_dir


@pytest.fixture
def base_persist_config(temp_data_dir: Path) -> PersistenceConfig:
    """Basic PersistenceConfig using the temporary directory."""
    return PersistenceConfig(ROOT_DATA_DIR=str(temp_data_dir))


@pytest.fixture
def base_stats_config() -> StatsConfig:
    """Basic StatsConfig with a few metrics."""
    return StatsConfig(
        processing_interval_seconds=0.01,  # Fast processing for tests
        metrics=[
            MetricConfig(
                name="Test/Value",
                source="custom",
                aggregation="mean",
                log_frequency_steps=1,
                log_to=["mlflow", "tensorboard", "console"],  # Log everywhere for tests
            ),
            MetricConfig(
                name="Test/Count",
                source="custom",
                raw_event_name="item_processed",
                aggregation="count",
                log_frequency_steps=1,
                log_to=["mlflow", "tensorboard", "console"],
            ),
            MetricConfig(
                name="Test/Rate",
                source="custom",
                aggregation="rate",
                rate_numerator_event="item_processed",  # Use value sum for rate
                log_frequency_seconds=0.05,
                log_frequency_steps=0,
                log_to=["mlflow", "tensorboard", "console"],
            ),
            MetricConfig(
                name="Test/ContextValue",
                source="custom",
                raw_event_name="context_event",
                context_key="my_val",
                aggregation="latest",
                log_frequency_steps=1,
                log_to=["mlflow", "tensorboard", "console"],
            ),
        ],
    )


@pytest.fixture
def base_trieye_config(
    temp_data_dir: Path,  # noqa: ARG001 - Used indirectly by base_persist_config
    base_persist_config: PersistenceConfig,
    base_stats_config: StatsConfig,
) -> TrieyeConfig:
    """Basic TrieyeConfig using temporary directory and base configs."""
    run_name = f"test_run_{time.time_ns()}"  # Ensure unique run name per test
    cfg = TrieyeConfig(
        app_name="test_app",
        run_name=run_name,
        persistence=base_persist_config,
        stats=base_stats_config,
    )
    return cfg


@pytest.fixture
def mock_mlflow_client() -> MagicMock:
    """Provides a mock MlflowClient instance."""
    mock_client = MagicMock(spec=MlflowClient)
    # Mock methods used by StatsProcessor/TrieyeActor/ActorLogic
    mock_client.log_metric = MagicMock(
        side_effect=None
    )  # Ensure log_metric doesn't raise errors
    mock_client.log_param = MagicMock(side_effect=None)
    mock_client.log_artifact = MagicMock(side_effect=None)
    mock_client.log_artifacts = MagicMock(side_effect=None)
    # Add a way to identify the mock run ID if needed
    mock_client._mock_run_id = "mock_mlflow_run_id_fixture"
    return mock_client


@pytest.fixture
def mock_tb_writer() -> MagicMock:
    """Provides a mock SummaryWriter instance."""
    mock_writer = MagicMock(spec=SummaryWriter)
    mock_writer.add_scalar = MagicMock()
    mock_writer.flush = MagicMock()
    mock_writer.close = MagicMock()
    # Mock the log_dir attribute expected by the actor
    mock_writer.log_dir = "/mock/tensorboard/log/dir"
    return mock_writer


# Fixture to create RawMetricEvent easily
@pytest.fixture
def create_event():
    def _create_event(
        name: str, value: float | int, step: int, context: dict | None = None
    ) -> RawMetricEvent:
        return RawMetricEvent(
            name=name,
            value=value,
            global_step=step,
            context=context or {},
            timestamp=time.time(),  # Add timestamp
        )

    return _create_event


# Fixture for dummy CheckpointData
@pytest.fixture
def dummy_checkpoint_data() -> CheckpointData:
    return CheckpointData(
        run_name="test_run",
        global_step=100,
        episodes_played=10,
        total_simulations_run=1000,
        model_state_dict={"layer.weight": [1.0]},
        optimizer_state_dict={"state": {}, "param_groups": []},
        actor_state={
            "last_processed_step": 95,
            "last_processed_time": time.monotonic() - 10,
        },
        user_data={"info": "test"},
        model_config_dict={"arch": "simple"},
        env_config_dict={"id": "CartPole-v1"},
    )


# Fixture for dummy BufferData
@pytest.fixture
def dummy_buffer_data() -> BufferData:
    # Store simple strings for testing serialization of generic list
    return BufferData(buffer_list=["exp1", "exp2", "exp3"])
