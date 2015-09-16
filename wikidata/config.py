#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

wikidata_all_json = u'D:\ROW\大创2015\wikidata\wikidata-20150907-all.json'

dbinfo={\
'host' : 'localhost'\
,'user' : 'root'\
,'passwd' : 'root'\
,'db' : 'wiki'\
,'port' : 3306\
,'charset' : 'utf8'\
}

entities_table = 'entities'
entity_properties_table = 'entity_properties'