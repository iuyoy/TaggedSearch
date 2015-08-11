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
    #<p ns="0" title="Q213710" snippet="<span class="searchmatch">ƻ</span><span class="searchmatch">��</span>��Ƭ �O����Ƭ �O����Ƭ <span class="searchmatch">ƻ</span><span class="searchmatch">��</span>��Ƭ <span class="searchmatch">ƻ</span><span class="searchmatch">��</span>��Ƭ �O����Ƭ Apple Records Apple Records ??? ?????? ?? ??? Apple Records Apple Records Apple Records Apple Records Apple Records ���åץ�?�쥳�`��" size="11698" wordcount="186" timestamp="2015-03-07T14:19:40Z"/>
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
        #print self.xml
        #print self.xml.xpath(u'//query/search/p')
        for i in self.xml.xpath(u'//query/search/p'):
            #print i.attrib
            #tempitem = Queryitem(i)
            self.itemlist.append(i.attrib)
    def setxml(self,xml):
        self.xml = xml