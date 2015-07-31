"""
获取最新的文章数
"""
import scrapy
import os,sys

sys.path.append('..')
from Scripts.ini_op import INI
try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider

class sp_cnbeta_1(Spider):
    name = "cnbeta1"
    allow_domains = ["cnbeta.com"]
    start_urls = ["http://m.cnbeta.com/wap/"]
        
    def parse(self, response):
        links = response.xpath('//div/a/@href').extract()
        print links[0]
        #ini.write('cnbeta','lastest','')
        pass

    def get_latest_id(self):
        ini=INI("cnbeta.ini")
        latest_id = ini.getint('Spider1','latest')
        return latest_id

    def set_latest_id(self,latest_id):
        ini=INI("cnbeta.ini")
        ret = ini.set('Spider1','latest',latest_id)
        return ret