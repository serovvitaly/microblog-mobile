from django.db import models


class PageUrl(models.Model):
    url = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
