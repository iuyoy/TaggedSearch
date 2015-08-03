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
try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider

class sp_cnbeta_id(Spider):
    name = "sp_cnbeta_id"
    allow_domains = ["cnbeta.com"]
    start_urls = ["http://m.cnbeta.com/wap/"]
        
    def parse(self, response):
        links = response.xpath('//div/a/@href').extract()
        print ("最新文章链接:"+str(links[0]))
        id = self.get_id(links[0])
        print ("最新的文章:"+str(links[0]))
        self.set_latest_id(id)
        pass

    def get_id(self,id):
        pattern = re.compile(u'_(\d+)\.')
        rs = pattern.search(id)
        if rs != None:
            return rs.groups()[0]

    def set_latest_id(self,latest_id):
        ini=INI("cnbeta.ini")
        ret = ini.write('Spider1','latest',latest_id)
        return ret