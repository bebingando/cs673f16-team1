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
from requirements.models import Project, Story, Task, Iteration
from django.contrib.auth.models import User

class TestDownloadfile(unittest.TestCase):

    admin_username="admin"
    admin_password="pass"
    proj_title = "PDF Report Test Project"


    proj_description = "To be or not to be-that is the question: Whether 'tis nobler in the mind to suffer The slings and arrows of outrageous fortune, Or to take arms against a sea of troubles, And, by opposing, end them. To die, to sleep- No more-and by a sleep to say we end The heartache and the thousand natural shocks That flesh is heir to-'tis a consummation Devoutly to be wished. To die, to sleep- To sleep, perchance to dream."



    iter_title1 = "Selenium Generated Iteration 1"
    iter_description1 = "1st Iteration created by selenium:------To be or not to be-that is the question: Whether 'tis nobler in the mind to suffer The slings and arrows of outrageous fortune, Or to take arms against a sea of troubles, And, by opposing, end them. To die, to sleep- No more-and by a sleep to say we end The heartache and the thousand natural shocks That flesh is heir to-'tis a consummation Devoutly to be wished. To die, to sleep- To sleep, perchance to dream."
    iter_title2 = "Selenium Generated Iteration 2"
    iter_description2 = "2rd Iteration created by selenium------To be or not to be-that is the question: Whether 'tis nobler in the mind to suffer The slings and arrows of outrageous fortune, Or to take arms against a sea of troubles, And, by opposing, end them. To die, to sleep- No more-and by a sleep to say we end The heartache and the thousand natural shocks That flesh is heir to-'tis a consummation Devoutly to be wished. To die, to sleep- To sleep, perchance to dream."
    iter_title3 = "Selenium Generated Iteration 3"
    iter_description3 = "3rd Iteration created by selenium------To be or not to be-that is the question: Whether 'tis nobler in the mind to suffer The slings and arrows of outrageous fortune, Or to take arms against a sea of troubles, And, by opposing, end them. To die, to sleep- No more-and by a sleep to say we end The heartache and the thousand natural shocks That flesh is heir to-'tis a consummation Devoutly to be wished. To die, to sleep- To sleep, perchance to dream."


    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True

        self.user = User(
            username='admin',
            password='pass'
        )

        self.story1 = Story(
            title='___Test Story 1___',
            description='___Test Story 1 Description------To be or not to be-that is the question: Whether \'tis nobler in the mind to suffer The slings and arrows of outrageous fortune, Or to take arms against a sea of troubles, And, by opposing, end them. To die, to sleep- No more-and by a sleep to say we end The heartache and the thousand natural shocks That flesh is heir to-\'tis a consummation Devoutly to be wished. To die, to sleep- To sleep, perchance to dream.',
            reason='___Story Reason___To be or not to be-that is the questionTo be or not to be-that is the question',
            test='___Story Test___To be or not to be-that is the questionTo be or not to be-that is the question',
            hours=3,
            status='Started',
            points='3 Points'
        )
        self.tasks1 = (Task(description='___Task Test 1.1___'),
                       Task(description='___Task Test 1.2___'),
                       Task(description='___Task Test 1.3___'))

        self.story2 = Story(
            title='___Test Story 2___',
            description='___Test Story 2 Description------To be or not to be-that is the question: Whether \'tis nobler in the mind to suffer The slings and arrows of outrageous fortune, Or to take arms against a sea of troubles, And, by opposing, end them. To die, to sleep- No more-and by a sleep to say we end The heartache and the thousand natural shocks That flesh is heir to-\'tis a consummation Devoutly to be wished. To die, to sleep- To sleep, perchance to dream.',
            reason='___Story Reason___To be or not to be-that is the questionTo be or not to be-that is the questionTo be or not to be-that is the question',
            test='___Story Test___To be or not to be-that is the questionTo be or not to be-that is the questionTo be or not to be-that is the question',
            hours=18,
            status='Unstarted',
            points='5 Points'
        )
        self.tasks2 = (Task(description='___Task Test 2.1___'),
                       Task(description='___Task Test 2.2___'),
                       Task(description='___Task Test 2.3___'))

        self.story3 = Story(
            title='___Test Story 3___',
            description='___Test Story 3 Description------To be or not to be-that is the question: Whether \'tis nobler in the mind to suffer The slings and arrows of outrageous fortune, Or to take arms against a sea of troubles, And, by opposing, end them. To die, to sleep- No more-and by a sleep to say we end The heartache and the thousand natural shocks That flesh is heir to-\'tis a consummation Devoutly to be wished. To die, to sleep- To sleep, perchance to dream.',
            reason='___Story Reason___To be or not to be-that is the questionTo be or not to be-that is the question',
            test='___Story Test___To be or not to be-that is the questionTo be or not to be-that is the question',
            hours=1,
            status='Completed',
            points='1 Point'
        )
        self.tasks3 = (Task(description='___Task Test 3.1___'),
                       Task(description='___Task Test 3.2___'))

        self.story4 = Story(
            title='___Test Story 4___',
            description='___Test Story 4 Description------To be or not to be-that is the question: Whether \'tis nobler in the mind to suffer The slings and arrows of outrageous fortune, Or to take arms against a sea of troubles, And, by opposing, end them. To die, to sleep- No more-and by a sleep to say we end The heartache and the thousand natural shocks That flesh is heir to-\'tis a consummation Devoutly to be wished. To die, to sleep- To sleep, perchance to dream.',
            reason='___Story Reason___To be or not to be-that is the questionTo be or not to be-that is the question',
            test='___Story Test___To be or not to be-that is the questionTo be or not to be-that is the question',
            hours=5,
            status='Accepted',
            points='2 Points'
        )
        self.tasks4 = (Task(description='___Task Test 4.1___'),)

        self.story5 = Story(
            title='___Test Story 5___',
            description='___Test Story 5 Description------To be or not to be-that is the question: Whether \'tis nobler in the mind to suffer The slings and arrows of outrageous fortune, Or to take arms against a sea of troubles, And, by opposing, end them. To die, to sleep- No more-and by a sleep to say we end The heartache and the thousand natural shocks That flesh is heir to-\'tis a consummation Devoutly to be wished. To die, to sleep- To sleep, perchance to dream.',
            reason='___Story Reason___To be or not to be-that is the questionTo be or not to be-that is the question',
            test='___Story Test___To be or not to be-that is the questionTo be or not to be-that is the question',
            hours=5,
            status='Started',
            points='0 Not Scaled'
        )
        self.tasks5 = (Task(description='___Task Test 5.1___'),)

    def test_downloadfile(self):
        self.create_Iteration()
        self.create_Story()
        self.move_story()
        self.download()
        #self.destroy()

    def create_Iteration(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Sign In").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys(TestDownloadfile.admin_username)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(TestDownloadfile.admin_password)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_css_selector(
            "i.glyphicon.glyphicon-plus").click()
        for i in range(60):
            try:
                if self.is_element_present(By.ID, "id_title"):
                    break
            except:
                pass
            
        else:
            self.fail("time out")
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys(
            TestDownloadfile.proj_title)
        for i in range(60):
            try:
                if self.is_element_present(By.ID, "id_description"):
                    break
            except:
                pass
            
        else:
            self.fail("time out")
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys(
            TestDownloadfile.proj_description)
        driver.find_element_by_link_text("Create Project").click()
        time.sleep(1)
        driver.find_element_by_xpath(
            "//a[contains(@data-open-proj, \'"+TestDownloadfile.proj_title+"\')]").click()
        #---Create iteration 1
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
        driver.find_element_by_id("id_title").send_keys(
            TestDownloadfile.iter_title1)
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys(
            TestDownloadfile.iter_description1)
        driver.find_element_by_xpath(
            "//div[@id='id_start_date_popover']/div/span/i").click()
        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, "//tr[1]/td[4]"):
                    break
            except:
                pass
            time.sleep(1)
        else:
            self.fail("time out")
        driver.find_element_by_xpath(
            "//div[@class='datetimepicker-days']/table/thead/tr[1]/th[3]").click()
        driver.find_element_by_xpath("//tr[2]/td[1]").click()
        driver.find_element_by_xpath(
            "//div[@id='id_end_date_popover']/div/span").click()
        #absolute path please be careful!!!!!!!!
        driver.find_element_by_xpath(
            "/html/body/div[5]/div[3]/table/thead/tr[1]/th[3]").click()
        driver.find_element_by_xpath(
            "//div[5]/div[3]/table/tbody/tr[2]/td[6]").click()
        driver.find_element_by_link_text("Create").click()
        time.sleep(1)

        # ---Create iteration 2
        driver.find_element_by_link_text("Iterations").click()
        driver.find_element_by_link_text("New Iteration").click()
        for i in range(60):
            try:
                if self.is_element_present(By.ID, "id_title"):
                    break
            except:
                pass
            
        else:
            self.fail("time out")
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys(
            TestDownloadfile.iter_title2)
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys(
            TestDownloadfile.iter_description2)
        driver.find_element_by_xpath(
            "//div[@id='id_start_date_popover']/div/span/i").click()
        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, "//tr[1]/td[4]"):
                    break
            except:
                pass
            
        else:
            self.fail("time out")
        driver.find_element_by_xpath(
            "//div[@class='datetimepicker-days']/table/thead/tr[1]/th[3]").click()
        driver.find_element_by_xpath("//tr[3]/td[1]").click()
        driver.find_element_by_xpath(
            "//div[@id='id_end_date_popover']/div/span").click()
        # absolute path please be careful!!!!!!!!
        driver.find_element_by_xpath(
            "/html/body/div[5]/div[3]/table/thead/tr[1]/th[3]").click()
        driver.find_element_by_xpath(
            "//div[5]/div[3]/table/tbody/tr[3]/td[6]").click()
        driver.find_element_by_link_text("Create").click()
        
        
        # ---Create iteration 3
        driver.find_elements_by_link_text("Iterations")[0].click()
        driver.find_element_by_link_text("New Iteration").click()
        for i in range(60):
            try:
                if self.is_element_present(By.ID, "id_title"):
                    break
            except:
                pass
            
        else:
            self.fail("time out")
        driver.find_element_by_id("id_title").clear()
        driver.find_element_by_id("id_title").send_keys(
            TestDownloadfile.iter_title3)
        driver.find_element_by_id("id_description").clear()
        driver.find_element_by_id("id_description").send_keys(
            TestDownloadfile.iter_description3)
        driver.find_element_by_xpath(
            "//div[@id='id_start_date_popover']/div/span/i").click()
        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, "//tr[1]/td[4]"):
                    break
            except:
                pass
           
        else:
            self.fail("time out")
        driver.find_element_by_xpath(
            "//div[@class='datetimepicker-days']/table/thead/tr[1]/th[3]").click()
        driver.find_element_by_xpath("//tr[4]/td[1]").click()
        driver.find_element_by_xpath(
            "//div[@id='id_end_date_popover']/div/span").click()
        # absolute path please be careful!!!!!!!!
        driver.find_element_by_xpath(
            "/html/body/div[5]/div[3]/table/thead/tr[1]/th[3]").click()
        driver.find_element_by_xpath(
            "//div[5]/div[3]/table/tbody/tr[4]/td[6]").click()
        driver.find_element_by_link_text("Create").click()
        

    def create_Story(self):
        driver = self.driver
        driver.find_elements_by_css_selector("i.glyphicon.glyphicon-plus")[0].click()
        self.enter_story_data(self.story1, self.tasks1)
        driver.find_element_by_link_text("Create User Story").click()
        time.sleep(2)
        driver.find_element_by_css_selector(
            "i.glyphicon.glyphicon-plus").click()
        self.enter_story_data(self.story2, self.tasks2)
        driver.find_element_by_link_text("Create User Story").click()
        time.sleep(2)
        driver.find_element_by_css_selector(
            "i.glyphicon.glyphicon-plus").click()
        self.enter_story_data(self.story3, self.tasks3)
        driver.find_element_by_link_text("Create User Story").click()
        time.sleep(2)
        driver.find_element_by_css_selector(
            "i.glyphicon.glyphicon-plus").click()
        self.enter_story_data(self.story4, self.tasks4)
        driver.find_element_by_link_text("Create User Story").click()
        time.sleep(2)
        driver.find_element_by_css_selector(
            "i.glyphicon.glyphicon-plus").click()
        self.enter_story_data(self.story5, self.tasks5)
        driver.find_element_by_link_text("Create User Story").click()
        time.sleep(2)

    def enter_story_data(self, story, tasks):
        try:
            driver = self.driver
            user = self.user
            driver.find_element_by_xpath("//input[@id='id_title']").clear()
            driver.find_element_by_xpath(
                "//input[@id='id_title']").send_keys(story.title)
            driver.find_element_by_xpath(
                "//textarea[@id='id_description']").clear()
            driver.find_element_by_xpath(
                "//textarea[@id='id_description']").send_keys(story.description)
            driver.find_element_by_id("id_reason").clear()
            driver.find_element_by_id("id_reason").send_keys(story.reason)
            driver.find_element_by_id("id_test").clear()
            driver.find_element_by_id("id_test").send_keys(story.test)

            #print(len(tasks))
            for x in range(0, len(tasks)):
                #print(tasks[x])
                driver.find_element_by_id("id_task_set-"+str(x)+"-description").clear()
                driver.find_element_by_id(
                    "id_task_set-"+str(x)+"-description").send_keys(tasks[x].description)
                driver.find_element_by_link_text("New Task").click()
                time.sleep(1)

            Select(
                driver.find_element_by_id("id_owner")).select_by_visible_text(
                user.username)
            driver.find_element_by_id("id_hours").clear()
            driver.find_element_by_id("id_hours").send_keys(story.hours)
            Select(
                driver.find_element_by_id("id_status")).select_by_visible_text(
                story.status)
            Select(
                driver.find_element_by_id("id_points")).select_by_visible_text(
                story.points)

        except Exception:
            return False
        return True

    def move_story(self):
        driver = self.driver
        driver.find_element_by_xpath(
            "//button[contains(@data-move-story, '" + self.story1.title + "')]").click()
        time.sleep(1)
        driver.find_element_by_xpath(
            "//a[contains(text(),'"+TestDownloadfile.iter_title1+"')]").click()
        time.sleep(1)

        driver.find_element_by_xpath(
            "//button[contains(@data-move-story, '" + self.story2.title + "')]").click()
        time.sleep(1)
        driver.find_element_by_xpath(
            "//a[contains(text(),'" + TestDownloadfile.iter_title1 + "')]").click()
        time.sleep(1)

        driver.find_element_by_xpath(
            "//button[contains(@data-move-story, '" + self.story3.title + "')]").click()
        time.sleep(1)
        driver.find_element_by_xpath(
            "//a[contains(text(),'" + TestDownloadfile.iter_title2 + "')]").click()
        

        driver.find_element_by_xpath(
            "//button[contains(@data-move-story, '" + self.story4.title + "')]").click()
        
        driver.find_element_by_xpath(
            "//a[contains(text(),'" + TestDownloadfile.iter_title2 + "')]").click()
        

    def download(self):
        driver = self.driver
        driver.find_element_by_xpath("//div[contains(@id, 'page-wrapper')]/span/div[2]/a").click()
        driver.find_element_by_link_text("Download").click()
        time.sleep(3)

        driver.find_element_by_xpath("//div[contains(@id, 'page-wrapper')]/span/div[2]/a").click()
        driver.find_element_by_xpath("//input[contains(@id, 'id_pie_chart')]").click()
        driver.find_element_by_xpath("//input[contains(@id, 'id_iteration_description')]").click()
        driver.find_element_by_xpath("//input[contains(@id, 'id_story_reason')]").click()
        driver.find_element_by_xpath("//input[contains(@id, 'id_story_task')]").click()
        time.sleep(2)
        driver.find_element_by_link_text("Download").click()
        time.sleep(3)

        driver.find_element_by_xpath("//div[contains(@id, 'page-wrapper')]/span/div[2]/a").click()
        driver.find_element_by_xpath("//input[contains(@id, 'id_iteration_description')]").click()
        driver.find_element_by_xpath("//input[contains(@id, 'id_iteration_duration')]").click()
        driver.find_element_by_xpath("//input[contains(@id, 'id_story_description')]").click()
        driver.find_element_by_xpath("//input[contains(@id, 'id_story_reason')]").click()
        driver.find_element_by_xpath("//input[contains(@id, 'id_story_test')]").click()
        driver.find_element_by_xpath("//input[contains(@id, 'id_story_task')]").click()
        driver.find_element_by_xpath("//input[contains(@id, 'id_story_owner')]").click()
        driver.find_element_by_xpath("//input[contains(@id, 'id_story_hours')]").click()
        driver.find_element_by_xpath("//input[contains(@id, 'id_story_status')]").click()
        driver.find_element_by_xpath("//input[contains(@id, 'id_story_points')]").click()
        driver.find_element_by_xpath("//input[contains(@id, 'id_pie_chart')]").click()
        time.sleep(2)
        driver.find_element_by_link_text("Download").click()
        time.sleep(3)

    def destroy(self):
        driver = self.driver
        driver.find_element_by_link_text("Dashboard").click()
        driver.find_element_by_xpath(
            "//a[contains(@data-del-proj, '" + TestDownloadfile.proj_title + "')]").click()
        driver.find_element_by_link_text("Delete Project").click()
        time.sleep(2)


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
