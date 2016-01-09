import sys
sys.path.append('libs/Wikipedia/')# #git clone git@github.com:goldsmith/Wikipedia.git

from urlparse import urlparse, urlunparse
import codecs
import fileinput
import json
import os.path
import pprint 
import requests
import results
import six
import time
import urllib, urllib2
import wikipedia

seen = {
    'NASA Open Source Agreement.data' :1, # skip
    'NASA Open Source Agreement' :1, # skip
}

def WikipediaResult(n,d=None):
    n = n + ".data"
    if not d:
        saw(n)
    if n not in seen :
        #print "Process:" + n
        if not d :
            return
        if not  d['categories']:
            return
        
        for c in d['categories']:
            cn = "Category:%s"  % c
            if  cn not in seen :
                print cn
                saw(cn)
        saw(n)


# from http://stackoverflow.com/questions/3627793/best-output-type-and-encoding-practices-for-repr-functions
def stdout_encode(u, default='UTF8'):
  return u

import codecs

def saw(x):

    x = x.decode('utf-8')
    
    y = x.encode('ascii', 'ignore')
    if x not in seen :
        seen[x]=1
        #print "saw", x

    if y not in seen :
        seen[y]=1
        #print "saw", y

def saw2(x):

    #x = x.decode('utf-8')
    
    y = x.encode('ascii', 'ignore')
    if x not in seen :
        seen[x]=1
        #print "saw", x

    if y not in seen :
        seen[y]=1
        #print "saw", y


def dowp(x):
    print "not loading from WP:" + x
    
def wp(x):
    if  x + ".data" in seen :
        #print  "TODO:process Page:" + x
        pass

def wp2(x): # ascii name
    if  x + ".data"  in seen :
        #print  "TODO:process Page:" + x
        pass

def WikipediaResultSubcat(n,d):
    if n not in seen :
        saw(n)
        wp2(n)

    if 'query' not in d:
        return
    
    for x in d['query']['categorymembers']:
        t =  x['title']
        wp(t)
        if  t not in seen :
            pass
        saw2( 'Category:' + t)

def WikipediaResultPages(n,d):
    if n not in seen :
        saw(n)
    if 'query' not in d:
        return
    for x in d['query']['categorymembers']:
        t =  x['title']      
        wp(t)
        saw2( t)


def process(filename, prefix):
    #### sub file, name
    f = open(filename)
    c = ""
    count = 0
    for l in f.readlines():
        #l = f.read();
        if l.startswith("#"):
            next
        else:
            if prefix in l:
                if count > 0 : # dont eval first line
                    #print "Eval:" + c
                    #try:
                    d = eval (c)
                    #except Exception as e:
                    #    print c
                    #    raise e

                # reset
                count = count + 1
                c = l
            else:
                c = c + l
            
    f.close()
    
def categorymembers(cmtype,category):
    url='https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'list': 'categorymembers',
        'cmtype': cmtype,
        'cmlimit': 'max',
        'format': 'json',
        'cmtitle': category,
    }
    
    r = requests.get(url, params=params)
    t = r.text
    d = json.loads(t)
    return d

def pages(category):
    return categorymembers('page',category)

def subcat(category):
    return categorymembers('subcat',category)

def data(name,x,d):
    saw(name)
    fname = "data/results_%s.py" % name
    term = "WikipediaResult%s" % name   
    f = open(fname,"a")
    f.write("%s(\"\"\"%s\"\"\"," % (term,x))
    d = pprint.pformat(d)
    f.write(d)
    f.write( ")\n")
    f.close()  

def load(name):
    fname = "data/results_%s.py" % name
    term = "WikipediaResult%s" % name
    process(fname,term)

def search (x):
    data("Pages",x, pages(x))
    data("Subcat",x, subcat(x))


load("Pages")
#pprint.pprint(seen)

load("Subcat")
#pprint.pprint(seen)

process("data/results_wikipedia_data.py", "WikipediaResult") # new
#pprint.pprint(seen)

# load the existing articles
process("data/results_wikipedia_data2.py", "WikipediaResult") # old
#pprint.pprint(seen)

