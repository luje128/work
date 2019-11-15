# -*- coding: utf-8 -*-
import re

import scrapy
from ..commands.crawlall import Command
from ..items import SnkbItem


class SnkbSpider(scrapy.Spider):
    name = 'snkb'
    allowed_domains = ['https://wasm.usyd.edu.au']
    start_urls = ['https://www.timetable.usyd.edu.au/personaltimetable/timetable/{}/current/?mode=schedule']

    # user_name = input('请输入账号：')
    # user_password = input('请输入密码：')

    def start_requests(self):
        login_url = 'https://wasm.usyd.edu.au/login.cgi?apprealm=usyd&appID=tt-studentweb&destURL=https%3A//www.timetable.usyd.edu.au/personaltimetable/'
        data = {
            'appID': 'tt-studentweb',
            'appRealm': 'usyd',
            'destURL': 'https://www.timetable.usyd.edu.au/personaltimetable/',
            'credential_0': 'mzha4228',
            'credential_1': 'zmyZMY1997',
            'Submit': '登入'
        }
        yield scrapy.FormRequest(url=login_url, formdata=data, callback=self.parse)

    def parse(self, response):
        str = response.xpath('//div[@class="auth-info"]/span/text()').extract_first()
        res_str = re.search('[0-9]+', str).group()
        for url in self.start_urls:
            yield scrapy.Request(url=url.format(res_str), callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        item = SnkbItem()
        for detail in response.xpath('//p[@class="class-details"]'):
            date = detail.xpath('../h3/text()').extract_first().strip()
            time_begin_at = detail.xpath('string(strong/text())').extract_first().split('to')[0].replace('.',
                                                                                                         '').strip()
            time_end_at = detail.xpath('string(strong/text())').extract_first().split('to')[1].replace('.', '').replace(
                ',', '').strip()
            week = detail.xpath('strong/span/text()').extract_first().replace('of', '').strip()
            semester = detail.xpath('strong/span/span/text()').extract_first().strip()
            course_id = detail.xpath('text()').extract_first().replace(':', '').strip().split(' ')[0]

            type = ' '.join(
                detail.xpath('text()').extract_first().replace(':', '').replace('in', '').strip().split(' ')[1:])

            location = detail.xpath('a/text()').extract_first().strip()
            item['date'] = date
            item['time_begin_at'] = time_begin_at
            item['time_end_at'] = time_end_at
            item['week'] = week
            item['semester'] = semester
            item['course_id'] = course_id
            item['type'] = type
            item['location'] = location
            print(item)
            yield item
