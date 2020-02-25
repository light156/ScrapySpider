# -*- coding: utf-8 -*-
from scrapy.exporters import JsonLinesItemExporter
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import pymysql

MYSQL_HOST = "127.0.0.1"
MYSQL_DBNAME = "claim_spider"
MYSQL_USER = "root"
MYSQL_PASSWORD = "takashi"


class SpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonExporterPipeline(object):
    def __init__(self):
        self.file = open('data.json', 'wb')
        self.exporter = JsonLinesItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        conn = pymysql.connect(host="127.0.0.1", user='root', password='takashi', db="claim_spider", charset='utf8')
        cursor = conn.cursor()
        cursor.execute("TRUNCATE TABLE firm_table")
        #cursor.execute("TRUNCATE TABLE claim_table")
        #cursor.execute("TRUNCATE TABLE claim_record")
        #cursor.execute("TRUNCATE TABLE claim_person")
        conn.commit()
        cursor.close()
        conn.close()
        self.dbpool = dbpool


    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(selfs, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)
