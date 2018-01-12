# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanMovieSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()  # 豆瓣详情页地址
    title = scrapy.Field()  # 电影名称
    year = scrapy.Field()  # 电影年份
    info = scrapy.Field()  # 影片基本信息
    related_info = scrapy.Field()  # 简介
    pass
