#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import sys,os
sys.path.append('..')
from Scripts.db_op import Db_op as DB
try:
    from Demo.ini import *
except:
    from Generate_Tags.ini import *
from Generate_Tags.ini import *
#get_data基类
class Get_data(object):
    db = DB(dbinfo = dbinfo)
    def __init__(self):
        super(Get_data, self).__init__()
        self.db.connect()
    def __delete__(self):
        self.db.close()

class Get_article(Get_data):
    def __init__(self):
        super(Get_article, self).__init__()
    def get_one_cnbeta_article(self , id = 0):
        id = int(id)
        if (id == 0):
            sql = "SELECT id,title,content FROM %s WHERE `level` = 0 LIMIT 1  " %(cnbeta_table)
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
        sql = """SELECT
	entity_id,
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
		WHEN 'descriptions_zh-hans' THEN
			wep.`value`
		WHEN 'descriptions_zh-cn' THEN
			wep.`value`
		WHEN 'descriptions_zh' THEN
			wep.`value`
		WHEN 'descriptions_en' THEN
			wep.`value`
		ELSE
			''
		END
	) AS `name`
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
GROUP BY
	entity_id
        """ %(wikidata_entities_table,wikidata_entity_properties_table,wikidata_word_table,words_table,word_name)
        result = self.db.select(sql)
        if(result):
            rs = self.db.fetchAllRows()
            return rs
        else:
            return []
    def get_all_level2_tags(self,word_name):
        word_name = self.db.SQL_filter(word_name)
        sql = """SELECT
	entity_id,
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
		WHEN 'descriptions_zh-hans' THEN
			wep.`value`
		WHEN 'descriptions_zh-cn' THEN
			wep.`value`
		WHEN 'descriptions_zh' THEN
			wep.`value`
		WHEN 'descriptions_en' THEN
			wep.`value`
		ELSE
			''
		END
	) AS `name`,
    count
FROM
	%s AS wep
RIGHT JOIN (
	SELECT
		wep2.`value`,
		count(wep2.`value`) AS `count`
	FROM
		%s AS wep2,
		%s AS ww,
		%s AS w
	WHERE
		w.id = ww.word_id
	AND ww.wikidata_id = wep2.entity_id
	AND word_name = '%s'
	AND (
		wep2.property_name = 'father_classification'
		OR wep2.property_name = 'main_classification'
		OR wep2.property_name = 'property'
		OR wep2.property_name = 'belong_to'
	)
	GROUP BY
		wep2.`value`
) AS meanings ON wep.entity_id = meanings.`value`,
%s AS we
WHERE
	we.wikidata_id = entity_id
AND we.sign = 1
GROUP BY
	entity_id
        """ %(wikidata_entity_properties_table,wikidata_entity_properties_table,wikidata_word_table,words_table,word_name,wikidata_entities_table)
        result = self.db.select(sql)
        if(result):
            rs = self.db.fetchAllRows()
            return rs
        else:
            return []