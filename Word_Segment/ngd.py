#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy
#from:https://github.com/SigmoidFreud/NormalizedGoogleDistance/blob/master/NGD.py

import google
import math
import sys
import json
import urllib
import time
def googlesearch(searchfor):
    qu = urllib.urlencode({'q': searchfor})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % qu
    response = urllib.urlopen(url)
    results = response.read()
    results = json.loads(results)
    data = results['responseData']
    return data

def NormalizedGoogleDistance(arg1,arg2):
    m = 42000000000
    if not arg1 and not arg2:
        print "need two words as arguments"
    fx = int(googlesearch(arg1)['cursor']['estimatedResultCount'])
    fy = int(googlesearch(arg2)['cursor']['estimatedResultCount'])
    fxy = int(googlesearch(arg1+"+"+arg2)['cursor']['estimatedResultCount'])
    ngdnumerator = max(math.log10(fx),math.log10(fy))-math.log10(fxy)
    ngddenominator = math.log10(m)-min(math.log10(fx),math.log10(fy))
    ngd = ngdnumerator/ngddenominator
    return ngd

def NBD2(word1,word2,fx = 0):
    m = 42000000000
    if not word1 and not word2:
        print "need two words as arguments"
    if fx ==0:
        fx = baidusearch(word1)
        time.sleep(1)
    fy = baidusearch(word2)
    time.sleep(1)
    fxy = baidusearch(word1+' '+word2)
    nbdnumerator = max(math.log10(fx),math.log10(fy))-math.log10(fxy)
    nbddenominator = math.log10(m)-min(math.log10(fx),math.log10(fy))
    nbd = nbdnumerator/nbddenominator
    return nbd

def baidusearch(word):
    qu = urllib.urlencode({'wd': word})
    url = 'http://www.baidu.com/s?%s&cl=3&tn=97639490_hao_pg&rsr=0' % qu
    response = urllib.urlopen(url)
    #results = response
    for i in response:
        if '百度为您找到相关结果约' in i:
            count = int(''.join(i.decode('utf8').split(u'百度为您找到相关结果约')[1].split(u'个')[0].split(',')))
            return count
    #results = json.loads(results)
    #data = results['responseData']
    #return data

def NBD(word1,word2,fx = 0):
    m = 42000000000
    if not word1 and not word2:
        print "need two words as arguments"
    if fx == 0:
        fx = bingsearch(word1)
    fy = bingsearch(word2)
    time.sleep(1)
    fxy = bingsearch(word1+' '+word2)
    nbdnumerator = max(math.log10(fx),math.log10(fy))-math.log10(fxy)
    nbddenominator = math.log10(m)-min(math.log10(fx),math.log10(fy))
    nbd = nbdnumerator/nbddenominator
    return nbd

def bingsearch(word):
    qu = urllib.urlencode({'q': word})
    url = 'http://cn.bing.com/search?%s' % qu
    response = urllib.urlopen(url)
    results = response.read()
    count = int(''.join(results.split('<span class="sb_count">')[1].split(' 条结果')[0].split(',')))
    return count
    
       
    #results = json.loads(results)
    #data = results['responseData']
    #return data
if __name__ == '__main__':
    #print NormalizedGoogleDistance(u'12年'.encode('utf8'),u'10年代'.encode('utf8'))

    print NBD2("天上","7月 ")
   # print bingsearch('7月 ')