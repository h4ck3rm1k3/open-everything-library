import requests
import sys
import pprint
import six
import urllib
import urllib.parse
reserved = {
    'property' : 'prop'
}

def varname(x):
    if x in reserved:
        return reserved[x]
    return x

for u in sys.argv[1:]:
    up = urllib.parse.urlparse(u)
    url= up.scheme + '://' + up.netloc + up.path
    qs = up.query
    q = urllib.parse.parse_qs(qs)
    args = []
    action = None

    if 'action' in q:
        action = q['action'][0]
        del q['action']


    for k in q:
        v = q[k][0]
        args.append("{name} = '{value}'".format(name=varname(k),value=v))

    if action:
        print ('def '+ action +' (' + (','.join(args)) + '):')
        print ("    action = \'{action}\'".format(action=action))
    else:
        
        print ('def '+ 'FOO' +' (' + (','.join(args)) + '):')

    print ("    url = \'{url}\'".format(url=url))
    print ("    params = {")
    if action:
        print ("        'action' : action,")
    for k in q:
        print ("        '{name}' : {variable},".format(name=k, variable=varname(k)))
    print ("    }")
    print ( "    return process(url,params)")
