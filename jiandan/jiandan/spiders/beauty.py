# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..utils import jandan_load_img
from ..items import BeautyItem
import re

class BeautySpider(CrawlSpider):
    name = 'beauty'
    allowed_domains = ['jandan.net']
    start_urls = ['http://jandan.net/ooxx']
    salt = ''   #煎蛋用于解密连接的salt
    pic_path_pattern = r'(http:\/\/.*\.sinaimg\.cn\/)(\w+)(\/.+)'

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'//jandan.net/ooxx/page-\d+#comments'), follow=True, callback='parse_page'),
    )

    pic_link_extractor = LinkExtractor(allow=r'//wx3.sinaimg.cn/large/')

    def parse_start_url(self, response):
        js_url_list = re.findall(r'.*<script\ssrc=\"\/\/(cdn.jandan.net\/static\/min.*?)\"><\/script>.*',response.text)
        print(js_url_list)
        js_url = "http://" + js_url_list[-1]
        yield scrapy.Request(url=js_url, callback=self.parse_js, priority=100)
        return []

    def parse_js(self, response):
        text = response.text
        pattern = r'.*jd\w+\(e,\"(\w+)\".*'
        search_result = re.search(pattern, text)
        self.salt = search_result.group(1)   

    def parse_page(self, response):
        img_hash_list = response.css("span.img-hash::text").extract()

        for img_hash in img_hash_list:
            img_url = jandan_load_img(img_hash, self.salt)
            img_url = 'http:' + img_url
            pic_path = re.match(self.pic_path_pattern, img_url)
            large_pic_url = pic_path.group(1) + 'large' + pic_path.group(3)

            yield BeautyItem(image_urls = [large_pic_url])
