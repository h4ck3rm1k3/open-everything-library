#!/usr/bin/python3

import pprint 
#import funcs
import re
import pprint
import os
import requests
import os.path
import json
import time
import codecs
import sys

import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

schema = avro.schema.parse(open("avro-schemas/git-hub-projects.avsc", "rb").read())
fn = "data/github/github-projects.avro"
writer = DataFileWriter(open(fn, "wb"), DatumWriter(), schema)

filename_pattern = re.compile(r'repositories\.\d+\.json')
KEYS= [
    u'id',
    u'name',
    u'full_name',
    u'url',
    u'issues_url',
    u'forks_url',
    u'subscription_url',
    u'notifications_url',
    u'collaborators_url',
    u'private',
    u'pulls_url',
    u'issue_comment_url',
    u'labels_url',
    u'owner',
    u'statuses_url',
    u'keys_url',
    u'description',
    u'tags_url',
    u'downloads_url',
    u'assignees_url',
    u'contents_url',
    u'git_refs_url',
    u'git_tags_url',
    u'milestones_url',
    u'languages_url',
    u'fork',
    u'commits_url',
    u'releases_url',
    u'issue_events_url',
    u'archive_url',
    u'comments_url',
    u'events_url',
    u'contributors_url',
    u'html_url',
    u'compare_url',
    u'merges_url',
    u'blobs_url',
    u'git_commits_url',
    u'hooks_url',
    u'teams_url',
    u'trees_url',
    u'branches_url',
    u'subscribers_url',
    u'stargazers_url']
            
def scan_files():
    dirname = 'sources/github/'
    files = os.listdir(dirname)
    
    for y in files:
        #print "Check:" + dirname + y
        if re.match('\d+',y ):
            files2 = os.listdir(dirname + y)
            for x in files2:
                #print "Check:" + dirname + x
                if filename_pattern.match(x):
                    yield dirname + y + "/" + x 


def process_file(fn):
     
    if (os.path.isfile(fn)):
        print("opening",fn)
        f = codecs.open(fn,'r',"utf-8")
        t = f.read()
        d= json.loads(t)
        for x in d:
            n = x['full_name']
            # now we
            #print ("Start:", n)
            y = {
                "id": x['id'],
                "name": x['name'],
                "full_name": x['full_name'],
                #"owner": x['owner']['id'],
                "owner_name": x['owner']['login'],
                "owner_type": x['owner']['type'],
                "html_url": x["html_url"],
                #"url": x["url"],
                "fork": x["fork"],                 
                "description": x["description"],
            }
            writer.append( y        )


def process_files():
    for f in scan_files():
        process_file(f)

process_files()
writer.close()
