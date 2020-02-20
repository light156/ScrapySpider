# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv


class AddressPipeline(object):
    def __init__(self):
        self.wf = open('address.csv', 'w')
        self.writer = csv.writer(self.wf)

    def process_item(self, item, spider):
        lines = self.writer.writerow([item["person_id"], item["address"]])
        self.wf.flush()
        return item

    def spider_closed(self, spider):
        self.wf.close()
