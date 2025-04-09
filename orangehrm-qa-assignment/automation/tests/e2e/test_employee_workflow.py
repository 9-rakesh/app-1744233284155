import pytest
from pages.login_page import LoginPage
from pages.pim_page import PIMPage
from utils.api_utils import APIUtils
from utils.db_utils import DatabaseUtils
from utils.performance_utils import PerformanceUtils
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

@pytest.mark.e2e
class TestEmployeeWorkflow:
    @pytest.fixture(autouse=True)
    def setup(self, browser):
        self.login_page = LoginPage(browser)
        self.pim_page = PIMPage(browser)
        self.api = APIUtils()
        self.db = DatabaseUtils()
        self.performance = PerformanceUtils()
        
        # Login to application
        self.login_page.load()
        self.login_page.login(settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD)
        
        yield
        
        # Cleanup
        self.db.close()
        self.api.close()

    @PerformanceUtils.measure_latency
    def test_add_employee_workflow(self, browser):
        """End-to-end test of employee creation workflow"""
        # API: Create employee via API
        employee_data = {
            "firstName": "Test",
            "lastName": "Employee",
            "empId": "E1001"
        }
        
        # Measure API performance
        api_result = self.performance.benchmark(
            lambda: self.api.post("/employees", data=employee_data),
            iterations=3
        )
        logger.info(f"API Performance: {api_result['mean']:.2f}s")
        
        # UI: Verify employee in PIM
        self.pim_page.navigate_to_pim()
        assert self.pim_page.search_employee(employee_data["empId"])
        
        # DB: Verify employee record
        db_result = self.db.execute_query(
            "SELECT * FROM employees WHERE emp_id = %s",
            (employee_data["empId"],)
        )
        assert len(db_result) == 1
        assert db_result[0]["first_name"] == employee_data["firstName"]
        
        # Performance: Measure full workflow
        workflow_time = self.performance.measure_latency(
            lambda: self._full_workflow(employee_data)
        )
        logger.info(f"Full workflow time: {workflow_time:.2f}s")

    def _full_workflow(self, employee_data):
        """Complete workflow for performance measurement"""
        self.api.post("/employees", data=employee_data)
        self.pim_page.navigate_to_pim()
        self.pim_page.search_employee(employee_data["empId"])
        self.db.execute_query(
            "SELECT * FROM employees WHERE emp_id = %s",
            (employee_data["empId"],)
        )
