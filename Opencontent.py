from urllib.parse import urlparse, urlunparse
import codecs
import fileinput
import json
import os.path
import pprint
import requests
#import results
import six
import sys
import time
import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse
#from filelock import FileLock
#import pymongo
import funcs

c = funcs.Context()
cname = 'Category:'
#name = 'Open content'
seen = {
    'Category:Linux_software':1,
    'Category:WikiProject Open Access articles':1, # tons of articles, not relevant
    'Category:Articles with imported Creative Commons Attribution 3.0 text' :1,
    'Category:Articles with imported Creative Commons Attribution 2.5 text':1,
    'Category:X Window programs':1,
    'Category:Single-board computers':1,
    'Category:Mozilla add-ons':1,
    'Category:Firefox OS software' :1,
    'Category:Android (operating system) software' :1,
    'Category:Android (operating system) games':1,
    'Category:Public domain books' :1,
    'Category:Public domain music' :1,
    'Category:Public commons' : 1,
    'Category:Citizen media' : 1, 
    'Category:Linux software' : 1  # dont process this because it is full of non free software
}

def wanted():
    filename = 'data/allcats.txt'
    f = open(filename)
    count = 0
    for l in f.readlines():
        l = l.replace("\n","")
        if l.startswith("#"):
            next
        else:
            yield "Category:" +l
    f.close()

def recurse(n, p):
    if n not in seen:
        seen[n]=1
    else:
        return

    if n not in c.pages.pages.data:
        print("TODO get cat page", n, p)
        c.pages.get(n)

                    
    if n not in c.cats.data:
        print("going to add", n)
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
                #recurse(sc, p2)

        pages = s['pages']
        if pages:
            #pprint.pprint(pages)
            for pg in pages:
                p2 = list(p)
                p2.append(n)
                if pg not in c.pages.pages.data:
                    #print("TODO", pg, p, n)
                    c.pages.get(pg)
        # pages
    
#Category:Open Content and all subcats.
for name in wanted():
    print ("check" + name)
    if 'Category:' not in name:
        recurse(cname + name,[])
    else:
        recurse(name,[])
