from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import unittest
import time
import os


class TestSideBar(unittest.TestCase):

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

    def test_sidebar(self):
        """Test the sidebar elements are all present and links function."""
        self.driver.get(self.base_url+"/issue_tracker")
        self.driver.find_element_by_id("username").send_keys(
            self.username)
        self.driver.find_element_by_id("password").send_keys(
            self.password)
        self.driver.find_element_by_id("password").send_keys(Keys.ENTER)
        time.sleep(1)
        self.assertTrue(self.driver.find_element_by_css_selector("nav.navbar-default.navbar-side").is_displayed())
        time.sleep(1)
        self.assertTrue("Create Issue" in self.driver.find_element_by_css_selector("nav.navbar-default.navbar-side li:nth-child(1)").text)
        self.assertTrue("Assigned" in self.driver.find_element_by_css_selector("nav.navbar-default.navbar-side li:nth-child(2)").text)
        self.assertTrue("Reported" in self.driver.find_element_by_css_selector("nav.navbar-default.navbar-side li:nth-child(3)").text)
        self.assertTrue("Closed" in self.driver.find_element_by_css_selector("nav.navbar-default.navbar-side li:nth-child(4)").text)
        self.assertTrue("Verified" in self.driver.find_element_by_css_selector("nav.navbar-default.navbar-side li:nth-child(5)").text)
        self.assertTrue("Search Issues" in self.driver.find_element_by_css_selector("nav.navbar-default.navbar-side li:nth-child(6)").text)
        self.assertTrue("PROJECT MANAGEMENT" in self.driver.find_element_by_css_selector("nav.navbar-default.navbar-side li:nth-child(7)").text)
        self.assertTrue("COMMUNICATION" in self.driver.find_element_by_css_selector("nav.navbar-default.navbar-side li:nth-child(8)").text)
        self.assertTrue("Admin Site" in self.driver.find_element_by_css_selector("nav.navbar-default.navbar-side li:nth-child(9)").text)
        self.driver.find_element_by_css_selector("a[href*='issue/create']").click()
        time.sleep(1)
        self.assertTrue("issue_tracker/issue/create/" in self.driver.current_url)
        self.driver.back()
        time.sleep(1)
        self.driver.find_element_by_css_selector("a[href*='issue/assigned']").click()
        time.sleep(1)
        self.assertTrue("issue_tracker/issue/assigned/" in self.driver.current_url)
        self.driver.back()
        time.sleep(1)
        self.driver.find_element_by_css_selector("a[href*='issue/reported']").click()
        time.sleep(1)
        self.assertTrue("issue_tracker/issue/reported/" in self.driver.current_url)
        self.driver.back()
        time.sleep(1)
        self.driver.find_element_by_css_selector("a[href*='issue/closed']").click()
        time.sleep(1)
        self.assertTrue("issue_tracker/issue/closed/" in self.driver.current_url)
        self.driver.back()
        time.sleep(1)
        self.driver.find_element_by_css_selector("a[href*='issue/verified']").click()
        time.sleep(1)
        self.assertTrue("issue_tracker/issue/verified/" in self.driver.current_url)