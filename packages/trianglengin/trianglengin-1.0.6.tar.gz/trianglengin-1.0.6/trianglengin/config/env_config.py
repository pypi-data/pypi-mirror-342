# File: trianglengin/config/env_config.py
from pydantic import (
    BaseModel,
    Field,
    computed_field,
    field_validator,
    model_validator,
)


class EnvConfig(BaseModel):
    """Configuration for the game environment (Pydantic model)."""

    ROWS: int = Field(default=8, gt=0)
    COLS: int = Field(default=15, gt=0)
    PLAYABLE_RANGE_PER_ROW: list[tuple[int, int]] = Field(
        default=[
            (3, 12),  # 9 cols, centered in 15
            (2, 13),  # 11 cols
            (1, 14),  # 13 cols
            (0, 15),  # 15 cols
            (0, 15),  # 15 cols
            (1, 14),  # 13 cols
            (2, 13),  # 11 cols
            (3, 12),  # 9 cols
        ]
    )
    NUM_SHAPE_SLOTS: int = Field(default=3, gt=0)

    # --- Reward System Constants (v3) ---
    REWARD_PER_PLACED_TRIANGLE: float = Field(default=0.01)
    REWARD_PER_CLEARED_TRIANGLE: float = Field(default=0.5)
    REWARD_PER_STEP_ALIVE: float = Field(default=0.005)
    PENALTY_GAME_OVER: float = Field(default=-10.0)
    # --- End Reward System Constants ---

    @field_validator("PLAYABLE_RANGE_PER_ROW")
    @classmethod
    def check_playable_range_length(
        cls, v: list[tuple[int, int]], info
    ) -> list[tuple[int, int]]:
        """Validates PLAYABLE_RANGE_PER_ROW."""
        # Pydantic v2 uses 'values' in validator context
        data = getattr(info, "data", None) or getattr(info, "values", {})

        rows = data.get("ROWS")
        cols = data.get("COLS")

        if rows is None or cols is None:
            return v

        if len(v) != rows:
            raise ValueError(
                f"PLAYABLE_RANGE_PER_ROW length ({len(v)}) must equal ROWS ({rows})"
            )

        for i, (start, end) in enumerate(v):
            if not (0 <= start < cols):
                raise ValueError(
                    f"Row {i}: start_col ({start}) out of bounds [0, {cols})."
                )
            if not (start < end <= cols):
                raise ValueError(
                    f"Row {i}: end_col ({end}) invalid. Must be > start_col ({start}) and <= COLS ({cols})."
                )
            # Allow zero width ranges (rows that are entirely death zones)
            # if end - start <= 0:
            #     raise ValueError(
            #         f"Row {i}: Playable range width must be positive ({start}, {end})."
            #     )

        return v

    @model_validator(mode="after")
    def check_cols_sufficient_for_ranges(self) -> "EnvConfig":
        """Ensure COLS is large enough for the specified ranges."""
        if hasattr(self, "PLAYABLE_RANGE_PER_ROW") and self.PLAYABLE_RANGE_PER_ROW:
            max_end_col = 0
            for _, end in self.PLAYABLE_RANGE_PER_ROW:
                max_end_col = max(max_end_col, end)

            if max_end_col > self.COLS:
                raise ValueError(
                    f"COLS ({self.COLS}) must be >= the maximum end_col in PLAYABLE_RANGE_PER_ROW ({max_end_col})"
                )
        return self

    @computed_field  # type: ignore[misc]
    @property
    def ACTION_DIM(self) -> int:
        """Total number of possible actions (shape_slot * row * col)."""
        # Ensure attributes exist before calculating
        if (
            hasattr(self, "NUM_SHAPE_SLOTS")
            and hasattr(self, "ROWS")
            and hasattr(self, "COLS")
        ):
            return self.NUM_SHAPE_SLOTS * self.ROWS * self.COLS
        return 0  # Should not happen with pydantic defaults


# Ensure model is rebuilt after computed_field definition
EnvConfig.model_rebuild(force=True)
