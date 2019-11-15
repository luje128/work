# -*- coding: utf-8 -*-
import scrapy

from ..items import XnkbItem


class XnkbSpider(scrapy.Spider):
    name = 'xnkb'
    allowed_domains = ['https://my.unsw.edu.au']
    start_urls = ['https://my.unsw.edu.au/active/studentTimetable/timetable.xml']
    login_url = 'https://ssologin.unsw.edu.au/cas/login?service=https%3A%2F%2Fmy.unsw.edu.au%2Factive%2FstudentTimetable%2Ftimetable.xml'

    def parse(self, response):
        lt = response.xpath('//input[@name="lt"]/@value').extract_first()
        formdata = {
            '_eventId': 'submit',
            'username': 'z5057568',
            'password': 'Zjmsbzx666',
            'submit': 'Agree and sign on',
            'lt': lt,
        }
        yield scrapy.FormRequest(url=self.login_url, formdata=formdata, callback=self.parse_1, dont_filter=True)

    def parse_1(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_2, dont_filter=True)

    def parse_2(self, response):
        item = XnkbItem()
        for i in response.xpath('/html/body/div[2]/form/section[3]/table//tr/td[@colspan="4"]/table//tr'):
            Class = i.xpath('string(td[1])').extract_first()
            Component = i.xpath('string(td[2])').extract_first()
            Section = i.xpath('string(td[3])').extract_first()
            Mode = i.xpath('string(td[4])').extract_first()
            Day = i.xpath('string(td[5])').extract_first()
            Time = i.xpath('string(td[6])').extract_first()
            Facility = i.xpath('string(td[7])').extract_first()
            Location = i.xpath('string(td[8])').extract_first()
            Weeks = i.xpath('string(td[9])').extract_first()
            Instructor = i.xpath('string(td[10])').extract_first()
            item['Class'] = Class
            item['Component'] = Component
            item['Section'] = Section
            item['Mode'] = Mode
            item['Day'] = Day
            item['Time'] = Time
            item['Facility'] = Facility
            item['Location'] = Location
            item['Weeks'] = Weeks
            item['Instructor'] = Instructor
            print(item)
            yield item
