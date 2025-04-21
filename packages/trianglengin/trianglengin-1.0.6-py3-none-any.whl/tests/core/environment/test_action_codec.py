import pytest

# Import directly from the library being tested
from trianglengin.config import EnvConfig
from trianglengin.core.environment.action_codec import decode_action, encode_action

# Use fixtures from the local conftest.py
# Fixtures are implicitly injected by pytest


def test_encode_decode_action(default_env_config: EnvConfig):
    """Test encoding and decoding actions."""
    config = default_env_config
    # Test some valid actions
    actions_to_test = [
        (0, 0, 0),
        (config.NUM_SHAPE_SLOTS - 1, config.ROWS - 1, config.COLS - 1),
        (0, config.ROWS // 2, config.COLS // 2),
    ]
    for shape_idx, r, c in actions_to_test:
        encoded = encode_action(shape_idx, r, c, config)
        decoded_shape_idx, decoded_r, decoded_c = decode_action(encoded, config)
        assert (shape_idx, r, c) == (decoded_shape_idx, decoded_r, decoded_c)


def test_encode_action_invalid_input(default_env_config: EnvConfig):
    """Test encoding with invalid inputs."""
    config = default_env_config
    with pytest.raises(ValueError):
        encode_action(-1, 0, 0, config)  # Invalid shape index
    with pytest.raises(ValueError):
        encode_action(config.NUM_SHAPE_SLOTS, 0, 0, config)  # Invalid shape index
    with pytest.raises(ValueError):
        encode_action(0, -1, 0, config)  # Invalid row
    with pytest.raises(ValueError):
        encode_action(0, config.ROWS, 0, config)  # Invalid row
    with pytest.raises(ValueError):
        encode_action(0, 0, -1, config)  # Invalid col
    with pytest.raises(ValueError):
        encode_action(0, 0, config.COLS, config)  # Invalid col


def test_decode_action_invalid_input(default_env_config: EnvConfig):
    """Test decoding with invalid inputs."""
    config = default_env_config
    action_dim = int(config.ACTION_DIM)  # type: ignore[call-overload]
    with pytest.raises(ValueError):
        decode_action(-1, config)  # Invalid action index
    with pytest.raises(ValueError):
        decode_action(action_dim, config)  # Invalid action index (out of bounds)
