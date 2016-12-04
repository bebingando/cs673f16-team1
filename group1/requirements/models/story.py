from django.db import models
from django.contrib.auth.models import User
from base import ProjMgmtBase
from project import Project
from iteration import Iteration


class Story(ProjMgmtBase):
    TYPE_FEATURE = 1
    TYPE_BUG = 2
    TYPE_CHORE = 3
    TYPE_RELEASE = 4

    TYPE_CHOICES = (
        (TYPE_FEATURE, "Feature"),
        (TYPE_BUG, "Bug Fix"),
        (TYPE_CHORE, "Chore"),
        (TYPE_RELEASE, "Release")
    )
    
    STATUS_UNSTARTED = 1
    STATUS_STARTED = 2
    STATUS_COMPLETED = 3
    STATUS_ACCEPTED = 4

    STATUS_CHOICES = (
        (STATUS_UNSTARTED, "Unstarted"),
        (STATUS_STARTED, "Started"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_ACCEPTED, "Accepted")
    )

    POINTS_NONE = 0
    POINTS_ONE = 1
    POINTS_TWO = 2
    POINTS_THREE = 3
    POINTS_FOUR = 4
    POINTS_FIVE = 5

    POINTS_CHOICES = (
        (POINTS_NONE, "0 Not Scaled"),
        (POINTS_ONE, "1 Point"),
        (POINTS_TWO, "2 Points"),
        (POINTS_THREE, "3 Points"),
        (POINTS_FOUR, "4 Points"),
        (POINTS_FIVE, "5 Points"),
    )
    
    PRIORITY_GREEN = "Low"
    PRIORITY_ORANGE = "Medium"
    PRIORITY_RED = "High"
    
    PRIORITY_CHOICES = (
        (PRIORITY_RED,"High"),
        (PRIORITY_ORANGE,"Medium"),
        (PRIORITY_GREEN, "Low"),
    )
    
    STORY_BELONGS_ICEBOX = 'ICEBOX'

    STORY_BELONGS_ITERATION = "ITERATION"
    
    STORY_BELONGS_BACKLOG = "BACKLOG"
    
    project = models.ForeignKey(Project)
    
    # 'ICEBOX', 'ITERATION', 'BACKLOG'
    belong = models.CharField(default="ICEBOX", max_length=128, blank=True)
    iteration = models.ForeignKey(
        Iteration,
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    reason = models.CharField(default='', max_length=1024, blank=True)
    test = models.CharField(default='', max_length=1024, blank=True)
    hours = models.IntegerField(default=0)
    owner = models.ForeignKey(
        User,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL)
    
    priority = models.CharField(
            choices =PRIORITY_CHOICES,
            max_length = 32,
            default = PRIORITY_GREEN)
    type = models.IntegerField(
        choices=TYPE_CHOICES,
        default=TYPE_FEATURE)
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=STATUS_UNSTARTED)
    points = models.IntegerField(
        choices=POINTS_CHOICES,
        default=POINTS_NONE)
    pause = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def description_as_list(self):
        return self.description.split('\n')

    def reason_as_list(self):
        return self.reason.split('\n')

    def test_as_list(self):
        return self.test.split('\n')

    class Meta:
        app_label = 'requirements'


def get_stories_for_project(project):
    if project is None:
        return None
    return Story.objects.filter(project_id=project.id)


def get_story(storyID):
    try:
        return Story.objects.get(id=storyID)
    except Exception as e:
        return None


def create_story(project, fields):
    if project is None:
        return None
    if fields is None:
        return None

    title = fields.get('title', '')
    description = fields.get('description', '')
    reason = fields.get('reason', '')
    test = fields.get('test', '')
    hours = fields.get('hours', 0)
    owner = fields.get('owner', None)
    type = fields.get('type', Story.TYPE_FEATURE)
    status = fields.get('status', Story.STATUS_UNSTARTED)
    points = fields.get('points', Story.POINTS_NONE)
    pause = fields.get('pause', False)
    priority = fields.get('priority', "Low")
    if owner is None or owner == '':
        owner = None
    else:
        try:
            owner = User.objects.get(id=owner)
        except Exception as e:
            owner = None

    story = Story(project=project,
                  title=title,
                  description=description,
                  reason=reason,
                  test=test,
                  hours=hours,
                  owner=owner,
                  type=type,
                  status=status,
                  points=points,
                  pause=pause,
                  belong = 'ICEBOX',
                  priority = priority
                  )
    story.save()
    return story


def delete_story(storyID):
    story = Story.objects.filter(id=storyID)
    story.delete()

