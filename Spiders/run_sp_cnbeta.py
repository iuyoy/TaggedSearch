#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
"""
crawl�ڹ����ⲿִ��
�о�������Щ��������
ceshiceshi
"""
from twisted.internet import reactor
from scrapy.spider import *
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from sp_cnbeta.sp_cnbeta.spiders.sp_cnbeta_1 import sp_cnbeta_1

settings = Settings({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
runner = CrawlerRunner(settings)

d = runner.crawl(sp_cnbeta_1)
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until the crawling is finished