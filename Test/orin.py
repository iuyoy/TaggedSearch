a = ['a','b','c']
if ('a' in a):
    print 'a'
if ('b' in a):
    print 'b'
if ('e' in a or 'd' in a):
    print 'ab'
if ('e' or 'd' in a):
    print 'ba'
if ('a' and 'd' in a):
    print 'da'