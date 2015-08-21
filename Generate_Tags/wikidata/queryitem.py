#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
import sys,os
import lxml

reload(sys)
sys.setdefaultencoding('utf-8')

class Queryitem(object):
    title = ''
    snippet = ''
    size = ''
    wordcount = ''
    timestamp = ''
    xml = ''
    def __init__(self,xml=''):
        super(Queryitem,self).__init__()
        self.xml = xml
        self.set_all_var()
    def set_all_var(self):
        self.set_title()
        self.set_snippet()
        self.set_size()
        self.set_wordcount()
        self.set_timestamp()
    def set_title(self):
        xpath = self.xml.xpath('//p/@title')
        if xpath != []:
            self.title = xpath[0]
        else:
            self.title = ''
    def set_snippet(self):
        xpath = self.xml.xpath('//p/@snippet')
        if xpath != []:
            self.snippet = xpath[0]
        else:
            self.snippet = ''
    def set_size(self):
        xpath = self.xml.xpath('//p/@size')
        if xpath != []:
            self.size = xpath[0]
        else:
            self.size = ''
    def set_wordcount(self):
        xpath = self.xml.xpath('//p/@wordcount')
        if xpath != []:
            self.wordcount = xpath[0]
        else:
            self.wordcount = ''
    def set_timestamp(self):
        xpath = self.xml.xpath('//p/@timestamp')
        if xpath != []:
            self.timestamp = xpath[0]
        else:
            self.timestamp = ''

class Queryitemlist(object):
    itemlist = []
    xml = ''
    def __init__(self,xml=''):
        super(Queryitemlist,self).__init__()
        self.setxml(xml)
    def setlist(self):
        for i in self.xml.xpath(u'//query/search/p'):
            self.itemlist.append(i.attrib)
    def setxml(self,xml):
        self.xml = xml