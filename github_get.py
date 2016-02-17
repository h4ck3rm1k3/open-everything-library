#!/usr/bin/python3

import requests
import os.path
import json
import time
import codecs
from secrets import access_token
access = '&access_token=' + access_token
import sys
start  = int(sys.argv[1])
print ("Start",start)

def get(s):

    fn = "sources/github/repositories.%d.json" % s
    
    if (os.path.isfile(fn)):
        print("opening",fn)
        f = open(fn)
        t = f.read()
    else:
        f = codecs.open(fn, "w","utf-8")
        print("getting %s to %s"  % (s, fn))
        u = 'https://api.github.com/repositories?since=%d%s' % (s,access)
        print("url",u)
        r = requests.get(u)
        t = r.text
        f.write(t)
        time.sleep(1)

    try:
        d= json.loads(t)
    except Exception as e:
        #print t
        raise e
    p = d[-1]
    return (p['id'])
    #print (t)
    

nextid = get(start)

while 1:
    nextid = get(nextid)
