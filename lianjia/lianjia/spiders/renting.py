# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.linkextractors import LinkExtractor
from ..items import RentingHouse
class RentingSpider(scrapy.Spider):
    name = 'renting'
    allowed_domains = ['sz.lianjia.com']
    start_urls = ['http://sz.lianjia.com/zufang/']
    page_pattern = "http://sz.lianjia.com/zufang/pg{page}/"
    detail_link_extractor = LinkExtractor(allow=r'https://sz.lianjia.com/zufang/\d+.html')
    
    detail_map = {
        '面积' : 'area',
        '房屋户型' : 'house_type',
        '楼层' : 'layer',
        '地铁' : 'subway',
        '位置' : 'position',
    }
    
    def parse(self, response):
        page_data = response.css('div.page-box::attr(page-data)').extract_first()
        page_data = json.loads(page_data)
        total_page = page_data['totalPage']
        for page in range(1,total_page + 1):
            url = self.page_pattern.format(page=page)
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        links = self.detail_link_extractor.extract_links(response)

        if links:
            for link in links:
                yield scrapy.Request(url=link.url, callback=self.parse_detail)
    
    def parse_detail(self, response):
        name = response.css('h1.main::text').extract_first()
        price = response.css('div.price span.total::text').extract_first()
        unit = response.css('div.price span.unit span::text').extract_first()
        
        if price is None:
            price = ''
        
        if unit is not None:
            price = price + ' ' + unit

        info = {}
        info_selector_list = response.css('div.zf-room p')
        for info_selector in info_selector_list:
            key_name = info_selector.css('i::text').extract_first().rstrip('：')
            if key_name in self.detail_map.keys():
                if key_name == '位置':
                    info[self.detail_map[key_name]] = '-'.join(info_selector.css('p a::text').extract())
                else:
                    info[self.detail_map[key_name]] = info_selector.css('p::text').extract_first().strip()

        manager = response.css('div.brokerName a.name::text').extract_first()

        item = RentingHouse(name=name, price=price, manager=manager, **info)
        return item
