# File: trieye/trieye/__init__.py
"""
Trieye Library: Asynchronous Stats & Persistence for ML Experiments using Ray.
"""

from .actor import TrieyeActor
from .actor_logic import ActorLogic
from .actor_state import ActorState
from .config import (
    DEFAULT_METRICS,
    AggregationMethod,
    DataSource,
    LogTarget,
    MetricConfig,
    PersistenceConfig,
    StatsConfig,
    TrieyeConfig,
    XAxis,
)
from .exceptions import (
    ConfigurationError,
    ProcessingError,
    SerializationError,
    TrieyeError,
)
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

__version__ = "0.1.0"

__all__ = [
    "DEFAULT_METRICS",  # Export default metrics list
    "ActorLogic",  # Added ActorLogic
    # Internal Components (exposed for potential extension/testing)
    "ActorState",  # Added ActorState
    "AggregationMethod",
    "BufferData",
    # Schemas & Types
    "CheckpointData",
    "ConfigurationError",
    "DataSource",
    "LoadedTrainingState",
    "LogContext",
    "LogTarget",
    "MetricConfig",
    "PathManager",
    "PersistenceConfig",
    "ProcessingError",  # Added ProcessingError
    "RawMetricEvent",
    "SerializationError",
    "Serializer",
    "StatsConfig",
    "StatsProcessor",
    # Core Actor
    "TrieyeActor",
    # Configuration
    "TrieyeConfig",
    # Exceptions
    "TrieyeError",
    "XAxis",
]
