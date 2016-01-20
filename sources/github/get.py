import requests
import os.path
import json
import time
import codecs
access_token='2611e35ee48db6f47777b749b8075a9de41a0b7d'
access = '&access_token=' + access_token
import sys
start  = int(sys.argv[1])
print ("Start",start)

def get(s):

    fn = "repositories.%d.json" % s
    
    if (os.path.isfile(fn)):
        print("opening",fn)
        f = open(fn)
        t = f.read()
    else:
        f = codecs.open(fn, "w","utf-8")
        print("getting",s)
        u = 'https://api.github.com/repositories?since=%d%s' % (s,access)
        print("url",u)
        r = requests.get(u)
        t = r.text
        f.write(t)
        time.sleep(2)

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
