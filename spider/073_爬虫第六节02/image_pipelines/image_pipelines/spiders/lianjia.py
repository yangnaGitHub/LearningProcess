# -*- coding: utf-8 -*-
import json

from scrapy.contrib.spiders import CrawlSpider, Rule
from ..items import ImagePipelinesItem
from scrapy.selector import Selector
from ..items import TaoTuLinkItem
from scrapy.linkextractors import LinkExtractor
import scrapy
import re

next_page = u"下一页"


class LianJiaSpider(CrawlSpider):
    name = "lianjia"
    allowed_domains = ["lianjia.com"]
    start_urls = [
        "http://su.lianjia.com/ershoufang/gaoxin1"
        #"http://bj.lianjia.com/ershoufang/rs%E7%87%95%E9%83%8A/"
    ]
    
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

    def parse_price(self, response):
        sel = Selector(response)
        for items in sel.css(".info"):
            try:
                #house_location = items.css(".houseInfo").xpath("./a/text()").extract()[0]
                #houseInfo = items.css(".houseInfo").xpath("text()").extract()[0]
                #total_price = items.css(".totalPrice").xpath("./span/text()").extract()[0]
                #unit_price = items.css(".unitPrice").xpath("./span/text()").extract()[0]
                #unit_price = int(re.findall(r'[\d|.]+', unit_price)[0])
                #house_size = float(re.findall(r'[\d|.]+', houseInfo.split("|")[2])[0])
                house_location = items.css(".row2-text").xpath("./a/span/text()").extract()[0]
                house_size = items.css(".row1-text").xpath("./text()").extract()[1].replace('\n', '').replace('\t', '').replace(' ', '').replace('|', ' ')#[0]
                total_price = items.css(".price-item").xpath("./span/text()").extract()[0]
                unit_price = items.css(".minor").xpath("./text()").extract()[0].replace('\t', '').replace('\n', '')
            except Exception as exc:
                pass
            else:
                print house_location, house_size, u"总价", total_price, unit_price

    def parse(self, response):
        sel = Selector(response)

        #page_data = sel.css(".page-box div::attr(page-data)").extract()[0]
        #page_url = "%s" % sel.css(".page-box div::attr(page-url)").extract()[0]
        #page_data = json.loads(page_data)
        #page_count = int(page_data.get("totalPage", 1))
        #for i in range(1, page_count+1):
        #    tmp = page_url.replace("{page}", str(i))
        #    next_request = response.urljoin(tmp)
        #    yield scrapy.Request(next_request, callback=self.parse_price)
        page_text = sel.css(".c-pagination a::attr(gahref)").extract()
        page_href = sel.css(".c-pagination a::attr(href)").extract()
        
        for index in range(len(page_text)):
            if page_text[index] == u"results_totalpage":
                TotalPageUrl = page_href[index]
        TotalPageList = re.findall('\d', TotalPageUrl)
        TotalPage = 0
        for index in range(len(TotalPageList) - 1):
            TotalPage = TotalPage + int(TotalPageList[index + 1]) * (10**(len(TotalPageList) - 2 - index))
        for i in range(1, TotalPage + 1):
            tmp = "/ershoufang/gaoxin1/d{page}".replace("{page}", str(i))
            #tmp = "/ershoufang/gaoxin1/d%d" % i
            next_request = response.urljoin(tmp)
            yield scrapy.Request(next_request, callback=self.parse_price)
        
