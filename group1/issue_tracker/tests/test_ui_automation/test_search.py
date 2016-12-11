from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import unittest
import time
import os


class SearchIssuesTestCase(unittest.TestCase):

    def setUp(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, '../chromedriver/chromedriver.exe')
        self.driver = webdriver.Chrome(filename)
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.username = "test"
        self.password = "testpw"
        self.title = "Searchable Title " + str(time.time())
        self.description = "These aren't the droids you're looking for"

    def tearDown(self):
        self.driver.quit()

    def create_testable_issue(self):
        """Creates an Issue to Search for."""
        self.driver.get(self.base_url + '/issue_tracker/issue/create')
        self.driver.find_element_by_id('username').send_keys(
            self.username)
        self.driver.find_element_by_id('password').send_keys(
            self.password)
        self.driver.find_element_by_id('password').send_keys(Keys.ENTER)
        time.sleep(1)
        self.driver.find_element_by_xpath(
            '//*[@id="id_project"]/option[2]').click()
        self.driver.find_element_by_xpath(
            '//*[@id="id_issue_type"]/option[2]').click()
        self.driver.find_element_by_id('id_title').send_keys(self.title)
        self.driver.find_element_by_id('id_description').send_keys(self.description)
        self.driver.find_element_by_xpath(
            '//*[@id="id_priority"]/option[2]').click()
        self.driver.find_element_by_xpath(
            '//*[@id="id_assignee"]/option[2]').click()
        self.driver.find_element_by_css_selector(
            '.btn-primary[value="Create"]').click()

    def test_search_single_field(self):
        """Searches for Issue using single field."""
        self.create_testable_issue()
        destination = self.driver.current_url
        # goes to the search page
        self.driver.find_element_by_css_selector(
            '#main-menu > li:nth-child(6) > a:nth-child(1)').click()
        time.sleep(1)
        # searches on title field
        self.driver.find_element_by_id('id_title').send_keys(self.title)
        self.driver.find_element_by_css_selector(
            '.btn-primary').click()
        time.sleep(1)
        title = self.driver.find_element_by_css_selector(
            '#page-wrapper > table:nth-child(2) > tbody:nth-child(2) > '
            'tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)')
        self.assertEqual(title.text, self.title)
        title.click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, destination)

    def test_search_multiple_fields(self):
        """Searches for Issue using multiple fields."""
        self.create_testable_issue()
        destination = self.driver.current_url

        time.sleep(1)
        self.driver.find_element_by_css_selector(
            '#main-menu > li:nth-child(6) > a:nth-child(1)').click()
        self.driver.find_element_by_css_selector('#id_priority').click()
        self.driver.find_element_by_css_selector(
            '#id_priority > option:nth-child(2)').click()
        time.sleep(1)
        self.driver.find_element_by_css_selector(
            '#id_description').send_keys('droids')
        self.driver.find_element_by_css_selector(
            '.btn-primary').click()
        time.sleep(1)
        self.driver.find_element_by_css_selector('table th:nth-of-type(6)').click()
        self.driver.find_element_by_css_selector('table th:nth-of-type(6)').click()
        title = self.driver.find_element_by_css_selector(
            '#page-wrapper > table:nth-child(2) > tbody:nth-child(2) > '
            'tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)')
        self.assertEqual(title.text, self.title)
        title.click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, destination)
