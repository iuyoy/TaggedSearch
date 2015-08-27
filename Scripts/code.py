#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy

def print_whatever_code(str):
    try:
        print str
    except:
        print str.encode('utf-8')