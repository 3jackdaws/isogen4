from django.db.models import Model
from django.db import models

class Log(Model):
    path = models.URLField()
    ip = models.GenericIPAddressField()
    access_time = models.DateTimeField(auto_now_add=True)
