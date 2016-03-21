from django.test import TestCase
from django.contrib.auth.models import User
from requirements import models
from requirements.models.project import Project
from requirements.models import iteration as mdl_iteration
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
        start_date = datetime.datetime.today() - datetime.timedelta(days=1)
        str_start_date = datetime.datetime.strftime(start_date,"%m/%d/%Y")
        earliest_possible_start_date = datetime.date.today()
        end_date = datetime.date.max
        str_end_date = datetime.datetime.strftime(end_date,"%m/%d/%Y")
        fields = {'title': title, 'description': description, 'start_date': str_start_date, 'end_date': str_end_date}
        iteration = mdl_iteration.create_iteration(p, fields)
        #iteration = models.project_api.add_iteration_to_project(
        #    title,
        #    description,
        #    start_date,
        #    end_date,
        #    p.id)
        
        #Asserting whether iteration was created successfully with an invalid start date of yesterday
        #Expected action will be that a date of today will automatically be inserted
        self.assertEqual(iteration.start_date, earliest_possible_start_date)

    def test_valid_date_for_iteration_end(self):
    	p = Project(title="title", description="desc")
        p.save()
        title = "title"
        description = "description"
        start_date = datetime.date.today() + datetime.timedelta(days=1)
        end_date = datetime.date.today()
        earliest_possible_end_date = start_date
        iteration = models.project_api.add_iteration_to_project(
            title,
            description,
            start_date,
            end_date,
            p.id)
	#Asserting whether iteration was created successfully with an invalid end date earlier than start date
        #Expected action will be that the function automatically returns an end date that is the same as the start date
        self.assertEqual(iteration.end_date, earliest_possible_end_date)
