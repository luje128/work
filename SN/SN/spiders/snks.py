# -*- coding: utf-8 -*-
import scrapy
from ..commands.crawlall import Command
from ..items import SnksItem


class SnksSpider(scrapy.Spider):
    name = 'snks'
    allowed_domains = ['https://exams.sydney.edu.au']
    start_urls = ['https://exams.sydney.edu.au/timetable/personal.php?db=17/']

    # user_name = input('请输入账号：')
    # user_password = input('请输入密码：')

    def start_requests(self):
        login_url = 'https://exams.sydney.edu.au/timetable/personal.php?db=17'
        data = {
            # '_token': '8e5fc1f6f29fe69',
            'tAccountName': 'mzha4228',
            'tWebPassword': 'zmyZMY1997',
            'action': 'login'
        }
        yield scrapy.FormRequest(url=login_url, formdata=data, callback=self.parse)

    def parse(self, response):
        item = SnksItem()
        for a in response.xpath('//td/strong'):
            name = a.xpath('text()').extract_first().strip()
            detail_list = a.xpath('../../following-sibling::tr[position()>0][position()<=12]/td[2]')
            # for b in detail_list:
            # abc = b.xpath('string(.)').extract_first().strip()
            item['exam'] = name.strip()
            item['date'] = detail_list[0].xpath('string(.)').extract_first().strip()
            item['time'] = detail_list[1].xpath('string(.)').extract_first().strip()
            item['writing_time'] = detail_list[2].xpath('string(.)').extract_first().strip()
            item['reading_time'] = detail_list[3].xpath('string(.)').extract_first().strip()
            item['campus'] = detail_list[4].xpath('string(.)').extract_first().strip()
            item['venue'] = detail_list[5].xpath('string(.)').extract_first().strip()
            item['building'] = detail_list[6].xpath('string(.)').extract_first().strip()
            item['room'] = detail_list[7].xpath('string(.)').extract_first().strip()
            item['your_seat'] = detail_list[8].xpath('string(.)').extract_first().strip()
            item['map'] = detail_list[9].xpath('string(.)').extract_first().strip()
            item['exam_conditions'] = detail_list[10].xpath('string(.)').extract_first().strip()
            item['materials_permitted'] = detail_list[11].xpath('string(.)').extract_first().strip()
            print(item)
            yield item
