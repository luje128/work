# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv

from .items import SnkbItem, SnksItem, SnzyItem


class SnPipeline(object):

    # 定义一个集合去重
    # self.wys = set()

    def __init__(self):
        # 打开文件，指定方式为写，利用newline=''参数把csv写数据时产生的空行消除
        self.file_snkb = open('SNKB.csv', 'w', newline='', encoding='utf-8-sig')
        self.file_snks = open('SNKS.csv', 'w', newline='', encoding='utf-8-sig')
        self.file_snzy = open('SNZY.csv', 'w', newline='', encoding='utf-8-sig')
        # 设置文件第一行的字段名，注意要跟spider传过来的字典item的key名称相同
        self.fieldnames_snkb = ['date', 'time_begin_at', 'time_end_at', 'week', 'semester', 'course_id', 'type',
                                'location']
        self.fieldnames_snks = ['exam', 'date', 'time', 'writing_time', 'reading_time', 'campus', 'venue', 'building',
                                'room',
                                'your_seat', 'map', 'exam_conditions', 'materials_permitted']
        self.fieldnames_snzy = ['CourseNumber', 'TitleName', 'DueTime']
        # 指定文件的写入方式为csv字典写入，参数1为指定具体文件，参数2为指定字段名
        self.writer_snkb = csv.DictWriter(self.file_snkb, fieldnames=self.fieldnames_snkb)
        self.writer_snks = csv.DictWriter(self.file_snks, fieldnames=self.fieldnames_snks)
        self.writer_snzy = csv.DictWriter(self.file_snzy, fieldnames=self.fieldnames_snzy)
        # 写入第一行字段名，因为只要写入一次，所以文件放在__init__里面
        self.writer_snkb.writeheader()
        self.writer_snks.writeheader()
        self.writer_snzy.writeheader()

    def process_item(self, item, spider):
        # content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        # self.file.write(content)
        # 写入spider传过来的具体数值
        if isinstance(item, SnkbItem):

            self.writer_snkb.writerow(item)

        elif isinstance(item, SnksItem):

            self.writer_snks.writerow(item)

        elif isinstance(item, SnzyItem):

            self.writer_snzy.writerow(item)

        return item

    def __del__(self):
        self.file_snkb.close()
        self.file_snks.close()
        self.file_snzy.close()
