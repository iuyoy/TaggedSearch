#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
import sys,os
import urllib2
import lxml.html

sys.path.append('..')
from Scripts.db_op import Db_op as DB
from Scripts.code import print_whatever_code as printout
from wikidata_api import Wikidata_api
from ini import *
from data_processing import *

#Wikidata_parse:解析一个页面,其实就是得到具体item的内容
class Wikidata_parse(Wikidata_api):
    url = 'https://www.wikidata.org/w/api.php'

    #page为具体访问的界面,是wikidata页面的title
    #对于内容是item的，page为Q+数字串，
    #对于内容是property的，page为Property:P+数字串
    parameters = {\
    'action':'parse'\
    ,'format':'xml'\
    ,'uselang':'zh'\
    ,'prop':'wikitext'\
    ,'contentmodel':'wikitext'\
    ,'page':'q468777'\
    }

    def __init__(self,page = ''):
        if page != '':
            self.set_para_page(page)
    #根据page获取item内容并提取需要的信息存入数据库
    def run(self,page = ''):
        url = self.generate_url(page)
        xml = super(Wikidata_parse, self).connect(url)
        data_process = Get_specific_info()
        wiki_dict = self.xml_process(xml)
        ret = data_process.run(wiki_dict)
        return ret
        
    def xml_process(self,xml=''):
        #try:
        doc = lxml.etree.HTML(xml.lower().decode('utf-8'))
        wikitext = doc.xpath('//wikitext/text()')
        if(len(wikitext)>0):
            wikitext[0] = wikitext[0].replace(":null,",":'',")
            wiki_dict = eval(wikitext[0])
            return wiki_dict
        else:
            return []
        #except:
            #print ('Translate wikitext to python_dict error.\n')
            #return []
    #根据wikidata:parse生成url
    def generate_url(self,page = ''):
        if(page != ''):
            self.set_para_page(page)
        return super(Wikidata_parse, self).generate_url()
    #设置参数page
    def set_para_page(self,page = 'q468777'):
        super(Wikidata_parse, self).update_parameter('page',page)
    def __del__(self):
        return 

#根据parse_queue来进行解析
class Parse_Orderly(object):
    db = DB(dbinfo = dbinfo)
    def __init__(self):
        super(Parse_Orderly,self).__init__()
    def run(self):
        while (not parse_queue.empty()):
            wikidata_id = parse_queue.get()
            if (not self.is_entity_in_db(wikidata_id)):
                printout("  Sub Wikidata_parse:%s is running." %(wikidata_id)) 
                WP = Wikidata_parse(wikidata_id)
                ret = WP.run()
            else:
                printout("  Wikidata_entity:%s has been inserted into db." %(wikidata_id)) 
                ret = True
        return True
    #wikidata实体是否存入数据库
    def is_entity_in_db(self,wikidata_id):
        self.db.connect()
        wikidata_id = self.db.SQL_filter(wikidata_id)
        sql = "SELECT is_ok FROM `%s` WHERE wikidata_id = '%s'" %(wikidata_entities_table,wikidata_id)
        result = self.db.select(sql)
        is_ok = 0
        if (result == True):
            is_ok = self.db.fetchOneRow()[0]
        self.db.close()
        #print sql,is_ok,result
        if (is_ok != 1):
            return False
        return True
        
if __name__ == '__main__':
    test = Wikidata_parse('Q2095')
    test.run()