#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
"""
crawl在工程外部执行
感觉中文有些编码问题
ceshiceshi
"""
import sys,os
import time

from twisted.internet import reactor
import scrapy
from scrapy.crawler import Crawler,CrawlerProcess,CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.settings import Settings
from sp_cnbeta.sp_cnbeta.spiders.sp_cnbeta_id import sp_cnbeta_id
from sp_cnbeta.sp_cnbeta.spiders.sp_cnbeta_main import sp_cnbeta_main
from scrapy.utils.project import get_project_settings


class run_sp_cnbeta(object):
    def __init__(self):
        super(run_sp_cnbeta,self).__init__()
    def run(self):
        process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
        process.crawl(sp_cnbeta_id)
        process.start() # the script will block here until the crawling is finished
    def stop(self):
        reactor.stop()
class run_spcnbeta_main(object):
    def __init__(self):
        super(run_spcnbeta_main,self).__init__()
    def run(self):
        process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)','ITEM_PIPELINES' : {'sp_cnbeta.sp_cnbeta.pipelines.SpCnbetaPipeline':300}})
        #process = CrawlerProcess(get_project_settings())
        process.crawl(sp_cnbeta_main)
        process.start() # the script will block here until the crawling is finished
if __name__ == "__main__":
    #a = run_sp_cnbeta()
    #a.run()
    #time.sleep(5)
    #a.stop()
    a = run_spcnbeta_main()
    a.run()