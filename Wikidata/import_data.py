#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import os,sys
sys.path.append(sys.path[0]+'/..')
import time
from Global.config import *
from Global.db_op import Db_op as DB
from Global.global_function import printout

from Tagged.get_data import Get_entity

class wikidata(object):
    db = DB(dbinfo = dbinfo)
    main_keys = ('labels','descriptions')
    sub_keys = ('zh-hans','zh-cn','zh','en')
    #property_needs = {'p910':u'main_classification','p106':'occupation ','p279':u'father_classification','p31':u'property','p361':u'belong_to'}
    property_needs = {'p910':1,'p106':2,'p1647':3,'p279':4,'p31':5,'p361':6}
    def __init__(self):
        super(wikidata,self).__init__()
        self.db.connect()
    #将wikidata的json数据按要求存入数据库
    def import_jsondata_to_db(self,filepath,start_line = 1,end_line = 2):
        line_num = 0
        for entity in open(filepath,'r'):
            if(line_num >= start_line ):
                ret = self.json_process(entity[:-2])
                if (not ret):
                    printout(3,'json_process line:%s error' %(line_num))
                    return False
                if(line_num % 1000 == 0):
                    printout(4,'line_num:%d' %(line_num))
                    #防止过于频繁的连接导致中断
                    time.sleep(1)
            elif(line_num % 100000 == 0):
                printout(4,'pass line_num:%d' %(line_num))
            line_num += 1
            if(end_line >= start_line and line_num == end_line):
                return
    #对json数据进行处理，提取需要的成分，存入数据库
    def json_process(self,json_str):
        if():
            json_str = json_str.replace(":null,",":'',")
            entity_dict = eval(json_str)
            wikidata_id = entity_dict['id'].lower()
            name_list = []
            for main_key in self.main_keys:
                for sub_key in self.sub_keys:
                    try:
                        name =self.code_and_filter(entity_dict[main_key][sub_key]['value'])
                    except Exception, e:
                        name = ''
                    name_list.append(name)
            property_list = []
            entity_property_dict = entity_dict['claims']
            for property_name in self.property_needs:
                if property_name.upper() in entity_property_dict:
                    entity_properties = entity_property_dict[property_name.upper()]
                    if (type(entity_properties) == list):
                        for entity_property in entity_properties:
                            if ('mainsnak'in entity_property and 'datavalue' in entity_property['mainsnak']):
                                entity_property = entity_property['mainsnak']['datavalue']
                                p_name = self.property_needs[property_name]
                                if(entity_property['type'] == 'wikibase-entityid'):
                                    p_value = self.db.SQL_filter('q'+str(entity_property['value']['numeric-id']))
                                else:
                                    p_value = self.db.SQL_filter(entity_property['value'])
                                property_list.append((p_name,p_value))

            id = self.insert_entity_into_db(wikidata_id,name_list,1)
            ret = True
            if id and property_list != []:
                ret = self.insert_entityproperty_into_db(id,property_list,0)
                if(ret):
                    #printout('save entity:%s successfully' %(wikidata_id),2)
                    self.db.close()
                    return ret
                else:
                    printout(3,'save entity:%s properties error' %(wikidata_id))
                    return False
            return ret
        else:
            printout (5,'Fail to connect mysql.')
            return False
    #entity加入entities表
    def insert_entity_into_db(self,wikidta_id,name_list,sign = 0):
        sql = "INSERT INTO `%s` (`wikidata_id`, `label_zh-hans`, `label_zh-cn`, `label_zh`, `label_en`, `description_zh-hans`, `description_zh-cn`, `description_zh`, `description_en`, `sign`)\
        VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"\
        %(entities_table,wikidta_id,name_list[0],name_list[1],name_list[2],name_list[3],name_list[4],name_list[5],name_list[6],name_list[7],sign)
        id = self.db.insert(sql)
        if(id > 0):
            return id
        else:
            return False
    #entity的properties加入entity_peoperty表
    def insert_entityproperty_into_db(self,id,property_list,sign = 0):
        sql = "INSERT INTO `"+ entity_properties_table +"` \
        (`entity_id`, `property_name`, `property_value`, `sign`) \
        VALUES ("+ str(id) +", %s, %s, "+str(sign)+");"
        ret = self.db.insert_list(sql,property_list)
        if(ret > 0):
            return True
        else:
            return False
    def code_and_filter(self,string):
        return self.db.SQL_filter(string.decode('raw_unicode_escape').encode('utf-8'))

#将别名导入mysql
class wikidata_alias(wikidata):
    sub_keys = {'zh-hans':1,'zh-cn':2,'zh':3,'en':4}
    def __init__(self):
        super(wikidata_alias,self).__init__()
    def import_jsondata_to_db(self, filepath, start_line = 1, end_line = 2):
        return super(wikidata_alias, self).import_jsondata_to_db(filepath, start_line, end_line)
    #json处理
    def json_process(self, json_str):
        if(self.db.connect()):
            json_str = json_str.replace(":null,",":'',")
            entity_dict = eval(json_str)
            wikidata_id = entity_dict['id'].lower()
            id = self.get_entityid(wikidata_id)
            if 'aliases' in entity_dict:
                paras = []
                aliases = entity_dict['aliases']
                for lang,lang_id in self.sub_keys.items(): 
                    if lang in aliases:
                        for alias in aliases[lang]:
                            value = super(wikidata_alias,self).code_and_filter(alias['value'])
                            paras.append((id,lang_id,value))
                if paras != []:
                    ret = self.insert_aliases_into_db(paras,0)
                    return ret
            return True
        else:
            printout (5,'Fail to connect mysql.')
            return False
    #加入数据库
    def insert_aliases_into_db(self,paras,sign = 0):
        sql = "INSERT INTO `"+ wiki_db +"`.`"+ entity_aliases_table +"` \
        (`entity_id`, `lang`, `value`, `sign`) \
        VALUES (%s, %s, %s, "+str(sign)+");"
        ret = self.db.insert_list(sql,paras)
        if(ret > 0):
            return True
        else:
            return False
    #获取id
    def get_entityid(self,wikidata):
        return Get_entity().get_id(wikidata)[0]
if __name__ == '__main__':
   wikidata_all_json = 'wikidata-20150907-all.json'
   #wd = wikidata()
   #wd.import_jsondata_to_db(wikidata_all_json,12213055,0)
   wd = wikidata_alias()
   wd.import_jsondata_to_db(wikidata_all_json,898471,0)