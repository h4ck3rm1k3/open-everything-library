from urlparse import urlparse, urlunparse
import codecs
import fileinput
import json
import os.path
import pprint
import requests
import results
import six
import sys
import time
import urllib, urllib2
from filelock import FileLock
import pymongo
import funcs

c = funcs.Context()
cname = 'Category:'
name = 'Open content'
seen = {
    'Category:Public domain books' :1,
    'Category:Public domain music' :1,
    'Category:Public commons' : 1,
    'Category:Citizen media' : 1, 
    'Category:Linux software' : 1  # dont process this because it is full of non free software
}

def recurse(n, p):
    if n not in seen:
        seen[n]=1
    else:
        return
    
    if n not in c.cats.data:
        print "going to add", n
        c.add_cat(n,p)
        #exit(0)
    else:
        s = c.cats.data[n]
        #print.pprint(s)
        subcats = s['subcats']
        if subcats:
           # pprint.pprint(subcats)
            for sc in subcats:
                p2 = list(p)
                p2.append(n)
                recurse(sc, p2)

        pages = s['pages']
        if pages:
            #pprint.pprint(pages)
            for pg in pages:
                p2 = list(p)
                p2.append(n)
                if pg not in c.pages.pages.data:
                    print "TODO", pg, p, n
                    c.pages.get(pg)
        # pages
    
#Category:Open Content and all subcats.
recurse(cname + name,[])
