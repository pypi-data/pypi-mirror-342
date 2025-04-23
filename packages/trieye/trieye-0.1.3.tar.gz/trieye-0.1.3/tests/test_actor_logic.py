# File: tests/test_actor_logic.py
import logging
import time
from pathlib import Path
from unittest.mock import MagicMock  # Import call

import pytest

# No longer need to import pathlib for patching Path.exists globally
# import pathlib
# Import from source
from trieye.actor_logic import ActorLogic
from trieye.actor_state import ActorState
from trieye.config import TrieyeConfig
from trieye.path_manager import PathManager
from trieye.schemas import (
    BufferData,
    CheckpointData,
    LogContext,
    RawMetricEvent,
)
from trieye.serializer import Serializer
from trieye.stats_processor import StatsProcessor

logger = logging.getLogger(__name__)


# --- Fixtures ---
@pytest.fixture
def mock_dependencies(
    base_trieye_config: TrieyeConfig,
    mock_mlflow_client: MagicMock,
    mock_tb_writer: MagicMock,
    temp_data_dir: Path,  # noqa: ARG001 - Used indirectly by real_path_manager
) -> dict:
    """Provides mocked dependencies for ActorLogic."""
    # Use real PathManager only for config reference if needed
    real_path_manager = PathManager(base_trieye_config.persistence)
    real_serializer = Serializer()

    # Mock the PathManager spec
    mock_path_manager = MagicMock(spec=PathManager)
    mock_path_manager.persist_config = (
        real_path_manager.persist_config
    )  # Keep real config

    # --- Mock get_*_path methods to return Mocks ---
    # Create distinct mocks for different path types if needed, or reuse if simple
    mock_cp_path_latest = MagicMock(spec=Path, name="mock_cp_path_latest")
    mock_cp_path_step = MagicMock(spec=Path, name="mock_cp_path_step")
    mock_buf_path_default = MagicMock(spec=Path, name="mock_buf_path_default")
    mock_buf_path_step = MagicMock(spec=Path, name="mock_buf_path_step")
    mock_config_path = MagicMock(spec=Path, name="mock_config_path")

    # Configure resolve() on the mocks to return themselves (or another mock if needed)
    # This simulates Path(...).resolve() returning a Path object
    mock_cp_path_latest.resolve.return_value = mock_cp_path_latest
    mock_cp_path_step.resolve.return_value = mock_cp_path_step
    mock_buf_path_default.resolve.return_value = mock_buf_path_default
    mock_buf_path_step.resolve.return_value = mock_buf_path_step
    mock_config_path.resolve.return_value = mock_config_path

    def get_checkpoint_path_side_effect(
        run_name=None,  # noqa: ARG001
        step=None,  # noqa: ARG001
        is_latest=False,
        is_best=False,
    ):
        # Return specific mocks based on args, or a default mock
        if is_latest:
            return mock_cp_path_latest
        # Add is_best handling if needed for other tests
        if is_best:  # Basic handling for is_best
            # You might want a separate mock for best if its behavior differs significantly
            return mock_cp_path_latest  # Reuse latest for simplicity here
        return mock_cp_path_step  # Default step-based mock

    def get_buffer_path_side_effect(run_name=None, step=None):  # noqa: ARG001
        if step is None:
            return mock_buf_path_default
        return mock_buf_path_step

    mock_path_manager.get_checkpoint_path = MagicMock(
        side_effect=get_checkpoint_path_side_effect
    )
    mock_path_manager.get_buffer_path = MagicMock(
        side_effect=get_buffer_path_side_effect
    )
    mock_path_manager.get_config_path = MagicMock(return_value=mock_config_path)
    # --- End Mock get_*_path ---

    mock_path_manager.update_checkpoint_links = MagicMock()
    mock_path_manager.update_buffer_link = MagicMock()
    mock_path_manager.find_latest_run_dir = MagicMock()
    mock_path_manager.create_run_directories = MagicMock()

    mock_serializer = MagicMock(spec=Serializer)
    mock_serializer.prepare_optimizer_state = real_serializer.prepare_optimizer_state
    mock_serializer.prepare_buffer_data = real_serializer.prepare_buffer_data
    mock_serializer.save_checkpoint = MagicMock()
    mock_serializer.save_buffer = MagicMock()
    mock_serializer.save_config_json = MagicMock()
    mock_serializer.load_checkpoint = MagicMock()
    mock_serializer.load_buffer = MagicMock()

    mock_actor_state = MagicMock(spec=ActorState)
    mock_actor_state.get_persistable_state.return_value = {
        "last_processed_step": 50,
        "last_processed_time": time.monotonic() - 10,
    }
    mock_actor_state.restore_from_state = MagicMock()

    mock_stats_processor = MagicMock(spec=StatsProcessor)
    mock_stats_processor.process_and_log = MagicMock()

    # Store the mock paths for reference in tests if needed
    mock_paths = {
        "cp_latest": mock_cp_path_latest,
        "cp_step": mock_cp_path_step,
        "buf_default": mock_buf_path_default,
        "buf_step": mock_buf_path_step,
        "config": mock_config_path,
    }

    return {
        "config": base_trieye_config,
        "actor_state": mock_actor_state,
        "path_manager": mock_path_manager,
        "serializer": mock_serializer,
        "stats_processor": mock_stats_processor,
        "mlflow_client": mock_mlflow_client,
        "mlflow_run_id": "mock_mlflow_run_id_fixture",
        "tb_writer": mock_tb_writer,
        "_mock_paths": mock_paths,  # Add mock paths for convenience
    }


