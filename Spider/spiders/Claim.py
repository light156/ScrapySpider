# -*- coding: utf-8 -*-
import os
import logging
from urllib.parse import urljoin

import scrapy
from scrapy import Request, FormRequest
from scrapy.utils.log import configure_logging

<<<<<<< HEAD
from Spider.items import ClaimRecordItem, PersonItem, ClaimItem
from Spider.items import MyItemLoader
=======
from Spider.items import ClaimRecordItem, ClaimRecordItemLoader
from Spider.items import PersonItem, PersonItemLoader
from Spider.items import ClaimItem, ClaimItemLoader
>>>>>>> 22c974afc008589b7f80f420f7ebf6e0d5794033
from Spider.utils.process import *

class ClaimSpider(scrapy.Spider):
    name = 'Claim'
    allowed_domains = ['www.ucl.ac.uk']
    start_urls = ['https://www.ucl.ac.uk/lbs/search/']
    formdata = {'start': '0', 'input_type': 'CB', 'input_sex': '', 'submit': 'View Records'} #'Next 50 →' 'View Records'
    total_num = 0

    def start_requests(self):
        yield FormRequest(url='https://www.ucl.ac.uk/lbs/search/', formdata=self.formdata, callback=self.parse)

    def parse(self, response):
        total_num_str = response.css(".result-title em::text").extract_first()
        total_num_str = re.match("\[(.*?) Rec.*", total_num_str).group(1)
        self.total_num = int(total_num_str.replace(",", ""))
        print(self.total_num)
        yield FormRequest(url=response.url, meta={'total_order': 0}, formdata=self.formdata,
                          callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        total_order = response.meta.get('total_order')

        claim_role_node_list = response.css('.full .four.columns.clear')
        claim_url_list = response.css('.full .twelve.columns.small a::attr(href)').extract()
        for order, (claim_role_node, claim_url) in enumerate(zip(claim_role_node_list, claim_url_list)):
            claim_role = claim_role_node.css("span::text").extract_first()
            parent = claim_role_node.xpath("..")
            claims = len(parent.css(".four.columns.clear"))
            person_url = parent.css("strong a::attr(href)").extract_first()

<<<<<<< HEAD
            item_loader = MyItemLoader(item=ClaimRecordItem())
=======
            item_loader = ClaimRecordItemLoader(item=ClaimRecordItem())
>>>>>>> 22c974afc008589b7f80f420f7ebf6e0d5794033
            item_loader.add_value(None, {"website_order": total_order+order+1, "person_id": person_url,
                                         "claim_id": claim_url, "claim_role": claim_role, "claim_role_note": claim_role})
            record_item = item_loader.load_item()

            yield record_item
            yield Request(url=urljoin(response.url, person_url), meta={'claims': claims}, callback=self.parse_person)
            try:
                re.match(".*view/(.+)", claim_url).group(1)
                yield Request(url=urljoin(response.url, claim_url), callback=self.parse_claim)
            except AttributeError:
                print("For Item %d, Claim ID doesn't exist."%(total_order+order+1))

        if total_order < self.total_num - 50:
            self.formdata['start'] = str(total_order)
            if total_order > self.total_num - 100:
                self.formdata["submit"] = 'Next %d →' % (self.total_num - total_order - 50)
            else:
                self.formdata["submit"] = 'Next 50 →'
            total_order += 50
            print(total_order)
            yield FormRequest(url=response.url, meta={'total_order': total_order},
                              formdata=self.formdata, callback=self.parse_item)

#logger = logging.getLogger(configure_logging())
#logger.setLevel(logging.INFO)

    def parse_person(self, response):
<<<<<<< HEAD
        item_loader = MyItemLoader(item=PersonItem(), response=response)
=======
        item_loader = PersonItemLoader(item=PersonItem(), response=response)
>>>>>>> 22c974afc008589b7f80f420f7ebf6e0d5794033
        item_loader.add_value("person_id", response.url)
        item_loader.add_css("name", ".twelve.columns.main .name::text")
        item_loader.add_value("claims", response.meta["claims"])
        # birth date & death date
        item_loader.add_value(None, process_person_date_dict(response.css('.date').extract_first("")))
        # further information
        further_info_str = response.xpath(
            "//h2[text()='Further Information']/following-sibling::table[1]").extract_first("")
        if further_info_str:
            values = match_keyword(further_info_str, "Absentee", "Maiden Name", "Spouse", "Wealth at death")
            values_dict = dict(zip(("absentee", "maiden_name", "spouse", "wealth_at_death"), values))
            item_loader.add_value(None, values_dict)

        person_item = item_loader.load_item()
        yield person_item


    def parse_claim(self, response):
<<<<<<< HEAD
        item_loader = MyItemLoader(item=ClaimItem(), response=response)
=======
        item_loader = ClaimItemLoader(item=ClaimItem(), response=response)
>>>>>>> 22c974afc008589b7f80f420f7ebf6e0d5794033
        item_loader.add_value("claim_id", response.url)
        # claim date, enslaved, money, money_s, money_d
        claim_str = response.css('.date').extract_first()
        values = process_claim_str(claim_str)
        item_loader.add_value(None, dict(zip(("claim_date", "enslaved", "money", "money_s", "money_d"), values)))
        # further information
        further_info_str = response.xpath("//h2[text()='Further Information']/"
                                          "following-sibling::table[1]").extract_first("")
        values = match_keyword(further_info_str, "Colony", "Parish", "Claim No.", "Estate")
        item_loader.add_value(None, dict(zip(("colony", "parish", "claim_no", "estate"), values)))
        # contested
        if match_keyword(further_info_str, "Contested"):
            item_loader.add_value("contested", "Yes")
        elif match_keyword(further_info_str, "Uncontested"):
            item_loader.add_value("contested", "No")

        claim_item = item_loader.load_item()
        yield claim_item
