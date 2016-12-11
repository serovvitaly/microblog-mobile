from django.core.management.base import BaseCommand
import urllib.request
import urllib.parse
import json
import re
from lxml import etree
import psycopg2
import time

conn = psycopg2.connect(database="microblog", user="postgres", password="123", host="localhost")
cur = conn.cursor()


class Command(BaseCommand):

    def parse_page_to_csv(self, page):
        page_content = self.get_page_content(page)
        page_content = page_content.replace('&','&amp;')
        root = etree.fromstring(page_content)
        # Получаем номер последней страницы
        r = root.xpath('//li[@class="pager-last last"]/a/@href')
        reg = re.compile('([\d]+)$')
        pst = reg.search(r[0])
        last_page = int(pst.group(0))
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

            # post_date = post_date.encode('utf-8')

            res = cur.execute(
                "INSERT INTO parsing_pages "
                "(source, link, title, content, post_date, comments_count, views_count) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    'naked-science',
                    'https://naked-science.ru' + link,
                    title,
                    content,
                    post_date,
                    comments_count,
                    views_count,
                )
            )
            conn.commit()
            print(res)

    def handle(self, *args, **options):
        root = etree.parse('/var/www/micro-blog/Sitemap file_ https___naked-science.ru_sitemap.xml')
        for url in root.xpath('/urlset/url/loc/text()'):
            cur.execute(
                "INSERT INTO parsing_pages "
                "(source, link) "
                "VALUES (%s, %s)",
                (
                    'naked-science',
                    url.strip(),
                )
            )
        conn.commit()