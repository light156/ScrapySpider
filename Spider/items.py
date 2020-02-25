# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Identity, Join


class ClaimRecordItem(scrapy.Item):
    website_order = scrapy.Field()
    person_id = scrapy.Field(
        input_processor=lambda s: re.match(".*view/(.*)", s[0]).group(1)
    )
    claim_id = scrapy.Field(
        input_processor=lambda s: re.match(".*view/(.*)", s[0]).group(1)
    )
    claim_role = scrapy.Field(
        input_processor=lambda s: re.match("(.*?) \[.*", s[0]+' []').group(1)
    )
    claim_role_note = scrapy.Field(
        input_processor=lambda s: re.match(".*?\[(.*?)\].*", s[0]+' []').group(1)
    )

    def get_insert_sql(self):
        insert_sql = """
            insert into claim_record(website_order, person_id, claim_id, claim_role, claim_role_note) 
            values (%s, %s, %s, %s, %s)
        """
        params = (self.get("website_order", ""), self.get("person_id", ""), self.get("claim_id", ""),
                  self.get("claim_role", ""), self.get("claim_role_note", ""))
        return insert_sql, params


class PersonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sex = scrapy.Field()
    person_id = scrapy.Field(
        input_processor=lambda s: re.match(".*view/(.*)", s[0]).group(1)
    )
    name = scrapy.Field()
    birth_date = scrapy.Field()
    death_date = scrapy.Field()
    absentee = scrapy.Field(
        input_processor=lambda s: ' '.join(s[0].split())
    )
    maiden_name = scrapy.Field()
    spouse = scrapy.Field()
    wealth_at_death = scrapy.Field(
        input_processor=
        lambda s: re.match("(\d*).*", s[0].replace('£','').replace(',', '')).group(1) if s else s
    )
    claims = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
               insert into claim_person(person_id_1, name, sex, birth_date, death_date, absentee, maiden_name, 
               spouse, wealth_at_death, claims)
               values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
           """
        params = (self.get("person_id", ""), self.get("name", ""), self.get("sex", ""), self.get("birth_date", ""),
                  self.get("death_date", ""), self.get("absentee", ""), self.get("maiden_name", ""),
                  self.get("spouse", ""), self.get("wealth_at_death", ""), self.get("claims", ""))
        return insert_sql, params


class ClaimItem(scrapy.Item):
    claim_id = scrapy.Field(
        input_processor=lambda s: re.match(".*view/(.*)", s[0]).group(1)
    )
    claim_date = scrapy.Field()
    enslaved = scrapy.Field()
    money = scrapy.Field(
        input_processor=lambda s: s[0].replace(',', '') if s else s
    )
    money_s = scrapy.Field()
    money_d = scrapy.Field()

    colony = scrapy.Field()
    parish = scrapy.Field()
    claim_no = scrapy.Field()
    estate = scrapy.Field()
    contested = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into claim_table(claim_id_1, claim_date, enslaved, money, money_s, money_d, colony, 
            parish, claim_no, estate, contested) 
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (self.get("claim_id", ""), self.get("claim_date", ""), self.get("enslaved", ""), self.get("money", ""),
                  self.get("money_s", ""), self.get("money_d", ""), self.get("colony", ""),self.get("parish", ""),
                  self.get("claim_no", ""), self.get("estate", ""), self.get("contested", ""))
        return insert_sql, params


class LegacyItem(scrapy.Item):
    website_order = scrapy.Field()
    person_id = scrapy.Field(
        input_processor=lambda s: re.match(".*view/(.*)", s[0]).group(1)
    )
    name = scrapy.Field()

    comm_id = scrapy.Field(
        input_processor=lambda s: re.match(".*view/(.*)", s[0]).group(1)
    )
    comm_type = scrapy.Field()
    business = scrapy.Field()
    econ_sector = scrapy.Field(
        input_processor=lambda s: s[0].replace(' (', '').replace(') ', '') if s else s
    )
    # Railway Investment
    railway_title = scrapy.Field()
    railway_code = scrapy.Field(
        input_processor=lambda s: s[0].replace('(', '').replace(')', '') if s else s
    )
    railway_amount = scrapy.Field(
        input_processor=lambda s: s[0].replace('£', '').replace(' ', '') if s else s
    )
    # Shared Fields by others
    firm_name = scrapy.Field()
    firm_id = scrapy.Field(
        input_processor=lambda s: re.match(".*view/(.*)", s[0]).group(1) if s else s
    )
    # Partnership Role
    partner_role = scrapy.Field()
    # Company Role
    management_role = scrapy.Field()
    # Further Information
    partner_share = scrapy.Field()
    shareholder = scrapy.Field()
    share_amount = scrapy.Field(
        input_processor=lambda s: ''.join(s[0].split()).replace('£', '')
    )

    def get_insert_sql(self):
        insert_sql = """
            insert into legacy_table(website_order, person_id, name, comm_id, comm_type, business, econ_sector, 
            railway_title, railway_code, railway_amount, firm_name, firm_id, partner_role, management_role, partner_share, 
            shareholder, share_amount) 
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (self.get("website_order", ""), self.get("person_id", ""), self.get("name", ""), self.get("comm_id", ""),
                  self.get("comm_type", ""), self.get("business", ""), self.get("econ_sector", ""), self.get("railway_title", ""),
                  self.get("railway_code", ""), self.get("railway_amount", ""), self.get("firm_name", ""),
                  self.get("firm_id", ""), self.get("partner_role", ""), self.get("management_role", ""),
                  self.get("partner_share", ""), self.get("shareholder", ""), self.get("share_amount", ""))

        return insert_sql, params


<<<<<<< HEAD
class FirmItem(scrapy.Item):
    website_order = scrapy.Field()
    firm_id = scrapy.Field()
    firm_name = scrapy.Field()
    address_st = scrapy.Field(
        input_processor=lambda s: re.match(" (.*),.*", s[0]).group(1) if s else s
    )
    address_city = scrapy.Field(
        input_processor=lambda s: re.match(".*, (.*?) \[.*", s[0]+' []').group(1) if s else s
    )
    year = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into firm_table(website_order, firm_id, firm_name, address_st, address_city, year) 
            values (%s, %s, %s, %s, %s, %s)
        """
        params = (self.get("website_order", ""), self.get("firm_id", ""), self.get("firm_name", ""),
                  self.get("address_st", ""), self.get("address_city", ""), self.get("year", ""))
        return insert_sql, params


class MyItemLoader(ItemLoader):
=======
class ClaimRecordItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class PersonItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class ClaimItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class LegacyItemLoader(ItemLoader):
>>>>>>> 22c974afc008589b7f80f420f7ebf6e0d5794033
    default_output_processor = TakeFirst()
