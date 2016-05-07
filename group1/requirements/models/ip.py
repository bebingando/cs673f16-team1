from django.db import models
from django.utils import timezone
import time
from datetime import datetime
from django.contrib.auth.models import User

class IPaddress(models.Model):
    #users = models.ForeignKey(User)
    ip = models.CharField(max_length=50)
    #now = time.time()
    last_time = models.DateTimeField(max_length=50)
    #input_time = models.DateTimeField(default = time.time())

    def __str__(self):
        return self.ip

    class Meta:
        app_label = 'requirements'
