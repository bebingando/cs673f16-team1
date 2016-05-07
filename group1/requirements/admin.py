from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.mail import send_mail
from django.contrib.auth.models import User

from requirements.models import files
from requirements.models import iteration
from requirements.models import project
from requirements.models import story
from requirements.models import story_comment
from requirements.models import story_attachment
from requirements.models import task
from requirements.models import user_association


# add by Zhi and Nora
class UserAdmin(BaseUserAdmin):
    def save_model(self, request, obj, form, change):
        print "we are using new function~!"
        if change and 'email' not in form.changed_data:
            cd = form.cleaned_data
            Subject = 'Your account has changed!'
            mesg = ''
            print "we are sending email"
            if 'is_active' in form.changed_data:
                if obj.is_active:
                    mesg = 'Welcome to 3blueprint! Your account is active now!\n'
                else:
                    mesg = '''Sorry, we find some problem about you acount.\n
                    So we disable your account few days for checking. Thank you for your understanding\n'''
            if 'is_staff' in form.changed_data:
                if obj.is_staff:
                    mesg = mesg + 'Now you are authorized to login admin system!\n'
                else:
                    mesg = mesg + 'Now you are not allow to login admin system\n'
            if 'is_superuser' in form.changed_data:
                if obj.is_superuser:
                    mesg = mesg + 'Now your are authorized as superuser!!\n'
                else:
                    mesg = mesg + 'You are not superuser any more!\n '
            if form.changed_data:
                mesg = mesg + 'These changes are made:\n'
                for changedPlace in form.changed_data:
                    mesg = mesg + changedPlace + '\n'
                mesg = mesg + '(These are changed by Admin)'
            send_mail(Subject, mesg,
                          'zhidou@hotmail.com', [cd.get('email')])
        obj.save()
admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register(files.ProjectFile)
admin.site.register(iteration.Iteration)
admin.site.register(project.Project)
admin.site.register(story.Story)
admin.site.register(story_comment.StoryComment)
admin.site.register(story_attachment.StoryAttachment)
admin.site.register(user_association.UserAssociation)