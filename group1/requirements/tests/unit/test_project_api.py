import datetime
import os
import shutil
import subprocess

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from django.http import HttpRequest
from django.test import Client
from django.test import RequestFactory
from django.test import TestCase

from requirements import models
from requirements.models import project
from requirements.models import project_api
from requirements.models import story
from requirements.models import user_association
from requirements.models import user_manager
from requirements.models.files import ProjectFile
from requirements.models.iteration import Iteration
from requirements.models.project import Project
from requirements.models.story import Story
from requirements.models.user_association import UserAssociation
from requirements.views.projects import upload_attachment
from django.core.files.base import File
from django.test import Client


class Obj():
    pass


class ProjectTestCase(TestCase):

    def setUp(self):
        self.__clear()

        self.__user = User(username="testUser", password="pass")
        self.__user.save()
        
         # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.__admin = User.objects.create_superuser(
            username='admin', email='admin@bu.edu', password='pass')
        self.__admin.save()


        

    def tearDown(self):
        self.__clear()
        # Clean up file created during open() and file created during upload
        git_root = subprocess.check_output("git rev-parse --show-toplevel", shell=True)
        if (os.path.exists(git_root.rstrip() + '/group1/project_files')):
            shutil.rmtree(git_root.rstrip() + '/group1/project_files')

    def __clear(self):
        UserAssociation.objects.all().delete
        Project.objects.all().delete
        User.objects.all().delete

    def test_get_all_projects_none(self):
        self.assertEqual(models.project_api.get_all_projects().count(), 0)

    def test_get_all_projects_one(self):
        p = Project(title="title", description="desc")
        p.save()
        self.assertEqual(models.project_api.get_all_projects().count(), 1)

    def test_get_all_projects_two(self):
        p = Project(title="title", description="desc")
        p.save()

        p2 = Project(title="title2", description="desc2")
        p2.save()

        self.assertEqual(models.project_api.get_all_projects().count(), 2)

    def test_get_projects_for_user_none(self):
        p = Project(title="title", description="desc")
        p.save()
        self.assertEqual(
            models.project_api.get_projects_for_user(
                self.__user.id).count(),
            0)

    def test_get_projects_for_user_one(self):
        p = Project(title="title", description="desc")
        p.save()

        u = UserAssociation(user=self.__user, project=p)
        u.save()

        self.assertEqual(
            models.project_api.get_projects_for_user(
                self.__user.id).count(),
            1)

    def test_get_project_pass(self):
        p = Project(title="title", description="desc")
        p.save()
        self.assertEqual(p, models.project_api.get_project(p.id))

    def test_get_project_fail(self):
        self.assertEqual(None, models.project_api.get_project(0))

    def test_get_project_users_none(self):
        p = Project(title="title", description="desc")
        p.save()
        self.assertEqual(models.project_api.get_project_users(p.id).count(), 0)

    def test_get_project_users_one(self):
        p = Project(title="title", description="desc")
        p.save()
        models.project_api.add_user_to_project(
            p.id,
            self.__user.username,
            models.user_association.ROLE_DEVELOPER)
        self.assertEqual(models.project_api.get_all_projects().count(), 1)

    def test_can_user_access_project_cant(self):
        p = Project(title="title", description="desc")
        p.save()
        self.assertEqual(
            models.project_api.can_user_access_project(
                self.__user.id,
                p.id),
            False)

    def test_can_user_access_project_can(self):
        p = Project(title="title", description="desc")
        p.save()
        u = UserAssociation(user=self.__user, project=p)
        u.save()
        self.assertEqual(
            models.project_api.can_user_access_project(
                self.__user.id,
                p.id),
            True)

    def test_create_project_pass(self):
        fields = {"title": "title",
                  "description": "desc"}
        p = models.project_api.create_project(self.__user, fields)
        self.assertEqual(1, Project.objects.filter(id=p.id).count())

    def test_create_project_fail_bad_fields(self):
        p = models.project_api.create_project(self.__user, None)
        self.assertEqual(0, Project.objects.count())

    def test_create_project_fail_bad_user(self):
        fields = {"title": "title",
                  "description": "desc"}

        # pass a null user
        p = models.project_api.create_project(None, fields)

        user = User(username="unknownuser", password="pass")

        p = models.project_api.create_project(user, fields)
        self.assertEqual(0, Project.objects.count())

    def test_add_user_to_project_pass(self):
        p = Project(title="title", description="desc")
        p.save()
        models.project_api.add_user_to_project(
            p.id,
            self.__user.username,
            models.user_association.ROLE_DEVELOPER)
        self.assertEqual(UserAssociation.objects.filter(project_id=p.id,
                                                        user_id=self.__user.id).count(), 1)

    def test_add_user_to_project_fail_bad_project(self):
        projID = 0
        models.project_api.add_user_to_project(
            projID,
            self.__user.username,
            models.user_association.ROLE_DEVELOPER)
        self.assertEqual(UserAssociation.objects.filter(project_id=projID,
                                                        user_id=self.__user.id).count(), 0)

    def test_add_user_to_project_fail_bad_user(self):
        p = Project(title="title", description="desc")
        p.save()

        # pass a null user
        models.project_api.add_user_to_project(
            p.id,
            None,
            models.user_association.ROLE_DEVELOPER)
        self.assertEqual(UserAssociation.objects.filter(project_id=p.id,
                                                        user_id=self.__user.id).count(), 0)

        # pass an unknown user
        user = User(username="unknownuser", password="pass")
        models.project_api.add_user_to_project(
            p.id,
            user,
            models.user_association.ROLE_DEVELOPER)
        self.assertEqual(UserAssociation.objects.filter(project_id=p.id,
                                                        user_id=self.__user.id).count(), 0)

    def test_remove_user_from_project_pass(self):
        p = Project(title="title", description="desc")
        p.save()
        models.project_api.add_user_to_project(
            p.id,
            self.__user.username,
            models.user_association.ROLE_DEVELOPER)
        self.assertEqual(UserAssociation.objects.filter(project_id=p.id,
                                                        user_id=self.__user.id).count(), 1)
        models.project_api.remove_user_from_project(p.id, self.__user.username)
        self.assertEqual(UserAssociation.objects.filter(project_id=p.id,
                                                        user_id=self.__user.id).count(), 0)

    def test_remove_user_from_project_fail_bad_project(self):
        p = Project(title="title", description="desc")
        p.save()
        models.project_api.add_user_to_project(
            p.id,
            self.__user.username,
            models.user_association.ROLE_DEVELOPER)
        self.assertEqual(UserAssociation.objects.filter(project_id=p.id,
                                                        user_id=self.__user.id).count(), 1)

        projID = p.id - 1
        models.project_api.remove_user_from_project(
            projID,
            self.__user.username)
        self.assertEqual(UserAssociation.objects.filter(project_id=p.id,
                                                        user_id=self.__user.id).count(), 1)

    def test_remove_user_from_project_fail_bad_user(self):
        p = Project(title="title", description="desc")
        p.save()
        models.project_api.add_user_to_project(
            p.id,
            self.__user.username,
            models.user_association.ROLE_DEVELOPER)
        self.assertEqual(UserAssociation.objects.filter(project_id=p.id,
                                                        user_id=self.__user.id).count(), 1)

        # pass a null user
        models.project_api.remove_user_from_project(p.id, None)
        self.assertEqual(UserAssociation.objects.filter(project_id=p.id,
                                                        user_id=self.__user.id).count(), 1)
        # test an unknown user
        user = User(username="unknownuser", password="pass")
        models.project_api.remove_user_from_project(p.id, user.username)
        self.assertEqual(UserAssociation.objects.filter(project_id=p.id,
                                                        user_id=self.__user.id).count(), 1)

    def test_delete_project_pass(self):
        p = Project(title="title", description="desc")
        p.save()
        self.assertEqual(1, Project.objects.filter(id=p.id).count())
        models.project_api.delete_project(p)
        self.assertEqual(0, Project.objects.filter(id=p.id).count())

    def test_delete_project_fail(self):
        p = Project(title="title", description="desc")
        p.save()
        self.assertEqual(1, Project.objects.filter(id=p.id).count())
        projID = p.id - 1
        models.project_api.delete_project(None)
        self.assertEqual(1, Project.objects.filter(id=p.id).count())

    def test_add_iteration_to_project_pass(self):
        p = Project(title="title", description="desc")
        p.save()
        title = "title"
        description = "description"

        start_date = datetime.date.today()
        end_date = datetime.date.max
        iteration = models.project_api.add_iteration_to_project(title,
                                                                description,
                                                                start_date,
                                                                end_date, p.id)

        self.assertEqual(start_date, iteration.start_date)
        self.assertEqual(end_date, iteration.end_date)
        self.assertEqual(title, iteration.title)
        self.assertEqual(description, iteration.description)
        self.assertEqual(1, p.iteration_set.count())

    def test_add_iteration_to_project_fail_bad_project(self):
        p = Project(title="title", description="desc")
        p.save()

        # pass a null prject
        title = "title"
        description = "description"
        start_date = datetime.date.today()
        end_date = datetime.date.max
        iteration = models.project_api.add_iteration_to_project(title,
                                                                description,
                                                                start_date,
                                                                end_date,
                                                                None)
        self.assertEqual(0, p.iteration_set.count())

        # pass an unknown project
        projID = p.id - 1
        iteration = models.project_api.add_iteration_to_project(title,
                                                                description,
                                                                start_date,
                                                                end_date,
                                                                projID)
        self.assertEqual(0, p.iteration_set.count())

    def test_get_iterations_for_project_none(self):
        p = Project(title="title", description="desc")
        p.save()
        iterations = models.project_api.get_iterations_for_project(p)
        self.assertEqual(0, iterations.count())

    def test_get_iterations_for_project_one(self):
        p = Project(title="title", description="desc")
        p.save()
        title = "title"
        description = "description"
        start_date = datetime.date.today()
        end_date = datetime.date.max
        iteration = models.project_api.add_iteration_to_project(title,
                                                                description,
                                                                start_date,
                                                                end_date,
                                                                p.id)

        self.assertEqual(start_date, iteration.start_date)
        self.assertEqual(end_date, iteration.end_date)
        self.assertEqual(title, iteration.title)
        self.assertEqual(description, iteration.description)
        iterations = models.project_api.get_iterations_for_project(p)
        self.assertEqual(1, iterations.count())
        
    def test_attachments_no_file_attached(self):
        p = Project(title="title", description="desc")
        p.save()
        self.assertEqual(models.project_api.get_all_projects().count(), 1)
        f = ProjectFile(
            project=p)
        try:
            f.save()
            self.fail("A missing File exception should be thrown")
        except IOError as e:
            if e.args[0] == 'Missing file':
                pass
            else:
                fail("Unknown exception was thrown")
        
        file_count = ProjectFile.does_attachment_exist(f)
        self.assertFalse(file_count, "File attachment exists and should not")
        
    def test_attachments_file_attached(self):
        p = Project(title="title", description="desc")
        p.save()
        self.assertEqual(models.project_api.get_all_projects().count(), 1)
        f = ProjectFile(
            project=p,
            file=SimpleUploadedFile('test.txt', 'This is some text to add to the file'),
            name=file.name)
        f.save()
        file_count = ProjectFile.does_attachment_exist(f)
        self.assertTrue(file_count, "File attachment should exist")
        
    def test_attachments_view_upload_attachment(self):
        p = Project(title="title", description="desc")
        p.save()
        models.project_api.add_user_to_project(
            p.id,
            self.__admin.username,
            models.user_association.ROLE_DEVELOPER)
         # Create an instance of a GET request.
        request = self.factory.get('/uploadprojectattachment/'+str(p.id))
        request.user = self.__admin

        try:
            response = upload_attachment(request, p.id)
            pass
        except:
            # reraise the exception, as it's an unexpected error
            self.fail("There should not be an exception thrown at the view level")    
    
    #test_attachments_file_too_large
    #created by Chris Willis (willisc@bu.edu)
    #tests attachment function response when a file over the 10 MB limit is uploaded
    def test_attachments_file_too_large(self):
        
        # Create a 20 MB file (larger than the allowed attachment size)
        upload_file = open('test.txt',"w+")
        upload_file.seek(20971520-1)
        upload_file.write("\0")
        upload_file.close()
        
        p = Project(title="title", description="desc")
        p.save()
        models.project_api.add_user_to_project(
           p.id,
            self.__admin.username,
            models.user_association.ROLE_DEVELOPER)
        
        request = self.factory.post('/uploadprojectattachment/'+str(p.id))
        request.user = self.__admin
        request.FILES['file'] = File(upload_file)
        
        try:
            response = upload_attachment(request, p.id)
            pass
        except:
            # reraise the exception, as it's an unexpected error
            self.fail("There should not be an exception thrown at the view level")
        finally:    
            # Clean up file created during open() and file created during upload
            os.remove('./test.txt')
        
        