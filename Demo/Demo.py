#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
import os,sys
import web
from Tsearch import Search_tags_by_word as get_tags
from Tsearch import Search_insite
reload(sys)
sys.setdefaultencoding("utf-8")

render = web.template.render('templates/')
urls = (
    '/','index'
    )

class index:
    function_option={'tags':'','insite':'','dbinfo':''}
    def GET(self):
        para = web.input(word=None,action=None)
        #决定显示什么界面
        self.choose_function(para.action)
        para['function_option'] = self.function_option
        if (para.word != None and para.word!=''):
            word_name = para.word.encode('utf-8')
            if(para.action == 'tags'):
                para['tags'] = self.show_tags(word_name)
            elif(para.action == 'insite'):
                try:
                    web_id = int(word_name)
                except:
                    web_id = 51200    
                para['insite'] = self.search_insite(web_id)
        return render.main(para)

    def show_tags(self,word_name):
        result = get_tags().run(word_name)
        return result
    def search_insite(self,word_name):
        result = Search_insite().run(word_name)
        return result

    def choose_function(self,option = 'insite'):
        if option in self.function_option:
            self.clear_function_option()
            self.function_option[option] = 'active in'
        else:
            self.choose_function()

    def clear_function_option(self):
        self.function_option={'tags':'','insite':'','dbinfo':''}
if __name__ == "__main__": 
    app = web.application(urls, globals())
    app.run()