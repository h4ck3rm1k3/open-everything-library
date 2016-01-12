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

c = funcs.Context()
cname = 'Category:'
name = 'Open content'
seen = {
    # dont care about open access right now  
    'Category:Android (operating system) games':1,
    'Category:Android (operating system) software' :1,
    'Category:Articles with imported Creative Commons Attribution 2.5 text':1,
    'Category:Articles with imported Creative Commons Attribution 3.0 text' :1,
    'Category:Citizen media' : 1,
    'Category:Debian people' :1 ,
    'Category:Firefox OS software' :1,
    'Category:Free software companies' : 1,
    'Category:Free software people': 1,
    'Category:FreeBSD people': 1,
    'Category:FreeDOS people': 1,
    'Category:GNOME companies' :1,
    'Category:GNU people':1,
    'Category:Inferno (operating system) people' : 1,
    'Category:Linux companies': 1,
    'Category:Linux people': 1,
    'Category:Linux software' : 1,  # dont process this because it is full of non free software
    'Category:Mozilla people' : 1,
    'Category:NetBSD people': 1,
    'Category:Netscape people': 1,
    'Category:Open access (publishing)' :1,
    'Category:Open content activists':1,
    'Category:Open hardware organizations and companies': 1,
    'Category:Open source people': 1,
    'Category:OpenBSD people' : 1,
    'Category:People associated with Bitcoin': 1,
    'Category:Perl people': 1,
    'Category:Plan 9 people': 1,
    'Category:Public commons' : 1,
    'Category:Public domain books' :1,
    'Category:Public domain music' :1,
    'Category:Red Hat people': 1,
    'Category:Single-board computers':1,
    'Category:Ubuntu (operating system) people' :1,
    'Category:WikiProject Open Access articles':1, # tons of articles, not relevant
    'Category:WikiProject Open Access' :1,
    'Category:Wikimedia Foundation people': 1,
    'Category:Wikipedia people':1,
    'Category:X Window System people': 1,
    'Category:X Window programs':1,
}

def  catpage(data, n, p):
    #pprint.pprint(data)
    #print( "cat",data['title'])
    #pprint.pprint(data.keys())
    pass


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
    if not 'Content-Length' in resp.headers:
        pprint.pprint(resp.headers)
    else:
        tlen = resp.headers['Content-Length']
        g = re.match('(\d+)', tlen)
        clen = 0
        if  g:
            tp = g.groups()[0]
            print(tp, tlen)
            clen = int(tp)        

    print("getting size", url, clen, tlen, pprint.pformat(resp.headers))
        
    if clen < 10000:
        try:
            html = requests.get(url, timeout=1).text
            head = {
                'code': resp.status_code,
                'text' : resp.text,
                'hdrs' :  resp.headers
            };

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
        
        else:
            print("too big", clen)
            pprint.pprint(head)
            
            c.extern.add(url,
                         {
                             'data': None,
                             'url': url,
                             'head' : head
                        }
            )
            
            
def page(data, n, p ):
    print( "page",n,p ) 

    for l in data['links']:
        if 'http' in l:
            if l not in links :
                links[l]=1
                extern(l)
                
    for l in data['references']:
        if 'http' in l:
            if l not in links :
                links[l]=1
                extern(l)


def recurse(n, p):
    if n not in seen:
        seen[n]=1
    else:
        return

    #print("Process:", n, p)
    if n not in c.pages.pages.data:
        print("TODO1 add :", n, p)      
        c.pages.get(n)
        pass
    else:
        data = c.pages.pages.data[n]
        catpage(data, n, p )
                    
    if n not in c.cats.data:
        print("Missing cat", n)
        exit(0)
    else:
        s = c.cats.data[n]
        subcats = s['subcats']
        if subcats:
            for sc in subcats:
                p2 = list(p)
                p2.append(n)
                recurse(sc, p2)

        pages = s['pages']
        if pages:
            for pg in pages:
                p2 = list(p)
                p2.append(n)
                if pg not in c.pages.pages.data:
                    if pg not in c.redirs.data:
                        print("TODO2", pg, p, n)
                        c.pages.get(pg)
                    else:
                        pg = c.redirs.data[pg]['to']
                        if pg not in c.pages.pages.data:
                            print("TODO3", pg, p, n)
                            c.pages.get(pg)
                        else:
                            data = c.pages.pages.data[pg]
                            page(data, pg, p)
                else:
                    data = c.pages.pages.data[pg]
                    page(data, pg, p)
        # pages
    
#Category:Open Content and all subcats.
recurse(cname + name,[])
