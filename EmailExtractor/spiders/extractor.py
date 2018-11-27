import scrapy
import re
from bs4 import BeautifulSoup
from urlparse import urlparse


class EmailExtractorSpider(scrapy.Spider):

    name = "extractor"

    founded = False
    bad_ext = [".jpg", ".png", ".jpeg", ".bmp"]

    def __init__(self, url, depth=2, **kwargs):
        self.allowed_domains = [urlparse(url).netloc]
        self.start_urls = [url]
        self.depth = depth
        super(EmailExtractorSpider, self).__init__(**kwargs)

    def parse(self, response):
        try:
            level = response.meta['level']
        except:
            level = 0

        html = response.body_as_unicode()
        emails = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", re.MULTILINE | re.IGNORECASE)
        emails = re.findall(emails, html)

        if len(emails) > 0:
            for email in emails:
                if email.endswith(tuple(self.bad_ext)):
                    continue
                self.founded = True
                yield {'email': email}
        elif level < self.depth and not self.founded:
            soup = BeautifulSoup(html, features='html.parser')
            for link in soup.findAll('a', attrs={'href': re.compile("^http")}):
                url = link.get('href')
                yield scrapy.Request(url, callback=self.parse, meta={'level': level + 1})

