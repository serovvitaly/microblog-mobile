from django.core.management.base import BaseCommand
from spider.service.WwwSpringOrgUk import WwwSpringOrgUk
from blog.models import Post
from spider.models import PageUrl
from termcolor import cprint
from grab.error import GrabTooManyRedirectsError

class Command(BaseCommand):

    def handle(self, *args, **options):
        for page_url in PageUrl.objects.all():
            cprint(str(page_url.id)+' - '+page_url.url, 'blue')
            try:
                page_service = WwwSpringOrgUk(page_url.url)
            except GrabTooManyRedirectsError:
                continue
            page_title = page_service.title()
            page_content = page_service.content()
            if page_title is None:
                continue
            Post(
                title=page_title,
                content=page_content,
                meta_data={'page_url_id': page_url.id}
            ).save()
