# 🧪 Tests Directory

This directory contains unit tests and validation scripts to ensure the integrity of the data processing pipeline.

## 📁 Structure
- `test_eda_utils.py`: Validates the shared functions in `scripts/eda_utils.py`.

## 🛠️ Running Tests
We use `pytest` for automated testing. You can run all tests from the project root:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=scripts tests/
```

Tests are automatically executed by the **GitHub Actions CI pipeline** on every push to the repository.
