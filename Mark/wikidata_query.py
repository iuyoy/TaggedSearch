#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
import sys,os

import urllib2
import lxml.html

import queryitem

reload(sys)
sys.setdefaultencoding('utf-8')
#
class wikidata_query(object):
    url = 'https://www.wikidata.org/w/api.php'
    uselang = 'zh'
    action = 'query'
    list = 'search'
    is_rawcontinue = 'rawcontinue='
    srsearch = 'apple'
    srnamespace = '0'
    #sroffset = '0'
    sroffset = '0'#下一个开始位置
    totalhits = '0'#总数
    #srlimit = '50'
    format = 'xml'
    srprop = 'size|wordcount|timestamp|snippet'
    #srprop = 'size|wordcount|timestamp|snippet|titlesnippet|redirecttitle|redirectsnippet|sectiontitle|sectionsnippet|isfilematch|categorysnippet'
    #search = []
    #other_parameter = ''
    result = queryitem.queryitemlist()
    def __init__(self):
        super(wikidata_query,self).__init__()

    def run(self,srsearch='apple',srlimit='50',other_parameter=''):
        url = self.generate_url(srsearch,self.sroffset,other_parameter,srlimit)
        html = self.connect(url)
        self.dealwith(html)
        while (int(self.sroffset) < int(self.totalhits)):
            url = self.generate_url(srsearch,self.sroffset,other_parameter,srlimit)
            html = self.connect(url)
            self.dealwith(html)
    def generate_url(self,srsearch='apple',sroffset='0',other_parameter='',srlimit='50'):
        url = self.url+'?uselang='+self.uselang+'&format='+self.format\
            +'&action='+self.action\
            +'&list='+self.list\
            +'&srsearch='+srsearch\
            +'&srnamespace='+self.srnamespace\
            +'&srlimit='+srlimit\
            +'&sroffset='+sroffset\
            +'&srprop='+self.srprop\
            +'&'+self.is_rawcontinue\
            +other_parameter
        return url
    def connect(self,url=''):
        #self.url = 'https://www.wikidata.org/w/api.php?action=query&list=search&srsearch=苹果&format=xml&srnamespace=0&srprop=size|wordcount|timestamp|score|snippet|titlesnippet|redirecttitle|redirectsnippet|sectiontitle|sectionsnippet|hasrelated|isfilematch|categorysnippet'
        if url == '':
            url = self.url
        print url
        request = urllib2.Request(url)
        response = urllib2.urlopen(url)
        html = response.read()
        return html
    def dealwith(self,html=''):
        doc = lxml.html.fromstring(html)
        doc = lxml.etree.HTML(html.lower().decode('utf-8'))
        totalhits = doc.xpath('//query/searchinfo/@totalhits')
        sroffset = doc.xpath('//query-continue/search/@sroffset')
        if totalhits != []:
            self.totalhits = totalhits[0]
        else:
            self.totalhits = 0
        if sroffset != []:
            self.sroffset = sroffset[0]
        else:
            self.sroffset = self.totalhits
        if sroffset > 0:
            self.result.setxml(doc)
            self.result.setlist()
        #print totalhits,sroffset
if __name__ == "__main__":
    rm = wikidata_query()
    rm.run('苹果')
    print rm.totalhits
    print len(rm.result.itemlist)
    for i in rm.result.itemlist:
        print i['title'],i['snippet'].encode('utf-8')
