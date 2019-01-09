from scrapy.spiders import XMLFeedSpider

class MySpider(XMLFeedSpider):
    name = 'mfwsitemap'
    allowed_domains = ['mafengwo.cn']
    start_urls = ['http://www.mafengwo.cn/sitemapIndex.xml']
    iterator = 'html'
    itertag = 'sitemap'

    def parse_node(self, response, node):
        item = {}
        item['loc'] = node.xpath('loc').extract()
        item['lastmod'] = node.xpath('lastmod').extract()
        return item