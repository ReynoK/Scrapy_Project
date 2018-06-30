# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from faker import Faker                 #引入Faker，pip install faker下载
from scrapy.http import HtmlResponse
import random
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
        self.user_agent = self.faker.user_agent()       #获得随机user_agent
        print(self.user_agent)
        request.headers.setdefault(b'User-Agent', self.user_agent)

class ChromeDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        spider.browser.get(request.url)
        for i in range(5):
            spider.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        return HtmlResponse(url = spider.browser.current_url, body = spider.browser.page_source, encoding = 'utf8', request = request)

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
