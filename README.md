# Health Policy Evaluation Kit

[![Tests](https://github.com/arcwangyu/health-policy-eval-kit/actions/workflows/tests.yml/badge.svg)](https://github.com/arcwangyu/health-policy-eval-kit/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A small, transparent Python toolkit for reproducible health-policy evaluation.

The first release focuses on **panel interrupted time-series analysis (panel ITS)** using unit fixed effects and cluster-robust standard errors. It includes synthetic data generation, input diagnostics, estimation, examples, tests, and bilingual documentation.

## Why this project exists

Health-policy studies often publish model descriptions without reusable code, tested data structures, or explicit diagnostics. This repository provides auditable workflows that researchers can run, inspect, adapt, and cite.

The project is intended for:

- health-policy and health-services researchers;
- public hospital and payment-reform evaluation;
- graduate teaching in quasi-experimental methods;
- reproducible methodological demonstrations.

## Current scope

Version `0.1.0` provides:

- simulation of multi-unit interrupted time-series data;
- validation of panel structure and pre/post observations;
- panel ITS estimation with unit fixed effects;
- cluster-robust standard errors at the unit level;
- optional covariate adjustment;
- tidy coefficient output;
- a fully runnable example;
- automated tests with GitHub Actions.

## Installation

Clone the repository and install it in editable mode:

```bash
git clone https://github.com/arcwangyu/health-policy-eval-kit.git
cd health-policy-eval-kit
python -m pip install -e ".[dev]"
```

## Quick start

```python
from health_policy_eval import simulate_panel_its, fit_panel_its

data = simulate_panel_its(
    n_units=30,
    n_periods=24,
    intervention_time=12,
    level_effect=-2.0,
    slope_effect=-0.15,
    seed=2026,
)

result = fit_panel_its(
    data=data,
    outcome="outcome",
    unit="unit",
    time="time",
    intervention_time=12,
)

print(result.effect_table())
```

Run the complete example:

```bash
python examples/01_panel_its_demo.py
```

## Model

For unit \(i\) at time \(t\), the baseline specification is:

\[
Y_{it} = \alpha_i + \beta_1 Time_t + \beta_2 Post_t
+ \beta_3 TimeAfter_t + \gamma X_{it} + \varepsilon_{it}
\]

where:

- \(\alpha_i\) represents unit fixed effects;
- `Post` estimates the immediate level change;
- `TimeAfter` estimates the post-intervention slope change;
- standard errors are clustered by unit.

This model does not establish causal effects by itself. Identification still depends on the intervention timing, absence of major co-interventions, functional-form adequacy, outcome measurement, and other design assumptions.

## Repository structure

```text
src/health_policy_eval/   package source
tests/                    automated tests
examples/                 runnable examples
docs/                     methodology and reporting guidance
.github/                  CI and contribution templates
```

## Reproducibility principles

1. Examples use synthetic data and can be run without restricted health data.
2. Public functions validate common structural errors before estimation.
3. Analytical changes require tests and maintainer review.
4. Releases are versioned and documented in `CHANGELOG.md`.
5. AI-assisted code must pass the same review and testing requirements as human-written code.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New contributors can begin with documentation improvements, additional diagnostics, or reproducible examples.

## Security

Do not upload patient-level, identifiable, confidential, or restricted institutional data. See [SECURITY.md](SECURITY.md).

## Citation

Citation metadata are provided in [CITATION.cff](CITATION.cff).

## License

MIT License. See [LICENSE](LICENSE).
