from django.db import models
from story import Story


class StoryAttachment(models.Model):
    
    # name of the file when it is stored in project_files (avoids conflicts)
    uuid = models.CharField(max_length=255,null=True)
    story = models.ForeignKey(Story)
    # original uploaded file name
    name = models.CharField(max_length=255)
    # will be uploaded to MEDIA_ROOT/story_attachments directory
    file = models.FileField(upload_to='story_attachments') 
    # timestamp to display when the file was uploaded
    last_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name
    
    
def get_attachments_for_story(story):
    if story is None:
        return None
    return StoryAttachment.objects.filter(story_id=story.id) 


def get_attachment(attachmentID):
    try:
        return StoryAttachment.objects.get(id=attachmentID)
    except Exception as e:
        return None

    
def create(story, fields):
    if story is None:
        return None
    if fields is None:
        return None

    name = fields.get('name', '')
    file = fields.get('file', '')

    newAttachment = StoryAttachment(
        story=story,
        name=name,
        file=file,
    )
    newAttachment.save()
    return newAttachment
