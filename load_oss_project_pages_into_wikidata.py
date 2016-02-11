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

dry_run = False

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

class Session:
    def __init__(self) :
        (token,cookie) = wb.get_token()
        self.token=token
        self.cookie=cookie

sd = shelve.open("wikidatacats_shelve")
def check_entity(sc,s):

    if sc.startswith("Wikipedia:"):
        print ("Not adding WP stuff: " + sc)

    if sc.startswith("User:"):
        print ("Not adding User stuff: " + sc)

    print ("Check: " + sc)        
    if sc in sd:
        e = 1  # skip processing
    else:
        (d,cookie2) = wb.wbgetentities(sc)
        e = wb.check_claims(d)

    if e is None:
        print ("#Missing, adding: " + sc )
        pprint.pprint(d)

        sd[sc]=d # save it
        s.cookie.update(cookie2)
        try :
            if not dry_run:
                r = wb.wbeditentity_new_item(s.token,s.cookie, sc)
                time.sleep(15)
            else:
                print ("#skipping in dry run: " + sc )

        except Exception as e:
            print ("Error" + sc, e)




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
        return CatPage(x, pages, subcats)

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


def main():
    ing = ignore()
    dc = Cache()
    s = Session()
    seen = {}
    f = open ("data/source_code_pages_final.txt")
    for l in f.readlines():
        d =l.split()

        name = None

        if len(d) > 2:
            pid =  d[2]

            if pid not in seen:
                seen[pid]=1
            else :
                continue
            if len(d) > 5:
                name = " ".join(d[3:-1])
            else:
                name = d[3]
        url = d[-1]
        if not name :
            #print(d)            
            continue
        if len(name) == 0:
            print(d)
            #continue
        if 'User:' in name :
            continue
        if 'File:' in name:
            continue
        if 'Template:' in name:
            continue
        if 'Help:' in name:
            continue

        if 'Wikipedia:' in name:
            continue

        if "creativecommons.org/licenses" in url :
            continue
        print (name, url, pid)
        check_entity(name,s)
        #time.sleep(20)


        
    # cats = read_list("cats",wb.wanted)
    # for c in cats:
        
    #     if c in ing:
    #         print ("Ignoring"+ c)
    #         continue

    #     p = dc.search(c)
    #     p.check_entity(c,s)

    #     p.proc_subcats(cats, ing) # process the subcats
    #     p.proc_pages(s) # process the subcats

if __name__ == "__main__":
    main()

