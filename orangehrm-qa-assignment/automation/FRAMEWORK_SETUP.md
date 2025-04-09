# OrangeHRM Test Automation Framework v1.0

## Key Features
- **Modular Design**: Page Object Model pattern implementation
- **Multi-Browser Support**: Chrome, Firefox, Edge
- **Advanced Reporting**: HTML and Allure reports
- **CI/CD Ready**: GitHub Actions integration
- **Test Data Management**: JSON-based test data

## Quick Start Guide

### 1. Environment Setup
```bash
# Clone repository
git clone https://github.com/your-repo/orangehrm-qa-assignment.git
cd orangehrm-qa-assignment/automation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
Edit `config/settings.py` for:
- Environment URLs
- Browser settings
- Timeout configurations

### 3. Running Tests
```bash
# Run all tests with reporting
python run_tests.py

# Run specific test suite
pytest -m login tests/
pytest -m pim tests/

# Run with different browsers
BROWSER=firefox pytest tests/
```

### 4. Viewing Reports
- HTML Report: `results/<timestamp>/test_report.html`
- Allure Report:
  ```bash
  allure serve results/allure_results
  ```

## Framework Architecture
```
automation/
├── config/              # Environment configurations
├── pages/               # Page Object classes
├── tests/               # Test scripts
├── data/                # Test data files
├── utils/               # Helper functions
├── results/             # Test reports
├── requirements.txt     # Dependencies
├── pytest.ini           # Pytest configuration
└── run_tests.py         # Test runner
```

## CI/CD Integration
Example GitHub Actions workflow:
```yaml
name: OrangeHRM Test Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9"]
        browser: [chrome, firefox]
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r automation/requirements.txt
    - name: Run tests
      env:
        BROWSER: ${{ matrix.browser }}
      run: |
        cd automation
        python run_tests.py
    - name: Upload report
      uses: actions/upload-artifact@v3
      with:
        name: test-report-${{ matrix.browser }}
        path: automation/results
