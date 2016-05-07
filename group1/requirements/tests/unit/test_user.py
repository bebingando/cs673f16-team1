
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
from cgi import FieldStorage
from django.db import transaction


class Obj():
    pass


class UserTestCase(TestCase):

    def setUp(self):
        self.__clear()

        self.__project = Project(title="title", description="desc")
        self.__project.save()
        self.__user1 = User(username="testClient", password="pass")
        self.__user1.save()
	self.__user2 = User(username="testOwner", password="pass")
        self.__user2.save()
	self.__user3 = User(username="testDeveloper", password="pass")
        self.__user3.save()
	self.__user = User(username="testNoassociation", password="pass")
        self.__user.save()

    def tearDown(self):
        self.__clear()

    def __clear(self):
        UserAssociation.objects.all().delete
        Project.objects.all().delete
        User.objects.all().delete
    
    def __addUserAsOwner(self):
        uao = UserAssociation(
            project=self.__project,
            user = self.__user2,
            role=user_association.ROLE_OWNER)
        uao.save()
        
    def __addUserAsClient(self):
        ua = UserAssociation(
            project=self.__project,
            user=self.__user1,
            role=user_association.ROLE_CLIENT)
        ua.save()

    def __addUserAsDev(self):
        ua = UserAssociation(
            project=self.__project,
            user=self.__user3,
            role=user_association.ROLE_DEVELOPER)
        ua.save()
 

    def test_user_owns_project_true(self):
       # owner = User(
        #    username="user",
        #    password="password",
        #    email="email@address.com")
       # owner.save()

        project = models.project_api.create_project(
            self.__user2, {
                'title': 'title', 'description': 'description'})
        self.assertEquals(
            models.project_api.user_owns_project(
                self.__user2,
                project),
            True)
    def test_user_owns_project_false(self):

        project = models.project_api.create_project(
            self.__user2, {
                'title': 'title', 'description': 'description'})
        self.assertEquals(
            models.project_api.user_owns_project(
                self.__user1,
                project),
            False)

    def testAddStoryAsOwner(self):
        self.__addUserAsOwner()
        self.assertEquals(
            user_manager.canCreateStoryInProject(
                userID= self.__user2.id,
                projectID=self.__project.id),
            True)

    def testEditStoryNoAssoc(self):
        self.assertEquals(
            user_manager.canEditStoryInProject(
                userID=self.__user1.id,
                projectID=self.__project.id),
            False)

    def testEditStoryAsClient(self):
         self.__addUserAsClient()
	 self.assertEquals(
            user_manager.canEditStoryInProject(
                userID=self.__user1.id,
                projectID=self.__project.id),
            True)

    def testIsOwner_IsOwner(self):
	self.__addUserAsOwner()
        self.assertEquals(
            user_manager.isOwner(
                userID=  self.__user2.id,
                projectID=self.__project.id),
            True)

    def testIsDeveloper_IsOwner(self):
        self.__addUserAsDev()
        self.assertEquals(
            user_manager.isOwner(
                userID=self.__user3.id,
                projectID=self.__project.id),
            False)


