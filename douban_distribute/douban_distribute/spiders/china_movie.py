# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy_redis.spiders import RedisSpider

class ChinaMovieSpider(RedisSpider):
    name = 'china_movie'
    allowed_domains = ['movie.douban.com']
    #start_urls = ['http://movie.douban.com/']

    url_pattern = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E5%8D%8E%E8%AF%AD&sort=recommend&page_limit=20&page_start={start_row}'
    page_row = 20
    start_row = 0

    def parse_page(self, response):
        print(response.body)
        content = json.loads(response.body)
        if len(content['subjects']) == 0:
            return
        start_row = response.meta['start_row'] + self.page_row
        url = self.url_pattern.format(start_row = start_row)
        print(url)
        meta = dict(start_row = start_row)
        yield scrapy.Request(url, callback = self.parse_page, meta = meta)

        for row in content['subjects']:
            yield scrapy.Request(row['url'], meta = row, callback = self.parse_detail)

    def parse(self, response):
        start_row = 0
        meta = dict(start_row = start_row)
        url = self.url_pattern.format(start_row = start_row)
        print(url)
        yield scrapy.Request(url, meta = meta, callback = self.parse_page)

    def parse_detail(self, response):
        actor_list = response.css('span.actor span.attrs a::text').extract()

        response.meta['actor'] = '/'.join(actor_list)

        yield response.meta
