from selenium import webdriver
import unittest
import os


class LoginTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, '../chromedriver/chromedriver.exe')
        cls.driver = webdriver.Chrome(filename)
        cls.driver.implicitly_wait(30)
        cls.base_url = "http://127.0.0.1:8000"
        cls.username = "test"
        cls.password = "testpw"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        
    def test_login(self):
        """Test user can log in."""
        self.driver.get(self.base_url+"/issue_tracker/issue/create")
        self.driver.find_element_by_id("username").clear()
        self.driver.find_element_by_id("username").send_keys(self.username)
        self.driver.find_element_by_id("password").clear()
        self.driver.find_element_by_id("password").send_keys(self.password)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual(
            "Create Issue",
            self.driver.find_element_by_link_text("Create Issue").text)
        self.driver.find_element_by_link_text("Logout").click()
