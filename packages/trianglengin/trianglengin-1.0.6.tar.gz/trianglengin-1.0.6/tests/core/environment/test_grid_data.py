# File: tests/core/environment/test_grid_data.py
import copy
import logging

import numpy as np
import pytest

from trianglengin.config.env_config import EnvConfig
from trianglengin.core.environment.grid.grid_data import GridData

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def default_config() -> EnvConfig:
    """Fixture for default environment configuration."""
    return EnvConfig()


@pytest.fixture
def default_grid(default_config: EnvConfig) -> GridData:
    """Fixture for a default GridData instance."""
    grid = GridData(default_config)
    return grid


def test_grid_data_initialization(default_grid: GridData, default_config: EnvConfig):
    """Test GridData initialization matches config."""
    assert default_grid.rows == default_config.ROWS
    assert default_grid.cols == default_config.COLS
    assert default_grid.config == default_config
    assert default_grid._occupied_np.shape == (default_config.ROWS, default_config.COLS)
    assert default_grid._color_id_np.shape == (default_config.ROWS, default_config.COLS)
    assert default_grid._death_np.shape == (default_config.ROWS, default_config.COLS)
    assert default_grid._occupied_np.dtype == bool
    assert default_grid._color_id_np.dtype == np.int8
    assert default_grid._death_np.dtype == bool
    assert not default_grid._occupied_np.any()
    assert (default_grid._color_id_np == -1).all()
    for r in range(default_config.ROWS):
        start_col, end_col = default_config.PLAYABLE_RANGE_PER_ROW[r]
        for c in range(default_config.COLS):
            expected_death = not (start_col <= c < end_col)
            assert default_grid._death_np[r, c] == expected_death
    assert hasattr(default_grid, "_lines")
    assert default_grid._lines is not None
    assert hasattr(default_grid, "_coord_to_lines_map")
    assert default_grid._coord_to_lines_map is not None
    assert len(default_grid._lines) >= 0


def test_grid_data_valid(default_grid: GridData, default_config: EnvConfig):
    """Test the valid() method (checks bounds only)."""
    assert default_grid.valid(0, 0)
    assert default_grid.valid(default_config.ROWS - 1, 0)
    assert default_grid.valid(0, default_config.COLS - 1)
    assert default_grid.valid(default_config.ROWS - 1, default_config.COLS - 1)
    assert not default_grid.valid(-1, 0)
    assert not default_grid.valid(default_config.ROWS, 0)
    assert not default_grid.valid(0, -1)
    assert not default_grid.valid(0, default_config.COLS)


def test_grid_data_is_death(default_grid: GridData, default_config: EnvConfig):
    """Test the is_death() method."""
    for r in range(default_config.ROWS):
        if r >= len(default_config.PLAYABLE_RANGE_PER_ROW):
            start_col, end_col = 0, 0
        else:
            start_col, end_col = default_config.PLAYABLE_RANGE_PER_ROW[r]

        for c in range(default_config.COLS):
            expected_death = not (start_col <= c < end_col)
            if 0 <= r < default_config.ROWS and 0 <= c < default_config.COLS:
                assert default_grid.is_death(r, c) == expected_death
            else:
                with pytest.raises(IndexError):
                    default_grid.is_death(r, c)

    with pytest.raises(IndexError):
        default_grid.is_death(-1, 0)
    with pytest.raises(IndexError):
        default_grid.is_death(default_config.ROWS, 0)
    with pytest.raises(IndexError):
        default_grid.is_death(0, -1)
    with pytest.raises(IndexError):
        default_grid.is_death(0, default_config.COLS)


