from selenium import webdriver
import unittest
import time
import os


class CreateIssueTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, '../chromedriver/chromedriver.exe')
        cls.driver = webdriver.Chrome(filename)
        cls.driver.implicitly_wait(30)
        cls.base_url = "http://127.0.0.1:8000"
        cls.username = "test"
        cls.password = "testpw"
        cls.title = "Sample Title"
        cls.description = "This is sample description"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_create_issue(self, with_title=True):
        """Test to create an Issue."""
        driver = self.driver
        driver.get(self.base_url + "/issue_tracker/issue/create/")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys(self.username)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(self.password)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_xpath(
            '//*[@id="id_project"]/option[2]').click()
        driver.find_element_by_xpath(
            '//*[@id="id_issue_type"]/option[2]').click()   
        if with_title:
            driver.find_element_by_id('id_title').send_keys(self.title)
            driver.find_element_by_id('id_description').send_keys(self.description)
            driver.find_element_by_xpath(
                '//*[@id="id_priority"]/option[2]').click()
            driver.find_element_by_xpath(
                '//*[@id="id_assignee"]/option[2]').click()
            driver.find_element_by_css_selector(
                '.btn-primary[value="Create"]').click()
            time.sleep(1)
            driver.find_element_by_link_text("Logout").click()