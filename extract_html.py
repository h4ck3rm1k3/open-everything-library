#!/usr/bin/python
import lxml
from lxml.html import  html5parser
#import sys
import getopt
import pprint
import sys

#optlist, args = getopt.getopt(sys.argv[1:], 't',['template='])
#pprint.pprint(optlist)
#pprint.pprint(args)
fn = sys.argv[1]
print "File in",fn
o = html5parser.parse(fn)
pprint.pprint(o)

def clean(t):
    return t.replace('{http://www.w3.org/1999/xhtml}','')

def crit(a):
    c = []
    
    for k in a:
        if k in ('capture','follow'):
            pass
        else:
            v = a[k]
            c.append("@" + k + "=" + "'" + v + "'")
        
    return "[" + " and ".join(c) + "]"
    
    
def context(x):
    p = x.getparent()
    if p:
        return context(x.getparent()) + "/"+ clean(x.tag) + crit(x.attrib)
    else:
        return clean(x.tag)
    
for element in o.iter():
    if 'capture' in element.attrib:
        #print "capture"
        print context(element)
        #print clean(element.tag)
        #pprint.pprint( element.attrib)
        #element.get('FOLLOW'),