@pytest.fixture
def actor_logic(mock_dependencies: dict) -> ActorLogic:
    """Provides an ActorLogic instance with mocked dependencies."""
    logic = ActorLogic(
        config=mock_dependencies["config"],
        actor_state=mock_dependencies["actor_state"],
        path_manager=mock_dependencies["path_manager"],
        serializer=mock_dependencies["serializer"],
        mlflow_run_id=mock_dependencies["mlflow_run_id"],
        mlflow_client=mock_dependencies["mlflow_client"],
        tb_writer=mock_dependencies["tb_writer"],
    )
    # Inject the mock stats processor after initialization
    logic.stats_processor = mock_dependencies["stats_processor"]
    return logic


# --- Tests ---


def test_logic_initialization(actor_logic: ActorLogic, mock_dependencies):
    """Test ActorLogic initialization."""
    assert actor_logic.config == mock_dependencies["config"]
    assert actor_logic.actor_state == mock_dependencies["actor_state"]
    assert actor_logic.path_manager == mock_dependencies["path_manager"]
    assert actor_logic.serializer == mock_dependencies["serializer"]
    assert actor_logic.mlflow_run_id == mock_dependencies["mlflow_run_id"]
    assert actor_logic.mlflow_client == mock_dependencies["mlflow_client"]
    assert actor_logic.tb_writer == mock_dependencies["tb_writer"]
    assert isinstance(actor_logic.stats_processor, MagicMock)


def test_logic_process_and_log_metrics(actor_logic: ActorLogic, mock_dependencies):
    """Test delegation to StatsProcessor."""
    raw_data = {1: {"event": [RawMetricEvent(name="event", value=1, global_step=1)]}}
    context = LogContext(
        latest_step=1,
        last_log_time=time.monotonic() - 1,
        current_time=time.monotonic(),
        event_timestamps={},
        latest_values={},
    )
    actor_logic.process_and_log_metrics(raw_data, context)
    mock_dependencies["stats_processor"].process_and_log.assert_called_once_with(
        raw_data, context
    )


def test_logic_save_initial_config(actor_logic: ActorLogic, mock_dependencies):
    """Test saving the initial configuration."""
    # Get the mock config path object
    mock_config_path = mock_dependencies["_mock_paths"]["config"]
    # Configure its exists method for the artifact logging check
    mock_config_path.exists.return_value = True

    actor_logic.save_initial_config()

    # Assert get_config_path was called
    mock_dependencies["path_manager"].get_config_path.assert_called_once()

    # Assert save_config_json was called with the correct path mock
    mock_dependencies["serializer"].save_config_json.assert_called_once_with(
        mock_dependencies["config"].model_dump(), mock_config_path
    )
    # Check artifact logging
    mock_dependencies["mlflow_client"].log_artifact.assert_any_call(
        mock_dependencies["mlflow_run_id"],
        str(mock_config_path),
        artifact_path="config",
    )


