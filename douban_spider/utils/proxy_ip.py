#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: 罗兴红
@contact: EX-LUOXINGHONG001@pingan.com.cn
@file: proxy_ip.py
@time: 2019/4/15 10:48
@desc:
'''
import requests
from fake_useragent import UserAgent


# 自己在百度云上搭建的免费代理ip池（PS:效果不佳）
def get_proxy_ip(self):
    ip_port = requests.get("http://106.12.8.109:8000/get/").content.decode()
    proxies = {"http": "http://" + ip_port}
    return proxies


# 阿布云代理HTTP隧道动态版
def get_aby_ip():
    """ 阿布云ip代理配置，包括账号密码 """
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"
    proxyUser = "HK2H176QG3F017VD"
    proxyPass = "28AE3DE6C65753A5"
    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies


if __name__ == '__main__':
    aby_proxy = get_aby_ip()
    print(aby_proxy)
    url = 'https://movie.douban.com/subject/1301720/discussion/1009429/'
    html = requests.get(url, proxies=aby_proxy)
    print(html.status_code)
