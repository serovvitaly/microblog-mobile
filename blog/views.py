from django.shortcuts import render
from django.views import generic
from blog.models import Post
from django.http import Http404


class IndexView(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        return {
            'posts': Post.objects.all(),
        }


class PostView(generic.TemplateView):
    template_name = 'post.html'

    def get_context_data(self, **kwargs):
        try:
            post = Post.objects.get(pk=kwargs['post_id'])
        except Post.DoesNotExist:
            raise Http404("Poll does not exist")
        return {
            'post': post,
            'posts': Post.objects.all(),
        }


class EditorView(generic.TemplateView):
    template_name = 'editor/index.html'

