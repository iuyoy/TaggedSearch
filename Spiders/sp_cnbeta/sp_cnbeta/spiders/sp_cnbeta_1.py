#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
"""
获取最新的文章数
"""
import scrapy
import os,sys
import re

sys.path.append('..')
from Scripts.ini_op import INI
from scrapy.spider import *

class sp_cnbeta_1(Spider):
    name = "cnbeta1"
    allow_domains = ["cnbeta.com"]
    start_urls = ["http://m.cnbeta.com/wap/"]
        
    def parse(self, response):
        links = response.xpath('//div/a/@href').extract()
        print links[0]
        pattern = re.compile('_(\d+)\.')
        rs = pattern.search(links[0])
        if rs != None:
            id = rs.groups()[0]
            print id
        self.set_latest_id(id)
        pass

    def get_latest_id(self):
        ini=INI("cnbeta.ini")
        latest_id = ini.readint('Spider1','latest')
        return latest_id

    def set_latest_id(self,latest_id):
        ini=INI("cnbeta.ini")
        ret = ini.write('Spider1','latest',latest_id)
        return ret