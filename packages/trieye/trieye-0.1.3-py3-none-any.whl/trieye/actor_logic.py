# File: trieye/actor_logic.py
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

from mlflow.tracking import MlflowClient
from torch.utils.tensorboard import SummaryWriter

# Use relative imports within trieye
from .actor_state import ActorState
from .exceptions import ConfigurationError, ProcessingError, SerializationError
from .path_manager import PathManager
from .schemas import (
    BufferData,
    CheckpointData,
    LoadedTrainingState,
    LogContext,
    RawMetricEvent,
)
from .serializer import Serializer
from .stats_processor import StatsProcessor

if TYPE_CHECKING:
    from .config import TrieyeConfig

logger = logging.getLogger(__name__)


class ActorLogic:
    """
    Encapsulates the core logic for statistics processing, persistence,
    and interactions between components, independent of Ray actor specifics.
    Owned and used by the TrieyeActor.
    """

    def __init__(
        self,
        config: "TrieyeConfig",
        actor_state: ActorState,
        path_manager: PathManager,
        serializer: Serializer,
        mlflow_run_id: str | None,
        mlflow_client: MlflowClient | None,
        tb_writer: SummaryWriter | None,
    ):
        self.config = config
        self.actor_state = actor_state
        self.path_manager = path_manager
        self.serializer = serializer
        self.mlflow_run_id = mlflow_run_id
        self.mlflow_client = mlflow_client
        self.tb_writer = tb_writer

        # Initialize StatsProcessor here, passing dependencies
        self.stats_processor = StatsProcessor(
            config=self.config.stats,
            run_name=self.config.run_name,
            tb_writer=self.tb_writer,
            mlflow_run_id=self.mlflow_run_id,
            _mlflow_client=self.mlflow_client,  # Pass client
        )
        logger.info("ActorLogic initialized.")

    def process_and_log_metrics(
        self, raw_data: dict[int, dict[str, list[RawMetricEvent]]], context: LogContext
    ):
        """Delegates processing and logging to the StatsProcessor."""
        if not self.stats_processor:
            logger.error("StatsProcessor not initialized in ActorLogic.")
            raise ConfigurationError("StatsProcessor not available.")
        try:
            self.stats_processor.process_and_log(raw_data, context)
        except ProcessingError as e:
            logger.error(f"Error during metric processing: {e}", exc_info=True)
            # Re-raise or handle as appropriate
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error during metric processing: {e}", exc_info=True
            )
            raise ProcessingError("Unexpected error in process_and_log_metrics") from e

    def load_initial_state(
        self, _auto_resume_run_name: str | None = None
    ) -> LoadedTrainingState:
        """
        Loads the initial training state (checkpoint and buffer).
        Prioritizes auto-resume from the latest previous run if enabled.

        Args:
            _auto_resume_run_name: If provided, forces auto-resume logic to
                                   look for files within this specific run name.
                                   Used primarily for testing save/load within the same run.

        Returns:
            LoadedTrainingState containing potentially loaded data.
        """
        logger.info("Attempting to load initial state...")
        loaded_checkpoint_data: CheckpointData | None = None
        loaded_buffer_data: BufferData | None = None
        checkpoint_run_name: str | None = None  # Track which run checkpoint came from

        # --- Determine Checkpoint Path ---
        # Simplified: Removed hypothetical config loading paths
        # auto_resume = self.config.persistence.AUTO_RESUME # Assuming AUTO_RESUME exists
        auto_resume = True  # Defaulting to True for now, add to config later if needed

        # Find latest previous run if auto-resuming
        latest_previous_run_name: str | None = None
        if auto_resume or _auto_resume_run_name:
            target_run = _auto_resume_run_name or self.config.run_name
            latest_previous_run_name = self.path_manager.find_latest_run_dir(
                current_run_name=target_run
            )

        checkpoint_to_load: Path | None = None
        # Try auto-resume from latest previous run
        if latest_previous_run_name:
            potential_latest_path = self.path_manager.get_checkpoint_path(
                run_name=latest_previous_run_name, is_latest=True
            )
            if potential_latest_path.exists():
                checkpoint_to_load = potential_latest_path.resolve()
                checkpoint_run_name = latest_previous_run_name
                logger.info(
                    f"Auto-resuming from latest checkpoint in '{latest_previous_run_name}': {checkpoint_to_load}"
                )
            else:
                logger.info(
                    f"Latest checkpoint link not found in run '{latest_previous_run_name}'."
                )

        # --- Load Checkpoint ---
        if checkpoint_to_load:
            try:
                loaded_checkpoint_data = self.serializer.load_checkpoint(
                    checkpoint_to_load
                )
                if loaded_checkpoint_data:
                    logger.info(
                        f"Successfully loaded checkpoint from step {loaded_checkpoint_data.global_step}."
                    )
                    # Restore actor state immediately after loading checkpoint
                    self.actor_state.restore_from_state(
                        loaded_checkpoint_data.actor_state
                    )
                else:
                    # Serializer already logged error, reset run name if load failed
                    checkpoint_run_name = None
            except SerializationError:
                # Serializer already logged error, reset run name
                checkpoint_run_name = None
                logger.error(f"Failed to load checkpoint from {checkpoint_to_load}.")

        # --- Determine Buffer Path ---
        # Simplified: Removed hypothetical config loading paths
        buffer_to_load: Path | None = None

        # 1. Try buffer from the same run as the loaded checkpoint
        if checkpoint_run_name:
            potential_buffer_path = self.path_manager.get_buffer_path(
                run_name=checkpoint_run_name
            )
            if potential_buffer_path.exists():
                buffer_to_load = potential_buffer_path.resolve()
                logger.info(
                    f"Loading buffer from checkpoint run '{checkpoint_run_name}': {buffer_to_load}"
                )
            else:
                logger.info(
                    f"Buffer file not found in checkpoint run '{checkpoint_run_name}'."
                )

        # 2. Try buffer from the latest previous run (if auto-resuming and no checkpoint was loaded or buffer wasn't found there)
        elif (
            latest_previous_run_name
        ):  # Use elif to avoid checking again if checkpoint_run_name was set
            potential_buffer_path = self.path_manager.get_buffer_path(
                run_name=latest_previous_run_name
            )
            if potential_buffer_path.exists():
                buffer_to_load = potential_buffer_path.resolve()
                logger.info(
                    f"Auto-resuming buffer from latest previous run '{latest_previous_run_name}': {buffer_to_load}"
                )
            else:
                logger.info(
                    f"Buffer file not found in latest previous run '{latest_previous_run_name}'."
                )

        # --- Load Buffer ---
        if buffer_to_load:
            try:
                loaded_buffer_data = self.serializer.load_buffer(buffer_to_load)
                if loaded_buffer_data:
                    logger.info(
                        f"Successfully loaded buffer with {len(loaded_buffer_data.buffer_list)} items."
                    )
            except SerializationError:
                # Serializer already logged error
                logger.error(f"Failed to load buffer from {buffer_to_load}.")

        if not loaded_checkpoint_data and not loaded_buffer_data:
            logger.info("No previous state found or loaded.")

        return LoadedTrainingState(
            checkpoint_data=loaded_checkpoint_data, buffer_data=loaded_buffer_data
        )

    def save_training_state(
        self,
        nn_state_dict: dict[str, Any],
        optimizer_state_dict: dict[str, Any],
        buffer_content: list[Any],
        global_step: int,
        episodes_played: int,
        total_simulations_run: int,
        actor_state_data: dict[str, Any],
        is_best: bool = False,
        save_buffer: bool = False,
        model_config_dict: dict | None = None,
        env_config_dict: dict | None = None,
        user_data: dict | None = None,
    ):
        """Saves the training state (checkpoint and optionally buffer)."""
        logger.debug(f"Preparing to save state at step {global_step}...")
        try:
            # Prepare optimizer state (e.g., move to CPU)
            prepared_opt_state = self.serializer.prepare_optimizer_state(
                optimizer_state_dict
            )

            # Create CheckpointData object
            checkpoint_data = CheckpointData(
                run_name=self.config.run_name,
                global_step=global_step,
                episodes_played=episodes_played,
                total_simulations_run=total_simulations_run,
                model_state_dict=nn_state_dict,
                optimizer_state_dict=prepared_opt_state,
                actor_state=actor_state_data,
                user_data=user_data or {},
                model_config_dict=model_config_dict or {},
                env_config_dict=env_config_dict or {},
            )

            # Save checkpoint file
            cp_path = self.path_manager.get_checkpoint_path(step=global_step)
            self.serializer.save_checkpoint(checkpoint_data, cp_path)

            # Update latest/best links
            self.path_manager.update_checkpoint_links(cp_path, is_best=is_best)

            # Log checkpoint artifact to MLflow
            self._log_artifact_safe(cp_path, "checkpoints")
            # Log link artifacts
            latest_cp_path = self.path_manager.get_checkpoint_path(is_latest=True)
            self._log_artifact_safe(latest_cp_path, "checkpoints")
            if is_best:
                best_cp_path = self.path_manager.get_checkpoint_path(is_best=True)
                self._log_artifact_safe(best_cp_path, "checkpoints")

            # Save buffer if requested
            if save_buffer and self.config.persistence.SAVE_BUFFER:
                logger.debug(
                    f"Preparing buffer data (size: {len(buffer_content)}) for saving..."
                )
                buffer_data = self.serializer.prepare_buffer_data(buffer_content)
                if buffer_data:
                    buf_path = self.path_manager.get_buffer_path(step=global_step)
                    self.serializer.save_buffer(buffer_data, buf_path)
                    # Update buffer link
                    self.path_manager.update_buffer_link(buf_path)
                    # Log buffer artifact to MLflow
                    self._log_artifact_safe(buf_path, "buffers")
                    latest_buf_path = self.path_manager.get_buffer_path()
                    self._log_artifact_safe(latest_buf_path, "buffers")
                else:
                    logger.warning(
                        f"Buffer saving skipped at step {global_step} due to preparation error."
                    )

            logger.info(f"Training state saved successfully at step {global_step}.")

        except SerializationError as e:
            logger.error(f"Serialization failed during save_training_state: {e}")
        except Exception as e:
            logger.error(
                f"Unexpected error during save_training_state: {e}", exc_info=True
            )

    def save_initial_config(self):
        """Saves the initial TrieyeConfig to JSON and logs it."""
        try:
            # Use get_config_path() method
            config_path = self.path_manager.get_config_path()
            self.serializer.save_config_json(self.config.model_dump(), config_path)
            self._log_artifact_safe(config_path, "config")
        except SerializationError as e:
            logger.error(f"Failed to save initial config: {e}")
        except Exception as e:
            logger.error(f"Unexpected error saving initial config: {e}", exc_info=True)

    def save_run_config(self, configs: dict[str, Any]):
        """Saves a combined configuration dictionary as a JSON artifact."""
        try:
            # Use get_config_path() method
            config_path = self.path_manager.get_config_path()
            self.serializer.save_config_json(configs, config_path)
            self._log_artifact_safe(config_path, "config")
        except SerializationError as e:
            logger.error(f"Failed to save run config: {e}")
        except Exception as e:
            logger.error(f"Unexpected error saving run config: {e}", exc_info=True)

    def _log_artifact_safe(self, local_path: Path, artifact_path: str | None = None):
        """Logs an artifact to MLflow, handling potential errors."""
        if self.mlflow_client and self.mlflow_run_id:
            if not local_path.exists():
                logger.warning(f"Attempted to log non-existent artifact: {local_path}")
                return
            try:
                self.mlflow_client.log_artifact(
                    self.mlflow_run_id, str(local_path), artifact_path=artifact_path
                )
                logger.debug(
                    f"Logged artifact '{local_path.name}' to MLflow path '{artifact_path or '.'}'."
                )
            except Exception as e:
                logger.error(
                    f"Failed to log artifact {local_path} to MLflow: {e}",
                    exc_info=True,
                )
