# -*- coding: utf-8 -*-
import scrapy

from ..items import XnksItem


class XnksSpider(scrapy.Spider):
    name = 'xnks'
    allowed_domains = ['https://my.unsw.edu.au']
    start_urls = ['https://my.unsw.edu.au/active/viewExamTT/viewExamTimetable.xml']
    login_url = 'https://ssologin.unsw.edu.au/cas/login?service=https%3A%2F%2Fmy.unsw.edu.au%2Factive%2FstudentTimetable%2Ftimetable.xml'

    def parse(self, response):
        lt = response.xpath('//input[@name="lt"]/@value').extract_first()
        formdata = {
            '_eventId': 'submit',
            'username': 'z5057568',
            'password': 'Zjmsbzx666',
            'submit': 'Agree and sign on',
            'lt': lt
        }
        yield scrapy.FormRequest(url=self.login_url, formdata=formdata, callback=self.parse_1, dont_filter=True)

    def parse_1(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_2, dont_filter=True)

    def parse_2(self, response):
        item = XnksItem()
        for i in response.xpath('//td[@class="formBody"]/table//tr[contains(@class,"data")]'):
            item['Day'] = i.xpath('td[@class="data"][1]/text()').extract_first()
            item['Date'] = i.xpath('td[@class="data"][2]/text()').extract_first()
            item['StartTime'] = i.xpath('td[@class="data"][3]/text()').extract_first()
            item['EndTime'] = i.xpath('td[@class="data"][4]/text()').extract_first()
            item['Course'] = i.xpath('td[@class="data"][6]/text()').extract_first()
            item['Paper'] = i.xpath('td[@class="data"][7]/text()').extract_first().strip()
            item['Location'] = i.xpath('td[@class="data"][8]/a/text()').extract_first()
            item['Materials'] = i.xpath('td[@class="data"][9]/text()').extract_first()
            print(item)
            yield item