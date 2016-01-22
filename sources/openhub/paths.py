#!/usr/bin/python
import lxml
from lxml.html import  html5parser
#import sys
import getopt
import pprint
import sys
from lxml import etree
#optlist, args = getopt.getopt(sys.argv[1:], 't',['template='])
#pprint.pprint(optlist)
#pprint.pprint(args)
fn = sys.argv[1]
print "File in",fn
o = html5parser.parse(fn)
#pprint.pprint(o)

#NS="{http://www.w3.org/1999/xhtml}"
NS="{html}"
def clean(t):
    return t.replace('{http://www.w3.org/1999/xhtml}','')

def crit(a):
    c = []

    for k in a:
        if k in ('capture','follow'):
            pass
        else:
            v = a[k]
            c.append("@" + k + "=" + "'" + v + "'")

    return "[" + " and ".join(c) + "]"


def context(x):
    p = x.getparent()
    if p:
        return context(x.getparent()) + "/"+ clean(x.tag) + crit(x.attrib)
    else:
        return clean(x.tag)

def paths(doc, xpath):
    #print "Check",xpath
    r = doc.xpath(
        xpath,
        namespaces={
            'html': 'http://www.w3.org/1999/xhtml'
        }
    )
    return r

for x in paths(o,
               "//html:div[@class='well searchable']"
               #"//{ns}:div[@class='well searchable']".format(ns=NS)
               #"/html/body[@zoom='1']/div[@id='page' and @class='container']/div[@id='page-contents']/div[@id='projects_index_page' and @class='col-md-12']/div[@id='projects_index_list']/div[@id='project_341570' and @class='well searchable']"
):
    print "\n\nFOUND"
    for keywords in paths(
            x,
            ".//html:div[@class='tags']/html:a[@href and @class='tag' and @itemprop='keywords']"
    ):
        print "\t","Keywords", keywords.text


    for lang in paths(
            x,
        ".//html:div[@class='add-info']/html:div[@class='main_language pull-left']/html:span"
    ):
        print "\t","Lang:",lang.text


    for changedate in paths(x,
                            ".//html:div[@class='info pull-left']/html:p/i/html:abbr[@class='date']"): #and @title
        print "\t","Changedate:",etree.tostring(changedate)

    for lic in paths(
            x,
            ".//html:div[@class='add-info']/html:div[@class='licenses pull-right']/html:span"
    ):
        print "\t","License:",lic.text
            
    for content in paths(x,
                      "./html:div[@id='inner_content' and @class='pull-left']"):
            
        for heading in paths(content,
                         "./html:h2[@class='title pull-left']"):                        
                 
            for title in paths(heading,
                               "./html:a"):
                print "\t","project.href",title.attrib['href']
                print "\t","project.title", title.attrib['title']           

        for summary in paths(content,
                             "./html:div[@class='info pull-left']/html:div[@class='desc']/html:span[@style='display: inline' and @id and @class='proj_desc_toggle']"):
            print "\t","Summary:",summary.text.replace("\n"," ")

        for desc in paths(content,
                          "./html:div[@class='info pull-left']/html:div[@class='desc']/html:span[@style='display: none' and @id and @class='proj_desc_toggle']"
                          ):
            print "\t","Desc", desc.text.replace("\n"," ")

        for something in paths(
                content,
                "./html:div[@class='stats pull-left']/html:p" #/html:a[@href]
        ):
            print "\t", something[1].text,":",something[0].text

        for reviews in paths(
                content,
                "./html:div[@class='reviews-and-pai pull-left']"
        ):
            #print "\t","reviews:",etree.tostring(reviews)
            #print "\t", something[1].text,":",something[0].text

            for reviews2 in paths(
                    reviews,
                    "./html:div[@class='reviews']/html:a[@href]"):
                print "\t","Reviews:",reviews2.text


            for act in paths(
                    reviews,
                    "./html:div[@class='twentyfive_project_activity_text']"):
                print "\t","activity:",act.text

            for rat in paths(
                    reviews,
                    ".//html:span[@itemprop='ratingValue']"):
                print "\t","rating:",rat.text

                
