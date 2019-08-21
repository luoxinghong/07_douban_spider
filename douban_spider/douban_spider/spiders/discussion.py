# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
import time
import logging
from copy import deepcopy
import requests
from douban_spider.items import Discussion
from lxml import etree
import random
from fake_useragent import UserAgent
import simplejson as json
import emoji

logger = logging.getLogger(__name__)


class DiscussionSpider(scrapy.Spider):
    name = 'discussion'
    # allowed_domains = ['douban.com']
    global null
    null = ""
    DISCUSSION_HEADERS = {'Host': 'movie.douban.com',
                          'Connection': 'keep-alive',
                          'Cache-Control': 'no-cache',
                          'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                          'Accept-Encoding': 'gzip, deflate, br',
                          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                          'Upgrade-Insecure-Requests': '1',
                          }

    DISCUSSION_URL = "https://movie.douban.com/subject/{}/discussion/?start={}&sort_by=time"

    def start_requests(self):
        file = open("./movie_id.txt", encoding="utf-8")
        for movie_id in file.readlines():
            movie_id = movie_id.replace("\n", "")
            discussion_page_url = self.DISCUSSION_URL.format(movie_id, 0)
            # 讨论page页不参与去重
            yield Request(discussion_page_url, callback=self.parse, dont_filter=True,
                          meta={"movie_id": movie_id})

    def parse(self, response):
        if response.status != 200:
            print('访问讨论page页异常，停止爬虫！！！，状态码是：', response.status)
            logger.warning("访问讨论page页异常，停止爬虫！！！，状态码是：：{}，URL是：{}".format(response.status,response.url))
        movie_id = response.meta["movie_id"]
        print("①话题地址：", response.url)
        html = response.body.decode()
        discussiones_total_num = re.findall('data-desc="(.*?)个话题', html)[0]
        print("②话题总数：", discussiones_total_num)
        discussiones_urls = re.findall('a href="(.*?)" title="', html)

        if int(discussiones_total_num) > 20:
            for i in range(20, int(discussiones_total_num), 20):
                time.sleep(3)
                res = requests.get(self.DISCUSSION_URL.format(movie_id, i), allow_redirects=False).text
                discussiones_urls_in_apage = re.findall('a href="(.*?)" title="', res)
                discussiones_urls += discussiones_urls_in_apage
        # print("③话题地址长度：", len(discussiones_urls))

        for url in discussiones_urls:
            yield Request(url, callback=self.parse_discussion_url, meta={"movie_id": movie_id})

    def parse_discussion_url(self, response):
        discussion_url = response.url
        print("④话题详细页地址：", discussion_url)
        # print("⑤话题详细页状态码：", response.status)
        movie_id = response.meta["movie_id"]

        discussion_title, discussion_content, discussiones, discussion_info = "", "", [], {}
        html = response.body.decode()
        if response.status != 200:
            print('访问讨论详情页异常，停止爬虫！！！，状态码是：', response.status)
            logger.warning("访问讨论详情页异常，停止爬虫！！！，状态码是：{}，URL是：{}".format(response.status, discussion_url))

        discussion_title = etree.HTML(html).xpath("//div[@id='content']/h1/text()")[0].strip().replace("\n", "")
        discussion_content = "".join(
            etree.HTML(html).xpath("//div[@id='link-report']/span/p[1]//text()")).strip().replace("\n", "")

        discussion_divs = etree.HTML(html).xpath("//div[@class='content report-comment']")
        for div in discussion_divs:
            if len(div.xpath(".//div[@class='reply-quote']")) > 0:
                first_str = "".join(
                    div.xpath(".//div[@class='reply-quote']//div[@class='all']//text()")).strip().replace("\n", "")
                second = "".join(div.xpath("./p//text()")).strip().replace("\n", "")
                discussion = first_str + "\t" + second
            else:
                discussion = "".join(div.xpath("./p//text()")).strip().replace("\n", "")
            discussiones.append(discussion)

        discussion_info = Discussion()
        discussion_info["movie_id"] = movie_id
        discussion_info["url"] = discussion_url
        discussion_info["discussion_title"] = discussion_title
        discussion_info["discussion_content"] = discussion_content
        discussion_info["discussiones"] = discussiones
        print("*" * 100)
        yield discussion_info
