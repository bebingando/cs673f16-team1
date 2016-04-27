from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from requirements.models import Project, Story, Task, Iteration
from django.contrib.auth.models import User
import unittest
import time
import re
import datetime


# created by Zhi and Nora
class TestStory(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True



    def testStoryAndIteration(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Sign In").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pass")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_xpath(
            "//a[@onclick=\"showDialog('/req/newproject');\"]").click()
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
            "Selenium Test Iteration create, edit and delete")
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id(
            "id_description").send_keys("Iteration Tests")
        driver.find_element_by_link_text("Create Project").click()

        time.sleep(1)
        driver.find_element_by_link_text(
            "Selenium Test Iteration create, edit and delete").click()
        driver.find_element_by_link_text("Iterations").click()
        driver.find_element_by_link_text("New Iteration").click()
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys("1st test iteration")
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys(
            "selenium create iteration test")
        driver.find_element_by_xpath(
            "//div[@id='id_start_date_popover']/div/span/i").click()
        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, "//tr[2]/td[4]"):
                    break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_xpath("//tr[2]/td[4]").click()
        driver.find_element_by_xpath(
            "//div[@id='id_end_date_popover']/div/span").click()
        driver.find_element_by_xpath(
            "//div[5]/div[3]/table/tbody/tr[1]/td[4]").click()
        driver.find_element_by_link_text("Create").click()
        time.sleep(3)
        driver.find_element_by_xpath("//a[@href='javascript:void(0)']").click()


        driver.find_element_by_link_text("Dashboard").click()
        time.sleep(1)
        driver.find_element_by_link_text(
            "Selenium Test Iteration create, edit and delete").click()
        driver.find_element_by_link_text("Iterations").click()
        driver.find_element_by_link_text("New Iteration").click()
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
        driver.find_element_by_id("id_title").send_keys("1st test iteration")
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys(
            "selenium create iteration test.")
        driver.find_element_by_xpath(
            "//div[@id='id_start_date_popover']/div/span/i").click()
        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, "//tr[6]/td[1]"):
                    break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_xpath("//tr[6]/td[1]").click()
        driver.find_element_by_xpath(
            "//div[@id='id_end_date_popover']/div/span").click()
        driver.find_element_by_xpath(
            "//div[5]/div[3]/table/tbody/tr[6]/td[4]").click()
        driver.find_element_by_link_text("Create").click()
        time.sleep(1)

        driver.find_element_by_link_text(
            "Selenium Test Iteration create, edit and delete").click()

        driver.find_element_by_link_text("Project Detail").click()
        driver.find_element_by_css_selector("i.glyphicon.glyphicon-plus").click()
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys("test 0 hour")
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys("test 0 hour")
        driver.find_element_by_id("id_hours").clear()
        driver.find_element_by_id("id_hours").send_keys("0")

        driver.find_element_by_link_text("Create User Story").click()
        time.sleep(2)
        driver.find_element_by_link_text("Close").click()

        driver.find_element_by_css_selector("i.glyphicon.glyphicon-plus").click()
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys("test 2 hour")
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys("test 2 hour")
        driver.find_element_by_id("id_hours").clear()
        driver.find_element_by_id("id_hours").send_keys("2")

        driver.find_element_by_link_text("Create User Story").click()
        time.sleep(2)

        driver.find_element_by_xpath(
                "//a[contains(@data-del-story, '" + "test 2 hour" + "')]").click()
        driver.find_element_by_link_text("Delete User Story").click()
        time.sleep(2)

        driver.find_element_by_xpath(
            "//a[contains(@data-del-iteration, '1st test iteration')]").click()
        for i in range(60):
            try:
                if self.is_element_present(By.LINK_TEXT, "Delete"):
                    break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_link_text("Delete").click()
        time.sleep(1)

        driver.find_element_by_link_text("Dashboard").click()

        k= driver.find_elements_by_link_text("Delete")
        j = len(k)
        while j > 0 and driver.find_element_by_link_text("Delete"):
            driver.find_element_by_link_text("Dashboard").click()
            driver.find_element_by_link_text("Delete").click()
            for i in range(60):
                try:
                    if self.is_element_present(By.LINK_TEXT, "Delete Project"):
                        break
                except:
                    pass
                time.sleep(1)
            else:
                self.fail("time out")
            driver.find_element_by_link_text("Delete Project").click()
            j = j - 1


        time.sleep(1)
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
