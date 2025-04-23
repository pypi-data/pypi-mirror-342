# File: trieye/tests/test_serializer.py
import json
from pathlib import Path

import cloudpickle
import numpy as np
import pytest
import torch

# Import from source
from trieye.schemas import BufferData, CheckpointData
from trieye.serializer import Serializer


@pytest.fixture
def serializer() -> Serializer:
    return Serializer()


def test_save_load_checkpoint(
    serializer: Serializer, dummy_checkpoint_data: CheckpointData, tmp_path: Path
):
    """Test saving and loading a valid CheckpointData object."""
    file_path = tmp_path / "checkpoint.pkl"
    serializer.save_checkpoint(dummy_checkpoint_data, file_path)
    assert file_path.exists()

    loaded_data = serializer.load_checkpoint(file_path)
    assert loaded_data is not None
    assert isinstance(loaded_data, CheckpointData)
    assert loaded_data.global_step == dummy_checkpoint_data.global_step
    assert loaded_data.model_state_dict == dummy_checkpoint_data.model_state_dict
    assert loaded_data.actor_state == dummy_checkpoint_data.actor_state


def test_load_nonexistent_checkpoint(serializer: Serializer, tmp_path: Path):
    """Test loading a checkpoint file that doesn't exist."""
    file_path = tmp_path / "nonexistent.pkl"
    loaded_data = serializer.load_checkpoint(file_path)
    assert loaded_data is None


def test_load_invalid_checkpoint(serializer: Serializer, tmp_path: Path):
    """Test loading a file that doesn't contain valid CheckpointData."""
    file_path = tmp_path / "invalid_checkpoint.pkl"
    # Save something else (e.g., a simple dict)
    with file_path.open("wb") as f:
        cloudpickle.dump({"invalid": "data"}, f)

    loaded_data = serializer.load_checkpoint(file_path)
    assert loaded_data is None


def test_save_load_buffer(
    serializer: Serializer, dummy_buffer_data: BufferData, tmp_path: Path
):
    """Test saving and loading a valid BufferData object."""
    file_path = tmp_path / "buffer.pkl"
    serializer.save_buffer(dummy_buffer_data, file_path)
    assert file_path.exists()

    loaded_data = serializer.load_buffer(file_path)
    assert loaded_data is not None
    assert isinstance(loaded_data, BufferData)
    assert loaded_data.buffer_list == dummy_buffer_data.buffer_list


def test_load_nonexistent_buffer(serializer: Serializer, tmp_path: Path):
    """Test loading a buffer file that doesn't exist."""
    file_path = tmp_path / "nonexistent_buffer.pkl"
    loaded_data = serializer.load_buffer(file_path)
    assert loaded_data is None


def test_prepare_optimizer_state(serializer: Serializer):
    """Test moving optimizer state tensors to CPU."""
    # Create a dummy optimizer state with tensors on CPU/GPU if possible
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    original_state = {
        "state": {
            0: {
                "step": torch.tensor(10, device=device),
                "exp_avg": torch.randn(5, device=device),
            },
            1: {
                "step": torch.tensor(5, device=device),
                "exp_avg": torch.randn(3, device=device),
            },
        },
        "param_groups": [{"lr": 0.01, "params": [0, 1]}],
    }

    prepared_state = serializer.prepare_optimizer_state(original_state)

    # Check structure remains
    assert "state" in prepared_state
    assert "param_groups" in prepared_state
    assert 0 in prepared_state["state"]

    # Check tensors are on CPU
    assert isinstance(prepared_state["state"][0]["step"], torch.Tensor)
    assert prepared_state["state"][0]["step"].device == torch.device("cpu")
    assert isinstance(prepared_state["state"][0]["exp_avg"], torch.Tensor)
    assert prepared_state["state"][0]["exp_avg"].device == torch.device("cpu")


def test_prepare_buffer_data(serializer: Serializer):
    """Test preparing buffer data."""
    buffer_list = ["exp1", ("exp2", {"a": 1}), 3]
    buffer_data = serializer.prepare_buffer_data(buffer_list)
    assert buffer_data is not None
    assert isinstance(buffer_data, BufferData)
    assert buffer_data.buffer_list == buffer_list

    # Test with non-list input - expect None
    invalid_buffer_data = serializer.prepare_buffer_data({"not": "a list"})  # type: ignore[arg-type]
    assert invalid_buffer_data is None


def test_save_config_json(serializer: Serializer, tmp_path: Path):
    """Test saving configuration to JSON."""
    config_dict = {
        "param_a": 1,
        "param_b": "string",
        "nested": {"c": 3.0},
        "path": Path("/tmp/test"),
        "tensor": torch.tensor([1, 2]),
        "numpy": np.array([3, 4]),
    }
    file_path = tmp_path / "config.json"
    serializer.save_config_json(config_dict, file_path)
    assert file_path.exists()

    # Load and check content
    with file_path.open("r") as f:
        loaded_json = json.load(f)
    assert loaded_json["param_a"] == 1
    assert loaded_json["nested"]["c"] == 3.0
    assert loaded_json["path"] == "/tmp/test"  # Path converted to string
    assert loaded_json["tensor"] == "<tensor/array>"  # Tensor represented as string
    assert loaded_json["numpy"] == "<tensor/array>"  # Numpy represented as string
