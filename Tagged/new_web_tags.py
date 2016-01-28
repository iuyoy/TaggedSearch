#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import os,sys,time
sys.path.append(sys.path[0]+'/..')

from Global.config import *
from Global.db_op import Db_op as DB
from Global.global_function import *
from jieba import posseg as pseg
import jieba

from Wikidata.api_wbsearchentities import Wbsearchentities as Wbsearch
from Word_Segment.ngd import *

common_word = 0
stop_word = 2

class Tag_website_step_by_step(object):
    db = DB(dbinfo = dbinfo)

    word_dict = {}
    relation_list = []
    def __init__(self):
        self.db.connect()
    ####
    #websites operations(word segment)
    ####
    def traversal_websites(self,start = 1,end = 1000):
        for id in range(int(start),int(end)):
            sql = "SELECT `id`,`url`,`docno`,`title`,`content`,`sign` FROM `wiki`.`websites` WHERE id = "+str(id)
            ret = self.db.select(sql)
            if ret:
                web_id,url,docno,title,content,sign = self.db.fetchOneRow()
                #print web_id,url,docno,title,content,sign
                self.clear_word_dict()
                self.segment_words(web_id,title,content)
            else:
                print "error @ web%d" %(id)

    ####
    #words operations()
    ####
    #traversal websites to build web tags relations
    def traversal_websites_to_build_web_tags_relations(self,start = 1,limit = 1):
        for id in xrange(start,start+limit):
            sql = ""
    #traversal words_tags calculate nbd
    def traversal_words_tags_calculate_nbd(self,start = 1,limit = 1):
        max_relation_id = self.get_max_word_tags_id(sign = 1)
        start = start if start!=1 else max_relation_id
        word_fx = (0,0)
        for id in xrange(start,start+limit):
            sql = "SELECT\
	                    `wwt`.`id`,\
	                    `ww`.`word_name`,\
	                    IF(`label_zh-hans`= '',IF(`label_zh-cn` = '',IF(`label_zh` = '',IF(`label_en` = '',IF (`description_zh-hans` = '',IF (`description_zh-cn` = '',IF (`description_zh` = '',`description_en`,`description_zh`),`description_zh-cn`),`description_zh-hans`),`label_en`),`label_zh`),`label_zh-cn`),`label_zh-hans`) AS `tag_name`,\
	                    `wwt`.`sign`\
                    FROM\
	                    `wiki`.`word_tags` AS wwt,\
	                    `wiki`.`words` AS ww,\
	                    `wiki`.`entities` AS we\
                    WHERE\
	                    wwt.sign = 0\
                    AND wwt.word_id = ww.id\
                    AND wwt.entity_id = we.id\
                    AND wwt.id = " + str(id)
            ret = self.db.select(sql)
            if ret:
                relation_id,word_name,tag_name,sign = self.db.fetchOneRow()
                print relation_id,word_name,tag_name,sign
                if word_fx[0] != id:
                    word_fx = (id,bingsearch(word_name.encode('utf8')))
                if tag_name == '':
                    rank = -1
                else:
                    rank = NBD2(word_name.encode('utf8'),tag_name.encode('utf8'),word_fx[1])
                print rank
                sql = "UPDATE `wiki`.`word_tags` SET `sign`=%s, `rank`=%s WHERE (`id`=%s)"
                ret = self.db.update(sql,(1,rank,id))
                if not ret:
                    print("Error:update rank") 
            else:
                print "not that id:%s" %(id)           
        else:
            print "Finished All"
    #traversal words_entities to build words-tags ralations 
    def traversal_words_entities_to_build_words_tags_ralations(self,start = 1,limit = 1):
        max_word_id = self.get_max_word_id(sign = 11)
        start = start if start!=1 else max_word_id
        sql = "SELECT `id`,`word_name`,`pos`,`sign` FROM `wiki`.`words` WHERE sign = 10 AND id >= " + str(max_word_id) + " LIMIT " + str(int(limit))
        ret = self.db.select(sql)
        if ret:
            word_list = self.db.fetchAllRows()
            print "length of word list:",len(word_list)
            for word_id,word_name,pos,sign in word_list:
                print "Now searching word:%s %s %s %s " %(word_id,word_name,pos,sign)
                relations = self.get_word_tags_relation(word_id)
                if relations:
                    for entity_id,wikidata_id,name,prop,count in relations:
                        #print word_name,name
                        
                        rank = 0
                        sql = "INSERT INTO `wiki`.`word_tags` (`word_id`, `entity_id`, `sign`, `rank`) VALUES (%s, %s, %s, %s);"
                        id = self.db.insert(sql,(word_id,entity_id,0,rank))
                    else:
                        self.change_word_sign(word_id,11)
                else:
                    self.change_word_sign(word_id,4)
            else:
                print "Finished All"
    #get word-tags relation
    def get_word_tags_relation(self,word_id = 0):
        word_id = int(word_id)
        sql = "SELECT we.`id`,`wikidata_id`,IF(`label_zh-hans`= '',IF(`label_zh-cn` = '',IF(`label_zh` = '',IF(`label_en` = '',IF (`description_zh-hans` = '',IF (`description_zh-cn` = '',IF (`description_zh` = '',`description_en`,`description_zh`),`description_zh-cn`),`description_zh-hans`),`label_en`),`label_zh`),`label_zh-cn`),`label_zh-hans`) \
        AS `name`,`property_name`,count(we.`id`) AS `count`\
        FROM `"+wiki_db+"`.`"+entities_table+"` AS we , `"+wiki_db+"`.`"+word_entity_table+"` AS wwe , `"+wiki_db+"`.`"+entity_properties_table+"` AS wep\
        WHERE wwe.entity_id = wep.entity_id AND we.wikidata_id = wep.property_value AND wwe.word_id = %s AND we.sign = 1\
        GROUP BY id ORDER BY `count` DESC"
        para = [word_id]
        entities = self.db.select(sql,para)
        if entities:
            return self.db.fetchAllRows()
        return False  
    #traversal words to build_word_entity_relations
    def traversal_words_to_build_word_entity_relations(self,start = 1,end = 1000):
        max_word_id = self.get_max_word_id(sign = 10)
        start = start if start!=1 else max_word_id
        for id in range(int(start),int(end)):
            sql = "SELECT `id`,`word_name`,`pos`,`sign` FROM `wiki`.`words` WHERE id = "+str(id)
            ret = self.db.select(sql)
            if ret:
                word_id,word_name,pos,sign = self.db.fetchOneRow()
                print word_id,word_name,pos,sign
                if sign == 0 :
                    print "Searching ..."
                    ret = self.build_word_entity_relations(word_id,word_name.encode('utf8'))
                    if ret:
                        self.change_word_sign(word_id,sign = 10)
                else:
                    print "Pass"
            else:
                print "error @ word%d" %(id)
    #build words and entities relations
    def build_word_entity_relations(self,word_id,word_name):
        #wbsearch查询得到relations
        relation_list = Wbsearch().run(word_name)
        ret = True
        if len(relation_list):
            for relation in relation_list:
                ret = self.add_word_entity_relation(word_id,relation['id'])
            if(ret):
                self.change_word_sign(word_id,10)
            else:
                print("error @ build_word_entity_relations")
                sys.exit(-1)
        else:
            self.change_word_sign(word_id,2)

    #add word and tag relation
    def add_word_entity_relation(self,word_id,wikidata_id,sign = 0):
        word_id = int(word_id)
        entity = self.get_entity_id(wikidata_id)
        sign = int(sign)
        if (entity):
            (entity_id,sign) = entity
            sign = int(sign)
            sql = "INSERT INTO `"+wiki_db+"`.`"+word_entity_table+"`(`word_id`,`entity_id`,`sign`) VALUES(%s,%s,%s)" 
            para = [word_id,entity_id,sign]
            ret = self.db.insert(sql,para)
        else:
            return -1
        return ret
    #get entity_id by wikidata_id
    def get_entity_id(self,wikidata_id):
        wikidata_id = self.db.SQL_filter(wikidata_id)
        sql = "SELECT id,sign FROM `"+wiki_db+"`.`"+entities_table+"` WHERE wikidata_id = %s"
        para = wikidata_id
        result = self.db.select(sql,para)
        return self.db.fetchOneRow()
    #get max word_id with sign =10
    def get_max_word_id(self,sign = 10):
        sql = "SELECT MAX(`id`) FROM `wiki`.`words` WHERE sign = "+str(int(sign))
        ret = self.db.select(sql)
        if ret:
            ret = self.db.fetchOneRow()[0]
            if ret:
                return ret+1
        return 1
    #get max word-tags_id with sign =10
    def get_max_word_tags_id(self,sign = 0):
        sql = "SELECT MAX(`id`) FROM `wiki`.`word_tags` WHERE sign = "+str(int(sign))
        ret = self.db.select(sql)
        if ret:
            ret = self.db.fetchOneRow()[0]
            if ret:
                return ret+1
        return 1
    #change word sign
    def change_word_sign(self,word_id,sign):
        sql = "UPDATE `wiki`.`words` SET sign = %s WHERE id = %s "
        ret = self.db.update(sql,(sign,word_id))
    #change single word sign to 1
    def change_single_word_sign(self,start = 1,end = 1000):
        for id in range(int(start),int(end)):
            sql = "SELECT `id`,`word_name`,`pos`,`sign` FROM `wiki`.`words` WHERE id = "+str(id)
            ret = self.db.select(sql)
            if ret:
                word_id,word_name,pos,sign = self.db.fetchOneRow()
                
                if len(word_name) == 1 and sign == 0 :
                    print word_id,word_name,pos,sign
                    self.change_word_sign(1)
            else:
                print "error @ word%d" %(id)
    #segment words
    def segment_words(self,web_id,title,content):
        title_words = jieba.lcut_for_search(title)
        content_words = jieba.lcut_for_search(content)
        for word in title_words:
            if word in self.word_dict:
                self.word_dict[word] += 1
            else:
                self.word_dict[word] = 1
        for word in content_words:
            if word in self.word_dict:
                self.word_dict[word] += 1
            else:
                self.word_dict[word] = 1
        for word,count in self.word_dict.items(): 
            ret = self.build_website_word_relations(web_id,word,count)
            if not ret:
                print "error @%s" %(word)
        print "Finish web %d" %(web_id)
    #build website word relations
    def build_website_word_relations(self,web_id,word,count):
        ret = self.check_word(word)
        word_id =0
        if ret:
            id,pos,sign = ret
            if sign == stop_word:
                word_id = id
            elif sign == common_word:
                word_id = id
        else:
            sql = 'INSERT INTO `wiki`.`words`(`word_name`,`pos`,`sign`) VALUES(%s,%s,%s)'
            id = self.db.insert(sql,(word,'comm',0))
            if id:
                word_id = id
        if word_id:
            sql = "INSERT INTO `wiki`.`websites_words` (`website_id`, `word_id`, `count`, `sign`, `rank`) VALUES (%s, %s, %s, %s, %s);"
            id = self.db.insert(sql,(web_id,word_id,count,0,0))
            if id:
                return True
            return False
        return True
    #is word existing
    def check_word(self,word_id):
        sql = "SELECT `id`,`pos`,`sign` FROM `wiki`.`words` WHERE `word_name` = %s"
        ret = self.db.select(sql,word_id)
        if ret:
            return self.db.fetchOneRow()
        else:
            return False

    ####
    #clear memory
    ####
    def clear_word_dict(self):
        self.word_dict.clear()
    def clear_relation_list(self):
        self.relation_list = []
if __name__ == '__main__':
    #we = Website_entities()
    #we.get_website()
    twsbs = Tag_website_step_by_step()
    #Divide websites into words,build websites and words relations
    #twsbs.traversal_websites(1,1001)

    #get words' tags,build words and tags relations
    #twsbs.traversal_words(1 ,41823)

    twsbs.traversal_words_tags_calculate_nbd(1,2000)