def test_logic_save_training_state_no_buffer(
    actor_logic: ActorLogic,
    mock_dependencies,
    dummy_checkpoint_data: CheckpointData,
):
    """Test saving state without the buffer."""
    step = dummy_checkpoint_data.global_step
    nn_state = dummy_checkpoint_data.model_state_dict
    opt_state = dummy_checkpoint_data.optimizer_state_dict
    actor_state_data = mock_dependencies["actor_state"].get_persistable_state()
    # Get the mock path objects
    mock_cp_path_step = mock_dependencies["path_manager"].get_checkpoint_path(step=step)
    mock_cp_path_latest = mock_dependencies["path_manager"].get_checkpoint_path(
        is_latest=True
    )
    # Configure exists for artifact logging checks
    mock_cp_path_step.exists.return_value = True
    mock_cp_path_latest.exists.return_value = True

    actor_logic.save_training_state(
        nn_state_dict=nn_state,
        optimizer_state_dict=opt_state,
        buffer_content=[],  # Empty buffer content
        global_step=step,
        episodes_played=dummy_checkpoint_data.episodes_played,
        total_simulations_run=dummy_checkpoint_data.total_simulations_run,
        actor_state_data=actor_state_data,
        is_best=False,
        save_buffer=False,  # Explicitly false
        model_config_dict=dummy_checkpoint_data.model_config_dict,
        env_config_dict=dummy_checkpoint_data.env_config_dict,
        user_data=dummy_checkpoint_data.user_data,
    )

    # Verify checkpoint save
    mock_dependencies["serializer"].save_checkpoint.assert_called_once()
    saved_cp_data = mock_dependencies["serializer"].save_checkpoint.call_args[0][0]
    assert isinstance(saved_cp_data, CheckpointData)
    assert saved_cp_data.global_step == step
    assert saved_cp_data.model_state_dict == nn_state
    assert saved_cp_data.optimizer_state_dict == opt_state  # Serializer handles prep
    assert saved_cp_data.actor_state == actor_state_data

    # Verify buffer NOT saved
    mock_dependencies["serializer"].save_buffer.assert_not_called()

    # Verify links updated (only latest) - check with keyword arg
    mock_dependencies["path_manager"].update_checkpoint_links.assert_called_once_with(
        mock_cp_path_step, is_best=False
    )
    mock_dependencies["path_manager"].update_buffer_link.assert_not_called()

    # Verify artifact logging (only checkpoint and latest link)
    mock_dependencies["mlflow_client"].log_artifact.assert_any_call(
        mock_dependencies["mlflow_run_id"],
        str(mock_cp_path_step),
        artifact_path="checkpoints",
    )
    mock_dependencies["mlflow_client"].log_artifact.assert_any_call(
        mock_dependencies["mlflow_run_id"],
        str(mock_cp_path_latest),
        artifact_path="checkpoints",
    )
    # Ensure buffer artifact was NOT logged
    assert not any(
        call.kwargs.get("artifact_path") == "buffers"
        for call in mock_dependencies["mlflow_client"].log_artifact.call_args_list
    )


