# Methodology notes

## Estimand

The basic panel interrupted time-series model estimates:

1. the pre-intervention linear trend;
2. the immediate outcome level change at the intervention;
3. the change in slope following the intervention.

Unit fixed effects absorb time-invariant differences between observational units. Cluster-robust standard errors allow within-unit dependence under large-cluster asymptotics.

## Minimum design checks

Before interpreting estimates, examine:

- the number of pre- and post-intervention observations;
- outcome definition and measurement stability;
- missing time points and duplicate unit-time records;
- concurrent reforms or shocks;
- seasonality and non-linear trends;
- anticipation and delayed implementation;
- serial correlation;
- heterogeneous intervention timing;
- sensitivity to alternative time windows and functional forms.

## Interpretation

`_post` is the estimated immediate level change at the first post-intervention period.

`_time_after` is the estimated difference between the post-intervention slope and the pre-intervention slope.

The total estimated effect several periods after implementation combines the level and slope-change terms.

## Reporting checklist

Report:

- intervention date and implementation process;
- unit and time definitions;
- number of units and observations;
- pre/post period counts;
- model equation and covariates;
- fixed effects and clustering level;
- diagnostics and robustness checks;
- coefficient estimates with confidence intervals;
- study limitations and identifying assumptions.
