# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from uuid import uuid4
from datetime import datetime
from itemadapter import ItemAdapter


class UUIDTimestampAditionPipeline:
    """used to add `uuid`, and `timestamp` to the response data scraped
    from pucweb1 spider (for now)
    
    ## Methods
    
    #### process(item, spider)
    - processes the yielded `item` from the `spider`
    """
    def process_item(self, item, spider: scrapy.Spider):
        """data yielded by the parse methods of the spiders are passed
        to pipelines process_item method, here we can make further ch-
        anges to the scraped data or store them in the database

        Args:
            item: item yielded by the parse method of the Spider
            spider (scrapy.Spider): spider that yielded the item

        Returns:
            _type_: depends on which spider passed the item to pipeline
        """
        if spider.name=="pucweb1":
            adapter = ItemAdapter(item)
            adapter.update({
                "id": f"{uuid4()}", 
                "timestamp": datetime.now().timestamp()})

        return item
