from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

#A test case to make sure a user can log directly into the Issue Tracker directly

class LoginTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        
    def test_login(self):
        #Verify login for a normal user works.
        self.driver.get("localhost:8000/issue_tracker/issue/create")
        self.driver.find_element_by_id("username").clear()
        self.driver.find_element_by_id("username").send_keys("admin")
        self.driver.find_element_by_id("password").clear()
        self.driver.find_element_by_id("password").send_keys("pass")
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual(
            "Create Issue",
            self.driver.find_element_by_link_text("Create Issue").text)
        self.driver.find_element_by_link_text("Logout").click()
