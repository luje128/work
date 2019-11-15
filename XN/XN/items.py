# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XnkbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Class = scrapy.Field()
    Component = scrapy.Field()
    Section = scrapy.Field()
    Mode = scrapy.Field()
    Day = scrapy.Field()
    Time = scrapy.Field()
    Facility = scrapy.Field()
    Location = scrapy.Field()
    Weeks = scrapy.Field()
    Instructor = scrapy.Field()


class XnksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Day = scrapy.Field()
    Date = scrapy.Field()
    StartTime = scrapy.Field()
    EndTime = scrapy.Field()
    Course = scrapy.Field()
    Paper = scrapy.Field()
    Location = scrapy.Field()
    Materials = scrapy.Field()


class XnzyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    name = scrapy.Field()
