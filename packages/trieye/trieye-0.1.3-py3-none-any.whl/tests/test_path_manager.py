# File: trieye/tests/test_path_manager.py
import time

import pytest

from trieye.config import PersistenceConfig
from trieye.path_manager import PathManager


@pytest.fixture
def path_manager(base_persist_config: PersistenceConfig) -> PathManager:
    """Provides a PathManager instance using the base temporary config."""
    # Ensure the run name is set for the test instance
    base_persist_config.RUN_NAME = "pm_test_run"
    base_persist_config.APP_NAME = "pm_test_app"
    pm = PathManager(base_persist_config)
    pm.create_run_directories()  # Create dirs for the test
    return pm


def test_directory_creation(
    path_manager: PathManager, base_persist_config: PersistenceConfig
):
    """Test if standard directories are created."""
    pm = path_manager
    assert pm.root_data_dir.exists()
    assert pm.app_root_dir.exists()
    assert pm.run_base_dir.exists()
    assert pm.checkpoint_dir.exists()
    assert pm.buffer_dir.exists()
    assert pm.log_dir.exists()
    assert pm.tb_log_dir.exists()
    assert pm.profile_dir.exists()

    assert pm.app_root_dir.name == base_persist_config.APP_NAME
    assert pm.run_base_dir.name == base_persist_config.RUN_NAME


def test_get_paths(path_manager: PathManager, base_persist_config: PersistenceConfig):
    """Test path generation methods."""
    pm = path_manager
    step = 123

    cp_path = pm.get_checkpoint_path(step=step)
    assert cp_path.name == f"checkpoint_step_{step}.pkl"
    assert cp_path.parent == pm.checkpoint_dir

    latest_cp_path = pm.get_checkpoint_path(is_latest=True)
    assert latest_cp_path.name == base_persist_config.LATEST_CHECKPOINT_FILENAME
    assert latest_cp_path.parent == pm.checkpoint_dir

    buf_path = pm.get_buffer_path(step=step)
    assert buf_path.name == f"buffer_step_{step}.pkl"
    assert buf_path.parent == pm.buffer_dir

    default_buf_path = pm.get_buffer_path()
    assert default_buf_path.name == base_persist_config.BUFFER_FILENAME
    assert default_buf_path.parent == pm.buffer_dir

    config_path = pm.get_config_path()
    assert config_path.name == base_persist_config.CONFIG_FILENAME
    assert config_path.parent == pm.run_base_dir

    profile_path = pm.get_profile_path(worker_id=0, episode_seed=456)
    assert profile_path.name == "worker_0_ep_456.prof"
    assert profile_path.parent == pm.profile_dir


def test_find_latest_run_dir(
    path_manager: PathManager, base_persist_config: PersistenceConfig
):
    """Test finding the latest previous run directory."""
    pm = path_manager
    app_runs_dir = base_persist_config.get_runs_root_dir()

    # Create dummy run directories with timestamps
    ts_now = time.strftime("%Y%m%d_%H%M%S")
    time.sleep(1.1)
    ts_latest = time.strftime("%Y%m%d_%H%M%S")
    time.sleep(1.1)
    ts_older = time.strftime("%Y%m%d_%H%M%S")  # This is actually the latest timestamp

    current_run = f"run_{ts_now}_current"
    latest_prev_run = f"run_{ts_latest}_latest"  # Middle timestamp
    older_run = f"run_{ts_older}_older"  # Latest timestamp among previous
    no_ts_run = "run_no_timestamp"

    (app_runs_dir / current_run).mkdir()
    (app_runs_dir / latest_prev_run).mkdir()
    (app_runs_dir / older_run).mkdir()
    (app_runs_dir / no_ts_run).mkdir()
    (app_runs_dir / "not_a_run_dir.txt").touch()  # Add a file

    # Update PathManager's current run name to simulate being in 'current_run'
    pm.persist_config.RUN_NAME = current_run
    pm._update_paths()  # Update internal paths

    found_latest = pm.find_latest_run_dir(current_run_name=current_run)

    # The latest *previous* run should be the one with the latest timestamp
    assert found_latest == older_run


def test_find_latest_run_dir_no_previous(path_manager: PathManager):
    """Test finding latest run when no other valid runs exist."""
    found_latest = path_manager.find_latest_run_dir(
        current_run_name=path_manager.persist_config.RUN_NAME
    )
    assert found_latest is None
