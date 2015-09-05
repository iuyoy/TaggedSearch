#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
import os,sys
import web
from Tsearch import *
reload(sys)
sys.setdefaultencoding( "utf-8" )

render = web.template.render('templates/')
urls = (
    '/','index'
    )

class index:
    def GET(self):
        search = web.input(word=None,action=None)
        if(search.action == 'tags' and search.word!=None):
            word_name = search.word.encode('utf-8')
            search['tags'] = self.show_tags(word_name)
        return render.main(search)

    def show_tags(self,word_name):
        result = Search_for_tags_by_word().run(word_name)
        return result
if __name__ == "__main__": 
    app = web.application(urls, globals())
    app.run()