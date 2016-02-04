#
import wikidatabase_lookup as wb
import reverse_cats as wp
import time
import requests
import json
import shelve
import os.path


def cache_list(name,f):
    fn = name+"_shelve"
    if not os.path.isfile(fn) :
        sd = shelve.open(fn)
        for x in f():
            sd[x]=1
        return sd
    else:
        return shelve.open(fn)

class CatPage :
    def __init__(self, pages, subcats) :
        self.pages=pages
        self.subcats = {}
        self.processcats(subcats)

    def processcats(self, d):
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
            print ("fetch: " + name + " : "+ x )
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


def main():
    dc = Cache()
    cats = cache_list("cats",wb.wanted)
    for c in cats:
        print (c)
        p = dc.search(c)
        for sc in p.subcats:
            if sc not in cats:
                print (" Missing" + sc )

if __name__ == "__main__":
    main()

