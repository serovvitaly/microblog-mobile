from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from spider.models import PageUrl


class Post(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    meta_data = JSONField()
    is_active = models.BooleanField(default=False)

    def source_url(self):
        return PageUrl.objects.get(pk=self.meta_data['page_url_id']).url

    def url(self):
        return '/post/' + str(self.id)

    def annotation(self):
        content_sections = self.content.split('<!--ANNOTATION_SPLITTER-->')
        if len(content_sections) == 1:
            return ''
        return strip_tags(content_sections[0]).strip()


class PostLog(models.Model):
    post = models.ForeignKey('Post')
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey('Post')
    user = models.ForeignKey(User)
    content = models.CharField(max_length=1200)
    created_at = models.DateTimeField(auto_now_add=True)


class PostGroup(models.Model):
    title = models.CharField(max_length=300)
    posts = models.ManyToManyField(Post)
    meta_data = JSONField()
