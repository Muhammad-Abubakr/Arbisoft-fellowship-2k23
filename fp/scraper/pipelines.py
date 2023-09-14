# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
from itemadapter import ItemAdapter
from psycopg import IntegrityError, Transaction
from django.core.exceptions import ValidationError
import asyncio

class ScraperPipeline:
    def process_item(self, item, spider):
        return item

class DocketPipeline:
    def process_item(self, item, spider):
        try:
            item.save()
        except (ValueError, IntegrityError, ValidationError) as e:
            spider.log(str(e), logging.DEBUG)
            return None
        return item