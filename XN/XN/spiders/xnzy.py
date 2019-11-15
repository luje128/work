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

from ..items import XnzyItem


class XnzySpider(scrapy.Spider):
    name = 'xnzy'
    allowed_domains = ['https://moodle.telt.unsw.edu.au']
    start_urls = ['https://moodle.telt.unsw.edu.au/calendar/view.php?view=month&time=1572526800']

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

        # self.login_url = 'https://moodle.telt.unsw.edu.au/calendar/view.php?view=month&time=1572526800'

        self.driver = webdriver.Chrome(chrome_options=self.options,
                                       executable_path='C:/Users\yvonn\Desktop\chromedriver.exe')

        for url in self.start_urls:
            self.driver.get(url=url)

            # 重写init初始化方法
            super(XnzySpider, self).__init__()
            # 分发给spider_close，使用信号量spider_closed
            dispatcher.connect(self.spider_close, signals.spider_closed)

            # 切换到登陆窗口的iframe句柄
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//div/iframe')))
            iframe = self.driver.find_element_by_tag_name('iframe')
            self.driver.switch_to.frame(iframe)

            # 获取账号、密码输入框
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
            self.driver.find_element_by_xpath('//*[@id="username"]').send_keys('z5188133')
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
            self.driver.find_element_by_xpath('//*[@id="password"]').send_keys('Hfy19971001')
            # 获取登陆提交按钮
            submit = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="submit"]')))
            # 由于普通元素获取但是无法点击，可以通过js点击解决
            self.driver.execute_script("arguments[0].click();", submit)

    def parse(self, response):
        # 获取目标网页等待元素加载完毕
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@data-region="day-content"]/ul/li/a[not(contains(@title,"AAP"))]')))
        # 获取作业信息剔除课表课程信息
        item = XnzyItem()
        for i in self.driver.find_elements_by_xpath(
                '//div[@data-region="day-content"]/ul/li/a[not(contains(@title,"AAP"))]'):
            # 循环点击
            i.find_element_by_xpath('span').click()
            # 获取目标信息的弹框详情等待元素加载完毕
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="container-fluid"]')))
            title = self.driver.find_element_by_xpath(
                '//div[@class="container-fluid"]/../../../div[1]/h3[@class="modal-title"]').text
            time = self.driver.find_element_by_xpath(
                '//div[@class="container-fluid"]/div[1]/div[@class="span11"]').text
            name = self.driver.find_element_by_xpath(
                '//div[@class="container-fluid"]/div/div[@class="span11"]/a').text
            item['title'] = title
            item['time'] = time
            item['name'] = name
            print(item)
            yield item
            # 提取信息完毕后点击关闭弹框按钮
            self.driver.find_element_by_xpath('//div[@class="container-fluid"]/../../../div[1]/button').click()
            # 返回目标网页主界面等待元素加载完毕
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@data-region="day-content"]/ul/li/a[not(contains(@title,"AAP"))]')))

    def spider_close(self):
        # 爬虫退出时关闭Chrome
        self.driver.quit()
