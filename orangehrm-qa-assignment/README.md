# OrangeHRM Test Automation Framework

## Overview
Comprehensive test automation framework for OrangeHRM with support for:
- Web UI testing (Selenium)
- API testing (REST services)
- Database validation
- Mobile testing (Appium)
- Performance benchmarking

## Features
- Cross-browser testing support
- Parallel test execution
- CI/CD ready with GitHub Actions
- Dockerized test environment
- Comprehensive reporting
- Page Object Model implementation
- Performance monitoring

## Getting Started

### Prerequisites
- Python 3.9+
- Docker (for containerized execution)
- Google Chrome/Firefox

### Installation
```bash
pip install -r automation/requirements.txt
```

## Test Execution

### Local Execution
```bash
# Run all tests with HTML report
pytest automation/tests -v --html=report.html

# Run specific test suite
pytest automation/tests/e2e -v

# Run with parallel execution (4 workers)
pytest automation/tests -n 4 --html=report.html

# Run with performance tracking
pytest automation/tests --perf-monitor
```

### Docker Execution
```bash
# Start all services in background
docker-compose up -d --build

# Run all tests
docker-compose run tests

# Run specific test suite
docker-compose run tests pytest automation/tests/e2e -v

# Scale Chrome nodes for parallel testing
docker-compose up -d --scale chrome=4

# View test results
open results/report.html  # Or on Windows: start results/report.html

# Stop and clean up containers
docker-compose down -v
```

## Framework Structure
```
📁 orangehrm-qa-assignment/
├── 📁 automation/
│   ├── 📁 config/          # Environment configurations
│   ├── 📁 pages/           # Page Object Models
│   ├── 📁 tests/           # Test cases
│   ├── 📁 utils/           # Utility modules
│   ├── requirements.txt    # Python dependencies
│   ├── pytest.ini          # Pytest configuration
│   └── run_tests.py        # Test runner
├── 📁 manual_testing/      # Manual test artifacts
├── 📁 results/             # Test outputs
├── .github/workflows/ci.yml # CI/CD pipeline
├── Dockerfile              # Test environment container
└── docker-compose.yml      # Service orchestration
```

## Configuration
Environment-specific settings are managed in:
- `config/test.json` - Docker test environment
- `config/staging.json` - Staging environment
- `config/production.json` - Production environment

## Reporting
Test results are generated in:
- HTML: `results/report.html`
- JUnit XML: `results/junit.xml` (CI/CD)
- Performance: `results/performance/`
- Screenshots: `results/screenshots/`

## CI/CD Pipeline
The GitHub Actions workflow:
1. Sets up Python environment
2. Starts Docker services
3. Runs tests in parallel
4. Uploads HTML report as artifact
5. Cleans up resources

## Writing Tests
1. Create Page Objects in `pages/` directory
2. Add test cases in `tests/` directory
3. Use utility modules for common operations

Example test:
```python
def test_login(browser):
    login_page = LoginPage(browser)
    login_page.load()
    login_page.login("admin", "admin123")
    assert login_page.is_logged_in()
```

## Support
For issues or questions, please open a GitHub issue.