def test_grid_data_is_occupied(default_grid: GridData, default_config: EnvConfig):
    """Test the is_occupied() method."""
    live_r, live_c = -1, -1
    for r in range(default_config.ROWS):
        start_c, end_c = default_config.PLAYABLE_RANGE_PER_ROW[r]
        if start_c < end_c:
            live_r, live_c = r, start_c
            break
    if live_r == -1:
        pytest.skip("Test requires at least one live cell.")

    assert not default_grid.is_occupied(live_r, live_c)
    default_grid._occupied_np[live_r, live_c] = True
    default_grid._color_id_np[live_r, live_c] = 1
    assert default_grid.is_occupied(live_r, live_c)

    live_r2, live_c2 = -1, -1
    for r in range(default_config.ROWS):
        start_c, end_c = default_config.PLAYABLE_RANGE_PER_ROW[r]
        for c in range(start_c, end_c):
            if (r, c) != (live_r, live_c):
                live_r2, live_c2 = r, c
                break
        if live_r2 != -1:
            break
    if live_r2 != -1:
        assert not default_grid.is_occupied(live_r2, live_c2)

    death_r, death_c = -1, -1
    for r in range(default_grid.rows):
        start_c, end_c = default_config.PLAYABLE_RANGE_PER_ROW[r]
        if start_c > 0:
            death_r, death_c = r, start_c - 1
            break
        if end_c < default_grid.cols:
            death_r, death_c = r, end_c
            break
    if death_r == -1:
        pytest.skip("Could not find a death zone cell.")

    default_grid._occupied_np[death_r, death_c] = True
    assert default_grid.is_death(death_r, death_c)
    assert not default_grid.is_occupied(death_r, death_c)

    with pytest.raises(IndexError):
        default_grid.is_occupied(-1, 0)
    with pytest.raises(IndexError):
        default_grid.is_occupied(default_config.ROWS, 0)


def test_grid_data_deepcopy(default_grid: GridData):
    """Test that deepcopy creates a truly independent copy."""
    grid1 = default_grid
    grid1._occupied_np.fill(False)
    grid1._color_id_np.fill(-1)
    mod_r, mod_c = -1, -1
    for r in range(grid1.rows):
        start_c, end_c = grid1.config.PLAYABLE_RANGE_PER_ROW[r]
        if start_c < end_c:
            mod_r, mod_c = r, start_c
            break
    if mod_r == -1:
        pytest.skip("Cannot run deepcopy test without playable cells.")

    grid1._occupied_np[mod_r, mod_c] = True
    grid1._color_id_np[mod_r, mod_c] = 5

    grid2 = copy.deepcopy(grid1)

    assert grid1.rows == grid2.rows
    assert grid1.cols == grid2.cols
    assert grid1.config == grid2.config
    assert grid1._occupied_np is not grid2._occupied_np
    assert grid1._color_id_np is not grid2._color_id_np
    assert grid1._death_np is not grid2._death_np
    assert hasattr(grid1, "_lines") and hasattr(grid2, "_lines")
    assert grid1._lines is not grid2._lines
    assert hasattr(grid1, "_coord_to_lines_map") and hasattr(
        grid2, "_coord_to_lines_map"
    )
    assert grid1._coord_to_lines_map is not grid2._coord_to_lines_map
    assert np.array_equal(grid1._occupied_np, grid2._occupied_np)
    assert np.array_equal(grid1._color_id_np, grid2._color_id_np)
    assert np.array_equal(grid1._death_np, grid2._death_np)
    assert grid1._lines == grid2._lines
    assert grid1._coord_to_lines_map == grid2._coord_to_lines_map

    mod_r2, mod_c2 = -1, -1
    for r in range(grid2.rows):
        start_c, end_c = grid2.config.PLAYABLE_RANGE_PER_ROW[r]
        for c in range(start_c, end_c):
            if (r, c) != (mod_r, mod_c):
                mod_r2, mod_c2 = r, c
                break
        if mod_r2 != -1:
            break

    if mod_r2 != -1:
        grid2._occupied_np[mod_r2, mod_c2] = True
        grid2._color_id_np[mod_r2, mod_c2] = 3
        assert not grid1._occupied_np[mod_r2, mod_c2]
        assert grid1._color_id_np[mod_r2, mod_c2] == -1
    else:
        grid2._occupied_np[mod_r, mod_c] = False
        grid2._color_id_np[mod_r, mod_c] = -1
        assert grid1._occupied_np[mod_r, mod_c]
        assert grid1._color_id_np[mod_r, mod_c] == 5

    if grid2._lines:
        grid2._lines.append(((99, 99),))
        assert ((99, 99),) not in grid1._lines
    dummy_coord = (99, 99)
    dummy_line_fs = frozenset([dummy_coord])
    if grid2._coord_to_lines_map:
        grid2._coord_to_lines_map[dummy_coord] = {dummy_line_fs}
        assert dummy_coord not in grid1._coord_to_lines_map
