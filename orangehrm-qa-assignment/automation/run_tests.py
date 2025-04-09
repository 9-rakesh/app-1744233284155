import pytest
import os
from datetime import datetime

def create_results_dir():
    """Create timestamped results directory"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = f"results/{timestamp}"
    os.makedirs(results_dir, exist_ok=True)
    return results_dir

if __name__ == "__main__":
    results_dir = create_results_dir()
    
    # Run tests with HTML report
    pytest.main([
        "-v",
        f"--html={results_dir}/test_report.html",
        "--self-contained-html",
        "tests/"
    ])
    
    # Generate Allure report
    if os.path.exists(f"{results_dir}/allure_results"):
        os.system(f"allure generate {results_dir}/allure_results -o {results_dir}/allure_report --clean")
        print(f"\nReports generated in: {os.path.abspath(results_dir)}")
