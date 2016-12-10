from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=300)
    content = JSONField()

    def url(self):
        return '/post/' + str(self.id)


class PostLog(models.Model):
    post = models.ForeignKey('Post')
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey('Post')
    user = models.ForeignKey(User)
    content = models.CharField(max_length=1200)
    created_at = models.DateTimeField(auto_now_add=True)
