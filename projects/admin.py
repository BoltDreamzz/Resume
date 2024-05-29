from django.contrib import admin
from .models import Project, SubProject, Message, Comment
# Register your models here.


admin.site.register(Project)
admin.site.register(SubProject)
admin.site.register(Message)
admin.site.register(Comment)