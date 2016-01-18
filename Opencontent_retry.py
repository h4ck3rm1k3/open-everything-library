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

from multiprocessing import Process, Pool

def extern(url):

        
    if url  in c.extern.data:
        print ("exists",url)
        return
    
    print ("loading link",url)

    try:
        resp = requests.head(url, timeout=1)
        head = {
            'code': resp.status_code,
            'text' : resp.text,
            'hdrs' :  resp.headers
        };

    except Exception as e:
        pprint.pprint(e)
        c.extern.add(url,
                     {
                         'data': None,
                         'url': url,
                         #'head' : head,
                         'error' : str(e),
                     })
        return None
    
    clen = 0
    tlen = 0
    if  'Content-Length' in resp.headers:
        tlen = resp.headers['Content-Length']
        g = re.match('(\d+)', tlen)
        clen = 0
        if  g:
            tp = g.groups()[0]
            print(tp, tlen)
            clen = int(tp)        

    print("getting size", url, clen, tlen)
          #, pprint.pformat(resp.headers))
        

    try:
        html = requests.get(url, timeout=1,verify=False, stream=True).text
        head = {
            'code': resp.status_code,
            'text' : resp.text,
            'hdrs' :  resp.headers
        };
        # truncat
        if len(html) <  20000:
            print ("Truncating html",len(html), url)
            html = None
            
        c.extern.add(url,
                     {
                         'data':html,
                         'url': url,
                         'head' : head
                     })
        

    except Exception as e:
        pprint.pprint(e)
        c.extern.add(url,
                     {
                         'data': None,
                         'url': url,
                         #'head' : head,
                         'error' : str(e),
                     } )
        return

pool = Pool(processes=20)

c = funcs.Context()

# build a res
y = ("\." + x for x in funcs.skip)
res = '.+(' +  "|".join( y)  + ")+$"
resre = re.compile(res)

seen = {}


for c2 in c.extern.db.find(
        {
            'length' :
            { '$exists' : False }
        }):
    l = -5
    #pprint.pprint(c2)
#db.external_pages.find({ ,{'url':1, 'length':1})
    if 'length'  in c2:
        # we did this
        continue
            
    url = c2['url']

    #ParseResult(scheme='http', netloc='musicbrainz.org', path='/release-group/550bf4b9-92ca-30ba-9ea2-8b45f9d081f1', params='', query='', fragment='')
    o = urlparse(url)
    if not o.netloc:
        print ("no netloc",url)
        l = -3
        #continue

    if not o.path:
        print ("no path",url)
        l = -2
        #continue

    p = o.path
    
    #pprint.pprint(o)
    d = o.netloc
    if d in seen:
        seen[d]=seen[d]+1
    else:
        #print ("new domain",d)
        seen[d]=1
    
    m  = re.match(resre,p)    
    if (m):
        #print ("skip", url, p , m.groups())
        l = -1
        #continue

    if 'data' not in c2:
        #print ("no data",url)
        l = 0
        #continue
        d = None
    else:   
        d = c2['data']
    
    if d is None :
        #print ("no data2",url)
        #continue
        l = -6
    else:
        l = len(d)
        
    print ("Update",url,l)
    x = c.extern.db.update(
        {
            '_id' : c2['_id']
        },
        {
            '$set':
            {
                'length': l
            }
        }
    )
    print ("after update", x)


pool.close()

print ("waiting")
pool.join()
