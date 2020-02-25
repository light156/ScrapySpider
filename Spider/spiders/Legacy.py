# -*- coding: utf-8 -*-
import sys
import os
import re

import scrapy
from urllib.parse import urljoin
from scrapy import Request, FormRequest

<<<<<<< HEAD
from Spider.items import LegacyItem, MyItemLoader
=======
<<<<<<< HEAD
from Spider.items import LegacyItem, MyItemLoader
=======
from Spider.items import LegacyItem, LegacyItemLoader
>>>>>>> 22c974afc008589b7f80f420f7ebf6e0d5794033
>>>>>>> 2b4d1433e506a14c377ce697c0cfa9c2ae9c9c2a
from Spider.utils.process import match_keyword


class LegacySpider(scrapy.Spider):
	name = 'Legacy'
	allowed_domains = ['www.ucl.ac.uk']
	start_urls = ['https://www.ucl.ac.uk/lbs/commercial/']

	formdata = {'input_roles': 'on', 'input_directorships': 'on', 'input_firms': 'on',
				'input_railways': 'on', 'input_investments': 'on'}
	total_num = 0

	def parse(self, response):
		total_num_str = response.css(".result-title em::text").extract_first()
		total_num_str = re.match("\[(.*?) Rec.*", total_num_str).group(1)
		self.total_num = int(total_num_str.replace(",", ""))
		print(self.total_num)
		yield Request(url=response.url, meta={'total_order': 0}, callback=self.parse_item)

	def parse_item(self, response):
		total_order = response.meta.get('total_order')

		person_id, name, temp_id, temp_name = "", "", "", ""
		info_list = response.css('.full tr')
		for order, info in enumerate(info_list):

			person = info.css('.four.columns.small a')
			if person:
				person_id, name = person.css("::attr(href)").extract_first(), person.css("::text").extract_first()
				temp_id, temp_name = person_id, name
			else:
				person_id, name = temp_id, temp_name
			comm_url = info.css('.two.columns.ta-right a::attr(href)').extract_first()

			meta_dict = {'website_order': total_order+order+1, 'person_id': person_id, 'name': name, 'comm_id': comm_url}
			yield Request(url=urljoin(response.url, comm_url), meta=meta_dict, callback=self.parse_commercial)

		if total_order < self.total_num-50:
			self.formdata['start'] = str(total_order)
			if total_order > self.total_num-100:
				self.formdata["submit"] = 'Next %d →' % (self.total_num-total_order-50)
			else:
				self.formdata["submit"] = 'Next 50 →'
			total_order += 50
			print(total_order)
			yield FormRequest(url=response.url, meta={'total_order': total_order},
							  formdata=self.formdata, callback=self.parse_item)


	def parse_commercial(self, response):
<<<<<<< HEAD
		item_loader = MyItemLoader(item=LegacyItem(), response=response)
=======
<<<<<<< HEAD
		item_loader = MyItemLoader(item=LegacyItem(), response=response)
=======
		item_loader = LegacyItemLoader(item=LegacyItem(), response=response)
>>>>>>> 22c974afc008589b7f80f420f7ebf6e0d5794033
>>>>>>> 2b4d1433e506a14c377ce697c0cfa9c2ae9c9c2a
		meta_dict = {key: response.meta[key] for key in ['website_order', 'person_id', 'name', 'comm_id']}
		item_loader. add_value(None, meta_dict)

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
