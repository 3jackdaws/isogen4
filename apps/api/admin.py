from django.contrib import admin
from .models import *

admin.site.register(TaskCollection)
admin.site.register(TaskCompletion)
admin.site.register(Task)
admin.site.register(Actor)