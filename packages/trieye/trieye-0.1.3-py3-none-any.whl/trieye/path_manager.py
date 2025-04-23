# File: trieye/trieye/path_manager.py
import datetime
import logging
import re
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .config import PersistenceConfig  # Use relative import

logger = logging.getLogger(__name__)


class PathManager:
    """Manages file paths, directory creation, and discovery for runs."""

    def __init__(self, persist_config: "PersistenceConfig"):
        self.persist_config = persist_config
        self.root_data_dir = self.persist_config._get_absolute_root()
        self.app_root_dir = self.persist_config.get_app_root_dir()
        self._update_paths()

    def _update_paths(self):
        """Updates paths based on the current RUN_NAME in persist_config."""
        self.run_base_dir = self.persist_config.get_run_base_dir()
        self.checkpoint_dir = (
            self.run_base_dir / self.persist_config.CHECKPOINT_SAVE_DIR_NAME
        )
        self.buffer_dir = self.run_base_dir / self.persist_config.BUFFER_SAVE_DIR_NAME
        self.log_dir = self.run_base_dir / self.persist_config.LOG_DIR_NAME
        self.tb_log_dir = self.run_base_dir / self.persist_config.TENSORBOARD_DIR_NAME
        self.profile_dir = self.run_base_dir / self.persist_config.PROFILE_DIR_NAME
        self.config_path = self.run_base_dir / self.persist_config.CONFIG_FILENAME

    def create_run_directories(self):
        """Creates necessary directories for the current run."""
        self.app_root_dir.mkdir(parents=True, exist_ok=True)
        self.run_base_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.tb_log_dir.mkdir(parents=True, exist_ok=True)
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        if self.persist_config.SAVE_BUFFER:
            self.buffer_dir.mkdir(parents=True, exist_ok=True)

    def get_checkpoint_path(
        self,
        run_name: str | None = None,
        step: int | None = None,
        is_latest: bool = False,
        is_best: bool = False,
    ) -> Path:
        """Constructs the absolute path for a checkpoint file."""
        target_run_base_dir = self.persist_config.get_run_base_dir(run_name)
        checkpoint_dir = (
            target_run_base_dir / self.persist_config.CHECKPOINT_SAVE_DIR_NAME
        )
        if is_latest:
            filename = self.persist_config.LATEST_CHECKPOINT_FILENAME
        elif is_best:
            filename = self.persist_config.BEST_CHECKPOINT_FILENAME
        elif step is not None:
            filename = f"checkpoint_step_{step}.pkl"
        else:
            filename = self.persist_config.LATEST_CHECKPOINT_FILENAME
        return checkpoint_dir / Path(filename).with_suffix(".pkl")

    def get_buffer_path(
        self, run_name: str | None = None, step: int | None = None
    ) -> Path:
        """Constructs the absolute path for the replay buffer file."""
        target_run_base_dir = self.persist_config.get_run_base_dir(run_name)
        buffer_dir = target_run_base_dir / self.persist_config.BUFFER_SAVE_DIR_NAME
        if step is not None:
            filename = f"buffer_step_{step}.pkl"
        else:
            filename = self.persist_config.BUFFER_FILENAME
        return buffer_dir / Path(filename).with_suffix(".pkl")

    def get_config_path(self, run_name: str | None = None) -> Path:
        """Constructs the absolute path for the config JSON file."""
        target_run_base_dir = self.persist_config.get_run_base_dir(run_name)
        return target_run_base_dir / self.persist_config.CONFIG_FILENAME

    def get_profile_path(
        self, worker_id: int, episode_seed: int, run_name: str | None = None
    ) -> Path:
        """Constructs the absolute path for a profile data file."""
        target_run_base_dir = self.persist_config.get_run_base_dir(run_name)
        profile_dir = target_run_base_dir / self.persist_config.PROFILE_DIR_NAME
        filename = f"worker_{worker_id}_ep_{episode_seed}.prof"
        return profile_dir / filename

    def find_latest_run_dir(self, current_run_name: str) -> str | None:
        """Finds the most recent *previous* run directory based on timestamp."""
        runs_root_dir = self.persist_config.get_runs_root_dir()
        potential_runs: list[tuple[datetime.datetime, str]] = []
        run_name_pattern = re.compile(r"(\d{8}_\d{6})")
        logger.info(f"Searching for previous runs in: {runs_root_dir}")

        try:
            if not runs_root_dir.exists():
                return None
            for d in runs_root_dir.iterdir():
                if d.is_dir() and d.name != current_run_name:
                    match = run_name_pattern.search(d.name)
                    if match:
                        try:
                            run_time = datetime.datetime.strptime(
                                match.group(1), "%Y%m%d_%H%M%S"
                            )
                            potential_runs.append((run_time, d.name))
                        except ValueError:
                            # Ignore if parse fails
                            pass
            if not potential_runs:
                return None
            potential_runs.sort(key=lambda item: item[0], reverse=True)
            latest_run_name = potential_runs[0][1]
            logger.info(f"Selected latest previous run: {latest_run_name}")
            return latest_run_name
        except Exception as e:
            logger.error(f"Error finding latest run directory: {e}", exc_info=True)
            return None

    def determine_checkpoint_to_load(
        self, load_path_config: str | None, auto_resume: bool
    ) -> Path | None:
        """Determines the absolute path of the checkpoint file to load."""
        current_run_name = self.persist_config.RUN_NAME
        checkpoint_to_load: Path | None = None
        if load_path_config:
            load_path = Path(load_path_config).resolve()
            if load_path.exists():
                checkpoint_to_load = load_path
            else:
                logger.warning(
                    f"Specified checkpoint path not found: {load_path_config}"
                )
        if not checkpoint_to_load and auto_resume:
            latest_run_name = self.find_latest_run_dir(current_run_name)
            if latest_run_name:
                potential_latest_path = self.get_checkpoint_path(
                    run_name=latest_run_name, is_latest=True
                )
                if potential_latest_path.exists():
                    checkpoint_to_load = potential_latest_path.resolve()
                    logger.info(
                        f"Auto-resuming from latest checkpoint in '{latest_run_name}': {checkpoint_to_load}"
                    )
        if not checkpoint_to_load:
            logger.info("No checkpoint found to load.")
        return checkpoint_to_load

    def determine_buffer_to_load(
        self,
        load_path_config: str | None,
        auto_resume: bool,
        checkpoint_run_name: str | None,
    ) -> Path | None:
        """Determines the buffer file path to load."""
        buffer_to_load: Path | None = None
        if load_path_config:
            load_path = Path(load_path_config).resolve()
            if load_path.exists():
                buffer_to_load = load_path
            else:
                logger.warning(f"Specified buffer path not found: {load_path_config}")
        if not buffer_to_load and checkpoint_run_name:
            potential_buffer_path = self.get_buffer_path(run_name=checkpoint_run_name)
            if potential_buffer_path.exists():
                buffer_to_load = potential_buffer_path.resolve()
                logger.info(
                    f"Loading buffer from checkpoint run '{checkpoint_run_name}': {buffer_to_load}"
                )
        if not buffer_to_load and auto_resume and not checkpoint_run_name:
            latest_previous_run_name = self.find_latest_run_dir(
                self.persist_config.RUN_NAME
            )
            if latest_previous_run_name:
                potential_buffer_path = self.get_buffer_path(
                    run_name=latest_previous_run_name
                )
                if potential_buffer_path.exists():
                    buffer_to_load = potential_buffer_path.resolve()
                    logger.info(
                        f"Auto-resuming buffer from latest previous run '{latest_previous_run_name}': {buffer_to_load}"
                    )
        if not buffer_to_load:
            logger.info("No suitable buffer file found to load.")
        return buffer_to_load

    def update_checkpoint_links(self, step_checkpoint_path: Path, is_best: bool):
        """Updates the 'latest' and optionally 'best' checkpoint links."""
        if not step_checkpoint_path.exists():
            return
        latest_path = self.get_checkpoint_path(is_latest=True)
        best_path = self.get_checkpoint_path(is_best=True)
        try:
            shutil.copy2(step_checkpoint_path, latest_path)
        except Exception as e:
            logger.error(f"Failed to update latest checkpoint link: {e}")
        if is_best:
            try:
                shutil.copy2(step_checkpoint_path, best_path)
            except Exception as e:
                logger.error(f"Failed to update best checkpoint link: {e}")

    def update_buffer_link(self, step_buffer_path: Path):
        """Updates the default buffer link ('buffer.pkl')."""
        if not step_buffer_path.exists():
            return
        default_buffer_path = self.get_buffer_path()
        try:
            shutil.copy2(step_buffer_path, default_buffer_path)
        except Exception as e:
            logger.error(f"Error updating default buffer file link: {e}")
