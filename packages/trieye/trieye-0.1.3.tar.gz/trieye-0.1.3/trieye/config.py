# File: trieye/config.py
import logging
import time
from pathlib import Path
from typing import Literal

from pydantic import (
    BaseModel,
    Field,
    ValidationInfo,  # Import ValidationInfo
    computed_field,
    field_validator,
    model_validator,
)

logger = logging.getLogger(__name__)

# --- Persistence Config ---


class PersistenceConfig(BaseModel):
    """Configuration for saving/loading artifacts (Pydantic model)."""

    ROOT_DATA_DIR: str = Field(default=".trieye_data")
    RUNS_DIR_NAME: str = Field(default="runs")
    MLFLOW_DIR_NAME: str = Field(default="mlruns")

    CHECKPOINT_SAVE_DIR_NAME: str = Field(default="checkpoints")
    BUFFER_SAVE_DIR_NAME: str = Field(default="buffers")
    LOG_DIR_NAME: str = Field(default="logs")
    TENSORBOARD_DIR_NAME: str = Field(default="tensorboard")
    PROFILE_DIR_NAME: str = Field(default="profile_data")

    LATEST_CHECKPOINT_FILENAME: str = Field(default="latest.pkl")
    BEST_CHECKPOINT_FILENAME: str = Field(default="best.pkl")
    BUFFER_FILENAME: str = Field(default="buffer.pkl")
    CONFIG_FILENAME: str = Field(default="configs.json")

    # Moved from TrainConfig
    SAVE_BUFFER: bool = Field(default=True)
    BUFFER_SAVE_FREQ_STEPS: int = Field(default=1000, ge=1)

    # Internal fields, not set by user directly
    RUN_NAME: str = Field(default="default_run", exclude=True)
    APP_NAME: str = Field(default="default_app", exclude=True)

    def _get_absolute_root(self) -> Path:
        """Resolves ROOT_DATA_DIR to an absolute path relative to the project root."""
        project_root = Path.cwd()
        root_path = project_root / self.ROOT_DATA_DIR
        return root_path.resolve()

    @computed_field  # type: ignore[misc]
    @property
    def MLFLOW_TRACKING_URI(self) -> str:
        """Constructs the absolute file URI for MLflow tracking."""
        abs_path = self.get_mlflow_abs_path()
        abs_path.mkdir(parents=True, exist_ok=True)
        return abs_path.as_uri()

    def get_app_root_dir(self) -> Path:
        """Gets the absolute path to the directory for the specific application."""
        root_path = self._get_absolute_root()
        return root_path / self.APP_NAME

    def get_runs_root_dir(self) -> Path:
        """Gets the absolute path to the directory containing all runs for the app."""
        app_root = self.get_app_root_dir()
        return app_root / self.RUNS_DIR_NAME

    def get_run_base_dir(self, run_name: str | None = None) -> Path:
        """Gets the absolute base directory path for a specific run."""
        runs_root = self.get_runs_root_dir()
        name = run_name if run_name else self.RUN_NAME
        return runs_root / name

    def get_mlflow_abs_path(self) -> Path:
        """Gets the absolute OS path to the MLflow directory for the app."""
        app_root = self.get_app_root_dir()
        return app_root / self.MLFLOW_DIR_NAME

    def get_tensorboard_log_dir(self, run_name: str | None = None) -> Path:
        """Gets the absolute directory path for TensorBoard logs for a specific run."""
        run_base = self.get_run_base_dir(run_name)
        return run_base / self.TENSORBOARD_DIR_NAME

    def get_profile_data_dir(self, run_name: str | None = None) -> Path:
        """Gets the absolute directory path for profile data for a specific run."""
        run_base = self.get_run_base_dir(run_name)
        return run_base / self.PROFILE_DIR_NAME

    def get_log_dir(self, run_name: str | None = None) -> Path:
        """Gets the absolute directory path for log files for a specific run."""
        run_base = self.get_run_base_dir(run_name)
        return run_base / self.LOG_DIR_NAME


# --- Stats Config ---

