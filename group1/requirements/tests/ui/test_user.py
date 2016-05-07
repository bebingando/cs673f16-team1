from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
import time
import re


class TestProjects(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_projects(self):
        driver = self.driver
 	driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Sign Up").click()
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("tester@bu.edu")
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("tester")
	driver.find_element_by_id("id_password1").clear()
        driver.find_element_by_id("id_password1").send_keys("123")
	driver.find_element_by_id("id_password2").clear()
        driver.find_element_by_id("id_password2").send_keys("123")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_css_selector(
            "a.btn.btn-lg.btn-success").click()
	driver.find_element_by_link_text("Sign In").click()

        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pass")
        driver.find_element_by_xpath("//button[@type='submit']").click()
	driver.get(self.base_url + "/admin/auth/user/")
	driver.find_element_by_link_text("tester").click()
	
        driver.find_element_by_id("id_is_active").click()
	time.sleep(2)

        driver.find_element_by_xpath("//input[@value='Save']").click()
        driver.find_element_by_link_text("Log out").click()
	driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Sign In").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("tester")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("123")
        driver.find_element_by_xpath("//button[@type='submit']").click()
	time.sleep(2)

        driver.find_element_by_link_text("tester").click()
        driver.find_element_by_link_text("Logout").click()
        driver.find_element_by_link_text("Home").click()

    
 	driver.find_element_by_link_text("Sign In").click()

        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pass")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.get(self.base_url + "/admin/auth/user/")
        driver.find_element_by_link_text("tester").click()
        driver.find_element_by_link_text("Delete").click()
        time.sleep(2)

        driver.find_element_by_xpath("//input[@type='submit']").click()
        driver.find_element_by_link_text("Log out").click()
        driver.get(self.base_url + "/")

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()

