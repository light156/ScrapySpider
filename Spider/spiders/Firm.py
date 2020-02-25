# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy import Request, FormRequest

from Spider.items import FirmItem


class FirmSpider(scrapy.Spider):
	name = 'Firm'
	allowed_domains = ['www.ucl.ac.uk']
	start_urls = ['https://www.ucl.ac.uk/lbs/firms/']

	formdata = {}
	total_num = 0

	def parse(self, response):
		#获取页面上有多少条
		total_num_str = response.css(".result-title em::text").extract_first()
		total_num_str = re.match("\[(.*?) Rec.*", total_num_str).group(1)
		self.total_num = int(total_num_str.replace(",", ""))
		print(self.total_num)
		yield Request(url=response.url, meta={'total_order': 0}, callback=self.parse_item)

	def parse_item(self, response):
		total_order = response.meta.get('total_order')  #看之前爬到了多少条（翻了几页）
		info_list = response.css('.full td')
		order = 0

		for info in info_list:
			firm_id = info.css('.four.columns.small strong a::attr(href)').extract_first()
			firm_id = re.match(".*view/(.*)", firm_id).group(1)
			firm_name = info.css('.four.columns.small strong a::text').extract_first()

			addr_years = info.css('.four.columns.ta-right.small.clear')
			if addr_years:
				for addr_year in addr_years:
					year = addr_year.css('em::text').extract_first("")
					addr = addr_year.xpath("following-sibling::div[1]/text()").extract_first("")
					addr = addr.replace("\r\n", '')

					firm_item = FirmItem()
					firm_item['website_order'] = total_order+order+1
					firm_item['firm_id'] = firm_id
					firm_item['firm_name'] = firm_name
					firm_item['year'] = year

					if addr.startswith(" , "):
						match_re = re.match("^ , (.*) \[.*\]$", addr)
						address_st, address_city = "", match_re.group(1)
					else:
						match_re = re.match("^ (.*), (.*?) \[.*\]$", addr)
						address_st, address_city = match_re.groups()

					firm_item['address_st'] = address_st
					firm_item['address_city'] = address_city

					yield firm_item
					order += 1
			else:
				firm_item = FirmItem()
				firm_item['website_order'] = total_order + order + 1
				firm_item['firm_id'] = firm_id
				firm_item['firm_name'] = firm_name
				yield firm_item
				order += 1

		## 给服务器发下一个post请求
		if total_order < self.total_num-50:
			self.formdata['start'] = str(total_order)
			if total_order > self.total_num-100:
				self.formdata["submit"] = 'Next %d →' % (self.total_num-total_order-50)
			else:
				self.formdata["submit"] = 'Next 50 →'
			total_order += 50
			print(total_order)
			yield FormRequest(url=response.url, meta={'total_order': total_order}, formdata=self.formdata, callback=self.parse_item)
