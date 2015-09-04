#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        word = self.get_argument('word')
        self.render("templates\demo.html", title="My title", word=word)
        

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(1234)
    tornado.ioloop.IOLoop.instance().start()