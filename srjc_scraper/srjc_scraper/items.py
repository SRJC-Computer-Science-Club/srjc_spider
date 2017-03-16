# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from __future__ import absolute_import
import scrapy


class SrjcScraperItem(scrapy.Item):
    section_id = scrapy.Field()
    short_name = scrapy.Field()
    long_name = scrapy.Field()
    description = scrapy.Field()

    units = scrapy.Field()
    status = scrapy.Field()

    current_enrolled = scrapy.Field()
    seats_remaining = scrapy.Field()

    start_date = scrapy.Field()
    end_date = scrapy.Field()
    final_date = scrapy.Field()

    times = scrapy.Field()
    pass
