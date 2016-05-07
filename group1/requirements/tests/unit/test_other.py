from django.test import TestCase
from django.contrib.auth.models import User
from requirements import models
from requirements.models import project
from requirements.models import project_api
from requirements.models import user_association
from requirements.models import user_manager
from requirements.models import story
from requirements.models.project import Project
from requirements.models.user_association import UserAssociation
from requirements.models.iteration import Iteration
from requirements.models.story import Story
import datetime


class Obj():
    pass


class ProjectTestCase(TestCase):

    def setUp(self):
        self.__clear()

        self.__user = User(username="testUser", password="pass")
        self.__user.save()

    def tearDown(self):
        self.__clear()

    def __clear(self):
        UserAssociation.objects.all().delete
        Project.objects.all().delete
        User.objects.all().delete

    def test_user_owns_project_true(self):
        owner = User(
            username="user",
            password="password",
            email="email@address.com")
        owner.save()

        project = models.project_api.create_project(
            owner, {
                'title': 'title', 'description': 'description'})
        self.assertEquals(
            models.project_api.user_owns_project(
                owner,
                project),
            True)

    def test_user_owns_project_false(self):
        owner = User(
            username="user",
            password="password",
            email="email@address.com")
        owner.save()

        user = User(
            username="user2",
            password="password",
            email="email@address.com")
        user.save()

        project = models.project_api.create_project(
            owner, {
                'title': 'title', 'description': 'description'})
        self.assertEquals(
            models.project_api.user_owns_project(
                user,
                project),
            False)
