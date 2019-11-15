# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 悉尼课表
class SnkbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    time_begin_at = scrapy.Field()
    time_end_at = scrapy.Field()
    week = scrapy.Field()
    semester = scrapy.Field()
    course_id = scrapy.Field()
    type = scrapy.Field()
    location = scrapy.Field()


# 悉尼考试
class SnksItem(scrapy.Item):
    exam = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    writing_time = scrapy.Field()
    reading_time = scrapy.Field()
    campus = scrapy.Field()
    venue = scrapy.Field()
    building = scrapy.Field()
    room = scrapy.Field()
    your_seat = scrapy.Field()
    map = scrapy.Field()
    exam_conditions = scrapy.Field()
    materials_permitted = scrapy.Field()


# 悉尼作业
class SnzyItem(scrapy.Item):
    CourseNumber = scrapy.Field()
    TitleName = scrapy.Field()
    DueTime = scrapy.Field()
