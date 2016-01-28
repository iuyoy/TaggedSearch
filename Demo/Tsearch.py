#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import sys,os
sys.path.append(sys.path[0]+'/..')

from Global.db_op import Db_op as DB
from Global.config import *
from Global.global_function import *
import jieba
from gensim import corpora, models, similarities

class Search(object):
    #name:[id,rank]
    search_words = {}
    #id:[count,wiki_id,name,rank]
    l1_tags = {}
    #id:[count,wiki_id,name,rank]
    l2_tags = {}
    max_search_length = 30
    real_sentence = ''

    corpus=[]
    vec=[]
    num_features = 0
    result = []
    #id:[(vec_id,count)]
    websites = {}

    def __init__(self,max_search_length = 30):
        super(Search, self).__init__()
        self.max_search_length = max_search_length
        self.db = DB(dbinfo = dbinfo)
        self.db.connect()
    
    def do_search(self,search_sentence,page = 1):
        self.reset()
        is_tool_long = self.sentence_segment(search_sentence)
        self.get_words()
        self.get_l1_tags()
        self.get_l2_tags()
        self.set_gensim()
        webs = self.get_websites(page)
        return (self.search_words,self.l1_tags,self.l2_tags,webs)

    #搜索语句处理
    def sentence_segment(self,search_sentence):
        search_sentence = modify_charater(search_sentence)
        search_sentence = search_sentence.split()
        search_length = 0
        self.real_sentence = ''
        for fragment in search_sentence:
            fragment_len = len(fragment)
            search_length += fragment_len
            if search_length > self.max_search_length:
                fragment = fragment[:self.max_search_length+len(fragment)-search_length]
                self.real_sentence += fragment+' '
            #将最长的部分加入搜索词中
            if fragment not in self.search_words:
                self.search_words[fragment] = [0,self.max_search_length]
            #分词
            for word in jieba.lcut_for_search(fragment):
                if word not in self.search_words:
                    self.search_words[word] = [0,float(len(word))*self.max_search_length/fragment_len]
            if search_length > self.max_search_length:
                return True#超长
        return False#长度正常

    #排序算法
    def set_gensim(self):
        for name,(word_id,rank) in self.search_words.items():
            self.vec.append([self.num_features,rank])
            self.search_websites_by_word(word_id)
            self.num_features += 1
        #for tag_id in self.l1_tags:
        #    self.vec.append([self.num_features,1.0])
        #    self.search_websites_by_tag(tag_id)
        #    self.num_features += 1
        for tag_id in self.l2_tags:
            self.vec.append([self.num_features,self.l2_tags[tag_id][3]])
            self.search_websites_by_tag(tag_id)
            self.num_features += 1
        self.corpus = list(self.websites.itervalues())
        self.websites = list(self.websites.iterkeys())
        if self.corpus != []:
            tfidf = models.TfidfModel(self.corpus)
            index = similarities.SparseMatrixSimilarity(tfidf[self.corpus], num_features=self.num_features)
            sims = index[tfidf[self.vec]]
            printout(1,'vec',self.vec)
            self.result = sorted(enumerate(sims), key=lambda e:e[1], reverse=True)
        else:
            self.result = []
     
    #获得页面信息       
    def get_websites(self,page = 1,npp=10):
        webs = {'page':page,'npp':0,'total':len(self.websites)}
        printout(1,len(self.websites),page)
        if (type(self.websites) == list):
            for index in xrange((page-1)*npp,page*npp):
                if index < webs['total']:
                    ret = self.get_website(self.websites[self.result[index][0]])
                    if ret:
                        webs[index-(page-1)*npp] = ret
                else:
                    index -= 1
                    break
            printout(1,'index',index)
            webs['npp'] = index-(page-1)*npp+1
        return webs

    #获得具体页面
    def get_website(self,page_id):
        sql = "SELECT `url`,`title`,`content`,`sign` FROM `"+search_db+"`.`"+sogou_sogou_table+"` WHERE id = %s"
        ret = self.db.select(sql,page_id)
        if ret:
            return self.db.fetchOneRow()
        return False

    #得到有word的所有页面
    def search_websites_by_word(self,word_id):
        sql = "SELECT `website_id`,`count`,`sign` FROM `"+wiki_db+"`.`"+websites_words_table+"` WHERE word_id = %s"
        ret = self.db.select(sql,word_id)
        if ret:
            for website,count,sign in self.db.fetchAllRows():
                if website in self.websites:
                    #id:[(vec_id,count)]
                    self.websites[website].append((self.num_features,count))
                else:
                    self.websites[website]=[(self.num_features,count)]

    #得到有tag的所有页面
    def search_websites_by_tag(self,tag_id):
        sql = "SELECT `website_id`,`count`,`sign` FROM `"+wiki_db+"`.`"+websites_tags_table+"` WHERE entity_id = %s"
        ret = self.db.select(sql,tag_id)
        if ret:
            for website,count,sign in self.db.fetchAllRows():
                if website in self.websites:
                    #id:[(vec_id,count)]
                    self.websites[website].append((self.num_features,count))
                else:
                    self.websites[website]=[(self.num_features,count)]
    
    #获取word的id
    def get_words(self):
        sql = "SELECT `id` FROM `"+wiki_db+"`.`"+words_table+"` WHERE `word_name`=%s"
        for word in self.search_words:
            ret = self.db.select(sql,word)
            if ret:
                id = self.db.fetchOneRow()
                self.search_words[word][0] = id[0]
        #printout(0,"uesd words number:%d" %(len(self.search_words)))

    #得到一级标签
    def get_l1_tags(self):
        sql = "SELECT we.`id`,we.`wikidata_id`,IF(`label_zh-hans`= '',IF(`label_zh-cn` = '',IF(`label_zh` = '',IF(`label_en` = '',IF (`description_zh-hans` = '',IF (`description_zh-cn` = '',IF (`description_zh` = '',`description_en`,`description_zh`),`description_zh-cn`),`description_zh-hans`),`label_en`),`label_zh`),`label_zh-cn`),`label_zh-hans`) AS `name` \
        FROM `"+wiki_db+"`.`"+entities_table+"` AS we,`"+wiki_db+"`.`"+word_entity_table+"` AS wwe \
        WHERE wwe.`entity_id` = we.`id` AND wwe.`word_id` = %s"
        for word_id,rank in self.search_words.itervalues():
            ret = self.db.select(sql,word_id)
            if ret:
                result = self.db.fetchAllRows()
                number_of_tags = len(result)
                for tag_id,wikidata_id,name in result:
                    if tag_id not in self.l1_tags:
                        self.l1_tags[tag_id] = [1,wikidata_id,name,float(rank)*2/number_of_tags]
                    else:
                        self.l1_tags[tag_id][0] += 1
                        self.l1_tags[tag_id][3] += float(rank)*2/number_of_tags
        #printout(0,"uesd l1 self.l1_tags number:%d" %(len(self.l1_tags)))

    #得到二级标签
    def get_l2_tags(self):
        sql = "SELECT we.`id`,`wikidata_id`,IF(`label_zh-hans`= '',IF(`label_zh-cn` = '',IF(`label_zh` = '',IF(`label_en` = '',IF (`description_zh-hans` = '',IF (`description_zh-cn` = '',IF (`description_zh` = '',`description_en`,`description_zh`),`description_zh-cn`),`description_zh-hans`),`label_en`),`label_zh`),`label_zh-cn`),`label_zh-hans`) \
AS `name`,`property_name` AS property,count(we.id) AS `count` \
FROM `"+wiki_db+"`.`"+entities_table+"` AS we,`"+wiki_db+"`.`"+entity_properties_table+"` AS wep \
WHERE we.wikidata_id = wep.property_value AND wep.entity_id = %s GROUP BY id \
ORDER BY `count` DESC;"
        for l1tag_id in self.l1_tags:
            ret = self.db.select(sql,l1tag_id)
            if ret:
                result = self.db.fetchAllRows()
                number_of_tags = len(result)
                for tag_id,wikidata_id,name,property,count in result:
                    if tag_id not in self.l2_tags:
                        #self.l2_tags[tag_id] = [count,wikidata_id,name,float(count)*self.l1_tags[l1tag_id][3]/number_of_tags]
                        self.l2_tags[tag_id] = [count,wikidata_id,name,self.l1_tags[l1tag_id][3]/number_of_tags]
                    else:
                        self.l2_tags[tag_id][0] += count
                        #self.l2_tags[tag_id][3] += float(count)*self.l1_tags[l1tag_id][3]/number_of_tags
                        self.l2_tags[tag_id][3] += self.l1_tags[l1tag_id][3]/number_of_tags

    #重置
    def reset(self):
        self.search_words.clear()
        self.l1_tags.clear()
        self.l2_tags.clear()
        self.websites.clear()
        self.vec = []
        self.corpus = []
        self.num_features = 0

if __name__ == '__main__':
    search_sentence = u"苹果"
    sh = Search()
    sh.do_search(search_sentence)
