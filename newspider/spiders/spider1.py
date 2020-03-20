# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.cmdline import execute
from newspider.items import QuestionItem, MyItemLoader

class Spider1Spider(scrapy.Spider):
    name = 'spider1'
    allowed_domains = ['www.igmchicago.org']
    #start_urls = ['http://www.igmchicago.org/igm-economic-experts-panel']
    start_urls = ['http://www.igmchicago.org/european-economic-experts-panel']

    def parse(self, response):
        url_list = response.css("h2 a::attr(href)").extract()
        for url in url_list:
            yield Request(url=url, callback=self.parse_question)

    def parse_question(self, response):
        time = response.css("h6::text").extract()
        keyword = response.css("h2::text").extract()
        question_list = response.css(".surveyQuestion")
        table_list = response.css("table")
        for question, table in zip(question_list, table_list):
            people = table.css(".parent-row")
            for person in people:
                item_loader = MyItemLoader(item=QuestionItem(), selector=person)
                item_loader.add_value("time", time)
                item_loader.add_value("url", response.url)
                item_loader.add_value("keyword", keyword)
                item_loader.add_value("question", question.css("*::text").extract())
                item_loader.add_css("name", ".response-name a::text")
                item_loader.add_css("univ", "td:nth-child(2)::text")
                item_loader.add_css("vote", "span::text")
                item_loader.add_css("confidence", ".confCell::text")
                item_loader.add_css("comment", ".gridComment::text")
                question_item = item_loader.load_item()
                yield(question_item)
