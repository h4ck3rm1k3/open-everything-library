import sys
sys.path.append('../Wikipedia/')# #git clone git@github.com:goldsmith/Wikipedia.git
sys.path.append('../beautifulsoup4-4.4.1/build/lib')
import wikipedia
import time
# fetch a page from wp and store in the database
def fetch_page(x, pages, redirs):
    x = x.replace("Category:Category:","Category:")

    if x in  pages.data:
        print("Wait, we have this:" + x)
        return pages.data[x]

    print("loading from WP:" + x)
    print(( "#" + x))
    #try :
    c = None
    #pprint.pprint(redirs.data)
    if x in redirs.data:
        r = redirs.data[x] # redirect
        print("reusing the redirect", x, "to ",  r)
        x = r

    try :
        results = wikipedia.page(x, auto_suggest=False, redirect=False)
        c = results.content
    except wikipedia.exceptions.RedirectError as r:
        r = r.redirect
        print("got redirect", r)
        redirs.db.insert({ "from":  x, "to": r })
        redirs.data[x]=r
        if r not in pages.data:
            results = wikipedia.page(r, auto_suggest=False, redirect=False)
        else:
            return pages.data[r]

    except requests.exceptions.ReadTimeout as e:
        print("Timeout", x)
        return

    #d = pprint.pformat(results.content)
    #pprint.pprint(results.__dict__)
    #pprint.pprint(dir(results))
    o = {
        'name' : x,
        'content': c,
        'categories' : results.categories,
        #'coordinates' : results.coordinates(),
        'images' : results.images,
        'images' : results.images,
        'links' : results.links,
        'original_title' : results.original_title,
        'pageid' : results.original_title,
        'references' : results.references,
        'revision_id' :results.revision_id,
        #'section' :results.section,
        'sections' :results.sections,
        'summary' :results.summary,
        'title': results.title,
        'url' : results.url,
    }
    #pprint.pprint(o)

    #d = json.dumps(o)
    #r = pages.db.insert(o)
    pages.data[x]=o # cache
    #print("after insert", r)
    #except Exception as e:
    #    print "error:", e

    print("zzz")
    time.sleep(1)
