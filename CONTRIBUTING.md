# Contributing

Contributions are welcome through public GitHub issues and pull requests.

## Before opening a pull request

1. Open or reference an issue describing the proposed change.
2. Keep each pull request focused on one purpose.
3. Add or update tests for analytical code.
4. Update documentation when behavior changes.
5. Confirm that no restricted, confidential, or identifiable data are included.

## Local checks

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

## Review standard

Analytical changes are reviewed for:

- statistical correctness;
- transparent assumptions;
- reproducibility;
- backward compatibility;
- test coverage;
- documentation quality.

AI-assisted contributions are permitted. Contributors remain responsible for verifying code, tests, citations, and methodological claims.
