from django.shortcuts import render
from django.views import generic
from blog.models import Post
from django.http import Http404


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
        if is_editor:
            posts = Post.objects.all()[0:30]
        else:
            posts = Post.objects.filter(is_active__exact=True).all()[0:30]
        return {
            'items': posts,
            #'columns_count': 3,
            'wrapper_widget': 'widget/multi-column.html',
            'item_widget': 'widget/post-mini.html',
            'is_editor': is_editor,
        }


class PostView(generic.TemplateView):
    template_name = 'post.html'

    def get_context_data(self, **kwargs):
        try:
            post = Post.objects.get(pk=kwargs['post_id'])
        except Post.DoesNotExist:
            raise Http404("Poll does not exist")
        return {
            'item': post,
            'posts': Post.objects.all()[0:10],
            'is_editor': self.request.user.has_perm('blog.change_post'),
            'sub_posts': Post.objects.all()[0:6],
        }


class EditorView(generic.TemplateView):
    template_name = 'editor/index.html'

