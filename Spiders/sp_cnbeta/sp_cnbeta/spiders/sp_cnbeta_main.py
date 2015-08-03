#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
"""
爬取文章
"""
import scrapy
import os,sys
import re
import time

sys.path.append('..')
#sys.path.append('D:/ROW/Code/GIT/TaggedSearch/')
#sys.path.append('D:/ROW/Code/GIT/TaggedSearch/Spiders/')
#sys.path.append('D:/ROW/Code/GIT/TaggedSearch/Spiders/sp_cnbeta/')
#sys.path.append('D:/ROW/Code/GIT/TaggedSearch/Spiders/sp_cnbeta/sp_cnbeta/')

from Scripts.ini_op import INI
from sp_cnbeta.sp_cnbeta.items import SpCnbetaItem
try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider

class sp_cnbeta_main(Spider):
    name = "sp_cnbeta_main"
    allow_domains = ["cnbeta.com"]
    current_id = 0
    latest_id = 0 
    #http://m.cnbeta.com/wap/view_416701.htm
    prefix = 'http://m.cnbeta.com/wap/view_'
    postfix = '.htm'
    def __del__(self):
        print "\nsave_id",self.current_id
        self.set_current_id(self.current_id)
    def start_requests(self):
        try:
            yield scrapy.Request("http://m.cnbeta.com/wap/",callback = self.parse_get_id)
        except:
            self.latest_id = self.get_latest_id()
        url = None
        self.current_id = self.get_current_id()
        print self.current_id,self.latest_id
        if (self.current_id <= self.latest_id - 2):
            if (self.current_id%2 == 0):
                self.current_id += 1
            else:
                self.current_id += 2
            url = self.joint_url(self.current_id)
            yield scrapy.Request(url,callback = self.parse)
    
    #default parse 
    def parse(self, response):
        #print "current_id:"+str(self.current_id)+"latest_id:"+str(self.latest_id)
        
        item = SpCnbetaItem()
        item['id'] = [self.current_id]
        item['url'] = [self.joint_url(self.current_id)]
        for section in response.xpath("//section[@class='clearfix']"):
            item['title'] = section.xpath("div[@class='title']/b/text()").extract()
            date = section.xpath("div[@class='time']/span[1]/text()").extract()[0]
            item['date'] = self.date_to_num(self.get_date_from_web(date))
            author = section.xpath("div[@class='time']/span/a/@href").extract()
            if author != []:
                item['author_url'] = author
                item['author_name'] = section.xpath("div[@class='time']/span/a/text()|div[@class='time']/span/a/span/text()").extract()
            else:
                item['author_url'] = []
                item['author_name'] = self.get_author(section.xpath("div[@class='time']/span[2]/text()").extract()[0])
            item['content'] = section.xpath("div[@class='content']/p/text()|/div[@class='content']/p/a/text()|/div[@class='content']/p/a/strong/text()").extract()
            item['picture'] = section.xpath("div[@class='content']/p/a/@href|/div[@class='content']/p/img/@src").extract()
            item['media'] = section.xpath("div[@class='content']/p/embed/@src|//div[@class='content']/p/iframe/@src").extract()
        #for i in item:
        #    print i,item[i][0]
        yield item
        if(self.current_id <= self.latest_id - 2):
            self.current_id += 2
            url = self.joint_url(self.current_id)
            yield scrapy.Request(url, callback = self.parse)
        else:
            self.__del__()

    #parse to get latest_id
    def parse_get_id(self, response):
        links = response.xpath('//div/a/@href').extract()
        print ("latest_url:"+str(links[0]))
        id = self.get_id(links[0])
        print ("latest_id:"+str(id))
        self.set_latest_id(id)
        self.latest_id = int(id)
        url = None
        self.current_id = self.get_current_id()
        print self.current_id,self.latest_id
        if (self.current_id <= self.latest_id - 2):
            if (self.current_id%2 == 0):
                self.current_id += 1
            else:
                self.current_id += 2
            url = self.joint_url(self.current_id)
            yield scrapy.Request(url,callback = self.parse)

    #change date to what we need
    def get_date_from_web(self,string): 
        pattern = re.compile('[:：]([0-9:\- ]+)')
        rs = pattern.search(string)
        if rs != None:
            return rs.groups()[0]
        else:
            return rs
    def date_to_num(self,date):
        try:
            return [time.mktime(time.strptime(date,'%Y-%m-%d %H:%M:%S'))]
        except:
            return []

    #change author_name to what we need
    def get_author(self,string):
        print string
        pattern = re.compile(u'[:：]([\d\D]+)')
        rs = pattern.search(string)
        print rs.groups()
        if rs != None:
            return rs.groups()
        else:
            return []
    
    def joint_url(self,id):
        return self.prefix+str(id)+self.postfix
    
    #get id by pattern
    def get_id(self,id):
        pattern = re.compile(u'_(\d+)\.')
        rs = pattern.search(id)
        if rs != None:
            return rs.groups()[0]
    #operate ini 
    def get_latest_id(self):
        ini=INI("cnbeta.ini")
        latest_id = ini.readint('Spider1','latest')
        return latest_id
    def set_latest_id(self,latest_id):
        ini=INI("cnbeta.ini")
        ret = ini.write('Spider1','latest',latest_id)
        return ret

    def get_current_id(self):
        ini=INI("cnbeta.ini")
        current_id = ini.readint('Spider1','current')
        return current_id
    def set_current_id(self,current_id):
        ini=INI("cnbeta.ini")
        ret = ini.write('Spider1','current',current_id)
        return ret