AggregationMethod = Literal[
    "latest", "mean", "sum", "rate", "min", "max", "std", "count"
]
LogTarget = Literal["mlflow", "tensorboard", "console"]
DataSource = Literal["trainer", "worker", "loop", "buffer", "system", "custom"]
XAxis = Literal["global_step", "wall_time", "episode"]


class MetricConfig(BaseModel):
    """Configuration for a single metric to be tracked and logged."""

    name: str = Field(
        ..., description="Unique name for the metric (e.g., 'Loss/Total')"
    )
    source: DataSource = Field(
        ...,
        description="Origin of the raw metric data (e.g., 'trainer', 'worker', 'custom')",
    )
    raw_event_name: str | None = Field(
        default=None,
        description="Specific raw event name if different from metric name (e.g., 'episode_end'). If None, uses 'name'.",
    )
    aggregation: AggregationMethod = Field(
        default="latest",
        description="How to aggregate raw values over the logging interval ('rate' calculates per second)",
    )
    log_frequency_steps: int = Field(
        default=1,
        description="Log metric every N global steps. Set to 0 to disable step-based logging.",
        ge=0,
    )
    log_frequency_seconds: float = Field(
        default=0.0,
        description="Log metric every N seconds. Set to 0 to disable time-based logging.",
        ge=0.0,
    )
    log_to: list[LogTarget] = Field(
        default=["mlflow", "tensorboard"],
        description="Where to log the processed metric.",
    )
    x_axis: XAxis = Field(
        default="global_step", description="The primary x-axis for logging."
    )
    rate_numerator_event: str | None = Field(
        default=None,
        description="Raw event name for the numerator in rate calculation (e.g., 'step_completed')",
    )
    context_key: str | None = Field(
        default=None,
        description="Key within the RawMetricEvent context dictionary to extract the value from.",
    )

    @field_validator("rate_numerator_event")
    @classmethod
    def check_rate_config(
        cls,
        v: str | None,
        info: ValidationInfo,  # Use ValidationInfo
    ):
        """Ensure numerator is specified if aggregation is 'rate'."""
        # Access field values via info.data
        if info.data.get("aggregation") == "rate" and v is None:
            metric_name = info.data.get("name", "Unknown Metric")
            raise ValueError(
                f"Metric '{metric_name}' has aggregation 'rate' but 'rate_numerator_event' is not set."
            )
        return v

    # Corrected signature for Pydantic v2 model_validator(mode='after')
    @model_validator(mode="after")
    def validate_rate_numerator_event(self) -> "MetricConfig":
        """Catch any remaining cases where rate_numerator_event is missing."""
        if self.aggregation == "rate" and self.rate_numerator_event is None:
            raise ValueError(
                f"Metric '{self.name}' has aggregation 'rate' but 'rate_numerator_event' is not set."
            )
        return self

    @property
    def event_key(self) -> str:
        """The key used to store/retrieve raw events for this metric."""
        return self.raw_event_name or self.name


class StatsConfig(BaseModel):
    """Overall configuration for statistics collection and logging."""

    processing_interval_seconds: float = Field(
        default=1.0,
        description="How often the TrieyeActor aggregates and logs metrics.",
        gt=0,
    )
    metrics: list[MetricConfig] = Field(
        default_factory=list, description="List of metrics to track and log."
    )

    @field_validator("metrics")
    @classmethod
    def check_metric_names_unique(cls, metrics: list[MetricConfig]):
        """Ensure all configured metric names are unique."""
        names = [m.name for m in metrics]
        if len(names) != len(set(names)):
            from collections import Counter

            duplicates = [name for name, count in Counter(names).items() if count > 1]
            raise ValueError(f"Duplicate metric names found in config: {duplicates}")
        return metrics


# --- Trieye Config ---


class TrieyeConfig(BaseModel):
    """Top-level configuration for the Trieye library/actor."""

    app_name: str = Field(
        default="default_app",
        description="Namespace for data storage (.trieye_data/<app_name>).",
    )
    run_name: str = Field(
        default_factory=lambda: f"run_{time.strftime('%Y%m%d_%H%M%S')}",
        description="Specific identifier for the current run.",
    )
    persistence: PersistenceConfig = Field(
        default_factory=PersistenceConfig,
        description="Configuration for data persistence.",
    )
    stats: StatsConfig = Field(
        default_factory=StatsConfig,
        description="Configuration for statistics collection and logging.",
    )

    @model_validator(mode="after")
    def sync_names_to_persistence(self) -> "TrieyeConfig":
        if hasattr(self, "persistence"):  # Check attribute exists before access
            self.persistence.RUN_NAME = self.run_name
            self.persistence.APP_NAME = self.app_name
        return self


