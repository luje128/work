# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv

from .items import XnkbItem, XnksItem, XnzyItem


class XnPipeline(object):
    # 定义一个集合去重
    # self.wys = set()

    def __init__(self):
        # 打开文件，指定方式为写，利用newline=''参数把csv写数据时产生的空行消除
        self.file_xnkb = open('XNKB.csv', 'w', newline='', encoding='utf-8-sig')
        self.file_xnks = open('XNKS.csv', 'w', newline='', encoding='utf-8-sig')
        self.file_xnzy = open('XNZY.csv', 'w', newline='', encoding='utf-8-sig')
        # 设置文件第一行的字段名，注意要跟spider传过来的字典item的key名称相同
        self.fieldnames_xnkb = ['Class', 'Component', 'Section', 'Mode', 'Day', 'Time', 'Facility',
                                'Location', 'Weeks', 'Instructor']
        self.fieldnames_xnks = ['Day', 'Date', 'StartTime', 'EndTime', 'Course', 'Paper', 'Location', 'Materials']
        self.fieldnames_xnzy = ['title', 'time', 'name']
        # 指定文件的写入方式为csv字典写入，参数1为指定具体文件，参数2为指定字段名
        self.writer_xnkb = csv.DictWriter(self.file_xnkb, fieldnames=self.fieldnames_xnkb)
        self.writer_xnks = csv.DictWriter(self.file_xnks, fieldnames=self.fieldnames_xnks)
        self.writer_xnzy = csv.DictWriter(self.file_xnzy, fieldnames=self.fieldnames_xnzy)
        # 写入第一行字段名，因为只要写入一次，所以文件放在__init__里面
        self.writer_xnkb.writeheader()
        self.writer_xnks.writeheader()
        self.writer_xnzy.writeheader()

    def process_item(self, item, spider):
        # content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        # self.file.write(content)
        # 写入spider传过来的具体数值
        if isinstance(item, XnkbItem):

            self.writer_xnkb.writerow(item)

        elif isinstance(item, XnksItem):

            self.writer_xnks.writerow(item)

        elif isinstance(item, XnzyItem):

            self.writer_xnzy.writerow(item)

        return item

    def __del__(self):
        self.file_xnkb.close()
        self.file_xnks.close()
        self.file_xnzy.close()
