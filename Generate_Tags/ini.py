#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

global dbinfo
global wikidata_entities_table,wikidata_entity_properties_table
global words_table,word_properties_table
dbinfo={\
'host' : '23.244.180.241'\
,'user' : 'search'\
,'passwd' : 'search&Tagged'\
,'db' : 'search'\
,'port' : 3306\
,'charset' : 'utf8'\
}
wikidata_entities_table = 'wikidata_entities'
wikidata_entity_properties_table = 'wikidata_entity_properties'
words_table = 'words'
word_properties_table = 'word_properties'

global parse_stack
parse_stack = []