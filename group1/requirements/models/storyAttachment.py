from django.db import models
from story import Story

class storyAttachment(models.Model):
    
    #file will be uploaded to MEDIA_ROOT/story_attachments directory
    file = models.FileField(upload_to='story_attachments')
    
    storyID = models.ForeignKey(Story)
    
    #name = original uploaded file name
    name = models.CharField(max_length=255,null=True)
    
    #UUID = name of the file when it is stored in project_files (avoids conflicts)
    UUID = models.CharField(max_length=255,null=True)
        
    def does_attachment_exist(self):
        return bool(self.file)