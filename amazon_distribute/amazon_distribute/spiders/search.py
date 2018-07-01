# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy_redis.spiders import RedisSpider
from scrapy.linkextractors import LinkExtractor
from selenium import webdriver

class SearchSpider(scrapy.Spider):
    name = 'search'
    start_urls = ['https://www.amazon.cn/s/ref=nb_sb_noss?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&url=search-alias%3Daps&field-keywords=python&rh=i%3Aaps%2Ck%3Apython']    

    def parse(self, response):
        print(response.body)
        le = LinkExtractor(restrict_css='div.s-item-container a.s-access-detail-page')
        meta = {'refer':response.url}
        for link in le.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_detail, meta = meta)
        
        le = LinkExtractor(restrict_css='a.pagnNext')
        links = le.extract_links(response)
        if links:
            next_url = links[0].url 
            print(next_url)
            yield scrapy.Request(next_url, callback=self.parse)
    def parse_detail(self, response):
        info = {}
        for row in response.css('div.content ul li'):
            key_ = row.css('li b::text').extract_first()
            value_ = row.css('li::text').extract_first()
            if value_ is None:
                value_ = row.css('li a::text').extract_first()
            value_ = value_.strip() if value_ is not None else '' 
            if key_:
                info[key_.strip()] = value_
        info['url'] = response.url
        info.update(response.meta)
        yield info


