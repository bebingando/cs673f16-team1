import uuid
import os
from django.db import models
from story import Story
from story import *


class StoryAttachment(models.Model):
    
    # name of the file when it is stored in project_files (avoids conflicts)
    uuid = models.CharField(max_length=255,null=True)
    story = models.ForeignKey(Story)
    # original uploaded file name
    name = models.CharField(max_length=255,null=True)
    # will be uploaded to MEDIA_ROOT/story_attachments directory
    file = models.FileField(upload_to='story_attachments') 
    # timestamp to display when the file was uploaded
    last_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name
    
def delete(attachmentUUID):
    try:
        attachment = StoryAttachment.objects.filter(uuid=attachmentUUID)
        attachment.delete()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        os.remove(os.path.join(BASE_DIR, '../../story_attachments/'+attachmentUUID))
    except Exception as e:
        return None
    
    
def get_attachments_for_story(story):
    if story is None:
        return None
    return StoryAttachment.objects.filter(story_id=story.id) 

def get_all_attachments():
    return StoryAttachment.objects.all() 


def get_attachment(attachmentUUID):
    try:
        return StoryAttachment.objects.get(uuid=attachmentUUID)
    except Exception as e:
        return None

def create(story_id, file):
    if story_id is None:
        return None
    if file is None:
        return None
    
    fileUUID = str(uuid.uuid4())
    story = get_story(story_id)
    name = file.name    
    file = file
    
    #rename file object to have UUID as name to avoid conflicts when retrieving files
    file.name=fileUUID
    
    newAttachment = StoryAttachment(
        uuid=fileUUID,
        story=story,
        name=name,
        file=file,
    )
    newAttachment.save()
    return newAttachment
