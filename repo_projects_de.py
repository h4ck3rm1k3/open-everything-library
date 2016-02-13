#! /usr/bin/python3


import time
import requests
import json
import shelve
import os.path
import pprint
import project_list
import generic_lookup as wapi
BASE_URL='http://de.wikipedia.org/w/api.php'

def projects():
    for p in project_list.plist:
        yield p

def main():
    api = wapi.WikimediaApi(BASE_URL)
    seen = {}
    for p in projects():
        for k in api.query_all(p):
            if k['ns'] == 0:
                if k['title'] not in seen:
                    seen[k['title']] = 1
                    print (k['title'])

if __name__ == "__main__":
    main()

