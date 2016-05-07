from django.db import models
from django.contrib.auth.models import User
from story import Story
from base import ProjMgmtBase
from iteration import Iteration
from user_association import UserAssociation
from django.http import HttpResponse

from requirements.models import project_api
from requirements.models import task
from project import Project

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

from reportlab.lib import colors
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Line
from reportlab.graphics.shapes import Drawing





class PDF(ProjMgmtBase):
    iteration_description = models.BooleanField(default = True)
    iteration_duration = models.BooleanField(default = True)
    story_description = models.BooleanField(default = True)
    story_reason = models.BooleanField(default = True)
    story_test = models.BooleanField(default=True)
    story_task = models.BooleanField(default = True)
    story_owner = models.BooleanField(default = True)
    story_hours = models.BooleanField(default = True)
    story_status = models.BooleanField(default = True)
    story_points = models.BooleanField(default = True)
    pie_chart = models.BooleanField(default = True)

    class Meta:
        app_label = 'requirements'


#
#
# def make_Statement(ProjectID):
#     try:
#         statement = ""
#
#         project = project_api.get_project(ProjectID)
#         statement += make_Project_Statement(project)
#
#         iterations = project_api.get_iterations_for_project(project)
#
#         iceboxStories = project_api.get_stories_with_no_iteration(project)
#         statement+="IceBox:\n"
#
#         for iceboxStory in iceboxStories:
#             statement += make_Story_Statement(iceboxStory)
#         for iteration in iterations:
#             statement += make_Iteration_Statement(iteration)
#             stories = project_api.get_stories_for_iteration(iteration)
#             for story in stories:
#                 statement += make_Story_Statement(story)
#         return statement
#
#     except Exception as e:
#         return "None1"
#
#
# #def fetch_Project(ProjectID):
# #    try:
# #        return project_api.get_project(ProjectID)
# #    except Exception as e:
# #        return "None2"
#
# def make_Project_Statement(Project):
#     try:
#         return "Project:"+Project.title+"\n"+"---------------------"+"\n"+"Description:"+Project.description+"\n"+"\n"
#     except Exception as e:
#         return "None3"
#
# def make_Iteration_Statement(iteration):
#     try:
#         return iteration.title+"\nIteration Description:"+iteration.description+"\n"
#     except Exception as e:
#         return "None4"
#
# def make_Story_Statement(story):
#     try:
#         return "\t"+story.title+"\n\tDescription:"+story.description+"\n\tImportance:"+str(story.points)+"\n\n"
#     except Exception as e:
#         return "None5"

#--------------Below are PDF makers:----------------
def make_Project_Statement(content, Project):
    try:
        styles = get_style_dic()
        content.append(Paragraph(Project.title, styles['projTitle']))
        content.append(Paragraph(Project.description, styles['projDes']))
    except Exception as e:
        return "None3"

def make_Iteration_Statement(content, iteration, args):
    try:
        styles = get_style_dic()
        content.append(Paragraph(iteration.title, styles['iterTitle']))
        if args['iteration_description']:
            content.append(Paragraph(iteration.description, styles['iterDes']))
        if args['iteration_duration']:
            content.append(Paragraph(str(iteration.start_date)+" - "+str(iteration.end_date), styles['iterNormal']))
    except Exception as e:
        return "None4"

def make_Stories_Statement(content, stories, args):
    try:
        styles = get_style_dic()
        for story in stories:
            content.append(Paragraph(story.title, styles['storyTitle']))
            if args['story_description']:
                content.append(Paragraph(story.description, styles['storyDes']))

            if args['story_reason']:
                content.append(Paragraph("Reason: "+story.reason, styles['storyNormal']))

            if args['story_test']:
                content.append(Paragraph("Test: " + story.test, styles['storyNormal']))

            if args['story_task']:
                make_Task_Statment(content, story)

            if args['story_owner']:
                if story.owner is None:
                    content.append(Paragraph("Owner: None", styles['storyNormal']))
                else:
                    content.append(Paragraph("Owner: "+story.owner.username, styles['storyNormal']))

            if args['story_hours']:
                content.append(Paragraph("Hours: "+str(story.hours), styles['storyNormal']))

            if args['story_status']:
                if story.status == 1:
                    content.append(Paragraph("Status: Unstarted", styles['storyNormal']))
                if story.status == 2:
                    content.append(Paragraph("Status: Started", styles['storyNormal']))
                if story.status == 3:
                    content.append(Paragraph("Status: Completed", styles['storyNormal']))
                if story.status == 4:
                    content.append(Paragraph("Status: Accepted", styles['storyNormal']))

            if args['story_points']:
                content.append(Paragraph("Importance: "+str(story.points), styles['storyNormal']))
    except Exception as e:
        return "None5"

