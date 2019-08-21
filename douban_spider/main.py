# -*- coding: utf-8 -*-
from scrapy import cmdline

# cmdline.execute("scrapy crawl douban -s JOBDIR=./jobdir".split())
cmdline.execute("scrapy crawl douban".split())
# cmdline.execute("scrapy crawl question".split())
# cmdline.execute("scrapy crawl discussion".split())
