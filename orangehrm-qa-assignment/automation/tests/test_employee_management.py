import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.pim_page import PIMPage

class TestEmployeeManagement:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.login_page = LoginPage(self.driver)
        self.pim_page = PIMPage(self.driver)
        # Login first
        self.login_page.login("Admin", "admin123")
        yield
        self.driver.quit()

    def test_add_employee(self):
        test_employee = ("John", "Doe")
        self.pim_page.navigate_to_pim()
        self.pim_page.add_employee(*test_employee)
        self.pim_page.search_employee(" ".join(test_employee))
        assert self.pim_page.verify_employee_in_list(" ".join(test_employee))

    def test_delete_employee(self):
        test_employee = ("Jane", "Smith")
        self.pim_page.navigate_to_pim()
        self.pim_page.add_employee(*test_employee)
        self.pim_page.search_employee(" ".join(test_employee))
        self.pim_page.delete_employee(" ".join(test_employee))
        assert not self.pim_page.verify_employee_in_list(" ".join(test_employee))

    def test_search_employee(self):
        self.pim_page.navigate_to_pim()
        self.pim_page.search_employee("Linda Anderson")
        assert self.pim_page.verify_employee_in_list("Linda Anderson")
