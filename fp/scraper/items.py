# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem

from api.models import Docket, Document


class DocketItem(DjangoItem):
    django_model = Docket
    
class DocumentItem(DjangoItem):
    django_model = Document
    