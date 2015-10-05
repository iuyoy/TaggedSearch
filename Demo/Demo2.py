#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
import os,sys
import web
import time
reload(sys)
sys.setdefaultencoding("utf-8")

render = web.template.render('templates/')
urls = (
    '/search','search',
    '/*.*','main',
    )

class main:
    def GET(self):
        para = web.input(ss=None,action=None)
        if (para.ss == None or para.ss == ''):
            return render.index()
        else:
            return render.search(para)
       
class search:
    def GET(self):
        time.sleep(2)
        return "123"
if __name__ == "__main__": 
    app = web.application(urls, globals())
    app.run()