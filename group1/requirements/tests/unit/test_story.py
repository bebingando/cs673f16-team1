from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from requirements import models
from requirements.models import project
from requirements.models import project_api
from requirements.models import user_association
from requirements.models import user_manager
from requirements.models import story
from requirements.models import story_comment
from requirements.models import story_attachment
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

    def test_get_project_stories(self):
        p = Project(title="title", description="desc")
        p.save()
        iterations = models.project_api.get_iterations_for_project(p)
        stories = models.story.get_stories_for_project(p)
        self.assertEqual(False, stories.exists())

    def test_get_project_stories_one(self):
        p = Project(title="title", description="desc")
        p.save()
        models.story.create_story(p, {"title": "title",
                                      "description": "desc",
                                      "reason": "reason",
                                      "test": "test",
                                      "status": 1})

        iterations = models.project_api.get_iterations_for_project(p)
        stories = models.story.get_stories_for_project(p)
        self.assertEqual(True, stories.exists())

    def test_create_story_pass(self):
        fields = {"title": "title",
                  "description": "desc",
                  "reason": "reason",
                  "test": "test",
                  "status": 1}
        s = models.story.create_story(self.__project, fields)
        self.assertEqual(1, self.__project.story_set.count())

    def test_create_story_fail(self):
        fields = {"title": "title",
                  "description": "desc",
                  "reason": "reason",
                  "test": "test",
                  "status": 1}

        # pass a null project
        s = models.story.create_story(None, fields)
        self.assertEqual(0, self.__project.story_set.count())

        # create a project, but don't save it
        p = Project(title="title", description="description")
        try:
            with transaction.atomic():
                s = models.story.create_story(p, fields)
        except Exception:
            pass
        self.assertEqual(0, self.__project.story_set.count())

    def test_delete_story_pass(self):
        fields = {"title": "title",
                  "description": "desc",
                  "reason": "reason",
                  "test": "test",
                  "status": 1}
        s = models.story.create_story(self.__project, fields)
        self.assertEqual(1, self.__project.story_set.count())
        models.story.delete_story(s.id)
        self.assertEqual(0, self.__project.story_set.count())

    def test_delete_story_fail(self):
        fields = {"title": "title",
                  "description": "desc",
                  "reason": "reason",
                  "test": "test",
                  "status": 1}
        s = models.story.create_story(self.__project, fields)
        self.assertEqual(1, self.__project.story_set.count())
        models.story.delete_story(s.id - 1)
        self.assertEqual(1, self.__project.story_set.count())
        
    def test_create_new_comment(self):
        fields = {"title": "title",
                  "description": "desc",
                  "reason": "reason",
                  "test": "test",
                  "status": 1}
        s = models.story.create_story(self.__project, fields)
        self.assertEqual(1, self.__project.story_set.count())
        comment = {'title': 'Test comment title', 'comment': 'Test comment body'} 
        c = models.story_comment.create_comment(s, comment)
        self.assertEqual('Test comment title', c.__str__())


    def test_get_comment_from_story(self):
        fields = {"title": "title",
                  "description": "desc",
                  "reason": "reason",
                  "test": "test",
                  "status": 1}
        s = models.story.create_story(self.__project, fields)
        self.assertEqual(1, self.__project.story_set.count())
        comment = {'title': 'Test comment title', 'comment': 'Test comment body'} 
        c = models.story_comment.create_comment(s, comment)
        self.assertEqual('Test comment title', c.__str__())
        self.assertIsNotNone(models.story_comment.get_comments_for_story(s))
    
    def test_get_comment_from_null_story(self):
        comment = models.story_comment.get_comments_for_story(None)
        self.assertIsNone(comment)
    
    def test_create_null_comment_from_story(self):
        fields = {"title": "title",
                  "description": "desc",
                  "reason": "reason",
                  "test": "test",
                  "status": 1}
        s = models.story.create_story(self.__project, fields)
        self.assertEqual(1, self.__project.story_set.count()) 
        c = models.story_comment.create_comment(s, None)
        self.assertIsNone(c)
        
    def test_create_comment_from_null_story(self):
        comment = {'title': 'Test comment title', 'comment': 'Test comment body'} 
        c = models.story_comment.create_comment(None, comment)
        self.assertIsNone(c)
        
    
    def test_get_comment_from_id(self):
        fields = {"title": "title",
                  "description": "desc",
                  "reason": "reason",
                  "test": "test",
                  "status": 1}
        s = models.story.create_story(self.__project, fields)
        self.assertEqual(1, self.__project.story_set.count())
        comment = {'title': 'Test comment title', 'comment': 'Test comment body'} 
        c = models.story_comment.create_comment(s, comment)
        self.assertEqual('Test comment title', c.__str__())
        self.assertIsNotNone(models.story_comment.get_comment(c.id))
    
    def test_get_comment_from_invalid_id(self):
        self.assertIsNone(models.story_comment.get_comment(-1000000))
    
    def test_get_all_comments(self):
        fields = {"title": "title",
                  "description": "desc",
                  "reason": "reason",
                  "test": "test",
                  "status": 1}
        s = models.story.create_story(self.__project, fields)
        self.assertEqual(1, self.__project.story_set.count())
        comment = {'title': 'Test comment title', 'comment': 'Test comment body'} 
        c = models.story_comment.create_comment(s, comment)
        self.assertEqual('Test comment title', c.__str__())
        self.assertEqual(1, models.story_comment.get_all_comments().count())
        
    def test_attachments_file_attachment(self):
        fields = {"title": "title",
                  "description": "desc",
                  "reason": "reason",
                  "test": "test",
                  "status": 1}
        s = models.story.create_story(self.__project, fields)
        self.assertEqual(1, self.__project.story_set.count())
        models.story_attachment.create(s.id, SimpleUploadedFile('test_it.txt', 'This is some text to add to the file'))
        attach = story_attachment.get_attachments_for_story(s)
        self.assertIsNotNone(attach, "File attachment should exist")
        for a in story_attachment.get_all_attachments():
            story_attachment.delete(a.uuid)
        
        
    def test_attachments_file_no_attachment(self):
        fields = {"title": "title",
                  "description": "desc",
                  "reason": "reason",
                  "test": "test",
                  "status": 1}
        s = models.story.create_story(self.__project, fields)
        self.assertEqual(1, self.__project.story_set.count())
        attach = models.story_attachment.create(s.id, None)
        self.assertIsNone(attach, "File attachment should NOT exist")
            
    def test_attachments_file_no_story(self):
        attach = models.story_attachment.create(None, SimpleUploadedFile('test_it.txt', 'This is some text to add to the file'))
        
        self.assertIsNone(attach, "File attachment should NOT exist")
    
    def test_attachments_get_attachments_for_non_story(self):
       attach = story_attachment.get_attachments_for_story(None)
       self.assertIsNone(attach, "File attachment should NOT exist")
    
    def test_attachments_get_all_attachments(self):
       attach = story_attachment.get_all_attachments()
       self.assertEqual(0, attach.count())
    
    def test_attachments_file_attachment(self):
        fields = {"title": "title",
                  "description": "desc",
                  "reason": "reason",
                  "test": "test",
                  "status": 1}
        s = models.story.create_story(self.__project, fields)
        self.assertEqual(1, self.__project.story_set.count())
        models.story_attachment.create(s.id, SimpleUploadedFile('test_it.txt', 'This is some text to add to the file'))
        attach = story_attachment.get_attachments_for_story(s)
        self.assertIsNotNone(attach, "File attachment should exist")
        a = attach.first()
        self.assertIsNotNone(a.uuid, "File attachment uuid should exist")
        self.assertIsNotNone(a.story, "File attachment story should exist")
        self.assertIsNotNone(a.name, "File attachment name should exist")
        self.assertIsNotNone(a.file, "File attachment file should exist")
        self.assertIsNotNone(a.last_updated, "File attachment last_updated should exist")
        
        for a in story_attachment.get_all_attachments():
            story_attachment.delete(a.uuid)  
            