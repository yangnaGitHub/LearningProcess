# -*- coding: utf-8 -*-
import json
import scrapy
from ..items import ImagePipelinesItem
from scrapy.selector import Selector
from ..items import TaoTuLinkItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

next_page = u"下一页"


class BaiduSpider(CrawlSpider):
    name = 'baidu'
    allowed_domains = ['baidu.com', "bdimg.com"]
    start_urls = [
        "http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%E8%83%8C%E5%8C%85&ct=201326592&v=flip"
    ]

    #rules = (
    #    Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    #)

    def parse_image(self, response):
        img_item = ImagePipelinesItem()
        sel = Selector(response)
        image_urls = []
        for img in sel.xpath('(//div)[@id="big-pic"]/p/a/img/@src'):
            image_urls.append(img.extract())

        img_item["image_urls"] = image_urls
        yield img_item

        try:
            next_request = sel.xpath("//a[text()='%s']/@href" % next_page).extract()[0]
        except Exception:
            pass
        else:
            if next_request is not None:
                next_request = response.urljoin(next_request)
                yield scrapy.Request(next_request, callback=self.parse_image)

    def parse(self, response):
        img_item = ImagePipelinesItem()
        sel = Selector(response)
        print sel.xpath("//title/text()").extract()[0]
        p = re.compile('"data":\[.*\]')
        result = p.search(response.body)
        tmp = result.group(0).split('"data":')[1]
        img_list = json.loads(tmp)
        img_urls = []
        for i in img_list:
            print i.get("thumbURL", "")
            img_url = i.get("thumbURL", "")
            if img_url:
                img_urls.append(img_url)

        img_item["image_urls"] = img_urls
        yield img_item
        #i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        #return i
