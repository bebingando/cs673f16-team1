from requirements.models import project_api
from django.contrib.auth.decorators import login_required
from django import forms
from requirements import models
from requirements.views import projects
from requirements.models import backlog
from requirements.models import user_manager
from requirements.models import story as mdl_story
from requirements.models import iteration as mdl_iteration
from requirements.models.user_manager import user_owns_project
from requirements.models.user_association import UserAssociation
from forms import IterationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
import datetime
from requirements.models.user_manager import user_can_access_project

@login_required(login_url='/signin')
def create_backlog(request):
    if not project_api.can_user_access_project(request.user.id, projectID):
        return redirect('/req/projects')
    
    backlog_content = request.backlog_content
    project_id = request.project_id
    backlog_title = request.backlog_title
    
    p = project_api.get_project(project_id)
    
    blog = backlog.Backlog(storyTitle=backlog_title, project=p, backlogContent=backlog_content)
    blog.save()
    
    #rest is UI interaction
    


@login_required(login_url='/signin')
def show_backlog(request, projectID):
    #Show backlog according to the project id
    if not project_api.can_user_access_project(request.user.id, projectID):
        return redirect('/req/projects')
    
    proj = project_api.get_project(projectID)
    logs = proj.backlog_set.all()
    l = len(logs)
    context = {
    #    'canOwnProject': request.user.has_perm(PERMISSION_OWN_PROJECT),
        'backlog': l,
        'theUser': request.user
               
    }
    return render(request, 'ProjectBacklog.html',context)


@login_required(login_url='/signin')
def edit_backlog(request, projectID, backlogID):
    if not project_api.can_user_access_project(request.user.id, projectID):
        return redirect('/req/projects')
    b = None
    try:
        b = backlog.Backlog.objects.get(id=backlogID)
    except Exception as e:
        return None
    
    ##put context here if UI complete

@login_required(login_url='/signin')
def update_backlog(request, backlogID):
    if not project_api.can_user_access_project(request.user.id, projectID):
        return redirect('/req/projects')
    b = None
    
    
    # Should coordinate with front end
    
    try:
        b = backlog.Backlog.objects.get(id=backlogID)
        b.backlogContent = request.backlog_content
        b.save()
    except Exception as e:
        return None   



    
    
    
    



    
