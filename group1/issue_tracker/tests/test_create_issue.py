from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
import time
import re


class CreateIssueTestCase(unittest.TestCase):
    """Tests for the create issue page."""
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
        
    def test_create_issue(self, with_title=True):
        """Common test paths for the create issue page tests.
        """
        driver = self.driver
        driver.get(self.base_url + "/issue_tracker/issue/create/")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pass")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        """Find the element project id and issue type to start entering data"""
        driver.find_element_by_xpath(
            '//*[@id="id_project"]/option[2]').click()
        driver.find_element_by_xpath(
            '//*[@id="id_issue_type"]/option[2]').click()   
        if with_title:
            """Enter the title of issue"""
            driver.find_element_by_id('id_title').send_keys(
                'Sample Title')
            """Enter the description"""
            driver.find_element_by_id('id_description').send_keys(
            'This is sample description')
            """Enter the priority value """
            driver.find_element_by_xpath(
            '//*[@id="id_priority"]/option[2]').click()
            """Enter the assignee value"""
            driver.find_element_by_xpath(
            '//*[@id="id_assignee"]/option[2]').click()
            """Click on create button"""
            driver.find_element_by_css_selector(
            '.btn-primary[value="Create"]').click()
            time.sleep(1)
            """Locate logout and click on it"""
            driver.find_element_by_link_text("Logout").click()
            

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
