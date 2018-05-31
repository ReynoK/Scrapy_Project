# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.exceptions import NotConfigured
from collections import defaultdict
import random
from urllib.parse import urlparse
from faker import Faker

class RandomHttpProxyMiddleware(object):


    def __init__(self, auth_encoding='latin-1', proxy_list = None):
        if not proxy_list:
            raise NotConfigured
        self.proxies = defaultdict(list)
        for proxy in proxy_list:
            parse = urlparse(proxy)
            self.proxies[parse.scheme].append(proxy)

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.get('HTTP_PROXY_LIST'):
            raise NotConfigured

        http_proxy_list = crawler.settings.get('HTTP_PROXY_LIST')
        auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING', 'latin-1')

        return cls(auth_encoding, http_proxy_list)
    def process_request(self, request, spider):
        self._set_proxy(request, 'http')

    def _set_proxy(self, request, scheme):
        proxy = random.choice(self.proxies[scheme])
        request.meta['proxy'] = proxy


class RandomUserAgentMiddleware(object):

    def __init__(self):
        self.faker = Faker(local='zh_CN')
        self.user_agent = ''

    @classmethod
    def from_crawler(cls, crawler):
        o = cls()
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        self.user_agent = getattr(spider, 'user_agent',self.user_agent)

    def process_request(self, request, spider):
        self.user_agent = self.faker.user_agent()
        request.headers.setdefault(b'User-Agent', self.user_agent)
