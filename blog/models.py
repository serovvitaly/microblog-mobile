from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from spider.models import PageUrl
import markdown

class Post(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    meta_data = JSONField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + '. ' + self.title

    def series(self):
        series_ids = []
        for rel in SeriesPost.objects.filter(post__exact=self).all():
            series_ids.append(rel.series_id)
        if len(series_ids) < 1:
            return None
        return Series.objects.filter(id__in=series_ids).all()

    def previous_posts(self):
        return PostGroup.objects.get(pk=2).posts.filter(is_active__exact=True).all()

    def following_posts(self):
        return PostGroup.objects.get(pk=2).posts.filter(is_active__exact=True).all()

    def source_url(self):
        return PageUrl.objects.get(pk=self.meta_data['page_url_id']).url

    def image(self):
        if 'image_url' not in self.meta_data:
            return False
        return self.meta_data['image_url']

    def url(self):
        return '/post/' + str(self.id)

    def annotation(self):
        content_sections = self.content.split('<!--ANNOTATION_SPLITTER-->')
        if len(content_sections) == 1:
            return ''
        annotation = strip_tags(markdown.markdown(content_sections[0]))
        return annotation.strip()


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


class Tag(models.Model):
    title = models.CharField(max_length=50)
    posts = models.ManyToManyField(Post, default=[])


class Series(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def posts(self):
        posts_ids = []
        for rel in SeriesPost.objects.filter(series__exact=self).all():
            posts_ids.append(rel.series_id)
        if len(posts_ids) < 1:
            return None
        return Post.objects.filter(id__in=posts_ids).all()


class SeriesPost(models.Model):
    series = models.ForeignKey(Series)
    post = models.ForeignKey(Post)
    number = models.IntegerField()