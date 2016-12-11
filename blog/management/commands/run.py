from django.core.management.base import BaseCommand
import urllib.request
import urllib.parse
import json
import re
from lxml import etree
from datetime import datetime
import psycopg2
import csv
import time

import locale
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

#conn = psycopg2.connect("dbname='microblog' user='postgres' host='localhost' password='123'")
conn = psycopg2.connect(database="microblog", user="postgres", password="123", host="localhost")
cur = conn.cursor()


class Command(BaseCommand):

    def get_page_content(self, page, term):
        url = 'https://naked-science.ru/views/ajax'
        data = {
            'view_name': 'rubric_article_block',
            'view_display_id': 'block',
            'view_args': str(term) + '/' + str(term),
            'view_path': 'taxonomy/term/' + str(term),
            'view_base_path': 'null',
            #'view_dom_id': '99600e61418512210d936c9eb07ea61c',
            #'pager_element': 0,
            'page': page,
        }
        data = urllib.parse.urlencode(data)
        data = data.encode('ascii')
        request = urllib.request.Request(url, data)
        with urllib.request.urlopen(request) as f:
            json_data = json.loads(f.read().decode('utf-8'))
            for item in json_data:
                if item['command'] == 'insert':
                    return item['data']
        return None

    def parse_page_to_csv(self, page, term):
        page_content = self.get_page_content(page, term)
        page_content = page_content.replace('&','&amp;')
        root = etree.fromstring(page_content)
        # Получаем номер последней страницы
        r = root.xpath('//li[@class="pager-last last"]/a/@href')
        reg = re.compile('([\d]+)$')
        try:
            pst = reg.search(r[0])
            last_page = int(pst.group(0))
        except IndexError:
            last_page = None
        # Получаем список статей
        posts_list = root.xpath('//div[@class="view-content"]/div')
        for post in posts_list:
            link = post.xpath('div[@class="views-field views-field-title"]/span/a/@href')[0]
            title = post.xpath('div[@class="views-field views-field-title"]/span/a/text()')[0]
            try:
                content = post.xpath('div[@class="views-field views-field-field-lead"]/div/text()')[0]
            except IndexError:
                content = ''
            post_date = \
            post.xpath('div[@class="views-field views-field-nothing"]/span/span[@class="post-date"]/text()')[0]
            comments_count = \
            post.xpath('div[@class="views-field views-field-nothing"]/span/span[@class="post-comment"]/text()')[0]
            views_count = \
            post.xpath('div[@class="views-field views-field-nothing"]/span/span[@class="post-view"]/text()')[0]
            views_count = views_count.replace(' ', '')
            if views_count[-1] == 'K':
                views_count = int(float(views_count[0:-1]) * 1000)
            elif views_count[-3:] == 'млн':
                views_count = int(float(views_count[0:-3]) * 1000000)
            cur.execute(
                "INSERT INTO parsing_pages "
                "(source, link, title, content, post_date, comments_count, views_count) "
                "VALUES (%(source)s, %(link)s, %(title)s, %(content)s, %(post_date)s, %(comments_count)s, %(views_count)s)"
                "ON CONFLICT (link) DO UPDATE SET "
                "title=%(title)s, content=%(content)s, post_date=%(post_date)s, "
                "comments_count=%(comments_count)s, views_count=%(views_count)s",
                {
                    'source': 'naked-science',
                    'link': 'https://naked-science.ru' + link.strip(),
                    'title': title,
                    'content': content,
                    'post_date': post_date,
                    'comments_count': comments_count,
                    'views_count': views_count,
                }
            )
            conn.commit()

    def handle(self, *args, **options):
        for page in range(1, 10):
            #time.sleep(1)
            print('Page', page)
            self.parse_page_to_csv(page, 10)