"""Panel interrupted time-series estimation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.regression.linear_model import RegressionResultsWrapper

from .diagnostics import PanelDiagnostic, validate_panel_its_data


@dataclass
class PanelITSResult:
    """Container for a fitted panel interrupted time-series model."""

    model: RegressionResultsWrapper
    diagnostic: PanelDiagnostic
    formula: str
    intervention_time: int | float

    def coefficient_table(self) -> pd.DataFrame:
        """Return coefficients without invoking the expensive model summary."""
        confidence = self.model.conf_int()
        frame = pd.DataFrame(
            {
                "estimate": self.model.params,
                "std_error": self.model.bse,
                "p_value": self.model.pvalues,
                "ci_lower": confidence.iloc[:, 0],
                "ci_upper": confidence.iloc[:, 1],
            }
        )
        frame.index.name = "term"
        return frame

    def effect_table(self) -> pd.DataFrame:
        """Return the baseline trend, level change, and slope change."""
        frame = self.coefficient_table()
        time_term = next(
            (term for term in frame.index if term.startswith('Q("') and term.endswith('")')),
            None,
        )
        terms = [term for term in [time_term, "_post", "_time_after"] if term is not None]
        output = frame.loc[terms].copy()
        rename_map = {time_term: "time"} if time_term is not None else {}
        return output.rename(index=rename_map)


def _quote(column: str) -> str:
    """Quote a column name for use in a Patsy formula."""
    escaped = column.replace('"', '\\"')
    return f'Q("{escaped}")'


def fit_panel_its(
    data: pd.DataFrame,
    outcome: str,
    unit: str,
    time: str,
    intervention_time: int | float,
    controls: Iterable[str] | None = None,
    cluster: str | None = None,
    minimum_pre_periods: int = 3,
    minimum_post_periods: int = 3,
) -> PanelITSResult:
    """Fit a basic panel interrupted time-series model.

    The specification includes a linear baseline trend, an immediate level
    change, a post-intervention slope change, unit fixed effects, optional
    controls, and cluster-robust standard errors.

    Notes
    -----
    This implementation is intentionally transparent. Researchers should
    assess serial correlation, non-linearity, seasonality, co-interventions,
    and alternative time specifications for substantive applications.
    """
    controls = list(controls or [])
    cluster_column = cluster or unit

    all_columns = [outcome, unit, time, cluster_column, *controls]
    missing_columns = [column for column in all_columns if column not in data.columns]
    if missing_columns:
        raise KeyError(f"Missing columns: {sorted(set(missing_columns))}")

    diagnostic = validate_panel_its_data(
        data=data,
        outcome=outcome,
        unit=unit,
        time=time,
        intervention_time=intervention_time,
        minimum_pre_periods=minimum_pre_periods,
        minimum_post_periods=minimum_post_periods,
    )

    if not diagnostic.is_valid:
        raise ValueError(
            "Data validation failed. Resolve duplicate unit-time rows and missing required values."
        )

    frame = data.copy()
    frame["_post"] = (frame[time] >= intervention_time).astype(int)
    frame["_time_after"] = (frame[time] - intervention_time).clip(lower=0)

    rhs = [
        _quote(time),
        "_post",
        "_time_after",
        f"C({_quote(unit)})",
        *[_quote(column) for column in controls],
    ]
    formula = f"{_quote(outcome)} ~ " + " + ".join(rhs)

    fitted = smf.ols(formula=formula, data=frame).fit(
        cov_type="cluster",
        cov_kwds={"groups": frame[cluster_column]},
    )

    return PanelITSResult(
        model=fitted,
        diagnostic=diagnostic,
        formula=formula,
        intervention_time=intervention_time,
    )
