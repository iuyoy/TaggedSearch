#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import sys,os
sys.path.append('..')
from Scripts.db_op import Db_op as DB
try:
    from Demo.ini import *
except:
    from ini import *

#get_data基类
class get_data(object):
    db = DB(dbinfo = dbinfo)
    def __init__(self):
        super(get_data,self).__init__()
        self.db.connect()
    def __delete__(self):
        self.db.close()

class get_word(get_data):
    def get_wordid_by_wordname(self,word_name):
        word_name = self.db.SQL_filter(word_name)
        sql = "SELECT id FROM %s WHERE word_name = '%s' " %(words_table,word_name)
        result = self.db.select(sql)
        if(result):
            return self.db.fetchAllRowsOneList()
        else:
            return []
   
class get_wikidata_entity(get_data):
    def get_meaningnames_by_wordname(self,word_name):
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
        
        
    def get_tagnames_by_wordname(self,word_name):
        word_name = self.db.SQL_filter(word_name)
        sql = """SELECT
	entity_id,
	(
		IF (
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
			) != '',
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
			),
			MAX(
				CASE wep.property_name
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
			)
		)
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

    def get_meanings_by_wordname(self,word_name):
        word_name = self.db.SQL_filter(word_name)
        sql = "SELECT ww.id AS words_table_id,ww.wikidata_id,is_ok,wep.id AS wep_table_id,property_name,`value` FROM %s AS wep,%s AS ww,%s AS w WHERE w.id = ww.word_id AND ww.wikidata_id = wep.entity_id AND word_name = '%s'" %(wikidata_entity_properties_table,wikidata_word_table,words_table,word_name)
       
        result = self.db.select(sql)
        if(result):
            rs = self.db.fetchAllRows()
            return rs
        else:
            return []