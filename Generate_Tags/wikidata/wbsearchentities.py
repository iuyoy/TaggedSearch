#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import sys,os

sys.path.append('..')
import urllib2
import lxml.html

from wikidata_api import Wikidata_api

class Wbsearchentities(Wikidata_api):
    parameters = {\
        'action':'wbsearchentities'\
        ,'search':'苹果'\
        ,'language':'zh'\
        ,'limit':'50'\
        ,'format':'xml'
        ,'continue':'0'
        }
    result = []
    def __init__(self, search = ''):
        if (search !=''):
            self.set_search(search)
    def run(self,search = '苹果'):
        self.reset()
        while(not self.is_complete()):
            url = self.generate_url(search)
            xml = super(Wbsearchentities, self).connect(url)
            self.xml_process(xml)
        return self.result

    def xml_process(self,xml=''):
        doc = lxml.etree.HTML(xml.lower().decode('utf-8'))
        is_success = doc.xpath('//api/@success')
        search_continue = doc.xpath('//api/@search-continue')

        if('1' not in is_success or search_continue == []):
            self.set_continue(-1)#表示没有下一页结果了
        else:
            self.set_continue(search_continue[0])

        for entity in doc.xpath('//search/entity'):
            if ('label' in entity.xpath('match/@type') or 'alias' in entity.xpath('match/@type')):
                self.set_result(entity)

    #加入结果集
    def set_result(self,entity):
        self.result.append(entity.attrib)

    #根据wikidata:wbsearchentities生成url
    def generate_url(self,search = ''):
        if (search != ''):
            self.set_search(search)
        return super(Wbsearchentities, self).generate_url()
    #查询是否完成
    def is_complete(self):
        if('continue' not in self.parameters or int(self.parameters['continue'])<0):
            return True
        return False

    #恢复整体初始状态
    def reset(self):
        self.reset_parameters()
        self.clear_result()
    #恢复参数初始状态
    def reset_parameters(self):
        self.parameters = {\
        'action':'wbsearchentities'\
        ,'search':'苹果'\
        ,'language':'zh'\
        ,'limit':'50'\
        ,'format':'xml'
        ,'continue':'0'
        }
    #清空结果集
    def clear_result(self):
        self.result = []
    #设置参数search
    def set_search(self,search):
        super(Wbsearchentities, self).update_parameter('search',search)
    #设置参数continue
    def set_continue(self,num):
        try:
            super(Wbsearchentities, self).update_parameter('continue',str(int(num)))
        except:
            print ('Parameter continue need to be number.')
if __name__ == '__main__':
    ws = Wbsearchentities()
    ws.run('苹果')