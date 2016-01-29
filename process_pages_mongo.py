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

wanted_pages ={}
merged_cats = {}

client = pymongo.MongoClient('mongodb://admin:password@127.0.0.1')
db = client.open_everything_library

class Wrapper:
    def __init__(self, db , key, alt_fields=None):
        self.db   = db
        self.data = funcs.load(db,key,alt_fields)

class PageWrapper:
    def __init__(self, pages, redirs):
        self.pages  = pages
        self.redirs = redirs

    def get(self, p2):

        if p2 in  pages.pages.data:
            pd = pages.pages.data[p2]    
            print "found page", p2, "in", p 
        else:
            if p2 in  pages.redirs.data:
                r = pages.redirs.data[p2]
                return self.get(r)
            else:
                print "missing page", p2, "in", p
                funcs.fetch_page(p2,self.pages.db, self.redirs.db)
            #exit(0)
        
cats   = Wrapper(db.categories,"name")
page_data  = Wrapper(db.page_data,"title",alt_fields=['name'])
redirs = Wrapper(db.redirs,"name")

pages = PageWrapper(page_data, redirs)



skip = {
    'Category:OS X' : 1,
    'Category:Articles with imported Creative Commons Attribution-ShareAlike 3.0 text' :1,
    'Category:Articles with imported Creative Commons Attribution 3.0 text':1   ,
    'Category:Linux games':1,
    'Category:Free daily newspapers':1,
}

for p in cats.data :
    
    if p in skip:
        print "Skipping", p
        next
    else:
        d = cats.data[p]
        if 'pages' not in d:
            print "no pages", p
        else:
            pl = d['pages']
            if not pl :
                print "no data", p
            else:
                for p2 in pl:
                    print "going to fetch", p2, "from:", p
                    pages.get(p2)

                
