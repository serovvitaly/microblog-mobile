from django.views import generic
from blog.models import Post, Series, Ribbon
from django.http import Http404, HttpResponseForbidden, HttpResponse, JsonResponse
import markdown
from django.template import loader, Context
import re


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
        }


class PostView(generic.TemplateView):
    template_name = 'post.html'

    def dispatch_OLD(self, request, *args, **kwargs):
        is_editor = request.user.has_perm('blog.change_post')
        if is_editor is not True:
            return HttpResponseForbidden('')
        post_id = int(kwargs['post_id'])
        post = Post.objects.get(pk=post_id)
        if post.is_active is True:
            post.is_active = False
        else:
            post.is_active = True
        post.save()
        return JsonResponse({
            'success': True,
            'is_active': post.is_active
        })

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
            'success': True,
            'is_active': post.is_active,
        })

    def snippet_post_1_callback(self, matches):
        post = Post.objects.get(pk=matches.group(1))
        url = post.url() + '?from=post_inner_' + str(self.post.id)
        return '<div class="alert alert-info"><strong><a href="'+url+'">'+post.title+'</a></strong></div>'

    def snippet_post_1(self, content):
        content = re.sub(r"\[post\:(\d+)\]", self.snippet_post_1_callback, content)
        return content

    def get_context_data(self, **kwargs):
        try:
            self.post = Post.objects.get(pk=kwargs['post_id'])
        except Post.DoesNotExist:
            raise Http404("Post not found")
        if self.request.user.has_perm('blog.change_post', self.post) is False and self.post.is_active is False:
            raise Http404("Post not found")
        post_content = self.post.content
        post_content = self.snippet_post_1(post_content)
        return {
            'RESULT_PAGE': '/hello/',
            'item': self.post,
            'post_content': markdown.markdown(post_content),
            'posts': Post.objects.filter(is_active__exact=True),
            'is_editor': self.request.user.has_perm('blog.change_post'),
            'sub_posts': Post.objects.all()[0:6],
        }


class PostsView(generic.View):
    def get(self, request):
        template = loader.get_template('widget/multi-column.html')
        start_post_index = int(request.GET['offset'])
        end_post_index = start_post_index + int(request.GET['limit'])
        context = Context({
            'items': Post.objects.filter(is_active__exact=True).all()[start_post_index:end_post_index],
            'item_widget': 'widget/post-mini.html',
        })
        return JsonResponse({
            'success': True,
            'html': template.render(context)
        })


class SeriesListView(generic.TemplateView):
    template_name = 'series.html'

    def get_context_data(self, **kwargs):
        is_editor = self.request.user.has_perm('blog.change_post')
        series_list = []
        for series in Series.objects.filter(is_active__exact=True).all():
            if series.posts(only_is_active=True):
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
            group = Ribbon.objects.get(pk=kwargs['group_id'])
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

