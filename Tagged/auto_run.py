#!/usr/bin/python
# -*- coding:utf-8 -*-
#author:iuyyoy 

import os,sys,time
sys.path.append(sys.path[0]+'/..')

def auto_run(command,max_error_number = 100):
	stop = False
	count = 0
	while (not stop):
		stop = not os.system(command)
		count += 1
		print "run %d times" %(count)
		if count == max_error_number:
			return False
		time.sleep(1)
def auto_run2(command,max_error_number = 100):
	stop = False
	count = 0
	for i in range(max_error_number):
		os.system(command)
		print "run %d times" %(i)
		time.sleep(2)
if __name__ == '__main__':
	if(len(sys.argv) > 1):
		auto_run(sys.argv[1])
	else:
		auto_run2('python new_web_tags.py')