def test_logic_save_training_state_with_buffer(
    actor_logic: ActorLogic,
    mock_dependencies,
    dummy_checkpoint_data: CheckpointData,
    dummy_buffer_data: BufferData,
):
    """Test saving state including the buffer."""
    step = dummy_checkpoint_data.global_step
    nn_state = dummy_checkpoint_data.model_state_dict
    opt_state = dummy_checkpoint_data.optimizer_state_dict
    buffer_content = dummy_buffer_data.buffer_list
    actor_state_data = mock_dependencies["actor_state"].get_persistable_state()
    # Get mock path objects
    mock_cp_path_step = mock_dependencies["path_manager"].get_checkpoint_path(step=step)
    mock_buf_path_step = mock_dependencies["path_manager"].get_buffer_path(step=step)
    mock_cp_path_latest = mock_dependencies["path_manager"].get_checkpoint_path(
        is_latest=True
    )
    mock_cp_path_best = mock_dependencies["path_manager"].get_checkpoint_path(
        is_best=True
    )  # Assume side effect handles this
    mock_buf_path_default = mock_dependencies["path_manager"].get_buffer_path()
    # Configure exists for artifact logging checks
    mock_cp_path_step.exists.return_value = True
    mock_buf_path_step.exists.return_value = True
    mock_cp_path_latest.exists.return_value = True
    mock_cp_path_best.exists.return_value = True
    mock_buf_path_default.exists.return_value = True

    actor_logic.save_training_state(
        nn_state_dict=nn_state,
        optimizer_state_dict=opt_state,
        buffer_content=buffer_content,
        global_step=step,
        episodes_played=dummy_checkpoint_data.episodes_played,
        total_simulations_run=dummy_checkpoint_data.total_simulations_run,
        actor_state_data=actor_state_data,
        is_best=True,  # Test best link
        save_buffer=True,  # Explicitly true
        model_config_dict=dummy_checkpoint_data.model_config_dict,
        env_config_dict=dummy_checkpoint_data.env_config_dict,
        user_data=dummy_checkpoint_data.user_data,
    )

    # Verify checkpoint save
    mock_dependencies["serializer"].save_checkpoint.assert_called_once()
    saved_cp_data = mock_dependencies["serializer"].save_checkpoint.call_args[0][0]
    assert isinstance(saved_cp_data, CheckpointData)
    assert saved_cp_data.global_step == step

    # Verify buffer save
    mock_dependencies["serializer"].save_buffer.assert_called_once()
    saved_buf_data = mock_dependencies["serializer"].save_buffer.call_args[0][0]
    assert isinstance(saved_buf_data, BufferData)
    assert saved_buf_data.buffer_list == buffer_content

    # Verify links updated (latest and best) - check with keyword arg
    mock_dependencies["path_manager"].update_checkpoint_links.assert_called_once_with(
        mock_cp_path_step, is_best=True
    )
    mock_dependencies["path_manager"].update_buffer_link.assert_called_once_with(
        mock_buf_path_step
    )

    # Verify artifact logging (checkpoint, latest, best, buffer, buffer link)
    mock_dependencies["mlflow_client"].log_artifact.assert_any_call(
        mock_dependencies["mlflow_run_id"],
        str(mock_cp_path_step),
        artifact_path="checkpoints",
    )
    mock_dependencies["mlflow_client"].log_artifact.assert_any_call(
        mock_dependencies["mlflow_run_id"],
        str(mock_cp_path_latest),
        artifact_path="checkpoints",
    )
    # Note: get_checkpoint_path side effect needs to handle is_best=True to return a distinct mock if needed
    # For now, assume it returns the same mock or configure side_effect more elaborately if needed.
    mock_dependencies["mlflow_client"].log_artifact.assert_any_call(
        mock_dependencies["mlflow_run_id"],
        str(
            mock_cp_path_best
        ),  # This might be same object as mock_cp_path_latest depending on side_effect
        artifact_path="checkpoints",
    )
    mock_dependencies["mlflow_client"].log_artifact.assert_any_call(
        mock_dependencies["mlflow_run_id"],
        str(mock_buf_path_step),
        artifact_path="buffers",
    )
    mock_dependencies["mlflow_client"].log_artifact.assert_any_call(
        mock_dependencies["mlflow_run_id"],
        str(mock_buf_path_default),
        artifact_path="buffers",
    )


