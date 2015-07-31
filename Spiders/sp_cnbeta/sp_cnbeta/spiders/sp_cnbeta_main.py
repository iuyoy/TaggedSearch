"""
≈¿»°Œƒ’¬
"""
import scrapy
import os,sys

sys.path.append('..')
from Scripts.ini_op import INI
from sp_cnbeta.sp_cnbeta.items import SpCnbetaItem
from scrapy.selector import Selector
try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle

class sp_cnbeta_main(CrawlSpider):
    name = "cnbeta1"
    allow_domains = ["cnbeta.com"]
    start_urls = ["http://m.cnbeta.com/wap/"]
        
    def parse(self, response):
        item = SpCnbetaItem()
        item['title'] = response.xpath('//title/text()').extract()
        item['links'] = response.xpath('//div/a/@href').extract()
        print item['links'][0]
        #ini.write('cnbeta','lastest','')
        yield item
    def get_latest_id(self):
        ini=INI("cnbeta.ini")
        latest_id = ini.getint('Spider1','latest')
        return latest_id
    def set_latest_id(self,latest_id):
        ini=INI("cnbeta.ini")
        ret = ini.set('Spider1','latest',latest_id)
        return ret