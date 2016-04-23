from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from requirements import models
from requirements.models import project
from requirements.models import project_api
from requirements.models import user_association
from requirements.models import user_manager
from requirements.models import story
from requirements.models import story_attachment
from requirements.models import task
from requirements.models.project import Project
from requirements.models.user_association import UserAssociation
from requirements.models.iteration import Iteration
from requirements.models.story import Story

import datetime
from cgi import FieldStorage
from django.db import transaction


class Obj():
    pass


class ProjectTestCase(TestCase):

    def setUp(self):
        self.__clear()

        self.__project = Project(title="title", description="desc")
        self.__project.save()
        self.__user = User(username="testUser", password="pass")
        self.__user.save()

    def tearDown(self):
        self.__clear()

    def __clear(self):
        UserAssociation.objects.all().delete
        Project.objects.all().delete
        User.objects.all().delete  
        
    def test_create_new_task(self):
        fields = {"title": "title",
                  "description": "desc",
                  "reason": "reason",
                  "test": "test",
                  "status": 1}
        s = models.story.create_story(self.__project, fields)
        self.assertEqual(1, self.__project.story_set.count())
        task = {'description': 'Test Task'}
        t = models.task.create_task(s, task)
        self.assertEqual('Test Task', t.__str__())


    def test_get_task_from_story(self):
        fields = {"title": "title",
                  "description": "desc",
                  "reason": "reason",
                  "test": "test",
                  "status": 1}
        s = models.story.create_story(self.__project, fields)
        self.assertEqual(1, self.__project.story_set.count())
        task = {'description': 'Test Task'}
        t = models.task.create_task(s, task)
        self.assertEqual('Test Task', t.__str__())
        self.assertIsNotNone(models.task.get_tasks_for_story(s))
    
    def test_get_task_from_null_story(self):
        task = models.task.get_tasks_for_story(None)
        self.assertIsNone(task)
    
    def test_create_null_task_from_story(self):
        fields = {"title": "title",
                  "description": "desc",
                  "reason": "reason",
                  "test": "test",
                  "status": 1}
        s = models.story.create_story(self.__project, fields)
        self.assertEqual(1, self.__project.story_set.count()) 
        t = models.task.create_task(s, None)
        self.assertIsNone(t)
        
    def test_create_task_from_null_story(self):
        task = {'description': 'Test Task'}
        t = models.task.create_task(None, task)
        self.assertIsNone(t)
        
    
    def test_get_task_from_id(self):
        fields = {"title": "title",
                  "description": "desc",
                  "reason": "reason",
                  "test": "test",
                  "status": 1}
        s = models.story.create_story(self.__project, fields)
        self.assertEqual(1, self.__project.story_set.count())
        task = {'description': 'Test Task'}
        t = models.task.create_task(s, task)
        self.assertEqual('Test Task', t.__str__())
        self.assertIsNotNone(models.task.get_task(t.id))
    
    def test_get_task_from_invalid_id(self):
        self.assertIsNone(models.task.get_task(-1000000))
    
    def test_get_all_tasks(self):
        fields = {"title": "title",
                  "description": "desc",
                  "reason": "reason",
                  "test": "test",
                  "status": 1}
        s = models.story.create_story(self.__project, fields)
        self.assertEqual(1, self.__project.story_set.count())
        task = {'description': 'Test Task'}
        t = models.task.create_task(s, task)
        self.assertEqual('Test Task', t.__str__())
        self.assertEqual(1, models.task.get_all_tasks().count())
        

            