# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
import time
import re


class TestIterations(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_iterations(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Sign In").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("pass")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_xpath(
            "//a[@onclick=\"showDialog('/requirements/newproject');\"]").click()
        
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys(
            "Move Test Iteration ")
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id(
            "id_description").send_keys("Move Tests")
        driver.find_element_by_link_text("Create Project").click()
        driver.find_element_by_link_text("Open").click()
        driver.find_element_by_link_text("Project Detail").click()

        driver.find_element_by_id("proj_icebox").click()
        driver.find_element_by_css_selector("i.glyphicon.glyphicon-plus").click()
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys(
            "Stroy 1 ")
        driver.find_element_by_id("id_hours").send_keys(
            "2")
        driver.find_element_by_link_text("Create User Story").click()
        time.sleep(2)
        driver.find_element_by_id("dropdownMenu1").click()
        time.sleep(2)
        value = driver.find_element_by_id("noiteration")
        if value.text == "No Iteration" :
            driver.find_element_by_link_text("Dashboard").click()
            driver.find_element_by_link_text("Delete").click()
            driver.find_element_by_link_text("Delete Project").click()
            time.sleep(1)
            driver.find_element_by_link_text("admin").click()
            driver.find_element_by_link_text("Logout").click()
            driver.find_element_by_link_text("Home").click()
    
    def tearDown(self):
        self.driver.quit()        
