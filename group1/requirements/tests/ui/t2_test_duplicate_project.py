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



    def test_duplicate_project_name(self):

        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Sign In").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pass")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_css_selector(
            "i.glyphicon.glyphicon-plus").click()
        for i in range(60):
            try:
                if self.is_element_present(By.ID, "id_title"):
                    break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys(
            "project title")
        for i in range(60):
            try:
                if self.is_element_present(By.ID, "id_description"):
                    break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys(
            "project description")
        driver.find_element_by_link_text("Create Project").click()
        time.sleep(1)
        driver.find_element_by_link_text("admin").click()
        driver.find_element_by_link_text("Logout").click()
        driver.find_element_by_link_text("Return to Home").click()


        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Sign In").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pass")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_css_selector(
            "i.glyphicon.glyphicon-plus").click()
        for i in range(60):
            try:
                if self.is_element_present(By.ID, "id_title"):
                    break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys(
            "project title")
        for i in range(60):
            try:
                if self.is_element_present(By.ID, "id_description"):
                    break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys(
            "project description")
        driver.find_element_by_link_text("Create Project").click()
        time.sleep(1)
        driver.find_element_by_link_text("Close").click()
        #time.sleep(1)
        #time.sleep(1)
        driver.find_element_by_xpath(
            "//a[contains(@data-del-proj, 'project title')]").click()
        time.sleep(1)
        driver.find_element_by_link_text("Delete Project").click()
        time.sleep(1)


        driver.find_element_by_link_text("admin").click()
        driver.find_element_by_link_text("Logout").click()


        driver.find_element_by_link_text("Return to Home").click()
        return True


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
