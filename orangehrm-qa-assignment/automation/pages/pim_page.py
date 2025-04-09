from selenium.webdriver.common.by import By
from .base_page import BasePage

class PIMPage(BasePage):
    # Locators
    PIM_MENU = (By.XPATH, "//span[text()='PIM']")
    ADD_EMPLOYEE_BUTTON = (By.LINK_TEXT, "Add Employee")
    FIRST_NAME_FIELD = (By.NAME, "firstName")
    LAST_NAME_FIELD = (By.NAME, "lastName")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    EMPLOYEE_LIST_BUTTON = (By.LINK_TEXT, "Employee List")
    SEARCH_EMPLOYEE_NAME = (By.XPATH, "//label[text()='Employee Name']/following::input[1]")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    EMPLOYEE_RECORD = (By.CSS_SELECTOR, ".oxd-table-card")
    DELETE_BUTTON = (By.CSS_SELECTOR, "button[title='Delete']")
    CONFIRM_DELETE = (By.CSS_SELECTOR, ".oxd-button--label-danger")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_pim(self):
        self.click(self.PIM_MENU)

    def add_employee(self, first_name, last_name):
        self.click(self.ADD_EMPLOYEE_BUTTON)
        self.enter_text(self.FIRST_NAME_FIELD, first_name)
        self.enter_text(self.LAST_NAME_FIELD, last_name)
        self.click(self.SAVE_BUTTON)

    def search_employee(self, name):
        self.click(self.EMPLOYEE_LIST_BUTTON)
        self.enter_text(self.SEARCH_EMPLOYEE_NAME, name)
        self.click(self.SEARCH_BUTTON)

    def verify_employee_in_list(self, name):
        employees = self.driver.find_elements(*self.EMPLOYEE_RECORD)
        for employee in employees:
            if name in employee.text:
                return True
        return False

    def delete_employee(self, name):
        self.search_employee(name)
        self.click(self.DELETE_BUTTON)
        self.click(self.CONFIRM_DELETE)
