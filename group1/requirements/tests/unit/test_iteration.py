from django.test import TestCase
from django.contrib.auth.models import User
from requirements import models
from requirements.models.project import Project
from requirements.models.user_association import UserAssociation
import datetime

class IterationDateTestCase(TestCase):

    def setUp(self):
        self.__clear()
        self.__user = User(username="admin", password="pass")
        self.__user.save()

    def tearDown(self):
        self.__clear()

    def __clear(self):
        UserAssociation.objects.all().delete
        Project.objects.all().delete
        User.objects.all().delete

    def test_valid_date_for_iteration_start(self):
        p = Project(title="title", description="desc")
        p.save()
        title = "title"
        description = "description"
        start_date = datetime.date.today() - datetime.timedelta(days=1)
        earliest_possible_start_date = datetime.date.today()
        end_date = datetime.date.max
        iteration = models.project_api.add_iteration_to_project(
            title,
            description,
            start_date,
            end_date,
            p.id)
        
        #Asserting whether iteration was created successfully with an invalid start date of yesterday
        #Expected action will be that a date of today will automatically be inserted
        self.assertEqual(iteration.start_date, earliest_possible_start_date)
