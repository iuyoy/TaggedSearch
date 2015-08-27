#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
import sys,os
import re

from ini import *
from Scripts.code import print_whatever_code as printout
from data_save import Data_save_by_file
from data_save import Data_save_by_db as DBSAVE

reload(sys)
sys.setdefaultencoding('utf-8')
#数据处理
class Get_specific_info(object):
    #实体格式{实体名:[标签名]}
    entity_format = {'':['']}
    #分析时的格式{实体名:{属性名:[疑似标签名]}}
    #analyse_format = {'type':'','id':'','labels':[],'descriptions':[],'aliases':[]\
     #   ,u'主分类':[],u'父类':[],u'性质':[],u'属于':[]} 
    analyse_format = {'type':'','id':'','labels':[],'descriptions':[],'aliases':[]\
        ,u'main_classification':[],'father_classification':[],'property':[],'belong_to':[]} 
    #labels = ['zh-hans','zh-cn','zh','en']
    #descriptions = ['zh-hans','zh-cn','zh']
    #aliases = ['zh-hans','zh-cn','zh']
    #claims = {'p910':'主分类','p279':'父类','p31':'性质','p361':'属于'}
    properties = ['mainsnak','datavalue','value',['entity-type','numeric-id']]
    keys = {'type':'','id':'','labels':['zh-hans','zh-cn','zh','en'],'descriptions':['zh-hans','zh-cn','zh'],'aliases':['zh-hans','zh-cn','zh'],'claims':{'p910':u'main_classification','p279':u'father_classification','p31':u'property','p361':u'belong_to'}}
    def __init__(self):
        super(Get_specific_info,self).__init__()
    #提取可能的标签,并且保存到数据库中
    def run(self,wiki_dict):
        if type(wiki_dict) == dict:
            self.traverse_list(wiki_dict)
            return self.save_entity()
        else:
            printout ('No wiki_data(dict)',2)
            return False
    def traverse_list(self,wiki_dict):
        self.reset_analyse_format()
        for key in self.keys:
            if (wiki_dict.has_key(key)):
                if(key == 'type' or key == 'id'):
                    self.analyse_format[key] = wiki_dict[key]
                elif(key == 'labels' or key == 'descriptions'):
                    for sub_key in self.keys[key]:
                        if (type(wiki_dict[key]) == dict and wiki_dict[key].has_key(sub_key) and wiki_dict[key][sub_key]['value'].decode('raw_unicode_escape') not in  self.analyse_format[key]):
                            self.analyse_format[key].append(wiki_dict[key][sub_key]['value'].decode('raw_unicode_escape'))
                        elif(type(wiki_dict[key]) == list and wiki_dict[key]!=[]):
                            self.save_error(str(wiki_dict['id'])+":"+str(wiki_dict[key])+'\n')
                elif(key == 'aliases'):
                    for sub_key in self.keys[key]:
                        if (type(wiki_dict[key]) == dict and wiki_dict[key].has_key(sub_key)):
                            for sub_dict in wiki_dict[key][sub_key]:
                                if(sub_dict['value'].decode('raw_unicode_escape') not in self.analyse_format[key]):
                                    self.analyse_format[key].append(sub_dict['value'].decode('raw_unicode_escape'))
                        elif (type(wiki_dict[key]) == list and wiki_dict[key] != []):
                            self.save_error(str(wiki_dict['id'])+":"+str(wiki_dict[key])+'\n')
                elif(key == 'claims'):
                    for sub_key in self.keys[key]:
                        if (type(wiki_dict[key]) == dict and wiki_dict[key].has_key(sub_key)):
                            for sub_dict in wiki_dict[key][sub_key]:
                                mainsnak = sub_dict['mainsnak']
                                if (mainsnak.has_key('datavalue')):
                                    entity_type = sub_dict['mainsnak']['datavalue']['value']['entity-type']
                                    if (entity_type == 'item'):
                                        value = 'q'+str(sub_dict['mainsnak']['datavalue']['value']['numeric-id'])
                                        parse_queue.put(value)
                                    else:
                                        value = sub_dict['mainsnak']['datavalue']['value']['numeric-id']
                                    if(value not in self.analyse_format[self.keys[key][sub_key]]):
                                        self.analyse_format[self.keys[key][sub_key]].append(value)
                        elif (type(wiki_dict[key]) == list and wiki_dict[key] != []):
                            self.save_error(str(wiki_dict['id'])+":"+str(wiki_dict[key])+'\n')


    def save_entity(self):
        save = DBSAVE()
        return save.save_entity(self.analyse_format)

    def save_error(self,error_info):
        fp = open('error_log.txt','a')
        fp.write(error_info)

    def reset_analyse_format(self):
         self.analyse_format = {'type':'','id':'','labels':[],'descriptions':[],'aliases':[]\
        ,u'main_classification':[],'father_classification':[],'property':[],'belong_to':[]} 

if __name__ == '__main__':
    print (help(Get_specific_info))

       