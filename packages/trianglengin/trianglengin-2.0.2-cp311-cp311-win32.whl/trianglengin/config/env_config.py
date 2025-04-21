# File: src/trianglengin/config/env_config.py

from pydantic import BaseModel, Field, ValidationInfo, field_validator, model_validator


class EnvConfig(BaseModel):
    """Configuration for the game environment (Pydantic model)."""

    ROWS: int = Field(default=8, gt=0)
    COLS: int = Field(default=15, gt=0)
    PLAYABLE_RANGE_PER_ROW: list[tuple[int, int]] = Field(  # Use List, Tuple
        default=[(3, 12), (2, 13), (1, 14), (0, 15), (0, 15), (1, 14), (2, 13), (3, 12)]
    )
    NUM_SHAPE_SLOTS: int = Field(default=3, gt=0)

    REWARD_PER_PLACED_TRIANGLE: float = Field(default=0.01)
    REWARD_PER_CLEARED_TRIANGLE: float = Field(default=0.5)
    REWARD_PER_STEP_ALIVE: float = Field(default=0.005)
    PENALTY_GAME_OVER: float = Field(default=-10.0)

    @field_validator("PLAYABLE_RANGE_PER_ROW")
    @classmethod
    def check_playable_range_length(
        cls,
        v: list[tuple[int, int]],
        info: ValidationInfo,  # Use List, Tuple
    ) -> list[tuple[int, int]]:  # Use List, Tuple
        """Validates PLAYABLE_RANGE_PER_ROW."""
        rows = info.data.get("ROWS")
        cols = info.data.get("COLS")

        if rows is None or cols is None:
            return v

        if len(v) != rows:
            raise ValueError(
                f"PLAYABLE_RANGE_PER_ROW length ({len(v)}) must equal ROWS ({rows})"
            )

        for i, (start, end) in enumerate(v):
            if not (0 <= start <= cols):
                raise ValueError(
                    f"Row {i}: start_col ({start}) out of bounds [0, {cols}]."
                )
            if not (start <= end <= cols):
                raise ValueError(
                    f"Row {i}: end_col ({end}) invalid. Must be >= start_col ({start}) and <= COLS ({cols})."
                )
        return v

    @model_validator(mode="after")
    def check_cols_sufficient_for_ranges(self) -> "EnvConfig":
        """Ensure COLS is large enough for the specified ranges."""
        if hasattr(self, "PLAYABLE_RANGE_PER_ROW") and self.PLAYABLE_RANGE_PER_ROW:
            max_end_col = max(
                (end for _, end in self.PLAYABLE_RANGE_PER_ROW), default=0
            )
            if max_end_col > self.COLS:
                raise ValueError(
                    f"COLS ({self.COLS}) must be >= max end_col ({max_end_col})"
                )
        return self
