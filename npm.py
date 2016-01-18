#!/usr/bin/python3

import pymongo
import pprint 
import funcs
import json
d = json.load(open("sources/npm/.cache.json"))
c = funcs.Context()


def clean(name,v):
    if name in v:        
        _data = v[name]
        if type(_data) is dict:
            n_data = []
            for vn in _data.keys() :
                vd = _data[vn]
                n_data.append([vn, vd ])
            v[name ] = n_data
    #return v

def clean2(name, v):
    # just take the keys
    if name in v:
        d2 = v['users']
        nd = []
        for k in d2.keys() :
            vd = d2[k]
            nd.append(k)
        v['users'] = nd

for nid in d.keys():

    v = d[nid]
    
    if not type(v) is dict:
        print( "Skip")
        pprint.pprint({ nid: v})
        
        continue
    
    v["_nid"]=nid
    cleanid = nid.replace(".","_")

    
    clean2('users',v)
    clean('versions',v)
    clean('dist-tags',v)

    clean('repository',v)
    
    #print (nid)

    try:
        c.npm.add(cleanid,v)
    except Exception as e:
        print (e)
        print ("ITEM:",pprint.pformat(v))
        raise e