def make_Task_Statment(content, story):
    tasks = task.get_tasks_for_story(story)
    styles = get_style_dic()
    content.append(Paragraph("Task:", styles['storyNormal']))
    i = 1
    for t in tasks:
        content.append(Paragraph(str(i)+". "+t.description, styles['taskNormal']))
        i = i+1

def get_story_count_list(ProjectID):
    count = []
    try:
        project = project_api.get_project(ProjectID)

        count.append(project_api.get_stories_with_no_iteration(project).count())

        iterations = project_api.get_iterations_for_project(project)
        for iteration in iterations:
            count.append(project_api.get_stories_for_iteration(iteration).count())

        return count
    except Exception as e:
        return "None6"

def get_story_name_list(ProjectID):
    name = ['icebox']
    try:
        project = project_api.get_project(ProjectID)
        iterations = project_api.get_iterations_for_project(project)
        for iteration in iterations:
            name.append(iteration.title)

        return name
    except Exception as e:
        return "None7"

def process_pdf(doc, ProjectID, args):
    try:
        story = []
        styles = get_style_dic()

        project = project_api.get_project(ProjectID)
        make_Project_Statement(story, project)
        add_Line(story)

        story.append(Paragraph("IceBox", styles['iterTitle']))
        make_Stories_Statement(story, project_api.get_stories_with_no_iteration(project), args)
        story.append(Paragraph("", styles['iterSpace']))

        iterations = project_api.get_iterations_for_project(project)
        for iteration in iterations:
            make_Iteration_Statement(story, iteration, args)
            make_Stories_Statement(story, project_api.get_stories_for_iteration(iteration), args)
            story.append(Paragraph("", styles['iterSpace']))

        if args['pie_chart']:
            story.append(Paragraph("&nbsp;", styles['bigSpace']))
            story.append(Paragraph("Stories Number In Iterations", styles['iterTitle']))
            draw_Pie(story, ProjectID)

        doc.build(story)
    except Exception as e:
        return "None8"

def get_style_dic():
    dic = {}

    dic['projTitle'] = getSampleStyleSheet()['Heading1']
    dic['projDes'] = getSampleStyleSheet()['Italic']
    dic['projDes'].fontSize = 13

    dic['iterTitle'] = getSampleStyleSheet()['Heading2']
    dic['iterTitle'].leading = 10
    dic['iterDes'] = getSampleStyleSheet()['Italic']
    dic['iterDes'].fontSize = 11
    dic['iterNormal'] = getSampleStyleSheet()['Normal']
    dic['iterNormal'].fontSize = 9
    dic['iterSpace'] = getSampleStyleSheet()['Normal']
    dic['iterSpace'].leading = 40

    dic['storyTitle'] = getSampleStyleSheet()['Heading2']
    dic['storyTitle'].leading = 6
    dic['storyTitle'].fontSize = 11
    dic['storyTitle'].leftIndent = 30
    dic['storyDes'] = getSampleStyleSheet()['Italic']
    dic['storyDes'].fontSize = 8
    dic['storyDes'].leading = 10
    dic['storyDes'].leftIndent = 30
    dic['storyNormal'] = getSampleStyleSheet()['Normal']
    dic['storyNormal'].leftIndent = 30
    dic['storySpace'] = getSampleStyleSheet()['Normal']
    dic['storySpace'].leading = 10

    dic['taskNormal'] = getSampleStyleSheet()['Normal']
    dic['taskNormal'].leftIndent = 60

    dic['bigSpace'] = getSampleStyleSheet()['Normal']
    dic['bigSpace'].leading = 50

    return dic

def add_Line(story):
    d = Drawing(450, 10)
    l = Line(0, 0, 450, 0)
    d.add(l)
    story.append(d)

def draw_Pie(story, ProjectID):
    d = Drawing(140, 180)
    pie = Pie()
    pie.sideLabels = 1
    pie.labels= get_story_name_list(ProjectID)
    pie.data = get_story_count_list(ProjectID)
    pie.width = 140
    pie.height = 140
    pie.y = 0
    pie.x = 150
    d.add(pie)
    story.append(d)

