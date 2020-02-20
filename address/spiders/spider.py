# -*- coding: utf-8 -*-
import scrapy
import csv
from address.items import AddressItem
from scrapy.loader import ItemLoader
from scrapy import Request


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['www.ucl.ac.uk']
    start_urls = ['https://www.ucl.ac.uk/lbs/']

    def parse(self, response):
        rf = open('claim_person.csv', 'r')
        reader = csv.reader(rf)
        for person_id in reader:
            url = "https://www.ucl.ac.uk/lbs/person/view/%s" % person_id[0]
            yield Request(url=url, meta={"person_id":person_id[0]}, callback=self.parse_item)

    def parse_item(self, response):
        addresses = response.xpath("//*[@id='addresses']/following-sibling::table[1]//*[@class='nine columns small']/text()").extract()
        for address in addresses:
            item = AddressItem()
            item["person_id"] = response.meta["person_id"]
            item["address"] = address
            yield item
