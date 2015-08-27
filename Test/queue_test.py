#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import Queue
q = Queue.Queue()
q.put(1)
if (1 in q):#error
    print True