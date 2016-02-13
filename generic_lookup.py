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

class Session:
    def __init__(self) :
        (token,cookie) = wb.get_token()
        self.token=token
        self.cookie=cookie

class WikimediaApi :
    
    DEFAULT_BASE_URL2='http://directory.fsf.org/w/api.php'
    DEFAULT_BASE_URL='https://www.wikidata.org/w/api.php'
    def __init__(self, baseurl=DEFAULT_BASE_URL):
        self.baseurl=baseurl
        self.session = None
        

    def login(self, user, passw, token=None, cookies=None):

        params = {
            'action': 'login',
            'format' : 'json',
            'lgname' : user,
            'lgpassword' : passw,
        }
        if token :
            params['lgtoken']=token
        if cookies:
            r = requests.post(self.base_url, params=params, cookies=cookies)
        else:
            r = requests.post(self.base_url, params=params)
        t = r.text
        #print ("login text: " + t)
        d = json.loads(t)
        #print ("logged: ")
        #pprint.pprint(d)
        self.session = Session(d,r.cookies)

    def dologin(self):
        d = login (
            secrets.generic[self.baseurl]['user'],
            secrets.generic[self.baseurl]['password'],
        )
        token=d[0]
        cookies=d[1]
        self.login (
            secrets.generic[self.baseurl]['user'],
            secrets.generic[self.baseurl]['password'],
            token['login']['token'],
            cookies,
        )

    def pprocess(self,r):
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

    def process(self, params, cookies=None):
        return self.pprocess(requests.get(self.baseurl, params=params, cookies=cookies))


    def post(self, body, cookies):
        try:
            #print("Cookies")
            #pprint.pprint(cookies)
            rs= requests.post(self.baseurl,
                              #headers = {
                              #    'content-type': 'application/json'
                              #},
                              data=body,
                              #json=body,
                              cookies=cookies)
            return self.pprocess(rs)
            #cookies.update(rs.cookies)
            #return r
        except Exception as e:
            pprint.pprint(body)
            raise e

    def query_tokens (self, cookies, meta = 'tokens'):
        action = 'query'

        params = {
            'format' : 'json',
            'type' : 'csrf', #|deleteglobalaccount|patrol|rollback|setglobalaccountstatus|userrights|watch
            'action' : action,
            'meta' : meta,
        }
        return self.process(self.base_url,params,cookies)


    def get_token(self):
        self.dologin()
        #pprint.pprint(cookies)
        (crsft,cookies2) = query_tokens(self.cookies)
        #pprint.pprint(cookies2)
        edit_cookie = cookies.copy()
        edit_cookie.update(cookies2)
        #pprint.pprint(edit_cookie)
        #pprint.pprint(crsft['query']['tokens'])
        csrftoken = crsft['query']['tokens']['csrftoken']
        self.session.cookie=edit_cookie
        self.session.token =csrftoken


    def query_external (self, euquery, cont = None, namespace=None, _list = 'exturlusage'):
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

        return self.process(params)

    def query_all (self, x):
        lastContinue = {'continue': ''}
    
        while True :
            #print ("#Going to process " + x)
            (r,c) = self.query_external("*."+x, lastContinue, namespace=0)

            count = 0
            if 'query' in r:
                if 'exturlusage' in r['query']:
                    for k in r['query']['exturlusage']:
                        #print (x, k['ns'], k['pageid'], k['title'], k['url'])
                        yield(k)
                        count = count +1
            if count == 0:
                # no new items found
                break
            if 'error' in r: raise Error(r['error'])
            if 'warnings' in r: print(r['warnings'])
            lastContinue = r['continue']
            



class WikidataApi (WikimediaApi ):
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

        return post(self.base_url,params, cookies)

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
        return process(params)

    def wbgetentities_by_id(x):

        params = {
            'action': 'wbgetentities',
            'ids' : x,
            'redirects': 'yes',
            'format' : 'json',
            'props': 'info|sitelinks|aliases|labels|descriptions|claims|datatype'
        }
        return process(params)


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
        return self.post(params, cookie)
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
    pass

if __name__ == "__main__":
    main()