def test_logic_load_initial_state_found(
    actor_logic: ActorLogic,
    mock_dependencies,
    dummy_checkpoint_data: CheckpointData,
    dummy_buffer_data: BufferData,
):
    """Test loading state when checkpoint and buffer are found in previous run."""
    previous_run = "previous_run_123"
    # Mock PathManager to simulate finding the previous run
    mock_dependencies["path_manager"].find_latest_run_dir.return_value = previous_run
    # Get the MOCK paths PathManager would generate
    mock_cp_path = mock_dependencies["path_manager"].get_checkpoint_path(
        run_name=previous_run, is_latest=True
    )
    mock_buf_path = mock_dependencies["path_manager"].get_buffer_path(
        run_name=previous_run
    )

    # Configure the exists method on the MOCK paths
    mock_cp_path.exists.return_value = True
    mock_buf_path.exists.return_value = True
    # Configure resolve to return the same mock object
    mock_cp_path.resolve.return_value = mock_cp_path
    mock_buf_path.resolve.return_value = mock_buf_path

    # Configure serializer mocks to return data when called with the determined paths
    mock_dependencies["serializer"].load_checkpoint.return_value = dummy_checkpoint_data
    mock_dependencies["serializer"].load_buffer.return_value = dummy_buffer_data

    # Execute the logic
    loaded_state = actor_logic.load_initial_state()

    # Verify PathManager was asked to find the latest run
    mock_dependencies["path_manager"].find_latest_run_dir.assert_called_once()

    # Verify exists was called on the MOCK paths
    mock_cp_path.exists.assert_called_once()
    mock_buf_path.exists.assert_called_once()

    # Verify resolve was called (because exists returned True)
    mock_cp_path.resolve.assert_called_once()
    mock_buf_path.resolve.assert_called_once()

    # Verify serializer load methods were called with the MOCK paths (which resolve to themselves)
    mock_dependencies["serializer"].load_checkpoint.assert_called_once_with(
        mock_cp_path
    )
    mock_dependencies["serializer"].load_buffer.assert_called_once_with(mock_buf_path)

    # Verify actor state was restored
    mock_dependencies["actor_state"].restore_from_state.assert_called_once_with(
        dummy_checkpoint_data.actor_state
    )

    # Verify returned state
    assert loaded_state is not None
    assert loaded_state.checkpoint_data == dummy_checkpoint_data
    assert loaded_state.buffer_data == dummy_buffer_data


def test_logic_load_initial_state_not_found(actor_logic: ActorLogic, mock_dependencies):
    """Test loading state when no previous run or files are found."""
    # Mock PathManager to simulate finding a previous run
    mock_dependencies[
        "path_manager"
    ].find_latest_run_dir.return_value = "previous_run_123"
    # Get the MOCK paths PathManager would generate
    mock_cp_path = mock_dependencies["path_manager"].get_checkpoint_path(
        run_name="previous_run_123", is_latest=True
    )
    mock_buf_path = mock_dependencies["path_manager"].get_buffer_path(
        run_name="previous_run_123"
    )

    # Configure the exists method on the MOCK paths to return False
    mock_cp_path.exists.return_value = False
    mock_buf_path.exists.return_value = False

    # Execute the logic
    loaded_state = actor_logic.load_initial_state()

    # Verify PathManager was asked to find the latest run
    mock_dependencies["path_manager"].find_latest_run_dir.assert_called_once()

    # Verify exists was called on the MOCK paths
    mock_cp_path.exists.assert_called_once()
    # Buffer path check might be skipped if checkpoint doesn't exist, depending on exact logic flow.
    # Current implementation checks buffer path based on checkpoint_run_name, which is None if cp load fails.
    # Then it checks based on latest_previous_run_name. So it *should* be called.
    mock_buf_path.exists.assert_called_once()

    # Verify resolve was NOT called (because exists returned False)
    mock_cp_path.resolve.assert_not_called()
    mock_buf_path.resolve.assert_not_called()

    # Verify serializer load methods were NOT called
    mock_dependencies["serializer"].load_checkpoint.assert_not_called()
    mock_dependencies["serializer"].load_buffer.assert_not_called()

    # Verify actor state was NOT restored
    mock_dependencies["actor_state"].restore_from_state.assert_not_called()

    # Verify returned state is empty
    assert loaded_state is not None
    assert loaded_state.checkpoint_data is None
    assert loaded_state.buffer_data is None
