'''
from .fromurl import FromUrlSpider
try:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError


class FromUrlsSpider(FromUrlSpider):

    name = "fromurls"

    allowed_domains = []
    urls = []

    def __init__(self, urls_file, depth=1, **kwargs):
        urls = open(urls_file).read().splitlines()
        for url in urls:
            self.allowed_domains.append(urlparse(url).netloc)
            self.urls.append(url)
        self.depth = depth
        super(FromUrlsSpider, self).__init__(**kwargs)
'''

class base(object):

    def __init__(self):
        print('base')


class A(base):

    def __init__(self):
        print('A')
        super(A, self).__init__()


class B(A):

    def __init__(self):
        print('B')
        super(B, self).__init__()

B()