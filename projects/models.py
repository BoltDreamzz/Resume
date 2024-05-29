from django.contrib.auth.models import User

# Create your models here.
from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='project_images')

    def __str__(self):
        return self.title


class SubProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    about_page_image = models.ImageField(upload_to='project_images')
    detail_page_image = models.ImageField(upload_to='project_images')

    def __str__(self):
        return f"{self.project}'s sub project"


class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f'Comment on {self.post}'


class Like(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    project_is_liked = models.BooleanField(default=False, null=False, blank=True)
    user_ip = models.GenericIPAddressField()


# models.py

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} to {self.recipient} - {self.timestamp}'
