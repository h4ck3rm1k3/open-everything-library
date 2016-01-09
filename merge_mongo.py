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
# db.addUser( { user: "admin", pwd: "password", roles: [ "userAdminAnyDatabase" ] } )

def lookup(memcache, database, key, obj):
    if key in memcache:
        return True
    else:
        memcache[key]=1
        database.insert(obj)
        print 'adding new new', key
        return False

def load(d,field):
    #d = db.pages
    res = {}
    for c in d.find():
        #pprint.pprint(c)
        if field not in c:
            print "Missing", field, "in", pprint.pformat(c)
        else:
            cn = c[field]
            res[cn]=c
    return res

def load_data(db, field, target):
    for p in db :
        d = db[p]
        if field in d:
            c = d[field]
            for pg in c:
                target[pg]=1

wanted_pages ={}
merged_cats = {}

client = pymongo.MongoClient('mongodb://admin:password@127.0.0.1')
db = client.open_everything_library
all_pages = load(db.pages,"name")
all_subcats = load(db.subcats,"name")
all_cats  = load(db.interesting_categories,"category")

all_cats2 = load(db.categories,"name")

load_data(all_pages, 'data', wanted_pages)
load_data(all_subcats, 'data', merged_cats)

for p in all_cats :
    #merged_cats[p]=1
    d = all_cats[p]

    sc = None
    pages = None
    
    if p in all_subcats:
        sc = all_subcats[p]['data']

    if p in  all_pages:
        pages = all_pages[p]['data']

    new = {
        'name' : p,
        'subcats': sc,
        'pages': pages,
    }

    #pprint.pprint(new)
    lookup(all_cats2, db.categories, p , new)

