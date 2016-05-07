from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
from django.test import LiveServerTestCase
import time

class AdminTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_wrong_pwd_3_times(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Sign In").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("wrongpassword")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual(
            "Username or Password is incorrect ! Please try again ! If you fail more than 2 times, you need to wait 60s for next try!",
            driver.find_element_by_css_selector("div.alert.alert-danger").text)
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("wrongpassword")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual(
            "Username or Password is incorrect ! Please try again ! If you fail more than 1 times, you need to wait 60s for next try!",
            driver.find_element_by_css_selector("div.alert.alert-danger").text)
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("wrongpassword")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual(
            "you have tried many times, please signin after 60s later.",
            driver.find_element_by_css_selector("div.alert.alert-danger").text)

        #user has to wait 60s for next try, even now user inputs the username with the correct pwd, system won't let user login
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pass")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual(
            "you have tried many times, please signin after 60s later.",
            driver.find_element_by_css_selector("div.alert.alert-danger").text)
        time.sleep(10)
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pass")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual(
            'you have tried many times, please signin after 60s later.',
            driver.find_element_by_css_selector("div.alert.alert-danger").text)
        time.sleep(50)

        #after 60s, user can try again.
        #if user input wrong, count restarts from 0
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("wrongpassword")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual(
            "Username or Password is incorrect ! Please try again ! If you fail more than 2 times, you need to wait 60s for next try!",
            driver.find_element_by_css_selector("div.alert.alert-danger").text)

        #if user input correct pwd, log in successfully
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pass")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual(
            "admin",
            driver.find_element_by_link_text("admin").text)
        driver.find_element_by_link_text("admin").click()
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

    '''
    def test_admin_site(self):
        self.browser.get(self.live_server_url+'/admin')
        body = self.brower.find_element_by_tag_name('body')
        self.assertIn('Django administration',body.text)
    '''
