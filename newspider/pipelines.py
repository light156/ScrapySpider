# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
from scrapy.exporters import CsvItemExporter

class NewspiderPipeline(object):
    def __init__(self):
        self.file = open('data.csv', mode='wb')
        self.fields_to_export = ['time', 'url', 'keyword', 'question', 'name', 'univ', 'vote', 'confidence', 'comment']
        #self.file = open('data_cfm.csv', mode='wb')
        #self.fields_to_export = ['url', 'question', 'name', 'univ', 'answer', 'confidence', 'comment']
        self.exporter = CsvItemExporter(self.file, fields_to_export=self.fields_to_export, encoding='utf-8',  delimiter='\t')

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def spider_closed(self, spider):
        self.file.close()

