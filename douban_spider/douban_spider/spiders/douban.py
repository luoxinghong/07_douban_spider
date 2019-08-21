# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
import time
import logging
from copy import deepcopy
import requests
from douban_spider.items import DoubanSpiderItem
from lxml import etree
from fake_useragent import UserAgent
from retrying import retry
import simplejson as json
import emoji


logger = logging.getLogger(__name__)

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    # allowed_domains = ['douban.com']
    global null
    null = ""
    regex = re.compile(r'\\(?![/u"])')

    short_headers = {'Host': 'api.douban.com',
                     'Connection': 'keep-alive',
                     'Cache-Control': 'no-cache',
                     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                     'Accept-Encoding': 'gzip, deflate',
                     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                     'Upgrade-Insecure-Requests': '1',
                     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
                     }

    index_headers = {'Host': 'api.douban.com',
                     'Pragma': 'no-cache',
                     'Connection': 'keep-alive',
                     'Cache-Control': 'no-cache',
                     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                     'Accept-Encoding': 'keep-gzip, deflate, br',
                     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                     'Upgrade-Insecure-Requests': '1',
                     }

    short_url = "http://api.douban.com/v2/movie/subject/{}/comments?start={}&count=20&apikey=0b2bdeda43b5688921839c8ecb20399b&city=%E5%8C%97%E4%BA%AC&client=&udid="

    movie_info_url = "http://api.douban.com/v2/movie/subject/{}?apikey=0b2bdeda43b5688921839c8ecb20399b&city=%E5%8C%97%E4%BA%AC&client=&udid="


    def get_shorturl_content(self, url):
        response = requests.get(url, headers=self.short_headers)
        try:
            res_temp = self.regex.sub(r"\\\\", response.content.decode('unicode_escape')).replace("null", "0")
        except Exception as e:
            pass
        finally:
            res_temp = response.content.decode()
        return json.loads(res_temp, strict=False)


    def start_requests(self):
        file = open("./movie_id.txt", encoding="utf-8")
        for movie_id in file.readlines():
            begin_url = self.movie_info_url.format(movie_id.replace("\n", ""))
            yield Request(begin_url, callback=self.parse, dont_filter=True, headers=self.index_headers,
                          meta={"id": movie_id.replace("\n", "")})

    def parse(self, response):
        try:
            res_dict = json.loads(self.regex.sub(r"\\\\", response.body.decode('unicode_escape').replace("null", "0")),
                              strict=False)
        except Exception as e:
            res_dict = json.loads(response.body.decode())

        # 电影url
        url = "https://movie.douban.com/subject/" + response.meta["id"]
        print("111电影名url：", url)

        # 电影名
        movie_name = res_dict["title"]
        # print("222电影名：", movie_name)

        # 电影编剧
        movie_scriptwriters = [i["name"] for i in res_dict["writers"]]
        # print("333编剧：", movie_scriptwriters)

        # 电影导演
        movie_directors = [i["name"] for i in res_dict["directors"]]
        # print("444导演：", movie_directors)

        # # 电影主演casts
        movie_actors = [i["name"] for i in res_dict["casts"]]
        # print("555主演：", movie_actors)

        # 电影类型
        movie_type = res_dict["genres"]
        # print("6666类型：", movie_type)

        # 电影地区
        movie_region = res_dict["countries"]
        # print("777地区：", movie_region)

        # 电影语言languages
        movie_language = res_dict["languages"]
        # print("888语言：", movie_language)

        # 电影时长
        if len(res_dict["durations"]) > 0:
            movie_duration = res_dict["durations"][0].replace("分钟", "").split(":")[-1]
        else:
            movie_duration = ""
        # print("999时长：", movie_duration)

        # 电影上映日期
        if len(res_dict["pubdates"]) > 0:
            movie_release_date = re.sub("\(.*\)", res_dict["pubdates"][0], "")
        else:
            movie_release_date = ""
        # print("10上映日期：", movie_release_date)

        # 电影别名aka
        movie_alias = res_dict["aka"]
        # print("11别名：", movie_alias)

        # # 电影评分
        movie_source = res_dict["rating"]["average"]
        # print("12评分：", movie_source)

        # 电影描述
        movie_description = res_dict["summary"]
        # print("13描述：", movie_description)

        # 电影短评
        num_for_short = res_dict["comments_count"]
        # print("14短评数量：", num_for_short)

        meta_data = {}
        meta_data["url"] = url
        meta_data["name"] = movie_name
        meta_data["scriptwriters"] = movie_scriptwriters
        meta_data["directors"] = movie_directors
        meta_data["actors"] = movie_actors
        meta_data["type"] = movie_type
        meta_data["region"] = movie_region
        meta_data["language"] = movie_language
        meta_data["duration"] = movie_duration
        meta_data["release_date"] = movie_release_date
        meta_data["alias"] = movie_alias
        meta_data["source"] = movie_source
        meta_data["description"] = movie_description
        meta_data["num_for_short"] = num_for_short
        meta_data["id"] = response.meta["id"]
        content_url = self.short_url.format(response.meta["id"], 20)
        yield Request(url=content_url, meta=meta_data, callback=self.parse_short, headers=self.short_headers)

    def parse_short(self, response):
        meta = deepcopy(response.meta)
        short_answers, recommendation_index, useful_num = [], [], []
        num_for_short = meta["num_for_short"] if meta["num_for_short"] < 501 else 500
        for count in range(0, num_for_short, 20):
            short_url = self.short_url.format(meta["id"], count)
            print("short_url", short_url)
            try:
                res = self.get_shorturl_content(short_url)
                if len(re.findall(r'"code":112', str(res))) > 0:
                    self.crawler.engine.close_spider(self, '程序异常，停止爬虫!')
                    print('！！！111程序异常，停止爬虫！！！，状态码是：', response.status)
                else:
                    short_answers_temp = [emoji.demojize(i["content"]) for i in res["comments"]]
                    recommendation_index_temp = [i["rating"]["value"] for i in res["comments"]]
                    useful_num_temp = [i["useful_count"] for i in res["comments"]]
                    short_answers.extend(short_answers_temp)
                    recommendation_index.extend(recommendation_index_temp)
                    useful_num.extend(useful_num_temp)
            except Exception as e:
                logger.info(e)
                continue
        info = DoubanSpiderItem()
        info["url"] = meta["url"]
        info["movie_id"] = meta["id"]
        info["name"] = meta["name"]
        info["scriptwriters"] = meta["scriptwriters"]
        info["directors"] = meta["directors"]
        info["actors"] = meta["actors"]
        info["type"] = meta["type"]
        info["region"] = meta["region"]
        info["language"] = meta["language"]
        info["duration"] = meta["duration"]
        info["release_date"] = meta["release_date"]
        info["alias"] = meta["alias"]
        info["source"] = meta["source"]
        info["description"] = meta["description"]
        info["short_answers"] = short_answers
        info["recommendation_index"] = recommendation_index
        info["useful_num"] = useful_num
        yield info


    def parse_question_url(self, response):
        url = response.url
        print("222parse_question_url", url)
        meta = deepcopy(response.meta)
        question_title, question_content, answers = "", "", []
        html_str = response.body.decode()
        question_info = {}

        question_title = etree.HTML(html_str).xpath("//h1[@class='clone-h1']/text()")[0].strip().replace("\n", "")

        question_content = "".join(
            etree.HTML(html_str).xpath("//div[@id='question-content']//text()")).strip().replace("\n", "")

        answers_divs = etree.HTML(html_str).xpath("//div[@class='answer']")
        for div in answers_divs:
            time.sleep(0.5)
            one_answer = {}
            answer_block_id = div.xpath("./@id")[0].split("-")[-1]
            answer_str = "".join(div.xpath(".//div[@class='content-text']//text()")).strip().replace("\n", "")

            second_answer_html = requests.get(
                url.replace("?from=subject_questions", "answers/{}/comments/?start=0".format(answer_block_id))).text

            second_answer_list = re.findall('"text":"(.*?),"created', str(second_answer_html))

            one_answer["first_floor"] = answer_str
            one_answer["second_floor"] = [emoji.demojize(i) for i in second_answer_list]

            answers.append(one_answer)

        question_info = QuestionInfo()
        question_info["movie_id"] = meta["id"]
        question_info["url"] = url
        question_info["question_title"] = question_title
        question_info["question_content"] = question_content
        question_info["answers"] = answers
        yield question_info