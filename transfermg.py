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

client = pymongo.MongoClient('mongodb://admin:password@127.0.0.1')

db = client.open_everything_library

def lookup(memcache, database, key, obj):
    if key in memcache:
        return True
    else:
        memcache[key]=1
        database.insert(obj)
        #print 'adding new new', key, obj
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

all_pages_data = load(db.page_data,"title")

all_pages = load(db.pages,"name")
wanted_pages ={}

for p in all_pages :
    d = all_pages[p]
    if 'data' in d:
        c = d['data'] 
        for pg in c:
            wanted_pages[pg]=1


merged_cats = {}

all_subcats = load(db.subcats,"name")
#pprint.pprint(all_subcats)
for p in all_subcats :
    d = all_subcats[p]
    if 'data' in d:
        c = d['data'] 
        for pg in c:
            merged_cats[pg]=1    

all_cats  = load(db.interesting_categories,"category")
#pprint.pprint(all_cats)
for p in all_cats :
    merged_cats[p]=1    

#exit(0)

sys.path.append('libs/Wikipedia/')# #git clone git@github.com:goldsmith/Wikipedia.git
import wikipedia

seen = {}

def WikipediaResult(n,d=None):
    name = n
    n = n + ".data"
    #if not d:
    #    saw(n)

        #    saw(n)
    if n not in seen:
        seen[n]=d
        if name not in wanted_pages :
            #print "Skip", n
            pass
        else:
            print "want page", name
            # save the page data
            lookup(all_pages_data, db.page_data, name, d)


    if "Category:" in name :
        if name not in merged_cats:
            #print "missing", name
            pass
        else:
            print "wanted cat", name


# from http://stackoverflow.com/questions/3627793/best-output-type-and-encoding-practices-for-repr-functions
def stdout_encode(u, default='UTF8'):
  return u

def saw2(x):
    y = x.encode('ascii', 'ignore')
    if x not in seen :
        seen[x]=1
        print "saw", x
    if y not in seen :
        seen[y]=1
        print "saw", y

def saw(x):
    x = x.decode('utf-8')
    return saw2(x)

def dowp(x):
    x = x.replace("Category:Category:","Category:")
    print "loading from WP:" + x
    #return

    print( "#" + x)
    try :
        results = wikipedia.page(x)
        #d = pprint.pformat(results.content)
        #pprint.pprint(results.__dict__)
        #pprint.pprint(dir(results))
        o = {
            'content': results.content,
            'categories' : results.categories,
            #'coordinates' : results.coordinates(),
            'images' : results.images,
            'links' : results.links,
            'original_title' : results.original_title,
            'pageid' : results.original_title,
            'references' : results.references,
            'revision_id' :results.revision_id,
            #'section' :results.section,
            'sections' :results.sections,
            'summary' :results.summary,
            'title': results.title,
            'url' : results.url,
        }
        #pprint.pprint(o)
        d = json.dumps(o)
    except Exception as e:
        print "error:", e
        d = ""
    fname = "data/results_wikipedia_data.py"
    with FileLock("myfile.txt"):
        f = codecs.open(fname,mode="a", encoding="utf-8")
        #f.write( "#" + x + "\n")
        x2 = x.replace("\"","\\\"") # quotex
        f.write(    "WikipediaResult(\"\"\"%s\"\"\",%s)\n" % (x2, d))
        f.close()

    print "zzz"
    time.sleep(1)

def wp(x):
    if  x + ".data" not in seen :
        #print  "load Page:" + x
        #saw2(x + ".data")
        #return # skip for now
        dowp(x)
    else:
        return

def wp2(x): # ascii name
    if  x + ".data" not in seen :
        #print  "load Page:" + x
        #saw(x + ".data")
        #return # skip for now
        dowp(x)
    else:
        return

subcats = {}

def WikipediaResultSubcat(n,d):
    if not 'query' in d:
        return
    m = d['query']['categorymembers']
    if len(m) == 0:
        return
    _subcats = []
    for x in m:
        t =  x['title']
        _subcats.append(t)
    subcats[n]= _subcats

allpages = {}

def WikipediaResultPages(n,d):
    if not 'query' in d:
        return
    _pages = []
    for x in d['query']['categorymembers']:
        t =  x['title']
        _pages.append(t)
    allpages[n]= _pages

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
                    try:
                        d = eval (c)
                    except Exception as e:
                        #print c
                        d = eval (c)
                        #raise e

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

process("data/results_wikipedia_data.py", "WikipediaResult") # new
process("data/results_wikipedia_data2.py", "WikipediaResult") # old

load("Pages")
#pprint.pprint(allpages)

#pprint.pprint(seen)

load("Subcat")
#pprint.pprint(subcats.keys())


def transfer(key, all_mem, target, name, source):

    if key in source:
        #print "not cached", key, name
        data = source[key]
        o = {
            "name": c,
            "data" : data
        }
        if not lookup(all_mem, target, key, o):
            #print "added" , key, name
            pass
        else:
            #print "new", name, key
            pass
            
        #new item add
    else:
        #print "Missing", name, key
        pass

for line in fileinput.input():

    line = line.replace("\n","")
    name = line
    c = "Category:"+line
    #if c not in all_:

    o = {"category": c }

    if not lookup(all_cats, db.interesting_categories, c, o):
        print "new '%s'" % c
        search(c)
        # process the cat
        
    transfer(c, all_subcats,db.subcats,"subcats",subcats)
    transfer(c, all_pages,db.pages,"pages",allpages)

# now finally transfer all the pages to mongo

