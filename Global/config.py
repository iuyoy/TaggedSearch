#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

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
'host' : 'loacalhost'\
,'user' : 'search'\
,'passwd' : 'search&Tagged'\
,'db' : 'search'\
,'port' : 3306\
,'charset' : 'utf8'\
}
#db
search_db = 'search'
#wiki_db = 'wiki'
wiki_db = 'search'
#table
entities_table = 'entities'
entity_properties_table = 'entity_properties'

wikidata_entities_table = 'wikidata_entities_new'
wikidata_entity_properties_table = 'wikidata_entity_properties_new'
wikidata_word_table = 'wikidata_word'
words_table = 'words'
word_properties_table = 'word_properties'
word_entity_table = 'word_entity'
cnbeta_table = 'sp_cnbeta'

#输出等级
print_level = 0