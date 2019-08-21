#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: 罗兴红
@contact: EX-LUOXINGHONG001@pingan.com.cn
@file: demo2.py
@time: 2019/2/21 16:06
@desc:
'''
import requests
import re
import time
import random
import string
from urllib.parse import quote
import shutil


headers = {'Host': 'api.douban.com',
           'Connection': 'keep-alive',
           'Cache-Control': 'no-cache',
           'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
           }
url_temp = "https://api.douban.com/v2/movie/search?q={}&apikey=0b2bdeda43b5688921839c8ecb20399b&start=0&count=10"


def get_proxy_ip():
    return "http://" + requests.get("http://127.0.0.1:8090/get/").content.decode()

file = open("./movie_name.txt", "r", encoding="utf-8")

for i, line in enumerate(file.readlines()):
    print(i, line.replace("\n", ""))

    url = quote(url_temp.format(line.replace("\n", "")), safe=string.printable)
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code == 200:
        if len(re.findall(r'"https:\\/\\/movie.douban.com\\/subject\\/(.*?)\\/", "id":',
                          response.content.decode())) > 0:
            movie_id = re.findall(r'"https:\\/\\/movie.douban.com\\/subject\\/(.*?)\\/", "id":',
                                  response.content.decode())[0]
            print(movie_id)
            print("*" * 50)
            with open("movie_id.txt", "a") as f:
                f.write(str(movie_id) + "\n")
                f.close()
        else:
            with open("no_search_result.txt", "a") as g:
                g.write(str(i + 1) + line)
                g.close()
    else:
        print("爬虫异常停止", response.status_code)
        break
