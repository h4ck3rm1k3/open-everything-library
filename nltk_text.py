#!/usr/bin/python3

# run the nltk over the wikipedia articles
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import nltk

import pymongo
import pprint 
import funcs

c = funcs.Context()
cname = 'Category:'
name = 'Open content'
seen = {}

def process(p):
    _title = p['title']
    _sum = p['summary']
    # sentences
    print ("Parse",_title)
    sents = sent_tokenize(_sum)
    for s in sents :
        #print("\tSent",s)    
        tokens = word_tokenize(s)

        # parts of speech
        pos_tagged = pos_tag(tokens)   

        entities = nltk.chunk.ne_chunk(pos_tagged)


        for sentence in entities:
            if isinstance(sentence, nltk.tree.Tree):
                print("Chec",pprint.pformat(sentence))

           
def recurse(n, p):
    if n not in seen:
        seen[n]=1
    else:
        return
    
    if n not in c.cats.data:
        print ("Missing cat", n)
    else:
        s = c.cats.data[n]
        subcats = s['subcats']
        if subcats:
            for sc in subcats:
                p2 = list(p)
                p2.append(n)
                recurse(sc, p2)

        pages = s['pages']
        if pages:
            for pg in pages:
                p2 = list(p)
                p2.append(n)
                if pg in c.pages.pages.data:
                    text = c.pages.pages.data[pg]
                    process(text)
        # pages
    
#Category:Open Content and all subcats.
recurse(cname + name,[])

