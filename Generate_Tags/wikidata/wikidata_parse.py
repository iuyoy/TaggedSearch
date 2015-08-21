#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
import sys,os
import urllib2
import lxml.html

from wikidata_api import Wikidata_api

reload(sys)
sys.setdefaultencoding('utf-8')

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
    #封装的一系列操作
    def run(self,page = ''):
        try:
            url = self.generate_url(page)
            xml = super(Wikidata_parse, self).connect(url)
            return self.xml_process(xml)
        except:
            print ('Parameter page is missing.\n')
            return []
    #对获得的xml的处理，返回dict类型
    def xml_process(self,xml=''):
        try:
            doc = lxml.etree.HTML(xml.lower().decode('utf-8'))
            wikitext = doc.xpath('//wikitext/text()')
            wiki_dict = eval(wikitext[0])
            return wiki_dict
        except:
            print ('Translate wikitext to python_dict error.\n')
            return []
    #根据wikidata:parse生成url
    def generate_url(self,page = ''):
        if(page != ''):
            self.set_para_page(page)
        return super(Wikidata_parse, self).generate_url()
    #设置参数page
    def set_para_page(self,page = 'q468777'):
        super(Wikidata_parse, self).update_parameter('page',page)


if __name__ == '__main__':
    test = Wikidata_parse('Q89')
    test.run()