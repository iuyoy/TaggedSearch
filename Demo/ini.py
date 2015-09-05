#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import Queue

global dbinfo
global wikidata_entities_table,wikidata_entity_properties_table,wikidata_word_table
global words_table,word_properties_table
dbinfo={\
'host' : '104.251.227.241'\
,'user' : 'search'\
,'passwd' : 'search&Tagged'\
,'db' : 'search'\
,'port' : 3306\
,'charset' : 'utf8'\
}
#wikidata_entities_table = 'wikidata_entities'
#wikidata_entity_properties_table = 'wikidata_entity_properties'
wikidata_entities_table = 'wikidata_entities_new'
wikidata_entity_properties_table = 'wikidata_entity_properties_new'
wikidata_word_table = 'wikidata_word'
words_table = 'words'
word_properties_table = 'word_properties'

global parse_queue
parse_queue = Queue.Queue()
