#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: 罗兴红
@contact: EX-LUOXINGHONG001@pingan.com.cn
@file: filter_emoji_blank.py
@time: 2019/4/15 10:56
@desc:
'''
import emoji
import re


def filter_str_emoji_blank(destr):
    destr_temp = emoji.demojize(destr)
    return re.sub("&.*?gt;"," ",destr_temp.strip().strip("\r\n").replace(u"\u3000", u"").replace(u"\xa0", u"").replace("&lt;p&gt;","").replace("&lt;/p&gt;",""))





if __name__ == '__main__':
    str = "fasfa\uE056\uE057"
    print(str)
    print(filter_str_emoji_blank(str))

