"""Input diagnostics for panel interrupted time-series analysis."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class PanelDiagnostic:
    """Summary of structural checks for panel ITS data."""

    n_rows: int
    n_units: int
    n_time_points: int
    min_pre_periods: int
    min_post_periods: int
    duplicate_unit_time_rows: int
    missing_required_values: int

    @property
    def is_valid(self) -> bool:
        """Return True when no duplicate keys or missing required values are present."""
        return self.duplicate_unit_time_rows == 0 and self.missing_required_values == 0


def validate_panel_its_data(
    data: pd.DataFrame,
    outcome: str,
    unit: str,
    time: str,
    intervention_time: int | float,
    minimum_pre_periods: int = 3,
    minimum_post_periods: int = 3,
) -> PanelDiagnostic:
    """Validate the panel structure needed for a basic panel ITS model.

    The function reports structural problems and raises a ValueError when
    minimum pre/post requirements are not met.
    """
    required = [outcome, unit, time]
    missing_columns = [column for column in required if column not in data.columns]
    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")

    missing_required_values = int(data[required].isna().sum().sum())
    duplicate_rows = int(data.duplicated(subset=[unit, time]).sum())

    counts = (
        data.assign(_post=data[time] >= intervention_time)
        .groupby(unit, observed=True)["_post"]
        .agg(
            pre=lambda series: int((~series).sum()),
            post=lambda series: int(series.sum()),
        )
    )

    if counts.empty:
        raise ValueError("The dataset contains no units.")

    min_pre = int(counts["pre"].min())
    min_post = int(counts["post"].min())

    if min_pre < minimum_pre_periods:
        raise ValueError(
            f"At least one unit has only {min_pre} pre-intervention periods; "
            f"{minimum_pre_periods} are required."
        )
    if min_post < minimum_post_periods:
        raise ValueError(
            f"At least one unit has only {min_post} post-intervention periods; "
            f"{minimum_post_periods} are required."
        )

    return PanelDiagnostic(
        n_rows=int(len(data)),
        n_units=int(data[unit].nunique()),
        n_time_points=int(data[time].nunique()),
        min_pre_periods=min_pre,
        min_post_periods=min_post,
        duplicate_unit_time_rows=duplicate_rows,
        missing_required_values=missing_required_values,
    )
