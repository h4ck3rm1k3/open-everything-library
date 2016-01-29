import pprint
seen = {}

def WikipediaResultSubcat(n,d):
    seen[ n] = 1
    for x in d['query']['categorymembers']:
        t =  x['title']
        if  t not in seen :
            print  t
        seen[ t ] = 1
                
def process():
    #### sub file, name
    f = open("data/results_Subcat.py")
    c = ""
    count = 0
    for l in f.readlines():
        #l = f.read();
        if "WikipediaResultSubcat" in l:
            if count > 0 : # dont eval first line

                #print "Eval:" + c
                d = eval (c)
            count = count + 1

            c = l
        else:
            c = c + l        
    f.close()
