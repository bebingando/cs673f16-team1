from requirements.models import project_api
from django.contrib.auth.decorators import login_required
from django import forms
from requirements import models
from requirements.views import projects
from requirements.models import backlog
from requirements.models import user_manager
from requirements.models import story as mdl_story
from requirements.models import iteration as mdl_iteration
from requirements.models import task as mdl_task
from requirements.models.user_manager import user_owns_project
from requirements.models.user_association import UserAssociation
from forms import BacklogForm
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

import logging

logger = logging.getLogger(__name__)


import datetime
from requirements.models.user_manager import user_can_access_project

PERMISSION_OWN_PROJECT = 'requirements.own_project'


@login_required(login_url='/signin')
def create_backlog(request, projectID):
    if request.method == 'POST':
        
        form = BacklogForm(request.POST)
        #if form.is_valid():
        '''
        p = project_api.get_project(projectID)
        blog = backlog.Backlog()
        blog.storyTitle = 'dsads'
        blog.project = p
        blog.backlogContent = 'dsadswfew'
        blog.storyStatus = 'Not start'
        blog.save()
        '''
            
            #try:
        blog = makeNewBacklog(request.POST, projectID)
        
        if blog != None:
            blog.save()
        #    blog.save()
        #    blog = form.save(commit = False)
            #except :
            #    logger.error('some thing wrong with create backlog')
            
        return HttpResponse("")
    else:
        form = BacklogForm()
    p = project_api.get_project(projectID)
    
    context = {
            'form' : form,
            'action': '/req/newbacklog/'+str(projectID),
            'button_desc':'Create Backlog',
            'title' : 'New backlog',
               
    }
    return render(request, 'ProjectBacklogSummary.html',context)     
    
    #rest is UI interaction
    

def makeNewBacklog(fields, pid):
    title = fields.get('storyTitle', '')
    proj = project_api.get_project(pid)
    content = fields.get('backlogContent','')
    status = 'Not Start'

    blog = backlog.Backlog()
    blog.storyTitle = title
    blog.project = proj
    blog.backlogContent = content
    blog.storyStatus = 'Not start'    
    
    return blog
    
    

@login_required(login_url='/signin')
def show_backlog(request, projectID):
    project = project_api.get_project(projectID)
    if project is None:
        return redirect('/req/projects')

    iterations = mdl_iteration.get_iterations_for_project(project)
    association = UserAssociation.objects.get(
        user=request.user,
        project=project)

    #Show backlog according to the project id
    if not project_api.can_user_access_project(request.user.id, projectID):
        return redirect('/req/projects')
    
    logs = project.backlog_set.all()
    context = {'projects': project_api.get_projects_for_user(request.user.id),
               'project': project,
               'stories': mdl_story.get_stories_for_project(project),
               'tasks': mdl_task.get_all_tasks(),
               'iterations': iterations,
               'association': association,
               'canOwnProject': request.user.has_perm(PERMISSION_OWN_PROJECT),
               'backlogs' : logs,
               }
    return render(request, 'ProjectBacklog.html',context)


@login_required(login_url='/signin')
def edit_backlog(request, projectID, backlogID):
    project = project_api.get_project(projectID)
    blog = backlog.Backlog.objects.get(id = backlogID)
    if project == None or blog == None:
        return HttpResponse('')
    
    if request.method == "POST":
        form = BacklogForm(request.POST, instance=blog)
        fields = request.POST 

        blog.storyTitle = fields.get('storyTitle', '')
        blog.project = project
        blog.backlogContent = fields.get('backlogContent','')
        blog.storyStatus = 'Edited'  
        blog.save()
        return HttpResponse('')      

    else:
        form = BacklogForm(instance = blog)
    
    context = {
            'form' : form,
            'action': '/req/editbacklog/'+str(projectID)+'/'+str(backlogID),
            'button_desc':'Update Backlog',
            'title' : 'Edit backlog',
               
    }
    return render(request, 'ProjectBacklogSummary.html',context)    
    
    
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


@login_required(login_url='/signin')
def delete_backlog(request, projectID, backlogID):
    proj = project_api.get_project(projectID)
    blog = backlog.Backlog.objects.get(id=backlogID)
    
    if proj == None or blog == None:
        return HttpResponse('')
    
    if request.method == 'POST':
        blog.delete()
        return HttpResponse('')
    else:
        form = BacklogForm(instance = blog)
    
    context = {
            'form' : form,
            'action': '/req/deletebacklog/'+str(projectID)+'/'+str(backlogID),
            'button_desc':'Delete Backlog',
            'title' : 'Delete backlog',
            'confirm_message' : 'This operation is not irreversible!'
    }
    
    return render(request, 'ProjectBacklogSummary.html',context) 
    
    
    
    
    
    
    



    
