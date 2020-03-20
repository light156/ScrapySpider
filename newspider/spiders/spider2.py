# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib.parse import urljoin
from newspider.items import CfmItem, MyItemLoader
from scrapy.loader import ItemLoader

class Spider2Spider(scrapy.Spider):
    name = 'spider2'
    allowed_domains = ['cfmsurvey.org']
    start_urls = ['https://cfmsurvey.org/surveys']

    def parse(self, response):
        url_list = response.css("h2 a::attr(href)").extract()
        for url in url_list[:2]:
            yield Request(url=urljoin(response.url, url), callback=self.parse_question)

    def parse_question(self, response):
        question_list = response.css(".views-accordion-how_the_experts_responded-block-header")
        table_list = response.css("table tbody")
        for question, table in zip(question_list, table_list):
            people = table.css("tr")
            for person in people:
                item_loader = MyItemLoader(item=CfmItem(), selector=person)
                item_loader.add_value("url", response.url)
                item_loader.add_value("question", question.css("::text").extract())
                item_loader.add_css("name", ".username::text")
                item_loader.add_css("univ", ".views-field-nothing::text")
                item_loader.add_css("answer", ".views-field-field-opinion::text")
                item_loader.add_css("confidence", ".views-field-field-expertise::text")
                item_loader.add_css("comment", ".comment-text div::text")
                question_item = item_loader.load_item()
                yield question_item
