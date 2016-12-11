from django.contrib import admin
from spider.models import PageUrl


class PageUrlAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['id', 'link', 'created_at']

    def link(self, rec):
        return '<a target="_blank" href="' + rec.url + '">' + rec.url + '</a>'

    link.allow_tags = True

admin.site.register(PageUrl, PageUrlAdmin)
