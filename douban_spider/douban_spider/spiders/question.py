# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
import time
import logging
from copy import deepcopy
import requests
from douban_spider.items import QuestionInfo
from lxml import etree
import random
from fake_useragent import UserAgent
import simplejson as json
import emoji
from scrapy_splash import SplashRequest
from utils.handle_html import filter_str_emoji_blank
from utils.proxy_ip import get_aby_ip

logger = logging.getLogger(__name__)


class QuestionSpider(scrapy.Spider):
    global null
    null = 0
    name = 'question'
    allowed_domains = ['douban.com']
    # start_urls = ['http://douban.com/']
    question_page_url = "https://movie.douban.com/subject/{}/questions/?start={}&type=all"
    question_answers_url = "https://movie.douban.com/subject/{}/questions/{}/answers/?start=0&limit=500&id="
    question_content_url = "https://movie.douban.com/subject/{}/questions/{}/"
    second_floor_url = "https://movie.douban.com/subject/{}/questions/{}/answers/{}/comments/?start=0"

    question_headers = {'Host': 'movie.douban.com',
                     'Connection': 'keep-alive',
                     'Cache-Control': 'max-age=0',
                     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                     'Accept-Encoding': 'keep-gzip, deflate, br',
                     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                     'Upgrade-Insecure-Requests': '1',
                     }

    def get_question_ids(self, html):
        question_urls = re.findall('a href="(.*?)" target="_blank" class="', html)
        ids = [i.split("/")[-2] for i in question_urls]
        return ids

    def get_question_titles(self, html):
        question_titles = re.findall('target="_blank" class="">(.*?)</a>', html)
        return question_titles

    def start_requests(self):
        file = open("./movie_id.txt", encoding="utf-8")
        for movie_id in file.readlines()[0:1]:
            movie_id = movie_id.replace("\n", "")
            question_page_url = self.question_page_url.format(movie_id, 0)
            yield Request(question_page_url, callback=self.parse, dont_filter=True,
                          meta={"movie_id": movie_id})

    def parse(self, response):
        meta_data = deepcopy(response.meta)
        print("①问题page地址：", response.url)
        html = response.body.decode()
        questiones_total_num = re.findall('<strong>(.*?)个问题</strong>', html)[0]
        print("②问题总数：", questiones_total_num)

        question_ids = self.get_question_ids(html)
        question_titles = self.get_question_titles(html)
        if int(questiones_total_num) > 20:
            for i in range(0, int(questiones_total_num), 20):
                yield Request(self.question_page_url.format(meta_data["movie_id"], i),
                              callback=self.parse_question_page,
                              dont_filter=True, meta=meta_data)
        else:
            for i, an_id in enumerate(question_ids):
                content_url = self.question_answers_url.format(meta_data["movie_id"], an_id)
                meta_data["an_id"] = an_id
                meta_data["title"] = question_titles[i]
                yield Request(content_url, callback=self.parse_content_url, meta=meta_data, dont_filter=True)

    def parse_question_page(self, response):
        meta_data = deepcopy(response.meta)
        html = response.body.decode()
        question_ids = self.get_question_ids(html)
        question_titles = self.get_question_titles(html)
        for i, an_id in enumerate(question_ids):
            content_url = self.question_content_url.format(meta_data["movie_id"], an_id)
            meta_data["an_id"] = an_id
            meta_data["title"] = question_titles[i]
            yield Request(content_url, callback=self.parse_content_url, meta=meta_data, dont_filter=True)

    def parse_content_url(self, response):
        meta_data = deepcopy(response.meta)
        html = response.body.decode()
        question_content = "".join(
            etree.HTML(html).xpath("//div[@id='question-content']//text()")).strip().replace("\n", "")
        meta_data["content"] = question_content
        meta_data["question_url"] = response.url
        answers_url = self.question_answers_url.format(meta_data["movie_id"], meta_data["an_id"])
        yield Request(answers_url, callback=self.parse_question_url, meta=meta_data, dont_filter=True)

    def parse_question_url(self, response):
        meta_data = deepcopy(response.meta)
        json_html = json.loads(response.body.decode())
        print("③answer地址：", meta_data["question_url"])
        print(meta_data)
        first_floor_list = [filter_str_emoji_blank(i["content"]) for i in json_html["answers"]]
        num_of_comments_list = [i["num_of_comments"] for i in json_html["answers"]]
        second_floor_id_list = [i["id"] for i in json_html["answers"]]

        answers = []
        for i, second_id in enumerate(num_of_comments_list):
            one_answer = {}
            one_answer["first_floor"] = first_floor_list[i]
            if second_id != 0:
                url = self.second_floor_url.format(meta_data["movie_id"], meta_data["an_id"], second_floor_id_list[i])
                html_json = requests.get(url, proxies=get_aby_ip(),headers=self.question_headers).text
                second_floor_answer = [filter_str_emoji_blank(i) for i in re.findall('text":"(.*?)","created_at',html_json)]
                one_answer["second_floor"] = second_floor_answer
            else:
                one_answer["second_floor"] = []
            answers.append(one_answer)

        question_info = QuestionInfo()
        question_info["movie_id"] = meta_data["movie_id"]
        question_info["url"] = meta_data["question_url"]
        question_info["question_title"] = meta_data["title"]
        question_info["question_content"] = meta_data["content"]
        question_info["answers"] = answers
        print("*" * 100)
        yield question_info

