#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 
import sys,os

import urllib2
#Wikidata_api 各个具体api封装的基类
class Wikidata_api(object):
    url = 'https://www.wikidata.org/w/api.php'
    parameters = {}
    def __init__(self,parameters = {}):
        super(Wikidata_api,self).__init__()
        self.parameters = parameters
    #通过GET连接wikidata,获取数据
    def connect(self,url=''):
        if url == '':
            url = self.url
        #print url
        request = urllib2.Request(url)
        response = urllib2.urlopen(url)
        html = response.read()
        return html

    #按照wikidata api的要求生成url    
    def generate_url(self):
        url = self.url
        if (len(self.parameters)>0):
            url+='?'
        for i in self.parameters:
            url += i+'='+self.parameters[i]+'&'
        return url

    #操作参数的方法
    #以dict为单位设置
    def set_parameters(self,parameters):
        self.parameters = parameters
    #清空参数
    def clear_parameters(self):
        self.parameters.clear()
    #修改或新增参数
    def update_parameter(self,p_name,p_value):
        self.parameters[p_name] = p_value
    #删除参数
    def delete_parameter(self,p_name):
        self.parameters.pop(p_name)
        
if __name__ == '__main__':
    test = Wikidata_api()
    test.set_parameters({'action':'query'})
    test.update_parameter('list','search')
    test.delete_parameter('list')
    url = test.generate_url()
    html = test.connect(url)
    print html