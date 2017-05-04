__author__ = 'alrifqi'
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from remoteworkscrapper.spiders import RemoteokSpider

process = CrawlerProcess(get_project_settings())
process.crawl(RemoteokSpider)
process.start()