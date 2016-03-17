from django.db import models
from django.contrib.auth.models import User
from base import ProjMgmtBase
from project import Project



class Backlog(ProjMgmtBase):
    
    storyTitle = models.CharField(default='',max_length=30)
    project = models.ForeignKey(Project)
    backlogContent = models.CharField(default='', max_length=512)
    
    def __str__(self):
        return self.title
    
    class Meta:
        app_label = 'requirements'
