# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from .items import DoubanSpiderItem, QuestionInfo,Discussion,UpdateItem
import traceback
import logging
from douban_spider.middlewares import UrlFilterAndAdd, URLRedisFilter
import os
from twisted.enterprise import adbapi


class DoubanSpiderPipeline(object):
    commit_sql_str = """insert into movie(name,scriptwriters,directors,actors,type,region,language,duration,release_date,source,alias,movie_id,description,short_answers,recommendation_index,useful_num) values ("{name}","{scriptwriters}","{directors}","{actors}","{type}","{region}","{language}","{duration}","{release_date}","{source}","{alias}","{movie_id}","{description}","{short_answers}","{recommendation_index}","{useful_num}");"""

    commit_sql_str2 = """insert into question_info(movie_id,url,question_title,question_content,answers) values ("{movie_id}","{url}","{question_title}","{question_content}","{answers}");"""

    commit_sql_str3 = """insert into discussion_info(movie_id,url,discussion_title,discussion_content,discussiones) values ("{movie_id}","{url}","{discussion_title}","{discussion_content}","{discussiones}");"""

    commit_sql_str4 = '''update movie set actors="{movie_actors}" where movie_id={id};'''

    def __init__(self, pool):
        self.dupefilter = UrlFilterAndAdd()
        self.dbpool = pool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings.get("MYSQL_HOST"),
            port=settings.get("MYSQL_PORT"),
            db=settings.get("MYSQL_DBNAME"),
            user=settings.get("MYSQL_USER"),
            passwd=settings.get("MYSQL_PASSWD"),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )

        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # print("add>>url:", item['url'])
        self.dupefilter.add_url(item['url'])

        if isinstance(item, DoubanSpiderItem):
            query = self.dbpool.runInteraction(self.do_insert, item)
            query.addErrback(self.handle_error, item, spider, item['url'])

        elif isinstance(item, QuestionInfo):
            query = self.dbpool.runInteraction(self.do_insert2, item)

        elif isinstance(item, Discussion):
            query = self.dbpool.runInteraction(self.do_insert3, item)
        elif isinstance(item, UpdateItem):
            query = self.dbpool.runInteraction(self.do_insert4, item)

    def handle_error(self, failure, item, spider, url):
        # 处理异步插入的异常
        print("!" * 100)
        print("URL", url)
        # print(item)
        print(failure)
        print("!" * 100)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        sqltext = self.commit_sql_str.format(
            name=pymysql.escape_string(str(item["name"])),
            scriptwriters=pymysql.escape_string(str(item["scriptwriters"])),
            directors=pymysql.escape_string(str(item["directors"])),
            actors=pymysql.escape_string(str(item["actors"])),
            type=pymysql.escape_string(str(item["type"])),
            region=pymysql.escape_string(str(item["region"])),
            language=pymysql.escape_string(str(item["language"])),
            duration=pymysql.escape_string(str(item["duration"])),
            release_date=pymysql.escape_string(item["release_date"]),
            source=pymysql.escape_string(str(item["source"])),
            alias=pymysql.escape_string(str(item["alias"])),
            movie_id=pymysql.escape_string(item["movie_id"]),
            description=pymysql.escape_string(str(item["description"])),
            short_answers=pymysql.escape_string(str(item["short_answers"])),
            recommendation_index=pymysql.escape_string(str(item["recommendation_index"])),
            useful_num=pymysql.escape_string(str(item["useful_num"]))
        )
        cursor.execute(sqltext)

    def do_insert2(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        sqltext2 = self.commit_sql_str2.format(
            movie_id=pymysql.escape_string(str(item["movie_id"])),
            url=pymysql.escape_string(str(item["url"])),
            question_title=pymysql.escape_string(str(item["question_title"])),
            question_content=pymysql.escape_string(str(item["question_content"])),
            answers=pymysql.escape_string(str(item["answers"]))
        )
        cursor.execute(sqltext2)

    def do_insert3(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        sqltext3 = self.commit_sql_str3.format(
            movie_id=pymysql.escape_string(str(item["movie_id"])),
            url=pymysql.escape_string(str(item["url"])),
            discussion_title=pymysql.escape_string(str(item["discussion_title"])),
            discussion_content=pymysql.escape_string(str(item["discussion_content"])),
            discussiones=pymysql.escape_string(str(item["discussiones"]))
        )
        cursor.execute(sqltext3)

    def do_insert4(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        sqltext4 = self.commit_sql_str4.format(
            movie_actors=pymysql.escape_string(item["movie_actors"]),
            id=pymysql.escape_string(item["id"])
        )
        print(sqltext4)
        print("*" * 100)
        cursor.execute(sqltext4)


    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
