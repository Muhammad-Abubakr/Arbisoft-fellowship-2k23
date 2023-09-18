from scrapy.crawler import CrawlerProcess
from django.core.management.base import BaseCommand
from scrapy.utils.project import get_project_settings
from scraper.spiders.pucweb1_spider import PucWeb1Spider

class Command(BaseCommand):
    help = "Crawls the documents for given doc id"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(PucWeb1Spider, docket_id="23-09011")
        process.start()
