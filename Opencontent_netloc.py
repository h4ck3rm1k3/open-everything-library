#!/usr/bin/python3
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
from filelock import FileLock
import pymongo
import funcs
import re
refs = {}
links = {}

#from multiprocessing import Process, Pool
#pool = Pool(processes=20)
c = funcs.Context()

for c2 in c.extern.db.find(
        {
            'net_domain' :
            { '$exists' : False }
        }):
    
    #ParseResult(scheme='http', netloc='musicbrainz.org', path='/release-group/550bf4b9-92ca-30ba-9ea2-8b45f9d081f1', params='', query='', fragment='')
    url = c2['url']
    o = urlparse(url)
    if not o.netloc:
         print ("no netloc:" + url)
         pprint.pprint(o)

    if not o.path:
        #raise Exception( ("no path"+url))
        p = "/"
    else:
        p = o.path
        
    d = o.netloc
    s = o.scheme
        
    x = c.extern.db.update(
        {
            '_id' : c2['_id']
        },
        {
            '$set':
            {
                'net_domain': o.netloc,
                'net_path': p,
                'net_schema' : o.scheme,
                'net_params' : o.params,
                'net_query' : o.query,
            }
        }
    )
    print ("after update", x)


#pool.close()
#print ("waiting")
#pool.join()
