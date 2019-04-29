from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from gymshark import settings
from gymshark.spiders.product import ProductSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(ProductSpider)
    process.start()
