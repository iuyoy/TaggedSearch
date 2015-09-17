#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
class process_data(object):
    def __init__(self):
        super(process_data, self).__init__()

class process_wikidata_entity(process_data):
    #ww.id AS words_table_id,ww.wikidata_id,is_ok,wep.id AS wep_table_id,property_name,`value`
    def to_meanings(self,meanings):
        for meaning in meanings:
            self.to_meaning(meaning)
    def get_wikidata_name(self,wikidata):
        return