# -*- coding: utf-8 -*-
import scrapy
import re
from remoteworkscrapper.items import RemoteworkscrapperItem
from scrapy.http import Request

from remoteworkscrapper.items import RemoteworkscrapperItem


class RemoteokSpider(scrapy.Spider):
    name = "remoteok_spider"
    allowed_domains = ["remoteok.io"]
    start_urls = 'https://remoteok.io/'

    def start_requests(self):
    	yield scrapy.Request(url=self.start_urls, callback=self.parse)

    def parse(self, response):
        res =  response.css("tr.job").extract()
        data = []
        for job in response.css('tr.job'):
            temp = RemoteworkscrapperItem()
            job_id = ''
            job_url = ''
            for index, attribute in enumerate(job.xpath('@*'), start=1):
                attribute_name = job.xpath('name(@*[%d])' % index).extract_first()
                if attribute_name == 'data-id':
                    job_id = attribute.extract()
                elif attribute_name == 'data-url':
                    job_url = attribute.extract()
            temp['title'] = job.css('td.company_and_position a.preventLink h2::text').extract()[0]
            temp['desc'] = self.clean_description(response.css("tr.expand-" + job_id + " div.description").xpath('./div').extract()[0])
            temp['url'] = 'https://remoteok.io'+job_url
            temp['company'] = job.css('td.company_and_position a.companyLink h3::text').extract()[0]
            temp['source'] = 'https://remoteok.io'
            yield temp

    def clean_description(self, desc):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, ' ', desc)
        return cleantext
