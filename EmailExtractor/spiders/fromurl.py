import scrapy
import re
from bs4 import BeautifulSoup

try:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError


class FromUrlSpider(scrapy.Spider):

    name = "fromurl"

    bad_ext = [".jpg", ".png", ".jpeg", ".bmp"]

    def __init__(self, url, depth=1, **kwargs):
        self.allowed_domains = [urlparse(url).netloc]
        self.urls = [url]
        self.depth = depth
        super(FromUrlSpider, self).__init__(**kwargs)

    def start_requests(self):
        return [scrapy.Request(url, callback=self.parse, meta={'level': 0, 'url': url}) for url in self.urls]

    def parse(self, response):
        level = response.meta['level']
        url = response.meta['url']

        html = response.body_as_unicode()
        emails = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", re.MULTILINE | re.IGNORECASE)
        emails = re.findall(emails, html)

        for email in emails:
            if email.endswith(tuple(self.bad_ext)):
                continue
            yield {'url': url, 'email': email}

        if level < self.depth:
            soup = BeautifulSoup(html, features='html.parser')
            for link in soup.findAll('a', attrs={'href': re.compile("^http")}):
                url = link.get('href')
                yield scrapy.Request(url, callback=self.parse, meta={'level': level + 1, 'url': url})
