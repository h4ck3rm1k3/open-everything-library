#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/h4ck3rm1k3/experiments/requests/')
import time
import requests
import json
import shelve
import pprint
import secrets;
import time
import logging

debug = 0
if debug:
    # Enabling debugging at http.client level (requests->urllib3->http.client)
    # you will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
    # the only thing missing will be the response.body which is not logged.
    try: # for Python 3
        from http.client import HTTPConnection
    except ImportError:
        from httplib import HTTPConnection
    HTTPConnection.debuglevel = 1

    logging.basicConfig() # you need to initialize logging, otherwise you will not see anything from requests
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def wanted():
    filename = 'data/allcats.txt'
    f = open(filename)
    count = 0
    for l in f.readlines():
        l = l.replace("\n","")
        if l.startswith("#"):
            next
        else:
            yield "Category:" +l
    f.close()

def makeReport(db,query):
    cursor = db.cursor()
    cursor.execute(query)
    text = ''
    #for val, cnt in cursor:
        #text += table_row.format(val,('{:,}'.format(cnt)))
    return text

BASE_URL='http://directory.fsf.org/w/api.php'

def login(user, passw, token=None, cookies=None):

    params = {
        'action': 'login',
        'format' : 'json',
        'lgname' : user,
        'lgpassword' : passw,
    }
    if token :
        params['lgtoken']=token
    if cookies:
        r = requests.post(BASE_URL, params=params, cookies=cookies)
    else:
        r = requests.post(BASE_URL, params=params)
    t = r.text
    #print ("login text: " + t)
    d = json.loads(t)
    #print ("logged: ")
    #pprint.pprint(d)
    return (d,r.cookies)


def dologin():
    d = login (
        secrets.wikidata['user'],
        secrets.wikidata['password']
    )
    token=d[0]
    cookies=d[1]
    (token2,cookies2) = login (
        secrets.wikidata['user'],
        secrets.wikidata['password'],
        token['login']['token'],
        cookies,
    )
    return (token2['login']['lgtoken'],cookies2)

def pprocess(r):
    t = r.text

    try:
        d = json.loads(t)
        if 'error' in d:
            pprint.pformat(r)
            raise Exception(pprint.pformat(d))
        return (d, r.cookies)

    except Exception as e:
        print ("error: " + t + " Err "+ str(e))
        raise e

def process(url, params, cookies=None):
    if cookies:
        #print("Cookies")
        #pprint.pprint(cookies)
        pass
    return pprocess(requests.get(url, params=params, cookies=cookies))


def post(url, body, cookies):
    try:
        #print("Cookies")
        #pprint.pprint(cookies)
        rs= requests.post(url,
                          #headers = {
                          #    'content-type': 'application/json'
                          #},
                          data=body,
                          #json=body,
                          cookies=cookies)
        return pprocess(rs)
        #cookies.update(rs.cookies)
        #return r
    except Exception as e:
        pprint.pprint(body)
        raise e

def query_tokens (cookies, meta = 'tokens'):
    action = 'query'

    params = {
        'format' : 'json',
        'type' : 'csrf', #|deleteglobalaccount|patrol|rollback|setglobalaccountstatus|userrights|watch
        'action' : action,
        'meta' : meta,
    }
    return process(BASE_URL,params,cookies)

def wbcreateclaim (entity,token,cookies,
                   _property,snaktype,value):
    action = 'wbcreateclaim'

    params = {
        #'utf8': '',
        'value': json.dumps({
            'entity-type':'item',
            'numeric-id': value
        }),
        #'bot': '',
        'action' : action,
        'entity' : entity,
        'format' : 'json',
        'property' : _property,
        'snaktype' : snaktype,
        #'value' : value,
        'token': token,
    }

    return post(BASE_URL,params, cookies)

def wbcreateclaim_instance_of_FreeSoftware (
        entity,
        token,
        cookies,
        _property = 'P31',
        snaktype = 'value',
        value = 341): # Q341 is free software
    return wbcreateclaim (entity,token,cookies, _property,snaktype,value)

def wbcreateclaim_instance_of_Wikimedia_category (
        entity,
        token,
        cookies,
        _property = 'P31',
        snaktype = 'value',
        value = 4167836):
    return wbcreateclaim (entity,token,cookies, _property,snaktype,value)

def wbgetentities(x):

    params = {
        'action': 'wbgetentities',
        'sites' : 'enwiki',
        'titles' : x,
        'redirects': 'yes',
        'format' : 'json',
        'props': 'info|sitelinks|aliases|labels|descriptions|claims|datatype'
    }
    return process(BASE_URL,params)

