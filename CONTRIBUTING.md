# Contributing to Kodro

## Development Setup

```bash
git clone https://github.com/mharoon1578/kodro.git
cd kodro
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Code Style

- **Formatter**: Black (line length 100)
- **Linter**: Ruff
- **Type checker**: MyPy (strict mode)
- **Tests**: pytest with coverage

## PR Checklist

- [ ] Tests pass (`pytest tests/ -v`)
- [ ] Type check passes (`mypy kodro/`)
- [ ] Lint passes (`ruff check kodro/ tests/`)
- [ ] Documentation updated (README, docs/, CHANGELOG)
- [ ] CHANGELOG.md updated

## Adding New Features

### New CLI Command
1. Add to `kodro/main.py` with `@app.command()` decorator
2. Update `kodro/utils.py` with display helpers if needed
3. Add tests in `tests/`
4. Update README.md and docs/

### New Framework Constitution
1. Add to `FRAMEWORK_ADDENDUMS` in `kodro/constants.py`
2. Follow symbolic notation format (max 250 tokens)
3. Include: ARCH, TYPE/DATA, TEST, ANTI patterns
4. Update docs/configuration.md

### New Phase Module
1. Add to `PHASE_TEMPLATES` in `kodro/constants.py`
2. Keep under 300 tokens
3. Include: OUTPUT format, RULES, Quality gates
4. Update docs/pipeline.md

## Issue Reporting

Include:
1. Python version
2. Kodro version (`kodro --version`)
3. Integration and framework used
4. Minimal reproduction steps
5. Expected vs actual gatekeeper behavior
