"""Synthetic data generators for reproducible examples."""

from __future__ import annotations

import numpy as np
import pandas as pd


def simulate_panel_its(
    n_units: int = 20,
    n_periods: int = 24,
    intervention_time: int = 12,
    baseline_level: float = 50.0,
    baseline_slope: float = 0.3,
    level_effect: float = -2.0,
    slope_effect: float = -0.1,
    unit_sd: float = 3.0,
    noise_sd: float = 1.0,
    seed: int | None = 2026,
) -> pd.DataFrame:
    """Simulate balanced panel interrupted time-series data.

    Parameters
    ----------
    n_units:
        Number of observational units.
    n_periods:
        Number of time points per unit.
    intervention_time:
        First time point classified as post-intervention.
    baseline_level:
        Expected outcome at time zero before unit-specific variation.
    baseline_slope:
        Pre-intervention time trend.
    level_effect:
        Immediate level change at the intervention.
    slope_effect:
        Change in slope after the intervention.
    unit_sd:
        Standard deviation of unit-specific intercepts.
    noise_sd:
        Standard deviation of observation-level noise.
    seed:
        Random seed.

    Returns
    -------
    pandas.DataFrame
        Columns: unit, time, post, time_after, outcome.
    """
    if n_units < 2:
        raise ValueError("n_units must be at least 2.")
    if n_periods < 4:
        raise ValueError("n_periods must be at least 4.")
    if not 1 <= intervention_time < n_periods - 1:
        raise ValueError(
            "intervention_time must leave at least one pre- and one post-intervention period."
        )
    if unit_sd < 0 or noise_sd < 0:
        raise ValueError("unit_sd and noise_sd must be non-negative.")

    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []

    unit_intercepts = rng.normal(0.0, unit_sd, size=n_units)

    for unit_index in range(n_units):
        unit_name = f"unit_{unit_index + 1:03d}"
        for time in range(n_periods):
            post = int(time >= intervention_time)
            time_after = max(0, time - intervention_time)
            expected = (
                baseline_level
                + unit_intercepts[unit_index]
                + baseline_slope * time
                + level_effect * post
                + slope_effect * time_after
            )
            outcome = expected + rng.normal(0.0, noise_sd)
            rows.append(
                {
                    "unit": unit_name,
                    "time": time,
                    "post": post,
                    "time_after": time_after,
                    "outcome": float(outcome),
                }
            )

    return pd.DataFrame(rows)
