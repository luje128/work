# -*- coding: utf-8 -*-
import scrapy
import base64
import scrapy
from scrapy import signals
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher

from ..items import SnzyItem


class SnzySpider(scrapy.Spider):
    name = 'snzy'
    allowed_domains = ['https://sts.sydney.edu.au']
    start_urls = [
        'https://canvas.sydney.edu.au/calendar#view_name=agenda']

    def __init__(self):
        # 定义chrome的配置
        self.options = webdriver.ChromeOptions()
        # 修改chrome的配置
        self.prefs = {
            'profile.default_content_setting_values': {
                'images': 2,  # 限制图片加载
                # 'javascript': 2  # 禁用js
            }
        }
        # 将变量传入
        self.options.add_experimental_option('prefs', self.prefs)
        # 设置无头
        self.options.add_argument('--headless')

        self.login_url = 'https://canvas.sydney.edu.au/calendar#view_name=agenda'

        self.driver = webdriver.Chrome(chrome_options=self.options,
                                       executable_path='C:/Users\yvonn\Desktop\chromedriver.exe')

        # print('-----正在解析中-----')
        # WebDriverWait(self.driver, 60).until(
        #     EC.presence_of_element_located((By.XPATH, '//div[@id="win0divSS_EXAMSCH1_VW$grid$0"]')))
        # for a in self.driver.find_elements_by_xpath(
        #         '//div[@id="win0divSS_EXAMSCH1_VW$grid$0"]/table//tr/td/div/span'):
        #     print(a.text)
        #
        # print('解析完毕!')

        super(SnzySpider, self).__init__()
        # 分发给spider_close，使用信号量spider_closed
        dispatcher.connect(self.spider_close, signals.spider_closed)

    def parse(self, response):
        item = SnzyItem()
        for a in response.xpath('//div[@class="agenda-event__container"]/ul/li'):
            CourseNumber = a.xpath('span[4]/text()').extract_first().split(' ')[1].strip()
            TitleName = a.xpath('span[2]/text()').extract_first().strip()
            DueTime = a.xpath('../../../div[@class="agenda-day"]/h3/span/text()').extract_first().strip()
            item['CourseNumber'] = CourseNumber
            item['TitleName'] = TitleName
            item['DueTime'] = DueTime
            print(item)
            yield item
    def spider_close(self):
        # 爬虫退出时关闭Chrome
        self.driver.quit()