# Rebuild models
PersistenceConfig.model_rebuild(force=True)
MetricConfig.model_rebuild(force=True)
StatsConfig.model_rebuild(force=True)
TrieyeConfig.model_rebuild(force=True)


# Default metrics list (can be imported and used by applications)
DEFAULT_METRICS = [
    MetricConfig(
        name="Loss/Total", source="custom", aggregation="mean", log_frequency_steps=10
    ),
    MetricConfig(
        name="Loss/Policy", source="custom", aggregation="mean", log_frequency_steps=10
    ),
    MetricConfig(
        name="Loss/Value", source="custom", aggregation="mean", log_frequency_steps=10
    ),
    MetricConfig(
        name="Loss/Entropy", source="custom", aggregation="mean", log_frequency_steps=10
    ),
    MetricConfig(
        name="Loss/Mean_Abs_TD_Error",
        source="custom",
        aggregation="mean",
        log_frequency_steps=10,
    ),
    MetricConfig(
        name="LearningRate",
        source="custom",
        aggregation="latest",
        log_frequency_steps=10,
    ),
    MetricConfig(
        name="Episode/Final_Score",
        source="custom",
        raw_event_name="episode_end",
        context_key="score",
        aggregation="mean",
        log_frequency_seconds=5.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="Episode/Length",
        source="custom",
        raw_event_name="episode_end",
        context_key="length",
        aggregation="mean",
        log_frequency_seconds=5.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="Episode/Triangles_Cleared_Total",
        source="custom",
        raw_event_name="episode_end",
        context_key="triangles_cleared",
        aggregation="mean",
        log_frequency_seconds=5.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="MCTS/Avg_Simulations_Per_Step",
        source="custom",
        raw_event_name="mcts_step",
        aggregation="mean",
        log_frequency_seconds=10.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="RL/Step_Reward_Mean",
        source="custom",
        raw_event_name="step_reward",
        aggregation="mean",
        log_frequency_seconds=10.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="Buffer/Size",
        source="custom",
        aggregation="latest",
        log_frequency_seconds=5.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="Progress/Total_Simulations",
        source="custom",
        aggregation="latest",
        log_frequency_seconds=5.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="Progress/Episodes_Played",
        source="custom",
        aggregation="latest",
        log_frequency_seconds=5.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="Progress/Weight_Updates_Total",
        source="custom",
        aggregation="latest",
        log_frequency_seconds=5.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="System/Num_Active_Workers",
        source="custom",
        aggregation="latest",
        log_frequency_seconds=10.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="System/Num_Pending_Tasks",
        source="custom",
        aggregation="latest",
        log_frequency_seconds=10.0,
        log_frequency_steps=0,
    ),
    MetricConfig(
        name="Rate/Steps_Per_Sec",
        source="custom",
        aggregation="rate",
        rate_numerator_event="step_completed",
        log_frequency_seconds=5.0,
        log_frequency_steps=0,
        log_to=["mlflow", "tensorboard", "console"],
    ),
    MetricConfig(
        name="Rate/Episodes_Per_Sec",
        source="custom",
        aggregation="rate",
        rate_numerator_event="episode_end",
        log_frequency_seconds=5.0,
        log_frequency_steps=0,
        log_to=["mlflow", "tensorboard", "console"],
    ),
    MetricConfig(
        name="Rate/Simulations_Per_Sec",
        source="custom",
        aggregation="rate",
        rate_numerator_event="mcts_step",  # Assuming mcts_step value is #sims
        log_frequency_seconds=5.0,
        log_frequency_steps=0,
        log_to=["mlflow", "tensorboard", "console"],
    ),
    MetricConfig(
        name="PER/Beta", source="custom", aggregation="latest", log_frequency_steps=10
    ),
]
