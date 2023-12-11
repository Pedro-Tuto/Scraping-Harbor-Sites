# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    harbor = scrapy.Field(value_type=str)
    merchandise = scrapy.Field(value_type=str)
    direction = scrapy.Field(value_type=str)
    daily_volume_in_tons = scrapy.Field(value_type=str)
    daily_volume_in_movs = scrapy.Field(value_type=str)