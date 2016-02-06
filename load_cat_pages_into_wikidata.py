#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
import wikidatabase_lookup as wb
import reverse_cats as wp
import time
import requests
import json
import shelve
import os.path
import pprint

def cache_list(name,f):
    fn = name+"_shelve"
    if not os.path.isfile(fn) :
        sd = shelve.open(fn)
        for x in f():
            sd[x]=1
        return sd
    else:
        return shelve.open(fn)

def read_list(name,f):
    d = {}
    for x in f():
        d[x]=1
    return d


class CatPage :
    def __init__(self, pages, subcats) :
        self.pages=pages
        self.subcats = {}
        self.processcats(subcats)

    def processcats(self, d):
        if d is None :
            return
        #pprint.pprint(d)
        if 'query' not in d:
            return None
        for x in d['query']['categorymembers']:
            t =  x['title']
            self.subcats[t]=x


class Cache :
    def __init__(self) :
        self.names = {}

    def open_cache(self, name):
        fn = name+"_shelve"
        sd = shelve.open(fn)
        return sd

    def data(self, name,x,d):
        # first get the data
        if name not in self.names :
            self.names[name] = self.open_cache(name)
        data =self.names[name]         
        if x not in data:
            print ("#fetch: " + name + " : "+ x )
            t = d(x) # call the function
            data[x]= t 
        else:
            return data[x]

    def search (self, x):
        pages = self.data("Pages",x, wp.pages)
        subcats =  self.data("Subcat",x, wp.subcat)
        #pprint s
        #for sc in subcats:
        #    # check if they are in the cache
        return CatPage(pages, subcats)

def ignore():
    d = {}
    filename = 'data/ignore.txt'
    f = open(filename)
    count = 0
    for l in f.readlines():
        l = l.replace("\n","")
        if l.startswith("#"):
            next
        else:
            d["Category:" +l]=1
    f.close()
    return d

def check_cats(sc,cookie, token):
    #print ("Check" + sc)

    if sc in wb.sd:
        e = 1  # skip processing
    else:
        (d,cookie2) = wb.wbgetentities(sc)
        e = wb.check_claims(d)

    if e is None:
        print ("#Missing, adding: " + sc )
        pprint.pprint(d)

        wb.sd[sc]=d # save it
        cookie.update(cookie2)
        try :
            r = wb.wbeditentity_new_item(token,cookie, sc)
        except Exception as e:
            print ("Error" + sc, e)

        time.sleep(10)

    # now

def main():
    ing = ignore()
    dc = Cache()
    
    (token,cookie) = wb.get_token()

    cats = read_list("cats",wb.wanted)
    for c in cats:
        check_cats(c,cookie,token)
        

        if c in ing:
            print ("Ignoring"+ c)
            continue

        p = dc.search(c)
        for sc in p.subcats:

            if sc not in cats:
                if sc in ing:
                    print ("Ignoring"+ sc)
                    continue
                print ("#Reading main Cat"+ c)        
                print ("#     new subcat "+sc)
                print (sc.replace("Category:",""))
                check_cats(sc,cookie,token)
            else:
                #print ("#     seen subcat "+sc)
                pass

if __name__ == "__main__":
    main()

