# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from dmoz.items import DmozItem


class DmozspiderSpider(CrawlSpider):
    name = 'dmozspider'
    allowed_domains = ['www.dmoz.org']
    start_urls = [
        'http://www.dmoz.org/Computers/Computer_Science/',
    ]

    rules = (
        Rule(LinkExtractor(allow=r'org/Computers/Computer_Science/', restrict_xpaths=("//ul[@class='directory dir-col']", )),
             callback='parse_cs_item', follow=True),
    )

    def parse_cs_item(self, response):
        directory_url = response.xpath('//ul[@class="directory-url"]/li')
        if not directory_url:
            return
        for li in directory_url:
            csitem = DmozItem()
            csitem['category'] = 'Computer Science'
            csitem['url'] = li.xpath('a/@href').extract()[0]
            csitem['subcategory'] = response.xpath('//li[@class="last"]/strong/text()').extract()[0]
            csitem['title'] = li.xpath('a/text()').extract()[0]
            csitem['description'] = li.xpath('a/following-sibling::node()').extract()[0].strip()
            yield csitem
