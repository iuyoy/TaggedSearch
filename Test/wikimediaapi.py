#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
import wikipedia

wikipedia.set_lang('en')
result = wikipedia.search("��˾")
for i in result:
    print i.encode('utf-8')