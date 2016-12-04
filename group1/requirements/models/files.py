from django.db import models
from project import Project
import os


class ProjectFile(models.Model):
    """
    A file attached to a project
    """

    file = models.FileField(upload_to='project_files')
    project = models.ForeignKey(Project)
    
    # name = original uploaded file name
    name = models.CharField(max_length=255, null=True)
    
    # UUID = name of the file when it is stored in project_files (avoids conflicts)
    uuid = models.CharField(max_length=255, null=True)
        
    def does_attachment_exist(self):
        return bool(self.file)


def delete(fileUUID):
    try:
        attachment = ProjectFile.objects.filter(uuid=fileUUID)
        attachment.delete()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        os.remove(os.path.join(BASE_DIR, '../../project_files/' + fileUUID))
    except Exception as e:
        return None