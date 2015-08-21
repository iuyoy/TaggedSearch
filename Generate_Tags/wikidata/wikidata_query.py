#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
import sys,os

import urllib2
import lxml.html

import queryitem
from wikidata_api import Wikidata_api
reload(sys)
sys.setdefaultencoding('utf-8')

#
class Wikidata_query(Wikidata_api):
    url = 'https://www.wikidata.org/w/api.php'
    #srsearcch是搜索的内容
    parameters = {\
    'action':'query'\
    ,'format':'xml'\
    ,'uselang':'zh'\
    ,'list':'search'\
    ,'srsearch':'apple'\
    ,'srnamespace':'0'\
    ,'sroffset':'0'\
    ,'totalhits':'0'\
    ,'srlimit':'50'\
    ,'srprop':'size|wordcount|timestamp|snippet'
    #srprop = 'size|wordcount|timestamp|snippet|titlesnippet|redirecttitle|redirectsnippet|sectiontitle|sectionsnippet|isfilematch|categorysnippet'
    ,'rawcontinue':''\
    }
    result = queryitem.Queryitemlist()
    def __init__(self,srsearch = ''):
        if (srsearch != ''):
            self.set_srsearch(srsearch)
    #封装的一系列操作
    def run(self,srsearch='apple'):
        try:
            while (int(self.parameters['sroffset']) <= int(self.parameters['totalhits'])):
                url = self.generate_url(srsearch)
                xml = super(Wikidata_query, self).connect(url)
                self.xml_process(xml)
        except:
            print 'Parameter sroffeset or Parameter totalhits are missing.'
    #对获得的xml的处理
    def xml_process(self,xml=''):
        doc = lxml.etree.HTML(xml.lower().decode('utf-8'))
        totalhits = doc.xpath('//query/searchinfo/@totalhits')
        sroffset = doc.xpath('//query-continue/search/@sroffset')
        if totalhits != []:
            self.set_totalhits(totalhits[0])
        else:
            self.set_totalhits(0)
        if sroffset != []:
            self.set_sroffset(sroffset[0])
        else:
            self.set_sroffset(int(self.parameters['totalhits'])+1)
        self.result.setxml(doc)
        self.result.setlist()
    #根据wikidata:query生成url
    def generate_url(self,srsearch = '',sroffset = ''):
        if (srsearch != ''):
            self.set_srsearch(srsearch)
        if (sroffset != ''):
            self.set_sroffset(sroffset)
        return super(Wikidata_query, self).generate_url()

    #设置参数srsearch
    def set_srsearch(self,srsearch='apple'):
        super(Wikidata_query, self).update_parameter('srsearch',srsearch)
    #设置参数sroffset
    def set_sroffset(self,sroffset = '0'):
        super(Wikidata_query, self).update_parameter('sroffset',sroffset)
    #设置参数totalhits
    def set_totalhits(self,totalhits):
        super(Wikidata_query, self).update_parameter('totalhits',totalhits)

    def __del__(self):
        return 
if __name__ == "__main__":
    rm = Wikidata_query()
    rm.run(u'苹果')
    print rm.parameters['totalhits']
    print rm.parameters['sroffset']
    print len(rm.result.itemlist)
    for i in rm.result.itemlist:
        print i['title']