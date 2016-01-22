import rdflib
from rdflib import URIRef, Graph, Namespace
from rdflib.plugins.parsers.notation3 import N3Parser

g = Graph()

f = open("directory.ttl")

ctx = []

predicates = {}

def parse(d):
  result = g.parse(data=d, format="turtle")
  for s,p,o in g:
    #print s,p,o
    sp = str(p)
    if sp not in predicates:
      #print sp;
      predicates[sp] = 1
    else:
      predicates[sp] = predicates[sp]+1

state = 0

for l in f.readlines():
  #print "Check:" + str(state) + ":"+ l
  if l.startswith("@"):
    continue

  elif l.startswith("<"):
    # next item
    d= "\n".join(ctx)
    print "Parse" + d
    parse(d)
    ctx=[l]
        
  else :
    #print "TODO",l
    #pass
    ctx.append(l)

