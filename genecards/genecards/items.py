# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GenecardsItem(scrapy.Item):
    # define the fields for your item here like:
    _1_cluster = scrapy.Field()
    _2_gene_name = scrapy.Field()
    _3_first = scrapy.Field()
    _4_second = scrapy.Field()
    _5_third = scrapy.Field()
