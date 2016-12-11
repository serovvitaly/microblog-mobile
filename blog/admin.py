from django.contrib import admin
from blog.models import Post
from blog.models import PostGroup
from django import forms
from django.template import engines
from ckeditor.widgets import CKEditorWidget
from django.utils.html import strip_tags

django_engine = engines['django']


class MicroBlogPostEditorWidget(forms.widgets.Textarea):
    template = 'admin/widget/multi-content-editor.html'
    def render(self, name, value, attrs=None):
        return django_engine.get_template(self.template).render()


class MicroBlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = ['title', 'content', 'is_active']
        #widgets = {
        #    'content': MicroBlogPostEditorWidget
        #}


class PostAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['title', 'is_active', 'length']
    form = MicroBlogPostForm

    def length(self, rec):
        return len(strip_tags(rec.content))


class PostGroupAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['title']


admin.site.register(Post, PostAdmin)
admin.site.register(PostGroup, PostGroupAdmin)
