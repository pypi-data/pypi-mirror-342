# File: trieye/tests/test_config.py
import pytest
from pydantic import ValidationError

from trieye.config import (
    MetricConfig,
    PersistenceConfig,
    StatsConfig,
    TrieyeConfig,
)


def test_persistence_config_defaults():
    """Test PersistenceConfig default values."""
    config = PersistenceConfig()
    assert config.ROOT_DATA_DIR == ".trieye_data"
    assert config.SAVE_BUFFER is True
    assert config.BUFFER_SAVE_FREQ_STEPS == 1000


def test_stats_config_defaults():
    """Test StatsConfig default values."""
    config = StatsConfig()
    assert config.processing_interval_seconds == 1.0
    assert isinstance(config.metrics, list)
    assert len(config.metrics) == 0  # Default is empty


def test_metric_config_validation():
    """Test MetricConfig validation."""
    # Valid config
    MetricConfig(name="Test/Metric", source="custom", aggregation="mean")

    # Invalid rate config (missing numerator) - SHOULD RAISE ValidationError
    # Pydantic v2 wraps the ValueError. Match the specific error detail.
    # The error message structure might look like:
    # "1 validation error for MetricConfig\nrate_numerator_event\n  Value error, Metric 'Test/Rate' has aggregation 'rate' but 'rate_numerator_event' is not set. [type=value_error, ..."
    # We match the core message raised by our validator.
    with pytest.raises(
        ValidationError,
        match="Metric 'Test/Rate' has aggregation 'rate' but 'rate_numerator_event' is not set.",
    ):
        MetricConfig(name="Test/Rate", source="custom", aggregation="rate")

    # Valid rate config
    MetricConfig(
        name="Test/Rate",
        source="custom",
        aggregation="rate",
        rate_numerator_event="event_a",
    )

    # Duplicate metric names in StatsConfig - SHOULD RAISE ValidationError
    # Match the ValueError message raised by the validator.
    with pytest.raises(ValidationError, match="Duplicate metric names found"):
        StatsConfig(
            metrics=[
                MetricConfig(name="Dup", source="custom", aggregation="mean"),
                MetricConfig(name="Dup", source="custom", aggregation="sum"),
            ]
        )


def test_trieye_config_defaults_and_sync():
    """Test TrieyeConfig defaults and name syncing."""
    config = TrieyeConfig(app_name="my_app", run_name="my_run")

    assert config.app_name == "my_app"
    assert config.run_name == "my_run"
    assert isinstance(config.persistence, PersistenceConfig)
    assert isinstance(config.stats, StatsConfig)

    # Check if names were synced to persistence config during initialization
    assert config.persistence.APP_NAME == "my_app"
    assert config.persistence.RUN_NAME == "my_run"

    # Test modification after init and re-validation triggers sync
    config.run_name = "new_run"
    # Re-validate to trigger sync (model_validator mode='after' runs on validation)
    # Creating a new model instance from the dict forces re-validation
    config_dict = config.model_dump()
    new_config = TrieyeConfig.model_validate(config_dict)

    assert new_config.persistence.RUN_NAME == "new_run"
    assert new_config.persistence.APP_NAME == "my_app"  # App name shouldn't change
