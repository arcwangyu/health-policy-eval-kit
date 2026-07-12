from health_policy_eval import fit_panel_its, simulate_panel_its


def test_panel_its_recovers_large_effects():
    data = simulate_panel_its(
        n_units=80,
        n_periods=30,
        intervention_time=15,
        baseline_slope=0.4,
        level_effect=-4.0,
        slope_effect=-0.25,
        noise_sd=0.4,
        seed=11,
    )

    result = fit_panel_its(
        data=data,
        outcome="outcome",
        unit="unit",
        time="time",
        intervention_time=15,
    )

    effects = result.effect_table()
    assert abs(effects.loc["_post", "estimate"] - (-4.0)) < 0.35
    assert abs(effects.loc["_time_after", "estimate"] - (-0.25)) < 0.05
    assert result.diagnostic.is_valid
