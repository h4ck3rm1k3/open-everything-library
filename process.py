import json
import pprint

cats = {}

def WikipediaResult(n,d):
    #print n,
    if 'categories' in d :
        for c in d['categories']:
            if c not in cats:
                print c
                cats[c]=1
    #print pprint.pprint(d)
    #o = json.loads(d)
    #print o
