#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: 罗兴红
@contact: EX-LUOXINGHONG001@pingan.com.cn
@file: tes.py
@time: 2019/3/14 10:51
@desc:
'''

# movie_id.txt 为根据电影名爬取的所有id
# movie_id2.txt  为到目前为止已爬取的全部id
# movie_id_total.txt   movie_id.txt不在movie_id2.txt的id

file = open("./movie_id2.txt", encoding="utf-8")
file2 = open("./movie_id_total.txt", encoding="utf-8")
l = file.readlines()
l2 = file2.readlines()

for i in l2:
    if i not in l:
        print(i.replace("\n",""))
