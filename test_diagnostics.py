import pytest

from health_policy_eval import simulate_panel_its, validate_panel_its_data


def test_diagnostic_reports_balanced_panel():
    data = simulate_panel_its(n_units=4, n_periods=12, intervention_time=6, seed=2)
    diagnostic = validate_panel_its_data(
        data,
        outcome="outcome",
        unit="unit",
        time="time",
        intervention_time=6,
    )
    assert diagnostic.n_units == 4
    assert diagnostic.min_pre_periods == 6
    assert diagnostic.min_post_periods == 6
    assert diagnostic.is_valid


def test_insufficient_pre_periods_rejected():
    data = simulate_panel_its(n_units=4, n_periods=12, intervention_time=2, seed=2)
    with pytest.raises(ValueError):
        validate_panel_its_data(
            data,
            outcome="outcome",
            unit="unit",
            time="time",
            intervention_time=2,
            minimum_pre_periods=3,
        )
