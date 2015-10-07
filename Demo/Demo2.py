#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
import os,sys
import web
import time
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append(sys.path[0]+'/..')
from Tagged.search import Search

render = web.template.render('templates/')
urls = (
    '/tags','tags',
    '/search','search',
    '/*.*','main',
    )
class main:
    def GET(self):
        self.para = web.input(ss=None,action=None)
        if (self.para.ss == None or self.para.ss == ''):
            return render.index()
        else:
            self.get_tags()
            return render.search(self.para)
    def get_tags(self):
        (words,l1_tags,l2_tags,webs) = Search().search_sentence_op(self.para.ss)
        self.para['words']=words
        self.para['l1_tags']=l1_tags
        self.para['l2_tags']=l2_tags
        self.para['webs']=webs

class tags:
    def GET(self):
       return
class search:
    def GET(self):                                                                    
        self.para = web.input(ss=None,action=None)
        if (self.para.ss == None or self.para.ss == ''):
            return render.index()
        else:
            self.get_tags()
            return render.search(self.para)
    def get_tags(self):
        (words,l1_tags,l2_tags) = Search().search_sentence_op(self.para.ss)
        self.para['words']=words
        self.para['l1_tags']=l1_tags
        self.para['l2_tags']=l2_tags

if __name__ == "__main__": 
    app = web.application(urls, globals())
    app.run()