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
import logging

# # these two lines enable debugging at httplib level (requests->urllib3->httplib)
# # you will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# # the only thing missing will be the response.body which is not logged.
# import httplib
# httplib.HTTPConnection.debuglevel = 1

# logging.basicConfig() # you need to initialize logging, otherwise you will not see anything from requests
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

def recurse(n, p):
    if n not in seen:
        seen[n]=1
    else:
        return
    
    if n not in c.cats.data:
        c.add_cat(n,p)       
        #xit(0)
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

#Category:Open Content and all subcats.
recurse(cname + name,[])
