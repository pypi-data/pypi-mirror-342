# File: trieye/actor.py
import logging
import threading
import time
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock  # Import MagicMock

import mlflow
import ray
from mlflow.tracking import MlflowClient
from torch.utils.tensorboard import SummaryWriter

# Use relative imports within trieye
from .actor_logic import ActorLogic
from .actor_state import ActorState
from .config import TrieyeConfig
from .exceptions import ConfigurationError
from .path_manager import PathManager
from .schemas import LoadedTrainingState, RawMetricEvent
from .serializer import Serializer

# Initialize logger at module level
logger = logging.getLogger(__name__)


@ray.remote(max_restarts=-1)
class TrieyeActor:
    """
    Ray actor combining statistics collection/processing and data persistence.
    Manages MLflow runs, TensorBoard logging, checkpointing, and buffer saving.
    Delegates logic to ActorState and ActorLogic.

    Allows injection of components for testing purposes via _setup_mock_dependencies.
    """

    def __init__(
        self,
        config: TrieyeConfig,
        # --- Dependencies are initially None, set via _setup_mock_dependencies or initialized ---
        _path_manager: PathManager | None = None,
        _serializer: Serializer | None = None,
        _actor_state: ActorState | None = None,
        # Constructor injection is less preferred now due to serialization issues
        _mlflow_client: MlflowClient | None = None,
        _tb_writer: SummaryWriter | None = None,
    ):
        global logger
        logger = logging.getLogger(__name__)

        self.config = config
        self._lock = threading.Lock()

        self.path_manager = _path_manager or PathManager(self.config.persistence)
        self.serializer = _serializer or Serializer()
        self.actor_state = _actor_state or ActorState()

        # --- Tracking Initialization ---
        self.mlflow_client: MlflowClient | MagicMock | None = _mlflow_client
        self.tb_writer: SummaryWriter | MagicMock | None = _tb_writer
        self.mlflow_run_id: str | None = None
        self.tb_log_dir: Path | None = (
            self.path_manager.tb_log_dir
        )  # Get path initially

        # Initialize tracking only if mocks weren't directly injected
        if _mlflow_client is None and _tb_writer is None:
            self._initialize_tracking()
        elif _mlflow_client:
            if hasattr(_mlflow_client, "_mock_run_id"):  # Handle injected mock
                self.mlflow_run_id = _mlflow_client._mock_run_id  # type: ignore[attr-defined]
            logger.info("Using constructor-injected MLflow client.")
        if _tb_writer:
            if hasattr(_tb_writer, "log_dir") and _tb_writer.log_dir:
                self.tb_log_dir = Path(_tb_writer.log_dir)
            logger.info("Using constructor-injected TensorBoard writer.")

        # Initialize logic handler
        self.logic = ActorLogic(
            config=self.config,
            actor_state=self.actor_state,
            path_manager=self.path_manager,
            serializer=self.serializer,
            mlflow_run_id=self.mlflow_run_id,
            mlflow_client=self.mlflow_client,  # type: ignore[arg-type] # Allow MagicMock
            tb_writer=self.tb_writer,  # type: ignore[arg-type] # Allow MagicMock
        )

        # --- File Logging ---
        self.log_file_path = (
            self.path_manager.log_dir / f"{self.config.run_name}_trieye.log"
        )
        self._file_handler: logging.FileHandler | None = None
        if (
            _path_manager is None
        ):  # Only setup if not testing with injected path manager
            self._setup_file_logging()
            self._log_paths_to_mlflow()

        # --- Final Setup ---
        if (
            _path_manager is None
        ):  # Only setup if not testing with injected path manager
            self.path_manager.create_run_directories()
            self.logic.save_initial_config()

        logger.info(
            f"TrieyeActor initialized for App: '{self.config.app_name}', Run: '{self.config.run_name}'. "
            f"MLflow Run ID: {self.mlflow_run_id}. Data Root: {self.path_manager.root_data_dir}"
        )

    def _initialize_tracking(self):
        """Initializes MLflow run and TensorBoard writer. Only called if not injected."""
        # MLflow
        try:
            mlflow_uri = self.config.persistence.MLFLOW_TRACKING_URI
            mlflow.set_tracking_uri(mlflow_uri)
            mlflow.set_experiment(self.config.app_name)
            active_run = mlflow.active_run()
            if not active_run:
                run = mlflow.start_run(run_name=self.config.run_name)
                self.mlflow_run_id = run.info.run_id
            else:
                self.mlflow_run_id = active_run.info.run_id
                run_name_tag = (
                    active_run.data.tags.get("mlflow.runName")
                    if active_run.data
                    else None
                )
                if run_name_tag != self.config.run_name:
                    logger.warning(
                        f"TrieyeActor joining existing MLflow run '{self.mlflow_run_id}' "
                        f"with name '{run_name_tag}' "
                        f"instead of configured name '{self.config.run_name}'."
                    )

            if self.mlflow_run_id:
                self.mlflow_client = MlflowClient()
                logger.info(f"Using MLflow run: {self.mlflow_run_id}")
                if hasattr(self, "logic") and self.logic:
                    self.logic.mlflow_client = self.mlflow_client
                    self.logic.mlflow_run_id = self.mlflow_run_id
                    if self.logic.stats_processor:
                        self.logic.stats_processor.mlflow_client = self.mlflow_client
                        self.logic.stats_processor.mlflow_run_id = self.mlflow_run_id
            else:
                logger.error("Failed to start or get active MLflow run.")
        except Exception as e:
            logger.error(f"Failed to initialize MLflow: {e}", exc_info=True)
            self.mlflow_run_id = None
            self.mlflow_client = None

        # TensorBoard
        if self.tb_log_dir:
            try:
                self.tb_writer = SummaryWriter(log_dir=str(self.tb_log_dir))
                logger.info(f"TensorBoard writer initialized at {self.tb_log_dir}")
                if hasattr(self, "logic") and self.logic:
                    self.logic.tb_writer = self.tb_writer
                    if self.logic.stats_processor:
                        self.logic.stats_processor.tb_writer = self.tb_writer
            except Exception as e:
                logger.error(f"Failed to initialize TensorBoard writer: {e}")
        else:
            logger.warning("TensorBoard log directory path is not set.")

    def _setup_mock_dependencies(self, mock_mlflow_run_id: str, mock_tb_log_dir: str):
        """
        Creates MagicMock instances for dependencies *within* the actor process.
        Called remotely by test fixtures. Avoids serializing mocks.
        """
        logger.info(
            f"Setting up mock dependencies internally with run_id: {mock_mlflow_run_id}"
        )
        # Create mock MLflow client
        self.mlflow_client = MagicMock(spec=MlflowClient)
        self.mlflow_client.log_metric = MagicMock(side_effect=None)
        self.mlflow_client.log_param = MagicMock(side_effect=None)
        self.mlflow_client.log_artifact = MagicMock(side_effect=None)
        self.mlflow_client.log_artifacts = MagicMock(side_effect=None)
        self.mlflow_client._mock_run_id = mock_mlflow_run_id  # Store the ID if needed
        self.mlflow_run_id = mock_mlflow_run_id

        # Create mock TensorBoard writer
        self.tb_writer = MagicMock(spec=SummaryWriter)
        self.tb_writer.add_scalar = MagicMock()
        self.tb_writer.flush = MagicMock()
        self.tb_writer.close = MagicMock()
        self.tb_writer.log_dir = mock_tb_log_dir  # Set log_dir attribute
        self.tb_log_dir = Path(mock_tb_log_dir)

        # Update the logic handler's references
        if hasattr(self, "logic") and self.logic:
            self.logic.mlflow_client = self.mlflow_client
            self.logic.tb_writer = self.tb_writer
            self.logic.mlflow_run_id = self.mlflow_run_id
            # Update stats processor's client too
            if self.logic.stats_processor:
                self.logic.stats_processor.mlflow_client = self.mlflow_client
                self.logic.stats_processor.mlflow_run_id = self.mlflow_run_id
                self.logic.stats_processor.tb_writer = self.tb_writer
        logger.info("Internal mock dependencies set.")
        # Return the run ID to confirm setup
        return self.mlflow_run_id

    def _log_paths_to_mlflow(self):
        """Logs relevant paths to MLflow parameters if client is available."""
        if (
            not self.mlflow_client
            or not self.mlflow_run_id
            or isinstance(self.mlflow_client, MagicMock)
        ):
            # Skip if client is a mock or not available
            return

        paths_to_log = {
            "tensorboard_log_dir": self.tb_log_dir,
            "trieye_log_file": self.log_file_path,
        }

        for key, path_obj in paths_to_log.items():
            if path_obj:
                try:
                    rel_path = path_obj.relative_to(self.path_manager.app_root_dir)
                    path_str = str(rel_path)
                except ValueError:
                    path_str = str(path_obj)
                except Exception as e:
                    logger.error(
                        f"Error processing path for MLflow logging ({key}): {e}"
                    )
                    path_str = f"Error: {e}"
                try:
                    # Ensure client is not the mock before calling
                    if self.mlflow_client and not isinstance(
                        self.mlflow_client, MagicMock
                    ):
                        self.mlflow_client.log_param(self.mlflow_run_id, key, path_str)
                except Exception as log_e:
                    logger.error(f"Failed to log {key} param to MLflow: {log_e}")

    def _setup_file_logging(self):
        """Sets up file logging for this actor. Only called if not injected."""
        try:
            self.log_file_path.parent.mkdir(parents=True, exist_ok=True)
            self._file_handler = logging.FileHandler(self.log_file_path, mode="a")
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - [TrieyeActor] - %(message)s"
            )
            self._file_handler.setFormatter(formatter)
            actor_instance_logger = logging.getLogger(__name__)
            if not any(
                isinstance(h, logging.FileHandler)
                and h.baseFilename == str(self.log_file_path)
                for h in actor_instance_logger.handlers
            ):
                actor_instance_logger.addHandler(self._file_handler)
                actor_instance_logger.setLevel(logging.INFO)
                actor_instance_logger.propagate = False

            logger.info(f"TrieyeActor file logging configured at: {self.log_file_path}")
        except Exception as e:
            logger.error(f"Failed to set up file logging for TrieyeActor: {e}")

    # --- Statistics Methods (Delegate to ActorState/ActorLogic) ---

    def log_event(self, event: RawMetricEvent):
        """Logs a single raw metric event."""
        if not isinstance(event, RawMetricEvent):
            logger.warning(f"Received non-RawMetricEvent object: {type(event)}")
            return
        if not event.is_valid():
            logger.warning(f"Received invalid (non-finite value) event: {event}")
            return

        with self._lock:
            self.actor_state.add_event(event)
        logger.debug(f"Logged event: {event.name}, Step: {event.global_step}")

    def log_batch_events(self, events: list[RawMetricEvent]):
        """Logs a batch of raw metric events."""
        valid_events = []
        for i, event in enumerate(events):
            if not isinstance(event, RawMetricEvent):
                logger.warning(
                    f"Skipping non-RawMetricEvent object in batch at index {i}: {type(event)}"
                )
                continue
            if not event.is_valid():
                logger.warning(
                    f"Skipping invalid (non-finite value) event in batch at index {i}: {event}"
                )
                continue
            valid_events.append(event)

        if not valid_events:
            logger.debug("No valid events in batch to log.")
            return

        with self._lock:
            for event in valid_events:
                self.actor_state.add_event(event)
        logger.debug(f"Logged batch of {len(valid_events)} valid events.")

    def process_and_log(self, current_global_step: int):
        """Processes buffered raw data and logs aggregated metrics based on time interval."""
        now = time.monotonic()
        with self._lock:
            last_processed_time = self.actor_state.get_last_processed_time()
            should_process = (
                now - last_processed_time
                >= self.config.stats.processing_interval_seconds
            )
            if not should_process:
                return

            data_to_process, max_step_processed = self.actor_state.get_data_to_process(
                current_global_step
            )
            if not data_to_process:
                self.actor_state.update_last_processed_time(now)
                return
            context = self.actor_state.get_log_context(current_global_step, now)

        try:
            if not hasattr(self, "logic") or self.logic is None:
                raise ConfigurationError(
                    "ActorLogic not initialized in process_and_log."
                )
            self.logic.process_and_log_metrics(data_to_process, context)
        except Exception as e:
            logger.error(f"Error during stats processing: {e}", exc_info=True)
            with self._lock:
                self.actor_state.update_last_processed_time(now)
            return

        with self._lock:
            self.actor_state.clear_processed_data(data_to_process.keys())
            self.actor_state.update_last_processed_step(max_step_processed)
            self.actor_state.update_last_processed_time(now)

    def force_process_and_log(self, current_global_step: int):
        """Forces processing and logging, bypassing time interval."""
        logger.info(f"Forcing stats processing up to step {current_global_step}.")
        now = time.monotonic()
        with self._lock:
            data_to_process, max_step_processed = self.actor_state.get_data_to_process(
                current_global_step
            )
            if not data_to_process:
                logger.info("No data to process in force_process_and_log.")
                self.actor_state.update_last_processed_time(now)
                return
            context = self.actor_state.get_log_context(current_global_step, now)

        try:
            if not hasattr(self, "logic") or self.logic is None:
                raise ConfigurationError(
                    "ActorLogic not initialized in force_process_and_log."
                )
            self.logic.process_and_log_metrics(data_to_process, context)
        except Exception as e:
            logger.error(f"Error during forced stats processing: {e}", exc_info=True)
            with self._lock:
                self.actor_state.update_last_processed_time(now)
            return

        with self._lock:
            self.actor_state.clear_processed_data(data_to_process.keys())
            self.actor_state.update_last_processed_step(max_step_processed)
            self.actor_state.update_last_processed_time(now)

    # --- Data Persistence Methods (Delegate to ActorLogic) ---

    def load_initial_state(
        self, _auto_resume_run_name: str | None = None
    ) -> LoadedTrainingState:
        """Loads the initial training state (checkpoint and buffer)."""
        if not hasattr(self, "logic") or self.logic is None:
            logger.error("ActorLogic not initialized in load_initial_state.")
            return LoadedTrainingState(checkpoint_data=None, buffer_data=None)
        return self.logic.load_initial_state(
            _auto_resume_run_name=_auto_resume_run_name
        )

    def save_training_state(
        self,
        nn_state_dict: dict[str, Any],
        optimizer_state_dict: dict[str, Any],
        buffer_content: list[Any],
        global_step: int,
        episodes_played: int,
        total_simulations_run: int,
        is_best: bool = False,
        save_buffer: bool = False,
        model_config_dict: dict | None = None,
        env_config_dict: dict | None = None,
        user_data: dict | None = None,
    ):
        """Saves the training state (checkpoint and optionally buffer)."""
        if not hasattr(self, "logic") or self.logic is None:
            logger.error("ActorLogic not initialized in save_training_state.")
            return

        actor_state_data = self.get_state()
        self.logic.save_training_state(
            nn_state_dict=nn_state_dict,
            optimizer_state_dict=optimizer_state_dict,
            buffer_content=buffer_content,
            global_step=global_step,
            episodes_played=episodes_played,
            total_simulations_run=total_simulations_run,
            actor_state_data=actor_state_data,
            is_best=is_best,
            save_buffer=save_buffer,
            model_config_dict=model_config_dict,
            env_config_dict=env_config_dict,
            user_data=user_data,
        )

    def save_run_config(self, configs: dict[str, Any]):
        """Saves the combined configuration dictionary as a JSON artifact."""
        if not hasattr(self, "logic") or self.logic is None:
            logger.error("ActorLogic not initialized in save_run_config.")
            return
        self.logic.save_run_config(configs)

    # --- State Management (Delegate to ActorState) ---

    def get_state(self) -> dict[str, Any]:
        """Returns the internal state for saving (minimal stats state)."""
        with self._lock:
            return self.actor_state.get_persistable_state()

    def set_state(self, state: dict[str, Any]):
        """Restores the internal state from saved data."""
        with self._lock:
            self.actor_state.restore_from_state(state)
        logger.info(
            f"TrieyeActor state restored. Last processed step: {self.actor_state.get_last_processed_step()}"
        )

    # --- Utility Methods ---

    def get_mlflow_run_id(self) -> str | None:
        """Returns the active MLflow run ID."""
        return self.mlflow_run_id

    def get_run_base_dir_str(self) -> str:
        """Returns the run base directory path as a string."""
        return str(self.path_manager.run_base_dir)

    def get_config(self) -> TrieyeConfig:
        """Returns the actor's configuration."""
        return self.config.model_copy(deep=True)

    def close_tb_writer(self):
        """Closes the TensorBoard writer if it exists."""
        if self.tb_writer:
            try:
                self.tb_writer.flush()
                self.tb_writer.close()
                logger.info("TrieyeActor: TensorBoard writer closed.")
                self.tb_writer = None
                if hasattr(self, "logic") and self.logic:
                    self.logic.tb_writer = None
                    if self.logic.stats_processor:
                        self.logic.stats_processor.tb_writer = None
            except Exception as e:
                logger.error(f"TrieyeActor: Error closing TensorBoard writer: {e}")

    def shutdown(self):
        """Gracefully shuts down the actor's resources."""
        logger.info("TrieyeActor shutdown requested.")
        last_step = -1
        max_buffered_step = -1
        try:
            with self._lock:
                last_step = self.actor_state.get_last_processed_step()
                if self.actor_state._raw_data_buffer:
                    max_buffered_step = max(self.actor_state._raw_data_buffer.keys())
        except Exception as e:
            logger.warning(f"Error getting final step during shutdown: {e}")
        final_step = max(last_step, max_buffered_step, 0) + 1

        try:
            self.force_process_and_log(current_global_step=final_step)
        except Exception as e:
            logger.error(f"Error during final forced processing in shutdown: {e}")

        self.close_tb_writer()

        if self._file_handler:
            try:
                self._file_handler.flush()
                self._file_handler.close()
                actor_instance_logger = logging.getLogger(__name__)
                actor_instance_logger.removeHandler(self._file_handler)
                logger.info("TrieyeActor file logger closed and removed.")
                self._file_handler = None
            except Exception as e:
                logger.error(f"Error closing file logger: {e}")

        try:
            # Only end run if it's not a mock and was likely started by this actor
            if self.mlflow_run_id and not isinstance(self.mlflow_client, MagicMock):
                active_run = mlflow.active_run()
                if active_run and active_run.info.run_id == self.mlflow_run_id:
                    mlflow.end_run()
                    logger.info(f"Ended MLflow run: {self.mlflow_run_id}")
        except Exception as e:
            logger.warning(
                f"Could not automatically end MLflow run {self.mlflow_run_id} during shutdown: {e}"
            )

        logger.info("TrieyeActor shutdown complete.")
