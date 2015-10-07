#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

#重要的全局变量

#输出等级
print_level = 1

#数据库信息

#dbinfo={\
#'host' : 'localhost'\
#,'user' : 'root'\
#,'passwd' : 'root'\
#,'db' : 'wiki'\
#,'port' : 3306\
#,'charset' : 'utf8'\
#}

dbinfo={\
'host' : '192.168.99.127'\
,'user' : 'root'\
,'passwd' : 'root'\
,'db' : 'search'\
,'port' : 3306\
,'charset' : 'utf8'\
}


#dbinfo={\
#'host' : 'localhost'\
#,'user' : 'search'\
#,'passwd' : 'search&Tagged'\
#,'db' : 'search'\
#,'port' : 3306\
#,'charset' : 'utf8'\
#}
#db
search_db = 'search'
#wiki_db = 'wiki'
wiki_db = 'search'
#table
entities_table = 'entities'
entity_properties_table = 'entity_properties'
entity_aliases_table = 'entity_aliases'

wikidata_entities_table = 'wikidata_entities_new'
wikidata_entity_properties_table = 'wikidata_entity_properties_new'
wikidata_word_table = 'wikidata_word'
words_table = 'words'
word_properties_table = 'word_properties'
word_entity_table = 'word_entity'

cnbeta_table = 'sp_cnbeta'
sogou_all_table = 'websites_news_all'
sogou_sogou_table = 'websites_sogou'
websites_words_table = 'websites_words'
websites_tags_table = 'websites_tags'

#结巴字典文件路径
#jieba_words_dict_path = r'C:\0pros\Python27\Lib\site-packages\jieba\dict.txt'
stopwords_path = './Word_Segment/stopwords.txt'