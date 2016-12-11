import urllib.request
from grab import Grab


class HttpService:

    def __init__(self, url):
        self.url = url
        self.html = None
        self.grab = Grab()
        self.grab.go(url)

    def html(self):
        if self.html is not None:
            return self.html
        with urllib.request.urlopen(self.url) as f:
            self.html = f.read().decode('utf-8')
            return self.html
