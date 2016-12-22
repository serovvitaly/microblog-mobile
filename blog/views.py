from django.views import generic
from blog.models import Post, Series, Group
from django.http import Http404, HttpResponseForbidden, HttpResponse, JsonResponse
import markdown


class IndexView(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        series_id = None
        try:
            if 'series' in self.request.GET:
                series_id = int(self.request.GET['series'])
        except ValueError:
            pass
        is_editor = self.request.user.has_perm('blog.change_post')
        if series_id:
            series = Series.objects.get(pk=series_id)
            posts = series.posts(only_is_active=True)
        else:
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
        content = request.POST.get('content')
        if content:
            post.content = content
        is_active = request.POST.get('is_active')
        if is_active:
            post.is_active = bool(int(is_active))
        post.save()
        return JsonResponse({
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
            'RESULT_PAGE': '/hello/',
            'item': post,
            'post_content': markdown.markdown(post.content),
            'posts': Post.objects.all()[0:10],
            'is_editor': self.request.user.has_perm('blog.change_post'),
            'sub_posts': Post.objects.all()[0:6],
        }


class SeriesListView(generic.TemplateView):
    template_name = 'series.html'

    def get_context_data(self, **kwargs):
        is_editor = self.request.user.has_perm('blog.change_post')
        series_list = []
        for series in Series.objects.all():
            if series.posts():
                series_list.append(series)
        return {
            'items': series_list,
            'wrapper_widget': 'widget/multi-column.html',
            'item_widget': 'widget/series-item.html',
            'is_editor': is_editor,
        }


class SeriesView(generic.TemplateView):
    template_name = 'series.html'

    def get_context_data(self, **kwargs):
        try:
            series = Series.objects.get(pk=kwargs['series_id'])
        except Series.DoesNotExist:
            raise Http404("Series not found")
        is_editor = self.request.user.has_perm('blog.change_post')
        posts = series.posts(only_is_active=True)
        return {
            'title': series.title,
            'items': posts,
            # 'columns_count': 3,
            'wrapper_widget': 'widget/multi-column.html',
            'item_widget': 'widget/series-item.html',
            'is_editor': is_editor,
        }


class GroupView(generic.TemplateView):
    template_name = 'series.html'

    def get_context_data(self, **kwargs):
        try:
            group = Group.objects.get(pk=kwargs['group_id'])
        except Series.DoesNotExist:
            raise Http404("Group not found")
        is_editor = self.request.user.has_perm('blog.change_post')
        posts = group.posts(only_is_active=True)
        return {
            'title': group.title,
            'items': posts,
            # 'columns_count': 3,
            'wrapper_widget': 'widget/multi-column.html',
            'item_widget': 'widget/post-mini.html',
            'is_editor': is_editor,
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

