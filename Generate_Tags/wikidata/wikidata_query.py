#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
import sys,os

sys.path.append('..')
import urllib2
import lxml.html

import queryitem
from wikidata_api import Wikidata_api
from Scripts import db_op as DB
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
    #,'srprop':'size|wordcount|timestamp|snippet'
    #srprop = 'size|wordcount|timestamp|snippet|titlesnippet|redirecttitle|redirectsnippet|sectiontitle|sectionsnippet|isfilematch|categorysnippet'
    ,'rawcontinue':''\
    }
    result = queryitem.Queryitemlist()
    def __init__(self,srsearch = ''):
        if (srsearch != ''):
            self.set_srsearch(srsearch)
    #检出一次结果
    def run(self,srsearch='apple'):
        if(not self.is_complete()):
            self.result.clear()
            url = self.generate_url(srsearch)
            xml = super(Wikidata_query, self).connect(url)
            self.xml_process(xml)
            print ("        end with %d total %d") %(int(self.parameters['sroffset'])-1,int(self.parameters['totalhits']))
            
     #将结果全部检出, 当数据过大时，返回'big'
    def run_all(self,srsearch='apple',big_return = 0):
        self.result.clear()
        self.reset_parameters()
        while (not self.is_complete()):
            url = self.generate_url(srsearch)
            xml = super(Wikidata_query, self).connect(url)
            self.xml_process(xml)
            if(big_return != 0 and int(self.parameters['totalhits'])>big_return):
                return 'big'
            if(int(self.parameters['totalhits']) > 0):
                print ("        end with %d total %d") %(int(self.parameters['sroffset'])-1,int(self.parameters['totalhits']))
            else:
                return []
        return self.result.itemlist
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
    
    def is_complete(self):
        return (int(self.parameters['sroffset']) >= int(self.parameters['totalhits']))&(int(self.parameters['sroffset']) > 0)

    #设置参数srsearch
    def set_srsearch(self,srsearch='apple'):
        super(Wikidata_query, self).update_parameter('srsearch',srsearch)
    #设置参数sroffset
    def set_sroffset(self,sroffset = '0'):
        super(Wikidata_query, self).update_parameter('sroffset',sroffset)
    #设置参数totalhits
    def set_totalhits(self,totalhits):
        super(Wikidata_query, self).update_parameter('totalhits',totalhits)
    def reset_parameters(self):
       self.parameters = {\
    'action':'query'\
    ,'format':'xml'\
    ,'uselang':'zh'\
    ,'list':'search'\
    ,'srsearch':'apple'\
    ,'srnamespace':'0'\
    ,'sroffset':'0'\
    ,'totalhits':'0'\
    ,'srlimit':'50'\
    #,'srprop':'size|wordcount|timestamp|snippet'
    #srprop = 'size|wordcount|timestamp|snippet|titlesnippet|redirecttitle|redirectsnippet|sectiontitle|sectionsnippet|isfilematch|categorysnippet'
    ,'rawcontinue':''\
    }
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