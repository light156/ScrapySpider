# -*- coding: utf-8 -*-
import os

import scrapy
from scrapy import Request

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

from Spider.items import PersonItem, PersonItemLoader
from Spider.items import ClaimItem, ClaimItemLoader
from Spider.utils.process import *

class ClaimSpider(scrapy.Spider):
    name = 'Claim'
    allowed_domains = ['www.ucl.ac.uk']
    start_urls = ['https://www.ucl.ac.uk/lbs/search/']

    def parse(self, response):
        #yield Request(url="https://www.ucl.ac.uk/lbs/person/view/27140", meta={"sex": "F"}, callback=self.parse_person)
        #yield Request(url="https://www.ucl.ac.uk/lbs/person/view/9058", callback=self.parse_person, dont_filter=True,
        #              meta={"sex": "NK", "website_order": 60, "claim_role": "",
        #                    "claim_url": "https://www.ucl.ac.uk/lbs/claim/view/8980", "claims": 1}
        browser = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"))

        browser.get("https://www.ucl.ac.uk/lbs/search/")
        Select(browser.find_element_by_id("input_type")).select_by_index(1)
        # select_sex = browser.find_element_by_id("input_sex")
        # Select(select_sex).select_by_index(i)
        # sex = select_sex.find_elements_by_tag_name("option")[i].get_attribute("value")
        browser.find_element_by_id("submit").click()

        while True:
            try:
                info_list = browser.find_elements_by_css_selector('.full td')
                for info in info_list:
                    person_url = info.find_element_by_css_selector("strong a").get_property("href")
                    claim_role_list = [claim_role.text for claim_role in
                                       info.find_elements_by_css_selector(".four.columns.clear span")]
                    claim_url_list = [claim_url.get_property("href") for claim_url in
                                      info.find_elements_by_css_selector(".twelve.columns.small a")]
                    yield Request(url=person_url, callback=self.parse_person,
                                  meta={"claim_role_list": claim_role_list, "claim_url_list": claim_url_list})
                next_button = browser.find_element_by_xpath("//input[contains(@value, 'Next')]")
            except NoSuchElementException:
                break
            else:
                next_button.click()


    def parse_person(self, response):
        person_dict = {"name": response.css('.twelve.columns.main .name::text').extract_first(""), "person_id": response.url}
        # birth date & death date
        person_date_str = response.css('.date').extract_first("")
        person_dict["birth_date"], person_dict["death_date"] = process_person_date_str(person_date_str)
        # further information
        further_info_str = response.xpath(
            "//h2[text()='Further Information']/following-sibling::table[1]").extract_first("")
        if further_info_str:
            values = match_keyword(further_info_str, "Absentee", "Maiden Name", "Spouse", "Wealth at death")
            values_dict = dict(zip(("absentee", "maiden_name", "spouse", "wealth_at_death"), values))
            person_dict = {**person_dict, **values_dict}
        # generate items
        claim_role_list, claim_url_list = response.meta["claim_role_list"], response.meta["claim_url_list"]
        person_dict["claims"] = len(claim_role_list)
        for order, (claim_role, claim_url) in enumerate(zip(claim_role_list, claim_url_list)):
            item_loader = PersonItemLoader(item=PersonItem(), response=response)
            item_loader.add_value(None, person_dict)
            item_loader.add_value(None, {"claim_role": claim_role, "claim_role_note": claim_role,
                                         "claim_id": claim_url, "website_order": response.url+"-%02d"%(order+1)})
            person_item = item_loader.load_item()
            yield person_item
            yield Request(url=claim_url, callback=self.parse_claim)


    def parse_claim(self, response):
        item_loader = ClaimItemLoader(item=ClaimItem(), response=response)
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
