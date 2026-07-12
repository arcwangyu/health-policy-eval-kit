"""Runnable demonstration using synthetic data."""

from health_policy_eval import fit_panel_its, simulate_panel_its


def main() -> None:
    data = simulate_panel_its(
        n_units=30,
        n_periods=24,
        intervention_time=12,
        baseline_level=60.0,
        baseline_slope=0.25,
        level_effect=-3.0,
        slope_effect=-0.12,
        seed=2026,
    )

    result = fit_panel_its(
        data=data,
        outcome="outcome",
        unit="unit",
        time="time",
        intervention_time=12,
    )

    print("Formula:")
    print(result.formula)
    print("\nDiagnostics:")
    print(result.diagnostic)
    print("\nCore ITS effects:")
    print(result.effect_table().round(4))


if __name__ == "__main__":
    main()
