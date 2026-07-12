import pandas as pd
import pytest

from health_policy_eval import simulate_panel_its


def test_simulated_panel_shape_and_columns():
    data = simulate_panel_its(n_units=5, n_periods=10, intervention_time=5, seed=7)
    assert isinstance(data, pd.DataFrame)
    assert len(data) == 50
    assert {"unit", "time", "post", "time_after", "outcome"}.issubset(data.columns)
    assert data.duplicated(["unit", "time"]).sum() == 0


def test_invalid_intervention_time_rejected():
    with pytest.raises(ValueError):
        simulate_panel_its(n_units=5, n_periods=10, intervention_time=0)
