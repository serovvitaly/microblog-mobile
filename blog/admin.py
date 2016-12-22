from django.contrib import admin
from blog.models import Tag, Post, PostGroup, Series, SeriesPost, PostRelation, PostRelationType
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
        fields = ['title', 'content', 'is_active', 'meta_data']
        #widgets = {
        #    'content': MicroBlogPostEditorWidget
        #}


class PostAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['id', 'title', 'source', 'is_active', 'length']
    list_filter = ['is_active']
    search_fields = ('title',)
    #form = MicroBlogPostForm

    def source(self, rec):
        source_url = rec.source_url()
        return '<a href="' + source_url + '">' + source_url + '</a>'
    source.allow_tags = True

    def has_image(self, rec):
        return bool(rec.image())
    has_image.boolean = True

    def length(self, rec):
        return len(strip_tags(rec.content))


class TagAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['title']


class PostGroupAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['title']


class SeriesAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['title']


class SeriesPostAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['series', 'post_link', 'number', 'post_is_active']
    list_filter = ['series']

    def post_link(self, rec):
        post = Post.objects.get(pk=rec.post_id)
        return '<a href="/admin/blog/post/' + str(post.id) + '/change/">' + post.title + '</a>'
    post_link.allow_tags = True

    def post_is_active(self, rec):
        post = Post.objects.get(pk=rec.post_id)
        return bool(post.is_active)
    post_is_active.boolean = True


class PostRelationAdmin(admin.ModelAdmin):
    list_display = ['id', 'post_from_link', 'post_to_link', 'type']

    def post_from_link(sel, rec):
        post_from = rec.post_from
        return str(post_from.id) + '. <a href="/admin/blog/post/' + str(post_from.id) + '/change/">' + post_from.title + '</a>'
    post_from_link.allow_tags = True

    def post_to_link(sel, rec):
        post_to = rec.post_to
        return str(post_to.id) + '. <a href="/admin/blog/post/' + str(post_to.id) + '/change/">' + post_to.title + '</a>'
    post_to_link.allow_tags = True


class PostRelationTypeAdmin(admin.ModelAdmin):
    list_display = ['title']


admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostGroup, PostGroupAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(SeriesPost, SeriesPostAdmin)
admin.site.register(PostRelation, PostRelationAdmin)
admin.site.register(PostRelationType, PostRelationTypeAdmin)
