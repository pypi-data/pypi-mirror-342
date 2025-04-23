
[![CI Status](https://github.com/lguibr/trieye/actions/workflows/ci_cd.yml/badge.svg)](https://github.com/lguibr/trieye/actions/workflows/ci_cd.yml)
[![PyPI version](https://badge.fury.io/py/trieye.svg)](https://badge.fury.io/py/trieye)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![codecov](https://codecov.io/gh/lguibr/trieye/graph/badge.svg?token=YOUR_CODECOV_TOKEN)](https://codecov.io/gh/lguibr/trieye) <!-- Replace with actual token/badge -->


# Trieye Library
<img src="bitmap.png" alt="logo" width="300"/>

## Overview

Trieye is a Python library designed to provide **asynchronous statistics collection, processing, logging, and data persistence** for machine learning experiments, particularly those using [Ray](https://www.ray.io/) for distributed computation. It aims to decouple these common operational concerns from the main application logic, offering a configurable and reusable solution via a dedicated Ray actor.

**Key Features:**

*   **Ray Actor Integration:** Core functionality is exposed via a `TrieyeActor` Ray actor for asynchronous operation, minimizing impact on the main training loop. Configurable fault tolerance (`max_restarts`).
*   **Configurable Statistics:** Define metrics, aggregation methods (mean, sum, rate, latest, etc.), logging frequency (by step or time), and logging targets (MLflow, TensorBoard, console) via Pydantic models (`TrieyeConfig`, `StatsConfig`, `MetricConfig`).
*   **Flexible Event System:** Applications send raw metric data points (`RawMetricEvent`) to the actor, tagged with a global step and optional context dictionary. Events with non-finite values are automatically skipped.
*   **Asynchronous Processing:** The actor buffers raw events (`ActorState`) and processes/aggregates them periodically (`ActorLogic`, `StatsProcessor`) based on configuration, preventing blocking in the main application.
*   **MLflow & TensorBoard Integration:** Automatically initializes and manages MLflow runs and TensorBoard writers within the actor, logging processed metrics and specified artifacts (checkpoints, buffers, configs).
*   **Data Persistence:** Handles saving and loading of application state (e.g., model checkpoints, replay buffers) using `cloudpickle` and Pydantic schemas (`ActorLogic`, `Serializer`). Manages file paths within a structured directory (`PathManager`) and logs artifacts to MLflow. Includes logic for auto-resuming from the latest checkpoint of the most recent previous run.
*   **Structured Configuration:** Uses Pydantic for clear, validated configuration (`TrieyeConfig`, `PersistenceConfig`, `StatsConfig`).
*   **Testability:** Designed with dependency injection in mind, allowing components like MLflow/TensorBoard clients to be mocked during testing.

## Installation

```bash
pip install trieye
```

Or, for development:

```bash
git clone https://github.com/lguibr/trieye.git
cd trieye
pip install -e .[dev]
```

**Dependencies:** Requires Python 3.10+ and relies on `ray[default]`, `mlflow`, `tensorboard`, `pydantic`, `cloudpickle`, `numpy`, and `torch`.

## Architecture

The library separates concerns into distinct components, orchestrated by the `TrieyeActor`:

```mermaid
graph LR
    subgraph Application
        AppLogic[Application Logic (e.g., Training Loop, Workers)]
    end

    subgraph TrieyeActor [Ray Actor: TrieyeActor]
        direction LR
        TA(TrieyeActor Façade) -- Manages --> AS[ActorState: Buffers, Timestamps]
        TA -- Delegates --> AL[ActorLogic: Orchestration]
        AL -- Uses --> PM[PathManager: File Paths]
        AL -- Uses --> SER[Serializer: Save/Load]
        AL -- Uses --> SP[StatsProcessor: Aggregation/Logging]
        SP -- Interacts --> MC[MLflow Client]
        SP -- Interacts --> TBW[TensorBoard Writer]
    end

    subgraph ExternalServices
        MLFLOW[MLflow Tracking Server/Files]
        TB[TensorBoard Event Files]
        FS[Filesystem: .trieye_data/]
    end

    AppLogic -- log_event() --> TA
    AppLogic -- save_training_state() --> TA
    AppLogic -- load_initial_state() --> TA

    TA -- Reads/Writes --> AS
    TA -- Calls --> AL

    AL -- Calls --> PM
    AL -- Calls --> SER
    AL -- Calls --> SP

    SP -- Logs --> MC
    SP -- Logs --> TBW

    SER -- Writes/Reads --> FS
    PM -- Manages --> FS
    MC -- Writes --> MLFLOW
    TBW -- Writes --> TB

    style TrieyeActor fill:#f9f,stroke:#333,stroke-width:2px
    style ExternalServices fill:#ccf,stroke:#333,stroke-width:1px
```

*   **`TrieyeActor` ([`trieye/actor.py`](trieye/actor.py)):** The central Ray actor (`@ray.remote`). Acts as a façade, receiving external calls (`log_event`, `save_training_state`, `load_initial_state`, `shutdown`). Manages thread safety (`threading.Lock`) and delegates core tasks to `ActorLogic`. Initializes and owns tracking clients (MLflow, TensorBoard) unless injected for testing. Handles actor lifecycle and shutdown.
*   **`ActorState` ([`trieye/actor_state.py`](trieye/actor_state.py)):** Manages the internal, mutable state within the actor: raw event buffers, latest metric values, event timestamps for rate calculation, and tracking of the last processed step/time. Provides methods for adding events, retrieving data for processing, clearing processed data, and getting/setting persistable state (e.g., `last_processed_step`).
*   **`ActorLogic` ([`trieye/actor_logic.py`](trieye/actor_logic.py)):** Encapsulates the core business logic, independent of Ray actor specifics. Orchestrates interactions between `ActorState`, `PathManager`, `Serializer`, and `StatsProcessor`. Contains the logic for processing stats, saving/loading checkpoints and buffers, handling auto-resume, and saving configuration files.
*   **`TrieyeConfig` ([`trieye/config.py`](trieye/config.py)):** Top-level Pydantic configuration model, containing `PersistenceConfig` and `StatsConfig`. Defines application/run names.
*   **`PersistenceConfig` ([`trieye/config.py`](trieye/config.py)):** Defines directories, filenames, save frequencies, and MLflow tracking URI.
*   **`StatsConfig` ([`trieye/config.py`](trieye/config.py)):** Defines metric processing rules (aggregation, frequency, targets) via a list of `MetricConfig`.
*   **`MetricConfig` ([`trieye/config.py`](trieye/config.py)):** Defines a single metric to be tracked (name, source event, aggregation, logging frequency/targets, etc.). Includes validation for rate metrics.
*   **`RawMetricEvent`, `CheckpointData`, `BufferData`, `LoadedTrainingState`, `LogContext` ([`trieye/schemas.py`](trieye/schemas.py)):** Pydantic models for structuring data (events, saved state, logging context). `BufferData` stores `list[Any]`, allowing applications to store arbitrary buffer content. `CheckpointData` includes actor state for seamless resumption.
*   **`PathManager` ([`trieye/path_manager.py`](trieye/path_manager.py)):** Manages the directory structure within `.trieye_data/<app_name>/runs/<run_name>/`. Provides methods for getting paths to checkpoints, buffers, logs, etc., and finding the latest previous run for auto-resuming.
*   **`Serializer` ([`trieye/serializer.py`](trieye/serializer.py)):** Handles serialization/deserialization using `cloudpickle` (for checkpoints/buffers) and JSON (for configs). Includes logic to prepare optimizer state (move to CPU) before saving.
*   **`StatsProcessor` ([`trieye/stats_processor.py`](trieye/stats_processor.py)):** Performs aggregation (mean, sum, rate, etc.) and logging logic based on `StatsConfig`. Interacts with MLflow Client and TensorBoard Writer. Used by `ActorLogic`.
*   **`exceptions.py` ([`trieye/exceptions.py`](trieye/exceptions.py)):** Custom exception classes (`ConfigurationError`, `SerializationError`, `ProcessingError`).

## Usage Example

```python
import logging
import random
import time

import ray

# Import necessary components from trieye
from trieye import (
    DEFAULT_METRICS,  # Example using default metrics
    BufferData,
    CheckpointData,
    MetricConfig,
    PersistenceConfig,  # Import PersistenceConfig if customizing
    RawMetricEvent,
    StatsConfig,
    TrieyeActor,
    TrieyeConfig,
)

# Configure logging for the application
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Configure Trieye
# Example: Customize persistence and add one custom metric to defaults
my_metrics = DEFAULT_METRICS + [
    MetricConfig(name="Custom/MyValue", source="custom", aggregation="mean", log_frequency_steps=20)
]

trieye_config = TrieyeConfig(
    app_name="my_rl_app",
    run_name=f"experiment_{time.strftime('%Y%m%d_%H%M%S')}",
    persistence=PersistenceConfig( # Optional: Customize persistence
        BUFFER_SAVE_FREQ_STEPS=50, # Save buffer more frequently
        ROOT_DATA_DIR=".my_app_data" # Example: change root dir
    ),
    stats=StatsConfig( # Optional: Customize stats
        processing_interval_seconds=2.0, # Process stats every 2 seconds
        metrics=my_metrics # Use the combined list
    )
)

# 2. Initialize Ray (if not already done)
if not ray.is_initialized():
    # Set lower Ray logging level to reduce noise if desired
    ray.init(logging_level=logging.WARNING)

# 3. Start the TrieyeActor
# Give the actor a unique name if you might need to get its handle later
actor_name = "trieye_logger_main"
try:
    # Use get_actor for resilience if script restarts and actor still exists
    trieye_actor = ray.get_actor(actor_name)
    logger.info(f"Reconnected to existing TrieyeActor '{actor_name}'.")
except ValueError:
    logger.info(f"Creating new TrieyeActor '{actor_name}'.")
    trieye_actor = TrieyeActor.options(name=actor_name, lifetime="detached").remote(config=trieye_config)

# Optional: Wait for actor to be ready by calling a method
try:
    run_id = ray.get(trieye_actor.get_mlflow_run_id.remote(), timeout=10)
    logger.info(f"TrieyeActor ready. MLflow Run ID: {run_id}")
except Exception as e:
    logger.error(f"Error waiting for TrieyeActor: {e}. Exiting.")
    ray.shutdown()
    exit(1)

# --- In your training loop ---
global_step = 0
buffer_size = 0
episodes_played = 0
my_buffer: list = []
my_model_state: dict = {}
my_optimizer_state: dict = {}

# Load initial state (example)
# Use the logic handler within the actor for loading
logger.info("Attempting to load initial state...")
initial_state = ray.get(trieye_actor.load_initial_state.remote())

if initial_state.checkpoint_data:
    cp_data = initial_state.checkpoint_data
    global_step = cp_data.global_step
    episodes_played = cp_data.episodes_played
    my_model_state = cp_data.model_state_dict
    my_optimizer_state = cp_data.optimizer_state_dict
    # Actor state is restored internally by load_initial_state
    logger.info(f"Resuming from Checkpoint: Step={global_step}, Episodes={episodes_played}")
    # ... apply model/optimizer state to your actual model/optimizer ...

if initial_state.buffer_data:
    my_buffer = initial_state.buffer_data.buffer_list
    buffer_size = len(my_buffer)
    logger.info(f"Loaded Buffer: {buffer_size} items")
    # ... potentially validate/process loaded buffer content ...


logger.info("Starting training loop...")
try:
    for i in range(global_step, global_step + 100): # Example loop continuing from loaded step
        time.sleep(0.1)
        current_step = i + 1 # Typically step increments after processing

        # Simulate adding to buffer
        my_buffer.append(f"experience_{current_step}")
        buffer_size = len(my_buffer)

        # Simulate training step
        loss = random.random() * 0.1
        my_model_state = {"param": current_step} # Update mock state
        my_optimizer_state = {"opt_param": current_step}

        # --- Log Metrics ---
        # Use default metric names if defined in config
        trieye_actor.log_event.remote(
            RawMetricEvent(name="Loss/Total", value=loss, global_step=current_step)
        )
        # Log event for rate calculation (must match rate_numerator_event in config)
        trieye_actor.log_event.remote(
            RawMetricEvent(name="step_completed", value=1, global_step=current_step)
        )
        # Log custom metric
        trieye_actor.log_event.remote(
            RawMetricEvent(name="Custom/MyValue", value=current_step * 2, global_step=current_step)
        )
        # Log buffer size
        trieye_actor.log_event.remote(
             RawMetricEvent(name="Buffer/Size", value=buffer_size, global_step=current_step)
        )

        # Simulate episode end occasionally
        if current_step % 10 == 0:
            episodes_played += 1
            score = random.random() * 100
            length = random.randint(50, 150)
            # Log event with context (must match raw_event_name and context_key in config)
            trieye_actor.log_event.remote(
                RawMetricEvent(
                    name="episode_end",
                    value=1, # Value often unused when context is primary data
                    global_step=current_step,
                    context={"score": score, "length": length}
                )
            )
            # Log progress
            trieye_actor.log_event.remote(
                 RawMetricEvent(name="Progress/Episodes_Played", value=episodes_played, global_step=current_step)
            )

        # --- Trigger Stats Processing ---
        # Actor handles interval check internally. Fire-and-forget.
        trieye_actor.process_and_log.remote(current_step)

        # --- Save State Periodically ---
        # Check if buffer should be saved based on frequency in config
        should_save_buffer = (current_step % trieye_config.persistence.BUFFER_SAVE_FREQ_STEPS == 0)
        # Example: Save checkpoint every 20 steps
        if current_step % 20 == 0:
            logger.info(f"Requesting save at step {current_step}, save buffer: {should_save_buffer}")
            # Pass actual state dicts and buffer content
            mock_model_config = {"layers": 2} # Example config
            mock_env_config = {"id": "env-v1"} # Example config

            trieye_actor.save_training_state.remote(
                nn_state_dict=my_model_state,
                optimizer_state_dict=my_optimizer_state,
                buffer_content=my_buffer, # Pass the actual buffer list
                global_step=current_step,
                episodes_played=episodes_played,
                total_simulations_run=current_step * 100, # Example simulation count
                save_buffer=should_save_buffer,
                model_config_dict=mock_model_config,
                env_config_dict=mock_env_config,
                user_data={"custom_info": "value"}, # Optional extra data
                is_best=False # Example: only save 'best' based on some evaluation condition
            )

        # Update global step for next iteration
        global_step = current_step

except KeyboardInterrupt:
    logger.info("Training interrupted by user.")
finally:
    # --- Cleanup ---
    logger.info("Training finished or interrupted. Shutting down TrieyeActor...")
    if trieye_actor:
        try:
            # Force final stats processing with the last known step
            logger.info(f"Forcing final log processing at step {global_step}...")
            ray.get(trieye_actor.force_process_and_log.remote(global_step), timeout=15)
            # Explicitly call shutdown to close files, TB writer, and potentially MLflow run
            logger.info("Calling actor shutdown...")
            ray.get(trieye_actor.shutdown.remote(), timeout=15)
            logger.info("TrieyeActor shutdown complete.")
        except Exception as e:
            logger.error(f"Error during TrieyeActor final processing or shutdown: {e}")
            # Optional: Force kill the actor if shutdown hangs or fails
            logger.warning("Attempting to kill actor after shutdown error.")
            try:
                ray.kill(trieye_actor)
            except Exception as kill_e:
                logger.error(f"Error killing TrieyeActor: {kill_e}")

    if ray.is_initialized():
        ray.shutdown()
    logger.info("Ray shut down. Done.")

```

## Configuration Details

*   **`TrieyeConfig`**: Top-level config.
    *   `app_name`: Namespace for data storage (`<ROOT_DATA_DIR>/<app_name>`).
    *   `run_name`: Specific identifier for the current run (defaults to timestamp).
    *   `persistence`: `PersistenceConfig` instance.
    *   `stats`: `StatsConfig` instance.
*   **`PersistenceConfig`**: Defines directories (`ROOT_DATA_DIR`, `RUNS_DIR_NAME`, etc.), filenames (`LATEST_CHECKPOINT_FILENAME`, etc.), buffer save frequency (`BUFFER_SAVE_FREQ_STEPS`), and MLflow URI (`MLFLOW_TRACKING_URI` computed property). See [`trieye/config.py`](trieye/config.py) for all options.
*   **`StatsConfig`**:
    *   `processing_interval_seconds`: How often the actor processes buffered stats (e.g., `1.0` for every second).
    *   `metrics`: A list of `MetricConfig` objects defining each metric to track.
*   **`MetricConfig`**:
    *   `name`: Final name used for logging (e.g., "Episode/Score"). Must be unique within `StatsConfig`.
    *   `source`: Origin identifier (e.g., "worker", "trainer", "custom"). Used for organization/filtering (currently informational).
    *   `raw_event_name`: The `name` field used in `RawMetricEvent` if different from the final `name`. If `None`, uses `name`. **Important:** This is the key the actor looks for in incoming events.
    *   `aggregation`: How to combine multiple raw values within a processing interval (`mean`, `sum`, `latest`, `rate`, `min`, `max`, `std`, `count`).
    *   `log_frequency_steps`/`log_frequency_seconds`: Control how often the *aggregated* metric is logged. Set to 0 to disable that frequency type. If both are > 0, logging occurs if *either* condition is met. If both are 0, the metric is aggregated but never logged automatically (useful for internal state).
    *   `log_to`: List of targets (`mlflow`, `tensorboard`, `console`).
    *   `x_axis`: Primary x-axis for logging (`global_step`, `wall_time`, `episode`). Note: `wall_time` and `episode` support might be limited depending on logging backend capabilities and how steps are provided. `global_step` is the most common and reliable.
    *   `context_key`: If the value comes from the `context` dictionary within `RawMetricEvent`, specify the key here (e.g., for `episode_end` events with `context={"score": 123}`). The `value` field of the `RawMetricEvent` is ignored in this case.
    *   `rate_numerator_event`: **Required if `aggregation="rate"`**. Specifies the `raw_event_name` whose **summed values** act as the numerator for the rate calculation (events per second). For example, if `rate_numerator_event="step_completed"` and the event value is always 1, this calculates steps/sec. If the event value represents simulations run in that step, it calculates simulations/sec.

## Testing Strategy

Testing `Trieye` involves several layers, following best practices for Ray applications:

1.  **Unit Tests (Components):** Individual components like `PathManager`, `Serializer`, `ActorState`, and `StatsProcessor` are tested in isolation using standard `pytest` fixtures and mocks (`unittest.mock`). These tests verify the core logic without involving Ray. See `tests/test_path_manager.py`, `tests/test_serializer.py`, `tests/test_actor_state.py`, `tests/test_stats_processor.py`.
2.  **Unit Tests (Actor Logic - Local Mode):** The `TrieyeActor`'s methods are tested using Ray's **local mode** (`ray.init(local_mode=True)`). This executes the actor's code synchronously in the main process, allowing direct interaction and state inspection, bypassing Ray's pickling and scheduling. Dependencies like MLflow/TensorBoard clients are injected as mocks. This approach provides high code coverage for the actor's internal logic. See `tests/test_actor.py` (tests using `trieye_actor_local` fixture).
3.  **Integration Tests (Remote Actor):** A few tests run the `TrieyeActor` as a **remote actor** (`@ray.remote`) on a minimal, multi-process Ray cluster initialized by `pytest`. These tests verify the actor's behavior in a distributed setting, including method calls via `actor.method.remote()`, state persistence across calls, and interaction with injected mocks for external services. These tests ensure the actor functions correctly within the Ray ecosystem. See `tests/test_actor.py` (tests marked with `@pytest.mark.integration` using `trieye_actor_integration` fixture).
4.  **Mocking:** External dependencies (MLflow, TensorBoard, file I/O via `PathManager`) are mocked using `unittest.mock.MagicMock` and injected into the relevant components (`TrieyeActor`, `ActorLogic`, `StatsProcessor`) during testing. This isolates tests from external services and filesystem side effects. Module-level functions (like `mlflow.start_run`) are patched using `unittest.mock.patch` where necessary.
5.  **Fixtures:** `pytest` fixtures (`tests/conftest.py`) provide reusable setup for configurations (`TrieyeConfig`), temporary directories (`tmp_path`), mock objects (`mock_mlflow_client`, `mock_tb_writer`), Ray initialization (session-scoped cluster, function-scoped local mode), and test data (`RawMetricEvent`, `CheckpointData`).
6.  **Coverage:** Code coverage is measured using `pytest-cov`, aiming for high coverage (>80%) of the core logic. Ray local mode helps include actor code in coverage reports.

This multi-layered approach ensures both the internal logic and the distributed behavior of the `TrieyeActor` are thoroughly validated.

## Contributing

Contributions are welcome! Please open an issue to discuss changes or submit a pull request. Ensure tests pass (`pytest tests`) and code meets formatting/linting standards (`ruff check . --fix && ruff format .`). Update type hints (`mypy .`) as needed.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.