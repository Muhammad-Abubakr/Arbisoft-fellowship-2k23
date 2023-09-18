# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
from scrapy.spiders import Spider
from requests import post

class ScraperPipeline:
    def process_item(self, item, spider):
        return item

class DocketPipeline:
    def process_item(self, item, spider: Spider):
        try:
            if spider.name == "pucweb1_dockets":
                post(url="http://127.0.0.1:8000/api/dockets/", data=item)
            else:
                post(url="http://127.0.0.1:8000/api/documents/", data=item)
        except Exception as e:
            spider.log(str(e), logging.DEBUG)
            return None

        return item