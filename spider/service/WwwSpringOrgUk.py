from spider.service.HttpService import HttpService
from weblib.error import DataNotFound

from lxml.html import HtmlElement
class WwwSpringOrgUk(HttpService):

    def title(self):
        try:
            title = self.grab.doc.select('//h1[@class="headline single"]').text()
            return title.strip()
        except DataNotFound:
            return None

    def content(self):
        nr = '\n\r'
        output_content = ''
        content = self.grab.doc.select('//div[@class="post_content"]/p | '
                                       '//div[@class="post_content"]/h2 | '
                                       '//div[@class="post_content"]/ul/li | '
                                       '//div[@class="post_content"]/ol/li | '
                                       '//div[@class="post_content"]/blockquote')
        for p in content:
            if len(p.text()) < 1:
                continue
            tag = p.node().tag
            #parent_tag = p.node().getparent().tag
            prefix = ''
            if tag == 'p':
                prefix = nr
            elif tag == 'h2':
                prefix = nr + '### '
            elif tag == 'li':
                prefix = '* '
            elif tag == 'blockquote':
                prefix = nr + '> '
            output_content += prefix + p.text() + nr
        return output_content.strip()
