from django.views import generic
from blog.models import Tag
from blog.models import Post
from django.http import Http404, HttpResponseForbidden
from django.http import HttpResponse, JsonResponse
import markdown


class IndexView(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        is_editor = self.request.user.has_perm('blog.change_post')
        #posts = PostGroup.objects.get(pk=2).posts
        #posts = Tag.objects.get(pk=1).posts.order_by('id')
        #if is_editor:
        #    posts = Post.objects.all()
        #else:
        posts = Post.objects.filter(is_active__exact=True).all()
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


class MetricsView(generic.View):

    def get(self, request):
        return HttpResponse('[{"target": "entries","datapoints": [[1.0, 1311836008],[2.0, 1311836009],[3.0, '
                            '1311836010],[5.0, 1311836011],[6.0, 1311836012]]}]')


class RenderView(generic.View):

    def post(self, request):
        return HttpResponse('[{"target": "entries","datapoints": [[1.0, 1311836008],[2.0, 1311836009],[3.0, '
                            '1311836010],[5.0, 1311836011],[6.0, 1311836012]]}]')