def wbgetentities_by_id(x):

    params = {
        'action': 'wbgetentities',
        'ids' : x,
        'redirects': 'yes',
        'format' : 'json',
        'props': 'info|sitelinks|aliases|labels|descriptions|claims|datatype'
    }
    return process(BASE_URL,params)


def check_claims(d):
    if 'entities' in d:
        if '-1' in d['entities']:
            #print ("todo: " +x)
            return None
        else:
            for e in d['entities']:
                if not e:
                    continue
                ed = d['entities'][e]
                #for c in ed['claims']:
                if 'P31' not in ed['claims']:
                    #print ("to add: " +x)
                    #wbcreateclaim_instance_of_Wikimedia_category(e,csrftoken,edit_cookie)
                    #                    time.sleep(5)
                    return e
                else:
                    #pprint.pprint(ed)
                    #print ("Ok"+ x)
                    return 1

def wbeditentity_new_item (
        token,
        cookie,
        name,
):
    action = 'wbeditentity'
    bot = '1'
    maxlag = '5'
    _format = 'json'
    _assert = 'user'
    new = 'item',
    summary = 'Bot: New item with sitelink from [[wikipedia:en:{name}]]'.format(name=name)
    data = {
        "labels": 
        {
            "en": 
            {
                "value": name, 
                "language": "en"
            }
        }, 
        "sitelinks": 
        {
            "enwiki": 
            {
                "site": "enwiki", 
                "title": name
            }
        }
    }


    params = {
        'action' : action,
        'maxlag' : maxlag,
        'format' : _format,
        'new' : new,
        'assert' : _assert,
        'bot' : bot,
        'token' : token,
        'summary' : summary,
        'data' : json.dumps(data)
    }
    #return process(url,params)
    return post(BASE_URL,params, cookie)

def get_token():
    (token,cookies) = dologin()
    #pprint.pprint(cookies)
    (crsft,cookies2) = query_tokens(cookies)
    #pprint.pprint(cookies2)
    edit_cookie = cookies.copy()
    edit_cookie.update(cookies2)
    #pprint.pprint(edit_cookie)
    #pprint.pprint(crsft['query']['tokens'])
    csrftoken = crsft['query']['tokens']['csrftoken']
    return (csrftoken,edit_cookie)

def query_external (euquery, cont = None, namespace=None, _list = 'exturlusage'):
    action = 'query'

    params = {
        'action' : action,
        'list' : _list,

        'format' : 'json',
        'eulimit': 500,
        'euexpandurl' : 1,
        'euquery' : euquery,
        'generator' : 'allpages'

        #&format=jsonfm
    }
    if namespace :
        params['apnamespace']=namespace

    if cont :
        params.update(cont)

    return process(BASE_URL,params)


def add_instance(x):
    if x not in sd:
        print ("fetch new " + x)
        (d,c) = wbgetentities(x)
        time.sleep(1)
        sd[x]=d
    else:
        d=sd[x]
    e = check_claims(d)
    if e and e != 1:
        print ("fetch check: " + x)
        (d,c) = wbgetentities(x)
        sd[x]=d
        time.sleep(1)
        e= check_claims(d) # check again after fetch
        if e and e != 1:
            print ("To Fix: "+ x)
            wbcreateclaim_instance_of_Wikimedia_category(e,csrftoken,edit_cookie)
            (d,c) = wbgetentities(x)
            sd[x]=d
            time.sleep(10)
            return d
        else:
            return d
    else:
        print ("Ok:"+ x)
        return d


def main():
    (token,cookies) = dologin()
    #pprint.pprint(cookies)
    (crsft,cookies2) = query_tokens(cookies)
    #pprint.pprint(cookies2)
    edit_cookie = cookies.copy()
    edit_cookie.update(cookies2)
    #pprint.pprint(edit_cookie)
    #pprint.pprint(crsft['query']['tokens'])
    csrftoken = crsft['query']['tokens']['csrftoken']

    for x in wanted():
        #

        if x not in sd:
            print ("fetch new " + x)
            (d,c) = wbgetentities(x)
            time.sleep(1)
            sd[x]=d
        else:
            d=sd[x]
        e = check_claims(d)
        if e and e != 1:
            print ("fetch check: " + x)
            (d,c) = wbgetentities(x)
            sd[x]=d
            time.sleep(1)
            e= check_claims(d) # check again after fetch
            if e and e != 1:
                print ("To Fix: "+ x)
                wbcreateclaim_instance_of_Wikimedia_category(e,csrftoken,edit_cookie)
                (d,c) = wbgetentities(x)
                sd[x]=d
                time.sleep(10)
        else:
            print ("Ok:"+ x)

            


if __name__ == "__main__":
    main()
