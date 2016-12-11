from django.core.management.base import BaseCommand
import urllib.request
import re
from spider.models import PageUrl


class Command(BaseCommand):

    def get_page_content(self, url):
        with urllib.request.urlopen(url) as f:
            html = f.read().decode('utf-8')
            return html

    def handle(self, *args, **options):
        list_url = 'http://www.spring.org.uk/page/'
        for page in range(1, 101):
            page_content = self.get_page_content(list_url+str(page))
            ptrn = re.compile('<h2 class="headline front"><a href="([^"]+)" rel="bookmark">')
            matches = ptrn.findall(page_content)
            print('Page', page, 'Count', len(matches))
            for post_url in matches:
                post_url = post_url.strip()
                rate, created = PageUrl.objects.get_or_create(url=post_url)
                rate.save()
