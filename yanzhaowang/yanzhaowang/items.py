# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YanzhaowangItem(scrapy.Item):
    schoolName = scrapy.Field()  #学校名
    location = scrapy.Field()  #所在地
    belong = scrapy.Field()  #隶属
    graduateSchool = scrapy.Field()  #研究生院
    optional = scrapy.Field()  #自划线
    type = scrapy.Field()  #专业分类
    subject = scrapy.Field()  #科目
    number = scrapy.Field()  #号码
    url = scrapy.Field()  #url
