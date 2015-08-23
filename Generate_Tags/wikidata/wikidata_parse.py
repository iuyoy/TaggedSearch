#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
import sys,os
import urllib2
import lxml.html

sys.path.append('..')
from Scripts.db_op import Db_op as DB
from wikidata_api import Wikidata_api
from ini import *
from Generate_Tags.data_processing import *

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
        #try:
        url = self.generate_url(page)
        xml = super(Wikidata_parse, self).connect(url)
        print ("Wikidata_Parse:%s") %(self.parameters['page'])
        data_process = Get_specific_info()
        wiki_dict = self.xml_process(xml)
        ret = data_process.run(wiki_dict)
        return ret
        #except:
            #print ('Parameter page is missing.\n')
            #return False
    #对获得的xml的处理，返回dict类型
    def xml_process(self,xml=''):
        #try:
        doc = lxml.etree.HTML(xml.lower().decode('utf-8'))
        wikitext = doc.xpath('//wikitext/text()')
        wikitext[0] = wikitext[0].replace(":null,",":'',")
        wiki_dict = eval(wikitext[0])
        return wiki_dict
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
#根据parse_stack来进行解析
class Parse_stackly(object):
    db = DB(dbinfo = dbinfo)
    def __init__(self):
        super(Parse_stackly,self).__init__()
        
    def run(self):
        print 'wikidata_parse',parse_stack
        while (parse_stack != []):
            wikidata_id = parse_stack.pop()
            if (not self.is_entity_in_db(wikidata_id)):
                WP = Wikidata_parse(wikidata_id)
                ret = WP.run()
                print 'current',parse_stack
            else:
                print ("Entity %s has been parsed.") %(wikidata_id.upper())

    def is_entity_in_db(self,wikidata_id):
        self.db.connect()
        wikidata_id = self.db.SQL_filter(wikidata_id)
        sql = "SELECT is_ok FROM `%s` WHERE wikidata_id = '%s'" %(wikidata_entities_table,wikidata_id)
        result = self.db.select(sql)
        is_ok = 0
        if (result == True):
            is_ok = self.db.fetchOneRow()[0]
        #print sql,is_ok,result
        if (is_ok != 1):
            return False
        return True
        self.db.close()

if __name__ == '__main__':
    test = Wikidata_parse('Q89')
    test.run()