class Context :
    def __init__(self):
        self.wanted_pages ={}
        self.merged_cats = {}
        self.client = pymongo.MongoClient('mongodb://admin:password@127.0.0.1')
        self.db = self.client.open_everything_library
        self.cats   = Wrapper(self.db.categories,"name")
        self.page_data  = Wrapper(
            self.db.page_data,
            "title",
            alt_fields=['name'])
        self.redirs = Wrapper(self.db.redirs,"from")
        self.extern = BigWrapper(self.db.external_pages,"url")
        self.pages = PageWrapper(self.page_data, self.redirs)
        self.wikidata = BigWrapper(self.db.wiki_data, "__subject__")

        self.github = BigWrapper(self.db.github,"full_name")
        self.ruby = BigWrapper(self.db.ruby,"name")

        self.npm = BigWrapper(self.db.npm,"id")
        self.fsd = BigWrapper(self.db.fsd,"__source__")


    def add_cat(self, n, p):
        print("add:",n, "Parents:", ",".join(p))
        _pages = pages(n)
        #pprint.pprint(_pages)

        #n = n.replace( "Category:","")
        subcats = subcat(n)
        #pprint.pprint(subcats)

        new = {
            'name' : n,
            'parents' : p,
            'subcats': subcats,
            'pages': _pages,
        }
        #pprint.pprint(new)
        self.cats.add(n , new)

