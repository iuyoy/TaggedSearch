#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import web

render = web.template.render('templates/')
urls = (
    '/','index'
    )

class index:
    def GET(self):
        search = web.input(word=None,action=None)
        
        return render.main(search)
    def show_tags(self):
        return 0
if __name__ == "__main__": 
    app = web.application(urls, globals())
    app.run()