# File: trieye/trieye/serializer.py
import json
import logging
from collections import deque
from pathlib import Path
from typing import Any

import cloudpickle
import numpy as np
import torch
from pydantic import BaseModel, ValidationError

# Use relative imports within trieye
from .exceptions import SerializationError
from .schemas import BufferData, CheckpointData

logger = logging.getLogger(__name__)


class Serializer:
    """Handles serialization and deserialization of training data."""

    def load_checkpoint(self, path: Path) -> CheckpointData | None:
        """Loads and validates checkpoint data from a file."""
        if not path.exists():
            logger.warning(f"Checkpoint file not found: {path}")
            return None
        try:
            with path.open("rb") as f:
                loaded_data = cloudpickle.load(f)
            # Validate using Pydantic model
            return CheckpointData.model_validate(loaded_data)
        except ValidationError as e:
            logger.error(f"Pydantic validation failed for checkpoint {path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error loading/deserializing checkpoint from {path}: {e}")
            raise SerializationError(f"Failed to load checkpoint from {path}") from e

    def save_checkpoint(self, data: CheckpointData, path: Path):
        """Saves checkpoint data to a file using cloudpickle."""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("wb") as f:
                cloudpickle.dump(data, f)
            logger.info(f"Checkpoint data saved to {path}")
        except Exception as e:
            logger.error(f"Failed to save checkpoint file to {path}: {e}")
            raise SerializationError(f"Failed to save checkpoint to {path}") from e

    def load_buffer(self, path: Path) -> BufferData | None:
        """Loads and validates buffer data from a file."""
        if not path.exists():
            logger.warning(f"Buffer file not found: {path}")
            return None
        try:
            with path.open("rb") as f:
                loaded_data = cloudpickle.load(f)
            # Validate using Pydantic model (basic structure check)
            # Application using Trieye is responsible for content validation
            return BufferData.model_validate(loaded_data)
        except ValidationError as e:
            logger.error(f"Pydantic validation failed for buffer {path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to load/deserialize buffer from {path}: {e}")
            raise SerializationError(f"Failed to load buffer from {path}") from e

    def save_buffer(self, data: BufferData, path: Path):
        """Saves buffer data (list[Any]) to a file using cloudpickle."""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("wb") as f:
                cloudpickle.dump(data, f)
            logger.info(f"Buffer data saved to {path}")
        except Exception as e:
            logger.error(f"Error saving buffer to {path}: {e}")
            raise SerializationError(f"Failed to save buffer to {path}") from e

    def prepare_optimizer_state(self, optimizer_state_dict: dict) -> dict[str, Any]:
        """Prepares optimizer state dictionary, moving tensors to CPU."""
        optimizer_state_cpu = {}
        try:

            def move_to_cpu(item):
                if isinstance(item, torch.Tensor):
                    return item.cpu()
                elif isinstance(item, dict):
                    return {k: move_to_cpu(v) for k, v in item.items()}
                elif isinstance(item, list):
                    return [move_to_cpu(elem) for elem in item]
                else:
                    return item

            optimizer_state_cpu = move_to_cpu(optimizer_state_dict)
        except Exception as e:
            logger.error(f"Could not prepare optimizer state for saving: {e}")
            # Return original dict on error? Or empty? Returning empty for safety.
            return {}
        return optimizer_state_cpu

    def prepare_buffer_data(self, buffer_content: list[Any]) -> BufferData | None:
        """Prepares buffer data for saving."""
        try:
            # Basic check if it's a list
            if not isinstance(buffer_content, list):
                logger.error(f"Buffer content is not a list: {type(buffer_content)}")
                return None
            # No content validation here, just wrap it
            return BufferData(buffer_list=buffer_content)
        except Exception as e:
            logger.error(f"Error preparing buffer data for saving: {e}")
            return None

    def save_config_json(self, configs: dict[str, Any], path: Path):
        """Saves the configuration dictionary as JSON."""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w") as f:

                def default_serializer(obj):
                    if isinstance(obj, torch.Tensor | np.ndarray):
                        return "<tensor/array>"
                    if isinstance(obj, deque):
                        return list(obj)
                    if isinstance(obj, Path):
                        return str(obj)
                    if isinstance(obj, BaseModel):
                        return obj.model_dump()  # Use Pydantic's dump
                    try:
                        # Attempt standard JSON serialization first
                        # Fallback to dict or str representation
                        return obj.__dict__ if hasattr(obj, "__dict__") else str(obj)
                    except TypeError:
                        return f"<object of type {type(obj).__name__}>"

                json.dump(configs, f, indent=4, default=default_serializer)
            logger.info(f"Run config saved to {path}")
        except Exception as e:
            logger.error(f"Failed to save run config JSON to {path}: {e}")
            raise SerializationError(f"Failed to save config JSON to {path}") from e
