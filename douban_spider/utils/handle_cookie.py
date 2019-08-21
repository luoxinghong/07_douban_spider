#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: 罗兴红
@contact: EX-LUOXINGHONG001@pingan.com.cn
@file: get_cookie.py
@time: 2019/4/15 11:31
@desc:
'''

CK_STR = '''bid=n8D0CAmDZn8; __utmc=223695111; __yadk_uid=AzOrEYwOvGNusFEMLaZoLp7pFtyVNrDq; push_noty_num=0; _vwo_uuid_v2=D92860BADCF2D7FEA9B7C7D7F4EEB1DAC|85c2cc5dacba53db38c28d2af20dc17d; ll="118282"; __utmc=30149280; __utmv=30149280.17094; ct=y; push_doumail_num=0; douban-fav-remind=1; __utmz=223695111.1554874378.87.20.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; ap_v=0,6.0; __utma=223695111.1607107514.1550564051.1554879619.1554944595.89; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1554947540%2C%22https%3A%2F%2Faccounts.douban.com%2Fpassport%2Flogin%22%5D; _pk_id.100001.4cf6=84d1e668b4fe5d05.1550564050.86.1554947540.1554944594.; _pk_ses.100001.4cf6=*; ps=y; __utma=30149280.1945138724.1550718447.1554944595.1554947663.87; __utmz=30149280.1554947663.87.26.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/safety/unlock_sms/resetpassword; __utmt=1; __utmb=30149280.1.10.1554947663; dbcl2="170940426:TVv8NLHdzMA"; ck=XwaC'''


def get_cookie(cookie_str):
    COOKIE_DICT = {i.split("=")[0]: i.split("=")[-1] for i in CK_STR.split("; ")}
    return COOKIE_DICT