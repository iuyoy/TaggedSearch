#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import sys,os
sys.path.append('..')
from Scripts.db_op import Db_op as DB
from Generate_Tags.ini import *
#get_data基类
class Get_data(object):
    db = DB(dbinfo = dbinfo)
    def __init__(self):
        super(Get_data, self).__init__()
        self.db.connect()
    def __delete__(self):
        try:
            self.db.close()
        except:
            pass
class Get_wikidata(Get_data):
    def __init__(self):
        super(Get_wikidata, self).__init__()
    def get_name(self,wikidata_id):
        wikidata_id = self.db.SQL_filter(wikidata_id)
        sql = """
        SELECT
	MAX(
		CASE wep.property_name
		WHEN 'labels_zh-hans' THEN
			wep.`value`
		WHEN 'labels_zh-cn' THEN
			wep.`value`
		WHEN 'labels_zh' THEN
			wep.`value`
		WHEN 'labels_en' THEN
			wep.`value`
		ELSE
			''
		END
	)
FROM
	%s AS wep
WHERE
	wep.entity_id = '%s'
GROUP BY
	wep.entity_id
        """ %(wikidata_entity_properties_table,wikidata_id)
        result = self.db.select(sql)
        if(result):
            return self.db.fetchOneRow()
        else:
            return []
class Get_article(Get_data):
    def __init__(self):
        super(Get_article, self).__init__()
    def get_one_cnbeta_article(self , id = 0):
        id = int(id)
        if (id == 0):
            sql = "SELECT id,title,content FROM %s WHERE `level` = 0 AND id > 53000 LIMIT 1  " %(cnbeta_table)
        else:
            sql = "SELECT id,title,content FROM %s WHERE `level` = 0 AND id = %d" %(cnbeta_table,id)
        result = self.db.select(sql)
        if(result):
            return self.db.fetchOneRow()
        else:
            return []

class Get_tags(Get_data):
    def __init__(self):
        super(Get_tags, self).__init__()
    def get_all_level1_tags(self,word_name):
        word_name = self.db.SQL_filter(word_name)
        sql = """SELECT DISTINCT
	entity_id
FROM
	%s AS we,
	%s AS wep,
	%s AS ww,
	%s AS w
WHERE
	w.id = ww.word_id
AND ww.wikidata_id = wep.entity_id
AND ww.wikidata_id = we.wikidata_id
AND word_name = '%s'
AND we.sign = 1
        """ %(wikidata_entities_table,wikidata_entity_properties_table,wikidata_word_table,words_table,word_name)
        result = self.db.select(sql)
        if(result):
            rs = self.db.fetchAllRows()
            return rs
        else:
            return []
    def get_all_level2_tags(self,word_name):
        word_name = self.db.SQL_filter(word_name)
        sql = """
	SELECT
	distinct wep.`value`
FROM
	%s AS wep,
	%s AS we,
	%s AS ww,
	%s AS w
WHERE
	w.id = ww.word_id
AND wep.`value` = we.wikidata_id
AND ww.wikidata_id = wep.entity_id
AND word_name = '%s'
AND (
	wep.property_name = 'father_classification'
	OR wep.property_name = 'main_classification'
	OR wep.property_name = 'property'
	OR wep.property_name = 'belong_to'
)
AND we.sign = 1
        """ %(wikidata_entity_properties_table,wikidata_entities_table,wikidata_word_table,words_table,word_name)
        result = self.db.select(sql)
        if(result):
            rs = self.db.fetchAllRows()
            return rs
        else:
            return []