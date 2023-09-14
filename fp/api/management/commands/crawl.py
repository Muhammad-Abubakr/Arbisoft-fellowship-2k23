from scrapy.crawler import CrawlerProcess
from django.core.management.base import BaseCommand
from scrapy.utils.project import get_project_settings
from scraper.spiders.pucweb1_dockets_spider import PucWeb1DocketsSpider

class Command(BaseCommand):
    help = "Crawls the dockets from pucweb1 homepage"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())

        process.crawl(PucWeb1DocketsSpider)
        process.start()