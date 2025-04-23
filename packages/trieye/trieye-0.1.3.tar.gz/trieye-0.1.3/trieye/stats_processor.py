# File: trieye/stats_processor.py
import logging
from collections import defaultdict
from typing import TYPE_CHECKING

import numpy as np
from mlflow.tracking import MlflowClient
from torch.utils.tensorboard import SummaryWriter

from .config import MetricConfig

# Use relative imports within trieye
from .exceptions import ProcessingError
from .schemas import LogContext, RawMetricEvent

if TYPE_CHECKING:
    from .config import StatsConfig

logger = logging.getLogger(__name__)


class StatsProcessor:
    """
    Processes raw metric data collected by the TrieyeActor and logs
    aggregated results according to the StatsConfig.
    """

    def __init__(
        self,
        config: "StatsConfig",
        run_name: str,
        tb_writer: SummaryWriter | None,
        mlflow_run_id: str | None,
        _mlflow_client: MlflowClient | None = None,  # Add injectable client
    ):
        self.config = config
        self.run_name = run_name
        self.mlflow_run_id = mlflow_run_id
        self._metric_configs: dict[str, MetricConfig] = {
            mc.name: mc for mc in config.metrics
        }
        # This will be updated by the actor instance or logic handler
        self._last_log_time: dict[str, float] = {}
        self.tb_writer = tb_writer
        self.mlflow_client: MlflowClient | None = _mlflow_client  # Use injected client

        # Initialize client only if not injected and run_id is valid
        if self.mlflow_client is None and self.mlflow_run_id:
            try:
                self.mlflow_client = MlflowClient()
                logger.info("StatsProcessor: MlflowClient initialized internally.")
            except Exception as e:
                logger.error(f"StatsProcessor: Failed to initialize MlflowClient: {e}")
                self.mlflow_client = None  # Ensure it's None on failure
        elif self.mlflow_client is not None:
            logger.info("StatsProcessor: Using injected MlflowClient.")
        else:
            logger.warning(
                "StatsProcessor: No MLflow run ID provided and no client injected, MLflow logging disabled."
            )

        logger.info("StatsProcessor initialized.")

    def _aggregate_values(self, values: list[float], method: str) -> float | int | None:
        """Aggregates a list of values based on the specified method."""
        if not values:
            return None
        try:
            finite_values = [v for v in values if np.isfinite(v)]
            if not finite_values:
                logger.debug(
                    f"No finite values found for aggregation method '{method}'."
                )
                return None

            if method == "latest":
                return finite_values[-1]
            elif method == "mean":
                return float(np.mean(finite_values))
            elif method == "sum":
                result = np.sum(finite_values)
                # Check if result is effectively an integer
                return (
                    int(result) if np.isclose(result, round(result)) else float(result)
                )
            elif method == "min":
                result = np.min(finite_values)
                return (
                    int(result) if np.isclose(result, round(result)) else float(result)
                )
            elif method == "max":
                result = np.max(finite_values)
                return (
                    int(result) if np.isclose(result, round(result)) else float(result)
                )
            elif method == "std":
                # std of a single value is 0, handle case with multiple identical values
                return float(np.std(finite_values)) if len(finite_values) > 1 else 0.0
            elif method == "count":
                return len(finite_values)
            else:
                logger.warning(f"Unsupported aggregation method: {method}")
                return None
        except Exception as e:
            logger.error(f"Error during aggregation '{method}': {e}")
            raise ProcessingError(f"Aggregation failed for method {method}") from e

    def _calculate_rate(
        self,
        metric_config: MetricConfig,
        context: LogContext,
        raw_data_for_interval: dict[int, dict[str, list[RawMetricEvent]]],
    ) -> float | None:
        """Calculates rate per second for a given metric over the interval."""
        if (
            metric_config.aggregation != "rate"
            or not metric_config.rate_numerator_event
        ):
            return None

        event_key = metric_config.rate_numerator_event
        time_delta = context.current_time - context.last_log_time
        if time_delta <= 1e-6:  # Use a smaller epsilon
            logger.debug(
                f"Time delta too small ({time_delta:.4f}s) for rate calculation of '{metric_config.name}'."
            )
            return None  # Avoid division by zero/tiny interval

        numerator_count = 0.0
        # Sum values for the numerator event across all steps in the interval
        for _step, step_data in raw_data_for_interval.items():
            if event_key in step_data:
                # Sum the 'value' field of the numerator events
                values = [float(e.value) for e in step_data[event_key] if e.is_valid()]
                numerator_count += sum(values)

        if numerator_count == 0:
            logger.debug(
                f"Numerator count is zero for rate calculation of '{metric_config.name}'."
            )
            return 0.0  # Return 0 rate if no events occurred

        rate = numerator_count / time_delta
        logger.debug(
            f"Calculated rate for '{metric_config.name}': {numerator_count} / {time_delta:.4f}s = {rate:.4f}"
        )
        return rate

    def _should_log(
        self, metric_config: MetricConfig, current_step: int, context: LogContext
    ) -> bool:
        """Determines if a metric should be logged based on step OR time frequency."""
        metric_name = metric_config.name

        # Check step frequency
        log_by_step = (
            metric_config.log_frequency_steps > 0
            and current_step >= 0  # Ensure step is valid
            and current_step % metric_config.log_frequency_steps == 0
        )
        if log_by_step:
            logger.debug(
                f"Logging '{metric_name}' due to step frequency ({current_step} % {metric_config.log_frequency_steps} == 0)."
            )
            return True

        # Check time frequency
        last_logged_time = self._last_log_time.get(metric_name, 0.0)
        time_delta = context.current_time - last_logged_time
        log_by_time = (
            metric_config.log_frequency_seconds > 0
            and time_delta >= metric_config.log_frequency_seconds
        )
        if log_by_time:
            logger.debug(
                f"Logging '{metric_name}' due to time frequency ({time_delta:.2f}s >= {metric_config.log_frequency_seconds:.2f}s)."
            )
            return True

        # If neither frequency is set > 0, never log automatically
        if (
            metric_config.log_frequency_steps <= 0
            and metric_config.log_frequency_seconds <= 0
        ):
            logger.debug(
                f"Metric '{metric_name}' has no positive log frequency, skipping automatic logging."
            )
            return False

        return False  # Default case if neither condition met

    def _log_to_targets(
        self,
        metric_config: MetricConfig,
        value: float | int,
        log_step: int,
        log_time: float,
    ):
        """Logs the processed value to configured targets."""
        if not np.isfinite(value):
            logger.warning(
                f"Attempted to log non-finite value ({value}) for {metric_config.name}. Skipping."
            )
            return

        # Ensure value is float for consistency, especially for MLflow/TB
        log_value = float(value)
        metric_name = metric_config.name

        if (
            "mlflow" in metric_config.log_to
            and self.mlflow_client
            and self.mlflow_run_id
        ):
            try:
                # Use the potentially injected client
                self.mlflow_client.log_metric(
                    run_id=self.mlflow_run_id,
                    key=metric_name,
                    value=log_value,
                    step=log_step,
                    timestamp=int(log_time * 1000),  # MLflow expects ms timestamp
                )
                logger.debug(
                    f"Logged '{metric_name}'={log_value:.4f} to MLflow at step {log_step}."
                )
            except Exception as e:
                logger.error(f"Failed to log {metric_name} to MLflow: {e}")
        if "tensorboard" in metric_config.log_to and self.tb_writer:
            try:
                self.tb_writer.add_scalar(metric_name, log_value, log_step)
                logger.debug(
                    f"Logged '{metric_name}'={log_value:.4f} to TensorBoard at step {log_step}."
                )
            except Exception as e:
                logger.error(f"Failed to log {metric_name} to TensorBoard: {e}")
        if "console" in metric_config.log_to:
            # Use standard logging for console output
            logger.info(f"STATS [{log_step}]: {metric_name} = {log_value:.4f}")

        # Update last logged time for this metric after successful logging attempt
        self._last_log_time[metric_name] = log_time

    def process_and_log(
        self, raw_data: dict[int, dict[str, list[RawMetricEvent]]], context: LogContext
    ):
        """Processes raw data and logs aggregated metrics."""
        if not raw_data:
            logger.debug("process_and_log called with no raw data.")
            return

        # --- Step 1: Aggregate non-rate metrics per step ---
        # metric_name -> step -> aggregated_value
        aggregated_step_values: dict[str, dict[int, float | int]] = defaultdict(dict)
        processed_event_keys: set[str] = set()  # Track which event keys were processed

        for step, step_event_dict in sorted(raw_data.items()):
            for metric_config in self.config.metrics:
                if metric_config.aggregation == "rate":
                    continue  # Skip rate metrics in this phase

                event_key = metric_config.event_key
                processed_event_keys.add(
                    event_key
                )  # Mark event key as potentially processed

                if event_key in step_event_dict:
                    event_list = step_event_dict[event_key]
                    values_to_aggregate: list[float] = []

                    if metric_config.context_key:
                        # Extract value from context
                        for event in event_list:
                            if metric_config.context_key in event.context:
                                try:
                                    val = float(
                                        event.context[metric_config.context_key]
                                    )
                                    if np.isfinite(val):
                                        values_to_aggregate.append(val)
                                except (ValueError, TypeError):
                                    logger.warning(
                                        f"Could not convert context value '{event.context.get(metric_config.context_key)}' to float for metric '{metric_config.name}' at step {step}."
                                    )
                    else:
                        # Extract value from event's value field
                        values_to_aggregate = [
                            float(e.value) for e in event_list if e.is_valid()
                        ]

                    if values_to_aggregate:
                        agg_value = self._aggregate_values(
                            values_to_aggregate, metric_config.aggregation
                        )
                        if agg_value is not None:
                            aggregated_step_values[metric_config.name][step] = agg_value
                        else:
                            logger.debug(
                                f"Aggregation resulted in None for metric '{metric_config.name}' at step {step}."
                            )
                    else:
                        logger.debug(
                            f"No valid values to aggregate for metric '{metric_config.name}' at step {step}."
                        )

        # --- Step 2: Log aggregated non-rate metrics based on frequency ---
        for metric_name, step_values in aggregated_step_values.items():
            if not step_values:
                continue

            # Use a different variable name to avoid redefining metric_config from outer scope
            current_metric_config: MetricConfig | None = self._metric_configs.get(
                metric_name
            )
            # Add check and assertion for None before proceeding
            if current_metric_config is None:
                logger.warning(
                    f"Metric config not found for '{metric_name}' during logging."
                )
                continue
            # assert current_metric_config is not None # mypy knows this from the 'if' check

            # Determine the step to log against (usually the latest step in the batch for this metric)
            latest_step_in_batch = max(step_values.keys())
            value_to_log = step_values[latest_step_in_batch]

            if self._should_log(current_metric_config, latest_step_in_batch, context):
                self._log_to_targets(
                    current_metric_config,
                    value_to_log,
                    latest_step_in_batch,
                    context.current_time,
                )

        # --- Step 3: Calculate and log rate metrics ---
        for rate_metric_config in self.config.metrics:
            if rate_metric_config.aggregation == "rate":
                # Log rate against the overall latest step in the context
                log_step = context.latest_step
                # Check time frequency for rate logging
                if self._should_log(rate_metric_config, log_step, context):
                    rate_value = self._calculate_rate(
                        rate_metric_config, context, raw_data
                    )
                    if rate_value is not None:
                        self._log_to_targets(
                            rate_metric_config,
                            rate_value,
                            log_step,
                            context.current_time,
                        )
                    else:
                        logger.debug(
                            f"Rate calculation returned None for metric '{rate_metric_config.name}'."
                        )

        # --- Step 4: Flush TensorBoard writer ---
        if self.tb_writer:
            try:
                self.tb_writer.flush()
            except Exception as e:
                logger.error(f"Error flushing TensorBoard writer: {e}")
