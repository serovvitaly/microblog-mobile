from spider.service.HttpService import HttpService
from weblib.error import DataNotFound


class WwwSpringOrgUk(HttpService):

    def title(self):
        try:
            title = self.grab.doc.select('//h1[@class="headline single"]').text()
            return title.strip()
        except DataNotFound:
            return None

    def content(self):
        output_content = ''
        content_obj = []
        content = self.grab.doc.select('//div[@class="post_content"]/p | '
                                       '//div[@class="post_content"]/h2 | '
                                       '//div[@class="post_content"]/blockquote')
        for p in content:
            tag = p.node().tag
            output_content += '<' + tag + '>' + p.text() + '</' + tag + '>'
            content_obj.append({
                'tag': p.node().tag,
                'text': p.text()
            })
        return output_content
