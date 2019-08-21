# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanSpiderItem(scrapy.Item):
    name = scrapy.Field()
    scriptwriters = scrapy.Field()
    directors = scrapy.Field()
    actors = scrapy.Field()
    type = scrapy.Field()
    region = scrapy.Field()
    language = scrapy.Field()
    duration = scrapy.Field()
    release_date = scrapy.Field()
    source = scrapy.Field()
    alias = scrapy.Field()
    movie_id = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    short_answers = scrapy.Field()
    recommendation_index = scrapy.Field()
    useful_num = scrapy.Field()


class QuestionInfo(scrapy.Item):
    movie_id = scrapy.Field()
    url = scrapy.Field()
    question_title = scrapy.Field()
    question_content = scrapy.Field()
    answers = scrapy.Field()

class Discussion(scrapy.Item):
    movie_id = scrapy.Field()
    url = scrapy.Field()
    discussion_title = scrapy.Field()
    discussion_content = scrapy.Field()
    discussiones = scrapy.Field()


class UpdateItem(scrapy.Item):
    movie_actors = scrapy.Field()
    id = scrapy.Field()
    url = scrapy.Field()

