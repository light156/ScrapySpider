# -*- coding: utf-8 -*-
import sys
import os

import scrapy
from scrapy import Request
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from Spider.items import LegacyItem, LegacyItemLoader
from Spider.utils.process import match_keyword


class LegacySpider(scrapy.Spider):
	name = 'Legacy'
	allowed_domains = ['www.ucl.ac.uk']
	start_urls = ['https://www.ucl.ac.uk/lbs/commercial/']

	def parse(self, response):
		#yield Request(url='https://www.ucl.ac.uk/lbs/commercial/view/2146006065',
		#			  meta={'person_id': 'https://www.ucl.ac.uk/lbs/commercial/view/2146006065', 'name': "name",
		#					'website_order':462}, callback=self.parse_commercial)
		driver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver')
		browser = webdriver.Chrome(executable_path=driver_path)
		browser.get("https://www.ucl.ac.uk/lbs/commercial/")
		person_id, name, temp_id, temp_name = "", "", "", ""
		website_order = 0
		while True:
			try:
				info_list = browser.find_elements_by_css_selector('.full tr')
				for info in info_list:
					try:
						person = info.find_element_by_css_selector('.four.columns.small a')
					except NoSuchElementException:
						person_id, name = temp_id, temp_name
					else:
						person_id, name = person.get_property("href"), person.text
						temp_id, temp_name = person_id, name
	
					commercial = info.find_element_by_css_selector('.two.columns.ta-right a')
					commercial_url = commercial.get_property("href")
					website_order += 1
					yield Request(url=commercial_url, dont_filter=True, callback=self.parse_commercial,
								  meta={'website_order': website_order, 'person_id': person_id, 'name': name})

				next_button = browser.find_element_by_xpath("//input[contains(@value, 'Next')]")
			except NoSuchElementException:
				break
			else:
				next_button.click()


	def parse_commercial(self, response):
		item_loader = LegacyItemLoader(item=LegacyItem(), response=response)

		meta_dict = {key: response.meta[key] for key in ['website_order', 'person_id', 'name']}
		item_loader.add_value(None, meta_dict)
		item_loader.add_value("comm_id", response.url)
		comm_type = response.css(".indtype.clearfix span::text").extract_first("")
		item_loader.add_value("comm_type", comm_type)

		if comm_type == "Railway Investment":
			item_loader.add_css("railway_title", ".extras strong::text")
			item_loader.add_css("railway_code", ".extras span:nth-child(2) ::text")
			item_loader.add_css("railway_amount", ".extras .highlight::text")
			item_loader.add_value(None, {"business":"railway", "econ_sector":"railway"})
		else:
			if comm_type != "General Investment":
				item_loader.add_css("firm_name", ".legacy-heading a::text")
				item_loader.add_css("firm_id", ".legacy-heading a::attr(href)")
			item_loader.add_css("business", ".extras strong::text")
			item_loader.add_css("econ_sector", ".extras::text")

			further_info_str = response.xpath("//h2[text()='Further Information']/"
											  "following-sibling::table[1]").extract_first("")

			values = match_keyword(further_info_str, "Partner Share", "Shareholder\?", "Share Amount")
			item_loader.add_value(None, dict(zip(("partner_share", "shareholder", "share_amount"), values)))

			if comm_type == "Partnership Role":
				item_loader.add_css("partner_role", ".legacy-heading em::text")
			elif comm_type == "Company Role":
				item_loader.add_css("management_role", ".legacy-heading em::text")

		legacy_item = item_loader.load_item()
		yield legacy_item
