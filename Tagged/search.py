#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import sys,os
sys.path.append(sys.path[0]+'/..')

from Global.db_op import Db_op as DB
from Global.config import *
from Global.global_function import *
import jieba

class Search(object):
    search_words = set()
    max_search_length = 30
    real_sentence = ''
    def __init__(self,max_search_length = 30):
        super(Search, self).__init__()
        self.max_search_length = max_search_length
        self.db = DB(dbinfo = dbinfo)
        self.db.connect()
    def run(self,search_sentence):
        print len(search_sentence),search_sentence
        self.search_sentence_op(search_sentence)
        return words
    
    def search_sentence_op(self,search_sentence):
        self.sentence_segment(search_sentence)
        self.search_words.add(word)
        #self.search_words.add(u'三千')
        #self.search_words.add(u'多核处理器')
        word_ids = self.get_words()
        print word_ids
        l1_tags = self.get_tags(word_ids)
        l2_tags = self.get_deep_tags(l1_tags)
        return (word_ids,l1_tags,l2_tags)
    #分词
    def sentence_segment(self,search_sentence):
        search_sentence = modify_charater(search_sentence)
        search_sentence = search_sentence.split()
        search_length = 0
        self.real_sentence = ''
        for fragment in search_sentence:
            search_length += len(fragment)
            if search_length > self.max_search_length:
                fragment = fragment[:self.max_search_length+len(fragment)-search_length]
                self.real_sentence += fragment+' '
            self.search_words |= set(jieba.lcut_for_search(fragment))
            if search_length > self.max_search_length:
                return 2
        return 1
    def get_words(self):
        word_ids = set()
        sql = "SELECT `id` FROM `wiki`.`words` WHERE `word_name`=%s"
        for word in self.search_words:
            ret = self.db.select(sql,word)
            if ret:
                id = self.db.fetchOneRow()
                word_ids.add(id[0])
        printout(0,"uesd words number:%d" %(len(word_ids)))
        return word_ids
    def get_tags(self,word_ids):
        tags = {}
        sql = "SELECT we.`id`,we.`wikidata_id`,IF(`label_zh-hans`= '',IF(`label_zh-cn` = '',IF(`label_zh` = '',IF(`label_en` = '',IF (`description_zh-hans` = '',IF (`description_zh-cn` = '',IF (`description_zh` = '',`description_en`,`description_zh`),`description_zh-cn`),`description_zh-hans`),`label_en`),`label_zh`),`label_zh-cn`),`label_zh-hans`) AS `name` \
        FROM `wiki`.`entities` AS we,`wiki`.`word_entity` AS wwe \
        WHERE wwe.`entity_id` = we.`id` AND wwe.`word_id` = %s"
        for word_id in word_ids:
            ret = self.db.select(sql,word_id)
            if ret:
                result = self.db.fetchAllRows()
                for tag_id,wikidata_id,name in result:
                    if tag_id not in tags:
                        tags[tag_id] = [1,wikidata_id,name]
                    else:
                        tags[tag_id][0] += 1
        printout(0,"uesd l1 tags number:%d" %(len(tags)))
        return tags
    def get_deep_tags(self,l1_tags):
        l2_tags = {}
        sql = "SELECT we.`id`,`wikidata_id`,IF(`label_zh-hans`= '',IF(`label_zh-cn` = '',IF(`label_zh` = '',IF(`label_en` = '',IF (`description_zh-hans` = '',IF (`description_zh-cn` = '',IF (`description_zh` = '',`description_en`,`description_zh`),`description_zh-cn`),`description_zh-hans`),`label_en`),`label_zh`),`label_zh-cn`),`label_zh-hans`) \
AS `name`,`property_name` AS property,count(we.id) AS `count` \
FROM wiki.entities AS we,wiki.entity_properties AS wep \
WHERE we.wikidata_id = wep.property_value AND wep.entity_id = %s GROUP BY id \
ORDER BY `count` DESC;"
        for tag_id in l1_tags:
            ret = self.db.select(sql,tag_id)
            if ret:
                result = self.db.fetchAllRows()
                for tag_id,wikidata_id,name,property,count in result:
                    if tag_id not in l2_tags:
                        l2_tags[tag_id] = [count,wikidata_id,name]
                    else:
                        l2_tags[tag_id][0] += count
        return l2_tags
    def clear(self):
        self.search_words = set()
if __name__ == '__main__':
    search_sentence = u"陆军"
    sh = Search()
    sh.run2(search_sentence)
