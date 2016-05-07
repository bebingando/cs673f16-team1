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

class TestCreate(unittest.TestCase):
 def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
        datetime.datetime.strptime("04/01/2015", "%m/%d/%Y").date()
        self.user = []
        self.user = self.user+[User(
            username='admin',
            password='pass'
        )]
        self.user = self.user+[User(
            username='test0',
            password='12345',
            email = 'test1@haha.xixi',
            first_name = 'test',
            last_name = 'blabla'
        ),User(
            username='test0',
            password='3456',
            email = 'test2@xixi.haha',
            first_name = 'hahaha',
            last_name = 'huhuhu'
        ),User(
            username='test1',
            password='1256',
            email = 'test1@haha.xixi',
            first_name = 'rad',
            last_name = 'cvb'
        ),User(
            username='test3',
            password='adfaa546ag',
            email = '',
            first_name = 'ewer',
            last_name = 'ndn'
        )
        ]


        self.nameArray=[]
        self.nameArray='test0'


 def test_story(self):
        self.home()
        self.passwordConfirm()
        self.nameConfirm()
       # self.emailConfirm()
       # self.withoutEmail()
        
        self.activate()
        self.deleteTestUser()
        return True

 def home(self):
        try:
            self.driver.get(self.base_url + "/")

        except Exception:
            return False
        return True


 def passwordConfirm(self):
        driver = self.driver
        user = self.user[1]
        self.createUser(1)

        driver.find_element_by_id("id_password1").clear()
        driver.find_element_by_id("id_password1").send_keys(user.password)
        driver.find_element_by_id("id_password2").clear()
        driver.find_element_by_id("id_password2").send_keys(user.password)
        time.sleep(2)

        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_xpath("//a[@href='/']").click()

        return True

 def nameConfirm(self):
        driver = self.driver
        user = self.user[2]
        self.createUser(2)

        time.sleep(2)
        driver.get(self.base_url + "/")

 def emailConfirm(self):
        driver = self.driver
        user = self.user[3]
        self.createUser(3)
        
        time.sleep(2)
        driver.get(self.base_url + "/")

 def withoutEmail(self):
        driver = self.driver
        user = self.user[4]
        self.createUser(4)

        time.sleep(2)
        driver.get(self.base_url + "/")

 def failLogin(self):
        driver = self.driver
        user = self.user[1]
       # driver.find_element_by_link_text("Sign In").click()

        # login with password and name but, not active
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys(user.username)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(user.password)
        #driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(2)

        driver.get(self.base_url + "/")
        return True



 def activate(self):
        driver = self.driver
        self.login(0)
        driver.get(self.base_url + "/admin/auth/user/")
  
        driver.find_element_by_link_text('test0').click()
        driver.find_element_by_xpath("//input[@id='id_is_active']").click()
	time.sleep(2)

        driver.find_element_by_xpath("//input[@id='id_is_staff']").click()
        driver.find_element_by_xpath("//input[@value='Save']").click()
        driver.find_element_by_link_text("Log out").click()
        driver.get(self.base_url + "/")

        self.login(1)
        time.sleep(2)
        driver.find_element_by_link_text("test0").click()
        driver.find_element_by_xpath("//a[@href='/signout']").click()
        driver.get(self.base_url + "/")

 def deleteTestUser(self):
        driver = self.driver
        self.login(0)
        driver.get(self.base_url + "/admin/auth/user/")

        #driver.find_element_by_xpath("//input[@value='16']").click()
        #driver.find_element_by_xpath("//option[@value='delete_selected']").click()
        #driver.find_element_by_xpath("//button[@type='submit']").click()
        #driver.find_element_by_xpath("//input[@type='submit']").click()


        driver.find_element_by_link_text('test0').click()
        driver.find_element_by_link_text("Delete").click()
       
	time.sleep(2)

        driver.find_element_by_xpath("//input[@type='submit']").click()
        #driver.find_element_by_link_text('test1').click()
        #driver.find_element_by_link_text("Delete").click()
        #time.sleep(1)

        #driver.find_element_by_xpath("//input[@type='submit']").click()

        driver.find_element_by_link_text("Log out").click()
        driver.get(self.base_url + "/")

        return True




 def createUser(self,i):
        driver = self.driver
        user = self.user[i]
        self.login(i)
        driver.find_element_by_xpath("//a[@href='/signup']").click()

        driver.find_element_by_id("id_first_name").clear()
        driver.find_element_by_id("id_first_name").send_keys(user.first_name)
        driver.find_element_by_id("id_last_name").clear()
        driver.find_element_by_id("id_last_name").send_keys(user.last_name)
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys(user.email)
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys(user.username)
        driver.find_element_by_id("id_password1").clear()
        driver.find_element_by_id("id_password1").send_keys(user.password)
        driver.find_element_by_id("id_password2").clear()
        if i == 1:
            driver.find_element_by_id("id_password2").send_keys("23456")
        else:
            driver.find_element_by_id("id_password2").send_keys(user.password)

        driver.find_element_by_xpath("//button[@type='submit']").click()

        return True


 def login(self,i):
        driver = self.driver
        user = self.user[i]
        driver.find_element_by_link_text("Sign In").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys(user.username)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(user.password)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(2)
        return True





 def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
