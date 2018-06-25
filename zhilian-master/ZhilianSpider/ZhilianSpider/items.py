# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class ZhilianspiderItem(scrapy.Item):
    _id = Field()
    from_website = Field()
    min_salary = Field()
    max_salary = Field()
    location = Field()
    publish_date = Field()
    work_type = Field()
    work_experience = Field()
    limit_degree = Field()
    people_count = Field()
    career_type = Field()
    work_duty = Field()
    work_need = Field()
    work_duty_content = Field()
    work_info_url = Field()


