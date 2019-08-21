# -*- coding: utf-8 -*-
BOT_NAME = 'douban_spider'
SPIDER_MODULES = ['douban_spider.spiders']
NEWSPIDER_MODULE = 'douban_spider.spiders'

##### ==============================自己定义的配置==============================
# 定义scraoy日志的目录，等级，名字
import datetime

to_day = datetime.datetime.now()
log_file_path = "./logs/{}_{}_{}.log".format(to_day.year, to_day.month, to_day.day)
LOG_LEVEL = "INFO"
LOG_FILE = log_file_path

ROBOTSTXT_OBEY = False

DOWNLOADER_MIDDLEWARES = {
    'douban_spider.middlewares.RandomUserAgentMiddleware': 2,
    'douban_spider.middlewares.DoubanSpiderSpiderMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # 这里要设置原来的scrapy的useragent为None，否者会被覆盖掉
    # 'douban_spider.middlewares.ProxyMiddleware': 542,  # 添加自己搭建的代理IP
    # 'douban_spider.middlewares.ABProxyMiddleware': 1,
}

# 增加爬虫速度及防ban配置
DOWNLOAD_DELAY = 0
DOWNLOAD_FAIL_ON_DATALOSS = False
CONCURRENT_REQUESTS = 5
CONCURRENT_REQUESTS_PER_DOMAIN = 5
CONCURRENT_REQUESTS_PER_IP = 5
COOKIES_ENABLED = False
DOWNLOAD_TIMEOUT = 60


#配置自己重写的RFPDupeFilter
DUPEFILTER_CLASS = 'douban_spider.middlewares.URLRedisFilter'

# 开启item_pipelines，入库
ITEM_PIPELINES = {
    'douban_spider.pipelines.DoubanSpiderPipeline': 300,
}

# msyql数据库配置
MYSQL_HOST = "localhost"
MYSQL_DBNAME = "douban"
MYSQL_USER = "root"
MYSQL_PASSWD = "lxh123"
MYSQL_PORT = 3306

# redis数据库配置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWD = "lxh123"
REDIS_DBNAME = 0
REDIS_KEY = "douban_moive"


# 配置user_agent的随机类型
RANDOM_UA_TYPE = 'random'

# 禁止重定向
# REDIRECT_ENABLED = False

# 允许状态码301
# HTTPERROR_ALLOWED_CODES = [301,302,403,404]


SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}


# 阿布云动态ip默认是1秒钟请求5次，（可以加钱，购买多次）。所以，当他是默认5次的时候，我需要对爬虫进行限速
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.2
# #  利用自带的retry设置重试次数
# RETRY_ENABLED = True
# RETRY_TIMES = 5
#RETRY_HTTP_CODECS= []
