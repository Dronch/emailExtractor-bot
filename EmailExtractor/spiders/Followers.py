import scrapy
import re


class FollowersSpider(scrapy.Spider):

    name = "followers"

    allowed_domains = ['www.instagram.com']

    def __init__(self, users, **kwargs):
        self.proxy_list = open('proxy.txt').read().splitlines()
        self.accounts = open(users).read().splitlines()
        self.logger.info('Total accounts: {}'.format(len(self.accounts)))
        super(FollowersSpider, self).__init__(**kwargs)

    def start_requests(self):
        pages = []
        for a in self.accounts:
            url = 'https://www.instagram.com/{userid}'.format(userid=a)
            page = scrapy.Request(url, callback=self.parse, meta={'username': a})
            pages.append(page)
        return pages

    def parse(self, response):
        match = re.search(r'"email":"(.*?)"', response.body_as_unicode())
        if match:
            yield {
                'username': response.meta['username'],
                'email': match.group(1)
            }
