from django.shortcuts import render
from django.views import generic
from blog.models import Tag
from blog.models import Post
from blog.models import PostGroup
from django.http import Http404, HttpResponseForbidden
from django.http import HttpResponse
import markdown


def super_column(iterable_object, parts_number):
    try:
        iter(iterable_object)
    except TypeError:
        return None
    output_arr = []
    part_number = 1
    for iterable_item in iterable_object:
        if part_number not in output_arr:
            output_arr.append([])
        print(part_number, iterable_item.id)
        output_arr[part_number-1].append(part_number)
        part_number += 1
        if part_number > parts_number:
            part_number = 1
    print(output_arr)


class IndexView(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        is_editor = self.request.user.has_perm('blog.change_post')
        #posts = PostGroup.objects.get(pk=2).posts
        posts = Tag.objects.get(pk=1).posts
        if is_editor:
            posts = posts.all()
        else:
            posts = posts.filter(is_active__exact=True).all()
        return {
            'items': posts,
            #'columns_count': 3,
            'wrapper_widget': 'widget/multi-column.html',
            'item_widget': 'widget/post-mini.html',
            'is_editor': is_editor,
        }


class PostView(generic.TemplateView):
    template_name = 'post.html'

    def post(self, request, post_id):
        is_editor = request.user.has_perm('blog.change_post')
        if is_editor is not True:
            return HttpResponseForbidden('')
        post = Post.objects.get(pk=post_id)
        post.content = request.POST.get('content')
        post.save()
        return HttpResponse({
            'success': True
        })

    def get_context_data(self, **kwargs):
        try:
            post = Post.objects.get(pk=kwargs['post_id'])
        except Post.DoesNotExist:
            raise Http404("Post not found")
        if self.request.user.has_perm('blog.change_post', post) is False and post.is_active is False:
            raise Http404("Post not found")
        return {
            'item': post,
            'post_content': markdown.markdown(post.content),
            'posts': Post.objects.all()[0:10],
            'is_editor': self.request.user.has_perm('blog.change_post'),
            'sub_posts': Post.objects.all()[0:6],
        }


class EditorView(generic.TemplateView):
    template_name = 'editor/index.html'

